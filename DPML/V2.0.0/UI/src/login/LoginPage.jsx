// LoginPage
// Description : กำหนด UI ของหน้าจอเข้าสู่ระบบ
// Author : Athiruj Poositaporn
import React, { Component } from "react";
import { Cookies } from "react-cookie";
import Swal from "sweetalert2";
import UserAPI from "../services/UserAPI";

const cookies = new Cookies();

class LoginPage extends Component {
  state = {
    username: null,
    password: null,
  };

  // handle_login
  // Description : เรียกใช้งาน UserAPI.login(data) เพื่อตรวจสอบสิทธิ์การเข้าสู่ระบบ
  // Author : Athiruj Poositaporn
  handle_login = () => {
    const data = {
      username: this.state.username,
      password: this.state.password,
    };
    // console.log("username: ", this.state.username);
    // console.log("password: ", this.state.password);
    UserAPI.login(data).then((response) => {
      if (response.status) {
        const { access_token, refresh_token } = response.data.tokens;
        const { role } = response.data;
        cookies.set("dpml_access", access_token, { path: "/", maxAge: 3600 });
        cookies.set("user_role", role, { path: "/", maxAge: 2592000 });
        cookies.set("username", this.state.username, {
          path: "/",
          maxAge: 2592000,
        });

        cookies.set("dpml_refresh", refresh_token, {
          path: "/",
          maxAge: 2592000,
        });
        window.location.href = "/upload";
      } else {
        if (response.data.status === "system_error") {
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
    });
  };

  // handle_change
  // Description : เก็บค่า usernama และ password
  // Author : Athiruj Poositaporn
  handle_change = (event) => {
    const { value, name } = event.target;
    switch (name) {
      case "username":
        this.state.username = value;
        break;
      case "password":
        this.state.password = value;
        break;

      default:
        break;
    }
  };

  // handle_input
  // Description : ตรวจสอบค่า input ของ username และ password
  // Author : Athiruj Poositaporn
  handle_input = () =>{
    const {username , password} = this.state
    if(!username || !password){
      let data = {
        icon:'error',
        title: 'Blank username or password.'
      }
      this.show_sweet_alert(data)
    }else{
      this.handle_login()
    }
  }

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

  render() {
    const dpml_refresh = cookies.get("dpml_refresh");
    if (dpml_refresh) window.location.href = "/upload";
    else
      return (
        <div className="hold-transition login-page">
          <div className="login-box">
            <div className="login-logo">DPML</div>
            {/* /.login-logo */}
            <div className="card">
              <div className="card-body login-card-body">
                <p className="login-box-msg">Sign in to continue</p>

                {/* Form sign in */}
                {/* <form> */}
                <div className="input-group mb-3">
                  <input
                    type="text"
                    name="username"
                    className="form-control"
                    onChange={(event) => {
                      this.handle_change(event);
                    }}
                    placeholder="Username"
                  />
                  <div className="input-group-append">
                    <div className="input-group-text">
                      <span className="fas fa-user" />
                    </div>
                  </div>
                </div>
                <div className="input-group mb-3">
                  <input
                    type="password"
                    name="password"
                    className="form-control"
                    onChange={(event) => {
                      this.handle_change(event);
                    }}
                    placeholder="Password"
                  />
                  <div className="input-group-append">
                    <div className="input-group-text">
                      <span className="fas fa-lock" />
                    </div>
                  </div>
                </div>
                <div className="row">
                  <div className="col-12">
                    <button
                      onClick={this.handle_input}
                      className="btn btn-primary btn-block"
                    >
                      Sign In
                    </button>
                  </div>
                </div>
                {/* </form> */}
                {/* Form sign in */}
              </div>
              {/* /.login-card-body */}
            </div>
          </div>
        </div>
      );
  }
}

export default LoginPage;
