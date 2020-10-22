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
const HvalueSchema = new Schema({
    value:{
        type:Number,
        required:true
    },
    time:{
        type:String
    }
 },{collection: 'SA_host_value'})
// 输出
const SA_host_value = module.exports = mon_sa.model("SA_host_value",HvalueSchema);
