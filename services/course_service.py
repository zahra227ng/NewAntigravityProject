class CourseService:
    _mock_courses = [
        {'id': 1, 'code': 'CS101', 'name': 'Intro to Computer Science', 'description': 'Learn basics of programming.'},
        {'id': 2, 'code': 'CS201', 'name': 'Data Structures', 'description': 'Advanced data organization.'}
    ]
    _next_id = 3

    @classmethod
    def get_all_courses(cls):
        return cls._mock_courses.copy()

    @classmethod
    def add_course(cls, code, name, description):
        course = {'id': cls._next_id, 'code': code, 'name': name, 'description': description}
        cls._mock_courses.append(course)
        cls._next_id += 1
        return True, "Course added successfully"

    @classmethod
    def update_course(cls, course_id, code, name, description):
        course_id = int(course_id)
        for c in cls._mock_courses:
            if c['id'] == course_id:
                c['code'] = code
                c['name'] = name
                c['description'] = description
                return True, "Course updated successfully"
        return False, "Course not found"

    @classmethod
    def delete_course(cls, course_id):
        course_id = int(course_id)
        cls._mock_courses = [c for c in cls._mock_courses if c['id'] != course_id]
        return True, "Course deleted successfully"
