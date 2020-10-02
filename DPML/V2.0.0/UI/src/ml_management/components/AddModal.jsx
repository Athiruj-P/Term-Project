/**
 * AddModal
 * Description : แสดงผล modal สำหรับเพิ่มข้อมูล model
 * Author : Athruj Poositporn
 */
import React, { Component } from "react";
import Swal from "sweetalert2";
import OverlayTrigger from "react-bootstrap/OverlayTrigger";
import Popover from "react-bootstrap/Popover";
import Modal from "react-bootstrap/Modal";
import LogAPI from "../../services/LogAPI";
const $ = require("jquery");

export class AddModal extends Component {
  state = {
    file_extension: "weights",
    file_accept_input: ".weights",
    has_file: false,
    has_model_name: false,
    model_name_rex: /^([\wก-๙]+ )+[\wก-๙]+$|^[\wก-๙]+$/,
    progress: 0, //css value
    show_progress_bar: "collapse", //CSS class
    tooltip_msg: {
      model_name: `Model name must contain minimum 3 characters and maximum 30 characters. English, Thai, number, a space ( ) and underscore (_) are allow.`,
      file: `Choose Machine Learning file which has file extension *.weights only.`,
    },
    err_msg_model_name: "",
    err_msg_file: "",
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
  handle_input_name = (model_name) => {
    const name = model_name.target.value;
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
      const { set_model_name } = this.props;
      this.setState({ err_msg_model_name: "", has_model_name: true });
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
    close("add");
  };

  /**
   * handle_submit
   * Description :  ฟังก์ชันสำหรับเรียกใช้ handle_upload เพื่ออัปโหลด
   * Author : Athruj Poositporn
   */
  handle_submit = () => {
    const { handle_upload } = this.props;
    let log_data = {
      username: "Athiruj_admin",
      action: null,
    };
    log_data.action = "Click submit on add machine learning model modal.";
    LogAPI.add_log(log_data);
    handle_upload();
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
          <Modal.Title>Add new model</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <form>
            {/* Model name */}
            <div className="form-group">
              <label>
                <code>*</code>Model name
              </label>
              <div className="row">
                <div className="col-10">
                  <input
                    type="text"
                    className="form-control"
                    name="model_name"
                    id="model_name"
                    maxlength="30"
                    required
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
                <code>*</code> Choose a model file
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
            onClick={this.handle_submit}
            type="button"
            className="btn btn-primary"
            disabled={
              !this.state.has_file || !this.state.has_model_name ? true : false
            }
          >
            Add new model
          </button>
        </Modal.Footer>
      </Modal>
    );
  }
}

export default AddModal;
