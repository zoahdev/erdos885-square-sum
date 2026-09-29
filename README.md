# Erdős #885 — square-sum constructions (companion archive)

**Author:** Yicheng Pan — a0917212213@gmail.com
**Draft date:** 2026-07-15
**Companion archive for** two preprints on the square-sum problem (Erdős problem [#885](https://www.erdosproblems.com/885)).

> **Neither paper resolves the `k = 5` case of #885.** Both give explicit partial
> constructions with independently recomputable certificates.

---

## Papers

| # | File | Title | Pages |
|---|------|-------|-------|
| A | [`square_sum_specialization.pdf`](square_sum_specialization.pdf) | An explicit 5×4 square-sum specialization and a genus-13 reduction | 6 |
| B | [`moving_lift_quotients.pdf`](moving_lift_quotients.pdf) | A split genus-three lift curve in a moving square-sum construction | 13 |

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
python verify_5x4.py            # 20 sums are squares
python verify_shift_packet.py   # four-shift packet + D-intersection + negative check
```

Exit code `0` = all checks pass. Both scripts are written so that perturbing any
input value makes them fail (verified: changing one digit of `A` flips the exit
code to `1`), so the checks are not vacuous.

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

## Correspondence

- The author has exchanged email with **Andrew Bremner** (who proved the `k = 4`
  case, [Br19]) regarding Erdős problem #885.

> **TODO (author):** add dates, topics discussed, and any feedback or suggestions
> received. This section is deliberately left as a placeholder — no specifics are
> asserted until the author supplies them.

---

## Links

- Forum thread: https://www.erdosproblems.com/885
- Preprint DOI (Zenodo): *TODO — add after Zenodo deposit*
- Forum comment by the author: *TODO — add link after posting*

---

## License

Papers © the author. Verification scripts in this repository are released under the
MIT License; see [`LICENSE`](LICENSE).
