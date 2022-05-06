---
layout: page
title: Version 1.1
subtitle: Released on May 6, 2022
---

We are glad to announce the release 1.1 of CosmoLattice! In particular, this new version comes together with a **gravitational wave** module. We summarize below the main features and bug corrections that
version 1.1 has added with respect to version 1.0.

**New features:**
- Gravitational waves sourced by the scalar sector.
- New ways of computing the spectra. The new default way improves the UV reconstruction of the spectra.

**Bug corrections:**
- Corrected a wrong normalization factor in the occupation number.
- The SU(2) magnetic power spectrum was outputing NaN  instead of machine precision for extremely small amplitudes.
- The initial conditions for the Leapfrog algorithm and the Velocity Verlet one did not conrrespond to the same physical time.
- The last spectra bin was printed twice.
- The 3D hdf5 output was ot working on some architectures (mostly linux based). Special thanks to Chenhuan Wang for pointing this out!
- When using a random seed, every process had a different random seed. This is not a problem per se but makes it impossible to reproduce the simulation with the single seed printed in the info file. Now all the process have the same random seed. Thanks to Jorge Baeza-Ballesteros for pointing this out!