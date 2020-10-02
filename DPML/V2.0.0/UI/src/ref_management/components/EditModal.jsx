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
    data: {
      file: null,
      model_name: null,
      model_width: undefined,
      model_height: undefined,
      model_un_id: undefined,
    },
    errors: {
      name: "",
      width: "",
      height: "",
      un_id: "",
      file: "",
    },
    validate: {
      name: false,
      width: false,
      height: false,
      un_id: false,
      file: false,
    },
    progress: 0, //css value
    show_progress_bar: "collapse", //CSS class
    tooltip_msg: {
      model_name: `Model name must contain minimum 3 characters and maximum 30 characters. English, Thai, number, a space ( ) and underscore (_) are allow.`,
      model_width: `Enter width of reference object.`,
      model_height: `Enter height of reference object.`,
      model_un_id: `Select measurement unit.`,
      file: `Choose Machine Learning file which has file extension *.weights only.`,
    },
    model_name_rex: /^([\wก-๙]+ )+[\wก-๙]+$|^[\wก-๙]+$/,
    old_model_data: {
      model_name: null,
      model_width: undefined,
      model_height: undefined,
      model_un_id: -1,
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
   * close_modal
   * Description :  ฟังก์ชันสำหรับตรวจสอบข้อมูลจาก form
   * Author : Athruj Poositporn
   */
  handle_change = (event) => {
    let { set_model_data } = this.props;
    const { name, value, files } = event.target;
    let { errors, validate, data, model_name_rex } = this.state;

    switch (name) {
      case "model_name":
        if (value.search(model_name_rex)) {
          errors.name =
            "Model name must be English, Thai, number, a space ( ) and underscore (_) are allow.";
          validate.name = false;
        } else if (value.length < 3 || value.length > 30) {
          errors.name =
            "Model name must contain minimum 3 characters and maximum 30 characters.";
          validate.name = false;
        } else {
          errors.name = "";
          validate.name = true;
          data.model_name = value;
        }
        break;

      case "width":
        if (value <= 0) {
          errors.width = "Width must greater than 0.";
          validate.width = false;
        } else {
          errors.width = "";
          validate.width = true;
          data.model_width = parseInt(value);
        }
        break;

      case "height":
        if (value <= 0) {
          errors.height = "Height must greater than 0.";
          validate.height = false;
        } else {
          errors.height = "";
          validate.height = true;
          data.model_height = parseInt(value);
        }
        break;

      case "unit":
        if (!Number(value)) {
          errors.un_id = "Please select measurement unit.";
          validate.un_id = false;
        } else {
          errors.un_id = "";
          validate.un_id = true;
          data.model_un_id = parseInt(value);
          // this.state.old_model_data.model_un_id = value
          $("#unit").val(value);
        }
        break;

      case "file":
        try {
          const file = files[0];
          const extension = file.name.split(".").pop().toLowerCase();
          if (extension !== "weights") {
            errors.file = "File extension must be *.weights";
            validate.file = false;
          } else {
            errors.file = "";
            validate.file = true;
            data.file = file;
          }
        } catch {
          validate.file = false;
        }
        break;

      default:
        break;
    }
    this.setState({ errors, validate, data });
    set_model_data(data);
  };

  /**
   * close_modal
   * Description :  ฟังก์ชันสำหรับปิด modal
   * Author : Athruj Poositporn
   */
  close_modal = () => {
    const { close } = this.props;
    let { errors, validate, data, old_model_data } = this.state;

    // clear input value
    $("#addModal #model_name").val("");
    $("#addModal #width").val("");
    $("#addModal #height").val("");
    $("#addModal #unit").val(0);
    $("#addModal #file").val("");

    // clear state variable value
    data = {
      file: null,
      model_name: null,
      model_width: undefined,
      model_height: undefined,
      model_un_id: undefined,
    };

    errors = {
      name: "",
      width: "",
      height: "",
      un_id: "",
      file: "",
    };

    validate = {
      name: false,
      width: false,
      height: false,
      un_id: false,
      file: false,
    };

    old_model_data = {
      model_name: null,
      model_width: undefined,
      model_height: undefined,
      model_un_id: -1,
    };

    // set state variable value
    this.setState({ data, errors, validate, old_model_data });
    // console.log("this old: ", old_model_data);
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
    log_data.action = "Click submit on edit reference model modal.";
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
    const { remo_id, tb_data } = this.props;
    const prop_remoid = remo_id;
    const temp = new Promise(function (resolve, reject) {
      tb_data.find(
        ({ remo_id, remo_name, remo_width, remo_height, remo_un_id }) => {
          if (remo_id === prop_remoid) {
            const model_data = {
              model_name: remo_name,
              model_width: remo_width,
              model_height: remo_height,
              model_un_id: remo_un_id,
            };
            $("#unit").val(remo_un_id);
            // console.log('unit: ',remo_un_id)
            resolve(model_data);
          }
        }
      );
    }).then((old_model_data) => {
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
    if (
      prevState.old_model_data === this.state.old_model_data &&
      this.state.old_model_data.model_un_id === -1
    ) {
      this.set_placeholder();
    }
  };
  
  render() {
    const { showModal, units } = this.props;
    const { name, file, un_id, width, height } = this.state.validate;

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
              <label>Model name</label>
              {/* <span className="font-weight-normal">(Optional)</span> */}
              <div className="row">
                <div className="col-10">
                  <input
                    type="text"
                    className="form-control"
                    name="model_name"
                    id="model_name"
                    required
                    maxLength="30"
                    placeholder={this.state.old_model_data.model_name}
                    onChange={(event) => {
                      this.handle_change(event);
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
              {/* Error message */}
              <div className="row">
                <div className="col-md-12">
                  <span className="text-red text-xs">
                    {this.state.errors.name}
                  </span>
                </div>
              </div>
              {/* Error message */}
            </div>
            {/* Model name */}

            {/* Width and Height */}
            <div className="form-group">
              <div className="row">
                {/* Width */}
                <div className="col-md-6">
                  <label>Width</label>
                  {/* <span className="font-weight-normal">(Optional)</span> */}
                  <div className="row">
                    <div className="col-10">
                      <input
                        type="number"
                        className="form-control"
                        name="width"
                        id="width"
                        required
                        placeholder={this.state.old_model_data.model_width}
                        onChange={(event) => {
                          this.handle_change(event);
                        }}
                      />
                    </div>

                    {/* Infomation */}
                    <div className="col-2 d-flex align-items-center">
                      <OverlayTrigger
                        placement="right"
                        overlay={this.render_tooltip(
                          this.state.tooltip_msg.model_width
                        )}
                      >
                        <div className="info-circle font-weight-bold text-light">
                          i
                        </div>
                      </OverlayTrigger>
                    </div>
                    {/* Infomation */}
                  </div>
                </div>
                {/* Width */}

                {/* Height */}
                <div className="col-md-6">
                  <label>Height</label>
                  {/* <span className="font-weight-normal">(Optional)</span> */}
                  <div className="row">
                    <div className="col-10">
                      <input
                        type="number"
                        className="form-control"
                        name="height"
                        id="height"
                        required
                        placeholder={this.state.old_model_data.model_height}
                        onChange={(event) => {
                          this.handle_change(event);
                        }}
                      />
                    </div>

                    {/* Infomation */}
                    <div className="col-2 d-flex align-items-center">
                      <OverlayTrigger
                        placement="right"
                        overlay={this.render_tooltip(
                          this.state.tooltip_msg.model_height
                        )}
                      >
                        <div className="info-circle font-weight-bold text-light">
                          i
                        </div>
                      </OverlayTrigger>
                    </div>
                    {/* Infomation */}
                  </div>
                </div>
                {/* Height */}
              </div>
              {/* Error messages */}
              <div className="row">
                <div className="col-md-6">
                  <span className="text-red text-xs">
                    {this.state.errors.width}
                  </span>
                </div>
                <div className="col-md-6">
                  <span className="text-red text-xs">
                    {this.state.errors.height}
                  </span>
                </div>
              </div>
              {/* Error messages */}
            </div>
            {/* Width and Height */}

            {/* Units */}
            <div className="form-group">
              <label>Unit</label>
              <div className="row">
                <div className="col-10">
                  <select
                    name="unit"
                    className="form-control"
                    id="unit"
                    onChange={(event) => {
                      this.handle_change(event);
                    }}
                    // value={this.state.old_model_data.model_un_id}
                  >
                    <option value="0">-- Please select unit --</option>
                    {units.map((item) => (
                      <option key={item.un_id} value={item.un_id}>
                        {item.un_name}
                      </option>
                    ))}
                  </select>
                </div>
                {/* Infomation */}
                <div className="col-2 d-flex align-items-center">
                  <OverlayTrigger
                    placement="right"
                    overlay={this.render_tooltip(
                      this.state.tooltip_msg.model_un_id
                    )}
                  >
                    <div className="info-circle font-weight-bold text-light">
                      i
                    </div>
                  </OverlayTrigger>
                </div>
                {/* Infomation */}
              </div>
              {/* Error message */}
              <div className="row">
                <div className="col-md-12">
                  <span className="text-red text-xs">
                    {this.state.errors.un_id}
                  </span>
                </div>
              </div>
              {/* Error message */}
            </div>
            {/* Units */}

            {/* Choose file */}
            <div className="form-group">
              <label htmlFor="input_model_file">Choose a model file</label>
              {/* <span className="font-weight-normal">(Optional)</span> */}
              <div className="row">
                <div className="col-md-10">
                  <input
                    // onChange={(event) => this.check_file_extension(event)}
                    onChange={(event) => {
                      this.handle_change(event);
                    }}
                    type="file"
                    className="form-control-file"
                    id="file"
                    name="file"
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
              <div className="row">
                <div className="col-md-12">
                  <span className="text-red text-xs">
                    {this.state.errors.file}
                  </span>
                </div>
              </div>
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
            disabled={name || file || un_id || width || height ? false : true}
          >
            Edit model
          </button>
        </Modal.Footer>
      </Modal>
    );
  }
}

export default EditModal;
