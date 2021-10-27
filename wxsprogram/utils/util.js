//等额本息计算
var benxi = ( num, year, lilv) => {
    //每月月供额=〔贷款本金×月利率×(1＋月利率)＾还款月数〕÷〔(1＋月利率)＾还款月数-1〕
    var mouth = parseInt(year) * 12,
        mouthlilv = parseFloat(lilv) / 12,
        dknum = parseFloat(num) * 10000;
    //每月月供
    var yuegong = (dknum * mouthlilv * Math.pow((1 + mouthlilv), mouth)) / (Math.pow((1 + mouthlilv), mouth) - 1);
    //总利息=还款月数×每月月供额-贷款本金
    var totalLixi = mouth * yuegong - dknum;
    //还款总额 总利息+贷款本金
    var totalPrice = totalLixi + dknum,
        leftFund = totalLixi + dknum;

    //循环月份
    var mouthdataArray = [],
        nowmouth = new Date().getMonth(),
        realmonth = 0;

    for (var i = 1; i <= mouth; i++) {
        realmonth = nowmouth + i;
        var yearlist = Math.floor(i / 12);
        realmonth = realmonth - 12 * yearlist;
        if (realmonth > 12) {
            realmonth = realmonth - 12
        }
        //每月应还利息=贷款本金×月利率×〔(1+月利率)^还款月数-(1+月利率)^(还款月序号-1)〕÷〔(1+月利率)^还款月数-1〕
        var yuelixi = dknum * mouthlilv * (Math.pow((1 + mouthlilv), mouth) - Math.pow((1 + mouthlilv), i - 1)) / (Math.pow((1 + mouthlilv), mouth) - 1);
        //每月应还本金=贷款本金×月利率×(1+月利率)^(还款月序号-1)÷〔(1+月利率)^还款月数-1〕
        var yuebenjin = dknum * mouthlilv * Math.pow((1 + mouthlilv), i - 1) / (Math.pow((1 + mouthlilv), mouth) - 1);
        leftFund = leftFund - (yuelixi + yuebenjin);
        if (leftFund < 0) {
            leftFund = 0
        }
        mouthdataArray[i - 1] = {
            monthName: realmonth + "月",
            yuelixi: yuelixi,
            yuebenjin: yuebenjin,
            //剩余还款
            leftFund: leftFund
        }
    }
    return {
        yuegong: yuegong,
        totalLixi: totalLixi,
        totalPrice: totalPrice,
        mouthdataArray: mouthdataArray,
        totalDknum: num,
        year: year
    };
};
//等额本金计算
var benjin = ( num, year, lilv) => {
    var mouth = parseInt(year) * 12,
        mouthlilv = parseFloat(lilv) / 12,
        dknum = parseFloat(num) * 10000,
        yhbenjin = 0; //首月还款已还本金金额是0
    //每月应还本金=贷款本金÷还款月数
    var everymonthyh = dknum / mouth
        //每月月供额=(贷款本金÷还款月数)+(贷款本金-已归还本金累计额)×月利率
    var yuegong = everymonthyh + (dknum - yhbenjin) * mouthlilv;
    //每月月供递减额=每月应还本金×月利率=贷款本金÷还款月数×月利率
    var yuegongdijian = everymonthyh * mouthlilv;
    //总利息=〔(总贷款额÷还款月数+总贷款额×月利率)+总贷款额÷还款月数×(1+月利率)〕÷2×还款月数-总贷款额
    var totalLixi = ((everymonthyh + dknum * mouthlilv) + dknum / mouth * (1 + mouthlilv)) / 2 * mouth - dknum;
    //还款总额 总利息+贷款本金
    var totalPrice = totalLixi + dknum,
        leftFund = totalLixi + dknum;

    //循环月份
    var mouthdataArray = [],
        nowmouth = new Date().getMonth(),
        realmonth = 0;

    for (var i = 1; i <= mouth; i++) {
        realmonth = nowmouth + i;
        var yearlist = Math.floor(i / 12);

        realmonth = realmonth - 12 * yearlist;

        if (realmonth > 12) {
            realmonth = realmonth - 12
        }
        yhbenjin = everymonthyh * (i - 1);
        var yuebenjin = everymonthyh + (dknum - yhbenjin) * mouthlilv;
        //每月应还利息=剩余本金×月利率=(贷款本金-已归还本金累计额)×月利率
        var yuelixi = (dknum - yhbenjin) * mouthlilv;
        leftFund = leftFund - yuebenjin;
        if (leftFund < 0) {
            leftFund = 0
        }
        mouthdataArray[i - 1] = {
            monthName: realmonth + "月",
            yuelixi: yuelixi,
            //每月本金
            yuebenjin: everymonthyh,
            //剩余还款
            leftFund: leftFund
        }
    }
    return {
        yuegong: yuegong,
        totalLixi: totalLixi,
        totalPrice: totalPrice,
        yuegongdijian: yuegongdijian,
        mouthdataArray: mouthdataArray,
        totalDknum: num,
        year: year
    }
}
const formatTime = date => {
    const year = date.getFullYear()
    const month = date.getMonth() + 1
    const day = date.getDate()
    const hour = date.getHours()
    const minute = date.getMinutes()
    const second = date.getSeconds()
    return `${[year, month, day].map(formatNumber).join('/')} ${[hour, minute, second].map(formatNumber).join(':')}`
}

const formatNumber = n => {
    n = n.toString()
    return n[1] ? n : `0${n}`
}

const objToUrlParams = (obj) =>{
    let str = '';
    Object.keys(obj).forEach((item)=>{
        str = `${str}${item}=${obj[item]}&`;
    });
    return str;
}

const numToFixed = (num,fixed = 2) =>{
    return (num*1).toFixed(0);
}

module.exports = {
    benxi,
    benjin,
    objToUrlParams,
    formatTime,
    numToFixed
}