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
