class GradeService:
    _mock_grades = [
        {'id': 1, 'student': 'John Doe (S001)', 'assignment': 'Project 1', 'score': '95.00'},
        {'id': 2, 'student': 'Jane Smith (S002)', 'assignment': 'Project 1', 'score': '88.50'}
    ]
    _next_id = 3

    @classmethod
    def get_all_grades(cls):
        return cls._mock_grades.copy()

    @classmethod
    def add_grade(cls, student, assignment, score):
        grade = {'id': cls._next_id, 'student': student, 'assignment': assignment, 'score': score}
        cls._mock_grades.append(grade)
        cls._next_id += 1
        return True, "Grade added successfully"

    @classmethod
    def update_grade(cls, db_id, student, assignment, score):
        db_id = int(db_id)
        for g in cls._mock_grades:
            if g['id'] == db_id:
                g['student'] = student
                g['assignment'] = assignment
                g['score'] = score
                return True, "Grade updated successfully"
        return False, "Grade not found"

    @classmethod
    def delete_grade(cls, db_id):
        db_id = int(db_id)
        cls._mock_grades = [g for g in cls._mock_grades if g['id'] != db_id]
        return True, "Grade deleted successfully"
