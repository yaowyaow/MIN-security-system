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
const MapSchema = new Schema({
    destLocX:{
        type:Number,
	required:true
    },
    destLocY:{
        type:Number,
	required:true
        
    },
    srcPort:{
        type:Number,
        required:true
    },
    srcLocX:{
        type:Number,
	required:true
    },
    srcLocY:{
        type:Number,
        required:true
    },
    srcName:{
        type:String,
    },
    destIp:{
        type:String,
    },
    time:{
	type:String,
    },
    srcIp:{
	type:String,
    },
    type:{
        type:String,
    },
    destName:{
        type:String   
    }
 },{collection: 'SA_event'})
// 输出
const SA_event = module.exports = mon_sa.model("SA_event",MapSchema);
