import { useAppStore } from "../stores"
import { Stack } from "@mui/material"

export default function EpisodePlayer() {
  const episode = useAppStore(state => state.playingEpisode)
  if (!episode) return null

  return (
    <Stack
      direction="row"
      sx={{
        width: "100%",
        position: "fixed",
        bottom: 0,
        left: 0,
        justifyContent: "center",
        py: 2,
      }}
    >
      <audio controls autoPlay src={`/episodes/${episode.audio_file}`}>
        Your browser does not support the audio element.
      </audio>
    </Stack>
  )
}
