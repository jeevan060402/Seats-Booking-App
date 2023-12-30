from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pymongo import MongoClient
from typing import List

app = FastAPI()

class SeatBooking(BaseModel):
    name: str
    age: int
    pickup: str
    destination: str
    phone_number: str
    email: str
    num_seats: int

# MongoDB Configuration
client = MongoClient("YOUR_MONGODB_CONNECTION_STRING")
db = client["train_db"]
seats_collection = db["booked_seats"]

total_seats = 80

def get_booked_seats():
    return [seat_doc['seat_number'] for seat_doc in seats_collection.find()]

@app.get("/available_seats/")
async def available_seats():
    booked_seats = get_booked_seats()
    return [seat for seat in range(1, total_seats + 1) if seat not in booked_seats]

@app.post("/book_seat/")
async def book_seat(seat_booking: SeatBooking):
    global total_seats

    booked_seats = get_booked_seats()

    if seat_booking.num_seats <= 0 or seat_booking.num_seats > 7:
        raise HTTPException(status_code=400, detail="Invalid number of seats")

    if len(booked_seats) + seat_booking.num_seats > total_seats:
        raise HTTPException(status_code=400, detail="Not enough seats available")

    available_seats = [seat for seat in range(1, total_seats + 1) if seat not in booked_seats]

    seats_to_book = []
    for seat in available_seats:
        if len(seats_to_book) < seat_booking.num_seats:
            seats_to_book.append(seat)

    booked_seat_numbers = []
    for seat_number in seats_to_book:
        seats_collection.insert_one({
            'seat_number': seat_number,
            'name': seat_booking.name,
            'age': seat_booking.age,
            'pickup': seat_booking.pickup,
            'destination': seat_booking.destination,
            'phone_number': seat_booking.phone_number,
            'email': seat_booking.email
        })
        booked_seat_numbers.append(seat_number)

    return {"message": "Seats booked successfully", "seats_booked": booked_seat_numbers}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
