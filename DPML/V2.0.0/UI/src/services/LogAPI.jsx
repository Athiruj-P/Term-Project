/**
 * LogAPI
 * Description : Service เรียกใช้ API ของ user_api
 * Author : Athruj Poositporn
 */
import axios from "axios";
import UserAPI from "./UserAPI";
import { dpml_config } from "../config";
import { Cookies } from "react-cookie";
const cookies = new Cookies();

export default {
  // get_log
  // Description : ฟังก์ชันสำหรับเรียกข้อมูลของ log
  // Author : Athiruj Poositaporn
  async get_log(data) {
    return await UserAPI.is_authen().then(async (res_authen) => {
      var recived_data = null;
      if (res_authen) {
        let from_data = new FormData();
        from_data.append("date_type", data.type);
        from_data.append("group", data.group);
        from_data.append("start_date", data.start_date);
        from_data.append("start_time", data.start_time);
        from_data.append("end_date", data.end_date);
        from_data.append("end_time", data.end_time);
        from_data.append("username", data.username);

        let response = {
          status: true,
          data: null,
        };

        let dpml_access = cookies.get("dpml_access");
        let config = {
          method: "post",
          url: dpml_config.log_get_log_url,
          headers: {
            Authorization: `Bearer ${dpml_access}`,
            "Content-Type": "application/json",
          },
          data: from_data,
        };
        recived_data = new Promise((resolve, reject) => {
          axios(config)
            .then((res) => {
              // console.log("Success get all: ", res.data);
              resolve(res);
            })
            .catch((err) => {
              response.status = false;
              try {
                // console.log("Error get all: ", err.response.data);
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

  // get_min_max_date
  // Description : ฟังก์ชันสำหรับเรียกข้อมูลวันที่แรกและวันที่ล่าสุดของไฟล์ประวัติการใช้งาน
  // Author : Athiruj Poositaporn
  async get_min_max_date(data) {
    return await UserAPI.is_authen().then(async (res_authen) => {
      var recived_data = null;
      if (res_authen) {
        let dpml_access = cookies.get("dpml_access");
        let config = {
          method: "post",
          url: dpml_config.log_get_min_max_date_url,
          headers: {
            Authorization: `Bearer ${dpml_access}`,
            "Content-Type": "application/json",
          },
        };
        let response = {
          status: true,
          data: null,
        };
        recived_data = new Promise((resolve, reject) => {
          axios(config)
            .then((res) => {
              resolve(res);
            })
            .catch((err) => {
              response.status = false;
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

  // add_log
  // Description : ฟังก์ชันสำหรับบันทึกการกระทำของผู้ใช้งานระบบ
  // Author : Athiruj Poositaporn
  async add_log(data) {
    var recived_data = null;
    UserAPI.is_authen().then((res_authen) => {
      if (res_authen) {
        let from_data = new FormData();
        from_data.append("action", data.action);
        let dpml_access = cookies.get("dpml_access");
        let config = {
          method: "post",
          url: dpml_config.log_add_log_url,
          headers: {
            Authorization: `Bearer ${dpml_access}`,
            "Content-Type": "application/json",
          },
          data: from_data,
        };

        let response = {
          status: true,
          data: null,
        };

        recived_data = new Promise((resolve, reject) => {
          axios(config)
            .then((res) => {
              resolve(res);
            })
            .catch((err) => {
              response.status = false;
              try {
                response.data = err.response.data;
              } catch (error) {
                response.data = "Server not response.";
              }
              resolve(response);
            });
        });
      }
    });
    return await recived_data;
  },
};
