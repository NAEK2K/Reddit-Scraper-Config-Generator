import React from "react";

export default function Feed() {
  return (
    <div className="w-full">
      <p className="text-white text-4xl font-thin pb-20 pt-6 pl-6">Feed</p>
      <div className="flex justify-evenly">
        <div className="">
          <p className="text-white font-thin">Title (Hyperlink)</p>
        </div>
        <div className="">
          <p className="text-white font-thin">Author</p>
        </div>
        <div className="">
          <p className="text-white font-thin">Votes</p>
        </div>
        <div className="">
          <p className="text-white font-thin">Cached Link</p>
        </div>
      </div>

      
    </div>
  );
}
