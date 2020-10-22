// 模型
var serv = require("../routes/api/ids_log");
const mongoose = require("mongoose");
const Schema = mongoose.Schema;//实例化Schema

// 各个模型 Schema
const LOGINSchema = new Schema({
    time: [Number],
    data: [Number]
}, {collection: 'login_time'})
// 输出
const LOGIN_data = module.exports = serv.mon_min.model("login_time",LOGINSchema);
