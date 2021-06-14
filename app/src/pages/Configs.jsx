import React, { useState } from "react";
// import CircleButton from "../components/CircleButton";
import Create from "../components/Create";

export default function Configs() {
  const [open, setOpen] = useState(false);
  return (
    <div className="w-full">
      <div className="flex justify-evenly">
        <div className="pt-10">
          <p className="text-white text-4xl font-thin ">Groups</p>
        </div>
        <div className="bg-white h-screen w-1 rounded-lg"></div>
        <div className="pt-10">
          <p className="text-white text-4xl font-thin">Scraper</p>
        </div>
      </div>
      <div className="absolute bottom-0 right-0">
        <button
          onClick={() => setOpen(!open)}
          class="rounded-full h-24 w-24 flex items-center justify-center bg-green-800 mr-1 mb-1 transition hover:bg-green-700 text-white font-thin"
        >
          Add
        </button>
      </div>
      {!open && (
        <div className="absolute inset-0 w-screen h-screen">
          <div className="flex h-full justify-center items-center">
            <Create />
          </div>
        </div>
      )}
    </div>
  );
}
