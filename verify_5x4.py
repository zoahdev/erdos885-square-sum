"""Verify the explicit 5x4 square-sum specialization (paper A).

Claim: for A (5 values) and B (4 values) below, every sum a + b is a perfect square.
This is a partial construction related to Erdos problem #885 (k=5 square-sum).
It does NOT resolve k = 5.

Run: python verify_5x4.py     (exit 0 = all checks pass)
"""
import math
import sys

A = [202720644, 827712900, 1476864900, 494706564, 80729856900]
B = [0, 358400700, 1398239500, 17139008700]


def is_square(n: int) -> bool:
    r = math.isqrt(n)
    return r * r == n


def main() -> int:
    ok = True

    print("== 5x4 square-sum specialization: every a + b is a square ==")
    for a in A:
        row = []
        for b in B:
            s = a + b
            good = is_square(s)
            ok &= good
            row.append("%d^2" % math.isqrt(s) if good else "FAIL(%d)" % s)
        print("a=%12d:  %s" % (a, "  ".join(row)))

    # Shape checks: 5 distinct rows, 4 distinct columns
    distinct_a = len(set(A)) == len(A)
    distinct_b = len(set(B)) == len(B)
    print("\ndistinct |A| = %d (expect 5): %s" % (len(set(A)), distinct_a))
    print("distinct |B| = %d (expect 4): %s" % (len(set(B)), distinct_b))
    ok &= distinct_a and distinct_b

    total = len(A) * len(B)
    print("total pairs checked: %d" % total)
    print("\nALL %d SUMS SQUARE: %s" % (total, bool(ok)))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
