#!/bin/bash
# ============================================================
#  organizer.sh  –  Grade CSV Archiver & Workspace Resetter
#  African Leadership University | BSE Year 1 Trimester 2
# ============================================================

# ── Configuration ────────────────────────────────────────────
SOURCE_FILE="grades.csv"
ARCHIVE_DIR="archive"
LOG_FILE="organizer.log"

# ── Step 1: Ensure the archive directory exists ───────────────
if [ ! -d "$ARCHIVE_DIR" ]; then
    mkdir -p "$ARCHIVE_DIR"
    echo "[INFO] Created archive directory: $ARCHIVE_DIR"
else
    echo "[INFO] Archive directory already exists: $ARCHIVE_DIR"
fi

# ── Step 2: Check that grades.csv exists and is not empty ─────
if [ ! -f "$SOURCE_FILE" ]; then
    echo "[ERROR] '$SOURCE_FILE' not found in the current directory. Exiting."
    exit 1
fi

if [ ! -s "$SOURCE_FILE" ]; then
    echo "[WARN] '$SOURCE_FILE' is empty – nothing to archive. Exiting."
    exit 0
fi

# ── Step 3: Generate a timestamp ─────────────────────────────
TIMESTAMP=$(date +"%Y%m%d-%H%M%S")

# ── Step 4: Build the archived filename ──────────────────────
# Strip .csv, append timestamp, re-add extension
BASE_NAME="${SOURCE_FILE%.csv}"
ARCHIVED_NAME="${BASE_NAME}_${TIMESTAMP}.csv"
ARCHIVED_PATH="${ARCHIVE_DIR}/${ARCHIVED_NAME}"

# ── Step 5: Move (rename + relocate) the file ────────────────
mv "$SOURCE_FILE" "$ARCHIVED_PATH"
echo "[INFO] Archived '$SOURCE_FILE'  →  '$ARCHIVED_PATH'"

# ── Step 6: Create a fresh empty grades.csv ──────────────────
touch "$SOURCE_FILE"
echo "[INFO] Created fresh empty file: $SOURCE_FILE"

# ── Step 7: Append log entry ─────────────────────────────────
{
    echo "------------------------------------------------------------"
    echo "Timestamp       : $TIMESTAMP"
    echo "Original file   : $SOURCE_FILE"
    echo "Archived as     : $ARCHIVED_PATH"
    echo "------------------------------------------------------------"
} >> "$LOG_FILE"

echo "[INFO] Log updated: $LOG_FILE"
echo "[DONE] Archive operation complete."
