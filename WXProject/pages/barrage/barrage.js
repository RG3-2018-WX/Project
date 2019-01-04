var util = require('../../utils/util.js');
var app = getApp()

Page({

  /**
   * 页面的初始数据
   */
  data: {
    listData: [],
    scrollTop: 0,
    help: '设置课设置字体颜色等，发送抽奖情况查看抽奖情况',
    num: 0,
    hasMsg: false,
    inputValue: "",
    msg: {
      time: "",
      content: "",
      userName: "",
      isUser: false
    },
    userInfo: {},
    picList: [],
    letterSytle: {},
    showModal:false
  },

  bindChange: function(event) {
    let input = event.detail.value
    if (input != "") {
      this.setData({
        ['msg.content']: input,
        ['msg.userName']: "userName",
        ['msg.isUser']: true,
        hasMsg: true
      })
    }
  },

  sentmsg: function(event) {
    let that = this;
    if (that.data.hasMsg) {
      let time = util.formatTime(new Date());
      that.setData({
        ['msg.time']: time
      })
      let history = that.data.listData;
      history.push(that.data.msg);
      let num = that.data.num + 1;
      that.setData({
        inputValue: "",
        listData: history,
        hasMsg: false,
        num: num
      });
      that.bottom();
      wx.request({
        url: 'https://668855.iterator-traits.com/api/u/activity/listapi/u/activity/commen?id=' + that.data.activityID,
        //url: 'https://668855.iterator-traits.com/api/u/activity/listapi/u/activity/commen' ,
        method: 'GET',
        data: {
          acontent: that.data.msg.content,
          activityID: that.data.activityID,
          openId : app.globalData.userInfo.openID,
          color: that.data.letterSytle.color,
          bolt : that.data.letterSytle.bolt,
          incline : that.data.letterSytle.incline,
          undetline : that.data.letterSytle.undetline,
        },
        header: '',
        success: function() {
          that.sendSuccess();
        },
        fail: function(res) {
          that.sendFail(res);
        }
      })
    }
  },

  sentpic: function(event) {
    let that = this;
    wx.chooseImage({
      count: 1,
      success: function(res) {
        let tempFilePaths = res.tempFilePaths;
        let time = util.formatTime(new Date());
        let msg = {
          content: tempFilePaths,
          time: time,
          isUer: true,
          type: 'image'
        };
        let history = that.data.listData;
        let picArr = that.data.picList;
        let pic = tempFilePaths.toString();
        picArr.push(pic)
        history.push(msg);
        that.setData({
          listData: history,
          picList: picArr
        })
        that.bottom();
      }
    })
  },

  sendSuccess:function()
  {
    let that = this;
    console.log('CC')
    let time = util.formatTime(new Date());
    let msg = {
      content:"弹幕发送成功",
      time:time,
      isUser:false,
    }
     let history = that.data.listData;
      history.push(msg);
      that.setData({
        listData: history,
      });
  },
  sendFail:function(res)
  {
    let that = this;
    console.log('FF')
    let time = util.formatTime(new Date());
    let msg = {
      content:"弹幕失败，请稍后在重试",
      time:time,
      isUser:false,
    }
     let history = that.data.listData;
      history.push(msg);
      that.setData({
        listData: history,
      });
  },
  bottom: function() {
    let query = wx.createSelectorQuery();
    query.select('#botton').boundingClientRect();
    query.selectViewport().scrollOffset();
    query.exec(function(res) {
      wx.pageScrollTo({
        scrollTop: res[0].bottom
      })
      res[1].scrollTop
    })
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function(options) {
    let activityID = app.globalData.activityID
    let userInfo = app.globalData.userInfo
    let letterSytle = app.globalData.letter
    let time = util.formatTime(new Date());
    let msg = {
      time: time,
      content: '欢迎参与活动：' + options.id,
      isUser: false,
    }
    let m = this.data.listData;
    let help = this.data.help;
    m.push(msg);
    time = util.formatTime(new Date());
    msg = {
      time: time,
      content: help,
      isUser: false,
    }
    m.push(msg);
    this.setData({
      listData: m,
      activityID: activityID,
      userInfo: userInfo,
      letterSytle: letterSytle
    })
  },

  setting: function() {
    /*this.setData({
      showModal:true
    })*/
    console.log('!!!')
    wx.navigateTo({
      url: '/pages/setting/setting'
    })
  },

  /**
   * 生命周期函数--监听页面初次渲染完成
   */
  onReady: function() {},

  /**
   * 生命周期函数--监听页面显示
   */
  onShow: function() {
    let letterSytle = app.globalData.letter
    console.log(letterSytle)
    this.setData({
      letterSytle: letterSytle
    })
  },

  /**
   * 生命周期函数--监听页面隐藏
   */
  onHide: function() {

  },

  /**
   * 生命周期函数--监听页面卸载
   */
  onUnload: function() {

  },

  /**
   * 页面相关事件处理函数--监听用户下拉动作
   */
  onPullDownRefresh: function() {

  },

  /**
   * 页面上拉触底事件的处理函数
   */
  onReachBottom: function() {

  },

  /**
   * 用户点击右上角分享
   */
  onShareAppMessage: function() {

  }
})