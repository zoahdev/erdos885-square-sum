# Erdős #885 — square-sum constructions (companion archive)

**Author:** Yicheng Pan — a0917212213@gmail.com
**Draft date:** 2026-07-15
**Companion archive for** two preprints on the square-sum problem (Erdős problem [#885](https://www.erdosproblems.com/885)).

> **Neither paper resolves the `k = 5` case of #885.** Both give explicit partial
> constructions with independently recomputable certificates.

---

## Papers

| # | File | Title | Pages | DOI |
|---|------|-------|-------|-----|
| A | [`square_sum_specialization.pdf`](square_sum_specialization.pdf) | An explicit 5×4 square-sum specialization and a genus-13 reduction | 6 | [10.5281/zenodo.23040929](https://doi.org/10.5281/zenodo.23040929) |
| B | [`moving_lift_quotients.pdf`](moving_lift_quotients.pdf) | A split genus-three lift curve in a moving square-sum construction | 13 | [10.5281/zenodo.23040933](https://doi.org/10.5281/zenodo.23040933) |

Both are deposited on Zenodo (CC-BY-4.0, `publication_type: preprint`, publication date
`2026-07-15`): <https://zenodo.org/records/23040929> and
<https://zenodo.org/records/23040933>. The Zenodo deposits include the PDF plus the
verification scripts listed below.

### A — explicit 5×4 specialization

For
```
A = {202720644, 827712900, 1476864900, 494706564, 80729856900}   (5 rows)
B = {0, 358400700, 1398239500, 17139008700}                      (4 columns)
```
every one of the 20 sums `a + b` is a perfect square. From this a genus-13
reduction is derived. Builds on Choudhry's rational (5,3) family.

### B — moving lift curve

Constructs a moving genus-3 lift curve whose Jacobian splits; ranks 12/16 computed
with Magma/PARI certificates. Builds on sammausberg's four-shift packet
`(0, 79200, 227205, 1258560)` with square abscissae `18², 234², 346², 514²`, and on
Choudhry's rational (5,3) family.

---

## Verification

All numeric claims are recomputed from scratch by two self-contained scripts
(Python ≥3.8, standard library only).

```bash
python verify_5x4.py             # 20 sums are squares
python verify_shift_packet.py    # four-shift packet + D-intersection + negative check
python verify_specialization.py  # m = -8/19 in exact rational arithmetic + negative control
```

Exit code `0` = all checks pass. The scripts are written so that perturbing any
input value makes them fail (verified: changing one digit of `A`, or replacing
`m = -8/19` by `-8/17`, flips the exit code to `1`), so the checks are not vacuous.

`verify_specialization.py` reproduces the `m = -8/19` specialization in exact rational
arithmetic (`fractions.Fraction`, no floating point): the 15 base sums, the candidate
fourth shift `b4 = -15740769200/1172889` from elliptic-curve addition, the evaluations
`F2 = (35668080/130321)²` and `F4 = (32892048/130321)²`, the identities
`a2 + b4 = 4·F2/D²` and `a4 + b4 = 4·F4/D²`, the invariant `λ(B) = 541359200/411195147`,
and the certificate input `c − a = 291985920 = 2⁹·3²·5·19·23·29` with its 192 parity-
compatible factor pairs. It also carries a **negative control**: at `m = +8/19` the
values `F2`, `F4` are *not* rational squares, so the sign of the specialization is forced.

**Results reproduced:**

- `verify_5x4.py` — all 20 sums are squares; roots range `14238² … 312840²`.
- `verify_shift_packet.py` —
  1. `u² + r` is a square for all `u ∈ {18, 234, 346, 514}`, `r ∈ {0, 79200, 227205, 1258560}`.
  2. `D(79200) ∩ D(227205) ∩ D(1258560) = {36, 468, 692, 1028}`, where
     `D(N) = {|a − b| : N = a·b}`. Factor-pair certificates for `1028`:
     `79200 = 1100 × 72`, `227205 = 1215 × 187`, `1258560 = 1748 × 720`.
  3. **Negative check:** `1029 ∉ D(79200)`, since `1029² + 4·79200 = 1375641` is not
     a square. (A follow-up comment on the #885 forum listed `1029`; that value is a
     typo — the correct value is `1028`, matching sammausberg's 2026-04-19 note.)

---

## Related work

- **Erdős–Rosenfeld [ErRo97]** — proved the statement for `k = 2`.
- **Jiménez-Urroz [Ji99]** — `k = 3`.
- **Bremner [Br19]** — `k = 4`.
- **Choudhry, arXiv:2508.07806** — rational `(m,n) = (3,3), (5,3), (4,4)` families;
  used by both papers here.
- **sammausberg**, #885 forum note, 2026-04-19 — the four-shift packet above and the
  `D`-intersection `{36, 468, 692, 1028}`.
- **Aleksanndr_NFA**, #885 forum comment, 2026-09-23 — reformulation, the genus-one
  curve behind three common differences, an explicit `k = 4` example, and a search
  over 8410 primitive triples that found no five numbers sharing four differences.

None of the above claims a resolution of `k = 5`, and neither do the papers here.

---

## Known discrepancy (open)

Paper A §4 states that the Mausberg shift set has

```
λ(Mausberg) = 951142 / 921557 .
```

Recomputing the same invariant from the four-shift packet `(0, 79200, 227205, 1258560)`
used elsewhere in these notes gives `28917 / 20102`, **not** `951142 / 921557`.
The invariant for the shift set in paper A reproduces exactly
(`λ = 541359200 / 411195147`), so the formula and its implementation agree with the
paper; the mismatch is therefore either a typo in the paper or a reference to a
different Mausberg packet than the one above.

**This does not affect the qualitative claim** — the two invariant values are unequal
either way, so the example is not affinely equivalent to Mausberg's — but the printed
fraction should be checked against the source `.tex` before publication.

---

## Correspondence

- The author has exchanged email with **Andrew Bremner** (who proved the `k = 4`
  case, [Br19]) regarding Erdős problem #885.

> **TODO (author):** add dates, topics discussed, and any feedback or suggestions
> received. This section is deliberately left as a placeholder — no specifics are
> asserted until the author supplies them.

---

## Links

- Forum thread: https://www.erdosproblems.com/885
- Preprint A (Zenodo): https://zenodo.org/records/23040929 — DOI `10.5281/zenodo.23040929`
- Preprint B (Zenodo): https://zenodo.org/records/23040933 — DOI `10.5281/zenodo.23040933`
- Forum comment by the author: *TODO — add link after posting*

---

## License

Papers © the author. Verification scripts in this repository are released under the
MIT License; see [`LICENSE`](LICENSE).
