# Folder Structure

## Overview

The root of this repository is in `$main`. The basic layout is:

- `admin`: Contains administrative stuff. Most notably `admin/emails` with
    e-mail exchanges I was a part of that pertain to the project.
- `code`: Contains the project main code.
- `docs`: Contains documentation (including this)
- `data`: Contains all project data
- `lib`: Libraries and aux files that can be shared by all code.
- `out`: Contains non-data output.
- `writeup`: Contains drafts, write-ups, etc. to be shared.

## Detailed Structure

- `admin/` contains administrative stuff. Notably
    - `admin/calls/` records all calls/meetings I was a part of.
    - `admin/emails/` contains all e-mail exchanges I was a part of that pertain to the project. Folders are named after the earliest e-mail in the thread they belong to: `YYYY-MM-DD - Subject`. Each file within those folders is an email in Markdown format, which is a plain text file that can be rendered as HTML, PDF, or DOCX (using [Pandoc](https://pandoc.org)).
        - `download_emails.py` is a short script to download emails for a given query from Gmail. (This assumes your project emails are stored in Gmail, of course.) Set up the authentication using the instructions [here](https://github.com/kylebarron/gmail_download/blob/master/README.md).
    - `admin/project.log.md`, is a chronological account of events in the project. Though it is not a great practice, I often do not record events in this file and let my Git history speak for itself.
- `tmp/` contains temporary files, as applicable.
- `lib/` contains external files that I use in every project. In particular it includes [this repository](https://github.com/kylebarron/lib).
- `README.md` is the top-level file with the overview of the project.

The main folders to generate output are `code` and `writeup`. All raw files that produce output will be in these two folders, and other folders should be thought of as auxiliary.

- `code/` contains the project's main code.
    - Folders in code are discrete steps in the project.
    - In each folder, files are numbered starting from `01` in the order in which they should be run. This numbering is usually kept up to date, but the project `Makefile` is the authoritative source of file dependencies. See the [`Makefile`](#makefile) section for more details.
    - `00` files typically contain auxiliary scripts to be called by other scripts.
    - `99` files typically contain test, beta, or one-off code.
    - There are sometimes symbolic links to `out`, `lib`, and `data` folders.
- `writeup/` contains all reports written that are related to the project. This includes all deliverable output, including summaries, reviews, analysis, power, etc.

The main auxiliary folders to `code` and `writeup` are `data` and `out`.

- `data/` contains input and output data, raw and processed files.
- `out/` contains processed output. Typically figures and tables.

`code`, `writeup`, `out`, and `data` have a common folder structure:

- Folders are numbered starting from `01` in the order in which the project step/request/part was done; e.g. `01data-pull`.
- `00` folders are auxiliary folders that have no particular order and are typically used by other folders.
- `99` folders are small discrete requests that do not necessarily fit elsewhere in the project.
- Sub-steps from the same request are sub-numbered. For example:
    ```
    03data-01query
    03data-02process
    ```
- Folders in `code` and `writeup` have analogues in all four folders as applicable. e.g.
    - `code/01data-pull` would contain the code that generates data/output/etc. for this part of the project is in
    - `writeup/01data-pull`
    - Raw files would usually be in `data/01data-pull/raw`
    - Processed data files would usually be in `data/01data-pull`
    - Output would always be in `out/01data-pull`

Naturally it is not always necessary for every folder created in `code` or `output` to have analogues everywhere. For instance, a literature review may only require content to be created in `writeup`. A `code` step may only involve data manipulation. However, generally speaking there are only two exceptions to this folder structure:

1. A given folder in `data` may contain files that are used in multiple steps of the project. There is no perfect way to handle this (the general version of this problem is what programmers call "dependency hell"). My preferred way is to use symbolic links (shortcuts). If your new step is `04bootstrap` and will use data from `01data-pull`, then create something like `data/04bootstrap/data-pull` as a symbolic link to `data/01data-pull`
2. Some data should not be anywhere in the project folder's root tree. This is commonly the case with CMS data, which are too massive to keep where we keep the project files. NBER's servers have special drives where to store CMS data and any manipulation thereof, which I call directly in my scripts.

While the second exception should qualify as the first exception and be solved with symbolic links as well, the symbolic links solution did not occur to me until I had already amassed a large code-base querying to and from external drives. Going forward, symbolic links should be used.


## Configuration files

- `.editorconfig` works with [EditorConfig](https://editorconfig.org/) to transfer settings across different text editors.
- `.envrc` works with [direnv](https://github.com/direnv/direnv) to perform a set of Bash commands every time you enter the directory. I have it set environment variables and enter the Conda environment automatically when I enter within the directory.
- `.gitignore` and `.gitattributes` work with the [Git version control system](https://git-scm.com/). The former file is a list of file and folder names that should not be included in the project's history. The latter helps Git to perform "diffs", a way of showing what parts of the file has changed, correctly.
- `Makefile` works with the program [Make](https://www.gnu.org/software/make/) to make project replication easier. Read more in the [`Makefile`](#makefile) section.
- `bibliography.bib` is a [Bibtex](https://www.sharelatex.com/learn/Bibliography_management_with_bibtex) file for automatic bibliography creation in documents.
- `environment.yml` is a file that works with Conda to define the environment you're working in. It's especially useful for use with R or Python, and lessens the chances of someone else not being able to reproduce the project's results. The file can be generated with `conda env export` from within a Conda environment.
- `setup.cfg` is a file that holds Python code settings. The large `yapf` block of settings defines the style of my code, so that I can run `yapf file.py` to automatically format the file. There are also editor plugins to do this.


## Makefile

I use [Make](https://www.gnu.org/software/make/) to manage the project in a more automated fashion and to make replication easier. At its core, it looks at the timestamps of your files, and if you've made any edits since the last time you ran Make, it will re-run those files _and all the files that depend on them_. Crucially, it also understands not to run any files that don't depend on files you've changed, and can intelligently run files in parallel (see [Makefile options](#makefile-options)), saving potentially a lot of time when updating files.

In general, I try to keep files numbered in the order they should be run, but the `Makefile` is the authoritative source of file dependencies. For example, a file starting with `03` might not depend on _all_ the files starting with `02`. The Makefile will know exactly what each file depends on.

Makefiles use Bash commands, and so can do anything that you can accomplish with Bash. Because of this, Make works best with Linux or MacOS. Since these projects often use restricted data that can't leave servers running Linux, using Make doesn't add any restrictions. It's possible to use it on Windows, however. The easiest method on Windows 10 is enabling [Windows Subsystem for Linux](https://docs.microsoft.com/en-us/windows/wsl/install-win10) (installing Ubuntu is easiest), which then includes Make by default.

### Using the Makefile

The program `make` runs **targets**, or a list of rules or commands specified in a `Makefile`.

My `Makefile`s are set up to be [self documenting](#Self-documenting functionality). To see the list of commands available to you, navigate to the root of the project directory and run `make` or `make help`. You should see something like:
```
$ make
Available rules:

all                 Run everything
code                Run code
dependencies        Install project dependencies
docs                Generate documentation
emails              Download emails relevant to the project from Gmail
help                See this help information
writeup             Generate writeup
sync                Sync project folder with Dropbox
```

Then to run one of the rules, just type it after `make`:
```
$ make docs
```

The `Makefile` must exist in the current directory. I generally use a single `Makefile` located at the root of the project directory for the entire project generation except for documentation. I use a `Makefile` located in the `docs/` folder to generate the documentation. This means that you'll need to move to the root of the project directory in order to run `make`. (Documentation generation is also possible by running `make docs` from the root of the project.) If you run `make` and see:
```
$ make
make: *** No targets specified and no makefile found.  Stop.
```
that means that you are in a directory without a `Makefile`.

#### Makefile options

To see everything that Make will run for a command, without actually running it, use the `-n` or `--dry-run` switch:
```
make docs --dry-run
```

To force Make to rebuild a target, supply the `-B` or `--always-make` switch. Note that this will cause Make to re-run **everything** that target depends on. This may be more than you want. The following will run all the rules specified in the `Makefile`:
```
make all -B
```

To make a build happen in parallel, just supply the `-j` switch with the number of cores you'd like to use. This will use up to 4 cores:
```
make code -j4
```

Of course, if you're trying to run `C`, but `C` depends directly on `B` which depends directly on `A`, it's impossible to run them in parallel and Make will use only one core.

### Adding to the Makefile

Make can understand very, very complex projects, but at its core it is rather simple. You give it a list of rules that each have three components:

1. Name(s) of the output file(s)
2. Name(s) of the file(s) this rule depends on
3. Instructions (as Bash commands) to create the output files

<!-- `all`, `clean` are conventions. -->


There are a couple of important quirks to remember when working with Makefiles:

1. **Makefiles must use tabs and not spaces for indentation.** In text editors, often when you hit the <kbd>Tab</kbd> key, the editor adds four spaces instead of the tab character, and in most programming languages, spaces are preferred to tabs. Most editors will automatically switch to using tab characters when you open a Makefile. Using [EditorConfig](https://editorconfig.org/) with the project's `.editorconfig` file will also help make sure every editor you use inputs tabs and not spaces in Makefiles.
2. **Each command is run in a separate sub-shell.** This means that if you have the target (note `$(MAKE)` is the correct way to run a sub-`Makefile`)

    ```Makefile
    docs:
    	cd docs
    	$(MAKE) all
    ```

    it will not do what you expect because the commands `cd docs` and `$(MAKE) all` are run separately in two different shells. The first shell moves into the `docs/` directory and then exits. The second is a _new shell_ in the directory of the Makefile, which will then run the `all` target of the current `Makefile`. So when you type `make docs`, it will not run the sub-`Makefile` located at `docs/Makefile`, but rather build the entire project defined within this `Makefile`'s `all` target.

    The correct way to do this is

    ```Makefile
    docs:
    	cd docs && $(MAKE) all
    ```

    where `&&` is the Bash operator to say "go into the `docs` directory, and if that command succeeded, then run the `all` target of the sub-`Makefile`". Using `&&` instead of `;` (the standard way to delimit multiple commands on a single line) is important here. If the `docs` directory didn't exist, or you didn't have the correct permissions to enter it, `cd docs; $(MAKE) all` would run `$(MAKE) all` regardless of if `cd docs` succeeded.

    As an example, consider the following `Makefile` in an empty folder:

    ```Makefile
    SHELL := /bin/bash
    all:
    	echo all

    docs:
    	cd docs; $(MAKE) all
    ```

    When you run `make docs`, the `all` target still gets run:

    ```
    $ make docs
    cd docs; make all
    /bin/bash: line 0: cd: docs: No such file or directory
    make[1]: Entering directory '/tmp'
    echo all
    all
    make[1]: Leaving directory '/tmp'
    ```

#### Use with Stata

Make works by looking at the [_exit code_](https://shapeshed.com/unix-exit-codes/) of each program. The exit code is a number returned after each program runs. This is the same idea as error codes (like `r(1)`) in Stata.

Annoyingly, when you run Stata batch scripts from the command line, even if the script encounters an error and stops, Stata reports a code of `0` back to the shell, which means no error was encountered. Therefore, if you use `stata -b do file.do` with Make, even if the file encountered an error, Stata will tell Make that the file ran correctly and that it's ok to run the next file in line. This is obviously unwanted.

To get around this, I use a wrapper (available [here](https://github.com/kylebarron/lib/blob/master/statab.sh) or [here](https://gist.github.com/kylebarron/e1488ed01f9bc83107e73b8c2b34368d) and also located at `lib/statab.sh`) to search the `.log` output any errors from Stata.

The only material difference is that when editing the `Makefile`, instead of using `stata -b do file.do`, use `$(RUN_STATA) file.do`, where `RUN_STATA` is a macro defined at the top of the Makefile, holding the text: `bash lib/statab.sh do`.

#### Self-documenting functionality

The repository I forked to create my project structure included a [big ugly block of code](https://github.com/drivendata/cookiecutter-data-science/blob/752ddc7868c03bf76ca62a96a3ab7b3077de4625/%7B%7B%20cookiecutter.repo_name%20%7D%7D/Makefile#L85-L144) at the end of the Makefile that does something awesome: semi-automatic Makefile documentation. That ugly code is what prints the output for `make` or `make help`:
```
$ make
Available rules:

all                 Run everything
code                Run code
dependencies        Install project dependencies
docs                Generate documentation
emails              Download emails relevant to the project from Gmail
help                See this help information
writeup             Generate writeup
sync                Sync project folder with Dropbox
```

In order for this to work, on the line preceding each target you want to document, write `## ` and your comment.
```Makefile
## Generate documentation
docs:
	cd docs && $(MAKE) all
```
