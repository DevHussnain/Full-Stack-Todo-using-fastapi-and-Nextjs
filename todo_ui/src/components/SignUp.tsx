"use client";
import { useState } from "react";

export default function SignUp() {
  const [name, setName] = useState("");
  const [password, setPassword] = useState("");
  const [isOpen, setIsOpen] = useState(false);

  const handleOpen = () => {
    setIsOpen(!isOpen);
  };

  async function handleSubmit() {
    const data = await fetch("http://localhost:8000/auth/", {
      method: "POST",
      body: JSON.stringify({
        username: name,
        password: password,
      }),
      headers: {
        "Content-Type": "application/json",
      },
    });
    if (data.ok) {
      alert("Successfully Registered!");
    } else {
      alert("Not Valid Username Or Password");
      console.log(name);
    }
  }

  return (
    <div className="w-full flex flex-col gap-4 shadow-lg shadow-gray-200 rounded-lg p-5 border">
      <h3
        className="text-2xl font-bold text-center cursor-pointer"
        onClick={() => handleOpen()}>
        Sign Up
      </h3>
      <div
        className={` transition-all duration-150 ${
          isOpen ? " h-44" : " h-0 overflow-hidden"
        }`}>
        <div className={`flex flex-col gap-3 transition-all duration-150`}>
          <input
            type="text"
            name=""
            id="name"
            value={name}
            onChange={(e: any) => setName(e.target.value)}
            className="bg-gray-100 py-3 px-2 rounded-lg"
            required
            placeholder="Name"
          />
          <input
            type="password"
            name=""
            id="password"
            value={password}
            onChange={(e: any) => setPassword(e.target.value)}
            className="bg-gray-100 py-3 px-2 rounded-lg"
            required
            placeholder="Password"
          />
          <button
            className="text-xl bg-blue-400 font-bold text-white px-2 py-3 rounded-lg"
            onClick={handleSubmit}>
            Submit
          </button>{" "}
        </div>
      </div>
    </div>
  );
}
