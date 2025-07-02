import { Container, Stack } from "@mui/material"
import CastInput from "./CastInput"
import EpisodesList from "./EpisodesList"
import ToastContainer from "./components/toastify"
import "./App.css"

function App() {
  return (
    <>
      <Container>
        <h1>VPodcasts</h1>
        <Stack spacing={5}>
          <CastInput />
          <EpisodesList />
        </Stack>
      </Container>
      <ToastContainer />
    </>
  )
}

export default App
