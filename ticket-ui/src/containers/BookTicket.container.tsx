import { Grid } from "@mui/material";
import React from "react";
import { BookTicketForm } from "../components/BookTicketForm.component";

const BookTicketContainer: React.FC = () => {
  return (
    <Grid container direction="row" justifyContent="center" alignItems="center">
      <BookTicketForm submitBook={async () => {}} />
      Display result      
    </Grid>
  );
};

export default BookTicketContainer;
