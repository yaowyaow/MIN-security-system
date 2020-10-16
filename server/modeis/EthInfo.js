// 模型
const mongoose = require("mongoose");
const Schema = mongoose.Schema;//实例化Schema

var mon_sa = mongoose
  .createConnection(
    "mongodb://pkusz:pkusz@localhost:27017/Situation_Awareness?authSource=admin",
    { useNewUrlParser: true }
        //,{mongos:true}
  );


// 各个模型 Schema
const EthInfoSchema = new Schema({
    bytes_sent:{
        type:Number,
        required:true
    },
    bytes_recv:{
        type:Number,
        required:true
    },
    name:{
        type:String
    },
    eth_status:{
        type:String,
        required:true
    },


 },{collection: 'EthInfo'})
// 输出
const EthInfo = module.exports = mon_sa.model("EthInfo",EthInfoSchema);
