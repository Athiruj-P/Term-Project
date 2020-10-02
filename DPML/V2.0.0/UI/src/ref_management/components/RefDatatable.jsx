/**
 * RefDatatable
 * Description : ส่วนตารางข้อมูลต้นแบบของวัตถุอ้างอิง
 * Author : Athruj Poositporn
 */
import React, { Component } from "react";
import { string } from "prop-types";

const $ = require("jquery");
$.DataTable = require("datatables.net-bs4");

export class RefDatatable extends Component {
  /**
   * setup_datatable
   * Description : กำหนดให้ตารางกลายเป็น datatable
   * Author : Athruj Poositporn
   */
  setup_datatable = () => {
    $(".tb_ref").DataTable({
      columnDefs: [
        {
          targets: [5, 6],
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
    if ($.fn.DataTable.isDataTable(".tb_ref")) {
      $(".tb_ref").DataTable().destroy();
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
  open_edit_modal = (ref_id) => {
    const { set_ref_id, open_modal } = this.props;
    set_ref_id(ref_id);
    open_modal("edit");
  };
  render() {
    const { tb_data, delete_model, switch_model } = this.props;
    return (
      <div className="row mt-4">
        <div className="col-md-12">
          <div className="dataTables_wrapper dt-bootstrap4">
            <table
              className="table table-striped table-hover tb_ref"
              ref={(tb_ref) => (this.tb_ref = tb_ref)}
            >
              <thead>
                <tr className="text-center">
                  <th>#</th>
                  <th>Model name</th>
                  <th>Width</th>
                  <th>Height</th>
                  <th>Unit</th>
                  <th>Status</th>
                  <th className="disabled-sorting">Action</th>
                </tr>
              </thead>
              <tbody>
                {tb_data.map((row, index) => (
                  <tr key={index + 1}>
                    {/* <script>{console.log(index + 1)}</script> */}
                    <td className="text-center">{index + 1}</td>
                    <td>{row.remo_name}</td>
                    <td className="text-center">{row.remo_width}</td>
                    <td className="text-center">{row.remo_height}</td>
                    <td className="text-center">
                      {row.un_name} ({row.un_abb_name})
                    </td>
                    <td className="text-center">
                      <label className="switch m-0">
                        <input
                          type="checkbox"
                          onClick={
                            row.remo_status === 1 ? console.log() : switch_model
                          }
                          value={row.remo_id}
                          disabled={row.remo_status === 1 ? true : false}
                          className={row.remo_status === 1 ? "check" : ""}
                        />
                        <div
                          // className="slider round "
                          className={
                            row.remo_status === 1
                              ? "slider round fade_05 no-drop"
                              : "slider round"
                          }
                        />
                      </label>
                    </td>
                    <td className="d-flex justify-content-center">
                      <div>
                        <button
                          className="btn btn-warning btn-sm mr-2"
                          value={row.remo_id}
                          onClick={() => {
                            row.remo_status !== 1
                              ? this.open_edit_modal(row.remo_id)
                              : console.log();
                          }}
                          disabled={row.remo_status === 1 ? true : false}
                        >
                          <span className="fas fa-pencil-alt text-white" />
                        </button>
                        <button
                          onClick={() => {
                            row.remo_status !== 1
                              ? delete_model(row.remo_id)
                              : console.log();
                          }}
                          className="btn btn-danger btn-sm"
                          value={row.remo_id}
                          disabled={row.remo_status === 1 ? true : false}
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

export default RefDatatable;
