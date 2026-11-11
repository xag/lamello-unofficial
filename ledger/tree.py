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
    ]


def build() -> Quern:
    root = Path(__file__).resolve().parents[1]
    lib, refs = consume(root, os.environ.get("QUERN_REGISTRY", root.parent / "quern-registry"))
    quern = Quern(packages=list(refs))
    quern = lib.effective(quern)
    quern.root.children = entries()
    return quern
