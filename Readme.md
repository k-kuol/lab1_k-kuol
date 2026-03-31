# Lab 1 – Grade Evaluator & Archiver

**African Leadership University** | BSE Year 1 Trimester 2
**Course:** Introduction to Python Programming and Databases

---

## Repository Contents

| File | Description |
|------|-------------|
| `grade-evaluator.py` | Python application that validates and evaluates student grades |
| `organizer.sh` | Bash script that archives the current `grades.csv` and resets the workspace |
| `grades.csv` | CSV file containing course assignment grades |
| `README.md` | This file |

---

## CSV Format

`grades.csv` must contain the following four columns:

```csv
assignment,group,score,weight
Quiz,Formative,85,20
Group Exercise,Formative,40,20
```

| Column | Description |
|--------|-------------|
| `assignment` | Name of the assignment |
| `group` | Either `Formative` or `Summative` |
| `score` | Grade received (0 – 100) |
| `weight` | Contribution to final grade (all weights must sum to 100) |

**Weight rules enforced by the program:**

- All weights together must equal **100**
- Formative assignments must total **60**
- Summative assignments must total **40**

---

## Running the Python Grade Evaluator

**Requirements:** Python 3.6 or higher (no third-party packages needed)

```bash
# 1. Clone or download the repository
git clone https://github.com/k-kuol/lab1_k-kuol.git
cd lab1_k-kuol

# 2. Run the evaluator
python3 grade-evaluator.py

# 3. When prompted, enter the filename:
#    Enter the name of the CSV file to process (e.g., grades.csv): grades.csv
```

**What the program checks and reports:**

| Feature | Detail |
|---------|--------|
| Score validation | Ensures every score is between 0 and 100 |
| Weight validation | Enforces Total = 100, Formative = 60, Summative = 40 |
| GPA calculation | `GPA = (Final Grade / 100) × 5.0` |
| Pass / Fail status | Student must score ≥ 50% in both categories to pass |
| Resubmission candidates | Lists failed Formative assignments with the highest weight |

**Sample output:**

```
--- Processing Grades ---
  [✓] All scores are within the valid range (0 – 100).
  [✓] Weights validated  (Total = 100 | Formative = 60 | Summative = 40).

==========================================================
                       GRADE REPORT
==========================================================

Assignment                          Group        Score  Weight
--------------------------------------------------------------
  Quiz                              Formative     85.0%    20%
  Group Exercise                    Formative     40.0%    20%  ✗
  Functions and Debugging Lab       Formative     45.0%    20%  ✗
  Midterm Project - Simple Calc     Summative     70.0%    20%
  Final Project - Text-Based Game   Summative     60.0%    20%

----------------------------------------------------------
  Formative score:                   56.67%  ✓ PASS
  Summative score:                   65.00%  ✓ PASS

  Final Grade:                       60.00%
  GPA (out of 5.0):                   3.00

  Note: ✗ marks assignments below the 50% threshold.

==========================================================
  FINAL STATUS :  ✅ PASSED
==========================================================

  ELIGIBLE FOR RESUBMISSION (failed Formative with highest weight = 20%):
     • Group Exercise  (Score: 40.0%,  Weight: 20%)
     • Functions and Debugging Lab  (Score: 45.0%,  Weight: 20%)
```

---

## Running the Shell Script Organizer

**Requirements:**
- A Unix/Linux/macOS terminal or Git Bash on Windows
- `grades.csv` must exist and be non-empty in the same directory

```bash
# 1. Make the script executable (first time only)
chmod +x organizer.sh

# 2. Run the script
./organizer.sh
```

**What the script does:**

1. Checks for an `archive/` directory — creates it if missing
2. Generates a timestamp (format: `YYYYMMDD-HHMMSS`)
3. Moves `grades.csv` → `archive/grades_<timestamp>.csv`
4. Creates a new, empty `grades.csv` in the current directory
5. Appends a log entry to `organizer.log`

**Sample output:**

```
[INFO] Created archive directory: archive
[INFO] Archived 'grades.csv'  →  'archive/grades_20251105-170000.csv'
[INFO] Created fresh empty file: grades.csv
[INFO] Log updated: organizer.log
[DONE] Archive operation complete.
```

**Sample `organizer.log` entry:**

```
------------------------------------------------------------
Timestamp       : 20251105-170000
Original file   : grades.csv
Archived as     : archive/grades_20251105-170000.csv
------------------------------------------------------------
```

> The log file accumulates entries across multiple runs — it is never overwritten.

---

## Error Handling

| Scenario | Behaviour |
|----------|-----------|
| `grades.csv` not found | Program exits with a clear error message |
| `grades.csv` is empty | Program exits with a clear error message |
| Score outside 0 – 100 | Program lists all invalid rows and exits |
| Weights don't sum correctly | Program reports which totals are wrong and exits |
| Non-numeric score/weight in CSV | Program exits with a descriptive error |

---

## Author

- **Name:** (your name)
- **GitHub:** (your GitHub username)
- **Course:** Introduction to Python Programming and Databases — BSE Year 1 T2
