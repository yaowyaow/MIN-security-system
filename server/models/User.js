// 模型
//var serv = require("../routes/api/ids_log");
var serv = require('../routes/api/users');
const mongoose = require("mongoose");
const Schema = mongoose.Schema;//实例化Schema

// 各个模型 Schema
const UseSchema = new Schema({
    name:{
        type:String,
        required:true
    },
    email:{
        type:String,
        required:true
    },
    password:{
        type:String,
        required:true
    },
    avatar:{
        type:String,
    },
    identity:{
        type:String,
        required:true
    },
    Date:{
        type:Date,
        default:Date.now
    }
}, {collection:"users"})
// 输出
//console.log(serv.mon_min);
module.exports = User = serv.mon_min.model("users",UseSchema);
