/**
 * ImageProcessingAPI
 * Description : Service เรียกใช้ API ของ image_processing_api
 * Author : Athruj Poositporn
 */
import axios from "axios";
import UserAPI from "./UserAPI";
import { dpml_config } from "../config";
import { Cookies } from "react-cookie";
const cookies = new Cookies();

export default {
  // upload_image
  // Description : ฟังก์ชันสำหรับอัปโหลดรูปภาพ และรับค่าจากการวัดขนาดวัตถุ
  // Author : Athiruj Poositaporn
  async upload_image(data) {
    return await UserAPI.is_authen().then(async (res_authen) => {
      if (res_authen) {
        let from_data = new FormData();
        from_data.append("file", data.file);
        from_data.append("unit", data.unit);

        // ###################################################
        // กำหนดค่าเพื่อใช้ในการตรวจสอบสถานะความถูกต้องของข้อมูลที่ได้รับ
        // ###################################################
        let response = {
          status: null,
          data: null,
        };
        // ###################################################

        // ################################
        // กำหนดค่าเพื่อใช้ในการทำ Progress bar
        // ################################
        let dpml_access = cookies.get("dpml_access");
        let config = {
          method: "put",
          url: dpml_config.img_upload_image_url,
          headers: {
            Authorization: `Bearer ${dpml_access}`,
            "Content-Type": "application/json",
          },
          data: from_data,
          onUploadProgress: function (progressEvent) {
            var percentCompleted = Math.round(
              (progressEvent.loaded * 100) / progressEvent.total
            );
            data.processing(percentCompleted === 100 ? "fade-in" : "d-none");
            data.progress_bar(percentCompleted);
          },
        };
        // ################################

        // ########################################
        // เรียกใช้ API สำหรับอัปโหลดรูปภาพและวัดขนาดวัตถุ
        // ########################################
        let recived_data = new Promise((resolve, reject) => {
          axios(config)
            .then((res) => {
              // console.log(res.data);
              resolve(res);
            })
            .catch((err) => {
              response.status = false;
              try {
                // console.log("err", err.response.data);
                response.data = err.response.data;
              } catch (error) {
                response.data = "Server not response.";
              }
              resolve(response);
            });
        });
        // ###################################################
        return await recived_data;
      }
    });
  },
  // upload_3d_image
  // Description : ฟังก์ชันสำหรับอัปโหลดรูปภาพ 2 มุมมอง และรับค่าจากการวัดขนาดวัตถุและ
  // Author : Athiruj Poositaporn
  async upload_3d_image(data) {
    return await UserAPI.is_authen().then(async (res_authen) => {
      if (res_authen) {
        let from_data = new FormData();
        from_data.append("img1", data.file[0]);
        from_data.append("img2", data.file[1]);
        from_data.append("unit", data.unit);        

        // ###################################################
        // กำหนดค่าเพื่อใช้ในการตรวจสอบสถานะความถูกต้องของข้อมูลที่ได้รับ
        // ###################################################
        let response = {
          status: null,
          data: null,
        };
        // ###################################################

        // ################################
        // กำหนดค่าเพื่อใช้ในการทำ Progress bar
        // ################################
        let dpml_access = cookies.get("dpml_access");
        let config = {
          method: "put",
          url: dpml_config.img_upload_3d_image_url,
          headers: {
            Authorization: `Bearer ${dpml_access}`,
            "Content-Type": "application/json",
          },
          data: from_data,
          onUploadProgress: function (progressEvent) {
            var percentCompleted = Math.round(
              (progressEvent.loaded * 100) / progressEvent.total
            );
            data.processing(percentCompleted === 100 ? "fade-in" : "d-none");
            data.progress_bar(percentCompleted);
          },
        };
        // ################################

        // ########################################
        // เรียกใช้ API สำหรับอัปโหลดรูปภาพและวัดขนาดวัตถุ
        // ########################################
        let recived_data = new Promise((resolve, reject) => {
          axios(config)
            .then((res) => {
              // console.log(res.data);
              resolve(res);
            })
            .catch((err) => {
              response.status = false;
              try {
                // console.log("err", err.response.data);
                response.data = err.response.data;
              } catch (error) {
                response.data = "Server not response.";
              }
              resolve(response);
            });
        });
        // ###################################################
        return await recived_data;
      }
    });
  },

  // get_all_unit
  // Description : ฟังก์ชันสำหรับดึงข้อมูลของหน่วยวัดขนาดทั้งหมด
  // Author : Athiruj Poositaporn
  async get_all_unit() {
    // console.log("UserAPI.is_authen(): ", UserAPI.is_authen());
    return await UserAPI.is_authen().then(async (res_authen) => {
      // console.log("in unit");
      if (res_authen) {
        let dpml_access = cookies.get("dpml_access");
        let config = {
          method: "get",
          url: dpml_config.img_get_all_unit_url,
          headers: {
            Authorization: `Bearer ${dpml_access}`,
            "Content-Type": "application/json",
          },
        };

        let recived_data = new Promise((resolve, reject) => {
          let response = {
            status: null,
            data: null,
          };
          axios(config)
            .then((res) => {
              // console.log("res: ", res);
              response.status = true;
              response.data = res.data;
              resolve(response);
            })
            .catch((err) => {
              response.status = false;
              // console.log("err",err)
              try {
                response.data = err.response.data;
              } catch (error) {
                response.data = "Server not response.";
              }
              resolve(response);
            });
        });
        // ###################################################
        return await recived_data;
      }
    });
  },
};
