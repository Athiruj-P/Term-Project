/**
 * ImageModal
 * Description : หน้าจอส่วนการแสดงผลลัพธ์
 * Author : Athruj Poositporn
 */
import React, { Component } from "react";

export class ImageModal extends Component {
  render() {
    const { image, image_2 } = this.props;
    return (
      <div
        className="modal fade"
        id={!image_2 ? "imageModal" : "image3DModal"}
        tabIndex={-1}
        role="dialog"
      >
        <div
          className={
            !image_2 ? "modal-dialog modal-lg" : "modal-dialog modal-xl"
          }
        >
          <div className="modal-content">
            <div className="modal-header">
              <h5 className="modal-title" id="title">
                Result image
              </h5>
              <button
                type="button"
                className="close"
                data-dismiss="modal"
                aria-label="Close"
              >
                <span aria-hidden="true">×</span>
              </button>
            </div>
            <div className="modal-body" style={{ maxHeight: "80%" }}>
              {!image_2 ? (
                <div className="row">
                  <div className="col-md-12">
                    <img src={image} alt="" width="100%" />
                  </div>
                </div>
              ) : (
                <div className="row">
                  <div className="col-md-6">
                    <img src={image} alt="" width="100%" />
                  </div>
                  <div className="col-md-6">
                    <img src={image_2} alt="" width="100%" />
                  </div>
                </div>
              )}
            </div>
            <div className="modal-footer d-flex justify-content-between">
              <button
                type="button"
                className="btn btn-secondary"
                data-dismiss="modal"
              >
                Close
              </button>
            </div>
          </div>
        </div>
      </div>
    );
  }
}

export default ImageModal;
