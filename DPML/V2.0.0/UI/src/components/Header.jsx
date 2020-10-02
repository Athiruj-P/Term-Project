// Header
// Description : กำหนด UI ในส่วน header 
// Author : Athiruj Poositaporn
import React, { Component } from "react";
import UserAPI from "../services/UserAPI";
import { Cookies } from "react-cookie";
const cookies = new Cookies();
class Header extends Component {
  state = {
    username: cookies.get("username"),
  };

  // handle_logout
  // Description : กำหนดให้ผู้ใช้งานออกจากระบบ และลบค่าต่าง ๆ จาก cookie
  // Author : Athiruj Poositaporn
  handle_logout = () => {
    UserAPI.logout();
    cookies.remove("username");
    cookies.remove("user_role");
    cookies.remove("dpml_access");
    cookies.remove("dpml_refresh");
    window.location.href = "/login";
  };

  render() {
    return (
      <div>
        <nav className="main-header navbar navbar-expand fixed-top bg-gradient-primary">
          {/* Left navbar links */}
          <ul className="navbar-nav">
            <li className="nav-item">
              <a
                className="nav-link"
                data-widget="pushmenu"
                href="/"
                role="button"
              >
                <i className="fas fa-bars text-white" />
              </a>
            </li>
          </ul>

          {/* Right navbar links */}
          <ul className="navbar-nav ml-auto">
            {/* Dropdown Menu */}
            <li className="nav-item dropdown">
              <a className="nav-link" data-toggle="dropdown" href="/">
                <span className="text-white text-md mr-3">
                  {this.state.username}
                </span>
                <i className="fas fa-user-circle text-white text-lg" />
              </a>

              <div className="dropdown-menu dropdown-menu-md dropdown-menu-right">
                <a
                  href="/"
                  onClick={this.handle_logout}
                  className="dropdown-item d-flex align-items-center justify-content-around"
                >
                  <i className="fas fa-sign-out-alt" />
                  Sign out
                </a>
              </div>
            </li>
          </ul>
        </nav>
      </div>
    );
  }
}

export default Header;
