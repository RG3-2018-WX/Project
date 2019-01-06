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
    showModal: false
  },

  bindChange: function(event) {
    let input = event.detail.value
    input = this.changeString(input)
    if (input != "") {
      this.setData({
        ['msg.content']: input,
        ['msg.userName']: "userName",
        ['msg.isUser']: true,
        hasMsg: true
      })
    }
  },
  changeString: function(input) {
    input = input.replace(/&/g, '&amp;');
    input = input.replace(/</g, '&lt;');
    input = input.replace(/>/g, '&gt;');
    input = input.replace(/"/g, '&quot;');
    input = input.replace(/'/g, '&#039;');
    return input
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
      if (that.data.msg.content == app.globalData.activityInfo.signNum) {
        that.sign();
      } else if (that.data.msg.content == '抽奖情况') {
        wx.request({
          url: 'https://tsinghuarg3.xyz/api/u/lottery/list',
          method: 'GET',
          data: {
            activityId: that.data.activityID,
            openId: app.globalData.userInfo.OpenId,
          },
          header: '',
          success: function(res) {
            console.log(res)
            if (res.data.code != 0) {
              that.sendFail(res.data.msg);
            } else {
              that.sentList(res);
            }
          },
          fail: function(res) {
            that.sendFail(res);
          }
        })
      } else {
        wx.request({
          url: 'https://tsinghuarg3.xyz/api/u/activity/comment',
          method: 'POST',
          data: {
            content: that.data.msg.content,
            activityId: that.data.activityID,
            openId: app.globalData.userInfo.OpenId,
            color: that.data.letterSytle.color,
            bolt: that.data.letterSytle.bolt,
            incline: that.data.letterSytle.incline,
            underline: that.data.letterSytle.underline,
          },
          header: '',
          success: function(res) {
            console.log(res)
            if (res.data.code != 0) {
              that.sendFail(res.data.msg);
            } else {
              that.sendSuccess();
            }
          },
          fail: function(res) {
            that.sendFail(res);
          }
        })
      }
    }
  },
  sign: function() {
    let that = this
    wx.request({
      url: 'https://tsinghuarg3.xyz/api/u/activity/sign',
      method: 'POST',
      data: {
        activityId: that.data.activityID,
        openId: app.globalData.userInfo.OpenId,
      },
      header: '',
      success: function(res) {
        let time = util.formatTime(new Date());
    let msg = {
      content: "登录成功",
      time: time,
      isUser: false,
    }
    let history = that.data.listData;
    history.push(msg);
    that.setData({
      listData: history,
    });
        console.log('登录')
        console.log(res)
      },
      fail: function(res) {
        let time = util.formatTime(new Date());
    let msg = {
      content: "登录失败",
      time: time,
      isUser: false,
    }
    let history = that.data.listData;
    history.push(msg);
    that.setData({
      listData: history,
    });
        console.log('登录失败')
        that.sendFail(res);
      }
    })
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
        wx.request({
          url: 'https://tsinghuarg3.xyz/api/u/activity/picture',
          method: 'POST',
          data: {
            picUrl: pic,
            activityId: that.data.activityID,
            openId: app.globalData.userInfo.OpenId,
          },
          header: '',
          success: function(res) {
            console.log(res)
            if (res.data.code != 0) {
              that.sendFail(res.data.msg);
            } else {
              that.sendSuccess();
            }
          },
          fail: function(res) {
            that.sendFail(res);
          }
        })
      }
    })
  },
  sentList: function(res) {
    let that = this;
    let list = res.data.data.list
    let history = that.data.listData;
    let msg = {};
    let time = util.formatTime(new Date());
    if (list[0]) {
      let history = that.data.listData;
      console.log("进来了")
      for (let i in list) {
        console.log(i)
        let name = list[i].name;
        let prize = list[i].prize;
        msg = {
          content: name + "中，获得" + prize,
          time: time,
          isUser: false,
        }
        history.push(msg);
      }
    } else
      msg = {
        content: "你没有获奖",
        time: time,
        isUser: false,
      }
    history.push(msg);
    that.setData({
      listData: history,
    });
  },
  sendSuccess: function() {
    let that = this;
    console.log('CC')
    let time = util.formatTime(new Date());
    let msg = {
      content: "弹幕发送成功",
      time: time,
      isUser: false,
    }
    let history = that.data.listData;
    history.push(msg);
    that.setData({
      listData: history,
    });
  },
  sendFail: function(res) {
    let that = this;
    console.log(res)
    let msg = {}
    let time = util.formatTime(new Date());
    if (res == 'Not Signed yet!') {
      console.log("login")
      msg = {
        content: "请先登录",
        time: time,
        isUser: false,
      }
    } else {
      msg = {
        content: "弹幕发送失败，请稍后在重试",
        time: time,
        isUser: false,
      }
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
    let activityID = app.globalData.activityInfo.activityID
    let activityName = app.globalData.activityInfo.activityName
    console.log(app.globalData.activityInfo.activityName)
    let userInfo = app.globalData.userInfo
    let letterSytle = app.globalData.letter
    let time = util.formatTime(new Date());
    let msg = {
      time: time,
      content: '欢迎参与活动：' + activityName,
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