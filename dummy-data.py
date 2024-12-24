import random
from faker import Faker

fake = Faker()

def generate_user():
    return {
        "_id": fake.uuid4(),
        "firstName": fake.first_name(),
        "lastName": fake.last_name(),
        "email": fake.unique.email(),
        "isVerified": random.choice([True, False]),
        "currentLocation": fake.city() + ", " + fake.country(),
        "currentLocationFootprint": fake.country_code(),
        "createdAt": fake.date_time_this_year().isoformat(),
        "updatedAt": fake.date_time_this_month().isoformat(),
        "preferredLanguage": random.choice(["EN", "ES", "FR", "IT"]),
        "numberOfEsims": random.randint(0, 5)
    }

fake_users = [generate_user() for _ in range(10)]

# Print the generated users
if __name__ == "__main__":
    for user in fake_users:
        print(user)
