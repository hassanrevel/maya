# backend/doc_handler.py

import sqlite3
import json

DB_PATH = "../db/hospital.db"


def connect_db():
    return sqlite3.connect(DB_PATH)


def add_doctor(name, specialization, available_days, available_times):
    conn = connect_db()
    cur = conn.cursor()

    cur.execute('''
        INSERT INTO doctors (name, specialization, available_days, available_times)
        VALUES (?, ?, ?, ?)
    ''', (
        name,
        specialization,
        json.dumps(available_days),
        json.dumps(available_times)
    ))

    conn.commit()
    conn.close()


def seed_doctors():
    doctors = [
        {
            "name": "Dr. Charlotte Reeves",
            "specialization": "Dermatology",
            "available_days": ["Monday", "Wednesday", "Friday"],
            "available_times": ["09:00", "13:00"]
        },
        {
            "name": "Dr. Thomas Bennett",
            "specialization": "Cardiology",
            "available_days": ["Tuesday", "Thursday"],
            "available_times": ["10:00", "14:00"]
        },
        {
            "name": "Dr. Emily Harrington",
            "specialization": "Neurology",
            "available_days": ["Monday", "Thursday"],
            "available_times": ["08:30", "12:30"]
        },
        {
            "name": "Dr. Oliver Clarke",
            "specialization": "General Practice",
            "available_days": ["Monday", "Tuesday", "Friday"],
            "available_times": ["09:00", "17:00"]
        },
        {
            "name": "Dr. Amelia Patel",
            "specialization": "Paediatrics",
            "available_days": ["Wednesday", "Thursday"],
            "available_times": ["10:30", "15:30"]
        }
    ]

    for doc in doctors:
        add_doctor(**doc)


if __name__ == "__main__":
    seed_doctors()
    print("Doctors seeded successfully.")
