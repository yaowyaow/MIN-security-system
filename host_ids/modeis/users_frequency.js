// 模型
const mongoose = require("mongoose");
const Schema = mongoose.Schema;//实例化Schema

// 各个模型 Schema
const Users_frequencySchema = new Schema({
    username:{
        type:String,
        
    },
    command:{
        type:Schema.Types.Mixed,
        
    },
    Time:{
        type:String,
        required:true
    }
}, {collection: 'userFrequency'})
// 输出
const Users_frequency = module.exports = mongoose.model("users_frequency",Users_frequencySchema);
