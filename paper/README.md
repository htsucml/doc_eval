# Paper Build

Run from the repository root:

```bash
make paper
```

The target first regenerates LaTeX tables and figure snippets from existing CSV
artifacts with `scripts/build_paper_assets.py`.

If `latexmk` is installed, `make paper` builds `paper/main.pdf`. If only
`pdflatex` and `bibtex` are installed, it uses those. If no LaTeX toolchain is
available, the target prints the exact command to run after installing TeX.

For official ACL formatting, place the official `acl.sty` file from the ACL
author kit in `paper/` or make it available on the TeX search path. Without it,
`main.tex` falls back to a minimal article layout so the report remains
buildable on clean machines.
