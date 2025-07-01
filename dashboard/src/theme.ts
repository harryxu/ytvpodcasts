import { createTheme } from "@mui/material/styles"

const theme = createTheme({
  components: {
    MuiButtonBase: {
      defaultProps: {
        disableRipple: true,
        disableTouchRipple: true,
      },
    },
    MuiButton: {
      defaultProps: {
        // disableElevation: true,
      },
    },
    MuiIconButton: {
      defaultProps: {
        disableRipple: true,
        disableTouchRipple: true,
      },
    },
    MuiFab: {
      defaultProps: {
        disableRipple: true,
      },
    },
  },
})

export default theme
