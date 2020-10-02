/**
 * RefManagement
 * Description : หน้าจอการจัดการข้อมูลต้นแบบของวัตถุอ้างอิง
 * Author : Athruj Poositporn
 */
import React, { Component } from "react";
import { Prompt } from "react-router";
import "./RefManagement.css";
import Swal from "sweetalert2";
import AddModal from "./components/AddModal";
import EditModal from "./components/EditModal";
import RefDatatable from "./components/RefDatatable";
import RefManagementAPI from "../services/RefManagementAPI";
import LogAPI from "../services/LogAPI";

const $ = require("jquery");
$.DataTable = require("datatables.net-bs4");
export class RefManagement extends Component {
  state = {
    type: "ref",
    file: null,
    model_name: null,
    model_width: undefined,
    model_height: undefined,
    model_un_id: undefined,
    progress: 0, //css value
    show_progress_bar: "collapse", //CSS class
    remo_id: 0,
    show_add_modal: false,
    show_edit_modal: false,
    is_processing: false,
    tb_data: [],
    units: [],
    abort: false,
  };

  /**
   * handle_edit_model
   * Description : ใช้งานเมื่อต้องการแก้ไขข้อมูลต้นแบบของวัตถุอ้างอิงโมเดลหนึ่ง ๆ
   * Author : Athruj Poositporn
   */
  handle_edit_model = () => {
    let data = {
      type: this.state.type,
      model_id: this.state.remo_id,
      file: this.state.file,
      name: this.state.model_name,
      width: this.state.model_width,
      height: this.state.model_height,
      un_id: this.state.model_un_id,
      username: "Athiruj",
      progress_bar: this.handle_progress_bar,
    };
    RefManagementAPI.check_duplicate_name(data).then((response) => {
      if (!this.state.abort) {
        if (!response.status) {
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
        } else if (!response.data.is_duplicate) {
          if (this.state.file) {
            this.setState({ show_progress_bar: "collapse show" });
          }
          this.setState({ is_processing: true });
          this.close_modal("edit");

          RefManagementAPI.edit_ref_model(data)
            .then((response) => {
              // console.log(response);
              if (!this.state.abort) {
                if (response.status) {
                  let message = {
                    icon: "success",
                    title: "Edited a model data successfully.",
                  };
                  this.show_sweet_alert(message);
                  this.reload_data_table();
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
                      title: response.data.mes
                        ? response.data.mes
                        : response.data,
                    };
                    this.show_sweet_alert(message);
                  }
                }
              }

              setTimeout(() => {
                this.setState({ is_processing: false });
                this.setState({ show_progress_bar: "collapse" });
                this.setState({ progress: 0 });
              }, 1000);
            })
            .then(() => {
              this.setState({
                file: null,
                model_name: "",
                model_width: "",
                model_height: "",
                model_un_id: "",
              });
            });
        } else {
          let message = {
            icon: "error",
            title:
              "This name has already taken, Please enter a unique model name.",
          };
          this.show_sweet_alert(message);
        }
      }
    });
  };

  /**
   * set_remo_id
   * Description : กำหนดค่าให้กับ remo_id เพื่อใช้งานร่วมกับการแก้ไขโมเดลหนึ่ง ๆ
   * Author : Athruj Poositporn
   */
  set_remo_id = (remo_id) => {
    this.setState({ remo_id });
  };

  /**
   * handle_delete_model
   * Description : ใช้งานเมื่อต้องการลบโมเดลหนึ่ง ๆ
   * Author : Athruj Poositporn
   */
  handle_delete_model = (remo_id) => {
    let log_data = {
      username: "Athiruj_admin",
      action: null,
    };
    log_data.action = "Click delete reference model button.";
    LogAPI.add_log(log_data);

    const data = {
      type: this.state.type,
      model_id: remo_id,
      username: "Athiruj",
    };
    // console.log("handle_delete_model : ", ml_id);
    Swal.fire({
      title: "Do you confirm",
      text: "to delete this model ?",
      icon: "warning",
      showCancelButton: true,
      confirmButtonColor: "#d33",
      cancelButtonColor: "",
      confirmButtonText: "Delete",
      reverseButtons: true,
    }).then((result) => {
      if (result.value) {
        RefManagementAPI.delete_ref_model(data).then((response) => {
          if (response.status) {
            Swal.fire("Deleted!", "The model has been deleted.", "success");
            this.reload_data_table();
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
      }
    });
  };

  /**
   * handle_switch_model
   * Description : ใช้งานเมื่อต้องการเปลี่ยนการใช้งานของโมเดล
   * Author : Athruj Poositporn
   */
  handle_switch_model = (switch_ref) => {
    let log_data = {
      username: "Athiruj_admin",
      action: null,
    };
    log_data.action = "Click switch active reference model button.";
    LogAPI.add_log(log_data);

    const data = {
      type: this.state.type,
      model_id: switch_ref.target.value,
      username: "Athiruj",
    };
    // ถ้าข้อมูลมากกว่า 1 และปุ่มนั้น ๆ ไม่ได้ ON
    Swal.fire({
      title: "Do you confirm",
      text: "to activate this model ?",
      icon: "warning",
      showCancelButton: true,
      confirmButtonColor: "#2AB934",
      cancelButtonColor: "",
      confirmButtonText: "Yes",
      reverseButtons: true,
    }).then((result) => {
      if (result.value) {
        RefManagementAPI.change_active_ref_model(data).then((response) => {
          if (response.status) {
            // Swal.fire("Deleted!", "The model has been deleted.", "success");
            let message = {
              icon: "success",
              title: "Change active model successfully.",
            };
            this.show_sweet_alert(message);
            this.reload_data_table();
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
      }
    });
  };

  // handle_upload
  // Description : ฟังก์ชันสำหรับการอัปโหลดไฟล์รูปภาพ
  // Author : Athiruj Poositaporn
  handle_upload = () => {
    let data = {
      type: this.state.type,
      file: this.state.file,
      name: this.state.model_name,
      width: this.state.model_width,
      height: this.state.model_height,
      un_id: this.state.model_un_id,
      username: "Athiruj",
      progress_bar: this.handle_progress_bar,
    };
    RefManagementAPI.check_duplicate_name(data).then((response) => {
      if (!this.state.abort) {
        if (!response.status) {
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
        } else if (!response.data.is_duplicate) {
          this.setState({
            is_processing: true,
            show_progress_bar: "collapse show",
          });
          this.close_modal("add");

          RefManagementAPI.upload_ref_model(data)
            .then((response) => {
              // console.log(response);
              if (!this.state.abort) {
                if (response.status) {
                  let message = {
                    icon: "success",
                    title: "Upload a model data successfully.",
                  };
                  this.show_sweet_alert(message);
                  this.reload_data_table();
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
                      title: response.data.mes
                        ? response.data.mes
                        : response.data,
                    };
                    this.show_sweet_alert(message);
                  }
                }
              }

              setTimeout(() => {
                this.setState({ is_processing: false });
                this.setState({ show_progress_bar: "collapse" });
                this.setState({ progress: 0 });
              }, 1000);
            })
            .then(() => {
              this.setState({ file: null, model_name: "" });
            });
        } else {
          let message = {
            icon: "error",
            title:
              "This name has already taken, Please enter a unique model name.",
          };
          this.show_sweet_alert(message);
        }
      }
    });
  };

  // handle_progress_bar
  // Description : ฟังก์ชันสำหรับการจัดเก็บค่าร้อยละของการอัปโหลดไฟล์
  // Author : Athiruj Poositaporn
  handle_progress_bar = (persentage) => {
    this.setState({ progress: persentage });
  };

  reload_data_table = () => {
    let data = {
      type: this.state.type,
      username: "Athiruj",
    };
    RefManagementAPI.get_all_model(data).then((response) => {
      // console.log(response);
      if (response.data.data) this.setState({ tb_data: response.data.data });
    });
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

  /**
   * close_modal
   * Description :  ฟังก์ชันสำหรับปิด modal
   * Author : Athruj Poositporn
   */
  close_modal = (modal) => {
    let data = {
      username: "Athiruj_admin",
      action: null,
    };
    if (modal === "add") {
      this.setState({ show_add_modal: false });
      data.action = "Close add reference modal.";
    } else if (modal === "edit") {
      this.setState({ show_edit_modal: false });
      data.action = "Close edit reference modal.";
    }
    LogAPI.add_log(data);
  };

  /**
   * open_modal
   * Description :  ฟังก์ชันสำหรับเปิด modal
   * Author : Athruj Poositporn
   */
  open_modal = (modal) => {
    if (this.state.progress == 0) {
      let data = {
        username: "Athiruj_admin",
        action: null,
      };
      if (modal === "add") {
        this.setState({ show_add_modal: true });
        data.action = "Open add reference modal.";
      } else if (modal === "edit") {
        this.setState({ show_edit_modal: true });
        data.action = "Open edit reference modal.";
      }
      LogAPI.add_log(data);
    }
  };

  /**
   * set_model_name
   * Description :  ฟังก์ชันสำหรับเก็บข้อมูลของ model
   * Author : Athruj Poositporn
   */
  set_model_data = (model_data) => {
    const {
      file,
      model_name,
      model_width,
      model_height,
      model_un_id,
    } = model_data;
    this.setState({ file, model_name, model_width, model_height, model_un_id });
  };

  /**
   * componentDidMount
   * Description :  ฟังก์ชันสำหรับกำหนดค่าให้กับ data table ใหม่เมื่อ component ติดตั้งแล้ว
   * Author : Athruj Poositporn
   */
  componentDidMount() {
    // กำหนดค่าเริ่มต้นให้กับตัวแปล
    this.reload_data_table();
    let data = { username: "Athiruj" };
    RefManagementAPI.get_all_unit(data).then((response) => {
      // console.log(response);
      if (response.data.data) this.setState({ units: response.data.data });
    });
  }

  /**
   * componentWillUnmount
   * Description :  ฟังก์ชันสำหรับเรียกใช้เมื่อ component จะถอนการติดตั้ง
   * Author : Athruj Poositporn
   */
  componentWillUnmount = () => {
    this.state.abort = true;
  };

  /**
   * componentDidUpdate
   * Description :  ฟังก์ชันเรียกใช้งานเมื่อมีการโหลดหน้าใหม่ หรือมีข้อมูลเปลี่ยนแปลง
   * Author : Athruj Poositporn
   */
  componentDidUpdate = () => {
    if (this.state.progress !== 0 || this.state.is_processing) {
      window.onbeforeunload = () => true;
    } else {
      window.onbeforeunload = undefined;
    }
  };

  render() {
    return (
      <div className="content-wrapper h-100">
        <div style={{ height: "4rem" }}></div>
        {/* Title */}
        <section className="content-header">
          <div className="container-fluid">
            <div className="row mb-2">
              <div className="col-sm-12">
                <h1>Reference model management</h1>
              </div>
            </div>
          </div>
        </section>
        {/* Title */}

        <section className="content">
          <div className="container-fluid">
            <div className="row">
              <div className="col-md-12 card">
                <div className="card-body">
                  <div className="row">
                    {/* Btn add new model */}
                    <button
                      onClick={() => {
                        this.open_modal("add");
                      }}
                      className="btn btn-primary"
                      data-toggle="modal"
                      data-target="#addModal"
                    >
                      <i className="fas fa-plus text-white mr-3" />
                      Add new model
                    </button>
                    {/* Btn add new model */}
                    {/* Progress bar */}
                    <div
                      className={
                        "ml-3 col-md-6 " + this.state.show_progress_bar
                      }
                    >
                      <div className="mt-3 dflex justify-content-center">
                        <div className="progress">
                          <div
                            className="progress-bar bg-success progress-bar-striped"
                            role="progressbar"
                            style={{
                              width: String(this.state.progress) + "%",
                            }}
                          >
                            Uploaded {this.state.progress} %
                          </div>
                        </div>
                      </div>
                    </div>
                    {/* Progress bar */}
                  </div>

                  {/* Data table */}
                  <RefDatatable
                    tb_data={this.state.tb_data}
                    delete_model={this.handle_delete_model}
                    set_ref_id={this.set_remo_id}
                    switch_model={this.handle_switch_model}
                    open_modal={this.open_modal}
                  />

                  {/* Add modal */}
                  <AddModal
                    showModal={this.state.show_add_modal}
                    close={this.close_modal}
                    set_model_data={this.set_model_data}
                    units={this.state.units}
                    handle_upload={this.handle_upload}
                  />

                  {/* Edit modal */}
                  <EditModal
                    showModal={this.state.show_edit_modal}
                    close={this.close_modal}
                    set_file={this.set_file}
                    units={this.state.units}
                    set_model_data={this.set_model_data}
                    handle_edit_model={this.handle_edit_model}
                    remo_id={this.state.remo_id}
                    tb_data={this.state.tb_data}
                    model_name={this.state.model_name}
                    model_width={this.state.model_width}
                    model_height={this.state.model_height}
                    model_un_id={this.state.model_un_id}
                  />
                </div>
              </div>
            </div>
          </div>
        </section>
      </div>
    );
  }
}

export default RefManagement;
