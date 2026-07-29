We welcome everyone to use $\mathcal{C}\mathtt{osmo}\mathcal{L}\mathtt{attice}$ for their own projects — you can freely download it and adapt it to your needs. Whenever you use $\mathcal{C}\mathtt{osmo}\mathcal{L}\mathtt{attice}$ in your research, no matter how much (or how little) you modify (or use) the code, and independently of which part of the code you touch (or use), please cite the basic versions of the code (namely *version 1.0* & *version 2.0*), together with our lattice-cosmology technique monographs $\mathtt{The~Art-I}$ (Ref. [@Figueroa_2020rrl]) and $\mathtt{The~Art-II}$ (Ref. [@BaezaBallesteros_2025tme]), where the basic ideas, algorithms and field-theory methods implemented in $\mathcal{C}\mathtt{osmo}\mathcal{L}\mathtt{attice}$ are explained.

For example, if you use only fundamental fields (*i.e.* scalar and/or gauge fields), you can acknowledge the code with a line like the one below. Copy the ready-to-paste **LaTeX** sentence, or grab the corresponding **BibTeX** entries.

<div class="cl-cite" data-cl-cite>
  <div class="cl-cite__tabs" role="tablist" aria-label="Citation formats">
    <button type="button" class="cl-cite__tab is-active" role="tab" aria-selected="true" data-pane="read">Citation</button>
    <button type="button" class="cl-cite__tab" role="tab" aria-selected="false" data-pane="latex">LaTeX</button>
    <button type="button" class="cl-cite__tab" role="tab" aria-selected="false" data-pane="bibtex">BibTeX</button>
  </div>

  <section class="cl-cite__pane is-active" role="tabpanel" data-pane="read">
    <p class="cl-cite__quote">In this work we use <span class="cl-cite__logo">CosmoLattice</span>, based on the lattice-cosmology techniques presented in <span class="cl-cite__refs">The&nbsp;Art&nbsp;I&nbsp;&amp;&nbsp;II</span>.</p>
    <p class="cl-cite__hint">Open the <b>LaTeX</b> or <b>BibTeX</b> tab to copy the entries.</p>
  </section>

  <section class="cl-cite__pane" role="tabpanel" data-pane="latex" hidden>
    <button type="button" class="cl-cite__copy" data-copy aria-label="Copy the LaTeX citation">
      <span class="cl-cite__copy-label">Copy</span>
    </button>
    <pre class="cl-cite__code"><code>In this work we use CosmoLattice~\cite{Figueroa:2021yhd,Baeza-Ballesteros:2026uao,Florio:2026vde},
based on the lattice-cosmology techniques presented
in~\cite{Figueroa:2020rrl,Baeza-Ballesteros:2025tme}.</code></pre>
  </section>

  <section class="cl-cite__pane" role="tabpanel" data-pane="bibtex" hidden>
    <button type="button" class="cl-cite__copy" data-copy aria-label="Copy all BibTeX entries">
      <span class="cl-cite__copy-label">Copy all</span>
    </button>
    <pre class="cl-cite__code"><code>@article{Figueroa:2021yhd,
    author  = "Figueroa, Daniel G. and Florio, Adrien and Torrent{\'\i}, Francisco and Valkenburg, Wessel",
    title   = "{CosmoLattice: A modern code for lattice simulations of scalar and gauge field dynamics in an expanding universe}",
    journal = "Comput. Phys. Commun.",
    volume  = "283",
    pages   = "108586",
    year    = "2023",
    doi     = "10.1016/j.cpc.2022.108586",
    eprint  = "2102.01031",
    archivePrefix = "arXiv",
    primaryClass  = "astro-ph.CO"
}

@article{Baeza-Ballesteros:2026uao,
    author  = "Baeza-Ballesteros, Jorge and Figueroa, Daniel G. and Florio, Adrien and Loayza, Nicol{\'a}s and Sattler, Franz R. and Torrent{\'\i}, Francisco and Urio, Ander",
    title   = "{CosmoLattice 2.0}",
    year    = "2026",
    eprint  = "2607.24978",
    archivePrefix = "arXiv",
    primaryClass  = "astro-ph.CO",
    reportNumber  = "MS-TP-26-22"
}

@article{Florio:2026vde,
    author  = "Florio, Adrien and Sattler, Franz R.",
    title   = "{TempLat: a versatile C++ engine for lattice field theories}",
    year    = "2026",
    eprint  = "2607.24908",
    archivePrefix = "arXiv",
    primaryClass  = "hep-lat"
}

@article{Figueroa:2020rrl,
    author  = "Figueroa, Daniel G. and Florio, Adrien and Torrent{\'\i}, Francisco and Valkenburg, Wessel",
    title   = "{The art of simulating the early Universe -- Part I: Integration techniques and canonical cases}",
    journal = "JCAP",
    volume  = "04",
    pages   = "035",
    year    = "2021",
    doi     = "10.1088/1475-7516/2021/04/035",
    eprint  = "2006.15122",
    archivePrefix = "arXiv",
    primaryClass  = "astro-ph.CO"
}

@article{Baeza-Ballesteros:2025tme,
    author  = "Baeza-Ballesteros, Jorge and Figueroa, Daniel G. and Florio, Adrien and Lizarraga, Joanes and Loayza, Nicol{\'a}s and Marschall, Kenneth and Opferkuch, Toby and Stefanek, Ben A. and Torrent{\'\i}, Francisco and Urio, Ander",
    title   = "{The art of simulating the early Universe. Part II. Non-canonical cases {\&} gravitational waves}",
    journal = "JCAP",
    volume  = "06",
    pages   = "087",
    year    = "2026",
    doi     = "10.1088/1475-7516/2026/06/087",
    eprint  = "2512.15627",
    archivePrefix = "arXiv",
    primaryClass  = "astro-ph.CO",
    reportNumber  = "DESY-25-191"
}</code></pre>
  </section>
</div>

<!--
If you also use fluids, then the previous acknowledgements should extend also to $\mathcal{C}\mathtt{osmo}\mathcal{L}\mathtt{attice}$ *version 3.0* and to the theory review $\mathtt{The~Art\text{-}III}$ (Ref. [@Figueroa_2026XYZ]), and read something like

*"In this work we use CosmoLattice~\cite{Figueroa:2021yhd,Baeza-Ballesteros:2026uao,Figueroa:2026XYZ}, based on the lattice-cosmology techniques presented in~\cite{Figueroa:2020rrl,Baeza-Ballesteros:2025tme,Figueroa:2026RST}"*
-->

If you have added new features — new dynamics (*e.g.* new interactions), a new observable (*e.g.* a field correlator), etc. — you can also add, after the citation, a line such as:

*"We have modified the module [...] so that the code can run the dynamics of [...]"* or *"We have added a new observable for [...]"*, etc.

<!-- 

OLD STUFF:

We welcome everyone to use CosmoLattice for their own projects. Whenever using CosmoLattice in your research, no matter how much (or little) you modify (or use) the code, and independently of which part of the code you touch (or use), please cite the basic versions of the code (namely version 1.0 & version 2.0), together with our lattice cosmology technique monographs $\mathtt{The~Art-I}$[@Figueroa_2020rrl] and $\mathtt{The~Art-II}$[@BaezaBallesteros_2025tme] where the basic ideas, algorithms and field theory methods implemented in CosmoLattice are explained. For example, if you use only fundamental fields (*i.e.* scalar and/or gauge fields), you could use a line as follows:

*"In this work we use CosmoLattice~\cite{Figueroa:2021yhd,Baeza-Ballesteros:2026uao}, based on the lattice-cosmology techniques presented in~\cite{Figueroa:2020rrl,Baeza-Ballesteros:2025tme}"*

If you also use fluids, then the previous acknowledgements should extend also to CosmoLattice *version 3.0* and to theory review $\mathtt{The~Art-III}$[@Figueroa:2026XYZ], and read something like

*"In this work we use CosmoLattice~\cite{Figueroa:2021yhd,Baeza-Ballesteros:2026uao,Figueroa:2026XYZ}, based on the lattice-cosmology techniques presented in~\cite{Figueroa:2020rrl,Baeza-Ballesteros:2025tme,Figueroa:2026RST}"*

If you have added new features, like new dynamics (*e.g.* new interactions), or built some new observable (*e.g.* a field correlator), etc, after citation, you can also add something like

*"We have modified the module [...] so that the code can run the dynamics of [...]"* 
*"We have added a new observable for [...]"*.
*etc*
 -->