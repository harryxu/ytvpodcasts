import {
  Avatar,
  Card,
  CardContent,
  List,
  ListItem,
  ListItemAvatar,
  ListItemText,
  Skeleton,
  Typography,
} from "@mui/material"
import useAxios from "axios-hooks"
import type { Episode } from "./types"

export default function EpisodesList() {
  const [episodesApi, refetch] = useAxios({
    url: "/api/episodes",
  })

  return (
    <Card variant="outlined">
      <CardContent>
        <Typography variant="h5">Episodes</Typography>
        {episodesApi.loading && <Skeleton />}
        {episodesApi.data && (
          <List>
            {episodesApi.data.data.map((episode: Episode) => (
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
      </CardContent>
    </Card>
  )
}
