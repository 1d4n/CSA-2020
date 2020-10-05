import json

with open('array', 'r') as arr:
    a = json.load(arr)

_g0 = 7


def f4(_p2, _p1, _p3, _p0):
    for _g1 in range(_p1, _p3):
        _p2[_g1] += _p0


def f3(_p2, _p1, _p3, _p0):
    for _g1 in range(_p1, _p3):
        _p2[_g1] -= _p0


def f2(_p2, _p1, _p3, _p0):
    for _g1 in range(_p1, _p3):
        _p2[_g1] ^= _p0


def _f1(_p1, _p0):
    _g2 = _p1[_p0+1]
    _g3 = ""
    for _g4 in range(_g2):
        _g3 += chr(_p1[_p0+2+_g4] ^ 0x37)
    return _g3


_g5 = [f4, f3, f2]


def f0(_p1, _p0):
    _g6 = 0
    flag = [1] * 40

    while _g6 < len(_p1):
        _g7 = _p1[_g6]
        if _g7 == 5:
            return ''.join(map(chr, flag)), _f1(_p1, _g6)  # The flag

        _g8 = _p1[_g6 + 1]
        _g9 = _p1[_g6 + 2]

        # if (_p0[_g8] % _g9 == 0) == (_g7 - 4 == 0):
        if _g7 == 4:
            flag[_g8] *= _g9  # reversing

        # _p0[_g8] = _p0[_g8] if (_p0[_g8] % _g9) else math.floor(_p0[_g8] / _g9)
        _ga = _p1[_g6 + 4]
        _gb = _p1[_g6 + 5]
        _gc = _p1[_g6 + 6] ^ _g7 - 3
        _gd = _p1[_gc]
        _g5[_ga](_p1, _g6 + _g0, (_gb + 1) * _g0, _gd)
        _g6 += _g0


print(f0(a, [0] * 41))
