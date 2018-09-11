//重写console.log,意义能够做一些事
console.log = (function(oriLogFunc){
    return function(){
    	//这里,或者是更外层你可以做一些其他事
        oriLogFunc.apply(null,Array.prototype.slice.call(arguments));
    }
})(console.log);
//利用a标签解析url(一般也用不到这么复杂的方法,location提供的方法就够了)
function parseURL(url) {
    var a =  document.createElement('a');
    a.href = url;
    return {
        source: url,
        protocol: a.protocol.replace(':',''),
        host: a.hostname,
        port: a.port||'80',
        query: a.search,
        params: (function(){
            var ret = {},
                seg = a.search.replace(/^\?/,'').split('&'),
                len = seg.length, i = 0, s;
            for (;i<len;i++) {
                if (!seg[i]) { continue; }
                s = seg[i].split('=');
                ret[s[0]] = s[1];
            }
            return ret;
        })(),
        file: (a.pathname.match(/\/([^\/?#]+)$/i) || [,''])[1],
        hash: a.hash.replace('#',''),
        path: a.pathname.replace(/^([^\/])/,'/$1'),
        relative: (a.href.match(/tps?:\/\/[^\/]+(.+)/) || [,''])[1],
        segments: a.pathname.replace(/^\//,'').split('/')
    };
}
//es6,数组去重,仅限于数组均为数值类型
function dedupe(array) {
  return Array.from(new Set(array));
}
dedupe([1, 1, 2, 3]) // [1, 2, 3]
/**
 * 判断两个版本字符串的大小
 * @param  {string} v1 原始版本
 * @param  {string} v2 目标版本
 * @return {number}    如果原始版本大于目标版本，则返回大于0的数值, 如果原始小于目标版本则返回小于0的数值。0当然是两个版本都相等拉。
 */
 
function compareVersion(v1, v2) {
    var _v1 = v1.split("."),
        _v2 = v2.split("."),
        _r = _v1[0] - _v2[0];
 
    return _r == 0 && v1 != v2 ? compareVersion(_v1.splice(1).join("."), _v2.splice(1).join(".")) : _r;
}
console.log(compareVersion("1.2.33.6", "1.2.33.6.7")); //-7
console.log(compareVersion("1.0", "1.0.1")); //-1
console.log(compareVersion("1.0", "0.0.5")); //1

//数字三位一切割
'223231312213123'.replace(/(\d)(?=(\d{3})+$)/g, "$1,"); //223,231,312,213,123

//去掉元素最后一位
'1234567'.slice(0,-1);

//图片转成base64图片,首先,你需要有一个input
document.querySelector('#testFile').onchange = function(){
    var reader = new FileReader();
    reader.readAsDataURL(this.files[0]);
    reader.onload = function(evt){
        document.querySelector('.call-back').innerHTML = '生成地址：'+evt.target.result;
        document.querySelector('.view-img').setAttribute('src',evt.target.result);
    }
}
//中英文混排,给中文加对应的样式,相关思路可扩展到其他地方
function change(anystring) {
    return anystring.replace(/([\u0391-\uFFE5]+)/ig, "<span class=\"cn\">$1<\/span>");
}
//检测设白IOS还是安卓
function checkOs(){
    var ua = navigator.userAgent.toLowerCase()
    var Exp_USERAGENT = {
        MicroMessenger :/micromessenger/i,//
        IOS : /(i(?:pad|phone|pod))(?:.*)cpu(?: i(?:pad|phone|pod))? os (\d+(?:[\.|_]\d+){1,})/,
        ANDROID : /(android)\s+([\d.]+)/,
        IPAD : /(ipad).*os\s([\d_]+)/,
        IPHONE : /(iphone\sos)\s([\d_]+)/,
    };
    var os = {},
    ipad = ua.match(Exp_USERAGENT.IPAD),        
    ios = ua.match(Exp_USERAGENT.IOS),
    iphone = !ipad && ua.match(Exp_USERAGENT.IPHONE),
    android = ua.match(Exp_USERAGENT.ANDROID);
    if (android){
        os.device = 'android',os.version = android[2]
    }else if (iphone){
        os.device = 'iphone',os.version = iphone[2].replace(/_/g, '.')
    }else{
        os.device = 'other',os.version=''
    }
    //weixin 
    if(Exp_USERAGENT.MicroMessenger.test(ua)){
        os.weixin=true;
    }else{
        os.weixin=false;
    }
    return os;
}
//获取url中的参数值
function getQueryString(name,noUnescape,customUrl){   
    var reg = new RegExp("(^|&)" + name + "=([^&]*)(&|$)",'i'); //构造一个含有目标参数的正则表达式对象
    var urlSearch = customUrl ? customUrl : window.location.search.substr(1); //判断是否有自定义url，没有的话去当前url的search。
    var r = urlSearch.match(reg);  //匹配目标参数
    if (r != null){
        if(!noUnescape){
            return unescape(r[2]);
        }else{
            return decodeURI(r[2]);
        }       
    }else{
        return ''; //返回参数值
    }
}
//简单的提示框,当前这样入参不太合适,最好修改成对象
function message(textMes,callback,timer){//弹窗函数
    if(!!document.querySelectorAll('#codetip').length) return false;
    //创建外部dom
    var codeTip = document.createElement('div');
    timer = timer || 2000;
    codeTip.id = 'codetip';
    codeTip.className = 'ep-code-tip-wrapper';
    //创建内部dom
    var codeTipInner = document.createElement('p');
    codeTipInner.innerHTML = textMes;
    codeTipInner.className = 'ep-code-tip-inner';
    //插入元素
    codeTip.appendChild(codeTipInner);
    var cssStyle = '.ep-code-tip-wrapper{position:fixed;left:10%;right:10%;top:200px;width:80%;text-align:center;font-size:16px;z-index:15;}\
    .ep-code-tip-inner{color:#fff;display:inline-block;line-height:24px;padding:8px 20px;background:#000;border-radius:5px;opacity:.8;}';
    createStyleDom(cssStyle);
    document.body.appendChild(codeTip);
    //倒计时移除元素
    setTimeout(function(){
        document.body.removeChild(document.querySelectorAll('#codetip')[0]);
        !!callback && callback();
    },timer);
}
function confirmWin(options){
    if(!!document.querySelectorAll('#epConfirm').length) return false;
    //创建外部dom
    var epConfirm = document.createElement('div');
    epConfirm.id = 'epConfirm';
    epConfirm.className = 'ep-confirm-wrapper';
    //创建confirmDes的文字描述区域
    var epConfirmDes = document.createElement('div');
    epConfirmDes.id = 'confirmDes';
    epConfirmDes.className = 'ep-confirm-des';
    epConfirmDes.innerHTML = options.text;
    //创建按钮区域
    var epConfirmBtn = document.createElement('div');
    epConfirmBtn.id = 'confirmSelect';
    epConfirmBtn.className = 'ep-confirm-select';
    //创建按钮区域
    var confirmSelectCancel = document.createElement('div');
    confirmSelectCancel.id = 'confirmSelectCancel';
    confirmSelectCancel.className = 'ep-confirm-select-cancel';
    confirmSelectCancel.innerText = options.cancelText;
    confirmSelectCancel.onclick = function(){
        if(options.callback){
            options.callback();
        }else{
            document.body.removeChild(document.querySelectorAll('#epConfirm')[0]);
            document.body.removeChild(document.querySelectorAll('#epMask')[0]);
        }
    }
    //创建按钮区域
    var confirmSelectSure = document.createElement('div');
    confirmSelectSure.id = 'confirmSelectSure';
    confirmSelectSure.className = 'ep-confirm-select-sure';
    confirmSelectSure.innerText = options.cancelSure;
    confirmSelectSure.onclick = function(){
        if(options.mCallBack){
            options.mCallBack();
        }else{
            document.body.removeChild(document.querySelectorAll('#epConfirm')[0]);
            document.body.removeChild(document.querySelectorAll('#epMask')[0]);
        }
    }
    //右上角的关闭弹层X号
    if(options.showClose){
        var closeConfirm = document.createElement('div');
        closeConfirm.id = 'closeConfirm';
        closeConfirm.className = 'ep-close-confirm';
        closeConfirm.innerText = '×';
        closeConfirm.onclick = function(){
            document.body.removeChild(document.querySelectorAll('#epConfirm')[0]);
            document.body.removeChild(document.querySelectorAll('#epMask')[0]);
        }
        epConfirm.appendChild(closeConfirm);
    }
    //隐藏层
    var epMask = document.createElement('div');
    epMask.id = 'epMask';
    epMask.className = 'ep-confirm-mask';
    //判断是否是有双按钮
    if(options.cancelText){
        epConfirmBtn.appendChild(confirmSelectCancel);
    }else{
        confirmSelectSure.className = 'ep-confirm-select-sure single';
    }
    //判断若是有title,显示title
    if(options.epConfirmTitle){
        var epConfirmTitle = document.createElement('h3');
        epConfirmTitle.innerText = options.epConfirmTitle;
        epConfirm.appendChild(epConfirmTitle);
    }
    //创建style标签
    var cssStyle = '.ep-confirm-wrapper{position:fixed;z-index:500;top:200px;left:50%;margin-left:-140px;width:280px;background-color:rgb(255,255,255);text-align:center;border-radius:5px;}\
    .ep-confirm-des{padding:20px;line-height:24px;font-size:14px;}\
    .ep-confirm-select{height:40px;line-height:40px;font-size:14px;border-top:1px solid rgb(221,221,221);}\
    .ep-confirm-select-sure{width:50%;float:right;color:#41aaf2;}\
    .ep-confirm-select-sure.single{width:100%;}\
    .ep-confirm-select-cancel{width:50%;float:left;border-right:1px solid #ddd;color:#41aaf2;box-sizing:border-box;-webkit-box-sizng:border-box;}\
    .ep-close-confirm{width:40px;position:absolute;top:0;right:0;color:#999;font-size:26px;}\
    .ep-confirm-mask{position:fixed;bottom:0;top:0;left:0;right:0;background:rgba(0,0,0,.5);}\
    .ep-confirm-title{width:100%;padding-top:14px;color:#333;font-size:18px;font-weight:bold;}';
    EP.createStyleDom(cssStyle);
    epConfirmBtn.appendChild(confirmSelectSure);
    epConfirm.appendChild(epConfirmDes);
    epConfirm.appendChild(epConfirmBtn);
    document.body.appendChild(epConfirm);
    document.body.appendChild(epMask);
}
//判断对象是否为空
function isEmptyObject(e) {  
    var t;  
    for (t in e)  
        return !1;  
    return !0  
}
//手机号替换正则,可扩展到其他很多需要分割替换的场景
'12345678901'.replace(/(\d{3})\d{4}(\d{4})/, '$1****$2');
//XMLHttpRequest发送ajax请求的简单示例(不考虑兼容性问题)
function sendAjax() {
    //构造表单数据
    var formData = new FormData();
    formData.append('username', 'duanzhihe');
    formData.append('id', 123456);
    //创建xhr对象 
    var xhr = new XMLHttpRequest();
    //设置xhr请求的超时时间
    xhr.timeout = 3000;
    //设置响应返回的数据格式
    xhr.responseType = "text";
    //创建一个 post 请求，采用异步
    xhr.open('POST', '/server', true);
    //注册相关事件回调处理函数
    xhr.onload = function(e) { 
    if(this.status == 200||this.status == 304){
        alert(this.responseText);
    }
    };
    xhr.ontimeout = function(e) { ... };
    xhr.onerror = function(e) { ... };
    xhr.upload.onprogress = function(e) { ... };
    //发送数据
    xhr.send(formData);
}
//封装一个防止重复点击的方法,一个参数是表示防止重复点击的唯一hash标示,一个是回掉函数
var repeatedClicksContainer = {}
function preventRepeatedClick(domHash,callback){ //防止重复点击事件
    if(repeatedClicksContainer.hasOwnProperty(domHash)){
        window.repeatedClicksTimer && clearTimeout(repeatedClicksTimer)
    }else{
        repeatedClicksContainer[domHash] = true;
        callback();
    }
    window.repeatedClicksTimer = setTimeout(function(){
        delete repeatedClicksContainer[domHash];
    },300)
}
//插入style标签
function createStyleDom(cssStyle){
    var loadStyleDom = document.createElement('style');
    loadStyleDom.type = 'text/css';
    loadStyleDom.innerHTML = cssStyle;
    document.getElementsByTagName('head')[0].appendChild(loadStyleDom);
}
//loading效果图
var gobalLoading = {
    show : function(){
        if (!!document.querySelector('#epShowLoading')) return false;
        //创建外部dom
        var epShowLoading = document.createElement('div');
        epShowLoading.id = 'epShowLoading';
        epShowLoading.className = 'ep-show-loading';
        //创建循环区块
        var loaders = document.createElement('div');
        loaders.className = 'ep-loaders';
        for (var i = 0; i < 8; i++) {
            loaders.appendChild(document.createElement('div'))
        }
        var loaderWrapper = document.createElement('div');
        loaderWrapper.className = 'ep-loader-wrapper';
        //插入dom
        loaderWrapper.appendChild(loaders);
        epShowLoading.appendChild(loaderWrapper);
        //创建样式
        var cssStyle = '.ep-show-loading{width: 100px; height: 120px; position: absolute; z-index: 999;top: 32%;left: 38%;right: 38%;}\
        .ep-show-loading .ep-loader-wrapper{transition: opacity .25s linear;opacity: 1;width: 20%;max-width: 1000px;margin: 4em auto;}\
        .ep-show-loading .ep-loaders{position: relative;}\
        .ep-show-loading .ep-loaders > div{ background-color: #fff;width: 15px;height: 15px;border-radius: 100%;margin: 2px;-webkit-animation-fill-mode: both;animation-fill-mode: both;position: absolute;}\
        .ep-show-loading .ep-loaders > div:nth-child(1){ top: 25px;left: 0;-webkit-animation: ball-spin-fade-loader 1s 0s infinite linear;animation: ball-spin-fade-loader 1s 0s infinite linear;}\
        .ep-show-loading .ep-loaders > div:nth-child(2){ top: 17.04545px;left: 17.04545px;-webkit-animation: ball-spin-fade-loader 1s 0.12s infinite linear;animation: ball-spin-fade-loader 1s 0.12s infinite linear;}\
        .ep-show-loading .ep-loaders > div:nth-child(3){ top: 0;left: 25px;-webkit-animation: ball-spin-fade-loader 1s 0.24s infinite linear;animation: ball-spin-fade-loader 1s 0.24s infinite linear;}\
        .ep-show-loading .ep-loaders > div:nth-child(4){ top: -17.04545px;left: 17.04545px;-webkit-animation: ball-spin-fade-loader 1s 0.36s infinite linear;animation: ball-spin-fade-loader 1s 0.36s infinite linear;}\
        .ep-show-loading .ep-loaders > div:nth-child(5){ top: -25px;left: 0;-webkit-animation: ball-spin-fade-loader 1s 0.48s infinite linear;animation: ball-spin-fade-loader 1s 0.48s infinite linear;}\
        .ep-show-loading .ep-loaders > div:nth-child(6){ top: -17.04545px;left: -17.04545px;-webkit-animation: ball-spin-fade-loader 1s 0.6s infinite linear;animation: ball-spin-fade-loader 1s 0.6s infinite linear;}\
        .ep-show-loading .ep-loaders > div:nth-child(7){ top: 0;left: -25px;-webkit-animation: ball-spin-fade-loader 1s 0.72s infinite linear;animation: ball-spin-fade-loader 1s 0.72s infinite linear;}\
        .ep-show-loading .ep-loaders > div:nth-child(8){ top: 17.04545px;left: -17.04545px;-webkit-animation: ball-spin-fade-loader 1s 0.84s infinite linear;animation: ball-spin-fade-loader 1s 0.84s infinite linear;}\
        @-webkit-keyframes ball-spin-fade-loader{50% {opacity: 0.3;-webkit-transform: scale(0.4);transform: scale(0.4);}100% {opacity: 1;-webkit-transform: scale(1);transform: scale(1);}}\
        @keyframes ball-spin-fade-loader{50% {opacity: 0.3;-webkit-transform: scale(0.4);transform: scale(0.4);}100% {opacity: 1;-webkit-transform: scale(1);transform: scale(1);}}\
        .ep-loading-mask{position: fixed;top: 0;left: 0;bottom: 0;right: 0;background-color: #000;opacity: 0.8;z-index: 10;}'
        createStyleDom(cssStyle);
        //创建mask
        var epLoadingMask = document.createElement('div');
        epLoadingMask.id = 'eploadingMask';
        epLoadingMask.className = 'ep-loading-mask';
        //插入到body
        document.body.appendChild(epShowLoading);
        document.body.appendChild(epLoadingMask);
    }
    hide : function(){
        if(!!document.querySelector('#epShowLoading')){
            document.body.removeChild(document.querySelector('#epShowLoading'))
            document.body.removeChild(document.querySelector('#eploadingMask'))
        }
    }
}
//去掉数组空元素
[undefined,undefined,1,'','false',false,true,null,'null'].filter(d=>d);
//横屏检测
function checkHorizontalScreen checkHorizontalScreen(){
    function landscapePrompt(){
        //创建外围的dom
        var promptDom = document.createElement('div');
            promptDom.id = 'epOutlandscapePrompt';
        //常见内dom
        var promptInnerDom = document.createElement('div');
            promptInnerDom.id = 'epInnerlandscapePrompt';
        //创建提示的图片
        var promptImgDom = document.createElement('img');
            promptImgDom.id = 'epOutlandscapeImgPrompt';
            promptImgDom.src = 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAIYAAADaCAMAAABU68ovAAAAXVBMVEUAAAD29vb////x8fH////////x8fH5+fn29vby8vL////5+fn39/f6+vr////x8fH////////+/v7////09PT////x8fH39/f////////////////////x8fH///+WLTLGAAAAHXRSTlMAIpML+gb4ZhHWn1c2gvHBvq1uKJcC6k8b187lQ9yhhboAAAQYSURBVHja7d3blpowFIDhTUIAOchZDkre/zE7ycySrbUUpsRN2/1fzO18KzEqxEVgTiZNfgmmtxRc8iaR8HNe8x4BtjQePKayYCIoyBSgvNNE1AkNSHqZyLqk97EgUCCHBzZ5mkg7ScvIJuIyOyXBRFxgpqWZyGsAZLB1KjsJi8nutHU4JCRbFRH8tmirI9k8Jx2sqNs8K/m0LQkrktO2crgcgXGB4AiTEsB0hJfo9MGgX7CGcYiYwQxmMOOvZwRhBG8tCoMXjBDeXvWCEcHbi14wgCBmMIMZzGAGM5jxETNwzMAxA8cMHDNwzMAxA8cMHDNwzMAxA8cMHDNwzMAxY6E2rUQxnH2tz9cirlJFwFBJedaPnUv0M7++egPDE8iAJcIDmxwH5wwv9vUviw2kLbVO3TJU5uul/EyB0FoLp4x60PdGUd3qPurrWyjGGTc05u+1dcgI7/+tCCPARWGhH7o5Y7RCf+bH9ctXLp6v2BVDxfqz0oPXeSVaNtINo/1SXDv4dck8IIkbhtC2ol+iouEonTBCbYvVMnXOjxww6s/RFrBUpXHh/gw1rHj5d/qhYn9Gpk2FWh6xRBRX5Oj3Znh2Sq49/L6+y8pB26q9GbE2dbA2mVbx6I+7MfBglLCttm73ZQi7AD3iL4HqjFYJHSPRppqaUaJ3ATpGa+ckpGak2hRRMyqjGMkvl+xyFeSMwjAqcsZgGDdyhl0oNTnDN4yenJGZFGxNChP5/Y3efh6SM2rDOJMzboYxkDMqwyjIGcIw6F+io2FU1IxIm1JqRmgXSkvNKNCXeTpGrU0JNSO2c6LIGPgCS8AuDHz9ta0SXWDtxoDRH+MqlbC2Dt2G2JFRadtQZt2qq/orGowdGb2euxYiqWEpVWhTBnszoNAPdStuQwxqf0aocdWKW4Z+DfszIh8pxJqbuCE4YAC+4bm0evtipjpgJHeFnyyt1Ku2xa0bhjxr27p75rECNwyI9ZwvXkHq+7aTaMEV44YYy/spfgjgjNHaWW+GeUhGEX7tLlVinIFDDSgnOwhi1V6bU0b6tVS9eAERe863g4dRrtiHdc6o+nn5vtyVVgR79Cqt4uL6gfHPQyGqtP2vf7HADGbcYwaOGThm4JiBYwaOGThm4JiBYwaOGThm4JiBYwaOGThm4JiBYwaOGThm4JjhtOM+J/AgT008yDMkN/dPP9hzS8zAMQN3OEYeekp5YU7KOKXwVXqiY+QS7smcinGKABWdiBgpPJTSMHJ4KidhhPBUSMLw4CmPhKHgKUXCkHsygum71ftNSgCX6bsl8FQyfbcL5EdYsDk0R3j7aiA5wpt5AjKg/2gLJEBD/0Hf2OOf/vRrj6z/7GtP4B3nMKyjHA12kIPSjnJs3FEO0TvKkYJHOWCR+rjJH0Vn6fI5PjNbAAAAAElFTkSuQmCC';
        //创建文案
        var promptDesDom = document.createElement('p');
            promptDesDom.id = 'epOutlandscapeDesPrompt';
            promptDesDom.innerText = '为了更好的体验，请使用竖屏浏览';
        //创建提示动画的style标签
        var cssStyle = '#epOutlandscapePrompt{position:fixed;top:0;bottom:0;left:0;right:0;background:#000;z-index:9999;}\
            #epInnerlandscapePrompt{position:absolute;width:100%;top:45%;margin-top:-75px;text-align:center;}\
            #epOutlandscapeImgPrompt{width:67px;height:109px;transform:rotate(90deg);-webkit-transform:rotate(90deg);animation:landscapeRotation infinite 1.5s ease-in-out;-webkit-animation:landscapeRotation infinite 1.5s ease-in-out;}\
            #epOutlandscapeDesPrompt{margin-top:20px;font-size:15px;color:#fff;}\
            @keyframes landscapeRotation{10%{transform:rotate(90deg);-webkit-transform:rotate(90deg)}50%{transform:rotate(0);-webkit-transform:rotate(0)}60%{transform:rotate(0);-webkit-transform:rotate(0)}90%{transform:rotate(90deg);-webkit-transform:rotate(90deg)}100%{transform:rotate(90deg);-webkit-transform:rotate(90deg)}}@-webkit-keyframes landscapeRotation{10%{transform:rotate(90deg);-webkit-transform:rotate(90deg)}50%{transform:rotate(0);-webkit-transform:rotate(0)}60%{transform:rotate(0);-webkit-transform:rotate(0)}90%{transform:rotate(90deg);-webkit-transform:rotate(90deg)}100%{transform:rotate(90deg);-webkit-transform:rotate(90deg)}}';
        EP.createStyleDom(cssStyle);
        //进行元素合并插入
        promptInnerDom.appendChild(promptImgDom);
        promptInnerDom.appendChild(promptDesDom);
        promptDom.appendChild(promptInnerDom);
        document.body.appendChild(promptDom);
    }
    function removeLandscapePrompt(){
        if(document.querySelector('#epOutlandscapePrompt')){
            document.body.removeChild(document.querySelector('#epOutlandscapePrompt'));
        }
    }
    function detectOrient() {
        var contextW = document.documentElement.clientWidth,
            contextH = document.documentElement.clientHeight;
        var screenW = window.screen.width,
            screenH = window.screen.height;
        if (contextW == screenH) {
            landscapePrompt();
        }else{
            removeLandscapePrompt()
        }
    }
    detectOrient();
    window.addEventListener('resize', detectOrient);
}
