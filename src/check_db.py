import sqlite3
import os
import pandas as pd

DB_PATH = "output/asana_simulation.sqlite"

def run_query(conn, query, description):
    print(f"\n--- {description} ---")
    try:
        df = pd.read_sql_query(query, conn)
        if df.empty:
            print("Result: Empty")
        else:
            print(df.to_string(index=False))
    except Exception as e:
        print(f"Error: {e}")

def main():
    if not os.path.exists(DB_PATH):
        print(f"Database file not found at {DB_PATH}")
        return

    conn = sqlite3.connect(DB_PATH)
    
    print("="*40)
    print(f"DATABASE INSPECTION: {DB_PATH}")
    print("="*40)

    run_query(conn, """
        SELECT 
            (SELECT COUNT(*) FROM users) as Total_Users,
            (SELECT COUNT(*) FROM teams) as Total_Teams,
            (SELECT COUNT(*) FROM projects) as Total_Projects,
            (SELECT COUNT(*) FROM tasks) as Total_Tasks
    """, "Data Volume Statistics")

    run_query(conn, """
        SELECT 
            t.name as Team_Name, 
            COUNT(tm.user_id) as Member_Count
        FROM teams t
        JOIN team_memberships tm ON t.id = tm.team_id
        GROUP BY t.id
        ORDER BY Member_Count DESC
        LIMIT 5
    """, "Top 5 Largest Teams")

    run_query(conn, """
        SELECT 
            t.name as Team, 
            u.full_name as Team_Lead, 
            tm.role
        FROM team_memberships tm
        JOIN users u ON tm.user_id = u.id
        JOIN teams t ON tm.team_id = t.id
        WHERE tm.role = 'admin'
        LIMIT 5
    """, "Sample Team Leaders")

    run_query(conn, """
        SELECT count(*) as Invalid_Time_Travel_Tasks
        FROM tasks 
        WHERE completed_at < created_at
    """, "Integrity Check: Tasks completed before creation")

    run_query(conn, """
        SELECT 
            is_completed, 
            COUNT(*) as Count 
        FROM tasks 
        GROUP BY is_completed
    """, "Completion Rates")

    conn.close()

if __name__ == "__main__":
    main()