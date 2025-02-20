# python-assignment

python app.py

keep this open

def generate_employee():
    diet_preferences = ["Vegan", "Vegetarian", "Halal", "Kosher", "Paleo", "Gluten-Free", "Dairy-Free", "Low-Carb", "Keto"]
    is_full_time = random.choice([True, False])

    if is_full_time:
        salary = random.randint(30000, 120000)
    else:
        salary = random.randint(10000, 40000)
    
    first_name = fake.first_name()
    last_name = fake.last_name()

    email = f"{first_name.lower()}.{last_name.lower()}@company.com"
    phone_number = f"07{random.randint(100000000, 999999999)}"

    return {
        "firstName": first_name,
        "lastName": last_name,
        "email": email,
        "isFullTime": is_full_time,
        "isActive": random.choice([True, False]),
        "salary": salary,
        "annualLeaveDays": random.randint(15, 28),
        "dietPreferences": random.sample(diet_preferences, k=random.randint(0, 2)),
        "phoneNumber": phone_number,
        "dateOfBirth": fake.date_of_birth(minimum_age=18, maximum_age=65).isoformat()
    }

collection.delete_many({})

# Insert 10 new employees
try:
    inserted_employees = collection.insert_many([generate_employee() for _ in range(10)])
    print(f"Successfully inserted {len(inserted_employees.inserted_ids)} employees.")
except Exception as e:
    print(f"Error inserting employees: {e}")

def insert_seed_employees(numberToInsert):
    try:
        inserted_employees = collection.insert_many([generate_employee() for _ in range(numberToInsert)])
        print(f"Successfully inserted {len(inserted_employees.inserted_ids)} employees.")
    except Exception as e:
        print(f"Error inserting employees: {e}")