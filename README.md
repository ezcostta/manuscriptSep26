# Andreev transport manuscript draft

Reorganized manuscript project for the ferromagnet--bilayer-graphene--superconductor junction.

## Compile

```nu
latexmk -pdf -interaction=nonstopmode -halt-on-error manuscript.tex
```

The current revision removes boxed equations, reformats the longer displays so they fit the two-column PRB layout, and compiles without overfull `\hbox` warnings.

## Structure

- `manuscript.tex`: main RevTeX file
- `sections/`: main-text sections
- `appendices/`: compact appendices
- `figures/`: active figures
- `latex/`: project macros and formatting
- `notes/`: planning notes
