from langchain_community.utilities.sql_database import SQLDatabase
from langchain_community.agent_toolkits import create_sql_agent
from langchain_core.tools import create_retriever_tool
from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone
from langchain.tools import tool
from llms import llm, embeddings
import sqlite3

# Retriever Tool

pc = Pinecone()

index_name = "wellington-grace-hospital-info"

index = pc.Index(index_name)

vector_store = PineconeVectorStore(index=index, embedding=embeddings)

retriever = vector_store.as_retriever(
    search_type="similarity_score_threshold",
    search_kwargs={"k": 4, "score_threshold": 0.4},
)

ask_hospital_info = create_retriever_tool(
    retriever,
    "ask_hospital_info",
    "Use this tool to answer general questions about the hospital, including facilities, departments, amenities, location, services, timings, and more.",
)

# Sql Agent tool

db = SQLDatabase.from_uri('sqlite:///db/hospital.db')

gemini_agent_executor = create_sql_agent(
    llm=llm,
    db=db,
    agent_type="zero-shot-react-description",
    verbose=False,
)

@tool
def ask_database(query: str) -> str:
    """
    Use this tool to retrieve information from the hospital database.
    It is suitable for answering questions related to doctors' schedules, patient records, and appointment details.
    such as availabilities, past appointments, doctors, specialities etc.
    """
    return gemini_agent_executor.invoke(query)

@tool
def book_appointment(name: str, contact_info: str, doctor_name: str, date: str, time: str, dob: str) -> str:
    """
    Use this tool to book a new appointment in the hospital.
    It requires patient's name, contact info, date of birth, doctor's name, date (YYYY-MM-DD), and time (HH:MM in 24hr format).
    """
    try:
        conn = sqlite3.connect("db/hospital.db")
        cursor = conn.cursor()

        # 1. Get or create patient
        cursor.execute("SELECT id FROM patients WHERE name = ? AND contact_info = ?", (name, contact_info))
        patient = cursor.fetchone()

        if patient:
            patient_id = patient[0]
        else:
            cursor.execute("INSERT INTO patients (name, contact_info, dob, unique_key) VALUES (?, ?, ?, ?)",
                           (name, contact_info, dob, name + "_" + contact_info))
            patient_id = cursor.lastrowid

        # 2. Get doctor id
        cursor.execute("SELECT id FROM doctors WHERE name = ?", (doctor_name,))
        doctor = cursor.fetchone()
        if not doctor:
            return f"Doctor named {doctor_name} not found."
        doctor_id = doctor[0]

        # 3. Insert appointment
        cursor.execute("""
            INSERT INTO appointments (patient_id, doctor_id, date, time, status)
            VALUES (?, ?, ?, ?, ?)
        """, (patient_id, doctor_id, date, time, "scheduled"))

        conn.commit()
        return f"Appointment booked successfully with Dr. {doctor_name} on {date} at {time}."

    except Exception as e:
        return f"Failed to book appointment: {str(e)}"

    finally:
        conn.close()


tools = [ask_database, book_appointment, ask_hospital_info]