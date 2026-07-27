#!/usr/bin/env bash
#
# check_params_sync.sh — verify the parameter database is internally consistent
# in three directions:
#
#   1. parameters.yaml  ->  Appendix_Parameters.md  (the appendix is generated)
#   2. C++ source       <-> parameters.yaml         (no parameter has drifted)
#   3. models.yaml      <-> models/*.h              (the model registry matches
#                                                    the shipped model headers)
#
# Run this locally before committing changes to parameters.yaml, the appendix,
# or any get<>/getOverride<>/getSeed call site:
#
#     bash documentation/scripts/check_params_sync.sh
#     # or, from documentation/:  make check-params
#
# Direction 1 runs the generator unit tests and a no-write `--check`: it exits
# non-zero (without modifying any file) if the committed appendix would change.
# Direction 2 runs the code<->YAML drift checker (check_params_code.py) and its
# tests. The script is git-independent and self-contained, so it can later be
# dropped into CI as-is.
#
# Override the interpreter with PYTHON=... (defaults to python3); PyYAML must be
# importable by it (pip install pyyaml).

# By default failures are reported as WARNINGS and the script exits 0, so a docs
# build still succeeds and the site can be published. Pass --strict (CI does) to
# exit non-zero instead when anything is out of sync.
#
# IMPORTANT: $PYTHON must be an interpreter that can import yaml. The default,
# bare `python3`, is usually NOT that interpreter outside an activated venv --
# and when the import fails every check below "fails" identically, which looks
# exactly like real drift. CI therefore passes PYTHON=tmp/.venv/bin/python
# explicitly. If every check fails at once, suspect the interpreter first.
set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON="${PYTHON:-python3}"

strict=0
for arg in "$@"; do
    case "$arg" in
        --strict) strict=1 ;;
        *) echo "usage: $(basename "$0") [--strict]" >&2; exit 2 ;;
    esac
done

# Fail fast and unambiguously if the interpreter cannot do the job, rather than
# letting it surface as four identical "out of sync" warnings.
if ! "$PYTHON" -c "import yaml" 2>/dev/null; then
    echo "error: '$PYTHON' cannot import yaml -- the checks below cannot run." >&2
    echo "       Re-run with PYTHON=/path/to/venv/bin/python (or pip install pyyaml)." >&2
    exit 2
fi

warned=0

# Run a check; on non-zero exit, print a warning (plus any extra hint lines
# passed as further arguments) and keep going instead of failing the build.
run_check() {
    local description="$1"; shift
    # Split args into the command (up to the first "--") and trailing hint lines.
    local -a cmd=() hints=()
    local seen_sep=0
    for arg in "$@"; do
        if [ "$arg" = "--" ] && [ "$seen_sep" -eq 0 ]; then
            seen_sep=1
            continue
        fi
        if [ "$seen_sep" -eq 0 ]; then cmd+=("$arg"); else hints+=("$arg"); fi
    done
    if ! "${cmd[@]}"; then
        echo "" >&2
        echo "warning: $description" >&2
        local hint
        for hint in ${hints[@]+"${hints[@]}"}; do
            echo "         $hint" >&2
        done
        warned=1
    fi
}

echo "==> [1/3] Appendix <- parameters.yaml"

echo "    Running generator unit tests"
run_check "generator unit tests failed" \
    "$PYTHON" "$SCRIPT_DIR/test_gen_param_appendix.py"

echo "    Checking the appendix is in sync with parameters.yaml"
run_check "the parameter appendix is out of sync with parameters.yaml." \
    "$PYTHON" "$SCRIPT_DIR/gen_param_appendix.py" --check \
    -- "Run 'make gen-params' in documentation/ and commit the result."

echo "==> [2/3] Code <-> parameters.yaml"

echo "    Running drift-checker unit tests"
run_check "drift-checker unit tests failed" \
    "$PYTHON" "$SCRIPT_DIR/test_check_params_code.py"

echo "    Checking parameters.yaml matches the get<> call sites"
run_check "parameters.yaml does not match the get<> call sites." \
    "$PYTHON" "$SCRIPT_DIR/check_params_code.py"

echo "==> [3/3] Model registry <-> code"

echo "    Checking models.yaml lists exactly the models in the code"
run_check "the model registry (models.yaml) does not match the models in the code." \
    "$PYTHON" "$SCRIPT_DIR/check_models_registry.py" \
    -- "Update documentation/source/data/models.yaml and run 'make gen-model-caps'."

if [ "$warned" -eq 0 ]; then
    echo "OK: parameter database is in sync (appendix, code, and model registry)."
    exit 0
fi

if [ "$strict" -eq 1 ]; then
    echo "ERROR: parameter database is out of sync (see above)." >&2
    exit 1
fi

echo "WARNING: parameter database checks reported issues (see above); continuing anyway." >&2
exit 0
