"""Tests of other Clamex sizes (Saar 2015, Sydor 2019) and Lamello's archived ratings of the
P-15 beside the P-14's: every value against the private copy it was read from, and the rules
that keep them off the P-14 (ledger: another-clamex-sizes-test-stands-in-only-below-the-p-14s-
rating, a-bending-test-in-an-unnamed-direction-is-never-rated).

The copies live in the private repo xag/furniture, under sources/lamello/<source id>/, beside
this repo or at $FURNITURE_REPO. Without them the checks fail, never skip.
"""

import hashlib
import os
import re
from pathlib import Path

import pytest
from quern.provenance import Quantity

from lamello_unofficial import P_14_2014, P_15_2013, knowledge

ROOT = Path(__file__).resolve().parents[1]
FURNITURE = Path(os.environ.get("FURNITURE_REPO", ROOT.parent / "furniture"))
NEW = ["saar-2015", "sydor-2019", P_15_2013[0], P_14_2014[0]]


def _sources() -> dict:
    return {s.id: s for s in knowledge()[0].children}


def _copy(source) -> Path:
    capture = source.payload["capture"]
    m = re.fullmatch(r"xag/furniture: (\S+) \(private\)", capture)
    assert m, f"{source.id}: capture {capture!r} names no copy in xag/furniture"
    path = FURNITURE / m.group(1)
    assert path.exists(), (f"the private copy of {source.id} is not at {path}: clone "
                           "xag/furniture beside this repo or set FURNITURE_REPO")
    return path


def _text(source) -> str:
    raw = _copy(source).with_suffix(".txt").read_bytes()
    try:
        return raw.decode("utf-8")
    except UnicodeDecodeError:
        return raw.decode("latin-1")  # the PDFs' text was extracted as ISO-8859-1


def _num(s: str) -> float:
    return {"two": 2.0}.get(s, None) or float(s)


def _saar(text: str) -> dict:
    """{clause id: {param: value}} as Saar et al. print them."""
    t1 = text[text.index("Table 1. Tensile"):text.index("Table 2. Shear")]
    t2 = text[text.index("Table 2. Shear"):]
    out = {"specimens": {
        "thickness": _num(re.search(r"made of (\d+) mm thick birch plywood", text)[1]),
        "specimens": _num(re.search(r"Both tests contained (\d+) specimens", text)[1])}}
    for cid, table, mode, row in [("table-1-clamex-p-15", t1, "pull_out", "P15"),
                                  ("table-1-clamex-p-10", t1, "pull_out", "P10"),
                                  ("table-2-clamex-p-15", t2, "shear", "P15"),
                                  ("table-2-clamex-p-10", t2, "shear", "P10")]:
        m = re.search(rf"Clamex {row}\s+(\d+\.\d+) \S (\d+\.\d+)", table)
        out[cid] = {mode: _num(m[1]), f"{mode}_sd": _num(m[2])}
    return out


def _sydor(text: str) -> dict:
    """{clause id: {param: value}} as Sydor & Pohl print them; the boards' thickness is
    drawn in Figure 3 and is not in the text, so it is checked by eye (see below)."""
    assert "The force for all samples\nwas exerted only in one direction (up)" in \
        text.replace("\r\n", "\n")
    table = text[text.index("Table 2. Rigidity"):text.index("Rastex  Particleboard")]
    out = {"samples": {
        "fasteners": _num(re.search(r"Each sample contained (two) 128 mm", text)[1]),
        "spacing": _num(re.search(r"contained two (\d+) mm\s+fasteners apart", text)[1]),
        "samples": _num(re.search(r"resulted in (\d+) aggregate characteristics", text)[1])}}
    for cid, label, board in [("table-2-clamex-plywood", "Plywood", "hardwood plywood"),
                              ("table-2-clamex-oak-glued", r"Oak \(glued\)", "glued oak wood board"),
                              ("table-2-clamex-pine-glued", r"Pine \(glued\)", "glued pine wood board")]:
        m = re.search(rf"{label}\s+(\d\.\d+)\s+\d+%\s+(\d+\.\d+)\s+(\d+\.\d+)\s+(\d+\.\d+)", table)
        out[cid] = {"stiffness": _num(m[1]) * 1000, "moment_max": _num(m[2]),
                    "moment_max_sd": _num(m[3]), "moment_at_50_mrad": _num(m[4]),
                    "density": _num(re.search(rf"{board} of (\d+) kg/m3", text)[1])}
    return out


def _lamello(text: str) -> dict:
    # the page puts a non-breaking character between a number and its unit
    m = re.search(r"Tensile strength:\s*Particle board\s*~ (\d+)\W?N[^\n]*\s*Beech\s*~ (\d+)\W?N",
                  text)
    return {"technical-data": {"pull_out_particleboard": _num(m[1]),
                               "pull_out_beech": _num(m[2])},
            "description": {"installation_depth":
                            _num(re.search(r"installation depth of (\d+) mm", text)[1])}}


READ = {"saar-2015": _saar, "sydor-2019": _sydor, P_15_2013[0]: _lamello, P_14_2014[0]: _lamello}
# Values no text extraction holds, with the reason each was read another way
BY_EYE = {("sydor-2019", "samples", "thickness"):
          "drawn as 18 in Figure 3 (p. 40), both boards; read from the rendered page"}


@pytest.mark.parametrize("sid", NEW)
def test_each_copy_is_what_was_fetched(sid):
    source = _sources()[sid]
    assert hashlib.sha256(_copy(source).read_bytes()).hexdigest() == source.payload["sha256"]


@pytest.mark.parametrize("sid", NEW)
def test_every_value_is_in_its_copy_and_every_printed_one_is_here(sid):
    """Each clause's params are exactly what the copy prints: no value missing, none added."""
    source = _sources()[sid]
    printed = READ[sid](_text(source))
    for clause in source.children:
        ours = {k: q.value for k, q in clause.params.items()
                if (sid, clause.id, k) not in BY_EYE}
        assert ours == pytest.approx(printed.get(clause.id, {})), clause.id


def test_the_p14_is_called_the_new_generation_on_its_2014_page():
    assert "Clamex P-14, the new generation" in _text(_sources()[P_14_2014[0]])


def test_no_clause_of_a_source_that_may_not_be_quoted_carries_a_quote():
    for sid in NEW:
        source = _sources()[sid]
        assert source.payload["licence"] in ("copyrighted", "unstated")
        assert all("quote" not in c.payload for c in source.children), sid


def _clauses(nodes) -> dict:
    """{clause path: (clause, its source)} in a knowledge()."""
    return {f"sources/{s.id}/{c.id}": (c, s) for s in nodes[0].children for c in s.children}


def _borrowed_and_grounded(nodes) -> list[str]:
    """Each connector param read from a clause about another connector that is grounded, or
    whose note does not name the connector it was measured on; and each param read from a
    clause that names no connector."""
    clauses, bad = _clauses(nodes), []
    for c in nodes[1].children:
        for name, q in c.params.items():
            for d in q.derived_from or []:
                clause, source = clauses[d.rsplit("/", 1)[0]]
                measured_on = clause.payload.get("connector") or source.payload.get("connector")
                if not measured_on:
                    bad.append(f"{c.id}.{name}: {d} names no connector")
                elif measured_on != c.name and (q.grounded or measured_on not in (q.note or "")):
                    bad.append(f"{c.id}.{name}: borrowed from {measured_on}")
    return bad


def test_a_borrowed_value_is_never_grounded():
    assert _borrowed_and_grounded(knowledge()) == []
    # and the check sees one: a P-15 value standing in for the P-14's
    nodes = knowledge()
    clamex = nodes[1].children[0]
    borrowed = Quantity(value=2512.18, unit="N", provenance="derived", grounded=True,
                        derived_from=["sources/saar-2015/table-2-clamex-p-15/shear"],
                        note="Lamello Clamex P-15's, in 21 mm birch plywood")
    clamex.params["shear_plywood"] = borrowed
    assert _borrowed_and_grounded(nodes) == ["lamello-clamex-p-14.shear_plywood: borrowed from "
                                             "Lamello Clamex P-15"]
    clamex.params["shear_plywood"] = borrowed.model_copy(update={"grounded": False})
    assert _borrowed_and_grounded(nodes) == []


def test_the_p15_stands_in_for_nothing_while_lamello_rates_it_above_the_p14():
    p15 = _sources()[P_15_2013[0]].children[0].params
    p14 = _sources()[P_14_2014[0]].children[0].params
    above = [k for k in p15.keys() & p14.keys() if p15[k].value > p14[k].value]
    assert above == ["pull_out_beech"]
    clauses = _clauses(knowledge())
    clamex = knowledge()[1].children[0]
    for name, q in clamex.params.items():
        for d in q.derived_from or []:
            clause, source = clauses[d.rsplit("/", 1)[0]]
            assert (clause.payload.get("connector") or source.payload.get("connector")) \
                != "Lamello Clamex P-15", name


def test_a_test_kept_elsewhere_is_a_clause_and_rates_nothing():
    clauses = _clauses(knowledge())
    clamex = knowledge()[1].children[0]
    listed = [t["clause"] for t in clamex.payload["tested_elsewhere"]]
    assert listed and all(p in clauses for p in listed)
    assert all(t["what"] and t["not_rated_because"] for t in clamex.payload["tested_elsewhere"])
    read = {d.rsplit("/", 1)[0] for q in clamex.params.values() for d in q.derived_from or []}
    assert not read & set(listed)
    # so the P-14 states strengths only where Lamello and Janíková rate it, and a check of a
    # plywood, oak or pine piece stays unjudged
    rated = {re.sub(r"^(shear|pull_out|moment_opening|moment_closing|stiffness_opening|"
                    r"stiffness_closing)_", "", k) for k in clamex.params
             if re.match(r"(shear|pull_out|moment|stiffness)_", k)}
    assert rated == {"particleboard", "mdf", "beech"}
