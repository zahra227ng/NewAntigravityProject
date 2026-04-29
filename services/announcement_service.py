class AnnouncementService:
    _mock_announcements = [
        {'id': 1, 'title': 'Welcome to Fall 2023', 'content': 'Classes start on September 1st.', 'date': '2023-08-25'},
        {'id': 2, 'title': 'Maintenance Window', 'content': 'System will be down on Sunday at 2 AM.', 'date': '2023-09-10'}
    ]
    _next_id = 3

    @classmethod
    def get_all_announcements(cls):
        return cls._mock_announcements.copy()

    @classmethod
    def add_announcement(cls, title, content, date):
        ann = {'id': cls._next_id, 'title': title, 'content': content, 'date': date}
        cls._mock_announcements.append(ann)
        cls._next_id += 1
        return True, "Announcement posted successfully"

    @classmethod
    def update_announcement(cls, db_id, title, content, date):
        db_id = int(db_id)
        for a in cls._mock_announcements:
            if a['id'] == db_id:
                a['title'] = title
                a['content'] = content
                a['date'] = date
                return True, "Announcement updated successfully"
        return False, "Announcement not found"

    @classmethod
    def delete_announcement(cls, db_id):
        db_id = int(db_id)
        cls._mock_announcements = [a for a in cls._mock_announcements if a['id'] != db_id]
        return True, "Announcement deleted successfully"
