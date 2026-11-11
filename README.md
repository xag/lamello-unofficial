# lamello-unofficial

Lamello's connectors and the tools that cut their seats, as data for [furniture-design](https://github.com/xag/furniture-design). **Unofficial**: Lamello did not write or endorse it, and nothing here speaks for Lamello.

## What is here

- `lamello_unofficial.knowledge()`: the Clamex P-14 connector (minimum workpiece width, minimum material thickness for each kind of cut, pull-out and shear strength in particle board, MDF and beech, the P-System setting P-14) and the two tools its groove is cut with (the Zeta P2, or a CNC machine with a P-System cutter).
- How much a Clamex P-14 corner joint resists being bent open or shut (9 and 15 N·m for a joint of two connectors in 18 mm particle board), from Janíková et al. (2025), *Materials* 18(9), 2114, an open-access study under CC BY 4.0: quoted, its text kept under `sources/janikova-2025/`, and halved per connector. furniture-design's sideways check reads it to count what a piece's corner joints hold.
- No kinds and no rules of its own. A joint that uses the connector is checked by furniture-design's rules: the joined parts are thick enough for the kind of cut and wide enough, and the joint is cut with one of the connector's tools at its setting.

## Sources

Every value comes from the technical data table of Lamello's Clamex P-14 product page (French edition, fetched 2026-11-11; the English address redirects there). The page is copyrighted, so it is cited by locator and values and never quoted. The copy as fetched is kept in a private repo, and `tests/test_values.py` checks every value against it: clone that repo beside this one, or set `FURNITURE_REPO`, or that test fails and says why.

## Using it

```python
from furniture_design.knowledge import knowledge as general, merge, mount
from lamello_unofficial import knowledge as lamello

tree.root.children = merge(general(), lamello()) + [pieces]
# or under one branch beside a tree's own requirements/:
tree.root.children.append(mount(merge(general(), lamello()), "knowledge"))
```

A joint then links `uses: ["connectors/lamello-clamex-p-14"]` and `made_with: ["tools/lamello-zeta-p2"]`, with `cut` (edge, surface, intermediate or mitre) and `setting: "P-14"` in its payload.

## Design ledger

```sh
uv sync
uv run quern brief .
uv run quern check
```

There is no flight-recorder boundary: nothing here touches storage, the network, the clock or randomness.

## Tests

`uv run pytest --testmon`, then `uv run pytest`. Both stop at the first failure.
