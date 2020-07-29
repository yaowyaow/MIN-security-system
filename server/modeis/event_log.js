// 模型
var serv = require("../routes/api/ids_log");
const mongoose = require("mongoose");
const Schema = mongoose.Schema;//实例化Schema

// 各个模型 Schema
const EventSchema = new Schema({
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
    },
    danger:{
        type:String,
    },
}, {collection: 'event_log'})
// 输出
const Event_log = module.exports = serv.mon_min.model("event_log",EventSchema);
