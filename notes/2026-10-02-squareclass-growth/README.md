# Squareclass growth in structured rational sumsets

**Author:** Pan Yicheng  
**AI assistance:** OpenAI, for literature retrieval, proof development, drafting, and consistency checks  
**Date:** 2 October 2026  
**Status:** Draft for review; not peer reviewed

This note derives two restrictions on structured rational sumsets from known theorems:

1. A fixed squareclass among translates of rational S-units has uniformly bounded multiplicity, using Beukers–Schlickewei
2. Dense subsets of proper generalized arithmetic progressions exhibit polynomial squareclass growth, using Bombieri–Zannier; Green–Ruzsa then gives a bounded-doubling corollary

It includes complete proofs of the deductions, an affine normalization for rational grids, all stated zero and sign cases, explicit constants, and an elementary explanation of the connection to Erdős Problem 885.

**No claim of originality or priority is made. This work does not resolve Erdős Problem 885.** Arbitrary rational coordinate sets need not meet either structural hypothesis.

## Read the note

- [Typeset research note](squareclass_growth.pdf)
- [Editable LaTeX source](squareclass_growth.tex)
- [Exact-rational consistency checker](check_squareclass_identities.py)

The note's bibliography links the primary sources. With a complete standard TeX Live installation, the PDF can be rebuilt by running `pdflatex squareclass_growth.tex` twice. The source uses the standard article, AMS mathematics, geometry, hyperref, and enumitem packages.

## Check the elementary identities

Run:

```sh
python3 check_squareclass_identities.py
```

The script requires Python 3.9 or later and only the standard library. It checks 84 affine-anchor fixtures, 90 progression/class-conversion fixtures, and 12 quadratic-pair fixtures, plus zero and sign checks, using exact rational arithmetic. These checks help catch normalization and bookkeeping mistakes. They are neither a search for square-grid witnesses nor computational proofs of the cited theorems or the unrestricted problem.
