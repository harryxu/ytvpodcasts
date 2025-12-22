import {
  Box,
  Card,
  CardContent,
  CircularProgress,
  IconButton,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  Stack,
  Typography,
} from "@mui/material"
import { CircleCheck, CircleX, RefreshCcw } from "lucide-react"

import { createFileRoute } from "@tanstack/react-router"
import { useEffect } from "react"
import { useDownloadTasksQuery } from "../api"
import { useTaskStore } from "../stores"

export const Route = createFileRoute("/tasks")({
  component: TaskList,
})

function TaskList() {
  const tasksQuery = useDownloadTasksQuery()
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
    <Box sx={{ position: "relative" }}>
      <Stack
        alignItems="flex-end"
        sx={{ position: "absolute", top: -38, right: 0 }}
      >
        <IconButton
          onClick={() => tasksQuery.refetch()}
          disabled={tasksQuery.isRefetching}
        >
          <RefreshCcw size={20} />
        </IconButton>
      </Stack>
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
    </Box>
  )
}
