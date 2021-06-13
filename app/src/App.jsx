import React from "react";

import { BrowserRouter as Router, Switch, Route, Link } from "react-router-dom";

import Navigation from "./components/Navigation";
import Create from "./components/Create";

// import Configs from "./pages/Configs";

export default function App() {
  return (
    <div class="bg-gray-900 h-full flex flex-cols">
      <Router>
        <Navigation />
        <Switch>
          <Route path="/"></Route>

          <Route path="/feed"></Route>
          <Route path="/settings"></Route>
        </Switch>
      </Router>
      <div className="flex justify-center items-center w-full">
        <Create />
      </div>
    </div>
  );
}
