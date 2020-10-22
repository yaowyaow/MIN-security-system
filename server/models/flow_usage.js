// 模型
var serv = require("../routes/api/ids_log");
const mongoose = require("mongoose");
const Schema = mongoose.Schema;//实例化Schema

let dict = {}
for(let i = 0; i < 24; i++){
    dict[i] = 'Number'
}
// 各个模型 Schema
const FLOWSchema = new Schema(dict, {collection: 'flow_usage'})
// 输出
const FLOW_data = module.exports = serv.mon_min.model("flow_usage",FLOWSchema);
