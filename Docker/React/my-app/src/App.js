import React, { Component } from 'react';
import axios from 'axios'
// import './App.css';
class App extends Component {
  getData(){
    axios.get('http://localhost:5001/get_all_user')
      .then(res=>{
        console.log(res.data)
      })
  }

  render() {
    return (
      <div className="App">
        <button onClick={()=>this.getData()}>Get all user</button>
        <br />
        <br />
        <form>
          <label>Username : </label>
          <input type="text"></input>
          <br />
          <label>password : </label>
          <input type="password"></input>
          <br />
          <label>role : </label>
          <input type="number"></input>
          <br />
          <label>status : </label>
          <input type="number"></input>
          <br /><br />
          <button type="submit">add new user</button>
        </form>
      </div>
    )
  }
}

export default App;
