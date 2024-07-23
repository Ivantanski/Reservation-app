"""Seed reservation system with fake data."""

import random
from faker import Faker
import psycopg2
import datetime

NUM_GUESTS = [1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 3, 4, 4, 4, 5, 5, 6, 7, 8, 9]
NUM_CUSTOMERS = 100

fake = Faker()

# Establish connection
conn = psycopg2.connect("postgresql://localhost:5433/joel")
curs = conn.cursor()

# Truncate tables
curs.execute("TRUNCATE customers RESTART IDENTITY CASCADE")

# Insert fake customers
for _ in range(NUM_CUSTOMERS):
    phone = fake.phone_number() if random.random() < 0.5 else None
    notes = fake.sentence() if random.random() < 0.3 else ""
    first_name = fake.first_name()
    last_name = fake.last_name()
    curs.execute(
        "INSERT INTO customers (first_name, last_name, phone, notes) VALUES (%s, %s, %s, %s)",
        (first_name, last_name, phone, notes)
    )

# Insert fake reservations
for _ in range(2 * NUM_CUSTOMERS):
    customer_id = random.randint(1, NUM_CUSTOMERS)
    start_at = fake.date_time_this_year(after_now=True)
    num_guests = random.choice(NUM_GUESTS)
    notes = fake.sentence() if random.random() < 0.3 else ""

    curs.execute(
        "INSERT INTO reservations (customer_id, num_guests, start_at, notes) VALUES (%s, %s, %s, %s)",
        (customer_id, num_guests, start_at, notes)
    )

# Commit changes
conn.commit()

# Close connection
curs.close()
conn.close()

