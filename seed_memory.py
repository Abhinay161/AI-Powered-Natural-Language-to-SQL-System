from vanna_setup import get_agent

agent = get_agent()

training_data = [
    ("How many patients are there?", "SELECT COUNT(*) AS total_patients FROM patients"),
    ("List all doctors", "SELECT name, specialization FROM doctors"),
    ("Show unpaid invoices", "SELECT * FROM invoices WHERE status != 'Paid'"),
    ("Total revenue", "SELECT SUM(paid_amount) FROM invoices"),
    ("Appointments today", "SELECT * FROM appointments WHERE DATE(appointment_date)=DATE('now')")
]

for question, sql in training_data:
    agent.memory.save_correct_tool_use(
        question,
        {"sql": sql}
    )

print("✅ Memory seeded successfully")