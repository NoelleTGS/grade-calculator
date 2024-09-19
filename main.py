import json
import math
import os.path
from subprocess import call
from time import sleep


class Grade:
    def __init__(self, ass_name, points, max_points, weight):
        self.name = ass_name
        self.points = points
        self.max_points = max_points
        self.weight = weight

    def to_dict(self):
        return {
            'name': self.name,
            'points': self.points,
            'max_points': self.max_points,
            'weight': self.weight
        }

    def from_dict(data):
        return Grade(data['name'], data['points'], data['max_points'], data['weight'])


class Type:
    def __init__(self, name, weight):
        self.name = name
        self.grades = []
        self.weight = weight

    def add_grade(self, name, points, max_points, weight):
        new_grade = Grade(name, points, max_points, weight)
        self.grades.append(new_grade)

    def to_dict(self):
        return {
            'name': self.name,
            'weight': self.weight,
            'grades': [grade.to_dict() for grade in self.grades]
        }

    def from_dict(data):
        type_obj = Type(data['name'], data['weight'])
        type_obj.grades = [Grade.from_dict(grade_data) for grade_data in data['grades']]
        return type_obj


class Course:
    def __init__(self, code):
        self.code = code
        self.types = []

    def add_type(self, a):
        self.types.append(a)

    def to_dict(self):
        return {
            'code': self.code,
            'types': [type.to_dict() for type in self.types]
        }

    def from_dict(data):
        course_obj = Course(data['code'])
        course_obj.types = [Type.from_dict(type_data) for type_data in data['types']]
        return course_obj


def clear():
    _ = call('clear' if os.name == 'posix' else 'cls')
    print("Grade Calculator\n--------------\n")


def save_data(courses):
    serialized_courses = [course.to_dict() for course in courses]
    with open('grades_data.json', 'w') as f:
        json.dump(serialized_courses, f, indent=4)


def load_data():
    courses = []
    with open('grades_data.json', 'r') as f:
        serialized_courses = json.load(f)
        for serialized_course in serialized_courses:
            course = Course.from_dict(serialized_course)
            courses.append(course)
    return courses


def calc_type_grade(type: Type):
    if len(type.grades) == 0:
        return 0
    points = 0
    maxpoints = 0
    for grade in type.grades:
        points += (grade.points / grade.max_points) * grade.weight
        maxpoints += grade.weight
    score = (points / maxpoints)

    return score * 100


def calc_grade(course: Course):
    typetotals = []
    for i in course.types:
        if len(i.grades) == 0:
            continue
        points = 0
        maxpoints = 0
        for grade in i.grades:
            points += (grade.points / grade.max_points) * grade.weight
            maxpoints += grade.weight
        score = (points / maxpoints)
        typetotals.append((score, i.weight))

    total = 0
    weight = 0
    for i in typetotals:
        total += i[0] * i[1]
        weight += i[1]

    try:
        total = total / weight
    except:
        total = 0

    return int(math.floor(total * 100))


def calc_letter_grade(i: int):
    if i >= 95:
        return 'A+'
    elif i >= 85:
        return 'A'
    elif i >= 80:
        return 'A-'
    elif i >= 77:
        return 'B+'
    elif i >= 73:
        return 'B'
    elif i >= 70:
        return 'B-'
    elif i >= 67:
        return 'C+'
    elif i >= 63:
        return 'C'
    elif i >= 60:
        return 'C-'
    elif i >= 55:
        return 'D+'
    elif i >= 50:
        return 'D'
    else:
        return 'F'


def view_grades():
    clear()
    print("Current Grades\n")
    for i in courses:
        grade = calc_grade(i)
        print(f"%s: %d%% (%s)" % (i.code, grade, calc_letter_grade(grade)))

    input("\nPress Enter to continue...")


def view_grades_full():
    clear()
    print("Current Grades\n")
    for i in courses:
        grade = calc_grade(i)
        print("%s: %d%% (%s)" % (i.code, grade, calc_letter_grade(grade)))
        for j in i.types:
            if len(j.grades) != 0:
                print(f"%s, average %d%%" % (j.name.upper(), calc_type_grade(j)))
                for k in j.grades:
                    assgrade = (k.points / k.max_points) * 100
                    print("%-20s %4g/%-3d (%3d%%, %2s)" % (
                        k.name, k.points, k.max_points, assgrade, calc_letter_grade(assgrade)))
        print("")

    input("\nPress Enter to continue...")


def add_grade():
    clear()
    for index, course in enumerate(courses):
        print(f"{index + 1}: {course.code}")
    course = int(input("\nAdd grade to which course? "))

    if course - 1 > len(courses) - 1:
        print("Invalid course.")
        sleep(3)
        return

    for index, type in enumerate(courses[course - 1].types):
        print(f"{index + 1}: {type.name}")
    type = int(input("Enter type: "))

    name = input("\nEnter grade name: ")
    points = float(input("Enter points: "))
    max_points = int(input("Enter max score: "))
    weight = int(input("Enter grade weight (enter 1 if all assignments weighted equally): "))
    courses[course - 1].types[type - 1].add_grade(name, points, max_points, weight)


def edit_grade():
    clear()
    print("No not yet\nShouldn't have fucked up")
    sleep(3)


def add_course(name):
    new_course = Course(name)
    courses.append(new_course)
    print(f"Course {name} added to course list.")
    sleep(3)


def add_type(course: Course):
    name = input("Enter type name: ")
    weight = int(input("Enter type weight: "))
    newtype = Type(name, weight)
    course.add_type(newtype)


def edit_type(course: Course):
    print("No not yet\nShouldn't have fucked up")
    sleep(3)


def delete_course():
    clear()
    for index, course in enumerate(courses):
        print(f"{index + 1}: {course.code}")
    course = int(input("\nDelete which course? "))

    if course - 1 > len(courses) - 1:
        print("Invalid course.")
        sleep(3)
        return

    temp = courses[course - 1].code
    courses.remove(course - 1)
    print(f"Deleted course {temp}.")
    sleep(3)


def remove_type(course: Course):
    clear()
    if not course.types:
        print("No types found.")
        sleep(3)
        return
    for index, type in enumerate(course.types):
        print(f"{index + 1}: {type.name}")
    type = int(input("\nEnter type: "))

    temp = course.types[type - 1].name
    course.types.pop(type - 1)
    print(f"Deleted type {temp}.")


def edit_course():
    clear()
    for index, course in enumerate(courses):
        print(f"{index + 1}: {course.code}")
    course = int(input("\nEdit which course? "))

    if course - 1 > len(courses) - 1:
        print("Invalid course.")
        sleep(3)
        return

    clear()

    print(f"Editing course: {courses[course - 1].code}\n")

    print("1. Add New Type")
    print("2. Edit Type")
    print("3. Delete Type")
    print("4. Delete Course")
    coursemode = int(input("\nSelect an option: "))

    if coursemode == 1:
        add_type(courses[course - 1])
    elif coursemode == 2:
        edit_type(courses[course - 1])
    elif coursemode == 3:
        remove_type(courses[course - 1])
    elif coursemode == 4:
        temp = courses[course - 1].code
        courses.pop(course - 1)
        print(f"Deleted course {temp}.")
        sleep(3)
    else:
        print("Invalid option.")
        sleep(3)


if os.path.isfile('grades_data.json'):
    courses = load_data()
else:
    courses = []

while True:
    clear()
    for i in courses:
        for j in i.types:
            j.grades.sort(key=lambda x: x.name)
    print("1. View Grades")
    print("2. View Grades (Advanced)")
    print("3. Add a Grade")
    print("4. Edit a Grade")
    print("5. Add a Course")
    print("6. Edit a Course")
    print("7. Quit\n")
    try:
        mode = int(input("Select an option: "))
    except:
        print("Invalid input. Please try again")
        sleep(3)
        continue
    if mode == 1:
        view_grades()
    elif mode == 2:
        view_grades_full()
    elif mode == 3:
        add_grade()
    elif mode == 4:
        edit_grade()
    elif mode == 5:
        code = input("Enter course code: ")
        add_course(code)
    elif mode == 6:
        edit_course()
    elif mode == 7:
        clear()
        quit()
    else:
        print("Invalid option.")
        sleep(3)

    save_data(courses)
