import mongoose from 'mongoose';

export const fakeUsers = [
  {
    _id: new mongoose.Types.ObjectId(),
    firstName: "John",
    lastName: "Doe",
    email: "john.doe@example.com",
    isVerified: true,
    currentLocation: "New York, USA",
    currentLocationFootprint: "US",
    createdAt: new Date("2023-01-15T10:00:00Z"),
    updatedAt: new Date("2023-11-20T15:00:00Z"),
    preferredLanguage: "EN",
    numberOfEsims: 2,
  },
  {
    _id: new mongoose.Types.ObjectId(),
    firstName: "Jane",
    lastName: "Smith",
    email: "jane.smith@example.com",
    isVerified: false,
    currentLocation: "London, UK",
    currentLocationFootprint: "GB",
    createdAt: new Date("2023-05-01T08:30:00Z"),
    updatedAt: new Date("2023-12-10T14:20:00Z"),
    preferredLanguage: "EN",
    numberOfEsims: 0,
  },
  {
    _id: new mongoose.Types.ObjectId(),
    firstName: "Carlos",
    lastName: "Gomez",
    email: "carlos.gomez@example.com",
    isVerified: true,
    currentLocation: "Barcelona, Spain",
    currentLocationFootprint: "ES",
    createdAt: new Date("2022-10-12T09:45:00Z"),
    updatedAt: new Date("2024-01-05T12:00:00Z"),
    preferredLanguage: "ES",
    numberOfEsims: 1,
  },
  {
    _id: new mongoose.Types.ObjectId(),
    firstName: "Anna",
    lastName: "Ivanova",
    email: "anna.ivanova@example.com",
    isVerified: false,
    currentLocation: "Moscow, Russia",
    currentLocationFootprint: "RU",
    createdAt: new Date("2023-03-20T13:15:00Z"),
    updatedAt: new Date("2023-11-29T18:00:00Z"),
    preferredLanguage: "RU",
    numberOfEsims: 0,
  },
  {
    _id: new mongoose.Types.ObjectId(),
    firstName: "Liam",
    lastName: "Murphy",
    email: "liam.murphy@example.com",
    isVerified: true,
    currentLocation: "Dublin, Ireland",
    currentLocationFootprint: "IE",
    createdAt: new Date("2021-11-05T16:45:00Z"),
    updatedAt: new Date("2023-10-15T19:30:00Z"),
    preferredLanguage: "EN",
    numberOfEsims: 2,
  },
  {
    _id: new mongoose.Types.ObjectId(),
    firstName: "Yuki",
    lastName: "Tanaka",
    email: "yuki.tanaka@example.com",
    isVerified: false,
    currentLocation: "Tokyo, Japan",
    currentLocationFootprint: "JP",
    createdAt: new Date("2023-07-18T07:25:00Z"),
    updatedAt: new Date("2023-09-20T12:45:00Z"),
    preferredLanguage: "JP",
    numberOfEsims: 0,
  },
  {
    _id: new mongoose.Types.ObjectId(),
    firstName: "Amara",
    lastName: "Okafor",
    email: "amara.okafor@example.com",
    isVerified: true,
    currentLocation: "Lagos, Nigeria",
    currentLocationFootprint: "NG",
    createdAt: new Date("2022-04-11T10:15:00Z"),
    updatedAt: new Date("2024-02-12T13:30:00Z"),
    preferredLanguage: "EN",
    numberOfEsims: 1,
  },
  {
    _id: new mongoose.Types.ObjectId(),
    firstName: "Chen",
    lastName: "Wang",
    email: "chen.wang@example.com",
    isVerified: false,
    currentLocation: "Shanghai, China",
    currentLocationFootprint: "CN",
    createdAt: new Date("2023-02-22T11:40:00Z"),
    updatedAt: new Date("2023-06-19T16:20:00Z"),
    preferredLanguage: "ZH",
    numberOfEsims: 0,
  },
  {
    _id: new mongoose.Types.ObjectId(),
    firstName: "Fatima",
    lastName: "Hassan",
    email: "fatima.hassan@example.com",
    isVerified: true,
    currentLocation: "Cairo, Egypt",
    currentLocationFootprint: "EG",
    createdAt: new Date("2020-12-30T14:55:00Z"),
    updatedAt: new Date("2024-01-15T17:00:00Z"),
    preferredLanguage: "AR",
    numberOfEsims: 1,
  },
  {
    _id: new mongoose.Types.ObjectId(),
    firstName: "Emily",
    lastName: "Johnson",
    email: "emily.johnson@example.com",
    isVerified: true,
    currentLocation: "Vancouver, Canada",
    currentLocationFootprint: "CA",
    createdAt: new Date("2023-09-01T09:00:00Z"),
    updatedAt: new Date("2023-12-25T14:45:00Z"),
    preferredLanguage: "EN",
    numberOfEsims: 0,
  },
]

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
        "preferredLanguage": random.choice(["EN", "ES", "FR", "DE", "JP"]),
        "numberOfEsims": random.randint(0, 5)
    }

fake_users = [generate_user() for _ in range(10)]

# Print the generated users
if __name__ == "__main__":
    for user in fake_users:
        print(user)

