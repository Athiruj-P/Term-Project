/**
 * UploadPage
 * Description : หน้าจออัปโหลดรูปภาพและแสดงผลลัพธ์
 * Author : Athruj Poositporn
 */
import React, { Component } from "react";
import { Prompt } from "react-router";
import "./uploadPage.css";
import ResultPage from "./ResultPage";
import Upload3D from "./Upload3D";
import Swal from "sweetalert2";
import ImageProcessingAPI from "../services/ImageProcessingAPI";
import LogAPI from "../services/LogAPI";
const $ = require("jquery");

class UploadPage extends Component {
  state = {
    // รายการของนามสกุลไฟล์ที่รองรับ
    file_extension: ["bmp", "jpg", "jpe", "png"],
    // รายการของนามสกุลไฟล์ที่รองรับ ใช้กับ <Input>
    file_accept_input: `
    .bmp,.jpg,.jpe,.png
    `,
    file: null,
    units: [],
    result: {},
    selected_unit: 0, //select value
    progress: 0, //css value
    show_progress_bar: "collapse", //CSS class
    show_result: false,
    show_processing: "d-none", //CSS class
    is_processing: false,
    abort: false,
  };

  componentDidUpdate = () => {
    if (this.state.progress !== 0 || this.state.is_processing) {
      window.onbeforeunload = () => true;
    } else {
      window.onbeforeunload = undefined;
    }
  };

  // handle_input_file
  // Description : ฟังก์ชันสำหรับตรวจสอบความถูกต้องของไฟล์รูปภาพ และจัดเก็บไฟล์
  // Author : Athiruj Poositaporn
  handle_input_file = (event) => {
    let log_data = {
      action: null,
    };
    log_data.action = "Choosen image file.";
    LogAPI.add_log(log_data);
    try {
      const file = event.target.files[0];
      const extension = file.name.split(".").pop().toLowerCase();
      if (this.state.file_extension.indexOf(extension) === -1) {
        $("#image_file").val("");
        $("#preview_img").attr("class", "d-none");
        $("#upload_img").attr("class", "");
        this.setState({ file: null });
        const mes = {
          icon: "error",
          title: "Wrong file extension, Please upload an new image.",
        };
        this.show_sweet_alert(mes);
      } else if (file.size > 10485760) {
        $("#image_file").val("");
        $("#preview_img").attr("class", "d-none");
        $("#upload_img").attr("class", "");
        this.setState({ file: null });
        const mes = {
          icon: "error",
          title: "Image file size is more than 10MB.",
        };
        this.show_sweet_alert(mes);
      } else {
        this.setState({ file });
        // window.location.origin + "/dist/img/upload_img.png"
        var reader = new FileReader();
        reader.onload = function (e) {
          $("#preview_img").attr("class", "");
          $("#preview_img").attr("src", e.target.result);
        };
        reader.readAsDataURL(file);
        $("#upload_img").attr("class", "d-none");
      }
    } catch (error) {
      $("#image_file").val("");
      this.setState({ file: null, selected_unit: 0 });
    }
  };

  // handle_unit
  // Description : ฟังก์ชันสำหรับจัดเก็บหน่วยที่ต้องการวัดขนาด
  // Author : Athiruj Poositaporn
  handle_unit = (event) => {
    let log_data = {
      username: "Some user",
      action: null,
    };
    log_data.action = "Selected measurement unit.";
    LogAPI.add_log(log_data);
    this.setState({ selected_unit: event.target.value });
  };

  // handle_processing
  // Description : ฟังก์ชันสำหรับจัดเก็บร้อยละของการอัปโหลดไฟล์
  // Author : Athiruj Poositaporn
  handle_processing = (show_processing) => {
    this.setState({ show_processing });
  };

  // handle_upload
  // Description : ฟังก์ชันสำหรับการอัปโหลดไฟล์รูปภาพ
  // Author : Athiruj Poositaporn
  handle_upload = () => {
    let log_data = {
      username: "Some user",
      action: null,
    };
    log_data.action = "Click upload image button.";
    LogAPI.add_log(log_data);
    this.setState({ is_processing: true });
    this.setState({ show_result: false });
    this.setState({ show_progress_bar: "collapse show" });
    let data = {
      file: this.state.file,
      unit: this.state.selected_unit,
      progress_bar: this.handle_progress_bar,
      processing: this.handle_processing,
    };

    ImageProcessingAPI.upload_image(data)
      .then((response) => {
        this.handle_processing("fade-out");

        // console.log(response);
        if (!this.state.abort) {
          if (response.status) {
            const result = {
              image: "data:image/png;base64," + response.data.img,
              measurement: {
                obj_status: "Object detected",
                obj_arr: response.data.img_data,
              },
            };
            this.setState({ result });
            this.setState({ show_result: true });
            let message = {
              icon: "success",
              title: "Measure object size successfully",
            };
            this.show_sweet_alert(message);
          } else {
            if (response.data.status === "ml_not_found") {
              const result = {
                image: "data:image/png;base64," + response.data.img,
                measurement: {
                  obj_status: "Object not detected",
                  obj_arr: [
                    {
                      lable: "-",
                      dimA: 0,
                      dimB: 0,
                      unit: "mm",
                    },
                  ],
                },
              };
              this.setState({ result });
              this.setState({ show_result: true });
              let message = {
                icon: "error",
                title: "Object not found.",
              };
              this.show_sweet_alert(message);
            } else if (response.data.status === "ref_not_found") {
              const result = {
                image: "data:image/png;base64," + response.data.img,
                measurement: {
                  obj_status: "Reference object not detected",
                  obj_arr: [
                    {
                      lable: "-",
                      dimA: 0,
                      dimB: 0,
                      unit: "mm",
                    },
                  ],
                },
              };
              this.setState({ result });
              this.setState({ show_result: true });
              let message = {
                icon: "error",
                title: "Reference object not found.",
              };
              this.show_sweet_alert(message);
            } else if (response.data.status === "system_error") {
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
        }

        setTimeout(() => {
          if (!this.state.abort) {
            if (
              response.status ||
              response.data.status === "ml_not_found" ||
              response.data.status === "ref_not_found"
            ) {
              $("html, body").animate(
                { scrollTop: $(document).height() },
                1000
              );
            }
          }
          this.setState({ show_processing: "fade-out" });
          this.setState({ is_processing: false });
          this.setState({ show_progress_bar: "collapse" });
          this.setState({ progress: 0 });
        }, 1000);
      })
      .then(() => {
        $("#image_file").val("");
        $("#preview_img").attr("class", "d-none");
        $("#upload_img").attr("class", "");
        this.setState({ file: null, selected_unit: 0 });
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

  // show_and_hide_progress_bar
  // Description : ฟังก์ชันสำหรับการแสดงหรือซ่อนแถบ pregress bar
  // Author : Athiruj Poositaporn
  show_and_hide_progress_bar = (str_class) => {
    this.setState({ show_progress_bar: str_class });
  };

  // handle_progress_bar
  // Description : ฟังก์ชันสำหรับการจัดเก็บค่าร้อยละของการอัปโหลดไฟล์
  // Author : Athiruj Poositaporn
  handle_progress_bar = (persentage) => {
    this.setState({ progress: persentage });
  };

  /**
   * componentDidMount
   * Description :  ฟังก์ชันสำหรับกำหนดค่าเริ่มต้นเมื่อ component ติดตั้งแล้ว
   * Author : Athruj Poositporn
   */
  componentDidMount = () => {
    ImageProcessingAPI.get_all_unit().then((response) => {
      if (response.status) {
        this.setState({ units: response.data });
      } else {
        const units = [
          { un_id: 1, un_name: "Milimeter", um_abb_name: "mm" },
          { un_id: 2, un_name: "Centimeter", um_abb_name: "cm" },
          { un_id: 3, un_name: "Meter", um_abb_name: "m" },
          { un_id: 4, un_name: "Inch", um_abb_name: "in" },
          { un_id: 5, un_name: "Feet", um_abb_name: "ft" },
          { un_id: 6, un_name: "Yard", um_abb_name: "yd" },
        ];
        this.setState({ units });
      }
    });
  };

  /**
   * componentDidMount
   * Description :  ฟังก์ชันเรียกใช้เมื่อ component จะถอนการติดตั้ง
   * Author : Athruj Poositporn
   */
  componentWillUnmount = () => {
    this.state.abort = true;
  };

  render() {
    return (
      <div className="content-wrapper">
        <Prompt
          when={this.state.progress !== 0 || this.state.is_processing}
          message="You have unsaved changes, are you sure you want to leave?"
        />
        <div style={{ height: "4rem" }}></div>

        <div className="col-12">
          <div className="card card-primary card-outline card-outline-tabs">
            <div className="card-header p-0 border-bottom-0">
              <ul className="nav nav-tabs" role="tablist">
                <li className="nav-item">
                  <a
                    className="nav-link"
                    id="measurement-2d-tab"
                    data-toggle="pill"
                    href="#measurement-2d"
                    role="tab"
                    aria-controls="measurement-2d"
                    aria-selected="false"
                  >
                    2D measurement
                  </a>
                </li>
                <li className="nav-item">
                  <a
                    className="nav-link active"
                    id="measurement-3d-tab"
                    data-toggle="pill"
                    href="#measurement-3d"
                    role="tab"
                    aria-controls="measurement-3d"
                    aria-selected="true"
                  >
                    3D measurement
                  </a>
                </li>
              </ul>
            </div>
            <div className="card-body">
              <div className="tab-content">
                <div
                  className="tab-pane fade"
                  id="measurement-2d"
                  role="tabpanel"
                  aria-labelledby="measurement-2d-tab"
                >
                  <section className="content-header">
                    <div className="container-fluid">
                      <div className="row mb-2">
                        <div className="col-sm-12">
                          <h1>Upload an image to measure object size</h1>
                        </div>
                      </div>
                    </div>
                  </section>
                  {/* Upload section */}
                  <form method="post" action="#" id="#">
                    <div className="form-group files color">
                      <img
                        src={
                          window.location.origin + "/dist/img/upload_img.png"
                        }
                        id="upload_img"
                        alt=""
                      />
                      <img id="preview_img" alt="" />
                      <input
                        type="file"
                        name="file"
                        id="image_file"
                        onChange={(event) => {
                          this.handle_input_file(event);
                        }}
                        className="text-center"
                        accept={this.state.file_accept_input}
                        disabled={!this.state.is_processing ? false : true}
                      />
                    </div>
                  </form>

                  {/* Select unit */}
                  <div className="row d-flex justify-content-center align-content-center">
                    <div className="offset-2"></div>
                    <div className="col-md-4 m-auto text-right">
                      Select measurement unit :
                    </div>
                    <div className="col-md-3">
                      <select
                        name="Unit"
                        className={
                          this.state.file !== null && !this.state.is_processing
                            ? "form-control"
                            : "form-control no-drop"
                        }
                        onChange={this.handle_unit}
                        disabled={
                          this.state.file !== null && !this.state.is_processing
                            ? false
                            : true
                        }
                        value={this.state.selected_unit}
                      >
                        <option value="0" defaultValue>
                          -- Please select unit --
                        </option>
                        {this.state.units.map((item) => (
                          <option key={item.un_id} value={item.un_id}>
                            {item.un_name}
                          </option>
                        ))}
                      </select>
                    </div>
                    <div className="offset-3"></div>
                  </div>
                  {/* Select unit */}

                  {/* Progress bar */}
                  <div className={this.state.show_progress_bar}>
                    <div className="row mt-3 dflex justify-content-center">
                      <div className="col-md-6 ">
                        <div className="progress">
                          <div
                            className="progress-bar progress-bar-striped"
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
                  </div>
                  {/* Progress bar */}

                  {/* Precessing gear */}
                  <div className="row dflex justify-content-center mt-3 mb-2">
                    <p className={this.state.show_processing}>
                      Processing
                      <span
                        className={
                          "fas fa-cog fa-lg p-2 loader " +
                          this.state.show_processing
                        }
                      ></span>
                    </p>
                  </div>
                  {/* Precessing gear */}

                  {/* Upload button */}
                  <div className="mt-3 row dflex justify-content-center">
                    <button
                      onClick={this.handle_upload}
                      className="btn col-md-3 btn-primary"
                      disabled={
                        this.state.file !== null &&
                        this.state.selected_unit !== 0 &&
                        !this.state.is_processing
                          ? false
                          : true
                      }
                    >
                      <i className="fas fa-upload text-white mr-3" />
                      <span className="text-lg">Upload</span>
                    </button>
                  </div>
                  {/* Upload button */}

                  {/* How to */}
                  {/* <div className="row">
                  <div className="col-md-12"> */}
                  <div className=" callout callout-info">
                    <h6>How to use</h6>
                    <ol style={{ fontSize: "14px" }}>
                      <li>
                        Drag and drop an image to the box or click
                        <button
                          className="btn btn-outline-secondary btn-sm ml-1 mr-1"
                          disabled
                        >
                          Choose File
                        </button>
                        button.
                        <ul>
                          <li>File extension : *.bmp,*.jpg, *.jpe, *.png</li>
                          <li>File size : Less than or equals to 10 MB</li>
                        </ul>
                      </li>
                      <li>Select measurement unit.</li>
                      <li>Click upload button</li>
                    </ol>
                  </div>
                  {/* </div>
                </div> */}

                  {/* How to */}
                  {/* Upload section */}

                  <hr />
                  {this.state.show_result ? (
                    <ResultPage
                      result={this.state.result}
                      units={this.state.units}
                      selected_unit={this.state.selected_unit}
                    />
                  ) : (
                    ""
                  )}
                </div>
                <div
                  className="tab-pane fade active show"
                  id="measurement-3d"
                  role="tabpanel"
                  aria-labelledby="measurement-3d-tab"
                >
                  <Upload3D />
                </div>
              </div>
            </div>
            {/* /.card */}
          </div>
        </div>

        {/* Content */}
        <section className="content">
          <div className="container-fluid"></div>
        </section>
        {/* Content */}
      </div>
    );
  }
}

export default UploadPage;
