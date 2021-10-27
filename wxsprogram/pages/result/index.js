// 获取应用实例
const util = require('../../utils/util.js')
Page({
  data: {
    bjResult : {
      total : '',
      lxTotal : ''
    },
    bxResult : {
      total : '',
      lxTotal : ''
    },
  	detailList : [],
  },
  dataHandle(bjResult,bxResult){
    //计算list
    let list = [];
    let diffValue = 0;
    bjResult.mouthdataArray.forEach((item,index)=>{
      let bxItem = bxResult.mouthdataArray[index];
      let lxDiffValue = util.numToFixed(bxItem.yuelixi - item.yuelixi);
      diffValue = util.numToFixed(diffValue*1 + lxDiffValue*1);
      list.push({
        bxValue : util.numToFixed(bxItem.yuebenjin),
        bxlxValue : util.numToFixed(bxItem.yuelixi),
        bjValue : util.numToFixed(item.yuebenjin),
        bjlxValue : util.numToFixed(item.yuelixi),
        lxDiffValue : lxDiffValue,
        lxDiffTotal : diffValue
      })
    });
    this.setData({
      bjResult : {
        total : util.numToFixed(bjResult.totalPrice),
        lxTotal :  util.numToFixed(bjResult.totalLixi),
      },
      bxResult: {
        total : util.numToFixed(bxResult.totalPrice),
        lxTotal :  util.numToFixed(bxResult.totalLixi),
      },
      detailList : list
    })
  },
  onLoad(options){
    let allMoney = options.allMoney;
    let years = parseInt(options.years);
    let rates = options.rates;
    let bjResult = util.benjin(allMoney,years,rates);
    let bxResult = util.benxi(allMoney,years,rates);
    this.dataHandle(bjResult,bxResult);
    console.log(bjResult,bxResult)
  }
})
