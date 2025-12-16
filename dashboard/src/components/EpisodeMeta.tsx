import {
  IconButton,
  ListItemIcon,
  ListItemText,
  Menu,
  MenuItem,
  Stack,
  Typography,
  useTheme,
} from "@mui/material"
import { useMutation, useQueryClient } from "@tanstack/react-query"
import axios from "axios"
import { Archive, Clock, Ellipsis, Trash } from "lucide-react"
import { useState } from "react"
import { toast } from "react-toastify"
import type { Episode } from "../types"

export default function EpisodeMeta({ episode }: { episode: Episode }) {
  const theme = useTheme()
  const [menuAnchorEl, setMenuAnchorEl] = useState<null | HTMLElement>(null)
  const menuOpen = Boolean(menuAnchorEl)

  const queryClient = useQueryClient()

  const archiveMutation = useMutation({
    mutationFn: async () => {
      await axios.post(`/api/episodes/${episode.id}/archive`)
    },
    onSuccess: () => {
      queryClient.invalidateQueries({
        queryKey: ["episodesList"],
      })

      toast.success("Episode has been archived.")
    },
  })

  const deleteMutation = useMutation({
    mutationFn: async () => {
      await axios.delete(`/api/episodes/${episode.id}`)
    },
    onSuccess: () => {
      queryClient.invalidateQueries({
        queryKey: ["episodesList"],
      })

      toast.success("Episode has been deleted.")
    },
  })

  const archiveEpisode = () => {
    archiveMutation.mutate()
    setMenuAnchorEl(null)
  }

  const deleteEpisode = () => {
    if (
      window.confirm(
        "Are you sure you want to delete this episode? This action cannot be undone."
      )
    ) {
      deleteMutation.mutate()
    }
    setMenuAnchorEl(null)
  }

  const isPending =
    archiveMutation.isPending ||
    deleteMutation.isPending ||
    queryClient.isFetching({ queryKey: ["episodesList"] }) > 0

  return (
    <>
      <Stack
        direction="row"
        alignItems="center"
        justifyContent="center"
        gap={0.5}
      >
        <EpisodeDuration duration={episode.duration} />
        <IconButton
          onClick={event => setMenuAnchorEl(event.currentTarget)}
          loading={isPending}
        >
          <Ellipsis size={15} color={theme.palette.grey[500]} />
        </IconButton>
      </Stack>
      <Menu
        anchorEl={menuAnchorEl}
        open={menuOpen}
        onClose={() => setMenuAnchorEl(null)}
      >
        <MenuItem onClick={archiveEpisode}>
          <ListItemIcon>
            <Archive size={16} />
          </ListItemIcon>
          <ListItemText>Archive</ListItemText>
        </MenuItem>
        <MenuItem onClick={deleteEpisode}>
          <ListItemIcon>
            <Trash size={16} color={theme.palette.error.main} />
          </ListItemIcon>
          <ListItemText>Delete</ListItemText>
        </MenuItem>
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
      <Typography variant="body2" color={theme.palette.grey[500]}>
        {hours > 0 && <>{`${hours.toString().padStart(2, "0")}:`}</>}
        {`${minutes.toString().padStart(2, "0")}:${seconds
          .toString()
          .padStart(2, "0")}`}
      </Typography>
    </Stack>
  )
}
