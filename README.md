# Windows Storage Analyzer & Cleanup Toolkit

A Python-based toolkit developed to investigate, analyse and manage storage consumption on Windows systems.

This project started as a practical attempt to address low disk space on a Windows computer and evolved into a broader storage investigation and cleanup workflow.

## Project Objectives

- Analyse disk space consumption across files and folders.
- Identify large files and storage-heavy directories.
- Categorise files by extension.
- Identify potential cleanup candidates.
- Investigate unfamiliar files before making deletion decisions.
- Support the identification of redundant, unnecessary and unwanted files.
- Help users decide whether files should be retained, deleted, uninstalled through their respective applications, or moved to another drive.
- Generate reports to support informed storage-management decisions.

## Features

### Storage Analyzer
- Scans the C drive.
- Identifies the largest folders.
- Identifies the largest individual files.
- Analyses file storage by extension.
- Generates CSV reports.
- Read-only scanning.

### Temporary File Cleanup Utility
- Scans designated temporary directories.
- Identifies potential cleanup candidates.
- Generates a report for review.
- Supports scan-first workflows before deletion.

### Storage Investigation Workflow

The project uses a cautious, evidence-based approach to storage management:

1. Scan storage.
2. Analyse large files and folders.
3. Identify potential unnecessary or redundant files.
4. Investigate unfamiliar files using metadata and file characteristics.
5. Review and validate cleanup candidates.
6. Decide whether to delete, retain, move or uninstall through the appropriate application.
7. Measure recovered disk space.

## Technologies

- Python
- PowerShell
- Windows filesystem
- CSV reporting
- File metadata inspection
- SHA-256 hashing
- Digital signature verification

## Project Background

Developed as a personal Python automation project to investigate and address a real-world Windows storage problem.

The project demonstrates the use of scripting, filesystem analysis, structured reporting, command-line tools and evidence-based decision-making for system storage management.

## Safety

The analyzer does not intentionally modify or delete files.

Cleanup operations should always be reviewed and validated before execution. Unknown files, Windows system files and installed application files should not be manually deleted without understanding their purpose.
