# backend/db_handler.py
import sqlite3
import json
from datetime import datetime

def connect_db(DB_PATH):
    return sqlite3.connect(DB_PATH)

def init_db(DB_PATH):
    conn = connect_db(DB_PATH)
    cur = conn.cursor()

    # Doctors
    cur.execute('''
        CREATE TABLE IF NOT EXISTS doctors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            specialization TEXT NOT NULL,
            available_days TEXT,
            available_times TEXT
        )
    ''')

    # Patients
    cur.execute('''
        CREATE TABLE IF NOT EXISTS patients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            dob TEXT NOT NULL,
            contact_info TEXT,
            unique_key TEXT UNIQUE
        )
    ''')

    # Appointments
    cur.execute('''
        CREATE TABLE IF NOT EXISTS appointments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id INTEGER,
            doctor_id INTEGER,
            date TEXT,
            time TEXT,
            status TEXT DEFAULT 'confirmed',
            FOREIGN KEY (patient_id) REFERENCES patients(id),
            FOREIGN KEY (doctor_id) REFERENCES doctors(id)
        )
    ''')

    conn.commit()
    conn.close()
