/**
 * ResultPage
 * Description : หน้าจอส่วนการแสดงผลลัพธ์
 * Author : Athruj Poositporn
 */
import React, { Component } from "react";
import ImageModal from "./components/ImageModal";
import LogAPI from "../services/LogAPI";
var conversions = require("conversions");
var convert = require("convert-units");
class ResultPage extends Component {
  state = {
    sub_selected_unit: 0,
    unit: "",
    units: [],
  };
  // scroll_to_top
  // Description : ฟังก์ชันสำหรับการเลื่อนหน้าจอไปด้านบนสุด
  // Author : Athiruj Poositaporn
  scroll_to_top = () => {
    let log_data = {
      action: null,
    };
    log_data.action = `Click "Upload another image" button`;
    LogAPI.add_log(log_data);
    window.scroll({ top: 0, left: 0, behavior: "smooth" });
  };

  // handle_unit
  // Description : ฟังก์ชันสำหรับการจัดเก็บค่าของหน่วยที่ใช้ในการวัดขนาด
  // Author : Athiruj Poositaporn
  handle_unit = (event) => {
    let log_data = {
      action: null,
    };
    const { units } = this.props;
    if (parseInt(event.target.value)) {
      var unit = units.find(
        (item) => item.un_id === parseInt(event.target.value)
      );
      this.setState({
        sub_selected_unit: parseInt(event.target.value),
        unit: unit.un_abb_name,
      });
    }
    try {
      log_data.action = `Change measurement unit to ${unit.un_abb_name}`;
    } catch {
      log_data.action = `Change measurement unit to none.`;
    }
    LogAPI.add_log(log_data);
  };

  // show_image_modal
  // Description : ฟังก์ชันสำหรับการแสดง modal ของภาพผลลัพธ์
  // Author : Athiruj Poositaporn
  show_image_modal = () => {
    window.$("#image3DModal").modal("show");
  };

  // unit_convert
  // Description : ฟังก์ชันสำหรับการเปลี่ยนค่าของขนาดจากหน่วยหนึ่ง เป็นอีกหน่วยหนึ่ง
  // Author : Athiruj Poositaporn
  unit_convert = (dim, unit) => {
    try {
      return (
        String(conversions(dim, unit, this.state.unit).toFixed(4)) +
        " " +
        this.state.unit
      );
    } catch {
      return "0";
    }
  };

  volume_convert = (volume, unit) => {
    try {
      return (
        String(
          convert(volume)
            .from(unit + "3")
            .to(this.state.unit + "3")
            .toFixed(4)
        ) +
        " " +
        "Cubic " +
        this.state.unit
      );
    } catch {
      return "0";
    }
  };

  /**
   * componentWillUnmount
   * Description :  ฟังก์ชันสำหรับเรียกใช้เมื่อ component จะติดตั้ง
   * Author : Athruj Poositporn
   */
  componentWillMount = () => {
    const { selected_unit } = this.props;
    const { units } = this.props;

    const unit = units.find((item) => item.un_id === parseInt(selected_unit));
    this.setState({
      sub_selected_unit: parseInt(selected_unit),
      unit: unit.un_abb_name,
    });
  };

  render() {
    const { units } = this.props;
    const { image_1, image_2, measurement } = this.props.result;
    return (
      <div className="row">
        {/* Result image */}
        <div className="col-md-7">
          <div className="card">
            <div className="card-header">
              <i className="fas fa-images fa-lg mr-2" />
              <span className="text-lg">Result image</span>
            </div>
            <div
              className="card-body text-center d-flex flex-row justify-content-center align-items-center"
              style={{ minHeight: "27rem" }}
              onClick={this.show_image_modal}
            >
              <div className="cell">
                <img
                  id="image_result_1"
                  // className="card-img-bottom h-100 d-inline-block"
                  src={image_1}
                />
              </div>
              <div className="cell">
                <img
                  id="image_result_2"
                  // className="card-img-bottom h-100 d-inline-block"
                  // onClick={this.show_image_modal}
                  src={image_2}
                />
              </div>
            </div>
          </div>
        </div>
        {/* Result image */}

        {/* Result measurement */}
        <div className="col-md-5">
          <div className="card">
            <div className="card-header">
              <i className="fas fa-ruler-combined fa-lg mr-2" />
              <span className="text-lg">Result</span>
            </div>
            <div className="card-body pb-2" style={{ height: "27rem" }}>
              {/* Select unit */}
              <div className="row d-flex justify-content-center align-content-center">
                <div className="col-md-6 text-right m-auto">
                  Select measurement unit :
                </div>
                <div className="col-md-5">
                  <select
                    name="Unit"
                    className="form-control"
                    defaultValue={this.state.sub_selected_unit}
                    onChange={this.handle_unit}
                  >
                    <option value="0" defaultValue>
                      -- Please select unit --
                    </option>
                    {units.map((item) => (
                      <option key={item.un_id} value={item.un_id}>
                        {item.un_name}
                      </option>
                    ))}
                  </select>
                </div>
                <div className="offset-1"></div>
              </div>
              {/* Select unit */}

              {/* Result */}
              <div
                className="jumbotron mt-3 pt-2 pb-2 overflow-auto"
                style={{ height: "60%" }}
              >
                <div className="container">
                  <p>
                    <span className="font-weight-bold">Status :</span>{" "}
                    {measurement.obj_status}
                  </p>
                  <p>
                    <span className="font-weight-bold">Object name :</span>{" "}
                    {measurement.obj_measurement_result.lable}
                  </p>
                  <p>
                    Dimension A :{" "}
                    {this.unit_convert(
                      measurement.obj_measurement_result.dimA,
                      measurement.obj_measurement_result.unit
                    )}
                  </p>
                  <p>
                    Dimension B :{" "}
                    {this.unit_convert(
                      measurement.obj_measurement_result.dimB,
                      measurement.obj_measurement_result.unit
                    )}
                  </p>
                  <p>
                    Dimension C :{" "}
                    {this.unit_convert(
                      measurement.obj_measurement_result.dimC,
                      measurement.obj_measurement_result.unit
                    )}
                  </p>
                  <p>
                    Volume :{" "}
                    {this.volume_convert(
                      measurement.obj_measurement_result.volume,
                      measurement.obj_measurement_result.unit
                    )}
                  </p>
                  <hr />
                </div>
              </div>
              {/* Result */}

              {/* Btn Go to top */}
              <div className="btn btn-info m-auto" onClick={this.scroll_to_top}>
                <i className="fas fa-chevron-circle-up text-white mr-3" />
                Upload another image
              </div>
              {/* Btn Go to top */}
            </div>
          </div>
        </div>
        {/* Result measurement */}
        <ImageModal image={image_1} image_2={image_2} />
      </div>
    );
  }
}

export default ResultPage;
