"""The Zeta P2 and the Clamex P drill jig as solids, for the assembly instructions' drawings: data in
furniture-design's model format (furniture_design.lineart.solids), each solid an op and its sizes in mm.

The Zeta P2 in its own frame: X along the front face (+X the operator's right), Y back from the front
face along the plunge, Z up from the base plate's underside; the cutter's middle plane at Z = 10. What
Lamello prints: the stop's 120 mm (60 + 60), the cutter's 100 mm, 10 mm from the base plate and from the
folded front stop to the cutter's middle. The rest Lamello does not print, and is measured from its own
drawings (the operating instructions' exploded view, PDF p. 80, scaled by the 120 mm stop and the
100.9 mm cutter; the assembled view, p. 4) and its product photos (scaled by the stop's 0-50 mm scale),
to about ±10 %.

The drill jig in the frame of the part it sits on: the origin at the top corner of the grooved edge, in
the middle of the groove; +X out of the part, Y along the edge, Z up from the face drilled into. The hole
is at X = -7.5, the access hole's distance from the joint face.
"""
from __future__ import annotations

import math


def _box(lo, hi, dark=False):
    return {"op": "box", "lo": list(lo), "hi": list(hi), **({"dark": True} if dark else {})}


def _rbox(lo, hi, r, axis, dark=False):
    return {"op": "rbox", "lo": list(lo), "hi": list(hi), "r": r, "axis": axis, **({"dark": True} if dark else {})}


def _cyl(r, h, axis, at, n=32, dark=False):
    return {"op": "cyl", "r": r, "h": h, "axis": axis, "at": list(at), "n": n, **({"dark": True} if dark else {})}


def _prism(profile, x0, x1):
    return {"op": "prism", "profile": [list(p) for p in profile], "x": [x0, x1]}


def zeta_p2() -> dict:
    """The machine's solids: those it always has, and per pose its swivelling front stop (a plate
    120 x 70 with a window for the cutter, and its protractor sector): 'flat', folded down, its underside
    at Z = 20, reaching forward, as it lies on a part to groove its edge; 'standing', upright on the front
    face, as it stands on a part to groove its face. dials: where its depth adjusters are and what each
    is set to (the standard one on max, the P-System one on the joint's setting)."""
    parts = []
    side = [(0, 0), (150, 0), (150, 26), (146, 30), (22, 30), (14, 30), (6, 28), (0, 22)]
    parts += [_prism(side, -60, -42), _prism(side, 42, 60),                 # the base plate's side boxes
              _box((-42, 0, 0), (42, 20, 4)), _box((-42, 0, 16), (42, 20, 26)),   # the front frame
              _box((-42, 20, 0), (42, 150, 3))]
    parts += [_box((x0, -2, 0), (x0 + 10, 4, 30)) for x0 in (-60, 50)]       # the corner blocks, hinge
    parts += [_rbox((-35, 26, 22), (35, 92, 57), 6, "y"),                     # the gear block
              _cyl(19, 18, "z", (0, 55, 57))]
    parts += [_cyl(23 if k % 2 == 0 else 19.5, 5, "z", (0, 55, 75 + 5 * k), dark=bool(k % 2)) for k in range(7)]
    parts += [_cyl(23, 4, "z", (0, 55, 110)),                                 # the lifting mechanism's top
              _rbox((-23, 90, 42), (23, 112, 98), 14, "y"),                   # the motor's collar
              _rbox((-26, 112, 39), (26, 292, 101), 16, "y")]                 # the motor housing
    for k in range(5):                                                        # its cooling slots
        y = 254 + 7 * k
        parts += [_box((-26.8, y, 58), (-25.8, y + 3, 82), dark=True), _box((25.8, y, 58), (26.8, y + 3, 82), dark=True)]
    parts += [_rbox((-23, 292, 44), (23, 302, 96), 14, "y"),                  # the end cap
              _cyl(10, 40, "y", (0, 302, 70), n=24, dark=True),              # the cable guard
              _rbox((-8, 116, 99), (8, 146, 106), 3, "y", dark=True)]        # the switch
    loop, R = [], 22                                                          # the bow handle
    for x, z in ([(-39, 70), (-39, 100), (-39, 128)]
                 + [(-39 + R - R * math.cos(math.radians(t)), 128 + R * math.sin(math.radians(t))) for t in range(15, 90, 15)]
                 + [(0, 150)]
                 + [(39 - R + R * math.cos(math.radians(t)), 128 + R * math.sin(math.radians(t))) for t in range(75, 0, -15)]
                 + [(39, 128), (39, 100), (39, 70)]):
        loop.append([round(x, 2), round(81 - (z - 70) * 0.28, 2), round(z, 2)])
    parts.append({"op": "tube", "path": loop, "w": 11, "h": 20, "r": 5, "normal": [0, 1, 0.28]})
    parts += [_cyl(8, 2, "x", (x, 81, 70), n=20) for x in (-46.5, 44.5)]     # its pivots
    parts += [_cyl(11, 13, "y", (51, 10, 41), n=14),                          # the standard depth adjuster
              _cyl(10, 22, "y", (-33, 34, 92), n=14),                         # the P-System depth adjuster
              _box((-40, 26, 86), (-26, 34, 98), dark=True),                  # its stop block
              _cyl(12, 30, "y", (51, 150, 16), n=28, dark=True)]             # the dust outlet
    flat_sector = [(0, 20)] + [(round(-68 * math.cos(math.radians(a)), 2), round(20 + 68 * math.sin(math.radians(a)), 2))
                               for a in range(0, 91, 6)]
    standing_sector = [(0, 20)] + [(round(68 * math.sin(math.radians(a)), 2), round(20 + 68 * math.cos(math.radians(a)), 2))
                                   for a in range(0, 91, 6)]
    poses = {
        "flat": [_box((-60, -78, 20), (60, -50, 23)), _box((-60, -50, 20), (-40, -6, 23)),
                 _box((40, -50, 20), (60, -6, 23)), _box((-0.6, -80, 23), (0.6, -70, 23.4), dark=True),
                 _prism(flat_sector, -64, -60)],
        "standing": [_box((-60, -3, 70), (60, 0, 100)), _box((-60, -3, 30), (-40, 0, 70)),
                     _box((40, -3, 30), (60, 0, 70)), _box((-0.6, -3.4, 96), (0.6, -3, 102), dark=True),
                     _prism(standing_sector, -64, -60)],
    }
    dials = [{"at": [51, 10, 41], "shows": "max"}, {"at": [-33, 34, 92], "shows": "setting"}]
    return {"parts": parts, "poses": poses, "dials": dials}


def drill_jig() -> dict:
    """The Clamex P drill jig on a part's grooved edge: the block on the face, its lip down the edge, the
    bush the drill goes through and the knurled nut that clamps it."""
    return {"parts": [_box((-34, -16, 0), (6, 16, 12)), _box((0, -16, -16), (6, 16, 0)),
                      _cyl(9, 8, "z", (-7.5, 0, 12), n=24), _cyl(7, 10, "x", (6, 0, -6), n=16)],
            "hole": [-7.5, 0]}
