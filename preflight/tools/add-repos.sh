#!/usr/bin/env bash
# Put code snapshots into a run folder for Pre-Flight step 2.
# Usage: add-repos.sh <run-folder> <cutoff "YYYY-MM-DD"> <repo-url> [<repo-url> ...]
# Each repo is cloned, checked out at the last commit on or before the cutoff,
# and its .git folder is removed so the tool cannot see later history.
set -euo pipefail
run="$1"; cutoff="$2"; shift 2
mkdir -p "$run/repos"; cd "$run/repos"
for url in "$@"; do
  name=$(basename "$url"); git clone -q "$url" "$name"
  c=$(git -C "$name" rev-list -1 --before="$cutoff 23:59:59" HEAD)
  git -C "$name" -c advice.detachedHead=false checkout -q "$c"
  echo "$name ${c:0:10} $(git -C "$name" log -1 --format=%ad --date=short)"
  rm -rf "$name/.git"
done
