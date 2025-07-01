import { Box, Button, CircularProgress, TextField } from "@mui/material"
import useAxios from "axios-hooks"
import { useState } from "react"

function isYouTubeWatchUrl(url: string): boolean {
  const regex = /^https:\/\/(www\.)?youtube\.com\/watch\?v=/
  return regex.test(url)
}

export default function CastInput() {
  const [videoUrl, setVideoUrl] = useState("")
  const [castAddApi, executeAddCast] = useAxios(
    {
      url: "/api/add",
      method: "POST",
    },
    { manual: true }
  )

  const handleAdd = async () => {
    if (!isYouTubeWatchUrl(videoUrl)) {
      alert("Video URL must be a youtube.com URL")
      return
    }

    // const resp = await executeAddCast({ data: { url: videoUrl } })
  }

  return (
    <Box sx={{ position: "relative" }}>
      <TextField
        disabled={castAddApi.loading}
        label="YouTube URL"
        variant="outlined"
        fullWidth
        value={videoUrl}
        onChange={e => setVideoUrl(e.target.value)}
      />
      <Box
        sx={{
          position: "absolute",
          right: 10,
          top: "50%",
          transform: "translateY(-50%)",
          display: "flex",
        }}
      >
        {!castAddApi.loading ? (
          <Button variant="contained" onClick={handleAdd}>
            Add
          </Button>
        ) : (
          <CircularProgress size="2rem" />
        )}
      </Box>
    </Box>
  )
}
