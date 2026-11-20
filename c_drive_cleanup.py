
import os
import csv
import argparse
from pathlib import Path
from datetime import datetime, timedelta

# --------------------------------
# CONFIGURATION
# --------------------------------

DAYS_OLD = 7

TEMP_LOCATIONS = [
    Path(os.environ.get("TEMP", "")),
    Path(r"C:\Windows\Temp")
]

REPORT_FILE = Path.home() / "Desktop" / "cleanup_report.csv"


def scan_files():
    """Find old temporary files without deleting anything."""

    cutoff = datetime.now() - timedelta(days=DAYS_OLD)
    candidates = []
    total_size = 0

    print("\nScanning temporary folders...\n")

    for folder in TEMP_LOCATIONS:

        if not folder.exists():
            continue

        print(f"Checking: {folder}")

        for root, dirs, files in os.walk(folder, followlinks=False):

            # Avoid following directory symlinks
            dirs[:] = [
                d for d in dirs
                if not (Path(root) / d).is_symlink()
            ]

            for filename in files:
                file_path = Path(root) / filename

                try:
                    if file_path.is_symlink():
                        continue

                    modified = datetime.fromtimestamp(
                        file_path.stat().st_mtime
                    )

                    if modified < cutoff:
                        size = file_path.stat().st_size

                        candidates.append({
                            "path": str(file_path),
                            "size": size,
                            "modified": modified
                        })

                        total_size += size

                except (PermissionError, OSError):
                    continue

    return candidates, total_size


def save_report(candidates):
    """Export the scan results to CSV."""

    REPORT_FILE.parent.mkdir(parents=True, exist_ok=True)

    with open(REPORT_FILE, "w", newline="", encoding="utf-8") as file:

        writer = csv.writer(file)

        writer.writerow([
            "File Path",
            "Size (MB)",
            "Last Modified"
        ])

        for item in candidates:
            writer.writerow([
                item["path"],
                round(item["size"] / (1024 * 1024), 2),
                item["modified"]
            ])

    print(f"\nReport saved at: {REPORT_FILE}")


def delete_files(candidates):
    """Delete identified files after explicit confirmation."""

    print("\nYou are about to delete these files.")
    print("Review the CSV report before proceeding.")

    confirmation = input(
        "\nType DELETE to confirm cleanup: "
    )

    if confirmation != "DELETE":
        print("Cleanup cancelled. No files deleted.")
        return

    deleted = 0
    recovered = 0

    for item in candidates:

        try:
            path = Path(item["path"])

            # Recheck that the file is still inside an approved folder
            if not any(
                path.is_relative_to(folder.resolve())
                for folder in TEMP_LOCATIONS
                if folder.exists()
            ):
                continue

            size = path.stat().st_size
            path.unlink()

            deleted += 1
            recovered += size

        except (PermissionError, OSError):
            continue

    print(f"\nFiles deleted: {deleted}")
    print(f"Space recovered: {recovered / (1024**3):.2f} GB")


def main():

    parser = argparse.ArgumentParser(
        description="C Drive Cleanup Assistant"
    )

    parser.add_argument(
        "--delete",
        action="store_true",
        help="Delete identified temporary files after confirmation"
    )

    args = parser.parse_args()

    candidates, total_size = scan_files()

    print("\n--------------- RESULTS ---------------")
    print(f"Files identified: {len(candidates)}")
    print(f"Potential space recovery: {total_size / (1024**3):.2f} GB")

    save_report(candidates)

    if args.delete:
        delete_files(candidates)
    else:
        print("\nSCAN ONLY: Nothing has been deleted.")
        print("Review the report before running with --delete.")


if __name__ == "__main__":
    main()
