import sqlite3
import random
from datetime import datetime, timedelta

conn = sqlite3.connect("clinic.db")
cursor = conn.cursor()

cursor.executescript("""
DROP TABLE IF EXISTS patients;
DROP TABLE IF EXISTS doctors;
DROP TABLE IF EXISTS appointments;
DROP TABLE IF EXISTS treatments;
DROP TABLE IF EXISTS invoices;

CREATE TABLE patients (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT,
    last_name TEXT,
    email TEXT,
    phone TEXT,
    date_of_birth DATE,
    gender TEXT,
    city TEXT,
    registered_date DATE
);

CREATE TABLE doctors (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    specialization TEXT,
    department TEXT,
    phone TEXT
);

CREATE TABLE appointments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    patient_id INTEGER,
    doctor_id INTEGER,
    appointment_date DATETIME,
    status TEXT,
    notes TEXT
);

CREATE TABLE treatments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    appointment_id INTEGER,
    treatment_name TEXT,
    cost REAL,
    duration_minutes INTEGER
);

CREATE TABLE invoices (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    patient_id INTEGER,
    invoice_date DATE,
    total_amount REAL,
    paid_amount REAL,
    status TEXT
);
""")

first_names = ["John","Jane","Alex","Chris","Sam","Anvesh","Rahul","Priya"]
last_names = ["Smith","Doe","Kumar","Reddy","Sharma","Patel"]
cities = ["Hyderabad","Delhi","Mumbai","Chennai","Bangalore","Pune"]
specializations = ["Dermatology","Cardiology","Orthopedics","General","Pediatrics"]
statuses = ["Scheduled","Completed","Cancelled","No-Show"]

# Insert doctors
for _ in range(15):
    cursor.execute(
        "INSERT INTO doctors (name,specialization,department,phone) VALUES (?,?,?,?)",
        (random.choice(first_names)+" Dr", random.choice(specializations), "Dept", "9999999999")
    )

# Insert patients
for _ in range(200):
    cursor.execute(
        "INSERT INTO patients (first_name,last_name,email,phone,date_of_birth,gender,city,registered_date) VALUES (?,?,?,?,?,?,?,?)",
        (
            random.choice(first_names),
            random.choice(last_names),
            None,
            None,
            "1990-01-01",
            random.choice(["M","F"]),
            random.choice(cities),
            datetime.now().date()
        )
    )

# Insert appointments
for _ in range(500):
    date = datetime.now() - timedelta(days=random.randint(0,365))
    cursor.execute(
        "INSERT INTO appointments (patient_id,doctor_id,appointment_date,status,notes) VALUES (?,?,?,?,?)",
        (
            random.randint(1,200),
            random.randint(1,15),
            date,
            random.choice(statuses),
            None
        )
    )

# Insert treatments
for _ in range(350):
    cursor.execute(
        "INSERT INTO treatments (appointment_id,treatment_name,cost,duration_minutes) VALUES (?,?,?,?)",
        (
            random.randint(1,500),
            "Treatment",
            random.randint(50,5000),
            random.randint(10,120)
        )
    )

# Insert invoices
for _ in range(300):
    total = random.randint(100,5000)
    paid = random.randint(0,total)
    status = "Paid" if paid == total else random.choice(["Pending","Overdue"])

    cursor.execute(
        "INSERT INTO invoices (patient_id,invoice_date,total_amount,paid_amount,status) VALUES (?,?,?,?,?)",
        (
            random.randint(1,200),
            datetime.now().date(),
            total,
            paid,
            status
        )
    )

conn.commit()
conn.close()

print("✅ Database created successfully")