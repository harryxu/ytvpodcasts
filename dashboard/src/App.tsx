import { Container, Stack } from "@mui/material"
import CastInput from "./CastInput"
import EpisodesList from "./EpisodesList"
import ToastContainer from "./components/toastify"
import "./App.css"
import { QueryClient, QueryClientProvider } from "@tanstack/react-query"

const queryClient = new QueryClient()

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <Container>
        <h1>VPodcasts</h1>
        <Stack spacing={5}>
          <CastInput />
          <EpisodesList />
        </Stack>
      </Container>
      <ToastContainer />
    </QueryClientProvider>
  )
}

export default App
