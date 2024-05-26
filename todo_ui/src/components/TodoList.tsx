"use client";
import React, { useEffect, useState } from "react";
import { RiDeleteBin2Line } from "react-icons/ri";
import { FaPencil } from "react-icons/fa6";
import { FaSquareCheck } from "react-icons/fa6";
import { FaCheck } from "react-icons/fa";

interface Todo {
  is_complete: boolean;
  id?: number | undefined;
  content?: string | undefined;
}

export default function TodoList() {
  const [content, setContent] = useState<Todo[]>([]);
  const [selectedTodoId, setSelectedTodoId] = useState<number | null>(null);
  const [updatedContent, setUpdatedContent] = useState<string>("");
  const [postContent, setPostContent] = useState<string>("");

  useEffect(() => {
    const token = localStorage.getItem("token");
    if (token) {
      fetchTodos(); // Call fetchTodos if token exists
    }
  }, []);

  async function fetchTodos() {
    const res = await fetch("http://localhost:8000/todos", {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        Authorization: "Bearer " + localStorage.getItem("token"),
      },
    });
    if (res.ok) {
      const data = await res.json();
      console.log(data);
      setContent(data);
    } else {
      alert("Check again");
    }
  }

  async function postTodos(content: string) {
    try {
      console.log(content);
      const res = await fetch("http://localhost:8000/todos", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: "Bearer " + localStorage.getItem("token"),
        },
        body: JSON.stringify({ content }), // Directly reference content property
      });
      if (res.ok) {
        const data = await res.json();
        fetchTodos();
      } else {
        throw new Error(`Error adding todo: ${await res.text()}`); // Extract error message
      }
    } catch (error) {
      console.error("Error adding todo:", error);
    }
  }

  async function updateCompletion(id: number, is_complete: boolean) {
    try {
      console.log(id, is_complete);
      const res = await fetch(`http://localhost:8000/todos/${id}`, {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
          Authorization: "Bearer " + localStorage.getItem("token"),
        },
        body: JSON.stringify({ is_complete }), // Destructure directly
      });

      if (res.ok) {
        const updatedTodo = {
          ...content.find((todo: any) => todo.id === id),
          is_complete,
        };
        setContent([...content.filter((todo) => todo.id !== id), updatedTodo]);
      } else {
        throw new Error(`Error updating completion: ${await res.text()}`); // Extract error message
      }
    } catch (error) {
      console.error("Error updating completion:", error);
      // Handle error gracefully (e.g., display error message to user)
    }
  }

  const handleUpdateClick = (id: any) => {
    setSelectedTodoId(id);
    setUpdatedContent(
      content.find((todo: any) => todo.id === id)?.content || "",
    ); // Get content for editing
  };

  async function updateContent(id: number, content: string) {
    try {
      console.log(id, content);
      const res = await fetch(`http://localhost:8000/todos/${id}`, {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
          Authorization: "Bearer " + localStorage.getItem("token"),
        },
        body: JSON.stringify({
          content: content,
        }),
      });

      if (res.ok) {
        const updatedTodo = {
          ...content.find((todo: { id: number }) => todo.id === id),
          content: updatedContent,
        };
        setContent([
          ...content.filter((todo: { id: number }) => todo.id !== id),
          updatedTodo,
        ]);
        setSelectedTodoId(null); // Clear selected todo
        setUpdatedContent(""); // Reset updated content
      } else {
        alert("Check again");
      }
    } catch (error) {
      console.error("Error updating completion:", error);
    }
  }

  async function deleteTodo(id: number) {
    const res = await fetch(`http://localhost:8000/todos/${id}`, {
      method: "DELETE",
      headers: {
        "Content-Type": "application/json",
        Authorization: "Bearer " + localStorage.getItem("token"),
      },
    });
    if (res.ok) {
      setContent(content.filter((todo: any) => todo.id !== id));
    } else {
      alert("Check again");
    }
  }

  const handleUpdateConfirm = (id: number, content: string) => {
    updateContent(id, content);
    setSelectedTodoId(null);
    fetchTodos();
  };

  let counter = 1;

  return (
    <>
      <div className="p-2 bg-blue-500 text-white font-semibold rounded shadow-md shadow-gray-500 flex justify-center items-center">
        Please Generate token First to access the service
      </div>
      <div className="flex flex-col gap-2">
        <div className="w-full flex gap-5 items-center">
          <input
            type="text"
            value={postContent}
            onChange={(e) => setPostContent(e.target.value)}
            className="px-3 py-2 bg-gray-100 my-2 shadow-md w-full outline-none"
          />
          <button
            onClick={() => postTodos(postContent.toString())}
            className="w-32 h-12 bg-blue-500 text-white">
            Add Todo
          </button>
        </div>
        {content?.map((todo: any) => (
          <div className="grid sm:grid-cols-[8%,70%,20%] listbpoint3:grid-cols-[8%,78%,20%] listbpoint2:grid-cols-[8%,80%,20%] listbpoint:grid-cols-[10%,79%,29%] gap-3 shadow-md p-2 justify-between border">
            <div className="flex justify-center">
              <h3>{counter++}</h3>
            </div>
            {selectedTodoId === todo.id ? ( // Conditional rendering for update view
              <>
                <div className="flex justify-between items-center">
                  <input
                    type="text"
                    value={updatedContent}
                    onChange={(e) => setUpdatedContent(e.target.value)}
                    className=" border-b w-full border-gray-500 outline-none"
                  />
                  <button
                    onClick={() => handleUpdateConfirm(todo.id, updatedContent)}
                    className="rounded-lg p-1 ">
                    <FaCheck className="text-green-500" />
                  </button>
                </div>
              </>
            ) : (
              <>
                <div className="flex justify-between">
                  <h3>{todo.content}</h3>
                  <FaPencil
                    onClick={() => handleUpdateClick(todo.id)}
                    className="text-blue-500 w-6 h-6 cursor-pointer"
                    title="Delete"
                  />
                </div>
              </>
            )}
            <div className="flex h-full gap-3 w-fit">
              <div className="">
                <RiDeleteBin2Line
                  onClick={() => deleteTodo(todo.id)}
                  className="text-red-500 w-6 h-6 cursor-pointer"
                  title="Delete"
                />
              </div>
              {todo.is_complete == true ? (
                <FaSquareCheck
                  className="h-6 w-6 text-green-400 rounded-md cursor-pointer"
                  onClick={() => updateCompletion(todo.id, !todo.is_complete)}
                />
              ) : (
                <div
                  className="h-6 w-6 border border-gray-800 rounded-md cursor-pointer"
                  onClick={() =>
                    updateCompletion(todo.id, !todo.is_complete)
                  }></div>
              )}
            </div>
          </div>
        ))}
      </div>
    </>
  );
}

