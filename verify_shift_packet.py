"""Verify the four-shift packet and the D-intersection used in paper B.

Checks three things:

1. Four-shift packet (sammausberg, 2026-04-19): for u in {18, 234, 346, 514}
   and every shift r in {0, 79200, 227205, 1258560}, the number u^2 + r is a square.

2. D(79200) n D(227205) n D(1258560) = {36, 468, 692, 1028}, where
   D(N) = {|a - b| : N = a*b}. Recomputed from scratch by divisor enumeration.

3. Negative check: 1029 is NOT in D(79200). (A follow-up comment on the Erdos
   problems forum listed 1029; that is a typo -- 1029^2 + 4*79200 is not a square.)

Run: python verify_shift_packet.py     (exit 0 = all checks pass)
"""
import math
import sys

ABSCISSAE = [18, 234, 346, 514]
SHIFTS = [0, 79200, 227205, 1258560]
NS = [79200, 227205, 1258560]
EXPECTED = {36, 468, 692, 1028}

# Explicit factor-pair certificates for 1028: (a, b) with a*b = N and |a - b| = 1028
CERT_1028 = {79200: (1100, 72), 227205: (1215, 187), 1258560: (1748, 720)}


def is_square(n: int) -> bool:
    r = math.isqrt(n)
    return r * r == n


def D(N: int) -> set:
    """D(N) = {|a - b| : N = a*b}, by divisor enumeration."""
    out = set()
    a = 1
    while a * a <= N:
        if N % a == 0:
            out.add(abs(N // a - a))
        a += 1
    return out


def main() -> int:
    ok = True

    print("== 1. four-shift packet: u^2 + r is a square ==")
    for u in ABSCISSAE:
        row = []
        for r in SHIFTS:
            s = u * u + r
            good = is_square(s)
            ok &= good
            row.append("%d^2" % math.isqrt(s) if good else "FAIL(%d)" % s)
        print("u=%4d:  %s" % (u, "  ".join(row)))

    print("\n== 2. D(79200) n D(227205) n D(1258560) ==")
    inter = D(NS[0])
    for n in NS[1:]:
        inter &= D(n)
    inter = sorted(inter)
    print("recomputed intersection: %s" % inter)
    match = set(inter) == EXPECTED
    print("matches {36, 468, 692, 1028}: %s" % match)
    ok &= match

    print("\n-- factor-pair certificates for 1028 --")
    for N, (a, b) in sorted(CERT_1028.items()):
        good = (a * b == N) and (abs(a - b) == 1028)
        ok &= good
        print("  %d = %d x %d   |diff| = %d   -> %s"
              % (N, a, b, abs(a - b), "OK" if good else "FAIL"))

    print("\n== 3. negative check: 1029 is NOT in D(79200) ==")
    val = 1029 ** 2 + 4 * 79200
    notin = (1029 not in D(79200)) and (not is_square(val))
    print("1029^2 + 4*79200 = %d, is square: %s" % (val, is_square(val)))
    print("1029 not in D(79200): %s" % notin)
    ok &= notin

    print("\nALL CHECKS PASS: %s" % bool(ok))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
