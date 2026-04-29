class AssignmentService:
    _mock_assignments = [
        {'id': 1, 'course': 'CS101', 'title': 'Project 1', 'due_date': '2023-10-15'},
        {'id': 2, 'course': 'CS201', 'title': 'Midterm Exam', 'due_date': '2023-11-01'}
    ]
    _next_id = 3

    @classmethod
    def get_all_assignments(cls):
        return cls._mock_assignments.copy()

    @classmethod
    def add_assignment(cls, course, title, due_date):
        assignment = {'id': cls._next_id, 'course': course, 'title': title, 'due_date': due_date}
        cls._mock_assignments.append(assignment)
        cls._next_id += 1
        return True, "Assignment added successfully"

    @classmethod
    def update_assignment(cls, db_id, course, title, due_date):
        db_id = int(db_id)
        for a in cls._mock_assignments:
            if a['id'] == db_id:
                a['course'] = course
                a['title'] = title
                a['due_date'] = due_date
                return True, "Assignment updated successfully"
        return False, "Assignment not found"

    @classmethod
    def delete_assignment(cls, db_id):
        db_id = int(db_id)
        cls._mock_assignments = [a for a in cls._mock_assignments if a['id'] != db_id]
        return True, "Assignment deleted successfully"
