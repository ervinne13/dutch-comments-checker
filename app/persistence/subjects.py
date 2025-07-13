from .db import get_db

def get_all_subjects_summary():
    db = get_db()
    # Raw SQL for performance, and I'm not yet good at using SQLAlchemy ORM anyway.
    # Should be good as we're not really accepting parameters here.
    with db.cursor() as cursor:
        cursor.execute('''
            SELECT 
                subjects.id AS subject_id,
                subjects.text AS subject_text,
                COUNT(comments.id) AS total_comment_count,
                COUNT(CASE WHEN scc.spam >= 3 THEN 1 END) AS spam_comment_count,
                COUNT(CASE WHEN tcc.toxic >= 0.3 THEN 1 END) AS toxic_comment_count
            FROM comments
            LEFT JOIN subjects ON subjects.id = comments.subject_id
            LEFT JOIN spam_comment_classifications AS scc ON scc.comment_id = comments.id
            LEFT JOIN toxic_comment_classifications AS tcc ON tcc.comment_id = comments.id
            GROUP BY subjects.id, subjects.text
            ORDER BY total_comment_count DESC;
        ''')
        results = cursor.fetchall()
    return results if results else []
