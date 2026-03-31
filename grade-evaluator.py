import csv
import sys
import os

# ─────────────────────────────────────────────
# CONSTANTS
# ─────────────────────────────────────────────
TOTAL_WEIGHT_EXPECTED    = 100
FORMATIVE_WEIGHT_EXPECTED = 60
SUMMATIVE_WEIGHT_EXPECTED = 40
PASS_THRESHOLD            = 50.0   # minimum % in each category
MAX_GPA                   = 5.0


def load_csv_data():
    """
    Prompts the user for a filename, validates it exists and is non-empty,
    then parses every row into a list of dictionaries.
    """
    filename = input("Enter the name of the CSV file to process (e.g., grades.csv): ").strip()

    # ── Error: file not found ──────────────────────────────────────────────
    if not os.path.exists(filename):
        print(f"\n[ERROR] The file '{filename}' was not found. "
              f"Please check the path and try again.")
        sys.exit(1)

    assignments = []

    try:
        with open(filename, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)

            # ── Error: empty file (e.g. freshly reset by organizer.sh) ────
            if reader.fieldnames is None:
                print(f"\n[ERROR] '{filename}' is empty. "
                      f"Please add grade data before running the evaluator.")
                sys.exit(1)

            for row in reader:
                assignments.append({
                    'assignment': row['assignment'].strip(),
                    'group':      row['group'].strip(),
                    'score':      float(row['score']),
                    'weight':     float(row['weight'])
                })

    except KeyError as e:
        print(f"\n[ERROR] Missing expected column in CSV: {e}. "
              f"Required columns: assignment, group, score, weight.")
        sys.exit(1)
    except ValueError as e:
        print(f"\n[ERROR] Non-numeric value found in score/weight column: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n[ERROR] An unexpected error occurred while reading the file: {e}")
        sys.exit(1)

    # ── Error: file has headers but no data rows ───────────────────────────
    if not assignments:
        print(f"\n[ERROR] '{filename}' contains headers but no grade records.")
        sys.exit(1)

    return assignments


def validate_scores(data):
    """
    TASK A — Grade Validation
    Every score must be in the range [0, 100].
    Prints a warning per invalid score; exits if any are found.
    """
    errors = []
    for item in data:
        if not (0 <= item['score'] <= 100):
            errors.append(
                f"  • '{item['assignment']}' has score {item['score']} "
                f"(must be between 0 and 100)"
            )
    if errors:
        print("\n[ERROR] Invalid score(s) detected:")
        for e in errors:
            print(e)
        sys.exit(1)


def validate_weights(data):
    """
    TASK B — Weight Validation
    Total weights must sum to 100, Formative to 60, Summative to 40.
    """
    total_weight     = sum(item['weight'] for item in data)
    formative_weight = sum(item['weight'] for item in data if item['group'] == 'Formative')
    summative_weight = sum(item['weight'] for item in data if item['group'] == 'Summative')

    errors = []
    if total_weight != TOTAL_WEIGHT_EXPECTED:
        errors.append(
            f"  • Total weight is {total_weight} (expected {TOTAL_WEIGHT_EXPECTED})"
        )
    if formative_weight != FORMATIVE_WEIGHT_EXPECTED:
        errors.append(
            f"  • Formative weight is {formative_weight} (expected {FORMATIVE_WEIGHT_EXPECTED})"
        )
    if summative_weight != SUMMATIVE_WEIGHT_EXPECTED:
        errors.append(
            f"  • Summative weight is {summative_weight} (expected {SUMMATIVE_WEIGHT_EXPECTED})"
        )

    if errors:
        print("\n[ERROR] Weight validation failed:")
        for e in errors:
            print(e)
        sys.exit(1)


def calculate_category_grade(data, group):
    """
    Returns the weighted percentage score for a given group (Formative/Summative).

    Formula:  sum(score_i * weight_i)  /  sum(weight_i)
    This gives the percentage the student achieved *within* that category.
    """
    group_items   = [item for item in data if item['group'] == group]
    total_weight  = sum(item['weight'] for item in group_items)
    weighted_sum  = sum(item['score'] * item['weight'] for item in group_items)
    return weighted_sum / total_weight   # percentage (0 – 100)


def calculate_final_grade(data):
    """
    TASK C — GPA Calculation
    Final Grade = sum(score_i * weight_i) / 100
    GPA         = (Final Grade / 100) * 5.0
    """
    weighted_sum = sum(item['score'] * item['weight'] for item in data)
    final_grade  = weighted_sum / TOTAL_WEIGHT_EXPECTED   # out of 100
    gpa          = (final_grade / 100) * MAX_GPA
    return final_grade, gpa


def get_resubmission_candidates(data):
    """
    TASK E — Resubmission Logic
    Among Formative assignments with score < 50%, find those with the
    highest weight.  If multiple share that weight, all are returned.
    """
    failed_formative = [
        item for item in data
        if item['group'] == 'Formative' and item['score'] < PASS_THRESHOLD
    ]
    if not failed_formative:
        return []

    max_weight = max(item['weight'] for item in failed_formative)
    return [item for item in failed_formative if item['weight'] == max_weight]


def print_summary(data, formative_pct, summative_pct, final_grade, gpa, passed):
    """
    Prints a formatted transcript-style report.
    """
    separator = "=" * 58

    print(f"\n{separator}")
    print(f"{'  GRADE REPORT':^58}")
    print(separator)

    # ── Per-assignment breakdown ───────────────────────────────────────────
    print(f"\n{'Assignment':<35} {'Group':<12} {'Score':>6} {'Weight':>7}")
    print("-" * 62)
    for item in data:
        flag = "  ✗" if item['score'] < PASS_THRESHOLD else ""
        print(
            f"  {item['assignment']:<33} {item['group']:<12} "
            f"{item['score']:>5.1f}%  {item['weight']:>5.0f}%{flag}"
        )

    # ── Category summary ──────────────────────────────────────────────────
    print(f"\n{'-' * 58}")
    print(f"  {'Formative score:':<30} {formative_pct:>6.2f}%"
          f"  {'✓ PASS' if formative_pct >= PASS_THRESHOLD else '✗ FAIL'}")
    print(f"  {'Summative score:':<30} {summative_pct:>6.2f}%"
          f"  {'✓ PASS' if summative_pct >= PASS_THRESHOLD else '✗ FAIL'}")
    print(f"\n  {'Final Grade:':<30} {final_grade:>6.2f}%")
    print(f"  {'GPA (out of 5.0):':<30} {gpa:>6.2f}")
    print(f"\n  Note: ✗ marks assignments below the 50% threshold.")


def evaluate_grades(data):
    """
    Orchestrates all validation and calculation tasks.
    """
    print("\n--- Processing Grades ---")

    # ── Task A: Score validation ───────────────────────────────────────────
    validate_scores(data)
    print("  [✓] All scores are within the valid range (0 – 100).")

    # ── Task B: Weight validation ──────────────────────────────────────────
    validate_weights(data)
    print("  [✓] Weights validated  (Total = 100 | Formative = 60 | Summative = 40).")

    # ── Task C: Grade & GPA calculation ───────────────────────────────────
    formative_pct  = calculate_category_grade(data, 'Formative')
    summative_pct  = calculate_category_grade(data, 'Summative')
    final_grade, gpa = calculate_final_grade(data)

    # ── Task D: Pass / Fail determination ─────────────────────────────────
    passed = (formative_pct >= PASS_THRESHOLD) and (summative_pct >= PASS_THRESHOLD)

    # ── Print report ──────────────────────────────────────────────────────
    print_summary(data, formative_pct, summative_pct, final_grade, gpa, passed)

    # ── Task F: Final decision ────────────────────────────────────────────
    separator = "=" * 58
    print(f"\n{separator}")
    if passed:
        print(f"  FINAL STATUS :  ✅  PASSED")
    else:
        print(f"  FINAL STATUS :  ❌  FAILED")
    print(separator)

    # ── Task E: Resubmission candidates ───────────────────────────────────
    candidates = get_resubmission_candidates(data)
    if candidates:
        print(f"\n  📋 ELIGIBLE FOR RESUBMISSION "
              f"(failed Formative with highest weight = {candidates[0]['weight']:.0f}%):")
        for item in candidates:
            print(f"     • {item['assignment']}  "
                  f"(Score: {item['score']:.1f}%,  Weight: {item['weight']:.0f}%)")
    else:
        print("\n  No Formative assignments are eligible for resubmission.")

    print()


# ─────────────────────────────────────────────
# ENTRY POINT
# ─────────────────────────────────────────────
if __name__ == "__main__":
    course_data = load_csv_data()
    evaluate_grades(course_data)
