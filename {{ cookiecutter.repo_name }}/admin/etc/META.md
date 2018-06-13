# Folder Structure

- `admin` contains administrative stuff. Notably
    - `admin/emails` contains all e-mail exchanges I was a part of that pertain to the project. Folders are named after the latest e-mail in the thread they belong to: `YYYY-MM-DD HH:MM [Time Zone] - [Truncated Subject Line]`; each file is in markdown format, which is a plain text file that can be rendered as html. To the extent it was possible, sub-folders here correspond to folders in `code` and `writeup` according to their folder structure (see below).
    - `admin/meetings` records all meetings I was a part of. Some will contain very detailed notes, but some not. I was rather erratic in this area. My apologies. As with `admin/emails`, these are sorted, to the extent it was possible, to correspond to the folder structure in `code` and `writeup` (see below).
    - `admin/project.log.md`, with a chronological account of events in the project. Though I was not as dilligent as I should have been in recording everything for every project, this will generally be much better documented than, say, `admin/meetings`.
- `tmp` contains temporary files, as applicable.
- `lib` contains external libraries, as applicable.
- `README.md` is this file with the project information.
- `TODO.md` contains the project's latest and TODOs.

The main folders to generate output are `code` and `writeup`. All raw files that produce output will be in these two folders, and other folders should be thought of as auxiliary.

- `code` contains the project's main code.
    - Folders in code are discrete steps in the project.
    - In each folder, files are numbered starting from `01` in the order in which they should be run.
    - `00` files typically contain auxiliary scripts to be called by other scripts.
    - `99` files typically contain test, beta, or one-off code.
    - There will often be symbolic links to `out`, `lib`, and `data`
- `writeup` contains the project's main write-up. This includes all deliverable output, including summaries, reviews, analysis, power, etc. Sub-folders often contain symbolic links to `out`, `lib`.

The main auxiliary folders to `code` and `writeup` are `data` and `out`

- `data` contains input and output data, raw and processed files.
- `out` contains processed output. Typically figures and tables.

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
- This is in part done for consistency, but in part because I will automatically generally create symbolic links to `data` and `out` as sub-folders in `code`, which will point to the analogue folder, via `make.py` (see below for more on `make.py`).

Naturally it is not always necessary for every folder created in `code` or `output` to have analogues everywhere. For instance, a literature review may only require content to be created in `writeup`. A `code` step may only involve data manipulation. However, generally speaking there are only two exceptions to this folder structure:

1. A given folder in `data` may contain files that are used in multiple steps of the project. There is no perfect way to handle this (the general version of this problem is what programmers call "dependency hell"). My preferred way is to use symbolic links (shortcuts). If your new step is `04bootstrap` and will use data from `01data-pull`, then create something like `data/04bootstrap/data-pull` as a symbolic link to `data/01data-pull`
2. Some data should not be anywhere in the project folder's root tree. This is commonly the case with CMS data, which are too massive to keep where we keep the project files. NBER's servers have special drives where to store CMS data and any manipulation thereof, which I call directly in my scripts.

While the second exception should qualify as the first exception and be solved with symbolic links as well, the symbolic links solution did not occur to me until I had already amassed a large code-base querying to and from external drives. Going forward, symbolic links should be used.

make.py
-------

`make.py` and `Makefile.py` are a system I devised to manage the project in a more automated fashion and to make replication easier. I do not think they are very good, but perhaps they are a decent-ish first attempt. Hence I do not necessarily recommend this system, but feel free to use it.

You can ignore it, of course, since files are numbered in the order in which they should be run (see above) and `python make.py --gen-bash` will generate a `make.sh` file that contains the near-equivalent commands that could be run from a bash prompt.

I styled it after `make`, which uses a `Makefile` to compile programs, and `make.py` from the Gentzkow-Shapiro lab, which uses python to provide a cross-platform make solution that integrates with SVN. Makefiles are great, but I liked the idea of integration with a version control system (though I decidedly prefer Git to SVN) and of having some standard ways of running specific files. However, I have not yet integrated `make.py` with `git`.

`make` was designed to compile often very complex projects, like C projects, which require different options and configurations for different platforms and architectures. By contrast, we usually run Stata, SAS, LaTeX, etc. files that would be helpful to automate but are not that complex to run.

`make.py` runs files specified in `Makefile.py`. In a `code` folder these will usually be `do` files for Stata. In a `writeup` folder these will usually be `tex` files for LaTeX. It can do 4 things:

- Run a file: Compile or run using the specified executable. This is the most general and often used functionality of `make.py`.
- Get a file/folder: The default is a symbolic link.
- Check a file/folder exists. You can specify which file(s) this file is relevant for. If it does not exist the code not run.
- Sync a file/folder locally or remotely (over ssh): This uses `rsync`, which is a utility that synchronizes folders. I think this is the least interesting functionality of `make.py`, but I use rsync to do the same tasks so often that I included it.
    - I tend to code locally and then synchronize files to NBER's servers This can be done using `rsync` over SSH.
    - Locally, I very often sync portions of the project to Dropbox. Though I could use the "get" functionality with copy set to "True", I find it easier to use the "sync" functionality, since it's already there and I get the power of `rsync` if I so need it.
