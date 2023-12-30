import { Component } from '@angular/core';
import { HttpClient } from '@angular/common/http';

interface BookingResponse {
  message: string;
  seats_booked: number[];
}

@Component({
  selector: 'app-seat-booking',
  templateUrl: './seat-booking.component.html',
  styleUrls: ['./seat-booking.component.css']
})
export class SeatBookingComponent {
  formData = {
    name: '',
    age: '',
    pickup: '', // Add other fields (pickup, destination, phone_number, email) here
    destination: '',
    phone_number: '',
    email: '',
    numSeats: 1
  };

  response: BookingResponse | null = null;

  constructor(private http: HttpClient) { }

  bookSeats() {
    this.http.post<BookingResponse>('http://localhost:8000/book_seat/', this.formData)
      .subscribe(
        (data) => {
          this.response = data;
        },
        (error) => {
          console.error('Error:', error.error.detail);
          this.response = null;
        }
      );
  }
}
