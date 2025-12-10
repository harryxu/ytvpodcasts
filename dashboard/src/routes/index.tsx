import {
  Avatar,
  Box,
  Card,
  CardContent,
  List,
  ListItem,
  ListItemAvatar,
  ListItemText,
  Pagination,
  Skeleton,
  Stack,
  styled,
  Typography,
} from "@mui/material"
import { useQuery } from "@tanstack/react-query"
import { createFileRoute } from "@tanstack/react-router"
import axios from "axios"
import { AudioLines, Play } from "lucide-react"
import { useState } from "react"
import { useAppStore } from "../stores"
import type { Episode, EpisodesResponse } from "../types"
import EpisodeMeta from "../components/EpisodeMeta"

export const Route = createFileRoute("/")({
  component: EpisodesList,
})

const EpisodeAvatar = styled(Avatar)(({ theme }) => ({
  width: 64,
  height: 64,
  "> img": {
    width: "100%",
    height: "100%",
    textAlign: "center",
    objectFit: "cover",
  },
  ".btn-play": {
    position: "absolute",
    width: "100%",
    height: "100%",
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    cursor: "pointer",
    backgroundColor: "#0000003f",
    opacity: 0,
    "&:hover": {
      opacity: 1,
    },
    "&.playing": {
      opacity: 1,
      backgroundColor: "#00000088",
    },
  },
  "@media (hover: none)": {
    ".btn-play": {
      opacity: 1,
    },
  },
}))

function EpisodesList() {
  const [currentPage, setCurrentPage] = useState(1)

  const episodesQuery = useQuery({
    queryKey: ["episodes", currentPage],
    queryFn: async (): Promise<EpisodesResponse> => {
      const res = await axios.get("/api/episodes", {
        params: { page: currentPage, per_page: 10 },
      })
      return res.data
    },
  })

  return (
    <Card variant="outlined">
      <CardContent>
        {episodesQuery.isPending && <Skeleton />}
        {episodesQuery.data && (
          <List>
            {episodesQuery.data.data.map(episode => (
              <EpisodeItem key={episode.id} episode={episode} />
            ))}
          </List>
        )}
        {(episodesQuery.data?.pagination?.total_pages ?? 0) > 1 && (
          <Pagination
            count={episodesQuery.data?.pagination?.total_pages ?? 0}
            page={currentPage}
            onChange={(_, page) => setCurrentPage(page)}
          />
        )}
      </CardContent>
    </Card>
  )
}

const EpisodeItem = ({ episode }: { episode: Episode }) => {
  const appStore = useAppStore()

  const headContent = (
    <Stack direction="row" alignItems="start" gap={0.5}>
      <Typography sx={{ fontSize: "1.2rem" }}>{episode.title}</Typography>
    </Stack>
  )

  return (
    <ListItem alignItems="flex-start" sx={{ gap: 2 }}>
      <ListItemAvatar>
        <EpisodeAvatar alt={episode.title}>
          <img src={episode.thumbnail} />
          {appStore.playingEpisode?.id === episode.id ? (
            <Box
              className="btn-play playing"
              onClick={() => appStore.setPlayingEpisode(undefined)}
            >
              <AudioLines size={20} color="#ffffff" />
            </Box>
          ) : (
            <Box
              className="btn-play"
              onClick={() => appStore.setPlayingEpisode(episode)}
            >
              <Play size={20} color="#ffffff8e" fill="#ffffffb0" />
            </Box>
          )}
        </EpisodeAvatar>
      </ListItemAvatar>
      <ListItemText
        primary={headContent}
        secondary={
          <Typography
            variant="body2"
            color="text.secondary"
            title={episode.description}
            sx={{
              overflow: "hidden",
              textOverflow: "ellipsis",
              display: "-webkit-box",
              WebkitLineClamp: 5,
              WebkitBoxOrient: "vertical",
            }}
          >
            <EpisodeMeta episode={episode} />
            {episode.description}
          </Typography>
        }
      />
    </ListItem>
  )
}
