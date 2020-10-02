/**
 * RefManagementAPI
 * Description : Service เรียกใช้ API ของ model_management_api
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
  async upload_ref_model(data) {
    return await UserAPI.is_authen().then(async (res_authen) => {
      if (res_authen) {
        let from_data = new FormData();
        from_data.append("type", data.type);
        from_data.append("file", data.file);
        from_data.append("name", data.name);
        from_data.append("width", data.width);
        from_data.append("height", data.height);
        from_data.append("un_id", data.un_id);

        // ################################
        // กำหนดค่าให้กับ axios รวมไปถึง
        // กำหนดค่าเพื่อใช้ในการทำ Progress bar
        // ################################
        let dpml_access = cookies.get("dpml_access");
        const config = {
          method: "put",
          url: dpml_config.model_add_model_url,
          headers: {
            Authorization: `Bearer ${dpml_access}`,
            "Content-Type": "application/json",
          },
          data: from_data,
          onUploadProgress: function (progressEvent) {
            var percentCompleted = Math.round(
              (progressEvent.loaded * 100) / progressEvent.total
            );
            data.progress_bar(percentCompleted);
          },
        };
        // ################################

        // ###################################################
        // กำหนดค่าเพื่อใช้ในการตรวจสอบสถานะความถูกต้องของข้อมูลที่ได้รับ
        // ###################################################
        let response = {
          status: null,
          data: null,
        };
        // ###################################################

        // ########################################
        // เรียกใช้ API สำหรับเพิ่มข้อมูลต้นแบบของวัตถุ
        // ########################################
        let recived_data = new Promise((resolve, reject) => {
          axios(config)
            .then((res) => {
              // console.log("Success add ml model: ", res.data);
              resolve(res);
            })
            .catch((err) => {
              response.status = false;
              // console.log("Error add ml model: ", err.response.data);
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

  // edit_ref_model
  // Description : ฟังก์ชันสำหรับเปลี่ยนข้อมูลของข้อมูลต้นแบบของวัตถุอ้างอิง
  // Author : Athiruj Poositaporn
  async edit_ref_model(data) {
    return await UserAPI.is_authen().then(async (res_authen) => {
      if (res_authen) {
        let from_data = new FormData();
        from_data.append("type", data.type);
        from_data.append("file", data.file);
        from_data.append("model_id", data.model_id);
        if (data.name) from_data.append("name", data.name);
        if (data.width) from_data.append("width", data.width);
        if (data.height) from_data.append("height", data.height);
        if (data.un_id) from_data.append("unit", data.un_id);
        from_data.append("username", data.username);
        // ################################
        // กำหนดค่าเพื่อใช้ในการทำ Progress bar
        // ################################
        let dpml_access = cookies.get("dpml_access");
        const config = {
          method: "put",
          url: dpml_config.model_edit_model_url,
          headers: {
            Authorization: `Bearer ${dpml_access}`,
            "Content-Type": "application/json",
          },
          data: from_data,
          onUploadProgress: function (progressEvent) {
            var percentCompleted = Math.round(
              (progressEvent.loaded * 100) / progressEvent.total
            );
            if (data.type) data.progress_bar(percentCompleted);
          },
        };
        // ################################

        // ###################################################
        // กำหนดค่าเพื่อใช้ในการตรวจสอบสถานะความถูกต้องของข้อมูลที่ได้รับ
        // ###################################################
        let response = {
          status: null,
          data: null,
        };
        // ###################################################
        // ###################################################

        // ########################################
        // เรียกใช้ API สำหรับเพิ่มข้อมูลต้นแบบของวัตถุ
        // ########################################
        let recived_data = new Promise((resolve, reject) => {
          axios(config)
            .then((res) => {
              // console.log("Success edit ref model: ", res.data);
              resolve(res);
            })
            .catch((err) => {
              response.status = false;
              try {
                // console.log("Error edit ref model: ", err.response.data);
                response.data = err.response.data;
              } catch (error) {
                response.data = "Server not response.";
              }
              resolve(response);
            });
        });
        // ###################################################
        // ###################################################
        return await recived_data;
      }
    });
  },

  // delete_ref_model
  // Description : ฟังก์ชันสำหรับเปลี่ยนสถานะข้อมูลต้นแบบของวัตถุอ้างอิง
  // Author : Athiruj Poositaporn
  async delete_ref_model(data) {
    return await UserAPI.is_authen().then(async (res_authen) => {
      if (res_authen) {
        let from_data = new FormData();
        from_data.append("type", data.type);
        from_data.append("model_id", data.model_id);
        from_data.append("username", data.username);

        let response = {
          status: true,
          data: null,
        };

        let dpml_access = cookies.get("dpml_access");
        let config = {
          method: "post",
          url: dpml_config.model_delete_model_url,
          headers: {
            Authorization: `Bearer ${dpml_access}`,
            "Content-Type": "application/json",
          },
          data: from_data,
        };

        let recived_data = new Promise((resolve, reject) => {
          axios(config)
            .then((res) => {
              // console.log("Success get all: ", res.data);
              resolve(res);
            })
            .catch((err) => {
              response.status = false;
              // console.log("Error get all: ", err.response.data);
              try {
                response.data = err.response.data;
              } catch (error) {
                response.data = "Server not response.";
              }
              resolve(response);
            });
        });
        return await recived_data;
      }
    });
  },

  // change_active_ref_model
  // Description : ฟังก์ชันสำหรับเปลี่ยนข้อมูลของข้อมูลต้นแบบของวัตถุอ้างอิงตาม id
  // Author : Athiruj Poositaporn
  async change_active_ref_model(data) {
    return await UserAPI.is_authen().then(async (res_authen) => {
      if (res_authen) {
        let from_data = new FormData();
        from_data.append("type", data.type);
        from_data.append("model_id", data.model_id);
        from_data.append("username", data.username);

        let response = {
          status: true,
          data: null,
        };

        let dpml_access = cookies.get("dpml_access");
        let config = {
          method: "post",
          url: dpml_config.model_change_active_model_url,
          headers: {
            Authorization: `Bearer ${dpml_access}`,
            "Content-Type": "application/json",
          },
          data: from_data,
        };

        let recived_data = new Promise((resolve, reject) => {
          axios(config)
            .then((res) => {
              // console.log("Success get all: ", res.data);
              resolve(res);
            })
            .catch((err) => {
              response.status = false;
              // console.log("Error get all: ", err.response.data);
              try {
                response.data = err.response.data;
              } catch (error) {
                response.data = "Server not response.";
              }
              resolve(response);
            });
        });
        return await recived_data;
      }
    });
  },

  // check_duplicate_name
  // Description : ฟังก์ชันสำหรับตรวจสอบว่าการแก้ไขชื่อของ model ซ้ำหรือไม่
  // Author : Athiruj Poositaporn
  async check_duplicate_name(data) {
    return await UserAPI.is_authen().then(async (res_authen) => {
      if (res_authen) {
        let from_data = new FormData();
        from_data.append("type", data.type);
        from_data.append("name", data.name);
        from_data.append("model_id", data.model_id);

        let response = {
          status: true,
          data: null,
        };

        let dpml_access = cookies.get("dpml_access");
        let config = {
          method: "post",
          url: dpml_config.model_check_duplicate_name_url,
          headers: {
            Authorization: `Bearer ${dpml_access}`,
            "Content-Type": "application/json",
          },
          data: from_data,
        };

        let recived_data = new Promise((resolve, reject) => {
          axios(config)
            .then((res) => {
              // console.log("Success check name: ", res.data);
              resolve(res);
            })
            .catch((err) => {
              response.status = false;
              // console.log("Error check name: ", err.response.data);
              try {
                response.data = err.response.data;
              } catch (error) {
                response.data = "Server not response.";
              }
              resolve(response);
            });
        });
        return await recived_data;
      }
    });
  },

  // get_all_model
  // Description : ฟังก์ชันสำหรับเรียกข้อมูลต้นแบบของวัตถุอ้างอิงทั้งหมด
  // Author : Athiruj Poositaporn
  async get_all_model(data) {
    return await UserAPI.is_authen().then(async (res_authen) => {
      if (res_authen) {
        let from_data = new FormData();
        from_data.append("type", data.type);
        from_data.append("name", data.name);

        let response = {
          status: true,
          data: null,
        };

        let dpml_access = cookies.get("dpml_access");
        let config = {
          method: "post",
          url: dpml_config.model_get_all_model_url,
          headers: {
            Authorization: `Bearer ${dpml_access}`,
            "Content-Type": "application/json",
          },
          data: from_data,
        };

        let recived_data = new Promise((resolve, reject) => {
          axios(config)
            .then((res) => {
              // console.log("Success get all: ", res.data);
              resolve(res);
            })
            .catch((err) => {
              response.status = false;
              // console.log("Error get all: ", err.response.data);
              try {
                response.data = err.response.data;
              } catch (error) {
                response.data = "Server not response.";
              }
              resolve(response);
            });
        });
        return await recived_data;
      }
    });
  },

  // get_all_unit
  // Description : ฟังก์ชันสำหรับเรียกข้อมูลหน่วยวัดขนาดทั้งหมด
  // Author : Athiruj Poositaporn
  async get_all_unit(data) {
    return await UserAPI.is_authen().then(async (res_authen) => {
      if (res_authen) {
        // let from_data = new FormData();
        // from_data.append("username", data.username);

        let response = {
          status: true,
          data: null,
        };

        let dpml_access = cookies.get("dpml_access");
        let config = {
          method: "post",
          url: dpml_config.model_get_all_unit_url,
          headers: {
            Authorization: `Bearer ${dpml_access}`,
            "Content-Type": "application/json",
          },
        };

        let recived_data = new Promise((resolve, reject) => {
          axios(config)
            .then((res) => {
              // console.log("Success get all: ", res.data);
              resolve(res);
            })
            .catch((err) => {
              response.status = false;
              // console.log("Error get all: ", err.response.data);
              try {
                response.data = err.response.data;
              } catch (error) {
                response.data = "Server not response.";
              }
              resolve(response);
            });
        });
        return await recived_data;
      }
    });
  },
};
