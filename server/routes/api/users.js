// @login & register npm node.js
const express = require("express");//表达
const router = express.Router();//路由
const bcrypt = require("bcrypt");//引用bcrypt
const gravatar = require('gravatar');//npm  gravatar

const mongoose = require("mongoose");

var mon_min = mongoose
  .createConnection(
   "mongodb://pkusz:pkusz@localhost:27017/Situation_Awareness?authSource=admin",
    { useNewUrlParser: true}
  );



module.exports.mon_min = mon_min;

const User = require("../../modeis/User");//引用
const jwt = require('jsonwebtoken');//引用 jsonwebtoken
const keys = require("../../config/keys");//加密名字keys.secretOrKey 引用
const passport = require("passport");



// $route get api/users/test
// @desc 返回的请求json
// @access public
router.get("/test",(req,res) => {
    // 打印返回一句话
    res.json({msg:"login works"})
})

// $route post api/users/register
// @desc 返回的请求json
// @access public
router.post("/register",(req,res) => {
    // console.log(req.body);
    // 查询数据库中是否拥有邮箱
    User.findOne({email:req.body.email})
        .then((user) => {
            // 提示
            if(user){
                return res.status(400).json("邮箱已经被注册!")
            
            }else{
                // 头像使用 https://en.gravatar.com/
                const avatar = gravatar.url(req.body.email, {s: '200', r: 'pg', d: 'mm'});

                const newUser = new User({
                    name:req.body.name,
                    email:req.body.email,
                    avatar,
                    password:req.body.password,
                    identity:req.body.identity //增加管理员身份
                })
                // npm官网bcrypt
                bcrypt.genSalt(10, function(err, salt) {
                    bcrypt.hash(newUser.password, salt, function(err, hash) {
                        //判断
                        if(err) throw err;

                        newUser.password = hash;

                        newUser.save()//存储
                                .then(user => res.json(user))
                                .catch(err => console.log(err));//失败
                    });
                });
            }
            
        })
})

// $route post api/users/login
// @desc 返回的token jwt passport 
// @access public

router.post("/login",(req,res) =>{
    const email = req.body.email;
    const password = req.body.password;
    console.log(req.body);
    console.log(req.params);

    //查询数据库
    User.findOne({email})
        .then(user => { 
            if(!user){
                return res.status(404).json("用户不存在！");
            }
            //密码匹配
            bcrypt.compare(password,user.password)
                .then(isMatch => {
                    if(isMatch){
                        //成功
                        // 规则rule 加密名字keys.secretOrKey 过期时间expiresIn:3600 函数token
                        const rule  = {
                            id:user.id,
                            name:user.name,
                            avatar:user.avatar,
                            identity:user.identity //增加
                        };
                        jwt.sign(rule,keys.secretOrKey,{expiresIn:3600},(err,token) => {
                            if(err) throw err;//成功
                            //失败
                            res.json({
                                success:true,
                                token:"Bearer "+token //mrwu换Bearer空格
                            });
                        })
                        // res.json({msg:"success"})
                    }else{
                        return res.status(400).json( "密码错误！")
                    }
                })

                
                
            

        })
}) 

// $route get api/users/current 
// @desc retrun current user
// @access Private
router.get("/current",passport.authenticate("jwt",{session:false}),(req,res) => {
    res.json({
        // 返回数据给用户
        id:req.user.id,
        name:req.user.name,
        email:req.user.email,
        identity:req.user.identity
    });
    console.log(req.params);
})

module.exports = router;//报错

