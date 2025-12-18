import { Box, Button, CircularProgress, TextField } from "@mui/material"
import { useMutation } from "@tanstack/react-query"
import axios from "axios"
import { useState } from "react"
import { toast } from "react-toastify"
import { useDownloadTasksQuery } from "../api"
import { isValidUrl } from "../utils"

export default function CastInput() {
  const [videoUrl, setVideoUrl] = useState("")

  const createCastMutation = useMutation({
    mutationFn: async (url: string) => {
      return axios.post("/api/add", { url })
    },
  })

  const taskQuery = useDownloadTasksQuery(false)

  const handleAdd = async () => {
    if (!isValidUrl(videoUrl)) {
      toast.error("Video URL must be a youtube.com URL", {
        position: "top-center",
        toastId: "error",
      })
      return
    }

    const resp = await createCastMutation.mutateAsync(videoUrl)
    if (resp.status === 200) {
      setVideoUrl("")
      toast.success("Video download task added.")
      taskQuery.refetch()
    }
  }

  return (
    <Box sx={{ position: "relative" }}>
      <TextField
        disabled={createCastMutation.isPending}
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
        {!createCastMutation.isPending ? (
          <Button
            variant="contained"
            onClick={handleAdd}
            disabled={videoUrl.trim() === ""}
          >
            Add
          </Button>
        ) : (
          <CircularProgress size="2rem" />
        )}
      </Box>
    </Box>
  )
}
