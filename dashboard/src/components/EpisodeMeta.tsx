import {
  Box,
  IconButton,
  Menu,
  MenuItem,
  Stack,
  Typography,
  useTheme,
} from "@mui/material"
import type { Episode } from "../types"
import { Clock, Ellipsis } from "lucide-react"
import { useState } from "react"

export default function EpisodeMeta({ episode }: { episode: Episode }) {
  const theme = useTheme()
  const [menuAnchorEl, setMenuAnchorEl] = useState<null | HTMLElement>(null)
  const menuOpen = Boolean(menuAnchorEl)
  return (
    <>
      <Stack
        direction="row"
        alignItems="center"
        justifyContent="center"
        gap={0.5}
      >
        <EpisodeDuration duration={episode.duration} />
        <IconButton onClick={event => setMenuAnchorEl(event.currentTarget)}>
          <Ellipsis size={15} color={theme.palette.grey[500]} />
        </IconButton>
      </Stack>
      <Menu
        anchorEl={menuAnchorEl}
        open={menuOpen}
        onClose={() => setMenuAnchorEl(null)}
      >
        <MenuItem>Archive</MenuItem>
        <MenuItem>Delete</MenuItem>
      </Menu>
    </>
  )
}

const EpisodeDuration = ({ duration }: { duration: number }) => {
  const theme = useTheme()

  const hours = Math.floor(duration / 3600)
  const minutes = Math.floor((duration % 3600) / 60)
  const seconds = Math.floor(duration % 60)

  return (
    <Stack direction="row" alignItems="center" gap={0.2}>
      <Clock size={10} color={theme.palette.grey[500]} />
      <Typography variant="body2">
        {hours > 0 && <>{`${hours.toString().padStart(2, "0")}:`}</>}
        {`${minutes.toString().padStart(2, "0")}:${seconds
          .toString()
          .padStart(2, "0")}`}
      </Typography>
    </Stack>
  )
}
