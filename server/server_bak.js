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

var mon_db1 = mongoose
  .createConnection(
    "mongodb://localhost:27017/Situation_Awareness",
    { useNewUrlParser: true }
	//,{mongos:true}
  );

//  .then(() => console.log('SA Connected'))
//  .catch(err => console.log(err));

var mon_min = mongoose
  .createConnection(
    "mongodb://localhost:27017/packet_flow",
    { useNewUrlParser: true}
  );

var mon_test = mongoose
  .createConnection(
	"mongodb://localhost:27017/packet_flow",
	{useNewUrlParser: true}
);
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

var teSchema = new Schema({
    version:{
	type:String,
    }
}, {collection: 'system.version'});




var acketSchema = new Schema({
    username:{
        type:String,

    },
    uuid:{
        type:String,
    },
    bytes:{
        type:Number,
    },
    command:{
        type:String,

    },
    src_ip:{
        type:String,
    },
    Time:{
        type:String,
    },
    sport:{
        type:Number,
    },
    dport:{
        type:Number,
    },
    packet_type:{
        type:String,
    },
    request:{
        type:String,
    },
    data:{
       // any:Schema.Types.Mixed
	type:String
    },
    survice:{
        type:Number,
    },
    dst_ip:{
        type:String,
    }
}, {collection: 'packet_flow'})



var testModel = mon_min.model('test', acketSchema);
testModel.find().sort({_id:-1}).limit(3)
      .then(packet => {
	console.log("this is a test");
        console.log(packet);
      })
      .catch(err => {
        console.log(2);
      });










var valueSchema = new Schema({
  value:Number,
  time:String
},{collection: 'SA_value'});

var valueModel = mon_db1.model('value', valueSchema);

var valueinfo = {};
valueModel.findOne({}, function(err, data){
  if (err) throw err;
  valueinfo = data;
	console.log(data);
});
/*
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
	



  })

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

  setInterval(() =>{

	console.log("60000 times");
	  valueModel.find().sort({_id:-1}).limit(540)
	    .then(packet => {
		console.log("send mongo_data");
		socket.emit('data', packet)
	    })
	    .catch(err => {
		confole.log(err);
	    });

	//120条数据是6个小时j
	host_valueModel.find().sort({_id:-1}).limit(120)
        .then(packet => {
                console.log("send host_value");
                socket.emit('host_value', packet)
        })
        .catch(err => {
                console.log(err);
        })	


	},60000)
	



})




app2.listen(9002, function() {
  console.log('listen on 9002')
})

*/

