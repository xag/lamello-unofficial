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
                 params={name: _published(v, unit, label) for name, v, unit, label in CLAMEX_P_14}),
            Node(id="product-description", kind="clause",
                 payload={"locator": "product description (Description du produit)",
                          "in_our_words": "the P-System groove is cut with the Zeta P2 groove "
                                          "cutter or a CNC machine"}),
        ])


def connectors() -> Node:
    params = {name: Quantity(value=float(v), unit=unit, provenance="derived", grounded=True,
                             derived_from=[f"{TECHNICAL_DATA}/{name}"], note=label)
              for name, v, unit, label in CLAMEX_P_14}
    clamex = Node(id="lamello-clamex-p-14", kind="connector", name="Lamello Clamex P-14",
                  payload={"maker": "Lamello", "setting": SETTING,
                           "kind_of_connector": "knock-down furniture connector seated in a "
                                                "P-System groove, closed with a lever through "
                                                "a 6 mm access hole"},
                  params=params,
                  links={"needs": ["tools/lamello-zeta-p2", "tools/cnc-with-p-system-cutter"],
                         "per": [TECHNICAL_DATA, DESCRIPTION]})
    return Node(id="connectors", kind="", children=[clamex])


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
    return [Node(id="sources", kind="", children=[source()]), connectors(), tools()]
