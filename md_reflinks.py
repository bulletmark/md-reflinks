#!/usr/bin/env python3
"Insert or update Markdown reference links list in Markdown files."

# Author: Mark Blakeney, Nov 2024
from __future__ import annotations

import re
import sys
from pathlib import Path

from argparse_from_file import ArgumentParser, Namespace


def init() -> Namespace:
    "Initialize command line arguments and options"
    opt = ArgumentParser(description=__doc__)

    opt.add_argument(
        '-a',
        '--all',
        action='store_true',
        help='append all reference links in the file (default: only append required links)',
    )

    opt.add_argument(
        '-n',
        '--no-normalize',
        action='store_true',
        help='do not normalize reference links (default: normalize keys to remove file name for local reference)',
    )

    opt.add_argument(
        '-f',
        '--force',
        action='store_true',
        help='force update of reference links even if they are unchanged (default: only update if changed)',
    )

    opt.add_argument(
        '-q',
        '--quiet',
        action='store_true',
        help='quiet mode (default: print updated files to stdout)',
    )

    opt.add_argument(
        'master_file_md', help='markdown master file to source link definitions'
    )

    opt.add_argument('file_md', nargs='+', help='markdown target file[s] to update')
    return opt.parse_args()


def normalize(file: Path, reflinks: dict[str, str]) -> dict[str, str]:
    "Normalizes reference links by removing the file name from local references"
    names = set((file.name, file.stem))
    normalized = {}
    for key, link in reflinks.items():
        if '#' in link:
            fname, flink = link.split('#', 1)
            if fname in names:
                link = '#' + flink

        normalized[key] = link

    return normalized


def parse_content(file: Path) -> tuple[list[str], set[str], dict[str, str]]:
    "Parses the given file to return body, tags, and reference links"
    body = []
    tags = set()
    reflinks = {}
    with file.open() as f:
        for line in f:
            if line.startswith('['):
                try:
                    key, value = line[1:].split(']:', 1)
                except ValueError:
                    pass
                else:
                    reflinks[key] = value.strip()
                    continue

            tags.update(t[1:-1] for t in re.findall(r'\[.+?\]', line))
            body.append(line)

    return body, tags, reflinks


def update_file(args: Namespace, master_reflinks: dict[str, str], file: Path) -> None:
    "Update the given file"
    body, tags, reflinks = parse_content(file)

    if args.all:
        newlinks = master_reflinks
    else:
        newlinks = {k: master_reflinks[k] for k in master_reflinks if k in tags}

    if not args.no_normalize:
        newlinks = normalize(file, newlinks)

    # Preserve any existing active reference links in the target file that
    # are not in the master file
    for key in reflinks:
        if key in tags and key not in newlinks:
            newlinks[key] = reflinks[key]

    # Update the target file if the reference links have changed or if force is specified
    if newlinks != reflinks or args.force:
        with file.open('w') as f:
            f.writelines(body)

            # Ensure there is at least one blank line before the reference links
            if newlinks:
                if body and body[-1].strip():
                    f.write('\n')

                # Write the reference links at the end of the file
                for key, value in newlinks.items():
                    f.write(f'[{key}]: {value}\n')

        if not args.quiet:
            print(f'Updated reference links in "{file}"')


def main() -> str | None:
    "Main code"
    args = init()

    master = Path(args.master_file_md)
    if not master.is_file():
        return f'Error: master file "{master}" does not exist.'

    # Parse the master file to get its reference links
    _, _, master_reflinks = parse_content(master)

    for file_str in args.file_md:
        file = Path(file_str)
        if not file.is_file():
            print(
                f'Warning: target file "{file}" does not exist, skipping.',
                file=sys.stderr,
            )
        elif not master.samefile(file):
            update_file(args, master_reflinks, file)


if __name__ == '__main__':
    sys.exit(main())
