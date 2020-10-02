/**
 * MLManagement
 * Description : หน้าจอการจัดการข้อมูลต้นแบบของวัตถุ
 * Author : Athruj Poositporn
 */
import React, { Component } from "react";
import { Prompt } from "react-router";
import "./MLManagement.css";
import Swal from "sweetalert2";
import AddModal from "./components/AddModal";
import EditModal from "./components/EditModal";
import MLDatatable from "./components/MLDatatable";
import MLManagementAPI from "../services/MLManagementAPI";
import LogAPI from "../services/LogAPI";

const $ = require("jquery");
$.DataTable = require("datatables.net-bs4");
export class MLManagement extends Component {
  state = {
    type: "ml",
    // tb_data เก็บข้อมูลของตาราง
    tb_data: [],
    file: null,
    model_name: "",
    progress: 0, //css value
    show_progress_bar: "collapse", //CSS class
    // ml_id เก็บ id ของโมเดล ใช้งานเมื่อต้องการแก้ไขโมเดลหนึ่ง ๆ
    ml_id: 0,
    show_add_modal: false,
    show_edit_modal: false,
    is_processing: false,
    abort: false,
  };

  /**
   * handle_add_model
   * Description : ใช้งานเมื่อต้องการเพิ่มโมเดลเข้าสู่ระบบ
   * Author : Athruj Poositporn
   */
  handle_add_model = () => {
    const fake_data = {
      id: 2,
      ml_name: "Model",
      switch: 1,
    };

    let { tb_data } = this.state;
    tb_data.push(fake_data);
    this.setState({ tb_data });

    // Sweet alert add success
    Swal.mixin({
      toast: true,
      position: "top-end",
      showConfirmButton: false,
      timer: 3000,
    }).fire({
      icon: "success",
      title: "Add new model successfully.",
    });

    window.$("#addModal").modal("hide");
  };

  /**
   * handle_edit_model
   * Description : ใช้งานเมื่อต้องการแก้ไขข้อมูลต้นแบบของวัตถุโมเดลหนึ่ง ๆ
   * Author : Athruj Poositporn
   */
  handle_edit_model = () => {
    let data = {
      type: this.state.type,
      file: this.state.file,
      name: this.state.model_name,
      model_id: this.state.ml_id,
      username: "Athiruj",
      progress_bar: this.handle_progress_bar,
    };
    MLManagementAPI.check_duplicate_name(data).then((response) => {
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

          MLManagementAPI.edit_ml_model(data)
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

  /**
   * set_ml_id
   * Description : กำหนดค่าให้กับ ml_id เพื่อใช้งานร่วมกับการแก้ไขโมเดลหนึ่ง ๆ
   * Author : Athruj Poositporn
   */
  set_ml_id = (ml_id) => {
    // console.log("ml_id: ", ml_id);
    this.setState({ ml_id });
  };

  /**
   * handle_delete_model
   * Description : ใช้งานเมื่อต้องการลบโมเดลหนึ่ง ๆ
   * Author : Athruj Poositporn
   */
  handle_delete_model = (ml_id) => {
    let log_data = {
      username: "Athiruj_admin",
      action: null,
    };
    log_data.action = "Click delete machine learning model button.";

    LogAPI.add_log(log_data);
    const data = {
      type: this.state.type,
      model_id: ml_id,
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
        MLManagementAPI.delete_ml_model(data).then((response) => {
          if (response.status) {
            // let { tb_data } = this.state;
            // tb_data = tb_data.filter((row) => row.id !== ml_id);
            // this.setState({ tb_data });
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
  handle_switch_model = (switch_ml) => {
    let log_data = {
      username: "Athiruj_admin",
      action: null,
    };
    log_data.action = "Click switch active machine learning model button.";
    LogAPI.add_log(log_data);

    const data = {
      type: this.state.type,
      model_id: switch_ml.target.value,
      username: "Athiruj",
    };
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
        MLManagementAPI.change_active_ml_model(data).then((response) => {
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
      username: "Athiruj",
      progress_bar: this.handle_progress_bar,
    };
    MLManagementAPI.check_duplicate_name(data).then((response) => {
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

          MLManagementAPI.upload_ml_model(data)
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

  /**
   * reload_data_table
   * Description :  ฟังก์ชันสำหรับกำหนดค่าให้กับ data table ใหม่
   * Author : Athruj Poositporn
   */
  reload_data_table = () => {
    let data = {
      type: this.state.type,
      username: "Athiruj",
    };
    MLManagementAPI.get_all_model(data).then((response) => {
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
      data.action = "Close add machine learning modal.";
    } else if (modal === "edit") {
      this.setState({ show_edit_modal: false });
      data.action = "Close edit machine learning modal.";
    }
    LogAPI.add_log(data);
  };

   /**
   * open_modal
   * Description :  ฟังก์ชันสำหรับเปิด modal
   * Author : Athruj Poositporn
   */
  open_modal = (modal) => {
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
  };

  /**
   * set_file
   * Description :  ฟังก์ชันสำหรับเก็บไฟล์ model
   * Author : Athruj Poositporn
   */
  set_file = (file) => {
    this.setState({ file });
  };

  /**
   * set_model_name
   * Description :  ฟังก์ชันสำหรับกำหนดชื่อของ model
   * Author : Athruj Poositporn
   */
  set_model_name = (model_name) => {
    this.setState({ model_name });
    // console.log("Name: ", this.state.model_name);
  };

  /**
   * componentDidMount
   * Description :  ฟังก์ชันสำหรับกำหนดค่าให้กับ data table ใหม่เมื่อ component ติดตั้งแล้ว
   * Author : Athruj Poositporn
   */
  componentDidMount() {
    // กำหนดค่าเริ่มต้นให้กับตัวแปร
    this.reload_data_table();
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
        <Prompt
          when={this.state.progress !== 0 || this.state.is_processing}
          message="You have unsaved changes, are you sure you want to leave?"
        />
        <div style={{ height: "4rem" }}></div>
        {/* Title */}
        <section className="content-header">
          <div className="container-fluid">
            <div className="row mb-2">
              <div className="col-sm-12">
                <h1>Machine Learning model management</h1>
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
                  <MLDatatable
                    tb_data={this.state.tb_data}
                    delete_model={this.handle_delete_model}
                    set_ml_id={this.set_ml_id}
                    switch_model={this.handle_switch_model}
                    open_modal={this.open_modal}
                  />

                  {/* Add modal */}
                  <AddModal
                    // add_model={this.handle_add_model}
                    showModal={this.state.show_add_modal}
                    close={this.close_modal}
                    set_file={this.set_file}
                    set_model_name={this.set_model_name}
                    handle_upload={this.handle_upload}
                  />

                  {/* Edit modal */}
                  <EditModal
                    showModal={this.state.show_edit_modal}
                    close={this.close_modal}
                    set_file={this.set_file}
                    set_model_name={this.set_model_name}
                    handle_edit_model={this.handle_edit_model}
                    ml_id={this.state.ml_id}
                    tb_data={this.state.tb_data}
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

export default MLManagement;
