import React from "react";

import { BrowserRouter as Router, Switch, Route } from "react-router-dom";

import Navigation from "./components/Navigation";

import Configs from "./pages/Configs";
import Feed from "./pages/Feed";
import Settings from "./pages/Settings";

export default function App() {

    return (
        <Router>
          <div className="bg-gray-900 h-full flex flex-row">
            <Navigation />
            <Switch>
              <Route exact path="/">
                <Configs />
              </Route>

              <Route exact path="/feed">
                <Feed />
              </Route>

              <Route exact path="/settings">
                <Settings />
              </Route>

            </Switch>
          </div>
        </Router>
)
}
