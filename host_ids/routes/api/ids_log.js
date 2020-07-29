// @login & register npm node.js
const express = require("express");//表达
const router = express.Router();//路由
const passport = require("passport");

const models = require('../../config/db');
const packet_flow = require("../../modeis/packet_flow");//引用
const event_log = require("../../modeis/event_log");
const users_frequency = require("../../modeis/users_frequency");
var process = require("child_process");


// $route post api/users/register
// @desc 返回的请求json
// @access public

router.get("/is_running", (req, res) => {
    process.exec('ps -aux | grep net_message.py | wc -l',function (error, stdout, stderr) {
        if (error !== null) {
          console.log('exec error: ' + error);
          }else{
	  console.log(stdout);
          res.json(stdout);}
	});
    });

router.get("/turn-on", (req, res) => {
    process.exec('python ../net_ids/net_message.py',function (error, stdout, stderr) {
        if (error !== null) {
          console.log('exec error: ' + error);
          }else{
          console.log(stdout);
          res.json(stdout);}
        });
    });


// 查询所有日志信息路由
router.get("/ids_log", (req, res) => {
    packet_flow.find({}).sort({_id:-1}).limit(10000)
      .then(packet => {
        res.json(packet);
      })
      .catch(err => {
        console.log(2);
        res.json(err);
      });
  });

//带有时间限制的日志查询
router.put("/ids_log_time", (req,res) => {
    if(req.body.params.time_s && req.body.params.time_e){
      packet_flow.find({"Time":{$gte:req.body.params.time_s,$lt:req.body.params.time_e}}).sort({_id:-1}).limit(10000)
      .then(packet => {
        res.json(packet);
      })
      .catch(err => {
        console.log(2);
        res.json(err);
      });
    }
});



// $route get api/alerts/detail/:id
// @desc 获取单个信息
// @access Privte
router.get("/ids_detail",(req,res) =>{
    packet_flow.findById(req.params.id)
        .then(packet => {
            res.json(packet);
        })
        .catch(err => {
            res.json(err);
        });
    });

//查询恶意流量检测日志
router.get("/event_log", (req,res) =>{
    event_log.find()
    .sort({ "_id": -1 })
    .limit(10000)
    .then(packet => {
      res.json(packet);
    })
    .catch(err => {
      console.log(2);
      res.json(err);
    });
})

//时间  查询 恶意流量
router.put("/event_log_time", (req,res) => {
    if(req.body.params.time_s && req.body.params.time_e){
      event_log.find({"Time":{$gte:req.body.params.time_s,$lt:req.body.params.time_e}}).sort({_id:-1}).limit(10000)
      .then(packet => {
        res.json(packet);
      })
      .catch(err => {
        console.log(2);
        res.json(err);
      });
    }
});


/*router.get("/event_detail",(req,res) =>{
    event_log.findById(req.params.id)
        .then(packet => {
            res.json(packet);
        })
        .catch(err => {
            res.json(err);
        });
    });
*/

router.get("/detection", (req,res) =>{
    packet_flow.distinct("username")
        .then(packet => {
	    res.json(packet );
	})
	.catch(err => {
	    res.json(err);
	});
    });


router.get("/users_frequency", (req,res) =>{
    users_frequency.find().sort({_id:-1}).limit(10000)
    .then(packet => {
	res.json(packet);
    })
    .catch(err => {
	res.json(err);
    })
});

router.put("/users_frequency_time", (req,res) => {
    if(req.body.params.time_s && req.body.params.time_e){
      users_frequency.find({"Time":{$gte:req.body.params.time_s,$lt:req.body.params.time_e}}).sort({_id:-1}).limit(10000)
      .then(packet => {
        res.json(packet);
      })
      .catch(err => {
        console.log(2);
        res.json(err);
      });
    }
});

router.put("/chart_tool_time", (req,res) =>{
    users_frequency.find({"username":req.body.params.username}, {"_id":0,"Time":1}).sort({_id:-1}).limit(60)
    .then(packet => {
        res.json(packet);
        console.log("chart_tool_x");
	console.log(req.body.params.username);
	console.log("end");
    })
    .catch(err => {
        res.json(err);
    })
});
/*
router.put("/chart_tool_freq", (req,res) =>{
    var list = [];
    var result = users_frequency.find({"username":req.body.params.username}, {"_id":0,"frequency":1});
    console.log(result.data);
  if(result.data!=undefined){
    result.data.forEach(function(err,doc) {
	if(error){
		console.log(error);
	}else{
		if(doc!=null){
			console.log(doc);
			list.push(doc.frequency);
		}else{
			res.json(list);
			console.log(list);
		}
	}
    });    
  }else{
	console.log(result);
  }
});
*/
router.put("/chart_tool_freq", (req,res) =>{
    users_frequency.find({"username":req.body.params.username}, {"_id":0,"frequency":1}).sort({_id:-1}).limit(60)
    .then(packet => {
        res.json(packet);
        console.log("chart_tool_y");
        console.log(req.body.params.username);
	//console.log(Object.values(packet));
        console.log("end");
    })
    .catch(err => {
        res.json(err);
    })
});

router.put("/ids_log_del", (req,res) => {
    if(req.body.params._id){
        packet_flow.deleteOne({_id:req.body.params._id}, function(error){
                if(error){
                        console.error(error);
                }else{
                        console.error("delete success");
                        res.send("ok");
                }
        });
    }
});

router.put("/event_log_del", (req,res) => {
    if(req.body.params._id){
        event_log.deleteOne({_id:req.body.params._id}, function(error){
                if(error){
                        console.error(error);
                }else{
                        console.error("delete success");
                        res.send("ok");
                }
        });
    }
});

router.put("/users_frequency_del", (req,res) => {
    if(req.body.params._id){
    	users_frequency.deleteOne({_id:req.body.params._id}, function(error){
		if(error){
			console.error(error);
		}else{
			console.error("delete success");
			res.send("ok");
		}
	});
    }
});

    


module.exports = router; // 报错



    
    
