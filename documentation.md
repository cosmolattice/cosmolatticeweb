---
layout: page
title: In a nutshell
# subtitle:
---

<p align="center">
  <img src="../assets/img/CL_iconSequence-removebgbis.png"   alt="drawing" width="800"
 />
</p>



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
For further information, see  Appendix A of the [user-manual](https://arxiv.org/pdf/2102.01031.pdf).
All options of CosmoLattice, as well as how to activate them and how to install the optional external
libraries are explained at length there.


## Download

CosmoLattice can be downloaded from the **GitHub repository**:
<b> <a href="http://github.com/cosmolattice/cosmolattice" target="_blank" rel="noopener noreferrer">cosmolattice/cosmolattice</a></b>
