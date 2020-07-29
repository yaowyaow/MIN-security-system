// 模型
const mongoose = require("mongoose");
const Schema = mongoose.Schema;//实例化Schema

// 各个模型 Schema
const EventSchema = new Schema({
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
    danger:{
        type:String,
    },
    request:{
        type:String,
    },
    message:{
        any:Schema.Types.Mixed
    }
}, {collection: 'event_log'})
// 输出
const Event_log = module.exports = mongoose.model("event_log",EventSchema);
