/**
 * UserAPI
 * Description : Service เรียกใช้ API ของ user_api
 * Author : Athruj Poositporn
 */
import axios from "axios";
import sha256 from "crypto-js/sha256";
import { Cookies } from "react-cookie";
import { dpml_config } from "../config";
const cookies = new Cookies();
export default {
  /**
   * login
   * Description : ฟังก์ชันสำหรับปรับสถานะการเข้าสู่ระบบของผู้ใช้งาน และกำหนด token
   * Author : Athruj Poositporn
   */
  async login(data) {
    let from_data = new FormData();
    from_data.append("username", data.username);
    from_data.append("password", sha256(data.password).toString());
    let response = {
      status: true,
      data: null,
    };
    let recived_data = new Promise((resolve, reject) => {
      axios
        .post(dpml_config.user_login_url, from_data, null)
        .then((res) => {
          //   console.log("Success get all: ", res.data);
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
  },

  /**
   * logout
   * Description : ฟังก์ชันสำหรับปรับสถานะการออกจากระบบของผู้ใช้งาน
   * Author : Athruj Poositporn
   */
  async logout(data) {
    let from_data = new FormData();
    const username = cookies.get("username");
    from_data.append("username", username);
    let response = {
      status: true,
      data: null,
    };
    let recived_data = new Promise((resolve, reject) => {
      axios
        .post(dpml_config.user_logout_url, from_data, null)
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
  },

  /**
   * refresh_token
   * Description : ฟังก์ชันสำหรับกำหนดค่าของ access token ใหม่
   * Author : Athruj Poositporn
   */
  async refresh_token(data) {
    // let from_data = new FormData();
    // from_data.append("username", data.username);
    // from_data.append("refresh_token", data.refresh_token);
    let response = {
      status: true,
      data: null,
    };
    let config = {
      method: "post",
      url: dpml_config.user_refresh_url,
      headers: {
        Authorization: `Bearer ${data.refresh_token}`,
        "Content-Type": "application/json",
      },
    };
    let recived_data = new Promise((resolve, reject) => {
      axios(config)
        .then((res) => {
          // console.log("Success refeash: ", res.data);
          resolve(res);
        })
        .catch((err) => {
          response.status = false;
          try {
            // console.log("Error refeash: ", err.response.data);
            response.data = err.response.data;
          } catch (error) {
            response.data = "Server not response.";
          }
          resolve(response);
        });
    });
    return await recived_data;
  },

  /**
   * is_authen
   * Description : ฟังก์ชันสำหรับตรวจสอบสิทธิ์การเข้าถึงของผู้ใช้งาน
   * Author : Athruj Poositporn
   */
  async is_authen() {
    let dpml_access = cookies.get("dpml_access");
    let dpml_refresh = cookies.get("dpml_refresh");
    if (dpml_access) {
      var recived_data = new Promise((resolve, reject) => {
        resolve(true);
      });
    } else if (dpml_refresh) {
      const data = { refresh_token: dpml_refresh };
      var recived_data = new Promise((resolve, reject) => {
        this.refresh_token(data).then((response) => {
          if (response.status) {
            cookies.set("dpml_access", response.data.refresh_token, {
              path: "/",
              maxAge: 3600,
            });
            resolve(true);
          } else {
            window.location.href = "/login";
          }
        });
      });
    } else {
      window.location.href = "/login";
    }
    return await recived_data;
  },
};
