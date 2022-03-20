import { useState } from "react";
import { TicketBookReply, TicketBookRequest } from "../models/BookRequest";

const SERVER_HOST = "http://localhost:8000";

export interface BookRequestResult {
    pnr: string
    allocatedSeats: string[]
}

export interface UseTicketBookState {
    loading: boolean
    bookRequestResult: BookRequestResult | undefined
}

// The list of API related to ticket
export interface UseTicketBookApi {
  bookTickets(
    username: string,
    phoneNumber: string,
    email: string,
    seatCount: number,
    idempotentID: string
  ): Promise<TicketBookReply>;
}

// Return type of useTicketBook hook
export interface UseTicketBook {
  ticketBookState: UseTicketBookState;
  ticketBookApi: UseTicketBookApi;
}

export const useTicketBook = (): UseTicketBook => {
  // Indicating that we are request response from server
  const [loading, setLoading] = useState(false);
  // Store the result returned by server
  const [bookRequestResult, setBookRequestResult] = useState<BookRequestResult>()

  return {
    ticketBookState: { loading, bookRequestResult },
    ticketBookApi: {
      bookTickets: async (
        username,
        phoneNumber,
        email,
        seatCount,
        idempotentID
      ) => {
        setLoading(true);
        setBookRequestResult(undefined)

        try {
          // Request to server
          const response = await fetch(`${SERVER_HOST}/ticket/book`, {
            headers: {
              Accept: "application/json",
              "Content-Type": "application/json",
            },
            mode: 'cors',
            method: "POST",
            body: JSON.stringify({
              username: username,
              telephone: phoneNumber,
              email: email,
              seat_count: seatCount,
              idempotent_id: idempotentID,
            } as TicketBookRequest),
          });
          const ticketBookReply: TicketBookReply = await response.json();

          // Convert response to the local data
          if (response.status === 200) {
            if (ticketBookReply.error) {
              throw Error(ticketBookReply.error);
            }

            setBookRequestResult({
                allocatedSeats: ticketBookReply.allocated_seats,
                pnr: ticketBookReply.request.pnr,
            })
            return ticketBookReply;
          } else {
            if (ticketBookReply.error) {
              throw new Error(ticketBookReply.error);
            }
            throw Error(`unknown error: ${response.status}`);
          }
        } finally {
          setLoading(false);
        }
      },
    },
  };
};
