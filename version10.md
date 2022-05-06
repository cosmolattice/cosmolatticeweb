---
layout: page
title: Version 1.0
subtitle: Released on February 1, 2021
---

<p>CosmoLattice is a modern package for <strong>lattice simulations of field dynamics in 
an expanding universe</strong>. We have developed CosmoLattice to provide a 
new up-to-date, relevant numerical tool for the scientific community working in the <strong>physics 
of the early universe</strong>.</p>

<p>Version 1-0 of CosmoLattice can simulate the dynamics of i) interacting
scalar field theories, ii) Abelian U(1) gauge theories, and iii) non-Abelian SU(2) gauge theories, either
in flat spacetime or an expanding FLRW background, including the case of self-consistent expansion sourced by
the fields themselves. CosmoLattice is ready to simulate the dynamics of field theories described by an action 
and a background metric of the type:</p>

<p align="center">
  <img src="../assets/img/action.svg" width="890"
 />
</p>


<p align="center">
  <img src="../assets/img/metric.svg" width="300"
 />
</p>

<p>We have conceived CosmoLattice as an <strong>evolving package that we plan to upgrade successively</strong>, 
by further developing modules for new tasks. To mention just a few, we plan to add e.g. the computation of gravitational waves (now developed in version 1.1), new initialization routines, and different evolution algorithms. CosmoLattice is in fact a platform to implement any system of dynamical equations suitable for discretization on a lattice, as it introduces its own language describing fields and operations between them, and hence it is a natural platform to implement new libraries to solve arbitrary field problems (related or not to cosmology).</p>

<h2 id="some-features">Some features:</h2>

<p>CosmoLattice incorporates a series of features that makes it very versatile and powerful. 
We list some of them:</p>

<ul>
  <li>It is written in <strong>C++</strong>, and  fully exploits the object oriented programming paradigm, 
with a modular structure and a clear separation between the physics and the technical details.</li>
  <li>It is <strong>MPI-based</strong> and uses a <strong>discrete Fourier transform parallelized in multiple 
spatial dimensions</strong>, which makes it specially appropriate for probing scenarios with 
well-separated scales, running very high resolution simulations, or simply very long ones.</li>
  <li>It introduces its own <strong>symbolic language</strong>, defining field variables and operations 
over them. This way, one can introduce differential equations and operators in a manner 
as close as possible to the continuum.</li>
  <li>it includes a library of <strong>numerical algorithms</strong>, ranging from second-order to tenth-order 
accuracy methods, suitable for simulating global and gauge theories 
in an expanding grid.</li>
  <li>Our evolution algorithms <strong>conserve energy up</strong> to the accuracy set by the order of the evolution 
algorithm, reaching even machine precision in the case of the highest order integrators.</li>
  <li>All our evolution algorithms for gauge theories (for both Abelian and non-Abelian) respect the <strong>Gauss constraint to machine precision</strong>.</li>
  <li><strong>Relevant observables</strong> are provided for each algorithm, such as field average amplitudes, relevant field 
spectra,  energy density components, or 3D lattice snapshots.</li>
  <li>It comes with the core library <strong>TempLat</strong>, which implements fields and algebraic operations and the handling of the parallelization technical details. It works <strong>in arbitrary dimensions</strong> (smaller or larger than 3), which makes it an ideal tool to develop new modules to solve problems in higher dimensions.</li>
</ul>

