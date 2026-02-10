from database import get_connection
from datetime import datetime

def insert_sample():
    conn = get_connection()
    cursor = conn.cursor()

    # Δύο δείγματα εγγραφές
    cursor.execute("""
    INSERT INTO deliberations
    (law_num, law_title, ministry, deliberation_title, deliberation_start, deliberation_end, source, last_updated)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, ("1234", "Νόμος Δοκιμής", "Υπουργείο Παιδείας", "Συζήτηση για θέμα Χ", "2026-02-01", "2026-02-05", "manual", datetime.now().isoformat()))

    cursor.execute("""
    INSERT INTO deliberations
    (law_num, law_title, ministry, deliberation_title, deliberation_start, deliberation_end, source, last_updated)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, ("5678", "Νόμος Δοκιμής 2", "Υπουργείο Οικονομικών", "Συζήτηση για θέμα Υ", "2026-01-15", "2026-01-20", "manual", datetime.now().isoformat()))

    conn.commit()
    conn.close()
    print("Inserted sample data successfully!")

if __name__ == "__main__":
    insert_sample()
