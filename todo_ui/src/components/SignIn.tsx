"use client";
import React, { useState } from "react";

const SignIn = () => {
  const [formData, setFormData] = useState({
    grant_type: "",
    username: "",
    password: "",
    scope: "",
    client_id: "",
    client_secret: "",
  });
  const [isOpen, setIsOpen] = useState(false);

  const handleChange = (e: any) => {
    const { name, value } = e.target;
    setFormData((prevState) => ({
      ...prevState,
      [name]: value,
    }));
  };

  const handleOpen = () => {
    setIsOpen(!isOpen);
  };

  const handleSubmit = async (e: any) => {
    e.preventDefault();
    const encodedData = new URLSearchParams(formData).toString();
    console.log(encodedData);
    // Send encodedData to your API endpoint
    const response = await fetch("http://localhost:8000/auth/token", {
      method: "POST",
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
      },
      body: encodedData,
    });
    if (response.ok) {
      const res = await response.json();
      localStorage.setItem("token", res.access_token);
      alert("Succesfully Logined!");
    } else {
      alert("User Not Found Please Resigter Or Enter valid Information!");
    }
  };

  return (
    <form
      onSubmit={handleSubmit}
      className="w-full flex flex-col gap-4 shadow-lg shadow-gray-200 rounded-lg p-5 border">
      <div
        className="text-2xl font-bold text-center cursor-pointer"
        onClick={() => handleOpen()}>
        Sign In
      </div>
      <div
        className={` transition-all duration-150 ${
          isOpen ? " h-44" : " h-0 overflow-hidden"
        }`}>
        <div className={`flex flex-col gap-3 transition-all duration-150`}>
          <input
            type="text"
            name="username"
            value={formData.username}
            onChange={handleChange}
            className="bg-gray-100 py-3 px-2 rounded-lg"
          />
          <input
            type="password"
            name="password"
            value={formData.password}
            onChange={handleChange}
            className="bg-gray-100 py-3 px-2 rounded-lg"
          />
          <button
            type="submit"
            className="text-xl bg-blue-400 font-bold text-white px-2 py-3 rounded-lg">
            Submit
          </button>
        </div>
      </div>
    </form>
  );
};

export default SignIn;
