class StudentService:
    _mock_students = [
        {'id': 1, 'student_id': 'S001', 'name': 'John Doe', 'email': 'john@example.com', 'enrollment_date': '2023-09-01'},
        {'id': 2, 'student_id': 'S002', 'name': 'Jane Smith', 'email': 'jane@example.com', 'enrollment_date': '2023-09-02'}
    ]
    _next_id = 3

    @classmethod
    def get_all_students(cls):
        return cls._mock_students.copy()

    @classmethod
    def add_student(cls, student_id, name, email, enrollment_date):
        student = {'id': cls._next_id, 'student_id': student_id, 'name': name, 'email': email, 'enrollment_date': enrollment_date}
        cls._mock_students.append(student)
        cls._next_id += 1
        return True, "Student added successfully"

    @classmethod
    def update_student(cls, db_id, student_id, name, email, enrollment_date):
        db_id = int(db_id)
        for s in cls._mock_students:
            if s['id'] == db_id:
                s['student_id'] = student_id
                s['name'] = name
                s['email'] = email
                s['enrollment_date'] = enrollment_date
                return True, "Student updated successfully"
        return False, "Student not found"

    @classmethod
    def delete_student(cls, db_id):
        db_id = int(db_id)
        cls._mock_students = [s for s in cls._mock_students if s['id'] != db_id]
        return True, "Student deleted successfully"
