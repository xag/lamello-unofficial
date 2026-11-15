"""Lamello's connectors and the tools that cut their seats, as data on furniture-design's
kinds (connector, tool, source, clause). Unofficial: Lamello neither wrote nor endorsed it.

Lamello's pages are copyrighted, so every clause here carries its locator and the values
it states, and no quote (furniture-design ledger:
a-copyrighted-source-is-cited-by-locator-and-values). The page as fetched is kept in the
private repo xag/furniture, and tests/test_values.py checks every value against it. Tests
of other Clamex sizes (Saar 2015, Sydor 2019) and Lamello's archived P-15 and P-14 pages are
cited the same way, their copies under sources/lamello/<source id>/ there, checked by
tests/test_other_sizes.py; the P-14 lists those tests in `tested_elsewhere` and takes no
value from them.

    from furniture_design.knowledge import knowledge as general, merge, mount
    from lamello_unofficial import knowledge as lamello
    tree.root.children.append(mount(merge(general(), lamello()), "knowledge"))

A joint then `uses` connectors/lamello-clamex-p-14 and is `made_with`
tools/lamello-zeta-p2, and furniture-design's rules check it.
"""

from __future__ import annotations

from quern.provenance import Quantity
from quern.tree import Node
from furniture_design.knowledge import with_authority

from . import models

SOURCE = "sources/lamello-clamex-p-14"
TECHNICAL_DATA = f"{SOURCE}/technical-data"
DESCRIPTION = f"{SOURCE}/product-description"
INSTRUCTIONS = "sources/lamello-clamex-p-14-instructions"
OPEN_AND_CLOSE = f"{INSTRUCTIONS}/open-and-close"

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
                 "licence": "copyrighted", "connector": "Lamello Clamex P-14",
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


def instructions() -> Node:
    """Lamello's instructions for the Clamex P-14 (Mode d'emploi), a two-page sheet of
    figures: how it closes is drawn, not written, so the clause says in our words what the
    figures show and carries no value."""
    return Node(
        id="lamello-clamex-p-14-instructions", kind="source",
        name="Lamello, Clamex P-14 instructions (Mode d'emploi)",
        payload={"publisher": "Lamello AG", "year": 2019,
                 "url": "https://www.lamello.com/fileadmin/products/Mode_d_emploi_ClamexP14.pdf",
                 "fetched": "2026-11-14, linked as Mode d'emploi from the Clamex P-14 page",
                 "sha256": "5b075112b363ee3a096c1c72271cf4cb9393f778b25cd0ef6a729a679ae4524d",
                 "licence": "copyrighted", "connector": "Lamello Clamex P-14",
                 "capture": "xag/furniture: sources/lamello/lamello-clamex-p-14-instructions/"
                            "Mode_d_emploi_ClamexP14.pdf (private)"},
        children=[
            Node(id="groove-and-hole", kind="clause",
                 payload={"locator": "p. 1, the section of the groove with the access hole (7.5) "
                                     "and the steps on p. 2 (Ø 6 mm drill, Art. No. 131506)",
                          "printed": {"access_hole_offset": "7.5", "access_hole_diameter": "Ø = 6 mm"}},
                 params={"access_hole_offset": _published(7.5, "mm", "7.5, from the joint face"),
                         "access_hole_diameter": _published(6, "mm", "Ø 6 mm drill")}),
            Node(id="open-and-close", kind="clause",
                 payload={"locator": "p. 2, the two figures marked open and close (sheet "
                                     "Clamex P-14 08/19)",
                          "in_our_words": "turned to close, the lever draws the two halves "
                                          "together across the joint line, square to it; "
                                          "turned to open, it pushes them apart the same way, "
                                          "the element then reaching across the joint line"}),
        ])


def connectors() -> Node:
    params = {name: Quantity(value=float(v), unit=unit, provenance="derived", grounded=True,
                             derived_from=[f"{TECHNICAL_DATA}/{name}"], note=label)
              for name, v, unit, label in CLAMEX_P_14}
    params.update({name: Quantity(value=float(v), unit="mm", provenance="derived", grounded=True,
                                  derived_from=[f"{TECHNICAL_DATA}/{name}"],
                                  note=f"size (L x H x I), {name}")
                   for name, v in CLAMEX_P_14_SIZE})
    hole = f"{INSTRUCTIONS}/groove-and-hole"
    params.update({name: Quantity(value=v, unit="mm", provenance="derived", grounded=True,
                                  derived_from=[f"{hole}/{name}"], note=note)
                   for name, v, note in [("access_hole_diameter", 6.0, "the hole it is closed through"),
                                         ("access_hole_offset", 7.5, "from the joint face to the "
                                                                     "hole's centre")]})
    params.update({name: _from(f"{BROCHURE}/clamex-p-14-installation/{name}", note)
                   for name, note in [("min_end_distance", "the first groove's middle from the end"),
                                      ("max_spacing", "the most between two grooves' middles")]})
    clamex = Node(id="lamello-clamex-p-14", kind="connector", name="Lamello Clamex P-14",
                  payload={"maker": "Lamello", "setting": SETTING,
                           "kind_of_connector": "knock-down furniture connector seated in a "
                                                "P-System groove, closed with a lever through "
                                                "a 6 mm access hole",
                           "engages": "square",
                           "tested_elsewhere": tested_elsewhere()},
                  params=params,
                  links={"needs": ["tools/lamello-zeta-p2", "tools/cnc-with-p-system-cutter"],
                         "drilled_with": ["tools/lamello-clamex-p-drill-jig"],
                         "per": [TECHNICAL_DATA, DESCRIPTION, OPEN_AND_CLOSE, hole,
                                 f"{BROCHURE}/clamex-p-14-installation", STUDY_RESULT,
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
                 payload={"locator": "Table 1, specimen A", "quote": "2 pcs Clamex P-14",
                          "connector": "Lamello Clamex P-14"},
                 params={"connectors": Quantity(value=2.0, unit="", provenance="published",
                                                grounded=True, note="2 pcs")}),
            Node(id="clamex-p-14-l-joint", kind="clause",
                 payload={"locator": "Results and discussion, specimen A",
                          "connector": "Lamello Clamex P-14",
                          "quote": "the tested joint A achieved average values of 9 Nm "
                                   "(tension), 15 Nm (compression), a stiffness of 55 Nm/rad "
                                   "(tension), and 237 Nm/rad (compression) in the bending "
                                   "tests in the angular plane"},
                 params={name: q(v, unit, words) for name, v, unit, words in L_JOINT}),
        ])


# Tests of other Clamex sizes, and Lamello's own ratings of the P-15 beside the P-14's.
# None of their values is a P-14 limit: they are clauses, and the connector lists them in
# `tested_elsewhere` (ledger: another-clamex-sizes-test-stands-in-only-below-the-p-14s-rating,
# a-bending-test-in-an-unnamed-direction-is-never-rated).

SAAR = "sources/saar-2015"
# Saar et al. (2015), Tables 1 and 2, in 21 mm birch plywood, 10 specimens each:
# (clause id, locator, connector, mode, mean N, standard deviation N, the test)
SAAR_ROWS = [
    ("table-1-clamex-p-15", "Table 1, row Clamex P15", "Lamello Clamex P-15", "pull_out",
     2204.52, 457.08, "pulled apart, a T-joint"),
    ("table-1-clamex-p-10", "Table 1, row Clamex P10", "Lamello Clamex P-10", "pull_out",
     1385.57, 50.47, "pulled apart, a T-joint"),
    ("table-2-clamex-p-15", "Table 2, row Clamex P15", "Lamello Clamex P-15", "shear",
     2512.18, 174.21, "sheared, an L-joint loaded 2 mm from the joint"),
    ("table-2-clamex-p-10", "Table 2, row Clamex P10", "Lamello Clamex P-10", "shear",
     1616.25, 153.04, "sheared, an L-joint loaded 2 mm from the joint"),
]


def _stated(value: float, unit: str, note: str) -> Quantity:
    return Quantity(value=float(value), unit=unit, provenance="published", grounded=True,
                    note=note)


def saar() -> Node:
    """Saar et al. (2015): free to read, no licence printed, so cited by locator and values."""
    return Node(
        id="saar-2015", kind="source",
        name="Saar, Kers, Luga, Reiska: Detachable connecting fittings failure loads on plywood "
             "furniture, Proceedings of the Estonian Academy of Sciences 64(1S), 113-117 (2015)",
        payload={"publisher": "Estonian Academy Publishers", "year": 2015,
                 "identifier": "doi:10.3176/proc.2015.1S.07",
                 "url": "https://kirj.ee/public/proceedings_pdf/2015/issue_1S/Proc-2015-1S-113-117.pdf",
                 "fetched": "2026-11-13",
                 "sha256": "0781987ea136c0a4f805d053b876beb0e6a692c5ae7b3ecb7d4e6b51f99ed6c5",
                 "licence": "unstated",
                 "licence_note": "free to read; no licence is printed on the article or on its "
                                 "landing page (kept beside the copy as landing.html)",
                 "capture": "xag/furniture: sources/lamello/saar-2015/saar-2015.pdf (private)"},
        children=[
            Node(id="specimens", kind="clause",
                 payload={"locator": "2. Materials and Methods, 2.3. Testing procedures",
                          "in_our_words": "specimens of 21 mm birch plywood, a T-joint pulled "
                                          "apart and an L-joint sheared, 10 specimens per test; "
                                          "the paper does not say how many connectors each "
                                          "specimen held"},
                 params={"thickness": _stated(21, "mm", "21 mm thick birch plywood"),
                         "specimens": _stated(10, "", "10 specimens per test")}),
            *[Node(id=cid, kind="clause",
                   payload={"locator": locator, "connector": connector,
                            "material": "birch plywood, 21 mm",
                            "in_our_words": f"{connector}, {test}: mean and standard "
                                            "deviation of 10 specimens"},
                   params={mode: _stated(mean, "N", f"mean, {test}"),
                           f"{mode}_sd": _stated(sd, "N", "standard deviation")})
              for cid, locator, connector, mode, mean, sd, test in SAAR_ROWS],
        ])


SYDOR = "sources/sydor-2019"
# Sydor & Pohl (2019), Table 2, Clamex P-10 rows, per fastener: (clause id, the row's label,
# the board, its density kg/m3 from Materials and methods, Mmax N m, its standard deviation,
# M at 50 mrad N m, cM N m/mrad)
SYDOR_ROWS = [
    ("table-2-clamex-plywood", "Plywood", "hardwood plywood", 727, 14.20, 2.14, 7.03, 0.124),
    ("table-2-clamex-oak-glued", "Oak (glued)", "edge-glued oak board", 698,
     18.13, 1.16, 10.36, 0.202),
    ("table-2-clamex-pine-glued", "Pine (glued)", "edge-glued pine board", 521,
     19.13, 1.85, 10.56, 0.219),
]


def sydor() -> Node:
    """Sydor & Pohl (2019): all rights reserved, so cited by locator and values."""
    return Node(
        id="sydor-2019", kind="source",
        name="Sydor, Pohl: Load-bearing capacity and characteristic forms of destruction of "
             "furniture joints made with rastex 15 and P-10 clamex fasteners, Annals of Warsaw "
             "University of Life Sciences - SGGW, Forestry and Wood Technology 106, 38-48 (2019)",
        payload={"publisher": "Warsaw University of Life Sciences Press", "year": 2019,
                 "identifier": "doi:10.5604/01.3001.0013.7735",
                 "url": "https://bibliotekanauki.pl/articles/2206681.pdf",
                 "fetched": "2026-11-13",
                 "sha256": "1df1043c8a4fe8fff12d3357cbeccbcc9d067e62721449420c301a029c331160",
                 "licence": "copyrighted",
                 "licence_note": "all rights reserved, per its Biblioteka Nauki record (kept "
                                 "beside the copy); free to read",
                 "capture": "xag/furniture: sources/lamello/sydor-2019/sydor-2019.pdf (private)"},
        children=[
            Node(id="samples", kind="clause",
                 payload={"locator": "Materials and methods, Figures 3 and 4",
                          "connector": "Lamello Clamex P-10",
                          "in_our_words": "a shelf board joined to the face of a side board (a "
                                          "T-joint) by two fasteners 128 mm apart, bent by a "
                                          "moment alone, the force always in one direction "
                                          "(up); the paper does not say whether that opens or "
                                          "closes the joint. Moments are per fastener, the "
                                          "joint's divided by 2; the expected value is the "
                                          "median of 10 samples"},
                 params={"fasteners": _stated(2, "", "two fasteners per sample"),
                         "spacing": _stated(128, "mm", "128 mm apart"),
                         "samples": _stated(10, "", "10 characteristics per variant"),
                         "thickness": Quantity(value=18.0, unit="mm", provenance="published",
                                               grounded=True,
                                               note="transcription: read from the drawing in "
                                                    "Figure 3, p. 40; not in the text")}),
            *[Node(id=cid, kind="clause",
                   payload={"locator": f"Table 2, Clamex / {label}",
                            "connector": "Lamello Clamex P-10", "material": f"{material}, 18 mm",
                            "in_our_words": "per fastener, the T-joint bent in one direction"},
                   params={"density": _stated(density, "kg/m3", "density measured before "
                                                                 "assembly (Materials and methods)"),
                           "moment_max": _stated(m, "N m", "Mmax, Nm per fastener"),
                           "moment_max_sd": _stated(sd, "N m", "standard deviation of Mmax"),
                           "moment_at_50_mrad": _stated(m50, "N m", "M50 mrad, Nm per fastener"),
                           "stiffness": _stated(c * 1000, "N m/rad",
                                                f"cM {c} Nm/mrad per fastener")})
              for cid, label, material, density, m, sd, m50, c in SYDOR_ROWS],
        ])


# Lamello's pages of the P-15 (2013) and the P-14 (2014), from the Internet Archive: the one
# edition of Lamello's ratings found that rates both in the same materials.
# (source id, connector, capture date, url, sha256, copy, installation depth mm,
#  tensile strength by material key N)
P_15_2013 = ("lamello-clamex-p-15-2013", "Lamello Clamex P-15", "2013-05-04",
             "https://web.archive.org/web/20130504183337/http://www.lamello.com/en/home/"
             "join-wood/p-system/clamex-p-15.html",
             "cbc28dcc6769ed195e59df8b26872aa7b306f69fb370c02a6324fac92ae19f1d",
             "clamex-p-15.en.html", 15, {"particleboard": 800, "beech": 1300})
P_14_2014 = ("lamello-clamex-p-14-2014", "Lamello Clamex P-14", "2014-10-18",
             "https://web.archive.org/web/20141018155152/http://www.lamello.com/en/home/"
             "join-wood/p-system/clamex-p-14.html",
             "5e9a274e1c8a54e0f365332568b30f473d4cf7a10cf0e094b2e9e65efe274a43",
             "clamex-p-14.en.html", 14, {"particleboard": 800, "beech": 1000})


def lamello_page(page: tuple) -> Node:
    sid, connector, captured, url, sha, copy, depth, tensile = page
    return Node(
        id=sid, kind="source", name=f"Lamello, {connector.removeprefix('Lamello ')} product page "
                                    f"(English), as archived on {captured}",
        payload={"publisher": "Lamello AG", "year": int(captured[:4]), "url": url,
                 "fetched": "2026-11-13, from the Internet Archive",
                 "sha256": sha, "licence": "copyrighted", "connector": connector,
                 "capture": f"xag/furniture: sources/lamello/{sid}/{copy} (private)"},
        children=[
            Node(id="technical-data", kind="clause",
                 payload={"locator": "technical data, Tensile strength"},
                 params={f"pull_out_{key}": _stated(v, "N", f"tensile strength in {key}, "
                                                            "approximate (~)")
                         for key, v in tensile.items()}),
            Node(id="description", kind="clause",
                 payload={"locator": "Description",
                          "in_our_words": f"its installation depth is {depth} mm"
                                          + ("; it is called the new generation"
                                             if connector.endswith("P-14") else "")},
                 params={"installation_depth": _stated(depth, "mm", "installation depth")}),
        ])


def tested_elsewhere() -> list[dict]:
    """The tests of other Clamex sizes the P-14 is not rated from, for a reader to find."""
    p15, p14 = (f"sources/{page[0]}/technical-data" for page in (P_15_2013, P_14_2014))
    above = (f"Lamello rated the P-15 above the P-14 in beech, {P_15_2013[7]['beech']} N against "
             f"{P_14_2014[7]['beech']} N in tension ({p15}, {p14}), so the P-15's value could "
             "overstate the P-14's")
    smaller = "the P-10 is a smaller connector, seated 10 mm deep against the P-14's 14 mm"
    out = [{"clause": f"{SAAR}/{cid}",
            "what": f"{connector}, {test}, 21 mm birch plywood: {mean} N, mean of 10",
            "not_rated_because": above if connector.endswith("P-15") else smaller}
           for cid, _loc, connector, _mode, mean, _sd, test in SAAR_ROWS]
    out += [{"clause": f"{SYDOR}/{cid}",
             "what": f"Lamello Clamex P-10, a T-joint of 18 mm {material} bent by a moment: "
                     f"{m} N m per fastener at most",
             "not_rated_because": smaller + "; and the paper does not say whether its one "
                                            "direction opens or closes the joint"}
            for cid, _label, material, _d, m, _sd, _m50, _c in SYDOR_ROWS]
    return out


# The Zeta P2's documents and what each says of setting it, cutting a groove and drilling the access
# hole: (source id, name, url, sha256, its copy in xag/furniture, [(clause id, locator, {param: (value,
# unit, as printed)})]); tests/test_zeta_p2.py finds each printed value in the text beside the copy
MANUAL = "sources/lamello-zeta-p2-manual"
MACHINING = "sources/lamello-machining-with-power-tools"
ANGLE_TIP = "sources/lamello-tip-angle-joints-zeta-p2"
DEPTH_TIP = "sources/lamello-tip-milling-depth-zeta-p2"
ZETA_DOCS = [
    ("lamello-zeta-p2-manual", "Lamello, Zeta P2 operating instructions (05/25, Art. No. 9881205VS)",
     "https://lamello.com/fileadmin/products/Operating_instructions_Zeta_P2.pdf",
     "4a3fc40f65d9b76dcb9a173e8fb939edf749c09e4e21d92d172e5b68723b619a",
     "sources/lamello/zeta-p2/Operating_instructions_Zeta_P2.pdf", [
         ("scope-of-delivery", "EN p. 6, Overview of machine, scope of delivery",
          {"spacer_thick": (4, "mm", "Spacer plate 4 mm"), "spacer_thin": (2, "mm", "Spacer 2 mm")}),
         ("groove-spacings", "EN p. 7, Recommended groove spacings, for the P-System",
          {"min_end_distance": (37, "mm", "min. 37 mm"), "max_spacing": (300, "mm", "max. 300 mm")}),
         ("cutting-grooves", "EN p. 8, Cutting grooves, 1 to 5", {}),
         ("p-system-depth", "EN p. 9, Use for the P-System: set the depth adjuster, and adjusting the "
                            "cutting depth after changing the cutter",
          {"recess": (0.5, "mm", "0.5 mm below the"), "per_turn": (0.7, "mm", "0.7 mm")}),
         ("angle-joint", "EN p. 10, Cutting grooves (angle joint), 1 and 2", {}),
         ("drill-access-hole", "EN p. 12, Drill access hole, and its note",
          {"drill_diameter": (6, "mm", "Spiral drill Ø 6 mm")}),
     ]),
    ("lamello-machining-with-power-tools", "Lamello, Machining with power tools (web page)",
     "https://lamello.com/solutions/lamello-expertise/machining-with-power-tools",
     "0d62b8d3baeb62f674c09cb5d8f6c3443f8908b00cb720bbf4a6e4f64d77dc78",
     "sources/lamello/zeta-p2/pages/machining-with-power-tools.en.html", [
         ("equal-distance", "Equal distance to the cutter",
          {"groove_offset": (10, "mm", "the distance to the centre of the cutter is exactly 10 mm")}),
         ("surface-connections", "180° surface connections, the spacers", {}),
         ("butt-angle-joints", "Butt angle joints", {}),
     ]),
    ("lamello-tip-angle-joints-zeta-p2", "Lamello, Tips and tricks: Angle joints with the Zeta P2",
     "https://lamello.com/solutions/lamello-expertise/tips-and-tricks/details-page/angle-joints-with-the-zeta-p2",
     "c1e88a1b478bfe057be3311def83a661faac75412cd44d7307b41c3552ad714b",
     "sources/lamello/zeta-p2/pages/tip_angle-joints-with-the-zeta-p2.en.html", [
         ("steps", "steps 1 to 6", {}),
     ]),
    ("lamello-tip-milling-depth-zeta-p2", "Lamello, Tips and tricks: Finely adjusting the milling depth "
                                          "on the Zeta P2",
     "https://lamello.com/solutions/lamello-expertise/tips-and-tricks/details-page/"
     "finely-adjusting-the-milling-depth-on-the-zeta-p2",
     "a380ec732b3dd2b606ed788da4c156f7d62e28b623e619a3fed0ce23fcf258cf",
     "sources/lamello/zeta-p2/pages/tip_finely-adjusting-the-milling-depth-on-the-zeta-p2.en.html", [
         ("steps", "steps 1 to 6", {"per_turn": (0.7, "mm", "0.7mm")}),
     ]),
]


BROCHURE = "sources/lamello-p-system-brochure"
BROCHURE_DOC = ("lamello-p-system-brochure", "Lamello, P-System brochure (English, 2026)",
                "https://lamello.com/fileadmin/Downloads/Broschueren/P-System/PDF/P-System_Broschuere_EN.pdf",
                "03e0c0efd71ab8f76a6f327fd415d5a53c2e6ef989f9a511d74df2abaecb4da2",
                "sources/lamello/zeta-p2/P-System_Broschuere_EN.pdf",
                [("clamex-p-14-installation", "p. 11, Clamex P-14, Installation 1 to 8",
                  {"min_end_distance": (37, "mm", "min.37 mm"), "max_spacing": (300, "mm", "max. 300 mm")})])


def brochure() -> Node:
    """The P-System brochure's page on the Clamex P-14: where its grooves go along a joint."""
    sid, name, url, sha, copy, clauses = BROCHURE_DOC
    (cid, loc, params), = clauses
    return Node(id=sid, kind="source", name=name,
                payload={"publisher": "Lamello AG", "year": 2026, "url": url, "fetched": "2026-11-15",
                         "sha256": sha, "licence": "copyrighted", "capture": f"xag/furniture: {copy} (private)"},
                children=[Node(id=cid, kind="clause",
                               payload={"locator": loc, "connector": "Lamello Clamex P-14",
                                        "printed": {k: v[2] for k, v in params.items()}},
                               params={k: _published(v[0], v[1], v[2]) for k, v in params.items()})])


VIDEO = "sources/lamello-video-clamex-p-14-non-mitred"
# Lamello's video, as its distributor Colonial Saw posted it: (id, name, url, sha256 of the account Gemini
# gave of it, kept privately under videos/<YouTube id>.md, [(clause id, locator, the words it rests on)]).
VIDEO_DOC = ("lamello-video-clamex-p-14-non-mitred",
             "Lamello, Joining with Clamex P-14: non-mitred angles (video, posted by its distributor Colonial "
             "Saw as Lamello Clamex P-14 | 90° Joint with Zeta P2)",
             "https://www.youtube.com/watch?v=8NCyH4o32Yo",
             "9d591493bd7dc2a40fe44b625d6654edeb36dced17b1a547134347a0f3d2de02",
             [("edge-groove-first", "00:25 to 00:43: step 1, the grooves in the edge, the base plate flat on the face",
               ["Step 1: Cut the grooves in the edge", "base plate lying flat against the large flat face"]),
              ("drill-the-edge-grooved-part", "00:44 to 00:55: the drill jig over the edge, at the groove, then the drill",
               ["drill jig", "aligned with the groove location"]),
              ("face-groove-upright", "01:37 to 01:56: step 4, the machine upright, its stop against the edge",
               ["The machine stands upright"])])


def video() -> Node:
    """Lamello's video of a Clamex P-14 angle joint cut with the Zeta P2, cited from the account Gemini
    gave of it: nobody here watched it."""
    sid, name, url, sha, clauses = VIDEO_DOC
    return Node(id=sid, kind="source", name=name,
                payload={"publisher": "Lamello AG (posted by Colonial Saw)", "url": url, "fetched": "2026-11-15",
                         "sha256": sha, "licence": "copyrighted", "authority": "maker",
                         "read_by": "Gemini (gemini.google.com, the model it calls Quick answers, 3.5 Flash-Lite), "
                                    "asked on 2026-11-15 for what is said and shown, with timestamps",
                         "capture": "xag/furniture: sources/videos/8NCyH4o32Yo.md (private), Gemini's account"},
                children=[Node(id=cid, kind="clause", payload={"locator": loc}) for cid, loc, _w in clauses])


def zeta_sources() -> list[Node]:
    """The Zeta P2's manual and Lamello's pages on using it, one clause per passage relied on, its
    values as printed."""
    out = []
    for sid, name, url, sha, copy, clauses in ZETA_DOCS:
        out.append(Node(
            id=sid, kind="source", name=name,
            payload={"publisher": "Lamello AG", "year": 2026, "url": url, "fetched": "2026-11-15",
                     "sha256": sha, "licence": "copyrighted",
                     "capture": f"xag/furniture: {copy} (private)"},
            children=[Node(id=cid, kind="clause",
                           payload={"locator": loc, "printed": {k: v[2] for k, v in params.items()}},
                           params={k: _published(v[0], v[1], v[2]) for k, v in params.items()})
                      for cid, loc, params in clauses]))
    return out


def _from(ref: str, note: str) -> Quantity:
    clause, param = ref.rsplit("/", 1)
    v = next(q for d in [*ZETA_DOCS, BROCHURE_DOC] for cid, _l, ps in d[5] for k, q in ps.items()
             if f"sources/{d[0]}/{cid}" == clause and k == param)
    return Quantity(value=float(v[0]), unit=v[1], provenance="derived", grounded=True,
                    derived_from=[ref], note=note)


ZETA_SAY = {
    "fr": {"name": "Lamello Zeta P2", "method": [
        "Régler la butée de profondeur standard sur « max » et la butée P-System sur « 14 », la "
        "même pour les deux pièces d'un assemblage.",
        "Faire une rainure d'essai dans une chute et y engager une moitié de Clamex P-14 : elle doit "
        "être à environ 0,5 mm sous la surface. Sinon, mettre la butée P-System sur « OFF », tourner "
        "sa vis de réglage (un tour : 0,7 mm) et refaire un essai.",
        "La fraise est à 10 mm de la plaque de base comme de la butée pivotante ; la cale de 2 mm ou "
        "de 4 mm rapproche la rainure d'autant de sa référence.",
        "Rainure dans un chant : rabattre la butée pivotante et la poser sur la face de référence. "
        "Rainure dans une face : machine debout, l'équerre de butée fixée sur la plaque de base, la "
        "plaque de base à fleur du chant de référence.",
        "Aligner le marquage central de la plaque de base sur le trait.",
        "Dans une jonction d'angle, fraiser d'abord la pièce rainurée dans son chant, puis reporter "
        "le milieu de chaque rainure sur l'autre pièce, les deux pièces tenues ensemble.",
        "Serrer la pièce ; tenir la machine à deux mains et plonger lentement et régulièrement "
        "jusqu'en butée. Le profil se fraise seul : attendre que le téton du mécanisme VMD revienne "
        "à fleur (1 à 2 secondes), puis relâcher."]},
    "en": {"name": "Lamello Zeta P2", "method": [
        "Set the standard depth adjuster to «max» and the P-System depth adjuster to «14», the same "
        "for both parts of a joint.",
        "Cut a test groove in an offcut and fit one half of a Clamex P-14: it should sit about 0.5 mm "
        "below the surface. If not, turn the P-System adjuster to «OFF», turn its adjusting screw "
        "(one turn: 0.7 mm) and cut another test.",
        "The cutter is 10 mm from the base plate and from the swivel stop; the 2 mm or 4 mm spacer "
        "brings the groove that much nearer its reference.",
        "Groove in an edge: fold the swivel stop down onto the reference face. Groove in a face: the "
        "machine upright, the stop square fixed on the base plate, the base plate flush with the "
        "reference edge.",
        "Line up the base plate's centre marking with the pencil line.",
        "In a corner joint, cut the part grooved in its edge first, then transfer the middle of each "
        "groove to the other part, the two held together.",
        "Clamp the part; hold the machine with both hands and plunge slowly and evenly to the stop. "
        "The profile cuts itself: wait until the VMD mechanism's pin is flush again (1 to 2 seconds), "
        "then let go."]},
}

JIG_SAY = {
    "fr": {"name": "Gabarit de perçage Clamex P (Lamello 125344)", "method": [
        "Mettre l'insert du gabarit sur « 14 ».",
        "Desserrer la molette, pousser le gabarit au milieu de la rainure, bien appuyé sur le chant "
        "et sur la face, et resserrer la molette.",
        "Tenir le gabarit et percer avec le foret hélicoïdal Ø 6 mm à pointe de centrage livré "
        "(Lamello 131506).",
        "Retirer le gabarit, vider les copeaux de la rainure, passer à la rainure suivante."]},
    "en": {"name": "Clamex P drill jig (Lamello 125344)", "method": [
        "Set the jig's insert to «14».",
        "Loosen the knurled nut, push the jig into the middle of the groove, resting well on the edge "
        "and on the face, and tighten the nut.",
        "Hold the jig and drill with the Ø 6 mm spiral drill with centring point that comes with it "
        "(Lamello 131506).",
        "Remove the jig, clear the chips from the groove, and move to the next groove."]},
}


def tools() -> Node:
    """The machine that cuts the P-System groove, following the general method of a biscuit or plate
    jointer and adding its settings, and the jig the Clamex P's access hole is drilled with."""
    return Node(id="tools", kind="", children=[
        Node(id="lamello-zeta-p2", kind="tool", name="Lamello Zeta P2",
             payload={"maker": "Lamello", "does": "cuts the P-System groove",
                      "spacers_mm": [2.0, 4.0], "say": ZETA_SAY, "model": models.zeta_p2()},
             params={"groove_offset": _from(f"{MACHINING}/equal-distance/groove_offset",
                                            "from the base plate and from the swivel stop to the "
                                            "middle of the groove"),
                     "test_recess": _from(f"{MANUAL}/p-system-depth/recess",
                                          "how far under the surface the connector sits in a test groove "
                                          "cut at the right depth")},
             links={"per": [DESCRIPTION, f"{MANUAL}/scope-of-delivery", f"{MANUAL}/p-system-depth",
                            f"{DEPTH_TIP}/steps", f"{MACHINING}/equal-distance",
                            f"{MACHINING}/surface-connections", f"{MANUAL}/angle-joint",
                            f"{ANGLE_TIP}/steps", f"{MACHINING}/butt-angle-joints",
                            f"{MANUAL}/cutting-grooves", f"{VIDEO}/edge-groove-first",
                            f"{VIDEO}/face-groove-upright"],
                    "follows": ["tools/plate-jointer"]}),
        Node(id="lamello-clamex-p-drill-jig", kind="tool", name="Lamello Clamex P drill jig",
             payload={"maker": "Lamello", "does": "drills a Clamex P's access hole square to the face, "
                                                  "centred on its groove", "say": JIG_SAY,
                      "model": models.drill_jig()},
             links={"per": [f"{MANUAL}/drill-access-hole", f"{VIDEO}/drill-the-edge-grooved-part"]}),
        Node(id="cnc-with-p-system-cutter", kind="tool", name="CNC machine with a P-System cutter",
             payload={"maker": "any", "does": "cuts the P-System groove"},
             links={"per": [DESCRIPTION]}),
    ])


# Who stands behind each source (furniture-design's AUTHORITIES).
AUTHORITY = {
    "lamello-clamex-p-14": "maker",
    "lamello-clamex-p-15-2013": "maker",
    "lamello-clamex-p-14-2014": "maker",
    "lamello-clamex-p-14-instructions": "maker",
    "lamello-zeta-p2-manual": "maker",
    "lamello-machining-with-power-tools": "maker",
    "lamello-tip-angle-joints-zeta-p2": "maker",
    "lamello-tip-milling-depth-zeta-p2": "maker",
    "lamello-p-system-brochure": "maker",
    "janikova-2025": "research",
    "saar-2015": "research",
    "sydor-2019": "research",
}


def knowledge() -> list[Node]:
    """Top-level branches to merge with furniture-design's: sources, connectors, tools."""
    return [Node(id="sources", kind="", children=with_authority([source(), study(), saar(), sydor(),
                                                  lamello_page(P_15_2013), lamello_page(P_14_2014),
                                                  instructions(), *zeta_sources(), brochure(), video()], AUTHORITY)),
            connectors(), tools()]
