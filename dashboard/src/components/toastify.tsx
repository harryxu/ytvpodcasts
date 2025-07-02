import {
  Slide,
  ToastContainer as ToastContainerComponent,
  type ToastContainerProps,
} from "react-toastify"

export default function ToastContainer(props: ToastContainerProps) {
  return (
    <ToastContainerComponent
      limit={3}
      autoClose={3000}
      position="top-right"
      theme="light"
      draggable
      hideProgressBar
      transition={Slide}
      {...props}
    />
  )
}
