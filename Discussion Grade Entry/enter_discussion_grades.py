from canvasapi import Canvas
from dotenv import load_dotenv
import os
import sys
import argparse

load_dotenv()

sys.tracebacklimit = 0  # Disable traceback for cleaner error messages

API_URL = "https://canvas.illinois.edu"
API_KEY = os.environ["CANVAS_API_KEY"]
ECE_120_COURSE_ID = os.environ["ECE_120_COURSE_ID"]

def get_discussion_section_student_IDs(course, desired_section, group_netIDs):
    sections = course.get_sections()
    desired_section_ID = None
    for section in sections:
        if desired_section in section.name:
            desired_section_ID = section.id
            break
    else:
        raise ValueError(f"Section ID for {desired_section} not found in course {course.name}")
    section = course.get_section(desired_section_ID)
    students = section.get_enrollments(type=['StudentEnrollment'])
    student_IDs = [student.user_id for student in students if student.user.get("login_id") in group_netIDs]
    if len(student_IDs) < len(group_netIDs):
        raise ValueError("Some netIDs are invalid or not in the specified section.")
    return desired_section_ID, student_IDs

def get_discussion_assignment_id(course, ws_number):
    discussion_group_ID = None
    assignment_groups = course.get_assignment_groups()
    for group in assignment_groups:
        if group.name == "Discussions":
            discussion_group_ID = group.id
            break
    if discussion_group_ID is None:
        raise ValueError("Discussion assignment group not found in course")
    assignments = course.get_assignments(assignment_group_id=discussion_group_ID)
    for assignment in assignments:
        if assignment.name == f"Discussion Worksheet#{ws_number}":
            return assignment.id
    return None

def enter_grades(course, assignment_id, section_ID, student_IDs, grade, comment):
    assignment = course.get_assignment(assignment_id)
    section = course.get_section(section_ID)
    submissions = [assignment.get_submission(studentID, include=["user"]) for studentID in student_IDs]
    for submission in submissions:
        print(f"[{section.name.split()[2].strip()}] {submission.user['name']}")
        print(f"Giving grade {grade}/10")
        if comment:
            print(f"Giving comment\n{comment}")
        submission.edit(submission={"posted_grade": grade},
                        comment={"text_comment": comment})
            

def main(ws_number, section, group_netIDs, grade, comment=None):
    canvas = Canvas(API_URL, API_KEY)
    course = canvas.get_course(ECE_120_COURSE_ID)
    discussion_ws_ID = get_discussion_assignment_id(course, ws_number)
    desired_section_ID, section_student_IDs = get_discussion_section_student_IDs(course, section, group_netIDs)
    enter_grades(course, discussion_ws_ID, desired_section_ID, section_student_IDs, grade, comment)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Enter discussion grades for students")
    parser.add_argument("--ws_number", type=int, help="Discussion worksheet number (e.g., 11)")
    parser.add_argument("--section", type=str, help="Section number (e.g., AB3)")
    parser.add_argument("--group_netIDs", type=str, nargs='+', help="netIDs of the students in the group")
    parser.add_argument("--grade", type=float, help="Grade to assign to all group members")
    parser.add_argument("--comment", type=str, help="Comma-separated comment to give to all group members", required=False, default="")
    args = parser.parse_args()
    if args.comment != "":
        raw_comment = args.comment.split(",")
        processed_comment = "\n".join(f"• {comment.strip()}" for comment in raw_comment)
        main(args.ws_number, args.section, args.group_netIDs, args.grade, processed_comment)
    else:
        main(args.ws_number, args.section, args.group_netIDs, args.grade)