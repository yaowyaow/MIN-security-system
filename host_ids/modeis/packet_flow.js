// 模型
const mongoose = require("mongoose");
const Schema = mongoose.Schema;//实例化Schema

// 各个模型 Schema
const PacketSchema = new Schema({
    username:{
        type:String,
        
    },
    command:{
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
    message:{
        any:Schema.Types.Mixed
    }
}, {collection: 'packet_flow'})
// 输出
const Packet_flow = module.exports = mongoose.model("packet_flow",PacketSchema);