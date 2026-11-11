"""Lamello's connectors and the tools that cut their seats, as data on furniture-design's
kinds (connector, tool, source, clause). Unofficial: Lamello neither wrote nor endorsed it.

Lamello's pages are copyrighted, so every clause here carries its locator and the values
it states, and no quote (furniture-design ledger:
a-copyrighted-source-is-cited-by-locator-and-values). The page as fetched is kept in the
private repo xag/furniture, and tests/test_values.py checks every value against it.

    from furniture_design.knowledge import knowledge as general, merge, mount
    from lamello_unofficial import knowledge as lamello
    tree.root.children.append(mount(merge(general(), lamello()), "knowledge"))

A joint then `uses` connectors/lamello-clamex-p-14 and is `made_with`
tools/lamello-zeta-p2, and furniture-design's rules check it.
"""

from __future__ import annotations

from quern.provenance import Quantity
from quern.tree import Node

SOURCE = "sources/lamello-clamex-p-14"
TECHNICAL_DATA = f"{SOURCE}/technical-data"
DESCRIPTION = f"{SOURCE}/product-description"

# The technical data table of the Clamex P-14 page, as fetched on 2026-11-11, in the
# order its rows appear there: (param, value, unit, what the row gives, in our words)
CLAMEX_P_14 = [
    ("min_width", 75, "mm", "narrowest workpiece"),
    ("min_thickness_edge", 12, "mm", "thinnest material for an edge cut"),
    ("min_thickness_surface", 15, "mm", "thinnest material for a surface cut"),
    ("min_thickness_intermediate", 29, "mm", "thinnest material for an intermediate upright"),
    ("min_thickness_mitre", 18, "mm", "thinnest material for a mitre"),
    ("pull_out_particleboard", 1070, "N", "pull-out strength in particle board"),
    ("pull_out_mdf", 1210, "N", "pull-out strength in MDF"),
    ("pull_out_beech", 1870, "N", "pull-out strength in beech"),
    ("shear_particleboard", 490, "N", "shear strength in particle board"),
    ("shear_mdf", 600, "N", "shear strength in MDF"),
    ("shear_beech", 2940, "N", "shear strength in beech"),
]
SETTING = "P-14"  # the P-System setting its groove is cut at
# The table's size row, "Taille (L x H x I)": length, height, thickness, in that order, mm.
# furniture-design draws a connector at its length along the joint and thickness across it.
CLAMEX_P_14_SIZE = [("length", 64), ("height", 27), ("thickness", 9.7)]


def _published(value: float, unit: str, label: str) -> Quantity:
    return Quantity(value=float(value), unit=unit, provenance="published", grounded=True,
                    source="technical data table", note=label)


def source() -> Node:
    return Node(
        id="lamello-clamex-p-14", kind="source", name="Lamello, Clamex P-14 product page",
        payload={"publisher": "Lamello AG", "year": 2026,
                 "url": "https://lamello.com/fr/produits/p-system/clamex-p-14",
                 "fetched": "2026-11-11, in a browser; the English address redirects here",
                 "sha256": "30effaf917c3d6276c5bcaecb45c3aad26f443b41f157b472e6a6ad4fa81ed58",
                 "licence": "copyrighted",
                 "capture": "xag/furniture: sources/lamello/clamex-p-14.fr.html (private)"},
        children=[
            Node(id="technical-data", kind="clause",
                 payload={"locator": "technical data table (Données techniques)",
                          "setting": SETTING},
                 params={**{name: _published(v, unit, label) for name, v, unit, label in CLAMEX_P_14},
                         **{name: _published(v, "mm", f"size (L x H x I), {name}")
                            for name, v in CLAMEX_P_14_SIZE}}),
            Node(id="product-description", kind="clause",
                 payload={"locator": "product description (Description du produit)",
                          "in_our_words": "the P-System groove is cut with the Zeta P2 groove "
                                          "cutter or a CNC machine"}),
        ])


def connectors() -> Node:
    params = {name: Quantity(value=float(v), unit=unit, provenance="derived", grounded=True,
                             derived_from=[f"{TECHNICAL_DATA}/{name}"], note=label)
              for name, v, unit, label in CLAMEX_P_14}
    params.update({name: Quantity(value=float(v), unit="mm", provenance="derived", grounded=True,
                                  derived_from=[f"{TECHNICAL_DATA}/{name}"],
                                  note=f"size (L x H x I), {name}")
                   for name, v in CLAMEX_P_14_SIZE})
    clamex = Node(id="lamello-clamex-p-14", kind="connector", name="Lamello Clamex P-14",
                  payload={"maker": "Lamello", "setting": SETTING,
                           "kind_of_connector": "knock-down furniture connector seated in a "
                                                "P-System groove, closed with a lever through "
                                                "a 6 mm access hole"},
                  params=params,
                  links={"needs": ["tools/lamello-zeta-p2", "tools/cnc-with-p-system-cutter"],
                         "per": [TECHNICAL_DATA, DESCRIPTION, STUDY_RESULT,
                                 f"{STUDY}/specimens", f"{STUDY}/table-1-specimen-a"]})
    # a corner joint's resistance to being bent open or shut, per connector: the study's
    # joint of two connectors, halved; in N mm and N mm/rad, the units the checks use
    for name, v, unit, words in L_JOINT:
        si = v * 1000.0
        clamex.params[f"{name}_particleboard"] = Quantity(
            value=si / STUDY_JOINT_CONNECTORS, unit=unit.replace("N m", "N mm"),
            provenance="derived", grounded=True,
            derived_from=[f"{STUDY_RESULT}/{name}", f"{STUDY}/table-1-specimen-a/connectors"],
            note=f"{words} for an L-joint of 18 mm particle board with two connectors, halved; "
                 "measured with an ABS edge band, 400 mm long")
    return Node(id="connectors", kind="", children=[clamex])


STUDY = "sources/janikova-2025"
STUDY_RESULT = f"{STUDY}/clamex-p-14-l-joint"
STUDY_JOINT_CONNECTORS = 2  # Table 1: specimen A is joined by 2 pcs Clamex P-14

# What specimen A (an L-shaped corner of 18 mm particle board, 400 mm long, two Clamex
# P-14) held in angular bending, per joint: (param, value, unit, the words it is in)
L_JOINT = [
    ("moment_opening", 9.0, "N m", "9 Nm (tension)"),
    ("moment_closing", 15.0, "N m", "15 Nm (compression)"),
    ("stiffness_opening", 55.0, "N m/rad", "55 Nm/rad (tension)"),
    ("stiffness_closing", 237.0, "N m/rad", "237 Nm/rad (compression)"),
]


def study() -> Node:
    """A study of the Clamex P-14 as a corner joint: CC BY, so quoted and kept here."""
    q = lambda v, unit, note: Quantity(value=v, unit=unit, provenance="published",  # noqa: E731
                                       grounded=True, source="Results and discussion",
                                       note=note)
    return Node(
        id="janikova-2025", kind="source",
        name="Janíková, Kořený, Gaff, Hlavatý: Comparative Study on Strengths of "
             "Ready-to-Assemble and Eccentric Furniture Joint, Materials 18(9), 2114 (2025)",
        payload={"publisher": "MDPI", "year": 2025, "identifier": "doi:10.3390/ma18092114",
                 "url": "https://www.mdpi.com/1996-1944/18/9/2114",
                 "sha256": "a52aa32ebe67a9b8ff4d8b9d6b4c382605e42eced6bb8a8f5e0ae8c90afd1ad4",
                 "licence": "cc-by-4.0",
                 "capture": "sources/janikova-2025/ma18092114.txt"},
        children=[
            Node(id="specimens", kind="clause",
                 payload={"locator": "2. Materials and Methods",
                          "quote": "Twenty replicates of each type of L-specimen were made with "
                                   "dimensions of 150 × 150 × 400 mm. The face and rear members "
                                   "were joined at a 90° angle. The base material was a "
                                   "three-layer particleboard (producer: DDL Lukapol from "
                                   "Slovakia; basic with lamination; 18 mm thickness)."},
                 params={"joint_length": Quantity(value=400.0, unit="mm", provenance="published",
                                                  grounded=True, note="150 × 150 × 400 mm"),
                         "thickness": Quantity(value=18.0, unit="mm", provenance="published",
                                               grounded=True, note="18 mm thickness")}),
            Node(id="table-1-specimen-a", kind="clause",
                 payload={"locator": "Table 1, specimen A", "quote": "2 pcs Clamex P-14"},
                 params={"connectors": Quantity(value=2.0, unit="", provenance="published",
                                                grounded=True, note="2 pcs")}),
            Node(id="clamex-p-14-l-joint", kind="clause",
                 payload={"locator": "Results and discussion, specimen A",
                          "quote": "the tested joint A achieved average values of 9 Nm "
                                   "(tension), 15 Nm (compression), a stiffness of 55 Nm/rad "
                                   "(tension), and 237 Nm/rad (compression) in the bending "
                                   "tests in the angular plane"},
                 params={name: q(v, unit, words) for name, v, unit, words in L_JOINT}),
        ])


def tools() -> Node:
    return Node(id="tools", kind="", children=[
        Node(id="lamello-zeta-p2", kind="tool", name="Lamello Zeta P2",
             payload={"maker": "Lamello", "does": "cuts the P-System groove"},
             links={"per": [DESCRIPTION]}),
        Node(id="cnc-with-p-system-cutter", kind="tool", name="CNC machine with a P-System cutter",
             payload={"maker": "any", "does": "cuts the P-System groove"},
             links={"per": [DESCRIPTION]}),
    ])


def knowledge() -> list[Node]:
    """Top-level branches to merge with furniture-design's: sources, connectors, tools."""
    return [Node(id="sources", kind="", children=[source(), study()]), connectors(), tools()]
