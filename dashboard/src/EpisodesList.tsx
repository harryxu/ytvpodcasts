import {
  Avatar,
  Card,
  CardContent,
  List,
  ListItem,
  ListItemAvatar,
  ListItemText,
  Pagination,
  Skeleton,
  Typography,
} from "@mui/material"
import { useQuery } from "@tanstack/react-query"
import axios from "axios"
import { useState } from "react"
import type { EpisodesResponse } from "./types"

export default function EpisodesList() {
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
              <ListItem
                key={episode.id}
                alignItems="flex-start"
                sx={{ gap: 2 }}
              >
                <ListItemAvatar>
                  <Avatar
                    alt={episode.title}
                    src={episode.thumbnail}
                    sx={{ width: 64, height: 64 }}
                  />
                </ListItemAvatar>
                <ListItemText
                  primary={episode.title}
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
