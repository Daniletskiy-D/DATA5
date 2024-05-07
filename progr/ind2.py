#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import json
import argparse


def tree(directory, 
         max_depth=None, 
         directories_only=False, 
         show_size=False, 
         indent=0):
    
    if max_depth is not None and indent > max_depth:
        return

    items = sorted(os.listdir(directory))
    for index, item in enumerate(items):
        full_path = os.path.join(directory, item)
        is_last = index == len(items) - 1

        if os.path.isdir(full_path):
            if not directories_only:
                print(
                    "    " * indent
                    + ("└── " if is_last else "├── ")
                    + "\033["
                    + item
                    + "/"
                    + "\033["
                )
            if show_size:
                print(
                    "    " * indent
                    + "    "
                    + (" " if is_last else "│")
                    + "    "
                    + "Size: "
                    + str(os.path.getsize(full_path))
                    + " b"
                )
            tree(full_path, max_depth, directories_only, show_size, indent + 1)
        elif not directories_only:
            print("    " * indent + ("└── " if is_last else "├── ") + item)
            if show_size:
                print(
                    "    " * indent
                    + "    "
                    + (" " if is_last else "│")
                    + "    "
                    + "Size: "
                    + str(os.path.getsize(full_path))
                    + " b"
                )


def tree_json(directory, 
              max_depth=None, 
              directories_only=False, 
              show_size=False):
    
    tree_dict = {}

    def build_tree_dict(directory, current_depth):
        if max_depth is not None and current_depth > max_depth:
            return

        items = sorted(os.listdir(directory))
        for item in items:
            full_path = os.path.join(directory, item)
            if os.path.isdir(full_path):
                if not directories_only:
                    tree_dict[item] = {}
                if show_size:
                    tree_dict[item]["size"] = os.path.getsize(full_path)
                build_tree_dict(full_path, current_depth + 1)
            elif not directories_only:
                tree_dict[item] = {}
                if show_size:
                    tree_dict[item]["size"] = os.path.getsize(full_path)

    build_tree_dict(directory, 0)
    return json.dumps(tree_dict, indent=4)


def main():
    parser = argparse.ArgumentParser(description="Display directory tree")
    parser.add_argument(
        "directory", nargs="?", default=".", 
        help="Directory to display tree for"
    )
    parser.add_argument(
        "-d", "--max-depth", type=int, 
        help="Max depth of directory tree"
    )
    parser.add_argument(
        "-o", "--directories-only", action="store_true", 
        help="Display only directories"
    )
    parser.add_argument(
        "-s",
        "--show-size",
        action="store_true",
        help="Display size of files and directories",
    )
    parser.add_argument(
        "-j", "--json", action="store_true", 
        help="Output tree in JSON format"
    )

    args = parser.parse_args()

    if args.json:
        print(
            tree_json(
                args.directory, args.max_depth, 
                args.directories_only, args.show_size
            )
        )
    else:
        tree(
            args.directory, args.max_depth, 
            args.directories_only, args.show_size
        )


if __name__ == "__main__":
    main()
