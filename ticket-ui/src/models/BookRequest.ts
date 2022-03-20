export interface TicketBookRequest {
  username: string;
  telephone: string;
  email: string;
  seat_count: number;
  idempotent_id: string;
}

export interface TicketBookReply {
  allocated_seats: string[]
  request: {
    username: string
    telephone: string
    email: string
    seat_count: number
    idempotent_id: string
    pnr: string
  }
  error?: string
}
