# Step-by-Step Guide: Batch File Renamer for Mac & Linux

## Overview

Safe, cross-platform Python CLI for batch renaming files. Replace dots/spaces, add prefixes/suffixes. Preview before applying. No dependencies.

This guide will help you safely rename files that have incorrect dots or spaces in their names. The script offers flexible options:

| Original Filename | Default (underscore) | With `--replace=-` | With `--replace=""` |
|-------------------|---------------------|-------------------|-------------------|
| `t2.v1.image.jpg.mp4` | `t2_v1_image_jpg.mp4` | `t2-v1-image-jpg.mp4` | `t2v1imagejpg.mp4` |
| `my file name.txt` | `my_file_name.txt` | `my-file-name.txt` | `myfilename.txt` |

You can also add prefixes and suffixes:
| Original | With `--prefix="2024_"` | With `--suffix="_final"` |
|----------|------------------------|-------------------------|
| `data.csv` | `2024_data.csv` | `data_final.csv` |

**Important:** The script is designed to be SAFE. By default, it only shows you what WOULD change without actually changing anything. You must explicitly confirm before any files are renamed.

---

## Prerequisites

### macOS
Your Mac already has Python 3 installed (macOS comes with it). To verify, open Terminal and type `python3 --version`.

### Linux (Ubuntu/Debian)
Most Linux distributions include Python 3. To verify, open a terminal and type `python3 --version`.

If Python 3 is not installed on Ubuntu/Debian:
```bash
sudo apt update
sudo apt install python3
```

---

## Step 1: Download/Save the Script

1. Save the `batch-file-renamer.py` file to a location you can easily find
2. **Recommended location:** Your home folder or Documents folder

**Example locations (Mac):**
- `/Users/YourName/batch-file-renamer.py`
- `/Users/YourName/Documents/batch-file-renamer.py`

**Example locations (Linux):**
- `/home/YourName/batch-file-renamer.py`
- `/home/YourName/Documents/batch-file-renamer.py`

---

## Step 2: Open Terminal

### macOS

There are several ways to open Terminal on Mac:

#### Method A: Using Spotlight (Easiest)
1. Press `Command (⌘) + Space` to open Spotlight
2. Type `Terminal`
3. Press `Enter` when Terminal appears

#### Method B: Using Finder
1. Open **Finder**
2. Click **Applications** in the sidebar
3. Open the **Utilities** folder
4. Double-click **Terminal**

#### Method C: Using Launchpad
1. Click the **Launchpad** icon in the Dock (grid of squares)
2. Type `Terminal` in the search bar
3. Click the Terminal icon

### Linux (Ubuntu/Debian)

#### Method A: Keyboard Shortcut (Easiest)
Press `Ctrl + Alt + T` to open Terminal.

#### Method B: Using Activities
1. Click **Activities** in the top-left corner (or press the Super/Windows key)
2. Type `Terminal`
3. Click the Terminal icon

---

## Step 3: Navigate to the Script Location

Once Terminal is open, you need to navigate to where you saved the script.

### If the script is in your home folder:
```bash
cd ~
```

### If the script is in Documents:
```bash
cd ~/Documents
```

### If the script is in Downloads:
```bash
cd ~/Downloads
```

**Tip:** You can verify the script is there by typing:
```bash
ls batch-file-renamer.py
```

If it shows the filename, you're in the right place!

---

## Step 4: Find the Path to Your Target Folder

You need to know the full path to the folder containing the files you want to rename.

### Easy Method: Drag and Drop
1. Open a **new Finder window**
2. Navigate to the folder with your files
3. In Terminal, type `python3 batch-file-renamer.py ` (with a space at the end)
4. **Drag the folder from Finder into the Terminal window**
5. The path will automatically appear!

### Manual Method
Common folder paths on Mac:
- Desktop: `/Users/YourName/Desktop/FolderName`
- Documents: `/Users/YourName/Documents/FolderName`
- Downloads: `/Users/YourName/Downloads/FolderName`
- External Drive: `/Volumes/DriveName/FolderName`

**Tip:** Replace `YourName` with your actual Mac username.

---

## Step 5: Preview the Changes (Dry Run)

**ALWAYS do this first!** This shows you what will change WITHOUT actually changing anything.

### Basic preview (replaces dots and spaces with underscores):
```bash
python3 batch-file-renamer.py "/path/to/your/folder"
```

### Preview with hyphen replacement:
```bash
python3 batch-file-renamer.py "/path/to/your/folder" --replace=-
```

### Preview with removal (no replacement character):
```bash
python3 batch-file-renamer.py "/path/to/your/folder" --replace=""
```

### Preview with a prefix added:
```bash
python3 batch-file-renamer.py "/path/to/your/folder" --prefix="2024-01-15_"
```

### Preview with a suffix added:
```bash
python3 batch-file-renamer.py "/path/to/your/folder" --suffix="_final"
```

### Preview with multiple options combined:
```bash
python3 batch-file-renamer.py "/path/to/your/folder" --replace=- --prefix="project_" --suffix="_v2"
```

### Preview with subdirectories included:
```bash
python3 batch-file-renamer.py "/path/to/your/folder" --recursive
```

### What you'll see:
```
======================================================================
FILE RENAMER: Dots & Spaces to Custom Character
======================================================================
Target Directory: /Users/scientist/Documents/experiment_data
Mode: PREVIEW ONLY (dry run)
Recursive: No
Replace dots/spaces with: '_'

======================================================================
PREVIEW OF CHANGES (No files have been modified yet)
======================================================================

Settings:
  Replace dots/spaces with: '_'

Files to rename:

[1] Directory: /Users/scientist/Documents/experiment_data
    BEFORE: t2.v1.image.jpg.mp4
    AFTER:  t2_v1_image_jpg.mp4

[2] Directory: /Users/scientist/Documents/experiment_data
    BEFORE: my file name.csv
    AFTER:  my_file_name.csv

======================================================================
Total files to rename: 2
======================================================================

To apply these changes, run the command again with --apply flag:
  python3 batch-file-renamer.py "/path/to/folder" --apply
```

**Review this carefully!** Make sure only the files you expect are listed.

---

## Step 6: Apply the Changes

Once you've reviewed the preview and are satisfied, add `--apply` to your command:

### Apply with default underscore replacement:
```bash
python3 batch-file-renamer.py "/path/to/your/folder" --apply
```

### Apply with hyphen replacement:
```bash
python3 batch-file-renamer.py "/path/to/your/folder" --replace=- --apply
```

### Apply with prefix:
```bash
python3 batch-file-renamer.py "/path/to/your/folder" --prefix="2024_" --apply
```

### Apply with all options:
```bash
python3 batch-file-renamer.py "/path/to/your/folder" --replace=- --prefix="project_" --suffix="_v2" --recursive --apply
```

### Confirmation prompt:
The script will show the preview again and ask:
```
Are you sure you want to rename these files?
Type 'yes' to confirm:
```

**Type `yes` and press Enter** to proceed, or anything else to cancel.

---

## Step 7: Review the Log File

After renaming, the script creates a log file in the target folder:
- Filename format: `rename_log_YYYYMMDD_HHMMSS.txt`
- Example: `rename_log_20241215_143022.txt`

This log contains:
- The settings used (replacement character, prefix, suffix)
- A record of all files that were renamed
- Any errors that occurred
- A summary of the operation

**Keep this log file** in case you need to reference what was changed.

---

## Quick Reference: All Options

| Option | Description | Example |
|--------|-------------|---------|
| (no options) | Preview with underscore replacement | `python3 batch-file-renamer.py /path` |
| `--apply` | Actually rename the files | `python3 batch-file-renamer.py /path --apply` |
| `--replace=CHAR` | Use custom replacement character | `--replace=-` or `--replace=""` |
| `--prefix=TEXT` | Add text before filename | `--prefix="2024_"` |
| `--suffix=TEXT` | Add text after filename (before extension) | `--suffix="_final"` |
| `--recursive` or `-r` | Include subdirectories | `--recursive` |

---

## Common Use Cases

### Use Case 1: Fix dots, replace with underscores (default)
```bash
# Preview
python3 batch-file-renamer.py "/Users/me/Data"

# Apply
python3 batch-file-renamer.py "/Users/me/Data" --apply
```
Result: `t2.v1.scan.nii.gz` → `t2_v1_scan_nii.gz`

### Use Case 2: Fix dots and spaces, replace with hyphens
```bash
# Preview
python3 batch-file-renamer.py "/Users/me/Data" --replace=-

# Apply
python3 batch-file-renamer.py "/Users/me/Data" --replace=- --apply
```
Result: `my file.v1.txt` → `my-file-v1.txt`

### Use Case 3: Remove all dots and spaces entirely
```bash
# Preview
python3 batch-file-renamer.py "/Users/me/Data" --replace=""

# Apply
python3 batch-file-renamer.py "/Users/me/Data" --replace="" --apply
```
Result: `t2.v1.image.jpg.mp4` → `t2v1imagejpg.mp4`

### Use Case 4: Add a date prefix to all files
```bash
# Preview
python3 batch-file-renamer.py "/Users/me/Data" --prefix="2024-01-15_"

# Apply
python3 batch-file-renamer.py "/Users/me/Data" --prefix="2024-01-15_" --apply
```
Result: `results.xlsx` → `2024-01-15_results.xlsx`

### Use Case 5: Add a version suffix to all files
```bash
# Preview
python3 batch-file-renamer.py "/Users/me/Data" --suffix="_v2"

# Apply
python3 batch-file-renamer.py "/Users/me/Data" --suffix="_v2" --apply
```
Result: `analysis.csv` → `analysis_v2.csv`

### Use Case 6: Full transformation with prefix and suffix
```bash
# Preview
python3 batch-file-renamer.py "/Users/me/Data" --replace=- --prefix="project_" --suffix="_final"

# Apply
python3 batch-file-renamer.py "/Users/me/Data" --replace=- --prefix="project_" --suffix="_final" --apply
```
Result: `t2.v1.scan.nii.gz` → `project_t2-v1-scan-nii_final.gz`

### Use Case 7: Process all subdirectories
```bash
# Preview
python3 batch-file-renamer.py "/Users/me/Data" --recursive

# Apply
python3 batch-file-renamer.py "/Users/me/Data" --recursive --apply
```

---

## Common Issues and Solutions

### "Permission denied" error
**Cause:** You don't have permission to rename files in that folder.

**Solution:**
1. Check that you own the files
2. For external drives, ensure they're not locked or read-only
3. Try running with `sudo` (administrator privileges):
   ```bash
   sudo python3 batch-file-renamer.py "/path/to/folder" --apply
   ```
   You'll need to enter your Mac password.

### "No such file or directory" error
**Cause:** The path to the folder is incorrect.

**Solution:**
1. Double-check the path spelling
2. Use the drag-and-drop method (Step 4) to get the correct path
3. Make sure to use quotes around paths with spaces

### "python3: command not found"
**Cause:** Python might not be in your system PATH.

**Solution:**
1. Try using the full path: `/usr/bin/python3`
2. Or install Python from python.org

### Script doesn't run / "Permission denied" on the script itself
**Cause:** The script file doesn't have execute permission.

**Solution:** Make the script executable:
```bash
chmod +x batch-file-renamer.py
```

### Files on an external drive aren't renaming
**Cause:** External drives may have different permissions.

**Solution:**
1. Make sure the drive is not write-protected
2. Check that the drive is formatted as APFS, HFS+, or exFAT (not NTFS)
3. Try copying files to your local drive first, renaming, then copying back

### My prefix/suffix has special characters and isn't working
**Cause:** Some characters have special meaning in the terminal.

**Solution:** Wrap the prefix/suffix in quotes:
```bash
python3 batch-file-renamer.py "/path" --prefix="2024-01-15_" --apply
```

---

## Safety Features Built Into This Script

1. **Dry run by default** - Nothing changes unless you add `--apply`
2. **Confirmation required** - You must type "yes" before changes are made
3. **Hidden files ignored** - Files starting with `.` are never touched
4. **Log file created** - Every operation is recorded with settings used
5. **Collision detection** - Won't overwrite if a file with the new name already exists
6. **Only processes the folder you specify** - Won't touch other folders unless you use `--recursive`
7. **Input validation** - Rejects invalid characters in replacement/prefix/suffix

---

## Example Walkthrough

Let's say Dr. Smith has files in `/Users/drsmith/Desktop/Lab_Data`:

```
t2.v1.scan.nii.gz
patient 001.data.2024.csv
control.group.a.results.xlsx
normal_file.pdf
```

### Scenario A: Just fix the dots and spaces (default)

**Step 1: Preview**
```bash
python3 batch-file-renamer.py "/Users/drsmith/Desktop/Lab_Data"
```

**Output shows:**
```
[1] BEFORE: t2.v1.scan.nii.gz
    AFTER:  t2_v1_scan_nii.gz

[2] BEFORE: patient 001.data.2024.csv
    AFTER:  patient_001_data_2024.csv

[3] BEFORE: control.group.a.results.xlsx
    AFTER:  control_group_a_results.xlsx

Total files to rename: 3
```

Note: `normal_file.pdf` isn't listed because it has no issues.

**Step 2: Apply**
```bash
python3 batch-file-renamer.py "/Users/drsmith/Desktop/Lab_Data" --apply
```

Type `yes` when prompted. Done!

---

### Scenario B: Add a date prefix to organize files

**Step 1: Preview**
```bash
python3 batch-file-renamer.py "/Users/drsmith/Desktop/Lab_Data" --prefix="2024-12-15_"
```

**Output shows:**
```
[1] BEFORE: t2.v1.scan.nii.gz
    AFTER:  2024-12-15_t2_v1_scan_nii.gz

[2] BEFORE: patient 001.data.2024.csv
    AFTER:  2024-12-15_patient_001_data_2024.csv

[3] BEFORE: control.group.a.results.xlsx
    AFTER:  2024-12-15_control_group_a_results.xlsx

[4] BEFORE: normal_file.pdf
    AFTER:  2024-12-15_normal_file.pdf

Total files to rename: 4
```

Note: Now `normal_file.pdf` IS included because it needs the prefix.

**Step 2: Apply**
```bash
python3 batch-file-renamer.py "/Users/drsmith/Desktop/Lab_Data" --prefix="2024-12-15_" --apply
```

---

## Need Help?

If you encounter issues not covered here:
1. Check that your folder path is correct
2. Make sure you have permission to modify the files
3. Try running the preview first to see if files are detected
4. Check the log file for specific error messages
5. Run `python3 batch-file-renamer.py --help` to see all options
