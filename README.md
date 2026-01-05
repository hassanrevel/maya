# 🏥 Maya — Agentic AI Hospital Receptionist

Maya is a conversational, goal-oriented AI system designed to automate the front-desk responsibilities of a hospital receptionist. Built using modern agentic AI patterns, Maya can answer hospital FAQs, check doctor availability, and book appointments through natural language dialogue while remaining grounded in structured hospital data.

This project demonstrates how a **single-agent, tool-augmented LLM** can reliably handle real-world administrative workflows in healthcare without the complexity of multi-agent orchestration.

---

## ✨ Key Features

- **Conversational Appointment Booking**  
  Collects patient details and schedules appointments via natural dialogue.

- **Doctor Availability & Scheduling**  
  Queries structured hospital databases to provide accurate availability information.

- **Hospital FAQs via RAG**  
  Answers questions about departments, services, visiting hours, facilities, and more using retrieval-augmented generation.

- **Goal-Oriented Reasoning (ReAct)**  
  Each user request is treated as a goal and solved through iterative Reason → Act → Observe steps.

- **Persistent Multi-Turn Memory**  
  Conversation context is preserved across turns using session-based memory.

- **Low-Complexity, High-Reliability Design**  
  A single-agent architecture with deterministic tools reduces failure modes compared to multi-agent systems.

---

## 🧠 System Architecture

Maya is implemented as a **stateful agent graph** using LangGraph:

- **LLM Reasoning Layer**  
  Interprets user intent and decides when to call tools.

- **Tool Layer**
  - SQL database access for doctors, patients, and appointments  
  - Vector search (Pinecone) for hospital knowledge  
  - Deterministic appointment booking logic  

- **Memory Layer**  
  Stores dialogue history for coherent multi-turn interactions.

This separation ensures that responses remain **context-aware, fluent, and factually grounded**.

---

## 🛠️ Tech Stack

- **Frontend**: Streamlit  
- **LLM**: Google Gemini (via LangChain)  
- **Agent Framework**: LangGraph  
- **RAG**: Pinecone + LangChain Retriever Tools  
- **Database**: SQLite  
- **Embeddings**: Google Generative AI Embeddings  

---

## 📁 Project Structure

```
.
├── main.py
├── maya_agent.py
├── tools.py
├── llms.py
├── ingest_RAG_info.py
├── setup.py
├── data/
│   └── hospital_info.txt
├── backend/
│   ├── db_handler.py
│   └── doc_handler.py
└── db/
    └── hospital.db
```

---

## 🚀 Getting Started

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Set Environment Variables
Create a `.env` file:
```env
GOOGLE_API_KEY=your_key_here
PINECONE_API_KEY=your_key_here
```

### 3. Initialize the Database
```bash
python setup.py
python backend/doc_handler.py
```

### 4. Ingest Hospital Knowledge (RAG)
```bash
python ingest_RAG_info.py
```

### 5. Run the Application
```bash
streamlit run main.py
```

---

## 💬 Example Queries

- “What departments does the hospital have?”
- “Is Dr. Charlotte Reeves available on Friday?”
- “Book an appointment with a cardiologist next Tuesday at 10am.”
- “Where is the emergency department located?”

---

## 📊 Design Rationale

Maya uses a **single-agent, tool-augmented design** rather than a multi-agent system. This approach reduces orchestration complexity, improves reliability, and ensures deterministic control over sensitive operations such as appointment booking.

---

## ⚠️ Limitations & Future Work

- No authentication or role-based access control  
- Limited to a single hospital schema  
- No conflict resolution for overlapping appointments  
- Scenario-based evaluation only  

Future work may include calendar integrations, patient portals, multilingual support, and advanced analytics.

---

## 📚 Research Context

This project strongly aligns with current research in conversational AI for healthcare administration, ReAct-style reasoning, agentic workflows using state graphs, and practical scalable alternatives to complex multi-agent systems.
