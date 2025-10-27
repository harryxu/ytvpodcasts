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
import type { DownloadTaskResponse } from "./types"

import { CancelOutlined, CheckCircleOutlined } from "@mui/icons-material"

const TaskList = () => {
  const tasksQuery = useQuery({
    queryKey: [],
    queryFn: async (): Promise<DownloadTaskResponse> => {
      const res = await axios.get("/api/tasks", {
        params: { page: 1, per_page: 10 },
      })
      return res.data
    },
  })

  return (
    <Card variant="outlined">
      <CardContent>
        {tasksQuery.data && (
          <List>
            {tasksQuery.data.data.map(item => (
              <ListItem key={item.id} alignItems="flex-start">
                <ListItemIcon>
                  {item.status === "success" && (
                    <CheckCircleOutlined color="success" />
                  )}
                  {item.status === "failed" && <CancelOutlined color="error" />}
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

export default TaskList
