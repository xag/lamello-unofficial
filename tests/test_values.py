"""The values against the page they were read from, and the data against furniture-design's
rules.

The page is copyrighted, so its copy lives in the private repo xag/furniture, checked out
beside this one (or at $FURNITURE_REPO). Without it the check of the values cannot run, and
it fails saying so rather than passing.
"""

import os
import re
from pathlib import Path

import pytest
from quern import Quern, run_rules
from quern.provenance import Quantity
from quern.tree import Node

from furniture_design.knowledge import knowledge as general, merge
from furniture_design.package import PACKAGE
from lamello_unofficial import CLAMEX_P_14, SETTING, knowledge

ROOT = Path(__file__).resolve().parents[1]
CAPTURE = Path(os.environ.get("FURNITURE_REPO", ROOT.parent / "furniture")) / \
    "sources/lamello/clamex-p-14.fr.txt"


def test_every_value_is_the_pages_in_the_pages_order():
    assert CAPTURE.exists(), (f"the private copy of the page is not at {CAPTURE}: clone "
                              "xag/furniture beside this repo or set FURNITURE_REPO")
    text = CAPTURE.read_text(encoding="utf-8")
    table = text[text.index("Données techniques"):]
    # the table's rows end in a value and a unit; tolerances (±) and the size are not limits
    rows = [(float(v.replace(" ", "")), u) for v, u in
            re.findall(r"\t(\d[\d ]*)\s*(mm|N)\s*$", table, flags=re.M)]
    assert rows == [(float(v), u) for _, v, u, _ in CLAMEX_P_14]
    assert re.search(rf"\t{re.escape(SETTING)}\s*$", table, flags=re.M)


def _tree(*extra: Node) -> Quern:
    tree = Quern(vocabulary=PACKAGE.vocabulary, rules=PACKAGE.rules, solvers=PACKAGE.solvers)
    tree.root.children = merge(general(), knowledge()) + list(extra)
    return tree


def test_the_data_passes_furniture_designs_rules():
    assert [(r.rule, r.node, r.verdict) for r in run_rules(_tree()) if not r.ok] == []


def test_no_clause_here_carries_a_quote():
    sources = knowledge()[0].children
    assert all(s.payload["licence"] == "copyrighted" for s in sources)
    assert all("quote" not in c.payload for s in sources for c in s.children)


def _box(thickness: float, cut: str = "surface", tool: str = "tools/lamello-zeta-p2") -> Node:
    def side(id_: str) -> Node:
        q = lambda v: Quantity(value=v, unit="mm", provenance="design-target", grounded=False)  # noqa: E731
        return Node(id=id_, kind="part", links={"uses": ["materials/birch-yellow"]},
                    params={"width": q(300), "thickness": q(thickness)},
                    payload={"shape": {"op": "box", "size": ["thickness", "width", 400]}})
    joint = Node(id="corner", kind="joint", payload={"cut": cut, "setting": SETTING},
                 links={"joins": ["pieces/box/left", "pieces/box/top"],
                        "uses": ["connectors/lamello-clamex-p-14"], "made_with": [tool]})
    return Node(id="pieces", kind="", children=[
        Node(id="box", kind="piece", children=[side("left"), side("top"), joint])])


@pytest.mark.parametrize("thickness,cut,holds", [
    (18, "surface", True), (15, "surface", True), (14, "surface", False),
    (18, "mitre", True), (16, "mitre", False), (12, "edge", True), (28, "intermediate", False)])
def test_a_clamex_joint_is_judged_by_the_pages_limits(thickness, cut, holds):
    results = [r for r in run_rules(_tree(_box(thickness, cut)))
               if r.rule == "a-joined-part-is-thick-enough-for-the-cut"]
    assert results and all(r.ok == holds for r in results)


def test_a_clamex_seat_is_cut_with_the_zeta_p2_or_a_cnc():
    for tool, holds in [("tools/lamello-zeta-p2", True), ("tools/cnc-with-p-system-cutter", True)]:
        r = [r for r in run_rules(_tree(_box(18, tool=tool)))
             if r.rule == "a-joint-is-cut-with-a-tool-its-connector-takes"]
        assert r and all(x.ok == holds for x in r)
