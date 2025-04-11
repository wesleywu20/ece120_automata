from canvasapi import Canvas
from dotenv import load_dotenv
import os
import argparse

load_dotenv()

API_URL = "https://canvas.illinois.edu"
API_KEY = os.environ["CANVAS_API_KEY"]
ECE_120_COURSE_ID = os.environ["ECE_120_COURSE_ID"]

def get_discussion_section_student_IDs(course, desired_section):
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
    student_netIDs = [student.user.get("login_id") for student in students]
    student_IDs = [student.user_id for student in students]
    return desired_section_ID, student_netIDs, student_IDs

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

def enter_grades(course, assignment_id, section_ID, student_IDs, student_netIDs, group_netIDs, grade, comment):
    assignment = course.get_assignment(assignment_id)
    section = course.get_section(section_ID)
    submissions = assignment.get_submissions(student_ids=student_IDs, include=["user"])
    for submission in submissions:
        if submission.user["login_id"] in student_netIDs and submission.user["login_id"] in group_netIDs:
            print(f"[{section.name.split()[2].strip()}] {submission.user['name']}")
            print(f"Giving grade {grade}/10")
            print(f"Giving comment\n{comment}")
            submission.edit(submission={"posted_grade": grade},
                            comment={"text_comment": comment})
            

def main(ws_number, section, group_netIDs, grade, comment):
    canvas = Canvas(API_URL, API_KEY)
    course = canvas.get_course(ECE_120_COURSE_ID)
    discussion_ws_ID = get_discussion_assignment_id(course, ws_number)
    desired_section_ID, section_netIDs, section_student_IDs = get_discussion_section_student_IDs(course, section)
    enter_grades(course, discussion_ws_ID, desired_section_ID, section_student_IDs, section_netIDs, group_netIDs, grade, comment)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Enter discussion grades for students")
    parser.add_argument("--ws_number", type=int, help="Discussion worksheet number (e.g., 11)")
    parser.add_argument("--section", type=str, help="Section number (e.g., AB3)")
    parser.add_argument("--group_netIDs", type=str, nargs='+', help="netIDs of the students in the group")
    parser.add_argument("--grade", type=float, help="Grade to assign to all group members")
    parser.add_argument("--comment", type=str, help="Comma-separated comment to give to all group members")
    args = parser.parse_args()
    raw_comment = args.comment.split(",")
    processed_comment = "\n".join(f"• {comment.strip()}" for comment in raw_comment)
    main(args.ws_number, args.section, args.group_netIDs, args.grade, processed_comment)