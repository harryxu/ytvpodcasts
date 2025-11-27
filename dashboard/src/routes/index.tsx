import {
  Avatar,
  Card,
  CardContent,
  colors,
  IconButton,
  List,
  ListItem,
  ListItemAvatar,
  ListItemText,
  Pagination,
  Skeleton,
  Stack,
  Typography,
} from "@mui/material"
import { useQuery } from "@tanstack/react-query"
import axios from "axios"
import { useState } from "react"
import type { Episode, EpisodesResponse } from "../types"
import { createFileRoute } from "@tanstack/react-router"
import { Play, PlayCircle } from "lucide-react"

export const Route = createFileRoute("/")({
  component: EpisodesList,
})

function EpisodesList() {
  const [currentPage, setCurrentPage] = useState(1)

  const episodesQuery = useQuery({
    queryKey: ["episodes", currentPage],
    queryFn: async (): Promise<EpisodesResponse> => {
      const res = await axios.get("/api/episodes", {
        params: { page: currentPage, per_page: 5 },
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
        <Pagination
          count={episodesQuery.data?.pagination?.total_pages ?? 0}
          page={currentPage}
          onChange={(_, page) => setCurrentPage(page)}
        />
      </CardContent>
    </Card>
  )
}

const EpisodeItem = ({ episode }: { episode: Episode }) => {
  const headContent = (
    <Stack direction="row" alignItems="center" gap={0.5}>
      <PlayCircle size={15} color={colors.grey[500]} />
      <Typography sx={{ fontSize: "1.2rem" }}>{episode.title}</Typography>
    </Stack>
  )

  return (
    <ListItem alignItems="flex-start" sx={{ gap: 2 }}>
      <ListItemAvatar>
        <Avatar
          alt={episode.title}
          src={episode.thumbnail}
          sx={{ width: 64, height: 64 }}
        />
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
            {episode.description}
          </Typography>
        }
      />
    </ListItem>
  )
}
