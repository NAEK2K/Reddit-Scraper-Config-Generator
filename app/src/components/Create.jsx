// import { useRef } from "react";
import Button from "./Button";
// import PopupContainer from "./PopupContainer";

export default function Create({ setOpen }) {
  return (
    <div className="h-32 w-64 rounded bg-gray-700">
      <div className="flex justify-center flex-col p-2 px-4">
        <div className="grid grid-cols-3">
          <p className="font-thin text-white text-center col-span-2 flex justify-end">Group Name</p>
          <div className="flex justify-end">
            <button
              onClick={() => setOpen(false)} 
              className="rounded-full h-4 w-4 flex items-center justify-center bg-red-900">
          </button>
          </div>
          
        </div>

        <input
          type="text"
          className="rounded font-thin mt-2 mb-4"
          placeholder="Group Name"
        />
        <div className=" flex justify-center">
          <Button
            setOpen={setOpen}  
            label="Submit" />
        </div>
      </div>
    </div>
  );
}
