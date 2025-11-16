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

import { CancelOutlined, CheckCircleOutlined } from "@mui/icons-material"
import { createFileRoute } from "@tanstack/react-router"

export const Route = createFileRoute("/pg")({
  component: Pg,
})

const taskData = [
  {
    id: "1",
    title: "Task 1",
    description: "Description for Task 1",
    status: "success",
  },
  {
    id: "2",
    title: "Task 2",
    description: "Description for Task 2",
    status: "failed",
  },
  {
    id: "3",
    title: "Task 3",
    description: "Description for Task 3",
    status: "pending",
  },
  {
    id: "4",
    title: "Task 4",
    description: "Description for Task 4",
    status: "processing",
  },
]

function Pg() {
  return (
    <Card variant="outlined">
      <CardContent>
        <List>
          {taskData.map(item => (
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
      </CardContent>
    </Card>
  )
}
