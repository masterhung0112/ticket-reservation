import { Alert, Grid } from "@mui/material";
import React, { useState } from "react";
import {
  BookTicketForm,
  BookTicketFormData,
} from "../components/BookTicketForm.component";
import { useTicketBook } from "../hooks/useTicketBook";

const randomText = () => (Math.random() + 1).toString(36).substring(7);

const BookTicketContainer: React.FC = () => {
  const { ticketBookState, ticketBookApi } = useTicketBook();
  const [idempotentId, setIdempotentId] = useState(randomText());
  const [error, setError] = useState<string | undefined>(undefined);

  const submitTicketBook = async (formData: BookTicketFormData) => {
    try {
      setError(undefined);
      await ticketBookApi.bookTickets(
        formData.username,
        formData.telephone,
        formData.email,
        parseFloat(formData.seat_count),
        idempotentId
      );
    } catch (e) {
      if (e instanceof Error) {
        setError(e.message);
      } else {
        setError(`${e}`);
      }
    }
  };

  return (
    <Grid
      container
      direction="row"
      justifyContent="center"
      alignItems="center"
      padding="12px"
    >
      {error ? (
        <Grid item md={8} xs={12}>
          <Alert severity="error">error</Alert>
        </Grid>
      ) : null}
      <Grid item md={8} xs={12}>
        <BookTicketForm
          loading={ticketBookState.loading}
          submitBook={submitTicketBook}
        />
      </Grid>
      <Grid item md={8} xs={12}>
        {ticketBookState.bookRequestResult ? <div>
          <h2>Your ticket</h2>
          <h3>PNR:</h3>
          <p>{ticketBookState.bookRequestResult.pnr}</p>
          <h3>Allocated Seats:</h3>
          <p>{ticketBookState.bookRequestResult.allocatedSeats.join(', ')}</p>
        </div> : null}
      </Grid>
    </Grid>
  );
};

export default BookTicketContainer;
