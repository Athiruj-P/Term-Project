import React, { Component } from "react";

const NavBar = ({ totleCounters }) => {
  return (
    <nav className="navbar navbar-light bg-light">
      <a className="navbar-brand">
        NavBar{" "}
        <span className="badge badge-pill badge-secondary">
          {totleCounters}
        </span>
      </a>
    </nav>
  );
};

export default NavBar;
