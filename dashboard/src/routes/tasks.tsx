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
import React, { useEffect } from "react"
import { useDownloadTasksQuery } from "../api"
import { useTaskStore } from "../stores"
import type { DownloadTask } from "../types"

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
              <TaskItem key={item.id} task={item} />
            ))}
          </List>
        </CardContent>
      </Card>
    </Box>
  )
}

const TaskItem = React.memo(({ task }: { task: DownloadTask }) => {
  return (
    <ListItem key={task.id} alignItems="flex-start">
      <ListItemIcon>
        {task.status === "success" && <CircleCheck color="green" />}
        {task.status === "failed" && <CircleX color="red" />}
        {(task.status === "pending" || task.status === "processing") && (
          <CircularProgress
            size={22}
            enableTrackSlot
            variant={task.progress ? "determinate" : "indeterminate"}
            value={task.progress ? task.progress._percent : undefined}
          />
        )}
      </ListItemIcon>
      <ListItemText
        primary={task.title}
        secondary={
          <Typography variant="body2" color="text.secondary">
            {task.description}
          </Typography>
        }
      />
    </ListItem>
  )
})
