import React, { Fragment } from "react";
import { Redirect } from "react-router-dom";
import Header from "./components/Header";
import NavBar from "./components/NavBar";
import { Cookies } from "react-cookie";
import UserAPI from "./services/UserAPI";
import LogAPI from "./services/LogAPI";

const cookies = new Cookies();

class ProtectedRoute extends React.Component {
  state = {
    isAuthenticated: null,
  };

  is_authen = () => {
    // cookies.set('userId', 'Pacman', { path: '/' ,maxAge : 10});
    let dpml_access = cookies.get("dpml_access");
    if (dpml_access) this.setState({ isAuthenticated: true });
    else if (cookies.get("dpml_refresh")) {
      const data = {
        refresh_token: cookies.get("dpml_refresh"),
      };
      UserAPI.refresh_token(data).then((response) => {
        if (response.status) {
          cookies.set("dpml_access", response.data.refresh_token, {
            path: "/",
            maxAge: 3600,
          });
          this.setState({ isAuthenticated: true });
        } else {
          this.setState({ isAuthenticated: false });
        }
      });
    } else {
      this.setState({ isAuthenticated: false });
    }
    // console.log(cookies.get("user_role"));
  };

  get_user_role() {
    return cookies.get("user_role");
  }

  check_role = () => {
    const Component = this.props.component;
    const { path } = this.props;
    const role = this.get_user_role();
    let log_data = {
      username: cookies.get("username"),
      action: null,
    };
    log_data.action = "Enter page " + path;
    if (role === "User") {
      if (path === "/upload") {
        LogAPI.add_log(log_data);
        return (
          <React.Fragment>
            <Header />
            <NavBar />
            <Component />
          </React.Fragment>
        );
      } else {
        LogAPI.add_log(log_data);
        return <Redirect to={{ pathname: "/upload" }} />;
      }
    } else {
      LogAPI.add_log(log_data);
      return (
        <React.Fragment>
          <Header />
          <NavBar />
          <Component />
        </React.Fragment>
      );
    }
  };

  componentWillMount = () => {
    this.is_authen();
  };

  render() {
    const Component = this.props.component;
    if (this.state.isAuthenticated !== null) {
      return this.state.isAuthenticated ? (
        this.check_role()
      ) : (
        <Redirect to={{ pathname: "/login" }} />
      );
    } else {
      return <React.Fragment></React.Fragment>;
    }
  }
}

export default ProtectedRoute;
