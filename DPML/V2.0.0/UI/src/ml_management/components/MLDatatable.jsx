/**
 * MLDatatable
 * Description : แสดง data table
 * Author : Athruj Poositporn
 */
import React, { Component } from "react";
// import parse from "html-react-parser";
const $ = require("jquery");
$.DataTable = require("datatables.net-bs4");

export class MLDatatable extends Component {
  /**
   * setup_datatable
   * Description : กำหนดให้ตารางกลายเป็น datatable
   * Author : Athruj Poositporn
   */
  setup_datatable = () => {
    $(".tb_ml").DataTable({
      columnDefs: [
        {
          targets: [2, 3],
          orderable: false,
        },
      ],
      pagingType: "full_numbers",
      pageLength: 10,
      bLengthChange: false,
      searching: true,
      language: {
        search: "_INPUT_",
        searchPlaceholder: "Search model",
      },
      autoWidth: false,
      responsive: true,
    });
    // this.setState({ tb_ml });
  };

  /**
   * componentDidMount
   * Description : เรียกใช้งาน setup_datatable() เมื่อหน้าจอถูกติดตั้งครั้งแรก
   * Author : Athruj Poositporn
   */
  componentDidMount() {
    this.setup_datatable();
  }

  /**
   * shouldComponentUpdate
   * Description : ทำลาย datatable เมื่อมีการเปลี่ยนแปลงของ component
   * Author : Athruj Poositporn
   */
  shouldComponentUpdate(nextProps, nextState) {
    // console.log("shouldComponentUpdate");
    if ($.fn.DataTable.isDataTable(".tb_ml")) {
      $(".tb_ml").DataTable().destroy();
    }
    return true;
  }

  /**
   * componentDidUpdate
   * Description : เรียกใช้ setup_datatable เมื่อมีการเปลี่ยนแปลงของ component
   * โดยจะไม่ทำงานเมื่อมีการ render ครั้งแรก
   * Author : Athruj Poositporn
   */
  componentDidUpdate(prevProps, prevState) {
    this.setup_datatable();
  }

  /**
   * open_modal
   * Description :  ฟังก์ชันสำหรับเปิด modal เพื่อแก้ไขข้อมูล
   * Author : Athruj Poositporn
   */
  open_edit_modal = (ml_id) => {
    const { set_ml_id, open_modal } = this.props;
    set_ml_id(ml_id);
    open_modal("edit");
  };

  render() {
    // console.log("render TB");
    const { tb_data, delete_model, switch_model } = this.props;
    return (
      <div className="row mt-4">
        <div className="col-md-12">
          <div className="dataTables_wrapper dt-bootstrap4">
            <table
              className="table table-striped table-hover tb_ml"
              ref={(tb_ml) => (this.tb_ml = tb_ml)}
            >
              <thead>
                <tr className="text-center">
                  <th>#</th>
                  <th>Model name</th>
                  <th>Status</th>
                  <th className="disabled-sorting">Action</th>
                </tr>
              </thead>
              <tbody>
                {tb_data.map((row, index) => (
                  <tr key={index + 1}>
                    <td className="text-center">{index + 1}</td>
                    <td>{row.mlmo_name}</td>
                    <td className="text-center">
                      <div className="testSwitch">
                        <label className="switch m-0">
                          <input
                            type="checkbox"
                            onClick={
                              row.mlmo_status === 1
                                ? console.log()
                                : switch_model
                            }
                            value={row.mlmo_id}
                            disabled={row.mlmo_status === 1 ? true : false}
                            className={row.mlmo_status === 1 ? "check" : ""}
                          />
                          <div
                            className={
                              row.mlmo_status === 1
                                ? "slider round fade_05 no-drop"
                                : "slider round"
                            }
                          />
                        </label>
                      </div>
                    </td>
                    <td className="d-flex justify-content-center">
                      <div>
                        <button
                          className="btn btn-warning btn-sm mr-2"
                          value={row.mlmo_id}
                          onClick={() => {
                            row.mlmo_status !== 1
                              ? this.open_edit_modal(row.mlmo_id)
                              : console.log();
                          }}
                          disabled={row.mlmo_status === 1 ? true : false}
                        >
                          <span className="fas fa-pencil-alt text-white" />
                        </button>
                        <button
                          onClick={() => {
                            row.mlmo_status !== 1
                              ? delete_model(row.mlmo_id)
                              : console.log();
                          }}
                          className="btn btn-danger btn-sm"
                          value={row.mlmo_id}
                          disabled={row.mlmo_status === 1 ? true : false}
                        >
                          <span className="fas fa-trash-alt text-white" />
                        </button>
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    );
  }
}

export default MLDatatable;
