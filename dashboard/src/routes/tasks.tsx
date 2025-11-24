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
import { CircleCheck, CircleX } from "lucide-react"

import { createFileRoute } from "@tanstack/react-router"
import { useDownloadTasksQuery } from "../api"
import { useTaskStore } from "../stores"
import { useEffect } from "react"

export const Route = createFileRoute("/tasks")({
  component: TaskList,
})

function TaskList() {
  const tasksQuery = useDownloadTasksQuery(false)
  const taskStore = useTaskStore()
  const setAllowAutoUpdate = taskStore.setAllowAutoUpdate

  useEffect(() => {
    setAllowAutoUpdate(false)
    return () => {
      setAllowAutoUpdate(true)
    }
  }, [setAllowAutoUpdate])

  if (tasksQuery.isLoading) return <CircularProgress />

  return (
    <Card variant="outlined">
      <CardContent>
        <List>
          {taskStore.tasks.map(item => (
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
      </CardContent>
    </Card>
  )
}
