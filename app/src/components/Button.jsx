import React from 'react';

export default function Button( { label } ) {
    return (
        <div className="py-1 px-2 bg-green-500 rounded flex justify-center items-center">
            <p className="text-white font-thin">{label}</p>
        </div>
    )
}