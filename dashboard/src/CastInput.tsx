import { Box, Button, TextField } from "@mui/material"

export default function CastInput() {
  return (
    <Box sx={{ position: "relative" }}>
      <TextField label="YouTube URL" variant="outlined" fullWidth />
      <Button
        variant="contained"
        sx={{
          position: "absolute",
          right: 10,
          top: "50%",
          transform: "translateY(-50%)",
        }}
      >
        Add
      </Button>
    </Box>
  )
}
