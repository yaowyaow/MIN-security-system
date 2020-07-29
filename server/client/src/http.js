
import axios from 'axios';
import {Message, Loading } from 'element-ui';
import router from './router';

let loading;//变量
//方法
function starLoding (){
    loading = Loading.service({
        //对象
        lock:true,
        text:'拼命加载中...',
        background:'rgba(0,0,0,0,7)'
    });
}


function endLoading(){
    loading.close();
}


// //请求拦截
axios.interceptors.request.use(
    config => {
        //加载动画
        starLoding();
        // 判断
        if(localStorage.eleToken){
            // 设置统一的请求header 头
            config.headers.Authorization = localStorage.eleToken;
        }
        // 
        return config;
    },
    error =>{
        return Promise.reject(error);
    }
)
// //响应拦截
axios.interceptors.response.use(response => {
    //结束加载动画
    endLoading();
    return response;
    },
    error =>{
        //错误提示
        endLoading();
        Message.error(error.response.data);

        // 获取错误状态码
        const {status} = error.response;
        if(status == 401){
            Message.error('token失效，请重新登录！');
            // 清除token
            localStorage.removeItem("eleToken");
            // 跳转登录页面
            router.push("/login");
        }
        return Promise.reject(error);
    }
)

export default axios;


