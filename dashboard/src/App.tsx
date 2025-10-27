import { Container, Stack, Tab } from "@mui/material"
import { TabPanel, TabContext, TabList } from "@mui/lab"
import CastInput from "./CastInput"
import EpisodesList from "./EpisodesList"
import ToastContainer from "./components/toastify"
import "./App.css"
import { QueryClient, QueryClientProvider } from "@tanstack/react-query"
import { useState } from "react"
import TaskList from "./TaskList"

const queryClient = new QueryClient()

function App() {
  const [tabValue, setTabValue] = useState("1")

  return (
    <QueryClientProvider client={queryClient}>
      <Container>
        <h1>VPodcasts</h1>
        <Stack spacing={5}>
          <CastInput />
          <TabContext value={tabValue}>
            <TabList onChange={(_e, newValue) => setTabValue(newValue)}>
              <Tab label="Episodes" value="1" />
              <Tab label="Tasks" value="2" />
            </TabList>
            <TabPanel value="1" keepMounted>
              <EpisodesList />
            </TabPanel>
            <TabPanel value="2" keepMounted>
              <TaskList />
            </TabPanel>
          </TabContext>
        </Stack>
      </Container>
      <ToastContainer />
    </QueryClientProvider>
  )
}

export default App
