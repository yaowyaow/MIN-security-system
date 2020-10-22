// 模型
var serv = require("../routes/api/ids_log");
const mongoose = require("mongoose");
const Schema = mongoose.Schema;//实例化Schema

// 各个模型 Schema
const UEBASchema = new Schema({
    username:{
        type:String,
    },
    mac_count:{
        type:Number,
    },
    score:{
        type:Number,
    },
    abnormal_flow:{
        type:Number,

    },
    url_count:{
        type:Number,
    },
    ip_count:{
        type:Number,
    },
    file_count:{
        type:Number,
    },
    new_ip_count:{
        type:Number,
    },
    date:{
        type:String,
    },
    time_count:{
        type:Number,
    }
}, {collection: 'ueba_data'})
// 输出
const UEBA_data = module.exports = serv.mon_min.model("ueba_data",UEBASchema);
