import React from 'react';
import Button from './Button'

export default function Create() {


    return (
        <div className="h-32 w-64 rounded bg-gray-700">
            <div className="flex justify-center flex-col p-2 px-4">
                <p className="font-thin text-white text-center">Group Name</p>
                <input type="text" className="rounded font-thin mt-2 mb-4" placeholder="Group Name"/>
                <div className=" flex justify-center">
                    <Button
                        label="Submit"
                    />
                </div>
                
            </div>
        </div>
    )
}