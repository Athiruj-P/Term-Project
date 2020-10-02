/**
 * EditModal
 * Description :  แสดง modal สำหรับแก้ไขข้อมูลของ model
 * Author : Athruj Poositporn
 */
import React, { Component } from "react";
import OverlayTrigger from "react-bootstrap/OverlayTrigger";
import Popover from "react-bootstrap/Popover";
import Modal from "react-bootstrap/Modal";
import LogAPI from "../../services/LogAPI";
const $ = require("jquery");

export class EditModal extends Component {
  state = {
    file_extension: "weights",
    file_accept_input: ".weights",
    has_file: false,
    has_model_name: false,
    model_name_rex: /^([\wก-๙]+ )+[\wก-๙]+$|^[\wก-๙]+$/,
    progress: 0, //css value
    show_progress_bar: "collapse", //CSS class
    tooltip_msg: {
      model_name: `Model name must contain minimum 3 characters and maximum 30 characters. English Thai number and underscore (_) are allow.`,
      file: `Choose Machine Learning file which has file extension *.weights only.`,
    },
    err_msg_model_name: "",
    err_msg_file: "",
    old_model_data: {
      model_name: "",
    },
  };
  /**
   * render_tooltip
   * Description :  ฟังก์ชันสำหรับกำหนดการแสดงผล tooltip
   * Author : Athruj Poositporn
   */
  render_tooltip = (text) => {
    return (
      <Popover id="popover-basic">
        <Popover.Content>{text}</Popover.Content>
      </Popover>
    );
  };

  /**
   * handle_input_file
   * Description : ฟังก์ชันสำหรับตรวจสอบและเพิ่มไฟล์ของ model
   * Author : Athruj Poositporn
   */
  handle_input_file = (event) => {
    try {
      const file = event.target.files[0];
      const extension = file.name.split(".").pop().toLowerCase();
      if (extension !== "weights") {
        const err_msg_file = "File extension must be *.weights";
        this.setState({ err_msg_file });
        event.target.value = "";
        this.setState({ has_file: false });
      } else {
        const { set_file } = this.props;
        this.setState({ err_msg_file: "", has_file: true });
        set_file(file);
      }
    } catch {
      this.setState({ err_msg_file: "", has_file: false });
      event.target.value = "";
    }
  };

  /**
 * handle_input_name
 * Description : ฟังก์ชันสำหรับตรวจสอบและเพิ่มชื่อของ model
 * Author : Athruj Poositporn
 */
  handle_input_name = (event) => {
    const { set_model_name } = this.props;
    const { model_name } = this.state.old_model_data;
    const name = event.target.value;
    // set_model_name(model_name);
    // console.log("[] model_name: ", model_name);
    // ตรวจสอบชื่อของข้อมูลต้นแบบวัตถุว่าถูกต้องหรือไม่ โดยถ้าถูกต้องจะคือค่า 0 และผิดจะคืนค่า -1
    if (name.search(this.state.model_name_rex)) {
      const err_msg_model_name =
        "Model name must be English, Thai, number, a space ( ) and underscore (_) are allow.";
      this.setState({ err_msg_model_name, has_model_name: false });
    } else if (name.length < 3 || name.length > 30) {
      const err_msg_model_name =
        "Model name must contain minimum 3 characters and maximum 30 characters.";
      this.setState({ err_msg_model_name, has_model_name: false });
    } else {
      this.setState({ err_msg_model_name: "", has_model_name: true });
      if(name)
        set_model_name(name);
    }
  };

  /**
   * close_modal
   * Description :  ฟังก์ชันสำหรับปิด modal
   * Author : Athruj Poositporn
   */
  close_modal = () => {
    const { close } = this.props;
    $("#model_name").val("");
    $("#input_model_file").val("");
    this.setState({
      err_msg_model_name: "",
      err_msg_file: "",
      has_model_name: false,
      has_file: false,
    });
    close("edit");
  };

  /**
   * handle_edit_model
   * Description :  ฟังก์ชันสำหรับเรียกใช้ handle_edit_model เพื่อแก้ไข model
   * Author : Athruj Poositporn
   */
  handle_edit_model = () => {
    const { handle_edit_model } = this.props;
    let log_data = {
      username: "Athiruj_admin",
      action: null,
    };
    log_data.action = "Click submit on edit machine learning model modal.";
    LogAPI.add_log(log_data);
    this.close_modal();
    handle_edit_model();
  };

  /**
   * set_placeholder
   * Description :  ฟังก์ชันสำหรับกำหนด placeholder ให้กับ form
   * Author : Athruj Poositporn
   */
  async set_placeholder() {
    const { ml_id, tb_data } = this.props;
    const temp = new Promise(function (resolve, reject) {
      tb_data.find(({ mlmo_id, mlmo_name }) => {
        // console.log(ml_id);
        if (mlmo_id === ml_id) {
          // console.log(mlmo_id);
          resolve(mlmo_name);
        }
      });
    }).then((name) => {
      const old_model_data = {
        model_name: name,
      };
      this.setState({ old_model_data });
    });
    return await temp;
  }

  /**
   * componentDidUpdate
   * Description :  ฟังก์ชันเรียกใช้งานเมื่อมีการโหลดหน้าใหม่ หรือมีข้อมูลเปลี่ยนแปลง
   * Author : Athruj Poositporn
   */
  componentDidUpdate = (prevProps, prevState) => {
    if (prevState.old_model_data === this.state.old_model_data) {
      this.set_placeholder();
    }
  };

  render() {
    const { showModal } = this.props;
    return (
      <Modal
        show={showModal}
        onHide={() => this.close_modal()}
        className="fade"
        aria-labelledby="contained-modal-title-vcenter"
        centered
      >
        <Modal.Header closeButton>
          <Modal.Title>Edit model</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <form>
            {/* Model name */}
            <div className="form-group">
              <label>
                Model name{" "}
                {/* <span className="font-weight-normal">(Optional)</span> */}
              </label>
              <div className="row">
                <div className="col-10">
                  <input
                    type="text"
                    className="form-control"
                    name="model_name"
                    id="model_name"
                    required
                    maxlength="30"
                    placeholder={this.state.old_model_data.model_name}
                    onChange={(event) => {
                      this.handle_input_name(event);
                    }}
                  />
                </div>

                {/* Infomation */}
                <div className="col-2 d-flex align-items-center">
                  <OverlayTrigger
                    placement="right"
                    overlay={this.render_tooltip(
                      this.state.tooltip_msg.model_name
                    )}
                  >
                    <div className="info-circle font-weight-bold text-light">
                      i
                    </div>
                  </OverlayTrigger>
                </div>
                {/* Infomation */}
              </div>
              <span className="text-red text-xs">
                {this.state.err_msg_model_name}
              </span>
            </div>
            {/* Model name */}

            {/* Choose file */}
            <div className="form-group">
              <label htmlFor="input_model_file">
                Choose a model file{" "}
                {/* <span className="font-weight-normal">(Optional)</span> */}
              </label>
              <div className="row">
                <div className="col-md-10">
                  <input
                    onChange={(event) => this.handle_input_file(event)}
                    type="file"
                    className="form-control-file"
                    id="input_model_file"
                    accept=".weights"
                    required
                  />
                </div>
                {/* Infomation */}
                <div className="col-2 d-flex align-items-center">
                  <OverlayTrigger
                    placement="right"
                    overlay={this.render_tooltip(this.state.tooltip_msg.file)}
                  >
                    <div className="info-circle font-weight-bold text-light">
                      i
                    </div>
                  </OverlayTrigger>
                </div>
                {/* Infomation */}
              </div>
              <span className="text-red text-xs">
                {this.state.err_msg_file}
              </span>
            </div>

            {/* Choose file */}
          </form>
        </Modal.Body>
        <Modal.Footer className="d-flex justify-content-between">
          <button
            type="button"
            className="btn btn-secondary"
            onClick={() => this.close_modal()}
          >
            Close
          </button>
          <button
            onClick={() => {
              this.handle_edit_model();
            }}
            type="button"
            className="btn btn-warning"
            disabled={
              this.state.has_file || this.state.has_model_name ? false : true
            }
          >
            Edit model
          </button>
        </Modal.Footer>
      </Modal>
    );

    // return (
    //   <div className="modal fade" id="editModal" tabIndex={-1} role="dialog">
    //     <div className="modal-dialog modal-dialog-centered" role="document">
    //       <div className="modal-content">
    //         <div className="modal-header">
    //           <h5 className="modal-title" id="title">
    //             Edit model
    //           </h5>
    //           <button
    //             type="button"
    //             className="close"
    //             data-dismiss="modal"
    //             aria-label="Close"
    //           >
    //             <span aria-hidden="true">×</span>
    //           </button>
    //         </div>
    //         <div className="modal-body">
    //           <form>
    //             {/* Model name */}
    //             <div className="form-group">
    //               <label>Model name</label>
    //               <div className="row">
    //                 <div className="col-10">
    //                   <input
    //                     type="text"
    //                     className="form-control"
    //                     name="model_name"
    //                     id="model_name"
    //                     required
    //                     placeholder="Old model name"
    //                   />
    //                 </div>
    //                 <div className="col-2 d-flex align-items-center">
    //                   <OverlayTrigger
    //                     placement="right"
    //                     overlay={this.render_tooltip(
    //                       this.state.tooltip_msg.model_name
    //                     )}
    //                   >
    //                     <div className="info-circle font-weight-bold text-light">
    //                       i
    //                     </div>
    //                   </OverlayTrigger>
    //                 </div>
    //               </div>
    //             </div>
    //             {/* Model name */}

    //             {/* Choose file */}
    //             <div className="form-group">
    //               <label htmlFor="input_model_file">Choose a model file</label>
    //               <div className="row">
    //                 <div className="col-md-10">
    //                   <input
    //                     onChange={(event) => this.check_file_extension(event)}
    //                     type="file"
    //                     className="form-control-file"
    //                     id="input_model_file"
    //                     accept=".weights"
    //                   />
    //                 </div>
    //                 {/* Infomation */}
    //                 <div className="col-2 d-flex align-items-center">
    //                   <OverlayTrigger
    //                     placement="right"
    //                     overlay={this.render_tooltip(
    //                       this.state.tooltip_msg.file
    //                     )}
    //                   >
    //                     <div className="info-circle font-weight-bold text-light">
    //                       i
    //                     </div>
    //                   </OverlayTrigger>
    //                 </div>
    //                 {/* Infomation */}
    //               </div>
    //             </div>

    //             {/* Choose file */}
    //           </form>
    //         </div>
    //         <div className="modal-footer d-flex justify-content-between">
    //           <button
    //             type="button"
    //             className="btn btn-secondary"
    //             data-dismiss="modal"
    //           >
    //             Close
    //           </button>
    //           <button
    //             onClick={edit_model}
    //             type="button"
    //             className="btn btn-warning"
    //           >
    //             Edit model
    //           </button>
    //         </div>
    //       </div>
    //     </div>
    //   </div>
    // );
  }
}

export default EditModal;
