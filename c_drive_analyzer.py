
import os
import csv
import heapq
import stat
from pathlib import Path
from collections import defaultdict

# ==========================================
# C DRIVE STORAGE ANALYZER
# READ ONLY - DOES NOT DELETE ANYTHING
# ==========================================

DRIVE = Path("C:/")
DESKTOP = Path.home() / "Desktop"

TOP_FILES_LIMIT = 50
TOP_FOLDERS_LIMIT = 30

folder_sizes = defaultdict(int)
extension_sizes = defaultdict(int)

largest_files = []
files_scanned = 0
folders_scanned = 0
errors = 0


def format_gb(size):
    return round(size / (1024 ** 3), 3)


def add_to_largest_files(size, path, modified):

    global largest_files

    item = (size, str(path), modified)

    if len(largest_files) < TOP_FILES_LIMIT:
        heapq.heappush(largest_files, item)

    elif size > largest_files[0][0]:
        heapq.heapreplace(largest_files, item)


def analyze_drive():

    global files_scanned, folders_scanned, errors

    print("\nStarting C Drive analysis...")
    print("This may take several minutes.\n")

    folder_sizes[str(DRIVE)] = 0

    for root, dirs, files in os.walk(
        DRIVE,
        topdown=True,
        followlinks=False
    ):

        folders_scanned += 1

        # Skip Windows junctions and symbolic links
        safe_dirs = []

        for directory in dirs:

            directory_path = Path(root) / directory

            try:
                info = directory_path.stat(
                    follow_symlinks=False
                )

                attributes = getattr(
                    info,
                    "st_file_attributes",
                    0
                )

                if not attributes & stat.FILE_ATTRIBUTE_REPARSE_POINT:
                    safe_dirs.append(directory)

            except OSError:
                errors += 1

        dirs[:] = safe_dirs

        for filename in files:

            file_path = Path(root) / filename

            try:
                info = file_path.stat(
                    follow_symlinks=False
                )

                attributes = getattr(
                    info,
                    "st_file_attributes",
                    0
                )

                if attributes & stat.FILE_ATTRIBUTE_REPARSE_POINT:
                    continue

                size = info.st_size
                modified = info.st_mtime

                files_scanned += 1

                # Add file size to its parent folders
                current = file_path.parent

                while True:

                    folder_sizes[str(current)] += size

                    if current == DRIVE:
                        break

                    parent = current.parent

                    if parent == current:
                        break

                    current = parent

                # Track file extension
                extension = file_path.suffix.lower()

                if not extension:
                    extension = "[No extension]"

                extension_sizes[extension] += size

                # Keep only the 50 largest files
                add_to_largest_files(
                    size,
                    file_path,
                    modified
                )

            except (PermissionError, OSError):
                errors += 1

        if folders_scanned % 500 == 0:
            print(
                f"Folders scanned: {folders_scanned:,} | "
                f"Files scanned: {files_scanned:,}"
            )


def save_reports():

    DESKTOP.mkdir(parents=True, exist_ok=True)

    # REPORT 1: Largest folders
    folder_report = sorted(
        [
            (size, path)
            for path, size in folder_sizes.items()
            if path != str(DRIVE)
        ],
        reverse=True
    )[:TOP_FOLDERS_LIMIT]

    with open(
        DESKTOP / "largest_folders.csv",
        "w",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.writer(file)

        writer.writerow([
            "Folder Path",
            "Size (GB)"
        ])

        for size, path in folder_report:
            writer.writerow([
                path,
                format_gb(size)
            ])

    # REPORT 2: Largest files
    with open(
        DESKTOP / "largest_files.csv",
        "w",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.writer(file)

        writer.writerow([
            "File Path",
            "Size (MB)",
            "Last Modified"
        ])

        for size, path, modified in sorted(
            largest_files,
            reverse=True
        ):

            writer.writerow([
                path,
                round(size / (1024 ** 2), 2),
                modified
            ])

    # REPORT 3: File type breakdown
    with open(
        DESKTOP / "file_type_breakdown.csv",
        "w",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.writer(file)

        writer.writerow([
            "File Extension",
            "Total Size (GB)"
        ])

        for extension, size in sorted(
            extension_sizes.items(),
            key=lambda x: x[1],
            reverse=True
        ):

            writer.writerow([
                extension,
                format_gb(size)
            ])

    print("\nAll reports generated successfully!")

    print(f"\nFiles scanned: {files_scanned:,}")
    print(f"Folders scanned: {folders_scanned:,}")
    print(f"Access errors/skipped items: {errors:,}")

    print("\nReports saved to:")
    print(DESKTOP)

    print("\n1. largest_folders.csv")
    print("2. largest_files.csv")
    print("3. file_type_breakdown.csv")


def main():

    if not DRIVE.exists():
        print("C Drive not found.")
        return

    analyze_drive()
    save_reports()

    print("\nAnalysis complete.")
    print("No files were deleted or modified.")


if __name__ == "__main__":
    main()
