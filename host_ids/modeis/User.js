// 模型
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
})
// 输出
module.exports = User = mongoose.model("users",UseSchema);