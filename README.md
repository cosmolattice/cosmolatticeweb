# Cosmolattice online documentation

To build the documentation, simply run in this directory:

```bash
bash build.sh
```

The output will be placed in the `website/site/` folder. You can simply view the documentation by opening `website/site/index.html` in your browser, e.g.

```bash
xdg-open website/site/index.html
```

Search does not work when the site is opened this way, because the browser
refuses to start the search worker over `file://`. If you need it, build with
the offline plugin enabled:

```bash
CL_OFFLINE=true bash build.sh
```

That flag is deliberately off by default so the published site does not carry
the shim and the duplicated search index it adds. It changes nothing else --
in particular, no URLs.

## Deployment

**Pushing to `main` publishes to <https://cosmolattice.net>.** There is no
separate deploy step to remember and no staging site: `.github/workflows/docs.yml`
builds on every push, and its `deploy` job -- gated on
`github.ref == 'refs/heads/main'` -- ships the result to GitHub Pages. Pushes to
any other branch build and check but never publish.

GitHub Pages is set to `build_type: workflow`, meaning GitHub builds nothing
itself and serves **only** what that workflow deploys. Two consequences worth
knowing before editing it:

- **Do not replace `actions/upload-pages-artifact` with `actions/upload-artifact`,
  and do not tar the site first.** `deploy-pages` consumes only the reserved
  `github-pages` artifact that the former produces. Packing it yourself still
  deploys *green*, and serves a site whose entire content is one file named
  `site.tar.gz`.
- **`source/docs/CNAME` must keep reaching the built output.** Jekyll used to copy
  a repo-root `CNAME` automatically; MkDocs does not, which is why it lives in
  `docs/`. Deploying without it makes GitHub clear the custom domain, and
  re-attaching re-provisions the TLS certificate -- hours of certificate warnings
  on the live domain. CI asserts its presence; keep that assertion.

A branch rename emits no push event, so if `main` is ever renamed the first
deployment afterwards has to be started by hand:

```bash
gh workflow run docs.yml --ref main
```

### Rollback

The site was migrated from a beautiful-jekyll site in July 2026 (issue #2). That
site is still intact, so reverting is a settings change -- the domain never moves
and DNS is never touched:

```bash
gh api -X PUT repos/cosmolattice/cosmolatticeweb/pages \
  -f build_type=legacy -f 'source[branch]=jekyll-legacy' -f 'source[path]=/'
```

The Jekyll content lives on the protected `jekyll-legacy` branch and the
`jekyll-final` tag.

## Parameter appendix (generated)

The parameter tables in `source/docs/Manual/Appendix_Parameters.md` are **generated**
from the single source of truth `source/data/parameters.yaml` (see
`source/data/parameters.schema.md` for the schema). Only the regions between the
`<!-- @gen:params:KEY -->` / `<!-- @endgen -->` markers are generated; everything
else in the appendix is hand-written prose and is left untouched.

**After editing `parameters.yaml`, regenerate the appendix and commit it:**

```bash
cd documentation
make gen-params      # rewrites the marker regions in Appendix_Parameters.md
```

Useful related targets (run from `documentation/`):

```bash
make check-params       # verify the database is in sync, both directions (no write)
make check-params-code  # only the code<->YAML drift check
make test-params        # run the generator + drift-checker unit tests
make docs               # build the full site (equivalent to bash build.sh)
make help               # list all targets
```

### Keeping `parameters.yaml` honest (two directions)

`make check-params` (also run automatically at the start of `build.sh`) verifies
the parameter database in **both** directions:

1. **Appendix ← YAML** — the generated tables match `parameters.yaml` (runs the
   generator unit tests + a no-write `--check`).
2. **Code ↔ YAML** — every parameter read in the C++ via
   `get<>`/`getOverride<>`/`getSeed` (in `include/` and `models/*.h`) appears in
   `parameters.yaml` with the right scope, and vice versa
   (`scripts/check_params_code.py`). This catches a parameter being
   added/removed/renamed in the code without updating the YAML.

So, before committing changes to `parameters.yaml`, the appendix, or any
`get<>` call site:

```bash
make check-params
# equivalently: bash scripts/check_params_sync.sh
```

If direction 1 fails, run `make gen-params` and commit the result. If direction
2 fails, update `parameters.yaml` to match the code (then `make gen-params`), or
— for an intentional code-only / YAML-only name — add a justified entry to the
`ALLOWLIST` in `scripts/check_params_code.py`. The check is git-independent and
self-contained, so it can be wired into CI unchanged later.
## Repository layout: docs vs code (two-repo workflow)

Since July 2026 the documentation lives in its own repository
(`cosmolattice/cosmolatticeweb`, branch `mkdocs-site`), extracted with full
git history from the `documentation/` folder of the CosmoLattice code
repository. Documentation changes are made **here**; code changes stay in the
code repository.

The build needs **no access to any private repository**: `build.sh` shallow-clones
the public code (branch `CLV2.0Alpha` by default) into
`tmp/code_source/cosmolattice` for the API reference (mkdoxy), `@emgithub`
line-number resolution, and the parameter/model drift checks.

Developers working alongside a local code checkout can point the build at it
instead:

```bash
CL_CODE_SOURCE=/path/to/cosmolattice bash build.sh   # use a local checkout
CL_CODE_BRANCH=SomeBranch bash build.sh              # or another public branch
```

If a code change adds or renames run parameters or models, update
`source/data/parameters.yaml` here and re-run `make check-params` /
`make check-models`; drift against the public code branch is reported by the
build.
