# Publishing runbook — Stage C / Phase 7

The flip that makes this MkDocs site replace the beautiful-jekyll site at
<https://cosmolattice.net>. Tracking issue: `cosmolattice/cosmolatticeweb#2`.

> **Read section 2 in full before starting.** The steps are ordered, and step b
> in particular exists to close a window that is expensive to reopen.

Downtime during the flip is acceptable — that was an explicit call. What is
*not* acceptable is losing the custom domain, because re-attaching it
re-provisions the TLS certificate and can leave `cosmolattice.net` throwing
certificate warnings for hours. That is a worse failure than being offline.

---

## 0. What actually connects this repo to the live site

Exactly one thing: the Pages configuration. Today:

```bash
gh api repos/cosmolattice/cosmolatticeweb/pages \
  --jq '{build_type, branch: .source.branch, cname, status}'
# {"build_type":"legacy","branch":"main","cname":"cosmolattice.net","status":"built"}
```

`legacy` means GitHub builds `main` with Jekyll itself. The moment it becomes
`workflow`, GitHub stops building anything and serves **only** what a workflow
has deployed. There is no automatic fallback: if no deployment has ever
succeeded, there is nothing to serve.

---

## 1. Preconditions

- [ ] Latest CI run on `mkdocs-site` is green, including
      `Assert CNAME, 404, feed and redirect stubs in output`.
- [ ] `website/site/CNAME` contains exactly `cosmolattice.net` in that run.
      This is the single highest-value check in the whole flip.
- [ ] Tag the Jekyll branch and take a mirror, both as rollback anchors:
      ```bash
      git tag -a jekyll-final -m "Jekyll site as served before the MkDocs flip" origin/main
      git push origin jekyll-final
      git clone --mirror git@github.com:cosmolattice/cosmolatticeweb.git \
        ~/cosmolatticeweb-preflip-mirror.git
      ```
- [ ] Note the current Pages config (section 0) so you can compare afterwards.

---

## 2. The flip

Run these in order. Each step says what to check before moving on.

### a. Rename the Jekyll branch out of the way

```bash
gh api -X POST repos/cosmolattice/cosmolatticeweb/branches/main/rename \
  -f new_name=jekyll-legacy
```

A rename is a native operation, not delete-and-recreate, so the existing
`allow_deletions: false` rule does not block it. `enforce_admins` is `false`
and you are an admin, so protection does not block it either — **nothing needs
to be unprotected first.**

### b. Pin Pages to the retired branch — **do not skip**

Pages may or may not have followed the rename in step a. Do not find out the
hard way; pin it:

```bash
gh api -X PUT repos/cosmolattice/cosmolatticeweb/pages \
  -f 'source[branch]=jekyll-legacy' -f 'source[path]=/'

gh api repos/cosmolattice/cosmolatticeweb/pages \
  --jq '{build_type, branch: .source.branch, cname, status}'
# want: legacy / jekyll-legacy / cosmolattice.net / built
```

Idempotent: a no-op if Pages already followed, a fix if it did not.

**Why this is the one step to be careful about, downtime tolerance
notwithstanding.** If Pages were left pointing at `main` while step c creates a
new `main` full of MkDocs sources, Pages — still in legacy mode — would try to
*Jekyll-build the MkDocs repo* and publish that over `cosmolattice.net`. That
branch has no `CNAME` at its repo root (ours lives at `source/docs/CNAME` and
only reaches the root of the built output), and publishing a Jekyll build with
no root `CNAME` is the documented way to have GitHub silently clear the custom
domain. Re-attaching it re-provisions the TLS certificate: hours of
certificate warnings on the live domain. Running this step closes that window
by construction instead of by assumption.

Do not continue until `cname` above still reads `cosmolattice.net`.

### c. Promote the MkDocs branch

```bash
gh api -X POST repos/cosmolattice/cosmolatticeweb/branches/mkdocs-site/rename \
  -f new_name=main
```

Pages is pinned to `jekyll-legacy` by step b, so this new `main` is not a
publishing source and nothing rebuilds. Confirm that is still true:

```bash
gh api repos/cosmolattice/cosmolatticeweb/pages \
  --jq '{build_type, branch: .source.branch, cname}'
# want: legacy / jekyll-legacy / cosmolattice.net
```

### d. Take the default branch back

Step a moved `default_branch` to `jekyll-legacy` along with the rename. Step c
does **not** claim it back — that rename has no idea it is recreating the
branch that used to be default. Left alone you get `default_branch =
jekyll-legacy`, i.e. `git clone` checks out the retired Jekyll site, new PRs
and issues target it, and the web UI opens on it, so the repo looks like the
migration never happened. Pages is unaffected either way; this is about
everyone else.

```bash
gh api -X PATCH repos/cosmolattice/cosmolatticeweb -f default_branch=main
gh api repos/cosmolattice/cosmolatticeweb --jq '.default_branch'   # want: main
```

Idempotent — harmless if `main` somehow already is the default.

### e. Re-protect the branches

GitHub carries a protection rule along with the branch it names. After the two
renames that leaves the rule on `jekyll-legacy` — the retired branch — while
the new `main` has none, because `mkdocs-site` never had one. That is
backwards, and it matters more now than it used to: `main` is the branch the
deploy job publishes from, so an unguarded force-push to it publishes whatever
it likes to `cosmolattice.net`.

```bash
gh api -X PUT repos/cosmolattice/cosmolatticeweb/branches/main/protection \
  --input - <<'JSON'
{ "required_status_checks": null,
  "enforce_admins": false,
  "required_pull_request_reviews": null,
  "restrictions": null,
  "allow_force_pushes": false,
  "allow_deletions": false }
JSON
```

Then verify both, rather than trusting that the rename moved things as
documented:

```bash
for b in main jekyll-legacy; do
  echo -n "$b: "
  gh api repos/cosmolattice/cosmolatticeweb/branches/$b/protection \
    --jq '{force: .allow_force_pushes.enabled, del: .allow_deletions.enabled}' \
    2>&1 | tail -1
done
# want: both branches present, force=false, del=false
```

Keep `jekyll-legacy` protected. It is the rollback target; it must not be
deletable.

These settings deliberately mirror what `main` had before — `enforce_admins:
false`, no required reviews, no required status checks. Adding required checks
would be a genuine improvement but changes how everyone works day to day, and
that is a decision to take separately from the flip. Note the deploy job
already cannot publish a broken build: it is `needs: build`.

### f. Point Pages at Actions

This is the step that takes the Jekyll site out of service. From here until
step g completes there is no current deployment, so expect the site to be down
or stale in between — that is the accepted downtime, and it is the only
stretch of it.

```bash
gh api -X PUT repos/cosmolattice/cosmolatticeweb/pages -f build_type=workflow

gh api repos/cosmolattice/cosmolatticeweb/pages --jq '{build_type, cname}'
# want: workflow / cosmolattice.net
```

If `cname` came back `null` here, **stop and do not proceed to step g.**
Re-set it before deploying:

```bash
gh api -X PUT repos/cosmolattice/cosmolatticeweb/pages -f cname=cosmolattice.net
```

Deploying while the custom domain is unset is what triggers the certificate
re-provisioning described at the top of this file.

### g. Start the first deployment by hand

**A branch rename emits no push event**, so nothing fires automatically after
step c. The first deployment has to be dispatched:

```bash
gh workflow run docs.yml --ref main
gh run watch "$(gh run list --workflow docs.yml --limit 1 --json databaseId --jq '.[0].databaseId')"
```

The `deploy` job is gated on `github.ref == 'refs/heads/main'`, so this is the
first time it will ever have run. Everything before this point has only
exercised `build`.

---

## 3. Verification

```bash
curl -sSI https://cosmolattice.net           | head -1   # 200
curl -sSI https://www.cosmolattice.net       | head -1   # redirect
curl -sS   https://cosmolattice.net/CNAME               # cosmolattice.net
gh api repos/cosmolattice/cosmolatticeweb/pages \
  --jq '{build_type, cname, status}'                    # workflow / cosmolattice.net / built
```

Then by hand:

- [ ] `/` shows **What is CosmoLattice ?**, not an install README.
- [ ] HTTPS valid and enforced; no certificate warning.
- [ ] Old permalinks redirect: `/features`, `/download`, `/usermanual`,
      `/people`, `/publications` …
- [ ] `/feed.xml` returns the RSS document, and its five item links resolve.
- [ ] A deliberately missing deep URL, e.g. `/Manual/NoSuchPage.html`, shows
      the styled 404 — logo and CSS present, not a bare unstyled page.
- [ ] Equations render; `@emgithub` embeds load; search returns results.

---

## 4. Rollback

The domain never moves and DNS is never touched, so rollback is a Pages
setting change:

```bash
gh api -X PUT repos/cosmolattice/cosmolatticeweb/pages \
  -f build_type=legacy -f 'source[branch]=jekyll-legacy' -f 'source[path]=/'
```

The Jekyll content is also preserved on the `jekyll-final` tag and in the
pre-flip mirror from section 1.
