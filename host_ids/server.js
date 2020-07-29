const express = require('express');
const mongoose = require('mongoose');
const path = require('path');
const bodyParser = require('body-parser');
const passport = require('passport');
const app = express();

app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: false }));

const mysql = require('mysql')
const models = require('./config/db');
//执行前端静态页面
if(process.env.NODE_ENV === "production"){
  app.use(express.static("client/dist"));
  app.get("*",(req,res) => {
    res.sendFile(path.resolve(__dirname,"client","dist","index.html"));
  });
}

const fs = require('fs');
//const path = require('path');

/*  读取文件内容
fs.readFile(path.join(__dirname,'/home/minuser/xin777/logs/event.log'),'utf-8',(err,datastr)=>{
	console.log(datastr);
});
*/



// 引入users.js
const users = require('./routes/api/users');
const alerts = require('./routes/api/alerts');
const ids_log = require('./routes/api/ids_log');

// DB config
const db = require('./config/keys').mongoURI;

// 使用body-parser中间件
//app.use(bodyParser.urlencoded({ extended: false }));
//app.use(bodyParser.json());

// Connect to mongodb
/*
mongoose
  .connect(
    db,{useNewUrlParser: true}
	)
  .then(() => console.log('MongoDB Connected'))
  .catch(err => console.log(err));
*/
mongoose
  .connect(
    "mongodb://localhost:27017/packet_flow",
    { useNewUrlParser: true }
  )
  .then(() => console.log('MongoDB Connected'))
  .catch(err => console.log(err));

// Connect to my sql
const connection = mysql.createConnection(models.mysql);
connection.connect();
var sql = 'SELECT * FROM alert';
connection.query(sql,function(err,result){
  if(err){
      console.log('[SELECT ERROR]-',err.message);
      return;
  }
  console.log('Mysql Connected');
})


// passport 初始化
app.use(passport.initialize());

require('./config/passport')(passport);

// app.get("/",(req,res) => {
//   res.send("Hello World!");
// })

// 使用routes
app.use('/api/users', users);
app.use('/api/alerts',alerts);
app.use('/api/ids_log', ids_log);

const port = process.env.PORT || 9003;
app.listen(port, () => {
  console.log(`Server running on port ${port}`);
});


