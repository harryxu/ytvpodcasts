import { ThemeProvider } from "@mui/material"
import CssBaseline from "@mui/material/CssBaseline"
import { StrictMode } from "react"
import { createRoot } from "react-dom/client"
import theme from "./theme.ts"

import { RouterProvider, createRouter } from "@tanstack/react-router"
import { routeTree } from "./routeTree.gen"
import { QueryClient, QueryClientProvider } from "@tanstack/react-query"

const basepath = import.meta.env.PROD ? "/dashboard" : "/"

const router = createRouter({ routeTree, basepath })

declare module "@tanstack/react-router" {
  interface Register {
    router: typeof router
  }
}

const queryClient = new QueryClient()

createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <QueryClientProvider client={queryClient}>
        <RouterProvider router={router} />
      </QueryClientProvider>
    </ThemeProvider>
  </StrictMode>
)
