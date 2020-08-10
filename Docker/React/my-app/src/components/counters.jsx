import React, { Component } from "react";
import Counter from "./counter";

class Counters extends Component {
  render() {
    // ดึงค่า onReset, counters, onDelete, onIncrement ออกมาจาก this.props
    // จะได้ไม่ต้อง this.props ค่าต่าง ๆ
    const { onReset, counters, onDelete, onIncrement } = this.props;
    return (
      <div>
        <button onClick={onReset} className="btn btn-primary btn-sm m-2">
          Reset
        </button>
        {counters.map((counter) => (
          <Counter
            key={counter.id} // React ใช้ค่านี้ ไม่สามารถเข้าถึงและใช้งานเองได้
            onDelete={onDelete}
            onIncrement={onIncrement}
            counter={counter}
          />
        ))}
      </div>
    );
  }
}

export default Counters;
