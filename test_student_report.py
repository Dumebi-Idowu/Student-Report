import unittest
import os
from student_report import get_grade, generate_report

class TestStudentReport(unittest.TestCase):

    def test_grades(self):
        self.assertEqual(get_grade(75), 'A')
        self.assertEqual(get_grade(65), 'B')
        self.assertEqual(get_grade(55), 'C')
        self.assertEqual(get_grade(47), 'D')
        self.assertEqual(get_grade(30), 'F')

    def test_report_generated(self):
        generate_report("Test Student", "72", "Test School", "secretkey123")
        self.assertTrue(os.path.exists("student_report.txt"))

    def test_report_content(self):
        generate_report("Dumebi", "85", "Test School", "secretkey123")
        with open("student_report.txt", "r") as f:
            content = f.read()
        self.assertIn("Dumebi", content)
        self.assertIn("PASSED", content)

    def tearDown(self):
        if os.path.exists("student_report.txt"):
            os.remove("student_report.txt")

if __name__ == "__main__":
    unittest.main()