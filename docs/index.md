<p align="center">
  <img src="images/CL_iconSequence-removebgbis.png"   alt="drawing" width="800"
 />
</p>

# What is CosmoLattice?

CosmoLattice is a modern package for **lattice simulations of field dynamics in 
an expanding universe**. We have developed CosmoLattice to provide a 
new up-to-date, relevant numerical tool for the scientific community working in the **physics 
of the early universe**.

The current version of CosmoLattice (**version 1.0**) can simulate the dynamics of i) interacting
scalar field theories, ii) Abelian U(1) gauge theories, and iii) non-Abelian SU(2) gauge theories, either
in flat spacetime or an expanding FLRW background, including the case of self-consistent expansion sourced by
the fields themselves. CosmoLattice is ready to simulate the dynamics of field theories described by an action 
and a background metric of the type:

<p align="center">
  <img src="images/action.svg" width="890"
 />
</p>


<p align="center">
  <img src="images/metric.svg" width="300"
 />
</p>

We have conceived CosmoLattice as an **evolving package that we plan to upgrade successively**, 
by further developing modules for new tasks. To mention just a few, we plan to add e.g. the computation of gravitational waves (**now in development**), new initialization routines, and different evolution algorithms. CosmoLattice is in fact a platform to implement any system of dynamical equations suitable for discretization on a lattice, as it introduces its own language describing fields and operations between them, and hence it is a natural platform to implement new libraries to solve arbitrary field problems (related or not to cosmology).


## Some features:

CosmoLattice incorporates a series of features that makes it very versatile and powerful. 
We list some of them:
 
-  It is written in **C++**, and  fully exploits the object oriented programming paradigm, 
with a modular structure and a clear separation between the physics and the technical details.
-  It is **MPI-based** and uses a **discrete Fourier transform parallelized in multiple 
spatial dimensions**, which makes it specially appropriate for probing scenarios with 
well-separated scales, running very high resolution simulations, or simply very long ones.
- It introduces its own **symbolic language**, defining field variables and operations 
over them. This way, one can introduce differential equations and operators in a manner 
as close as possible to the continuum.
-  it includes a library of **numerical algorithms**, ranging from second-order to tenth-order 
accuracy methods, suitable for simulating global and gauge theories 
in an expanding grid.
- Our evolution algorithms **conserve energy up** to the accuracy set by the order of the evolution 
algorithm, reaching even machine precision in the case of the highest order integrators. 
- All our evolution algorithms for gauge theories (for both Abelian and non-Abelian) respect the **Gauss constraint to machine precision**.
- **Relevant observables** are provided for each algorithm, such as field average amplitudes, relevant field 
spectra,  energy density components, or 3D lattice snapshots. 
- It comes with the core library **TempLat**, which implements fields and algebraic operations and the handling of the parallelization technical details. It works **in arbitrary dimensions** (smaller or larger than 3), which makes it an ideal tool to develop new modules to solve problems in higher dimensions.


## Documentation

- ***The Art of Simulating the Early Universe*** **[arXiv:2006.15122](https://arxiv.org/pdf/2006.15122.pdf)** . 
A dissertation on lattice techniques for the simulation of scalar-gauge field theories. 
It provides the theoretical basis for the equations implemented in CosmoLattice. 

- _**CosmoLattice user manual**_  **[arXiv:2102.01031](https://arxiv.org/pdf/2102.01031.pdf)** .  
A manual that explains in detail the use and structure of the code, including: 1) how to install 
CosmoLattice and the different required libraries, 2) the general structure of the code and 
the most important files, 3) how to set up and run a simulation for the first time, for both 
scalar and scalar-gauge theories.

## Basic installation

*Minimal requirements:* `CMake` version 3 or above, `g++` version 5 or above, `fftw3`.

```
git clone https://github.com/cosmolattice/cosmolattice.git
cd cosmolattice   
mkdir build                     
cd build                        
cmake -DMODEL=lphi4 ../
make cosmolattice
```

This will compile the ``lphi4`` model. To run it with the default input file, you can do

``
./lphi4 input=../src/models/parameter-files/lphi4.in
``

The above commands just represent a very brief guide for the installation and execution of CosmoLattice. 
For further information, see  Appendix A of the [user-manual](https://arxiv.org/pdf/2102.XXXXX.pdf).
All options of CosmoLattice, as well as how to activate them and how to install the optional external 
libraries are explained at length there.

## If you use CosmoLattice

- CosmoLattice is freely available to anyone who wants to use or modify it. However, whenever 
using CosmoLattice in your research, no matter how much (or little) you modify the code, 
<b>please cite both [arXiv:2006.15122](https://arxiv.org/pdf/2006.15122.pdf)  
and  [arXiv:2102.01031](https://arxiv.org/pdf/2102.01031.pdf) in your papers</b>. 

- Also, if you publish a paper using CosmoLattice, we would love to hear about it. We 
plan to keep an **updated list of papers** using the code on this website.

- Finally, if you would like to **help developing** some aspects of CosmoLattice, or even 
implement your own modules with some new functionality we have not envisaged, please contact 
us and let us know about your idea(s).

## Download

CosmoLattice can be downloaded from the **GitHub repository**: 
<b> <a href="http://github.com/cosmolattice/cosmolattice" target="_blank" rel="noopener noreferrer">cosmolattice/cosmolattice</a></b>


## Mailing list

We have created a mailing list in order to share information on new updates, report bugs, 
inform about events, etc.  In order to subscribe, send a blank e-mail to: 
<a href="mailto:cosmolattice+subscribe@googlegroups.com">**cosmolattice+subscribe@googlegroups.com**</a>

## Authors

- Daniel G. Figueroa
- <a href="https://afloriosite.wordpress.com/" target="_blank" rel="noopener noreferrer"> Adrien Florio </a>
- Francisco Torrenti
- Wessel Valkenburg

## Contact
 If you have any questions or comments about CosmoLattice, please send us an e-mail to: **<daniel.figueroa@ific.uv.es>**, **<adrien.florio@stonybrook.edu>**, **<f.torrenti@unibas.ch>**
