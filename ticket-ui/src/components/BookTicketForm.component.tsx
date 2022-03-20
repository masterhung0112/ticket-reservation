import React from "react";
import { Box, Button, FormControl, TextField } from "@mui/material";
import PhoneInput from "react-phone-number-input";
import { Controller, useForm } from "react-hook-form";

export interface BookTicketFormData {
  username: string;
  telephone: string;
  email: string;
  seat_count: string;
}

export interface BookTicketFormProps {
  loading: boolean;
  submitBook(formData: BookTicketFormData): Promise<void>;
}

export const BookTicketForm: React.FC<BookTicketFormProps> = ({
  loading,
  submitBook,
}) => {
  const {
    handleSubmit,
    control,
    formState: { errors },
  } = useForm<BookTicketFormData>();

  const onFormSubmit = (data: BookTicketFormData) => {
    // console.log("Email:", email, "Password: ", password);
    // You should see email and password in console.
    // ..code to submit form to backend here...
    // console.log(data);
    submitBook && submitBook(data);
  };

  return (
    <Box sx={{ display: "flex", flexWrap: "wrap" }}>
      <form onSubmit={handleSubmit(onFormSubmit)}>
        <Controller
          name="username"
          control={control}
          rules={{ required: true }}
          render={({ field }) => (
            <TextField
              {...field}
              required
              name="username"
              label="Name"
              fullWidth
              margin="normal"
              error={!!errors.username}
              disabled={loading}
            />
          )}
        />
        <Controller
          name="email"
          control={control}
          rules={{
            required: true,
            pattern: {
              value: /^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$/i,
              message: "Invalid email address",
            },
          }}
          render={({ field }) => (
            <TextField
              {...field}
              required
              name="email"
              label="Email"
              fullWidth
              margin="normal"
              error={!!errors.email}
              helperText={errors.email && errors.email.message}
              disabled={loading}
            />
          )}
        />
        <FormControl fullWidth margin="normal" required>
          <Controller
            name="telephone"
            control={control}
            rules={{ required: true }}
            render={({ field }) => (
              <PhoneInput {...field} placeholder="Enter phone number" />
            )}
          />
        </FormControl>
        <Controller
          name="seat_count"
          control={control}
          rules={{ required: true }}
          render={({ field }) => (
            <TextField
              {...field}
              name="seatCount"
              label="Seats"
              type="number"
              InputLabelProps={{
                shrink: true,
              }}
              required
              fullWidth
              margin="normal"
              error={!!errors?.seat_count}
              disabled={loading}
            />
          )}
        />
        <Button type="submit" variant="contained" fullWidth disabled={loading}>
          Book
        </Button>
      </form>
    </Box>
  );
};
