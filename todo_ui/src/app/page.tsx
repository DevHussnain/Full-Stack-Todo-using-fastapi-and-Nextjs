import SignIn from "@/components/SignIn";
import SignUp from "@/components/SignUp";
import TodoList from "@/components/TodoList";
import { ToastContainer } from "react-toastify";

export default function Home() {
  return (
    <>
      <div className="flex justify-center ">
        <div className="flex flex-col gap-5 sm:w-full lg:w-1/2">
          <SignUp />
          <SignIn />
          <TodoList />
        </div>
        <div className="absolute bottom-0 p-3 bg-red-500 w-screen text-center text-white font-semibold">
          The Token Expires Adter 20 of your Sign In.
        </div>
      </div>
      <ToastContainer />
    </>
  );
}
