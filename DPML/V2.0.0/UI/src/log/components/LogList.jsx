// LogList
// Description : กำหนดการแสดงผลของแต่ละบรรทัดของ log
// Author : Athiruj Poositaporn
import React, { Component } from "react";
import "../LogPage.css";

export class LogList extends Component {
  // text_color
  // Description : กำหนดสีของ log ตามประเภท
  // Author : Athiruj Poositaporn
  text_color = (text) => {
    if (text.substr(0, 40).search("INFO") !== -1) {
      return " text-info";
    } else if (text.substr(0, 40).search("WARNING") !== -1) {
      return " text-warning";
    } else if (text.substr(0, 40).search("DEBUG") !== -1) {
      return " text-secondary";
    } else if (text.substr(0, 40).search("ERROR") !== -1) {
      return " text-danger";
    }
  };
  render() {
    const { log_data } = this.props;
    // console.log("log_data.length: ", log_data.length);
    return (
      <ul className="list-group">
        {log_data.length > 0 ? (
          log_data.map((log, index) => (
            <li
              key={index}
              className={
                (index + 1) % 2 === 0
                  ? "list-group-item p-1 text-sm"
                  : "list-group-item p-1 text-sm bg-light"
              }
            >
              <span className={
                this.text_color(log)
              }>{log}</span>
              
            </li>
          ))
        ) : (
          <li className="text-center">No data.</li>
        )}
      </ul>
    );
  }
}

export default LogList;
