import React, { Component } from "react";
import { Route, BrowserRouter, Switch } from "react-router-dom";
import UploadPage from "./upload/UploadPage";
import LoginPage from "./login/LoginPage";
import MLManagement from "./ml_management/MLManagement";
import RefManagement from "./ref_management/RefManagement";
import LogPage from "./log/LogPage";
import ProtectedRoute from "./ProtectedRoute";
// import { BrowserRouter as Router, Switch, Route, Link } from "react-router-dom";
class App extends Component {
  render() {
    return (
      <BrowserRouter>
        <Switch>
          <Route path="/login" component={LoginPage} />
          <ProtectedRoute path="/upload" component={UploadPage} />
          <ProtectedRoute path="/ml_management" component={MLManagement} />
          <ProtectedRoute path="/ref_management" component={RefManagement} />
          <ProtectedRoute path="/log" component={LogPage} />
          <Route component={LoginPage} />
        </Switch>
      </BrowserRouter>
    );
  }
}

export default App;
