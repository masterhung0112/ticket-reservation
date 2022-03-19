export interface UseTicketBookState {

}

export interface UseTicketBookApi {
    bookTickets(
        username: string,
        phoneNumber: string,
        email: string,
        seatCount: number
    )
}

export interface UseTicketBook {
    ticketBookState: UseTicketBookState
    ticketBookApi: UseTicketBookApi
}

export const useTicketBook = (): UseTicketBook => {
    return {
        ticketBookState: {},
        ticketBookApi: {
            bookTickets: () => { throw Error('not implemented')}
        }
    }
}