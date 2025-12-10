import { Box, Stack, Typography, useTheme } from "@mui/material"
import type { Episode } from "../types"
import { Clock } from "lucide-react"

export default function EpisodeMeta({ episode }: { episode: Episode }) {
  return (
    <Box>
      <EpisodeDuration duration={episode.duration} />
    </Box>
  )
}

const EpisodeDuration = ({ duration }: { duration: number }) => {
  const theme = useTheme()

  const hours = Math.floor(duration / 3600)
  const minutes = Math.floor((duration % 3600) / 60)
  const seconds = Math.floor(duration % 60)

  return (
    <Stack direction="row" alignItems="center" gap={0.2} marginBottom={1}>
      <Clock size={10} color={theme.palette.grey[500]} />
      <Typography variant="body2">
        {hours > 0 && (
          <>
            {hours} hr{hours > 1 && "s"}{" "}
          </>
        )}
        <>
          {minutes} min{minutes > 1 && "s"}{" "}
        </>
        {hours < 1 && (
          <>
            {seconds} sec{seconds > 1 && "s"}
          </>
        )}
      </Typography>
    </Stack>
  )
}
