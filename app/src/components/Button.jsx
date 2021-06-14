import React from 'react';

export default function Button( { label, setOpen } ) {
    return (
        <button
            onClick={() => setOpen(false)} 
            className="py-1 px-2 bg-green-500 rounded flex justify-center items-center">
            <p className="text-white font-thin">{label}</p>
        </button>
    )
}