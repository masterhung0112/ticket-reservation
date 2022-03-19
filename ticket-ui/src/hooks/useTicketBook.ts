export interface UseTicketBookState {

}

export interface UseTicketBookApi {
    bookTickets(
        username: string,
        phoneNumber: string,
        email: string,
        seatCount: number
    ): Promise<void>
}

export interface UseTicketBook {
    ticketBookState: UseTicketBookState
    ticketBookApi: UseTicketBookApi
}

export const useTicketBook = (): UseTicketBook => {
    return {
        ticketBookState: {},
        ticketBookApi: {
            bookTickets: async () => { throw Error('not implemented')}
        }
    }
}