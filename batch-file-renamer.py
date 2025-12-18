#!/usr/bin/env python3
"""
@file batch-file-renamer.py
@brief Safely renames files by replacing internal dots and spaces, with optional prefix/suffix.

This script processes files in a specified directory, replacing all dots and spaces
in filenames EXCEPT the final extension dot. Supports customizable replacement
characters and adding prefixes or suffixes to filenames.

Cross-platform compatible: Works on macOS, Linux (Ubuntu, etc.), and Windows.

Example transformations:
    "t2.v1.image.jpg.mp4"       -> "t2_v1_image_jpg.mp4" (default)
    "t2.v1.image.jpg.mp4"       -> "t2-v1-image-jpg.mp4" (with --replace=-)
    "t2.v1.image.jpg.mp4"       -> "t2v1imagejpg.mp4"    (with --replace="")
    "my file.name.txt"          -> "my_file_name.txt"    (spaces also replaced)
    "data.csv"                  -> "2024-01-15_data.csv" (with --prefix=2024-01-15_)
    "results.xlsx"              -> "results_final.xlsx"  (with --suffix=_final)

@author Generated for safe file renaming operations
@version 2.1.0
@see https://github.com/yourusername/batch_file_renamer

@section USAGE
    Preview changes (dry run - no actual changes):
        python3 batch-file-renamer.py /path/to/folder

    Apply changes after preview:
        python3 batch-file-renamer.py /path/to/folder --apply

    Use different replacement character:
        python3 batch-file-renamer.py /path/to/folder --replace=-
        python3 batch-file-renamer.py /path/to/folder --replace=""

    Add prefix or suffix:
        python3 batch-file-renamer.py /path/to/folder --prefix="2024-01-15_"
        python3 batch-file-renamer.py /path/to/folder --suffix="_final"
        python3 batch-file-renamer.py /path/to/folder --prefix="project_" --suffix="_v2"

    Process subdirectories recursively:
        python3 batch-file-renamer.py /path/to/folder --recursive --apply

    Combined example:
        python3 batch-file-renamer.py /path/to/folder --replace=- --prefix="2024_" --apply

@section SAFETY_FEATURES
    - Dry run by default (preview only)
    - Requires explicit --apply flag to make changes
    - Skips hidden files (starting with .)
    - Skips files that would not change
    - Creates detailed log of all operations
    - Validates folder exists before processing
    - Displays comprehensive scan summary

@section COMPATIBILITY
    - macOS (10.x+)
    - Linux (Ubuntu, Debian, CentOS, etc.)
    - Windows (with Python 3.6+)
    - No external dependencies (uses only Python standard library)
"""

import os
import sys
import argparse
from datetime import datetime


# ------------------------------------------------------------------------------
# Constants
# ------------------------------------------------------------------------------
MAX_FILES_LIMIT = 10000  # Upper bound for safety (NASA Principle #2)
LOG_FILENAME_PREFIX = "rename_log_"
DEFAULT_REPLACEMENT = "_"


# ------------------------------------------------------------------------------
# Core Functions
# ------------------------------------------------------------------------------
def validate_directory(directory_path):
    """
    Validates that the provided path exists and is a directory.

    @param directory_path: Path to validate
    @return: Tuple (is_valid: bool, error_message: str or None)
    """
    if not directory_path:
        return False, "No directory path provided."

    if not os.path.exists(directory_path):
        return False, f"Path does not exist: {directory_path}"

    if not os.path.isdir(directory_path):
        return False, f"Path is not a directory: {directory_path}"

    return True, None


def validate_replacement_char(replacement):
    """
    Validates the replacement character is safe for filenames.

    @param replacement: The replacement string to validate
    @return: Tuple (is_valid: bool, error_message: str or None)
    """
    # Characters not allowed in filenames (cross-platform safety)
    invalid_chars = ['/', '\\', ':', '*', '?', '"', '<', '>', '|', '\0']

    for char in replacement:
        if char in invalid_chars:
            return False, f"Invalid character in replacement: '{char}'"

    # Reasonable length limit
    if len(replacement) > 10:
        return False, "Replacement string too long (max 10 characters)"

    return True, None


def validate_prefix_suffix(value, label):
    """
    Validates prefix or suffix is safe for filenames.

    @param value: The prefix or suffix string to validate
    @param label: "prefix" or "suffix" for error messages
    @return: Tuple (is_valid: bool, error_message: str or None)
    """
    if not value:
        return True, None

    # Characters not allowed in filenames (cross-platform safety)
    invalid_chars = ['/', '\\', ':', '*', '?', '"', '<', '>', '|', '\0']

    for char in value:
        if char in invalid_chars:
            return False, f"Invalid character in {label}: '{char}'"

    # Reasonable length limit
    if len(value) > 100:
        return False, f"{label.capitalize()} too long (max 100 characters)"

    return True, None


def generate_new_filename(original_filename, replacement="_", prefix="", suffix=""):
    """
    Generates a new filename by replacing internal dots and spaces.
    Optionally adds prefix and/or suffix to the base filename.

    @param original_filename: The original filename to process
    @param replacement: Character(s) to replace dots and spaces with (default: "_")
    @param prefix: String to add before the filename (default: "")
    @param suffix: String to add after the filename, before extension (default: "")
    @return: Tuple (new_filename: str, was_changed: bool)

    Examples with default replacement:
        "t2.v1.image.jpg.mp4" -> "t2_v1_image_jpg.mp4"
        "my file name.txt"    -> "my_file_name.txt"
        "simple.txt"          -> "simple.txt" (no internal dots/spaces)

    Examples with prefix/suffix:
        "data.csv" + prefix="2024_" -> "2024_data.csv"
        "results.xlsx" + suffix="_final" -> "results_final.xlsx"
    """
    assert isinstance(original_filename, str), "Filename must be a string"
    assert len(original_filename) > 0, "Filename cannot be empty"

    # Skip hidden files (start with dot)
    if original_filename.startswith('.'):
        return original_filename, False

    # Find the last dot (the real extension separator)
    last_dot_index = original_filename.rfind('.')

    # Handle files with no extension
    if last_dot_index == -1:
        base_name = original_filename
        extension = ""
    else:
        base_name = original_filename[:last_dot_index]
        extension = original_filename[last_dot_index:]  # Includes the dot

    # Count characters that need replacement
    dots_count = base_name.count('.')
    spaces_count = base_name.count(' ')
    needs_char_replacement = (dots_count > 0) or (spaces_count > 0)
    needs_prefix_suffix = bool(prefix) or bool(suffix)

    # If nothing to change, return original
    if not needs_char_replacement and not needs_prefix_suffix:
        return original_filename, False

    # Replace dots and spaces in base name
    new_base_name = base_name
    if needs_char_replacement:
        new_base_name = new_base_name.replace('.', replacement)
        new_base_name = new_base_name.replace(' ', replacement)

    # Apply prefix and suffix
    new_base_name = prefix + new_base_name + suffix

    # Reconstruct filename
    new_filename = new_base_name + extension

    was_changed = (new_filename != original_filename)

    return new_filename, was_changed


def collect_files_to_rename(directory_path, replacement="_", prefix="", suffix="",
                            recursive=False):
    """
    Collects all files that need renaming in the specified directory.

    @param directory_path: Path to the directory to scan
    @param replacement: Character(s) to replace dots and spaces with
    @param prefix: String to add before filenames
    @param suffix: String to add after filenames (before extension)
    @param recursive: If True, also scan subdirectories
    @return: Tuple (files_to_rename: list, stats: dict)
             files_to_rename: List of tuples (original_path, new_path, original_name, new_name)
             stats: Dictionary with scan statistics
    """
    files_to_rename = []
    stats = {
        'total_files_scanned': 0,
        'hidden_files_skipped': 0,
        'hidden_dirs_skipped': 0,
        'files_already_clean': 0,
        'files_to_rename': 0,
        'directories_scanned': 0
    }

    if recursive:
        # Walk through directory tree
        for root, dirs, files in os.walk(directory_path):
            stats['directories_scanned'] += 1

            # Count and skip hidden directories
            hidden_dirs = [d for d in dirs if d.startswith('.')]
            stats['hidden_dirs_skipped'] += len(hidden_dirs)
            dirs[:] = [d for d in dirs if not d.startswith('.')]

            for filename in files:
                stats['total_files_scanned'] += 1

                if stats['total_files_scanned'] > MAX_FILES_LIMIT:
                    print(f"Warning: Exceeded {MAX_FILES_LIMIT} files. Stopping scan.")
                    return files_to_rename, stats

                # Count hidden files
                if filename.startswith('.'):
                    stats['hidden_files_skipped'] += 1
                    continue

                new_filename, was_changed = generate_new_filename(
                    filename, replacement, prefix, suffix
                )

                if was_changed:
                    original_path = os.path.join(root, filename)
                    new_path = os.path.join(root, new_filename)
                    files_to_rename.append((original_path, new_path, filename, new_filename))
                    stats['files_to_rename'] += 1
                else:
                    stats['files_already_clean'] += 1
    else:
        stats['directories_scanned'] = 1

        # Only process files in the specified directory (not subdirectories)
        try:
            entries = os.listdir(directory_path)
        except PermissionError:
            print(f"Error: Permission denied to read directory: {directory_path}")
            return files_to_rename, stats

        for filename in entries:
            filepath = os.path.join(directory_path, filename)

            # Skip directories (count hidden ones)
            if os.path.isdir(filepath):
                if filename.startswith('.'):
                    stats['hidden_dirs_skipped'] += 1
                continue

            stats['total_files_scanned'] += 1

            if stats['total_files_scanned'] > MAX_FILES_LIMIT:
                print(f"Warning: Exceeded {MAX_FILES_LIMIT} files. Stopping scan.")
                return files_to_rename, stats

            # Count hidden files
            if filename.startswith('.'):
                stats['hidden_files_skipped'] += 1
                continue

            new_filename, was_changed = generate_new_filename(
                filename, replacement, prefix, suffix
            )

            if was_changed:
                new_path = os.path.join(directory_path, new_filename)
                files_to_rename.append((filepath, new_path, filename, new_filename))
                stats['files_to_rename'] += 1
            else:
                stats['files_already_clean'] += 1

    return files_to_rename, stats


def display_preview(files_to_rename, stats, replacement, prefix, suffix):
    """
    Displays a preview of all files that will be renamed.

    @param files_to_rename: List of file tuples to display
    @param stats: Dictionary with scan statistics
    @param replacement: The replacement character being used
    @param prefix: The prefix being added
    @param suffix: The suffix being added
    @return: None
    """
    # Display scan summary first
    print("\n" + "-" * 70)
    print("SCAN SUMMARY")
    print("-" * 70)
    print(f"  Directories scanned:    {stats['directories_scanned']}")
    print(f"  Total files scanned:    {stats['total_files_scanned']}")
    print(f"  Hidden files skipped:   {stats['hidden_files_skipped']}")
    print(f"  Hidden folders skipped: {stats['hidden_dirs_skipped']}")
    print(f"  Files already clean:    {stats['files_already_clean']}")
    print(f"  Files to rename:        {stats['files_to_rename']}")
    print("-" * 70)

    if not files_to_rename:
        print("\nNo files need renaming in this directory.")
        return

    print("\n" + "=" * 70)
    print("PREVIEW OF CHANGES (No files have been modified yet)")
    print("=" * 70)

    # Show current settings
    replace_display = f"'{replacement}'" if replacement else "(remove)"
    print(f"\nSettings:")
    print(f"  Replace dots/spaces with: {replace_display}")
    if prefix:
        print(f"  Add prefix: '{prefix}'")
    if suffix:
        print(f"  Add suffix: '{suffix}'")

    print("\nFiles to rename:")
    for i, (orig_path, new_path, orig_name, new_name) in enumerate(files_to_rename, 1):
        # Show relative directory if different from base
        directory = os.path.dirname(orig_path)
        print(f"\n[{i}] Directory: {directory}")
        print(f"    BEFORE: {orig_name}")
        print(f"    AFTER:  {new_name}")

    print("\n" + "=" * 70)
    print(f"Total files to rename: {len(files_to_rename)}")
    print("=" * 70)


def apply_renames(files_to_rename, directory_path, replacement, prefix, suffix):
    """
    Applies the file renames and creates a log file.

    @param files_to_rename: List of file tuples to rename
    @param directory_path: Base directory (used for log file location)
    @param replacement: The replacement character used (for logging)
    @param prefix: The prefix used (for logging)
    @param suffix: The suffix used (for logging)
    @return: Tuple (success_count: int, error_count: int, log_path: str)
    """
    if not files_to_rename:
        return 0, 0, None

    success_count = 0
    error_count = 0
    log_entries = []

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_filename = f"{LOG_FILENAME_PREFIX}{timestamp}.txt"
    log_path = os.path.join(directory_path, log_filename)

    print("\n" + "=" * 70)
    print("APPLYING CHANGES")
    print("=" * 70)

    for orig_path, new_path, orig_name, new_name in files_to_rename:
        try:
            # Check if destination already exists
            if os.path.exists(new_path):
                error_msg = f"SKIPPED (destination exists): {orig_name}"
                print(f"  [!] {error_msg}")
                log_entries.append(f"SKIPPED: {orig_path} -> {new_path} (destination exists)")
                error_count += 1
                continue

            # Perform the rename
            os.rename(orig_path, new_path)
            print(f"  [OK] {orig_name} -> {new_name}")
            log_entries.append(f"RENAMED: {orig_path} -> {new_path}")
            success_count += 1

        except PermissionError:
            error_msg = f"FAILED (permission denied): {orig_name}"
            print(f"  [X] {error_msg}")
            log_entries.append(f"FAILED: {orig_path} -> Permission denied")
            error_count += 1

        except OSError as e:
            error_msg = f"FAILED ({str(e)}): {orig_name}"
            print(f"  [X] {error_msg}")
            log_entries.append(f"FAILED: {orig_path} -> {str(e)}")
            error_count += 1

    # Write log file
    try:
        replace_display = f"'{replacement}'" if replacement else "(removed)"
        with open(log_path, 'w') as log_file:
            log_file.write(f"Rename Operation Log - {timestamp}\n")
            log_file.write(f"Directory: {directory_path}\n")
            log_file.write(f"Replacement: {replace_display}\n")
            if prefix:
                log_file.write(f"Prefix: '{prefix}'\n")
            if suffix:
                log_file.write(f"Suffix: '{suffix}'\n")
            log_file.write("=" * 70 + "\n\n")
            for entry in log_entries:
                log_file.write(entry + "\n")
            log_file.write(f"\nSummary: {success_count} successful, {error_count} errors\n")
    except IOError:
        print(f"\nWarning: Could not write log file to {log_path}")
        log_path = None

    return success_count, error_count, log_path


def parse_arguments():
    """
    Parses command line arguments.

    @return: Parsed arguments namespace
    """
    parser = argparse.ArgumentParser(
        description="Safely rename files by replacing dots and spaces, with optional prefix/suffix.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  Preview changes:
    python3 batch-file-renamer.py /path/to/folder

  Apply with default underscore replacement:
    python3 batch-file-renamer.py /path/to/folder --apply

  Use hyphen as replacement:
    python3 batch-file-renamer.py /path/to/folder --replace=-

  Remove dots and spaces entirely:
    python3 batch-file-renamer.py /path/to/folder --replace=""

  Add date prefix:
    python3 batch-file-renamer.py /path/to/folder --prefix="2024-01-15_"

  Add version suffix:
    python3 batch-file-renamer.py /path/to/folder --suffix="_v2"

  Combined options:
    python3 batch-file-renamer.py /path/to/folder --replace=- --prefix="project_" --suffix="_final" --apply
        """
    )

    parser.add_argument(
        "directory",
        help="Path to the directory containing files to rename"
    )

    parser.add_argument(
        "--apply",
        action="store_true",
        help="Actually apply the changes (default is preview only)"
    )

    parser.add_argument(
        "--recursive",
        "-r",
        action="store_true",
        help="Process subdirectories recursively"
    )

    parser.add_argument(
        "--replace",
        type=str,
        default="_",
        metavar="CHAR",
        help="Character(s) to replace dots and spaces with (default: '_'). Use --replace=\"\" to remove them entirely."
    )

    parser.add_argument(
        "--prefix",
        type=str,
        default="",
        metavar="TEXT",
        help="Text to add at the beginning of each filename (before the base name)"
    )

    parser.add_argument(
        "--suffix",
        type=str,
        default="",
        metavar="TEXT",
        help="Text to add at the end of each filename (after base name, before extension)"
    )

    return parser.parse_args()


def main():
    """
    Main entry point for the script.

    @return: Exit code (0 for success, 1 for error)
    """
    # Parse command line arguments
    args = parse_arguments()

    # Normalize and expand the directory path (handles ~ for home directory)
    directory_path = os.path.expanduser(args.directory)
    directory_path = os.path.abspath(directory_path)

    # Validate directory
    is_valid, error_message = validate_directory(directory_path)
    if not is_valid:
        print(f"Error: {error_message}")
        return 1

    # Validate replacement character
    is_valid, error_message = validate_replacement_char(args.replace)
    if not is_valid:
        print(f"Error: {error_message}")
        return 1

    # Validate prefix
    is_valid, error_message = validate_prefix_suffix(args.prefix, "prefix")
    if not is_valid:
        print(f"Error: {error_message}")
        return 1

    # Validate suffix
    is_valid, error_message = validate_prefix_suffix(args.suffix, "suffix")
    if not is_valid:
        print(f"Error: {error_message}")
        return 1

    # Display header
    replace_display = f"'{args.replace}'" if args.replace else "(remove)"
    print("\n" + "=" * 70)
    print("BATCH FILE RENAMER")
    print("=" * 70)
    print(f"Target Directory: {directory_path}")
    print(f"Mode: {'APPLY CHANGES' if args.apply else 'PREVIEW ONLY (dry run)'}")
    print(f"Recursive: {'Yes' if args.recursive else 'No'}")
    print(f"Replace dots/spaces with: {replace_display}")
    if args.prefix:
        print(f"Prefix: '{args.prefix}'")
    if args.suffix:
        print(f"Suffix: '{args.suffix}'")

    # Collect files that need renaming
    files_to_rename, stats = collect_files_to_rename(
        directory_path,
        replacement=args.replace,
        prefix=args.prefix,
        suffix=args.suffix,
        recursive=args.recursive
    )

    # Display preview
    display_preview(files_to_rename, stats, args.replace, args.prefix, args.suffix)

    # If not applying, show instructions and exit
    if not args.apply:
        if files_to_rename:
            print("\nTo apply these changes, run the command again with --apply flag:")
            cmd_parts = [f'python3 batch-file-renamer.py "{directory_path}"']
            if args.replace != "_":
                cmd_parts.append(f'--replace="{args.replace}"')
            if args.prefix:
                cmd_parts.append(f'--prefix="{args.prefix}"')
            if args.suffix:
                cmd_parts.append(f'--suffix="{args.suffix}"')
            if args.recursive:
                cmd_parts.append("--recursive")
            cmd_parts.append("--apply")
            print(f"  {' '.join(cmd_parts)}")
        return 0

    # Confirm before applying
    if files_to_rename:
        print("\nAre you sure you want to rename these files?")
        response = input("Type 'yes' to confirm: ").strip().lower()

        if response != 'yes':
            print("Operation cancelled. No files were modified.")
            return 0

        # Apply the renames
        success_count, error_count, log_path = apply_renames(
            files_to_rename,
            directory_path,
            args.replace,
            args.prefix,
            args.suffix
        )

        # Display summary
        print("\n" + "=" * 70)
        print("SUMMARY")
        print("=" * 70)
        print(f"Successfully renamed: {success_count} files")
        print(f"Errors/Skipped: {error_count} files")
        if log_path:
            print(f"Log file saved to: {log_path}")
        print("=" * 70)

    return 0


# ------------------------------------------------------------------------------
# Entry Point
# ------------------------------------------------------------------------------
if __name__ == "__main__":
    sys.exit(main())
