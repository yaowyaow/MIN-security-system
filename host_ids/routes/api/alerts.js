// @login & register npm node.js
const express = require("express");//表达
const router = express.Router();//路由
const passport = require("passport");
const mysql = require('mysql');
const models = require('../../config/db');


var conn = mysql.createConnection(models.mysql);

conn.connect();

// $route get api/alerts
// @desc 获取所有的信息
// @access Privte
router.get("/",passport.authenticate("jwt",{session:false}),(req,res) =>{
	conn.query('SELECT a.id,a.location_id,a.level,a.full_log,a.timestamp,b.hostname,c.name,(SELECT GROUP_CONCAT(d.cat_name) from category d WHERE d.cat_id in (select e.cat_id from signature_category_mapping e where e.rule_id =a.rule_id))cat_name FROM alert a,server b,location c  WHERE a.server_id = b.id and a.location_id = c.id order by id desc limit 100',function(error,result){
        if(error) throw error;
        console.log('数据库操作成功');
        res.json(result);
    });
})
// $route get api/alerts/detail/:id
// @desc 获取单个信息
// @access Privte
router.get("/detail",passport.authenticate("jwt",{session:false}),(req,res) =>{
    let deta=`SELECT FROM alert where id= `+ req.body.id;
    conn.query(deta,null,function(error,result){
        if(error) throw error;
        console.log('数据库操作成功');
        res.json(result);
    });
})
// $route post api/alerts/delete/:id
// @desc 删除接口
// @access Privte 
router.use("/delete",passport.authenticate("jwt",{session:false}),(req,res) =>{
    console.log(req.body.id);
    let del=`DELETE FROM alert where id= `+ req.body.id;
    conn.query(del,null,function(err,rows){
        if(err){
            res.json({
            ok:false,
            message:'删除失败',
            error:err
            })
        }
        else{
           res.json({
               ok:true,
               message:'删除成功'
           })
        }
        res.end;
    });
})

module.exports = router; // 报错



    
    
