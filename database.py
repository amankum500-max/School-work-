"""Database Layer"""
import sqlite3
from datetime import datetime

DB_FILE = "school.db"

def get_db():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    c = conn.cursor()
    c.executescript("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE, password TEXT, role TEXT,
        full_name TEXT, active INTEGER DEFAULT 1);

    CREATE TABLE IF NOT EXISTS students(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        roll_no TEXT UNIQUE, name TEXT, father TEXT, mother TEXT,
        class_name TEXT, section TEXT, gender TEXT, dob TEXT,
        contact TEXT, parent_contact TEXT, address TEXT,
        admission_date TEXT, transport_route TEXT, hostel TEXT);

    CREATE TABLE IF NOT EXISTS marks(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        roll_no TEXT, subject TEXT, exam TEXT,
        marks TEXT, total TEXT);

    CREATE TABLE IF NOT EXISTS student_fees(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        roll_no TEXT UNIQUE,
        tuition_fee REAL DEFAULT 0, transport_fee REAL DEFAULT 0,
        hostel_fee REAL DEFAULT 0, admission_fee REAL DEFAULT 0,
        dress_fee REAL DEFAULT 0, exam_fee REAL DEFAULT 0,
        book_fee REAL DEFAULT 0, notebook_fee REAL DEFAULT 0,
        misc_fee REAL DEFAULT 0, admission_paid INTEGER DEFAULT 0);

    CREATE TABLE IF NOT EXISTS bills(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        bill_no TEXT UNIQUE, roll_no TEXT, month TEXT, bill_date TEXT,
        tuition REAL DEFAULT 0, transport REAL DEFAULT 0, hostel REAL DEFAULT 0,
        admission REAL DEFAULT 0, dress REAL DEFAULT 0, exam REAL DEFAULT 0,
        book REAL DEFAULT 0, notebook REAL DEFAULT 0, misc REAL DEFAULT 0,
        prev_due REAL DEFAULT 0, total REAL DEFAULT 0, paid REAL DEFAULT 0,
        balance REAL DEFAULT 0, status TEXT DEFAULT 'Unpaid');

    CREATE TABLE IF NOT EXISTS payments(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        receipt_no TEXT, roll_no TEXT, bill_id INTEGER,
        amount REAL, mode TEXT, pay_date TEXT, remark TEXT);

    CREATE TABLE IF NOT EXISTS expenses(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        category TEXT, description TEXT, amount REAL,
        exp_date TEXT, staff_id TEXT);
    """)

    default_users = [
        ("admin", "admin123", "Admin", "School Admin"),
        ("accountant", "acc123", "Accountant", "Head Accountant"),
        ("teacher", "teach123", "Teacher", "Class Teacher"),
    ]
    for u, p, r, n in default_users:
        try:
            c.execute("INSERT INTO users(username,password,role,full_name) VALUES(?,?,?,?)",
                      (u, p, r, n))
        except sqlite3.IntegrityError:
            pass

    conn.commit()
    conn.close()

def run(q, p=()):
    conn = get_db()
    cur = conn.execute(q, p)
    conn.commit()
    lastid = cur.lastrowid
    conn.close()
    return lastid

def all(q, p=()):
    conn = get_db()
    rows = conn.execute(q, p).fetchall()
    conn.close()
    return rows

def one(q, p=()):
    conn = get_db()
    row = conn.execute(q, p).fetchone()
    conn.close()
    return row

def current_month():
    return datetime.now().strftime("%Y-%m")

def today():
    return datetime.now().strftime("%Y-%m-%d")
