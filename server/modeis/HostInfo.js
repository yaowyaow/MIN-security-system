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
const HostInfoSchema = new Schema({
    Disk_Utilization:{
        type:Number,
        required:true
    },
    Cpu_Utilization:{
        type:Number,
        required:true
    },
    time:{
        type:String
    },
    Memory_Utilization:{
        type:Number,
        required:true
    },
    Boot_Time:{
        type:Number,
        required:true
    },
    Run_Time:{
        type:Number,
        required:true
    },
    Routing_NIC_Name:{
        type:String,
        required:true
    },
    Routing_NIC_MAC_Address:{
        type:String,
        required:true
    },
    Routing_Gateway:{
        type:String,
        required:true
    },
    Routing_IP_Netmask:{
        type:String,
        required:true
    },


 },{collection: 'HostInfo'})
// 输出
const HostInfo = module.exports = mon_sa.model("HostInfo",HostInfoSchema);
