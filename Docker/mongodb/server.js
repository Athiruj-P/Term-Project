const express = require("express");
const app = express();
const connectDb = require("./src/connection");

const PORT = 8080;

app.get("/users", (req, res) => {
  res.send("Get users \n");
});

app.get("/user-create", (req, res) => {
  res.send("User created \n");
});

app.listen(PORT, function() {
  console.log(`Listening on ${PORT}`);

  connectDb().then(() => {
    console.log("MongoDb connected");
  });
})