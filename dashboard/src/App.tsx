import { Container, Stack } from "@mui/material"
import CastInput from "./CastInput"
import EpisodesList from "./EpisodesList"

function App() {
  return (
    <Container>
      <h1>VPodcasts</h1>
      <Stack spacing={5}>
        <CastInput />
        <EpisodesList />
      </Stack>
    </Container>
  )
}

export default App
