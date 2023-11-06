---
layout: page
title: Version 1.3
subtitle: Released on Novermber 6, 2023
---

Version 1.3 of CosmoLattice is now publicly available. The main change corrects the excess of memory that is used by CosmoLattice.

**Changes:**

- Excess memory use corrected. The memory (in GB) required now is roughly 8*2*N^3*(Ndof+0.75)/(2^30), N = number of points per dimension, Ndof = Number of degrees of freedom.
- Ocupation number is now optional for scalar singlets and is off by default. To switch it on, set OccNumb=true in the input parameter file.
