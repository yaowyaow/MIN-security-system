// @login & register npm node.js
const express = require("express");//表达
const router = express.Router();//路由
const passport = require("passport");
const mongoose = require("mongoose");

var mon_min = mongoose
  .createConnection(
    "mongodb://pkusz:pkusz@127.0.0.1:27017/Situation_Awareness?authSource=admin",
    { useNewUrlParser: true}
  );



module.exports.mon_min = mon_min;

const models = require('../../config/db');
const eth_info = require("../../modeis/EthInfo");//引用
var process = require("child_process");

//console.log(packet_flow.find({}).limit(3));
/*
packet_flow.find({}).sort({_id:-1}).limit(3)
      .then(packet => {
        console.log(packet);
      })
      .catch(err => {
        console.log(2);
      });
*/

// $route post api/users/register
// @desc 返回的请求json
// @access public

//router.get("/is_running", (req, res) => {
//    process.exec('ps -aux | grep net_message.py | wc -l',function (error, stdout, stderr) {
//        if (error !== null) {
//          console.log('exec error: ' + error);
//          }else{
//	  console.log(stdout);
//          res.json(stdout);}
//	});
//    });

//router.get("/turn-on", (req, res) => {
//    process.exec('python ../net_ids/net_message.py -vs',function (error, stdout, stderr) {
//        if (error !== null) {
//          console.log('exec error: ' + error);
//          }else{
//          console.log("run:" + stdout);
//          res.json(stdout);}
//        });
//    });

//router.get("/turn-off", (req, res) => {
//    process.exec('python ../net_ids/shutdown.py',function (error, stdout, stderr) {
//	console.log("turn-off");
//        if (error !== null) {
//          console.log('exec error: ' + error);
//          }else{
//          console.log("run:" + stdout);
//          res.json(stdout);}
//        });
//    });


// 查询最新的主机信息
router.get("/ethinfo", (req, res) => {
//    var mon_min = mongoose
//  .createConnection(
//    "mongodb://pkusz:pkusz@localhost:27017/Situation_Awareness?authSource=admin",
//    { useNewUrlParser: true }
    // ,{mongos:true}
//  )
//  mon_min.on('connected',function(err){
//    if(err){
//        console.log('SA连接失败：'+err);
//    }else{
//        console.log('SA Connected!');
//    }
//});

    eth_info.find().sort({_id:-1})
      .then(packet => {
        res.json(packet);
      })
      .catch(err => {
        console.log(err);
        res.json(err);
      });
  });

module.exports = router; // 报错



    
    
