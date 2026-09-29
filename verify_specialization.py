"""Exact rational verification of the m = -8/19 specialization (paper A).

Reproduces, in exact rational arithmetic (fractions.Fraction, no floating point):

1. Choudhry's one-parameter subfamily with (f,g,u1,u2,v1,v2) = (4,1,2,1,3,1):
   the five columns a1..a5 and shifts b1,b2,b3, and that all 15 sums are rational squares.
2. The candidate fourth shift b4 from elliptic-curve addition on (a1, a3, a5).
3. At m = -8/19:  F2 = (35668080/130321)^2 and F4 = (32892048/130321)^2,
   b4 = -15740769200/1172889, and the identities a2 + b4 = 4*F2/D^2, a4 + b4 = 4*F4/D^2.
4. NEGATIVE CONTROL: at m = +8/19 the values F2, F4 are NOT rational squares,
   so the sign of the specialization is forced.
5. The affine-equivalence invariant lambda(B) for the displayed shift set.
6. The integer-shift certificate input: c - a = 291985920 = 2^9*3^2*5*19*23*29
   with 192 parity-compatible factor pairs.

Run: python verify_specialization.py     (exit 0 = all reproduced claims pass)
"""
import math
import sys
from fractions import Fraction as Q

M = Q(-8, 19)                      # the specialization
M_CONTROL = Q(8, 19)               # negative control (wrong sign)

PAPER_F2 = Q(35668080, 130321)
PAPER_F4 = Q(32892048, 130321)
PAPER_B4 = Q(-15740769200, 1172889)
PAPER_LAMBDA_MINE = Q(541359200, 411195147)

A_SET = [202720644, 827712900, 1476864900, 494706564, 80729856900]
B_SET = [0, 358400700, 1398239500, 17139008700]


def is_rational_square(x: Q):
    """Return (True, root) if x is a square of a rational, else (False, None)."""
    n, d = x.numerator, x.denominator
    if n < 0:
        return False, None
    rn, rd = math.isqrt(n), math.isqrt(d)
    if rn * rn == n and rd * rd == d:
        return True, Q(rn, rd)
    return False, None


def columns(m: Q):
    return [
        4 * (24 * m * m + 145 * m - 4) ** 2,
        100 * (24 * m * m + 49 * m + 4) ** 2,
        25 * (97 * m * m + 8) ** 2,
        4 * (24 * m * m - 145 * m - 4) ** 2,
        100 * (24 * m * m - 49 * m + 4) ** 2,
    ]


def shifts13(m: Q):
    return (
        Q(0),
        96 * (3 * m - 4) * (3 * m + 4) * (8 * m - 1) * (8 * m + 1),
        3300 * (m - 1) * (m + 1) * (6 * m - 1) * (6 * m + 1),
    )


def Dpoly(m: Q):
    return 97 * m * m - 8 * m - 8


def b4(m: Q):
    return (Q(12) * (2 * m - 1) * (2 * m + 1) * (3 * m - 1) * (3 * m + 1)
            / Dpoly(m) ** 2
            * (35 * m + 4) * (85 * m - 28) * (89 * m - 20) * (109 * m + 20))


def F2(m: Q):
    return (3252420900 * m ** 8 - 268152720 * m ** 7 - 846520196 * m ** 6
            + 226981960 * m ** 5 + 70762193 * m ** 4 - 37069520 * m ** 3
            - 3000736 * m ** 2 + 1580800 * m + 160000)


def F4(m: Q):
    return (3122350884 * m ** 8 - 865433712 * m ** 7 - 1137811292 * m ** 6
            + 310045192 * m ** 5 + 136716497 * m ** 4 - 33456848 * m ** 3
            - 6350752 * m ** 2 + 978688 * m + 135424)


def lambda_inv(shifts):
    """lambda(B) = (b0-b2)(b1-b3) / ((b0-b3)(b1-b2)) for ordered b0<b1<b2<b3."""
    b = sorted(shifts)
    return Q((b[0] - b[2]) * (b[1] - b[3]), (b[0] - b[3]) * (b[1] - b[2]))


def main() -> int:
    ok = True
    a = columns(M)
    b1, b2, b3 = shifts13(M)
    b4v = b4(M)

    print("== 1. the 5x3 base: all 15 sums a_i + b_j are rational squares ==")
    good15 = all(is_rational_square(ai + bj)[0] for ai in a for bj in (b1, b2, b3))
    print("   15 sums all squares:", good15)
    ok &= good15

    print("\n== 2. candidate fourth shift b4 (elliptic-curve addition) ==")
    print("   b4 =", b4v)
    print("   matches paper -15740769200/1172889 :", b4v == PAPER_B4)
    ok &= (b4v == PAPER_B4)

    print("\n== 3. columns 1,3,5 already work with b4 ==")
    s135 = [is_rational_square(a[i] + b4v)[0] for i in (0, 2, 4)]
    print("   a1+b4, a3+b4, a5+b4 squares:", s135)
    ok &= all(s135)

    print("\n== 4. the two remaining conditions: F2, F4 rational squares ==")
    g2, r2 = is_rational_square(F2(M))
    g4, r4 = is_rational_square(F4(M))
    print("   F2(-8/19) =", r2, " square:", g2, " matches paper:", r2 == PAPER_F2)
    print("   F4(-8/19) =", r4, " square:", g4, " matches paper:", r4 == PAPER_F4)
    ok &= g2 and g4 and (r2 == PAPER_F2) and (r4 == PAPER_F4)

    g24 = is_rational_square(a[1] + b4v)[0]
    g44 = is_rational_square(a[3] + b4v)[0]
    print("   a2+b4 square:", g24, " | a4+b4 square:", g44)
    id2 = (a[1] + b4v) == 4 * F2(M) / Dpoly(M) ** 2
    id4 = (a[3] + b4v) == 4 * F4(M) / Dpoly(M) ** 2
    print("   identity a2+b4 == 4*F2/D^2 :", id2)
    print("   identity a4+b4 == 4*F4/D^2 :", id4)
    ok &= g24 and g44 and id2 and id4

    print("\n== 5. NEGATIVE CONTROL: m = +8/19 must FAIL ==")
    cg2 = is_rational_square(F2(M_CONTROL))[0]
    cg4 = is_rational_square(F4(M_CONTROL))[0]
    print("   F2(+8/19) square:", cg2, " F4(+8/19) square:", cg4, " (both must be False)")
    ok &= (not cg2) and (not cg4)

    print("\n== 6. affine-equivalence invariant lambda(B) ==")
    lam = lambda_inv(B_SET)
    print("   lambda(displayed shifts) =", lam)
    print("   matches paper 541359200/411195147 :", lam == PAPER_LAMBDA_MINE)
    ok &= (lam == PAPER_LAMBDA_MINE)
    print("   NOTE: lambda for the Mausberg packet, recomputed from (0,79200,227205,1258560),")
    print("         is", lambda_inv([0, 79200, 227205, 1258560]),
          "-- the paper states 951142/921557; see README for this open discrepancy.")

    print("\n== 7. integer-shift certificate input ==")
    diff = A_SET[3] - A_SET[0]
    fac = diff == 2 ** 9 * 3 ** 2 * 5 * 19 * 23 * 29
    print("   c - a =", diff, " == 2^9*3^2*5*19*23*29 :", fac)
    pairs = 0
    x = 1
    while x * x <= diff:
        if diff % x == 0:
            y = diff // x
            if (x + y) % 2 == 0:
                pairs += 1
        x += 1
    print("   parity-compatible factor pairs:", pairs, " (paper: 192)")
    ok &= fac and (pairs == 192)

    print("\nALL REPRODUCED CLAIMS PASS:", bool(ok))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
