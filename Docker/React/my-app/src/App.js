import React, { Component } from "react";
import axios from "axios";
import NavBar from "./components/navbar";
import Counters from "./components/counters";
// import './App.css';
class App extends Component {
  // getData(){
  //   axios.get('http://localhost:5001/get_all_user')
  //     .then(res=>{
  //       console.log(res.data)
  //     })
  // }
  state = {
    counters: [
      { id: 1, value: 4 },
      { id: 2, value: 0 },
      { id: 3, value: 0 },
      { id: 4, value: 0 },
    ],
  };

  handleIncrement = (counter) => {
    //   Clone ค่าของ this.state.counters ให้กับ counters ทำให้กลายเป็นค่าเดียวกัน
    const counters = [...this.state.counters];
    const index = counters.indexOf(counter);
    counters[index].value++;
    this.setState({ counters });
    console.log(this.state.counters[index]);
  };

  handleReset = () => {
    const counters = this.state.counters.map((c) => {
      c.value = 0;
      return c;
    });
    this.setState({ counters });
  };

  handleDelete = (counterId) => {
    const counters = this.state.counters.filter((c) => c.id !== counterId);
    this.setState({ counters });
    // or
    // this.setState({ counters: counters })
  };

  render() {
    return (
      <React.Fragment>
        <NavBar
          totleCounters={this.state.counters.filter((c) => c.value > 0).length}
        />
        <main className="container">
          <Counters
            counters={this.state.counters}
            onReset={this.handleReset}
            onIncrement={this.handleIncrement}
            onDelete={this.handleDelete}
          />
        </main>
      </React.Fragment>
    );
  }
}

export default App;
