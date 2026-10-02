#!/usr/bin/env python3
"""Exact-rational regression checks for the squareclass research note.

This checks algebraic identities and bookkeeping on fixed fixtures only.
It neither searches for square-sum witnesses nor tests/proves the analytic
theorems or their universal bounds. No floating point is used.
"""

from fractions import Fraction as F
from itertools import product
from math import isqrt, lcm, prod


def squareclass(x):
    """A rational squareclass as a parity-support set; -1 records the sign."""
    x = F(x)
    if not x:
        raise ValueError("Zero has no multiplicative squareclass")
    support = {-1} if x < 0 else set()
    n = abs(x.numerator) * x.denominator
    p = 2
    while p * p <= n:
        parity = 0
        while n % p == 0:
            n //= p
            parity ^= 1
        if parity:
            support.add(p)
        p += 1
    if n > 1:
        support.add(n)
    return frozenset(support)


def rank(vectors):
    pivots = {}
    for vector in vectors:
        v = set(vector)
        while v:
            p = max(v)
            if p not in pivots:
                pivots[p] = v
                break
            v.symmetric_difference_update(pivots[p])
    return len(pivots)


def class_rank(values):
    return rank(squareclass(x) for x in values if x)


def rational_square(x):
    x = F(x)
    return x >= 0 and isqrt(x.numerator) ** 2 == x.numerator and isqrt(x.denominator) ** 2 == x.denominator


def check_anchor_and_scaling():
    fixtures = [
        ([F(-5, 2), F(0), F(3, 7), F(7, 3)], [F(-4), F(1, 3), F(5)]),
        ([F(0), F(1), F(4)], [F(1)]),
        ([F(-9), F(-4), F(-1)], [F(0), F(1, 2)]),
    ]
    transforms = [(F(1), F(0)), (F(3, 5), F(-11, 7)), (F(-2), F(9, 4)), (F(7), F(0))]
    checks = 0
    for A, B in fixtures:
        T = {a + b for a, b in product(A, B)}
        assert 0 not in T
        original_vectors = [squareclass(x) for x in T]
        h = rank(original_vectors)
        c = len(set(original_vectors))
        assert c <= 2 ** h
        for a0, b0 in product(A, B):
            q0 = a0 + b0
            U = {(a - a0) / q0 for a in A if a != a0}
            assert len(U) == len(A) - 1 and 0 not in U and -1 not in U
            normalized_column = {(a + b0) / q0 for a in A if a != a0}
            assert {1 + u for u in U} == normalized_column
            assert len({squareclass(x) for x in normalized_column}) <= c
            assert rank(original_vectors + [squareclass(x) for x in normalized_column]) == h
            full_ratios = {x / q0 for x in T}
            assert class_rank(full_ratios) in {h, h - 1}
            assert rank([squareclass(x) for x in full_ratios] + [squareclass(q0)]) == h
            for scale, shift in transforms:
                A1 = [scale * a + shift for a in A]
                B1 = [scale * b - shift for b in B]
                a1, b1 = scale * a0 + shift, scale * b0 - shift
                U1 = {(a - a1) / (a1 + b1) for a in A1 if a != a1}
                T1 = {a + b for a, b in product(A1, B1)}
                assert U1 == U
                assert T1 == {scale * x for x in T}
                assert len({squareclass(x) for x in T1}) == c
                assert abs(class_rank(T1) - h) <= 1
                checks += 1
    # Fixed illustrations: common scaling does not preserve span rank.
    assert class_rank([F(1), F(4)]) == 0
    assert class_rank([F(2), F(8)]) == 1
    return checks


def check_rational_gap_slicing():
    # Both fixtures are proper rational rank-two progressions.
    fixtures = [(F(-5, 3), (F(1, 2), F(5)), (5, 3)),
                (F(3, 7), (F(-2, 3), F(11)), (4, 2))]
    qs = [F(1), F(-1), F(2), F(-3), F(2, 3), F(-5, 7)]
    checks = 0
    for p0, steps, lengths in fixtures:
        coords = list(product(*(range(L) for L in lengths)))
        point = lambda n: p0 + sum((F(ni) * vi for ni, vi in zip(n, steps)), F(0))
        P = {point(n) for n in coords}
        V = prod(lengths)
        assert len(P) == V
        d = len(lengths)
        j = max(range(d), key=lambda i: lengths[i])
        L = lengths[j]
        assert steps[j] != 0 and L ** d >= V
        # The second shift forces exactly one zero term.
        for b in (F(0), -p0, F(-13, 11)):
            lines = {}
            for n in coords:
                key = tuple(ni for i, ni in enumerate(n) if i != j)
                lines.setdefault(key, []).append(point(n) + b)
            assert len(lines) == V // L
            all_points = [x for line in lines.values() for x in line]
            assert len(set(all_points)) == V
            assert set(all_points) == {p + b for p in P}
            sparse = set(all_points[::2]) | {all_points[-1]}
            z = int(F(0) in sparse)
            assert len([x for x in sparse if x]) == len(sparse) - z
            for line in lines.values():
                assert len(line) == L
                assert all(line[k + 1] - line[k] == steps[j] for k in range(L - 1))
                for q in qs:
                    quotients = [x / q for x in line]
                    D = lcm(*(x.denominator for x in quotients))
                    integral_line = [D * D * x for x in quotients]
                    assert all(x.denominator == 1 for x in integral_line)
                    assert all(integral_line[k + 1] - integral_line[k] == integral_line[1] - integral_line[0] for k in range(L - 1))
                    assert integral_line[1] != integral_line[0]
                    for x, y in zip(line, integral_line):
                        belongs = bool(x) and squareclass(x) == squareclass(q)
                        assert belongs == (bool(y) and rational_square(y))
                    # After reversal if necessary, nonnegative terms are contiguous.
                    ordered = sorted(integral_line)
                    nonnegative = [i for i, x in enumerate(ordered) if x >= 0]
                    assert not nonnegative or nonnegative == list(range(nonnegative[0], L))
                    checks += 1
    return checks


def check_quadratic_pair_algebra():
    # Represent a+b*sqrt(q) by the exact rational pair (a,b).
    checks = 0
    for q, v in product((F(2), F(-1), F(-3), F(5, 7)), (F(1), F(-2, 3), F(7, 5))):
        u = q * v * v - 1
        assert u != 0 and u != -1
        x, y = (F(1, 2), v / 2), (F(1, 2), -v / 2)
        xy = (x[0] * y[0] + q * x[1] * y[1], x[0] * y[1] + x[1] * y[0])
        assert (x[0] + y[0], x[1] + y[1]) == (F(1), F(0))
        assert xy == (-u / 4, F(0))
        assert y == (x[0], -x[1])
        assert squareclass(1 + u) == squareclass(q)
        checks += 1
    for s in range(1, 8):
        assert 8 * (2 * s + 1) + 8 == 16 * s + 16
        assert 8 * (2 * s) + 8 == 16 * s + 8
    return checks


if __name__ == "__main__":
    a = check_anchor_and_scaling()
    g = check_rational_gap_slicing()
    q = check_quadratic_pair_algebra()
    try:
        squareclass(F(0))
    except ValueError:
        pass
    else:
        raise AssertionError("Zero must not be assigned a squareclass")
    print(f"PASS: {a} affine-anchor checks; {g} rational GAP/class-conversion checks; {q} quadratic-pair checks; zero and sign checks")
    print("Fixed exact-rational fixtures only; no witness search and no claim to computationally prove the cited theorems.")
