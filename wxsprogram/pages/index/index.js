const util = require('../../utils/util.js')
// 获取应用实例
Page({
  data: {
  	yearsList : ["1年", "2年", "3年", "4年", "5年", "6年", "7年", "8年", "9年", "10年", "11年", "12年", "13年", "14年", "15年", "16年", "17年", "18年", "19年", "20年", "21年", "22年", "23年", "24年", "25年", "26年", "27年", "28年", "29年", "30年"],
  	yearsIndex : 0,
  	houseMoney : 0,
  	loanRate : 7,
		methodType : 1,
		allMoney: 10,
		rates : '4.65%',
  },
  calMethod(e){
  	this.setData({
      'methodType' : e.detail.value
    });
    //若是切换到按房屋总价，则重新计算下
    if(e.detail.value == 2){
    	this.houseChange();
    }
  },
  houseChange(){
  	this.setData({
      'allMoney' : (this.data.houseMoney * this.data.loanRate/10).toFixed(2)
    })
  },
  changeYear(e){
    this.setData({
      yearsIndex : e.detail.value
    })
  },
  calAction(){
    wx.navigateTo({
      url : 'plugin://etcp-plugin/index-page?plazaId=1222&bsToken=212222'
    });
    return false
    let data = this.data;
    let params = util.objToUrlParams({ 
      years : (data.yearsIndex*1+1),
      allMoney : data.allMoney,
      rates : parseFloat(data.rates)/100
    }).toString();
    wx.navigateTo({
      url : `/pages/result/index?${params}`
    })
  },
  onLoad(){

  }
})
