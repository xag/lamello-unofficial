"""The Zeta P2, its drill jig and the Clamex P-14's access hole: every value against the copy it was
read from, and the grooves and holes of a corner joint as the assembly instructions give them.

The copies are Lamello's, copyrighted, kept in the private repo xag/furniture beside this one (or at
$FURNITURE_REPO); without them these tests fail, saying where they looked.
"""

import hashlib
import os
import re
from pathlib import Path

from quern import Quern, run_rules
from quern.provenance import Quantity
from quern.tree import Node

from furniture_design.knowledge import knowledge as general, merge
from furniture_design.package import PACKAGE
from furniture_design.scene import scene, seats
from lamello_unofficial import BROCHURE_DOC, VIDEO_DOC, ZETA_DOCS, knowledge

ROOT = Path(__file__).resolve().parents[1]
FURNITURE = Path(os.environ.get("FURNITURE_REPO", ROOT.parent / "furniture"))


def _copy(rel: str) -> Path:
    path = FURNITURE / rel
    assert path.exists(), (f"the private copy {path} is missing: clone xag/furniture beside this repo or "
                           "set FURNITURE_REPO")
    return path


def _flat(text: str) -> str:
    return re.sub(r"\s+", " ", text)


def test_every_value_of_the_zeta_p2s_documents_is_printed_in_the_copy_fetched():
    for sid, _name, _url, sha, copy, clauses in [*ZETA_DOCS, BROCHURE_DOC]:
        path = _copy(copy)
        assert hashlib.sha256(path.read_bytes()).hexdigest() == sha, sid
        text = _flat(path.with_suffix(".txt").read_text(encoding="utf-8"))
        for cid, _locator, params in clauses:
            for param, (_value, _unit, printed) in params.items():
                assert _flat(printed) in text, (sid, cid, param, printed)


def test_every_passage_of_lamellos_video_is_in_the_account_kept():
    """The video is cited from the account Gemini gave of it, kept privately by its YouTube id."""
    sid, _name, url, sha, clauses = VIDEO_DOC
    path = _copy(f"sources/videos/{url.rsplit('=', 1)[1]}.md")
    assert hashlib.sha256(path.read_bytes()).hexdigest() == sha
    text = path.read_text(encoding="utf-8")
    for cid, _locator, words in clauses:
        for w in words:
            assert w in text, (cid, w)


def test_the_access_holes_values_are_printed_on_the_clamex_p14_sheet():
    sheet = next(s for s in knowledge()[0].children if s.id == "lamello-clamex-p-14-instructions")
    path = _copy("sources/lamello/zeta-p2/Operating_instructions_Clamex_P14.pdf")
    assert hashlib.sha256(path.read_bytes()).hexdigest() == sheet.payload["sha256"]
    text = _flat(path.with_suffix(".txt").read_text(encoding="utf-8"))
    clause = next(c for c in sheet.children if c.id == "groove-and-hole")
    for param, printed in clause.payload["printed"].items():
        assert printed in text, (param, printed)
    assert {k: q.value for k, q in clause.params.items()} == {"access_hole_offset": 7.5, "access_hole_diameter": 6}


def _tools() -> dict:
    return {n.id: n for n in knowledge()[2].children}


def test_the_zeta_p2_follows_the_general_jointer_and_states_its_offset_and_spacers():
    zeta = _tools()["lamello-zeta-p2"]
    assert zeta.links["follows"] == ["tools/plate-jointer"]
    assert zeta.params["groove_offset"].value == 10 and zeta.params["groove_offset"].derived_from == [
        "sources/lamello-machining-with-power-tools/equal-distance/groove_offset"]
    assert zeta.payload["spacers_mm"] == [2.0, 4.0]
    for lang in ("fr", "en"):
        assert len(zeta.payload["say"][lang]["method"]) == 7
    clamex = next(c for c in knowledge()[1].children if c.id == "lamello-clamex-p-14")
    assert clamex.links["drilled_with"] == ["tools/lamello-clamex-p-drill-jig"]
    assert {k: clamex.params[k].value for k in ("access_hole_diameter", "access_hole_offset",
                                                "min_end_distance", "max_spacing")} == \
        {"access_hole_diameter": 6, "access_hole_offset": 7.5, "min_end_distance": 37, "max_spacing": 300}


def _corner(thickness: float) -> Quern:
    """A top resting on a side, flush with its outside, joined by two Clamex P-14 cut with the Zeta P2."""
    def part(id_, size, at):
        return Node(id=id_, kind="part", links={"uses": ["materials/birch-yellow"]},
                    payload={"shape": {"op": "box", "size": size}, "transform": {"translate": at}})
    joint = Node(id="corner", kind="joint", payload={"cut": "surface", "setting": "P-14"},
                 params={"count": Quantity(value=2, unit="", provenance="design-target")},
                 links={"joins": ["pieces/box/top", "pieces/box/side"],
                        "uses": ["connectors/lamello-clamex-p-14"], "made_with": ["tools/lamello-zeta-p2"]})
    box = Node(id="box", kind="piece", children=[part("side", [thickness, 300, 400], [0, 0, 0]),
                                                  part("top", [500, 300, thickness], [0, 0, 400]), joint])
    tree = Quern(vocabulary=PACKAGE.vocabulary, rules=PACKAGE.rules, solvers=PACKAGE.solvers)
    tree.root.children = merge(general(), knowledge()) + [Node(id="pieces", kind="", children=[box])]
    return tree


def test_a_corner_cut_with_the_zeta_p2_is_grooved_10_mm_from_its_outside_and_drilled_inside():
    for thickness, offset in ((18, 10), (16, 8), (20, 10)):
        sc = scene(_corner(thickness), "pieces/box")
        side, top = seats(sc, sc.joints[0])
        assert (side.part, side.reference, side.offset, top.reference) == ("side", "left", offset, "left")
        assert side.hole_side == "right" and side.hole == (6, 7.5)
        assert [m.path for m in sc.joints[0].methods] == [
            "tools/plate-jointer", "tools/lamello-zeta-p2", "tools/lamello-clamex-p-drill-jig"]


def test_the_zeta_p2s_sources_and_tools_break_none_of_furniture_designs_rules():
    tree = _corner(18)
    ours = ("sources/lamello-zeta-p2-manual", "sources/lamello-machining-with-power-tools",
            "sources/lamello-tip-", "tools/lamello-", "connectors/lamello-")
    broken = [(r.rule, r.node) for r in run_rules(tree, "") if not r.ok and r.node.startswith(ours)]
    assert not broken, broken


def test_the_zeta_p2_and_its_jig_are_drawn_from_models_that_hold_lamellos_printed_sizes():
    """The models build into closed solids; the machine's front stop is 120 mm wide (60 + 60) and lies,
    folded flat, 20 mm above the base (10 + 10 to the cutter); the jig's hole is the access hole's
    7.5 mm from the joint face."""
    import numpy as np
    from furniture_design import lineart as la
    tools = _tools()
    model = tools["lamello-zeta-p2"].payload["model"]
    flat = la.solids(model["poses"]["flat"])
    v = np.vstack([m.v for m in flat[:3]])
    assert v[:, 0].max() - v[:, 0].min() == 120 and v[:, 2].min() == 20
    assert len(la.solids(model["parts"])) > 30
    assert {d["shows"] for d in model["dials"]} == {"max", "setting"}
    jig = tools["lamello-clamex-p-drill-jig"].payload["model"]
    clamex = next(c for c in knowledge()[1].children if c.id == "lamello-clamex-p-14")
    assert -jig["hole"][0] == clamex.params["access_hole_offset"].value
    assert tools["lamello-zeta-p2"].params["test_recess"].value == 0.5
