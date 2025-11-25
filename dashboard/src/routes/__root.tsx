import { Container, Stack, Tab, Tabs } from "@mui/material"
import {
  createRootRoute,
  Link,
  Outlet,
  useNavigate,
  useRouterState,
} from "@tanstack/react-router"
import { TanStackRouterDevtools } from "@tanstack/react-router-devtools"
import { useState } from "react"
import CastInput from "../CastInput"
import ToastContainer from "../components/toastify"
import "../App.css"
import TaskUpdater from "../components/TaskUpdater"

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
        <h1>VPodcasts</h1>
        <Stack spacing={5}>
          <CastInput />
          <Tabs value={tabValue} onChange={handleTabChange}>
            <Tab label="Episodes" value="/" />
            <Tab label="Tasks" value="/tasks" />
          </Tabs>
          <Outlet />
        </Stack>
      </Container>
      <TaskUpdater />
      <ToastContainer />
      <TanStackRouterDevtools />
    </>
  )
}

export default App
