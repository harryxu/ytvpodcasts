import { Container, Stack, Tab, Tabs } from "@mui/material"
import {
  createRootRoute,
  Link,
  Outlet,
  useNavigate,
  useRouterState,
} from "@tanstack/react-router"
import { Rss } from "lucide-react"
import { useState } from "react"
import "../App.css"
import CastInput from "../components/CastInput"
import EpisodePlayer from "../components/EpisodePlayer"
import EventStream from "../components/EventStream"
import ToastContainer from "../components/toastify"

export const Route = createRootRoute({
  component: App,
  notFoundComponent: () => {
    return (
      <div>
        <p>The page you are looking for does not exist.</p>
        <Link to="/">Start Over</Link>
      </div>
    )
  },
})

function App() {
  const { location } = useRouterState()

  const [tabValue, setTabValue] = useState(location.pathname)
  const navigate = useNavigate()

  const handleTabChange = (_e: any, value: any) => {
    setTabValue(value)
    navigate({ to: value })
  }

  return (
    <>
      <Container>
        <h1>
          VPodcasts
          <a href="/rss" target="_blank">
            <Rss color="orange" />
          </a>
        </h1>
        <Stack spacing={5} marginBottom={20}>
          <CastInput />
          <Tabs value={tabValue} onChange={handleTabChange}>
            <Tab label="Episodes" value="/" />
            <Tab label="Tasks" value="/tasks" />
          </Tabs>
          <Outlet />
        </Stack>
      </Container>
      <EpisodePlayer />
      <EventStream />
      <ToastContainer />
      {/* <TanStackRouterDevtools /> */}
    </>
  )
}

export default App
