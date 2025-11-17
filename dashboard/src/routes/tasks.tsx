import {
  Card,
  CardContent,
  CircularProgress,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  Typography,
} from "@mui/material"
import { useQuery } from "@tanstack/react-query"
import axios from "axios"
import { CircleCheck, CircleX } from "lucide-react"
import type { DownloadTaskResponse } from "../types"

import { createFileRoute } from "@tanstack/react-router"

export const Route = createFileRoute("/tasks")({
  component: TaskList,
})

function TaskList() {
  const tasksQuery = useQuery({
    queryKey: ["tasks"],
    queryFn: async (): Promise<DownloadTaskResponse> => {
      const res = await axios.get("/api/tasks", {
        params: { page: 1, per_page: 10 },
      })
      return res.data
    },
  })

  if (tasksQuery.isLoading) return <CircularProgress />

  return (
    <Card variant="outlined">
      <CardContent>
        {tasksQuery.data && (
          <List>
            {tasksQuery.data.data.map(item => (
              <ListItem key={item.id} alignItems="flex-start">
                <ListItemIcon>
                  {item.status === "success" && <CircleCheck color="green" />}
                  {item.status === "failed" && <CircleX color="red" />}
                  {(item.status === "pending" ||
                    item.status === "processing") && (
                    <CircularProgress size={22} enableTrackSlot />
                  )}
                </ListItemIcon>
                <ListItemText
                  primary={item.title}
                  secondary={
                    <Typography variant="body2" color="text.secondary">
                      {item.description}
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
