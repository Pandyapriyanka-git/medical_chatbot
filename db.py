import sqlite3
import os

DB_PATH = 'medical_knowledge.db'

def init_db():
    if not os.path.exists(DB_PATH):
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()

        # Create tables
        c.execute('''
            CREATE TABLE diseases (
                id INTEGER PRIMARY KEY,
                name TEXT,
                description TEXT,
                symptoms TEXT,
                treatments TEXT
            )
        ''')
        c.execute('''
            CREATE TABLE chat_history (
                id INTEGER PRIMARY KEY,
                question TEXT,
                answer TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # Add 5 diseases
        diseases = [
            ("Diabetes", "A chronic condition that affects how your body processes blood sugar (glucose).",
             "Increased thirst, frequent urination, hunger, fatigue, blurred vision.",
             "Insulin therapy, diet control, exercise, oral medications."),
            ("Hypertension", "A condition in which the force of the blood against artery walls is too high.",
             "Headaches, shortness of breath, nosebleeds, chest pain.",
             "Lifestyle changes, antihypertensive drugs, stress management."),
            ("Asthma", "A respiratory condition marked by spasms in the bronchi of the lungs.",
             "Wheezing, shortness of breath, chest tightness, coughing.",
             "Inhalers, corticosteroids, avoiding triggers."),
            ("Migraine", "A neurological condition that causes intense headaches and other symptoms.",
             "Throbbing pain, nausea, vomiting, sensitivity to light and sound.",
             "Pain relievers, anti-nausea drugs, preventive medications."),
            ("Kidney Infection", "A type of urinary tract infection (UTI) that travels to the kidneys.",
             "Fever, back or side pain, nausea, frequent urination, burning sensation when urinating.",
             "Antibiotics, hydration, hospital care in severe cases.")
        ]
        c.executemany("INSERT INTO diseases (name, description, symptoms, treatments) VALUES (?, ?, ?, ?)", diseases)

        conn.commit()
        conn.close()

def get_all_diseases():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT name, description, symptoms, treatments FROM diseases")
    rows = c.fetchall()
    conn.close()
    return [{'name': r[0], 'description': r[1], 'symptoms': r[2], 'treatments': r[3]} for r in rows]

def save_chat(question, answer):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO chat_history (question, answer) VALUES (?, ?)", (question, answer))
    conn.commit()
    conn.close()

def get_chat_history():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT question, answer, timestamp FROM chat_history ORDER BY timestamp DESC")
    rows = c.fetchall()
    conn.close()
    return rows

def delete_chat(question):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("DELETE FROM chat_history WHERE question = ?", (question,))
    conn.commit()
    conn.close()
