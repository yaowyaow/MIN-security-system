const express = require('express');
const mongoose = require('mongoose');
const path = require('path');
const bodyParser = require('body-parser');
const passport = require('passport');
const app = express();

var http = require('http')
var app2 = http.Server(app);



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
const ids_log = require('./routes/api/ids_log');
const users = require('./routes/api/users');
const alerts = require('./routes/api/alerts');
//const ids_log = require('./routes/api/ids_log');

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
var mon_db1 = mongoose
  .createConnection(
    "mongodb://localhost:27017/Situation_Awareness",
    { useNewUrlParser: true }
	//,{mongos:true}
  );
//  .then(() => console.log('SA Connected'))
//  .catch(err => console.log(err));

/*
var mon_min = mongoose
  .createConnection(
    "mongodb://localhost:27017/packet-flow",
    { userNewUrlParser: true}
  );
*/
//global.mon_min = mon_min
//.then(() => console.log('packet-flow Connected'))
// .catch(err => console.log(err));



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


var Schema = mongoose.Schema;
//网络态势威胁值
var valueSchema = new Schema({
  value:Number,
  time:String
},{collection: 'SA_value'});

var valueModel = mon_db1.model('value', valueSchema);

var valueinfo = {};
valueModel.findOne({}, function(err, data){
  if (err) throw err;
  valueinfo = data;
});

//主机态势威胁值
var host_valueSchema = new Schema({
  value:Number,
  time:String
},{collection: 'SA_host_value'});

var host_valueModel = mon_db1.model('host_value', host_valueSchema);
host_valueModel.findOne({}, function(err, data){
  if (err) throw err;
  host_valueinfo = data;
});

//网络态势预测值
var predict_valueSchema = new Schema({
  value:Number,
  time:String
}, {collection: 'SA_predict_value'});

var predict_valueModel = mon_db1.model('predict_value', predict_valueSchema);
/*
predict_valueModel.findOne({}, function(err, data){
  if (err) throw err;
  host_valueinfo = data;
	console.log("预测值", data);
});
*/
//主机态势预测值
var predict_host_valueSchema = new Schema({
  value:Number,
  time:String
},{collection: 'SA_host_predict_value'});
var predict_host_valueModel = mon_db1.model('predict_host_value', predict_host_valueSchema);
/*send test
predict_host_valueModel.findOne({}, function(err, data){
  if (err) throw err;
  host_valueinfo = data;
        console.log("预测值", data);
});
*/


io = require('socket.io')(app2)
io.on('connection', function(socket) {
  //socket.emit('news', 'Hello world');
  socket.on('request', function(data) {
    console.log("res ***************");
    console.log(data);
   //当客户端发送request时，则返回第一批数据

   valueModel.find().sort({_id:-1}).limit(540)
            .then(packet => {
                console.log("send mongo_data");
		packet = packet.reverse();
                socket.emit('data', packet)
            })
            .catch(err => {
                console.log(err);
            })

  //第一次发送host_value
  host_valueModel.find().sort({_id:-1}).limit(120)
        .then(packet => {
                console.log("send host_value");
		packet = packet.reverse();
                socket.emit('host_value', packet)
        })
        .catch(err => {
                console.log(err);
        })
  //第一次发送网络态势预测值

  predict_valueModel.find().sort({_id:-1}).limit(540)
            .then(packet => {
                console.log("send predict_value");
		packet = packet.reverse();
                socket.emit('predict_data', packet)
            })
            .catch(err => {
                console.log(err);
            })
  //第一次发送主机态势预测值
  predict_host_valueModel.find().sort({_id:-1}).limit(120)
        .then(packet => {
                console.log("send predict host_value");
		packet = packet.reverse();
                socket.emit('predict_host_value', packet)
        })
        .catch(err => {
                console.log(err);
        })


  })
/*
  //第一次发送value
  valueModel.find().sort({_id:-1}).limit(540)
            .then(packet => {
                console.log("send mongo_data");
                socket.emit('data', packet)
            })
            .catch(err => {
                console.log(err);
            })

  //第一次发送host_value
  host_valueModel.find().sort({_id:-1}).limit(120)
	.then(packet => {
		console.log("send host_value");
		socket.emit('host_value', packet)
	})
	.catch(err => {
		console.log(err);
	})
*/

  setInterval(() =>{

	console.log("60000 times");
	//网络态势值
	  valueModel.find().sort({_id:-1}).limit(540)
	    .then(packet => {
		console.log("send mongo_data", packet);
		packet = packet.reverse();
		socket.emit('data', packet)
	    })
	    .catch(err => {
		confole.log(err);
	    });

	//主机态势值，120条数据是6个小时j
	host_valueModel.find().sort({_id:-1}).limit(120)
        .then(packet => {
                console.log("send host_value", packet);
		packet = packet.reverse();
                socket.emit('host_value', packet)
        })
        .catch(err => {
                console.log(err);
        });
	//网络态势预测值

	predict_valueModel.find().sort({_id:-1}).limit(540)
            .then(packet => {
                console.log("send predict_value");
		packet = packet.reverse();
                socket.emit('predict_data', packet)
            })
            .catch(err => {
                console.log(err);
            })
	//主机态势预测值
	predict_host_valueModel.find().sort({_id:-1}).limit(120)
        .then(packet => {
                console.log("send predict host_value");
		packet = packet.reverse();
                socket.emit('predict_host_value', packet)
        })
        .catch(err => {
                console.log(err);
        })

	


	},60000)
	



})




app2.listen(9002, function() {
  console.log('listen on 9002')
})



