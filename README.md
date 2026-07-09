# Water Graph Art

A collection of Python and Shell scripts designed to create "git art" on your GitHub contribution graph using water and ripple themes.

## Scripts

- **`fast_ripple.sh`**: Generates concentric ripple patterns using `git commit-tree` for high-speed commit generation.
- **`generate_ripples.py`**: Creates interference patterns simulating two water drops using `git commit --allow-empty`.
- **`rain_grid.py`**: Simulates matrix-style heavy rain drops falling down the commit grid.

## Usage

Run the desired script locally to generate a fresh `.git` history containing the art pattern, then force push to a repository to update your contribution graph.

> **Note:** These scripts rewrite git history and are intended for empty or dedicated "art" repositories.
