import React from 'react';
import {
  BrowserRouter as Router,
  Switch,
  Route,
  Link
} from "react-router-dom";

export default function Navigation() {
    return (
        <div className="bg-green-800 h-screen w-1/12 grid grid-rows-3">
            <Link to="/" className="hover:bg-green-700 transition flex items-center justify-center transform">
                        <p className="text-white font-thin"> 
                            Configs
                        </p>
            </Link>
            <Link to="/feed" className="hover:bg-green-700 transition flex items-center justify-center transform">
                        <p className="text-white font-thin"> 
                            Feed
                        </p>
            </Link>
            <Link to="/settings" className="hover:bg-green-700 transition flex items-center justify-center transform">
                        <p className="text-white font-thin"> 
                            Settings
                        </p>
            </Link>
        </div>
    )
}