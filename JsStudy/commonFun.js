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
    codeTip.style.position = 'fixed';
    codeTip.style.left = '10%';
    codeTip.style.right = '10%';
    codeTip.style.top = '200px';
    codeTip.style.width = '80%';
    codeTip.style.textAlign = 'center';
    codeTip.style.fontSize = '16px';
    codeTip.style.zIndex = '15';
    //创建内部dom
    var codeTipInner = document.createElement('p');
    codeTipInner.style.color = '#fff';
    codeTipInner.style.display = 'inline-block';
    codeTipInner.style.lineHeight = '24px';
    codeTipInner.style.padding = '20px';
    codeTipInner.style.background = '#000';
    codeTipInner.style.borderRadius = '5px';
    codeTipInner.style.opacity = '.8';
    codeTipInner.innerHTML = textMes;
    //插入元素
    codeTip.appendChild(codeTipInner);
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
    epConfirm.style.position = 'fixed';
    epConfirm.style.zIndex = '500';
    epConfirm.style.top = '200px';
    epConfirm.style.left = '50%';
    epConfirm.style.marginLeft = '-140px';
    epConfirm.style.width = '280px';
    epConfirm.style.backgroundColor = '#fff';
    epConfirm.style.textAlign = 'center';
    epConfirm.style.borderRadius = '5px';
    //创建confirmDes的文字描述区域
    var epConfirmDes = document.createElement('div');
    epConfirmDes.id = 'confirmDes';
    epConfirmDes.style.padding = '20px';
    epConfirmDes.style.lineHeight = '24px';
    epConfirmDes.style.fontSize = '14px';
    epConfirmDes.innerHTML = options.text;
    //创建按钮区域
    var epConfirmBtn = document.createElement('div');
    epConfirmBtn.id = 'confirmSelect';
    epConfirmBtn.style.height = '40px';
    epConfirmBtn.style.lineHeight = '40px';
    epConfirmBtn.style.fontSize = '14px';
    epConfirmBtn.style.borderTop = '1px solid #ddd';
    //创建按钮区域
    var confirmSelectCancel = document.createElement('div');
    confirmSelectCancel.id = 'confirmSelectCancel';
    confirmSelectCancel.style.width = '50%';
    confirmSelectCancel.style.float = 'left';
    confirmSelectCancel.style.borderRight = '1px solid #ddd';
    confirmSelectCancel.style.boxSizing = 'border-box';
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
    confirmSelectSure.style.width = '50%';
    confirmSelectSure.style.float = 'right';
    confirmSelectSure.style.color = '#41aaf2';
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
        closeConfirm.style.width = '40px';
        closeConfirm.style.position = 'absolute';
        closeConfirm.style.top = '0';
        closeConfirm.style.right = '0';
        closeConfirm.style.color = '#999';
        closeConfirm.style.fontSize = '26px';
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
    epMask.style.position = 'fixed';
    epMask.style.bottom = '0';
    epMask.style.top = '0';
    epMask.style.left = '0';
    epMask.style.right = '0';
    epMask.style.background = 'rgba(0,0,0,.5)';
    //判断是否是有双按钮
    if(options.cancelText){
        epConfirmBtn.appendChild(confirmSelectCancel);
    }else{
        confirmSelectSure.style.width = '100%';
    }
    //判断若是有title,显示title
    if(options.epConfirmTitle){
        var epConfirmTitle = document.createElement('h3');
        epConfirmTitle.id = 'epConfirmTitle';
        epConfirmTitle.style.width = '100%';
        epConfirmTitle.style.paddingTop = '14px';
        epConfirmTitle.style.color = '#333';
        epConfirmTitle.style.fontSize = '18px';
        epConfirmTitle.style.fontWeight = 'bold';
        epConfirmTitle.innerText = options.epConfirmTitle;
        epConfirm.appendChild(epConfirmTitle);
    }
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
//loading效果图
var gobalLoading = {
    show : function(){
        if(!!document.querySelector('#epShowLoading')) return false;
        //创建外部dom
        var epShowLoading = document.createElement('div');
        epShowLoading.id = 'epShowLoading';
        epShowLoading.className = 'ep-show-loading';

        //创建循环区块
        var loaders = document.createElement('div');
        loaders.className = 'ep-loaders';
        for(var i = 0; i < 8; i ++){
            loaders.appendChild(document.createElement('div'))
        }
        var loaderWrapper = document.createElement('div');
        loaderWrapper.className = 'ep-loader-wrapper';

        loaderWrapper.appendChild(loaders);
        epShowLoading.appendChild(loaderWrapper);

        //创建mask层
        var epLoadingMask = document.createElement('div');
        epLoadingMask.id = 'eploadingMask';
        epLoadingMask.className = 'ep-loading-mask';

        document.body.appendChild(epShowLoading);
        document.body.appendChild(epLoadingMask);
        //创建样式
        var loadStyleDom = document.createElement('style');
        loadStyleDom.type = 'text/css';
        var _style_ = new Array();
        _style_.push('.ep-show-loading{width: 100px; height: 120px; position: absolute; z-index: 999;top: 32%;left: 38%;right: 38%;}');
        _style_.push('.ep-show-loading .ep-loader-wrapper{transition: opacity .25s linear;opacity: 1;width: 20%;max-width: 1000px;margin: 4em auto;}')
        _style_.push('.ep-show-loading .ep-loaders{position: relative;}');
        _style_.push('.ep-show-loading .ep-loaders > div{ background-color: #fff;width: 15px;height: 15px;border-radius: 100%;margin: 2px;-webkit-animation-fill-mode: both;animation-fill-mode: both;position: absolute;}')
        _style_.push('.ep-show-loading .ep-loaders > div:nth-child(1){ top: 25px;left: 0;-webkit-animation: ball-spin-fade-loader 1s 0s infinite linear;animation: ball-spin-fade-loader 1s 0s infinite linear;}')
        _style_.push('.ep-show-loading .ep-loaders > div:nth-child(2){ top: 17.04545px;left: 17.04545px;-webkit-animation: ball-spin-fade-loader 1s 0.12s infinite linear;animation: ball-spin-fade-loader 1s 0.12s infinite linear;}')
        _style_.push('.ep-show-loading .ep-loaders > div:nth-child(3){ top: 0;left: 25px;-webkit-animation: ball-spin-fade-loader 1s 0.24s infinite linear;animation: ball-spin-fade-loader 1s 0.24s infinite linear;}')
        _style_.push('.ep-show-loading .ep-loaders > div:nth-child(4){ top: -17.04545px;left: 17.04545px;-webkit-animation: ball-spin-fade-loader 1s 0.36s infinite linear;animation: ball-spin-fade-loader 1s 0.36s infinite linear;}')
        _style_.push('.ep-show-loading .ep-loaders > div:nth-child(5){ top: -25px;left: 0;-webkit-animation: ball-spin-fade-loader 1s 0.48s infinite linear;animation: ball-spin-fade-loader 1s 0.48s infinite linear;}')
        _style_.push('.ep-show-loading .ep-loaders > div:nth-child(6){ top: -17.04545px;left: -17.04545px;-webkit-animation: ball-spin-fade-loader 1s 0.6s infinite linear;animation: ball-spin-fade-loader 1s 0.6s infinite linear;}')
        _style_.push('.ep-show-loading .ep-loaders > div:nth-child(7){ top: 0;left: -25px;-webkit-animation: ball-spin-fade-loader 1s 0.72s infinite linear;animation: ball-spin-fade-loader 1s 0.72s infinite linear;}')
        _style_.push('.ep-show-loading .ep-loaders > div:nth-child(8){ top: 17.04545px;left: -17.04545px;-webkit-animation: ball-spin-fade-loader 1s 0.84s infinite linear;animation: ball-spin-fade-loader 1s 0.84s infinite linear;}')
        _style_.push('@-webkit-keyframes ball-spin-fade-loader{50% {opacity: 0.3;-webkit-transform: scale(0.4);transform: scale(0.4);}100% {opacity: 1;-webkit-transform: scale(1);transform: scale(1);}}')
        _style_.push('@keyframes ball-spin-fade-loader{50% {opacity: 0.3;-webkit-transform: scale(0.4);transform: scale(0.4);}100% {opacity: 1;-webkit-transform: scale(1);transform: scale(1);}}')
        _style_.push('.ep-loading-mask{position: fixed;top: 0;left: 0;bottom: 0;right: 0;background-color: #000;opacity: 0.8;z-index: 10;}')
        loadStyleDom.innerHTML= _style_.join('');
        document.getElementsByTagName('head')[0].appendChild(loadStyleDom);
    }
    hide : function(){
        if(!!document.querySelector('#epShowLoading')){
            document.body.removeChild(document.querySelector('#epShowLoading'))
            document.body.removeChild(document.querySelector('#eploadingMask'))
        }
    }
}
