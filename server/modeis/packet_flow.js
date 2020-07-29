// 模型
var serv = require('../routes/api/ids_log')
const mongoose = require("mongoose");

const Schema = mongoose.Schema;//实例化Schema

// 各个模型 Schema
const PacketSchema = new Schema({
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
        required:true
    },
    sport:{
        type:Number,
    },
    dport:{
        type:Number,
        required:true
    },
    packet_type:{
        type:String,
    },
    request:{
        type:String,
    },
    data:{
        any:Schema.Types.Mixed
    },
    survice:{
	type:Number,
    },
    dst_ip:{
	type:String,
    }
}, {collection: 'packet_flow'})
// 输出
//console.log(serv.mon_min);
const Packet_flow  = serv.mon_min.model("packet_flow",PacketSchema);
/*
Packet_flow.find({}).sort({_id:-1}).limit(4)
      .then(packet => {
	console.log(packet);
      })
      .catch(err => {
        console.log(2);
      });
*/
module.exports  = Packet_flow;
