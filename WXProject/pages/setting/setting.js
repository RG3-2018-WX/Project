var util = require('../../utils/util.js')
var app = getApp()

Page({

  /**
   * 页面的初始数据
   */

  data: {
    style:[
          {name: '粗体字', value: '1',checked: true},
          {name: '斜体字', value: '2',checked: false},
          {name: '下划线', value: '3',checked: false}
    ],
    color:['red','blue','yellow','green','black','#00FFFF'],
    letterColor:''
  },

  onLoad: function (options) {
    let arr = this.data.style
    arr[0].checked = app.globalData.letter.bolt;
    arr[1].checked = app.globalData.letter.incline;
    arr[2].checked = app.globalData.letter.underline;
    this.setData({
      letterColor:app.globalData.letter.color,
      style:arr
    })
  },

  select:function(event){
    let that = this;
    var arr = that.data.style;
    console.log(arr)
    console.log(event)
    var index = event.currentTarget.dataset.index;
    console.log(index)
    arr[index].checked = !arr[index].checked;
    console.log(arr);
    that.setData({
      style:arr
    })
  },

  bindColorTap:function(event)
  {
    let that = this;
    let index = event.target.dataset.index
    console.log(index);
    let color = that.data.color[index]
    console.log(color);
    that.setData({
      letterColor:color
    })
  },

  save:function(event)
  {
    let that = this;
    app.globalData.letter ={
      color:that.data.letterColor,
      bolt:that.data.style[0].checked,
      incline:that.data.style[1].checked,
      underline:that.data.style[2].checked
    }
    wx.switchTab({
      url: '/pages/barrage/barrage'
    })
  },
  /**
   * 生命周期函数--监听页面初次渲染完成
   */
  onReady: function () {
    
  },

  /**
   * 生命周期函数--监听页面显示
   */
  onShow: function () {
  },

  /**
   * 生命周期函数--监听页面隐藏
   */
  onHide: function () {
    
  },

  /**
   * 生命周期函数--监听页面卸载
   */
  onUnload: function () {
    
  },

  /**
   * 页面相关事件处理函数--监听用户下拉动作
   */
  onPullDownRefresh: function () {
    
  },

  /**
   * 页面上拉触底事件的处理函数
   */
  onReachBottom: function () {
    
  },

  /**
   * 用户点击右上角分享
   */
  onShareAppMessage: function () {
    
  }
})