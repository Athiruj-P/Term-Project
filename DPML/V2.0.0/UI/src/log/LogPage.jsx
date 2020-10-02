// LogPage
// Description : กำหนด UI ส่วนของหน้าจอตรวจสอบประวัติการใช้งานระบบ
// Author : Athiruj Poositaporn
import React, { Component } from "react";
import DateRangePicker from "react-bootstrap-daterangepicker";
import moment from "moment";
import Swal from "sweetalert2";
import LogList from "./components/LogList";
import "bootstrap-daterangepicker/daterangepicker.css";
import LogAPI from "../services/LogAPI";
const $ = require("jquery");

export class LogPage extends Component {
  state = {
    startDate: moment().subtract(1, "days"),
    endDate: moment(),
    ranges: {
      Today: [moment(), moment()],
      Yesterday: [moment().subtract(1, "days"), moment().subtract(1, "days")],
      "Last 7 Days": [moment().subtract(6, "days"), moment()],
      "Last 30 Days": [moment().subtract(29, "days"), moment()],
      "This Month": [moment().startOf("month"), moment().endOf("month")],
      "Last Month": [
        moment().subtract(1, "month").startOf("month"),
        moment().subtract(1, "month").endOf("month"),
      ],
    },
    minDate: "",
    maxDate: moment(),
    data: [],
    date: "today",
    type: "all",
    load: false,
    label: "",
  };

  // componentDidMount
  // Description : กำหนดค่าเริ่มต้นของหน้าจอหลักจากติดตั้ง component แล้ว
  // Author : Athiruj Poositaporn
  componentDidMount = () => {
    let { date, type, label } = this.state;
    let start = this.state.startDate.format("YYYY-MM-DD HH:mm:ss");
    let end = this.state.endDate.format("YYYY-MM-DD HH:mm:ss");
    const data = {
      username: "Athiruj_admin",
    };
    label = start + " - " + end;
    if (start === end) {
      label = start;
    }
    LogAPI.get_min_max_date(data).then((response) => {
      // console.log("logpage: ",response);
      if (response.status) {
        let { minDate, maxDate } = response.data.min_max_date;
        this.setState({ minDate });
      } else {
        if (response.data.status === "system_error") {
          let message = {
            icon: "error",
            title: "System error, Please try again later.",
          };
          this.show_sweet_alert(message);
        } else {
          this.setState({ show_result: false });
          let message = {
            icon: "error",
            title: response.data.mes ? response.data.mes : response.data,
          };
          this.show_sweet_alert(message);
        }
      }
    });
    this.setState({ label });
    this.handle_get_log();
  };

  // handle_apply
  // Description : กำหนดค่าให้กับ startDate endDate เมื่อมีการเปลี่ยนแปลงค่าจาก daterange picker
  // Author : Athiruj Poositaporn
  handle_apply = (event, picker) => {
    const { startDate, endDate } = picker;
    let start = startDate.format("YYYY-MM-DD HH:mm:ss");
    let end = endDate.format("YYYY-MM-DD HH:mm:ss");
    const label = start + " - " + end;
    this.setState({
      startDate: picker.startDate,
      endDate: picker.endDate,
      label,
    });

    if (this.state.date === "date_picker") this.handle_get_log();
  };

  // show_sweet_alert
  // Description : ฟังก์ชันสำหรับการแสดงผล Sweet alert ตามข้อความที่ได้รับ
  // Author : Athiruj Poositaporn
  show_sweet_alert = (message) => {
    Swal.mixin({
      toast: true,
      position: "top-end",
      showConfirmButton: false,
      timer: 3000,
    }).fire({
      icon: message.icon,
      title: message.title,
    });
  };

  // handle_get_log
  // Description : เรียกใช้งาน LogAPI.get_log(data) เพิ่อนำค่า log มาแสดงผล
  // Author : Athiruj Poositaporn
  handle_get_log = () => {
    const { type, startDate, endDate, date } = this.state;
    const group = type;
    const start_date = startDate.format("YYYY-MM-DD");
    const start_time = startDate.format("HH:mm:ss");
    const end_date = endDate.format("YYYY-MM-DD");
    const end_time = endDate.format("HH:mm:ss");
    const data = {
      type: date,
      group: group,
      start_date: start_date,
      start_time: start_time,
      end_date: end_date,
      end_time: end_time,
      username: "Athiruj_admin",
    };
    LogAPI.get_log(data)
      .then((response) => {
        if (response.status) {
          let message = {
            icon: "success",
            title: "Get logs successfully.",
          };
          this.show_sweet_alert(message);
          this.setState({ data: response.data.log });
        } else {
          if (response.data.status === "system_error") {
            let message = {
              icon: "error",
              title: "System error, Please try again later.",
            };
            this.show_sweet_alert(message);
          } else {
            this.setState({ show_result: false });
            let message = {
              icon: "error",
              title: response.data.mes ? response.data.mes : response.data,
            };
            this.show_sweet_alert(message);
          }
        }
      })
      .then(() => {});
  };

  // handle_radio
  // Description : กำหนดค่า date และ type ตามการกด radio 
  // Author : Athiruj Poositaporn
  handle_radio = (event) => {
    const { name, value, id } = event.target;
    let data = {
      username: "Athiruj_admin",
      action: null,
    };
    // console.log("name : ", name, "| value : ", value);
    if (name === "setting-date" && id === "date-picker") {
      this.state.date = "date_picker";
      data.action = "Click on date picker radio.";
    } else if (name === "setting-date" && id === "today") {
      this.state.date = "today";
      data.action = "Click on today radio.";
    } else {
      this.state.type = value;
      data.action = "Click on log type.";
    }
    if (data.action) LogAPI.add_log(data);
    this.handle_get_log();
  };

  render() {
    let { label } = this.state;
    let locale = {
      format: "YYYY-MM-DD HH:mm:ss",
      separator: " - ",
      applyLabel: "Apply",
      cancelLabel: "Cancel",
      weekLabel: "W",
      customRangeLabel: "Custom Range",
      daysOfWeek: moment.weekdaysMin(),
      monthNames: moment.monthsShort(),
      firstDay: moment.localeData().firstDayOfWeek(),
    };

    // const test_var = "";
    let minDate = this.state.minDate;
    let maxDate = this.state.maxDate;

    // console.log("[] minDate: ", this.state.minDate);
    // console.log("[] maxDate: ", this.state.maxDate);

    return (
      <div className="content-wrapper h-100">
        <div style={{ height: "4rem" }}></div>
        {/* Title */}
        <section className="content-header">
          <div className="container-fluid">
            <div className="row mb-2">
              <div className="col-sm-12">
                <h1>Log</h1>
              </div>
            </div>
          </div>
        </section>
        {/* Title */}

        {/* Content */}
        <section className="content">
          <div className="container-fluid">
            <div className="card card-primary">
              <div className="card-header">
                <h3 className="card-title">Options</h3>
                <div className="card-tools">
                  <button
                    type="button"
                    className="btn btn-tool"
                    data-card-widget="collapse"
                  >
                    <i className="fas fa-minus"></i>
                  </button>
                </div>
              </div>
              {/* /.card-header */}

              {/* form start */}
              <div className="card-body pb-0">
                <form role="form">
                  <div className="row">
                    {/* Date */}
                    <div className="col-md-6">
                      <div className="form-group">
                        {/* Title */}
                        <p className="font-weight-bold text-lg ">
                          <i className="fas fa-calendar-alt"></i> Date
                        </p>
                        {/* Title */}

                        {/* Content */}
                        <div className="d-flex flex-column">
                          {/* Radio today */}
                          <div className="p-2">
                            <label>
                              <input
                                id="today"
                                type="radio"
                                name="setting-date"
                                className="mr-2"
                                value="today"
                                defaultChecked
                                onClick={this.handle_radio}
                              />
                              Today
                            </label>
                          </div>
                          {/* Radio today */}

                          {/* Radio datetime range picker */}
                          <div className="p-2">
                            <label>
                              <input
                                id="date-picker"
                                type="radio"
                                name="setting-date"
                                className="mr-2"
                                value={label}
                                onClick={this.handle_radio}
                              />
                              Date and Time
                            </label>
                          </div>
                          <div className="p-2 col-10">
                            {this.state.minDate ? (
                              <DateRangePicker
                                onApply={(event, picker) => {
                                  this.handle_apply(event, picker);
                                }}
                                initialSettings={{
                                  opens: "center",
                                  drops: "up",
                                  timePicker: true,
                                  timePicker24Hour: true,
                                  showDropdowns: true,
                                  timePickerSeconds: true,
                                  startDate: this.state.startDate,
                                  endDate: this.state.endDate,
                                  locale: locale,
                                  minDate: minDate,
                                  maxDate: maxDate,
                                }}
                              >
                                <div className="input-group">
                                  <input
                                    type="text"
                                    className="form-control"
                                    value={label}
                                  />
                                  <span className="input-group-btn">
                                    <div className="btn btn-default date-range-toggle">
                                      <i className="fas fa-calendar" />
                                    </div>
                                  </span>
                                </div>
                              </DateRangePicker>
                            ) : (
                              ""
                            )}
                          </div>
                          {/* Radio datetime range picker */}

                          <div className="offset-2"></div>
                        </div>
                        {/* Content */}
                      </div>
                    </div>
                    {/* Date */}

                    {/* Type */}
                    <div className="col-md-6">
                      <div className="form-group">
                        {/* Title */}
                        <p className="font-weight-bold text-lg ">
                          <i className="fas fa-dolly"></i> Type
                        </p>
                        {/* Title */}

                        {/* Content */}
                        <div className="d-flex">
                          {/* Radio all day */}
                          <div className="p-2">
                            <label>
                              <input
                                id="all"
                                type="radio"
                                name="setting-data"
                                className="mr-2"
                                value="all"
                                defaultChecked
                                onClick={this.handle_radio}
                              />
                              All log
                            </label>
                          </div>
                          {/* Radio all day */}

                          {/* Radio user */}
                          <div className="p-2">
                            <label>
                              <input
                                id="user"
                                type="radio"
                                name="setting-data"
                                className="mr-2"
                                value="USER"
                                onClick={this.handle_radio}
                              />
                              User
                            </label>
                          </div>
                          {/* Radio user */}

                          {/* Radio system */}
                          <div className="p-2">
                            <label>
                              <input
                                id="system"
                                type="radio"
                                name="setting-data"
                                className="mr-2"
                                value="SYSTEM"
                                onClick={this.handle_radio}
                              />
                              System
                            </label>
                          </div>
                          {/* Radio system */}
                        </div>
                        {/* Content */}
                      </div>
                    </div>
                    {/* Type */}
                  </div>
                </form>
              </div>
              {/* /.card-body */}
            </div>
            <div className="card card-secondary">
              <div className="card-header">
                <h3 className="card-title">Log list</h3>
              </div>
              {/* /.card-header */}
              <div className="card-body bg-dark-gray">
                <div className="row mb-2 font-weight-bold">
                  legend:
                  <span className="text-secondary ml-2 mr-2">[Debug] </span> ,{" "}
                  <span className="text-info ml-2 mr-2">[INFO] </span>,{" "}
                  <span className="text-warning ml-2 mr-2">[Warning] </span>,{" "}
                  <span className="text-danger ml-2 mr-2">[Error]</span>
                </div>
                <div className="row d-block">
                  <LogList log_data={this.state.data} />
                </div>
              </div>
              {/* /.card-body */}
            </div>
          </div>
        </section>

        {/* Content */}
      </div>
    );
  }
}

export default LogPage;
