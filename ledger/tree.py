"""The decisions lamello-unofficial is bound by, as a ledger. Read it with
`uv run quern brief .`, never whole.

Vocabulary: ledger@0.7.0 and grounding@1.2.0, pinned in quern.lock.
"""

from __future__ import annotations

import os
from pathlib import Path

import quern.grounding  # noqa: F401
from quern import Node, Quern
from quern.library import consume


def _alt(id_: str, name: str, why: str) -> Node:
    return Node(id=id_, kind="alternative", name=name, payload={"why": why})


def entries() -> list[Node]:
    return [
        Node(
            id="the-products-are-data-on-furniture-designs-kinds", kind="decision",
            name="Lamello's connectors and tools are knowledge nodes on furniture-design's kinds (source, "
                 "clause, connector, tool), shipped as Python (`knowledge()`); this repo defines no kind or "
                 "rule and publishes no quern package. A Lamello check that the general rules cannot state "
                 "would be the first reason to publish one",
            payload={"decided_on": "2026-11-11",
                     "the_owner": "lamello specific should not be in furniture design package, they should be "
                                  "in a lamello unofficial package.",
                     "why": "Everything the Clamex P-14 page states (minimum thickness per cut, minimum width, "
                            "strengths, the setting, the tools) is a value furniture-design's joint rules "
                            "already read. A quern package carries kinds and rules; one carrying none would "
                            "prove nothing at its publish gate."},
            children=[
                _alt("an-empty-quern-package", "Publish a lamello-unofficial@ quern package anyway",
                     "Its gate would have no rule to exercise and no counter-example to refute."),
                _alt("lamello-rules", "Write Lamello-specific rules (the P-14 setting, the Zeta P2)",
                     "Each is an instance of a general rule furniture-design states for any maker."),
            ],
        ),
        Node(
            id="the-values-are-checked-against-a-private-copy", kind="decision",
            name="Every value is checked by a test against the page as fetched, kept in the private repo "
                 "xag/furniture; the test fails, never skips, when that copy is not beside this repo",
            payload={"decided_on": "2026-11-11",
                     "why": "The page is copyrighted, so neither it nor its words are here (furniture-design "
                            "decision a-copyrighted-source-is-cited-by-locator-and-values); a value with no "
                            "copy to check it against is a number someone typed."},
            links={"rests_on": ["the-products-are-data-on-furniture-designs-kinds"]},
            children=[
                _alt("skip-without-the-copy", "Skip the check when the copy is absent",
                     "A skipped check reads as green on every machine that cannot run it."),
            ],
        ),
        Node(
            id="a-published-test-of-a-product-is-its-data-here", kind="decision",
            name="A published test of a Lamello product by someone else (a study's measured values) is data "
                 "here, on the product's node, cited as its own source: quoted and kept in this repo when "
                 "its licence allows (CC BY), cited by locator and values when it does not. A value "
                 "measured on one material is stored under that material's key, never applied to another",
            payload={"decided_on": "2026-11-11",
                     "why": "Lamello rates the Clamex P-14 in pull-out and shear but says nothing of a "
                            "corner joint bent open or shut; Janíková et al. (2025) measured it, in 18 mm "
                            "particle board. Under moment_<mode>_particleboard, a check of a plywood piece "
                            "still finds nothing for plywood and says so."},
            links={"rests_on": ["the-products-are-data-on-furniture-designs-kinds"]},
            children=[
                _alt("take-particleboard-for-plywood", "Use the particle board values for plywood",
                     "No source says plywood holds a Clamex at least as well."),
            ],
        ),
        Node(
            id="another-clamex-sizes-test-stands-in-only-below-the-p-14s-rating", kind="decision",
            name="A test of another Clamex size (P-10, P-15) is kept as a clause and listed in the P-14's "
                 "`tested_elsewhere`. It stands in for a P-14 value only when Lamello's own ratings, of one "
                 "edition, put that size at or below the P-14 in every material both are rated in; it then "
                 "goes on the P-14 under the material's key, grounded False, its note naming the connector "
                 "it was measured on. Saar et al.'s P-15 values in birch plywood do not stand in: Lamello "
                 "rated the P-15 above the P-14 in beech",
            payload={"decided_on": "2026-11-13",
                     "why": "A shoe bench of birch plywood joined by Clamex P-14 cannot be judged sideways: "
                            "Lamello rates the P-14 only in particle board, MDF and beech, and no study found "
                            "tests it in plywood. Saar et al. (2015) tested the P-15, which the P-14 succeeded "
                            "(Lamello's 2014 page calls the P-14 the new generation), in 21 mm birch plywood. "
                            "A value taken from a stronger connector would let the check pass a piece the P-14 "
                            "may not hold, and ungrounded marks the value but the check still reads it. "
                            "Lamello's pages of 2013 (P-15) and 2014 (P-14) are the one edition found that "
                            "rates both in the same materials: equal in particle board (800 N in tension), the "
                            "P-15 above in beech (1300 N against 1000 N). tests/test_other_sizes.py holds the "
                            "comparison and that no P-14 value is read from a P-15 clause while it stands."},
            links={"rests_on": ["a-published-test-of-a-product-is-its-data-here"]},
            children=[
                _alt("borrow-the-p-15-ungrounded", "Put Saar's P-15 means on the P-14 as shear_plywood and "
                     "pull_out_plywood, ungrounded",
                     "Lamello rates the P-15 above the P-14 in beech, so the value could overstate the P-14."),
                _alt("scale-by-the-beech-ratio", "Scale the P-15's values by the beech ratio, 1000/1300",
                     "No source says the ratio in beech, in tension, holds in plywood, or in shear."),
                _alt("compare-with-todays-p-14-page", "Compare the P-15's 2013 ratings with today's P-14 page "
                     "(1870 N in beech)",
                     "Lamello restated its ratings between editions: the P-14's own particle board figure "
                     "went from 800 N (2014) to 1070 N (today), so two editions' figures do not compare."),
            ],
        ),
        Node(
            id="a-bending-test-in-an-unnamed-direction-is-never-rated", kind="decision",
            name="A joint bent in one direction that its source does not name as opening or closing it, "
                 "or bent with another connector size, is kept as a clause and never becomes a "
                 "moment_opening_<key> or moment_closing_<key>",
            payload={"decided_on": "2026-11-13",
                     "why": "The frame check counts a joint at the mean of its opening and closing moments, "
                            "and the direction matters: Janíková et al. (2025) measured a P-14 corner joint at "
                            "9 N m bent open and 15 N m bent shut. Sydor & Pohl (2019) bent T-joints of Clamex "
                            "P-10 with the force 'only in one direction (up)', without saying whether that "
                            "opens or closes the joint. Their plywood, oak and pine moments are clauses the "
                            "P-14 lists in `tested_elsewhere`, and a plywood piece's frame check stays "
                            "unjudged."},
            links={"rests_on": ["a-published-test-of-a-product-is-its-data-here"]},
            children=[
                _alt("take-it-as-both", "Use the one direction's moment for both opening and closing",
                     "It may be the stronger direction; in Janíková's P-14 joint closing holds 1.7 times "
                     "what opening does."),
                _alt("take-it-as-opening", "Use it as the opening moment, the weaker one in Janíková",
                     "Nothing says Sydor's 'up' opened the joint, and it was a P-10, not a P-14."),
            ],
        ),
        Node(
            id="this-repos-own-work-is-agpl", kind="decision",
            name="This repo's own work is licensed AGPL-3.0-or-later, copyright Xavier Grehant, as "
                 "furniture-design is; a study quoted here keeps its own licence (CC BY), and Lamello's "
                 "names and values are cited, not licensed. A contribution from anyone else is merged only "
                 "with an agreement that lets the copyright holder license it under other terms as well",
            payload={"decided_on": "2026-11-11",
                     "why": "Same terms as the package it extends (furniture-design decision "
                            "this-repos-own-work-is-agpl): open source, and nobody may host it closed."},
            children=[
                _alt("apache-2.0", "Apache-2.0, as quern is",
                     "Lets anyone host it in a closed paid service."),
            ],
        ),
        Node(
            id="the-code-is-agpl-and-the-knowledge-odbl", kind="decision",
            name="The code is licensed AGPL-3.0-or-later and the knowledge base, the database knowledge() "
                 "returns, ODbL-1.0; a contribution is merged only once its author grants the "
                 "maintainer the right to license it under other terms as well (CONTRIBUTING.md)",
            payload={"decided_on": "2026-11-11",
                     "the_owner": "il faut que ça reste élégant et standard pour ne pas perdre la confiance "
                                  "des utilisateurs et contributeurs",
                     "why": "The AGPL is a copyright licence, and the values in the base are facts copyright "
                            "does not cover. The ODbL rests on copyright, the database right and a contract "
                            "(section 2.1): a database derived from this one and used publicly must stay "
                            "under the ODbL (4.4), and so must one behind an app (4.6). A package independent "
                            "of the base, loaded beside it unmodified, is a Collective Database it does not "
                            "reach; that is the line standard licences draw, and the owner's own private "
                            "packages sit on the same side of it."},
            links={"supersedes": ["this-repos-own-work-is-agpl"]},
            children=[
                _alt("agpl-for-everything", "Keep the AGPL on the data too",
                     "It leaves the values and the database right uncovered."),
                _alt("a-licence-of-our-own", "Write a licence that also reaches independent packages, as the SSPL does",
                     "Not standard; the owner wants to keep users' and contributors' trust."),
                _alt("cc-by-sa", "CC BY-SA 4.0 for the data",
                     "It has no clause making an app publish the database behind it."),
            ],
        ),
        Node(
            id="only-the-owner-earns-from-the-knowledge", kind="decision",
            name="The knowledge base, the database knowledge() returns, is licensed CC BY-NC-SA 4.0 with one "
                 "added permission (designing, building and selling furniture with it); any other commercial "
                 "use of the data needs a commercial licence from the copyright holder. The code stays "
                 "AGPL-3.0-or-later",
            payload={"decided_on": "2026-11-11",
                     "the_owner": "Je voudrais être le seul à pouvoir gagner de l'argent avec ces données",
                     "why": "Under the ODbL anyone could sell an app on the data once they published the "
                            "database behind it. CC BY-NC-SA 4.0 is a standard licence that also licenses "
                            "database rights (section 4) for non-commercial use only, and lets the licensor "
                            "offer separate terms (6(c)): commercial licences, and the added permission "
                            "for makers. Single values a reader takes from the base are facts and stay "
                            "outside any licence; extracting a substantial part is not."},
            links={"supersedes": ["the-code-is-agpl-and-the-knowledge-odbl"]},
            children=[
                _alt("keep-the-odbl", "Keep the ODbL",
                     "Lets anyone earn from the data once they publish their derived database."),
                _alt("no-maker-permission", "CC BY-NC-SA with no added permission",
                     "Leaves a maker who sells a piece designed with it unsure they may."),
            ],
        ),
        Node(
            id="the-knowledge-is-shared-unchanged-and-improved-only-here", kind="decision",
            name="The knowledge base, the database knowledge() returns, is licensed CC BY-NC-ND 4.0 with one "
                 "added permission (designing, building and selling furniture with it): anyone may use it and "
                 "share it unchanged for a non-commercial purpose, and adapt it for their own use, but no "
                 "adapted version and no database built on a substantial part of it may be shared, so an "
                 "improvement is published here, under the contributor agreement, or not at all. Commercial use "
                 "needs a commercial licence. The code stays AGPL-3.0-or-later",
            payload={"decided_on": "2026-11-12",
                     "the_owner": "je pense que j'ai intérêt à laisser ouvert, et à interdire de dupliquer le "
                                  "contenu ... c'est exactement ce qu'il faut",
                     "why": "Under CC BY-NC-SA a copy could grow on its own, with people contributing to it "
                            "under terms that give the owner no commercial right to what they add. CC BY-NC-ND "
                            "4.0 lets copies be shared but never an adapted one (2(a)(1), 3(a)), and treats a "
                            "database holding a substantial part of this one as adapted (4(b)). Keeping the base "
                            "open is what draws people to use and improve it; closing it would leave nobody "
                            "building on it."},
            links={"supersedes": ["only-the-owner-earns-from-the-knowledge"]},
            children=[
                _alt("keep-share-alike", "Keep CC BY-NC-SA",
                     "A copy could grow elsewhere, and what people add there could not be sold by the owner."),
                _alt("close-the-base", "Move the base to a private repo and take contributions through a platform",
                     "Turned down by the owner: people would neither build on it nor improve it."),
                _alt("no-redistribution", "A licence that forbids sharing even unchanged copies",
                     "No standard licence does, GitHub lets anyone fork a public repo, and an unchanged copy "
                     "cannot grow."),
            ],
        ),
    ]


def build() -> Quern:
    root = Path(__file__).resolve().parents[1]
    lib, refs = consume(root, os.environ.get("QUERN_REGISTRY", root.parent / "quern-registry"))
    quern = Quern(packages=list(refs))
    quern = lib.effective(quern)
    quern.root.children = entries()
    return quern
