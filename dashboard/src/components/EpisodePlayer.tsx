import { IconButton, Stack } from "@mui/material"
import { X } from "lucide-react"
import { useAppStore } from "../stores"
import { useEffect, useRef, useState } from "react"

export default function EpisodePlayer() {
  const episode = useAppStore(state => state.playingEpisode)
  const audioRef = useRef<HTMLAudioElement>(null)
  const [playerVisible, setPlayerVisible] = useState(false)

  useEffect(() => {
    if (!episode) {
      audioRef.current?.pause()
    }
  }, [episode])

  return (
    <Stack
      direction="row"
      onTransitionEnd={() => setPlayerVisible(episode ? true : false)}
      sx={{
        width: "100%",
        position: "fixed",
        bottom: episode ? "0" : "-100px",
        left: 0,
        alignItems: "center",
        justifyContent: "center",
        py: 2,
        pl: "40px",
        transition: "all 0.3s ease-in-out",
      }}
    >
      {(episode || playerVisible) && (
        <audio
          controls
          autoPlay
          src={episode ? `/episodes/${episode.audio_file}` : undefined}
          ref={audioRef}
        >
          Your browser does not support the audio element.
        </audio>
      )}
      <IconButton
        onClick={() => {
          useAppStore.setState({ playingEpisode: undefined })
        }}
      >
        <X />
      </IconButton>
    </Stack>
  )
}
