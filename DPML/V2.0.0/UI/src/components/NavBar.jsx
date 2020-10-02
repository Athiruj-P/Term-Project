// NavBar
// Description : กำหนด UI ส่วนของ side navigation bar
// Author : Athiruj Poositaporn
import React, { Component } from "react";
import { NavLink } from "react-router-dom";
import { Cookies } from "react-cookie";
const cookies = new Cookies();
const $ = require("jquery");
class NavBar extends Component {
  state = {
    is_admin: cookies.get("user_role") === "Admin" ? true : false,
  };

  // hide_side_nav
  // Description : ซ่อน side navigation bar
  // Author : Athiruj Poositaporn
  hide_side_nav() {
    if (!$("body").hasClass("sidebar-collapse"))
      $("body").addClass("sidebar-collapse");
    if ($("body").hasClass("sidebar-open"))
      $("body").attr("class", "sidebar-mini sidebar-closed sidebar-collapse");
  }
  render() {
    return (
      <React.Fragment>
        <aside className="position-fixed main-sidebar sidebar-dark-primary elevation-4">
          {/* Brand Logo */}
          <NavLink
            onClick={this.hide_side_nav}
            to="/upload"
            className="brand-link d-flex align-content-center"
          >
            <img
              src="dist/img/dpml_logo_white.png"
              alt="DPML Logo"
              style={{ opacity: ".8" }}
            />
            <span
              className="brand-text font-weight-bold ml-4 pl-2"
              style={{ fontSize: "30px" }}
            >
              DPML
            </span>
          </NavLink>
          {/* Sidebar */}
          <div className="sidebar">
            {/* Sidebar Menu */}
            <nav className="mt-2">
              <ul
                className="nav nav-pills nav-sidebar flex-column"
                data-widget="treeview"
                role="menu"
                data-accordion="true"
              >
                {/* Upload image */}
                <li className="nav-item">
                  <NavLink
                    onClick={this.hide_side_nav}
                    to="/upload"
                    className="nav-link"
                  >
                    <i className="nav-icon fas fa-upload" />
                    <p>Upload an image</p>
                  </NavLink>
                </li>
                {this.state.is_admin ? (
                  <React.Fragment>
                    {/* ML Management */}
                    <li className="nav-item">
                      <NavLink
                        onClick={this.hide_side_nav}
                        to="/ml_management"
                        className="nav-link"
                      >
                        <i className="nav-icon fas fa-cogs" />
                        <p>ML Management</p>
                      </NavLink>
                    </li>

                    {/* Ref Management */}
                    <li className="nav-item">
                      <NavLink
                        onClick={this.hide_side_nav}
                        to="/ref_management"
                        className="nav-link"
                      >
                        <i className="nav-icon fas fa-tag" />
                        <p>Ref Management</p>
                      </NavLink>
                    </li>

                    {/* Log */}
                    <li className="nav-item">
                      <NavLink
                        onClick={this.hide_side_nav}
                        to="/log"
                        className="nav-link"
                      >
                        <i className="nav-icon fas fa-history" />
                        <p>Log</p>
                      </NavLink>
                    </li>
                  </React.Fragment>
                ) : (
                  ""
                )}
              </ul>
            </nav>
            {/* /.sidebar-menu */}
          </div>
          {/* /.sidebar */}
        </aside>
      </React.Fragment>
    );
  }
}

export default NavBar;
