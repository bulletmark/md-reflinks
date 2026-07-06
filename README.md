# md-reflinks
[![PyPi](https://img.shields.io/pypi/v/md-reflinks)](https://pypi.org/project/md-reflinks/)

`md-reflinks` is a command-line tool that manages common [Markdown
reference-style links](https://spec.commonmark.org/current/#reference-link)
across multiple Markdown files. You maintain a single **master** Markdown file
which contains all your reference link definitions, e.g. "`[python]: https://python.org`"
typically all listed together at the bottom of the file.
`md-reflinks` reads that master file and injects the referenced definitions into
one or more **target** files. This means you only have to manage your reference
links in one Markdown file.

By default, only the links that are actually referenced in a target file (i.e.
those which are referenced as `[key]` tags in the body) are replaced or added
but you can also choose to append all master link definitions to the target file
if you prefer. Reference links defined and used in the target that are not
present in the master file are preserved.


## Usage

Type `md-reflinks -h` to view the usage summary:

```
usage: md-reflinks [-h] [-a] [-n] [-f] [-q]
                      master_file_md file_md [file_md ...]

Insert Markdown reference links list in Markdown files.

positional arguments:
  master_file_md      markdown master file to source link definitions
  file_md             markdown target file[s] to update

options:
  -h, --help          show this help message and exit
  -a, --all           append all reference links in the file (default: only
                      append required links)
  -n, --no-normalize  do not normalize reference links (default: normalize
                      keys to remove file name for local reference)
  -f, --force         force update of reference links even if they are
                      unchanged (default: only update if changed)
  -q, --quiet         quiet mode (default: print updated files to stdout)

Note you can set default starting options in ~/.config/md-reflinks.py-
flags.conf.
```

## Installation and Running

The easiest way to install and run `md-reflinks` is via [uvx] which is provided
by installing [uv], e.g.:

```bash
uvx md-reflinks README.md docs/*.md
```

The above will run the latest version of `md-reflinks` without needing to
explicitly install it locally. `uvx` will handle installation if needed (on the
fly very quickly). You can also install it explicitly using [`uv tool
install`][uvtool] if you prefer.

The above example will read reference link definitions from `README.md` and
update those required in all the Markdown files in the `docs/` directory,
inserting, deleting, or replacing them at the bottom of each file.

Note you can also use a wildcard to update all Markdown files in the current
directory and `md-reflinks` will automatically skip the master file itself to
avoid self-injection, e.g.:

```bash
uvx md-reflinks README.md *.md
```

## License

Copyright (C) 2026 Mark Blakeney. This program is distributed under the terms
of the GNU General Public License. This program is free software: you can
redistribute it and/or modify it under the terms of the GNU General Public
License as published by the Free Software Foundation, either version 3 of the
License, or any later version. This program is distributed in the hope that it
will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public
License at <https://www.gnu.org/licenses/gpl-3.0.html> for more details.

[uv]: https://docs.astral.sh/uv
[uvx]: https://docs.astral.sh/uv/guides/tools/#running-tools
[uvtool]: https://docs.astral.sh/uv/guides/tools/#installing-tools
