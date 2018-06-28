# {{cookiecutter.project_name}}

{{cookiecutter.description}}

## Project Organization

```
├── .editorconfig                <- Settings transferrable across text editors.
│                                   See editorconfig.org.
├── .envrc                       <- Set environment variables and automatically
│                                   enter Conda environment when you enter the
│                                   project directory.
├── .gitattributes               <- Git file settings.
├── .gitignore                   <- List of files and folders to not store in
│                                   the Git repository.
├── LICENSE                      <- Open source project license file (optional).
├── Makefile                     <- Makefile with commands like `make code` or
│                                   `make writeup`.
├── README.md                    <- The top-level README for explanation of the
│                                   project.
├── bibliography.bib             <- Bibtex file for the project.
├── environment.yml              <- File for reproducing the analysis
│                                   environment with Conda. Can be generated
│                                   with `conda env export` from within an
│                                   environment.
├── setup.cfg                    <- Python code settings.
│
├── admin                        <- Administrative stuff.
│   ├── calls                    <- Call notes.
│   ├── emails                   <- Email records.
│   │   └── download_emails.py   <- File to download project-related emails
│   │                               from Gmail.
│   ├── etc
│   │   └── META.md              <- Explanation of project structure (outdated).
│   └── project_log.md           <- Project log (Changelog).
│
├── code                         <- Source code for use in this project.
│   ├── __init__.py              <- Makes code a Python module
│   │
│   ├── data                     <- Scripts to download or generate data
│   │   └── make_dataset.py
│   │
│   ├── features                 <- Scripts to turn raw data into features for
│   │   │                           modeling
│   │   └── build_features.py
│   │
│   ├── models                   <- Scripts to train models and then use
│   │   │                           trained models to make predictions
│   │   ├── predict_model.py
│   │   └── train_model.py
│   │
│   └── visualization            <- Scripts to create exploratory and results
│       │                           oriented visualizations
│       └── visualize.py
│
├── data
│   ├── external                 <- Data from third party sources.
│   ├── interim                  <- Intermediate data that has been transformed.
│   ├── processed                <- The final, canonical data sets for modeling.
│   └── raw                      <- The original, immutable data dump.
│
├── docs                         <- Data dictionaries, manuals, and all other
│   │                               explanatory materials.
│   ├── docx                     <- Documentation in Word format.
│   ├── html                     <- Documentation in HTML format.
│   │   └── mkdocs               <- Documentation in HTML format built by
│   │                               Mkdocs.
│   ├── Makefile                 <- Makefile with commands to generate
│   │                               documentation.
│   ├── mkdocs.yml               <- Mkdocs configuration file.
│   ├── pdf                      <- Documentation in PDF format.
│   ├── sphinx                   <- Sphinx documentation. Currently unused and
│   │                               may be removed from the structure.
│   └── src                      <- Documentation source files
│       └── aux                  <- Auxiliary documentation files
│           └── helpers.js       <- Used for Mathjax in Mkdocs
│
├── out                          <- Generated graphics, figures, and tables to
│                                   be used in writeup
│
└── writeup                      <- Generated analysis as HTML, PDF, LaTeX, etc.
    ├── docx                     <- Reports in Word format.
    ├── html                     <- Reports in HTML format.
    ├── md                       <- Reports in Markdown format (except source
    │                               files)
    ├── pdf                      <- Reports in PDF format.
    └── src                      <- Report source files
        ├── lit_review.md
        └── report.pmd

```

Out folder for non-Medicare projects:

```
out
├── fig
├── tab
└── log

```


Out folder for Medicare projects:

```
out
├── 0001
│   ├── fig
│   └── tab
├── 01
│   ├── fig
│   └── tab
├── 05
│   ├── fig
│   └── tab
├── 100
│   ├── fig
│   └── tab
├── 20
│   ├── fig
│   └── tab
└── log
```
