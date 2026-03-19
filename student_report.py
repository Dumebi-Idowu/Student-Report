import os
from datetime import datetime

def get_grade(score):
    if score >= 70:
        return 'A'
    elif score >= 60:
        return 'B'
    elif score >= 50:
        return 'C'
    elif score >= 45:
        return 'D'
    else:
        return 'F'

def generate_report(student_name, score, school_name, signing_key):
    score = int(score)
    grade = get_grade(score)
    status = "PASSED" if grade != 'F' else "FAILED"
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    report = f"""
STUDENT REPORT
==============
School:   {school_name}
Date:     {date}

Student:  {student_name}
Score:    {score}
Grade:    {grade}
Status:   {status}

Verified by key: {signing_key[:4]}****
==============
    """

    print(report)

    with open("student_report.txt", "w") as f:
        f.write(report)

    print("✅ Report saved to student_report.txt")

if __name__ == "__main__":
    student_name = os.environ.get("STUDENT_NAME", "Unknown")
    score        = os.environ.get("STUDENT_SCORE", "0")
    school_name  = os.environ.get("SCHOOL_NAME", "Unknown School")
    signing_key  = os.environ.get("SIGNING_KEY", "")

    if not signing_key:
        print("❌ Error: Signing key not set!")
        exit(1)

    generate_report(student_name, score, school_name, signing_key)