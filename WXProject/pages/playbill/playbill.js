var app = getApp()
Page({

  /**
   * 页面的初始数据
   */
  data: {
    listData: []
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function(options) {
    let activityID = app.globalData.activityInfo.activityID;
    this.setData({
      activityID: activityID
    })
    console.log(activityID)
    let that = this;
    wx.request({
      url: 'https://668855.iterator-traits.com/api/u/activity/detail?id=' + activityID,
      method: 'GET',
      header: "",
      data: {
        activityId: activityID
      },
      success: function(res) {
        console.log(res)
        console.log(res.code)
        if (res.data.code != 0) {
          console.log('no activity')
          that.showNoActivity(res.data.msg)
        } else {
          that.getList(res)
        }
      },
      fail: function(err) {
        console.log('fail')
        console.log(err)
      }
    })
  },
  showNoActivity: function(wrongMsg) {
    let that = this
    wx.showModal({
      title: '没有查询到该活动',
      content: wrongMsg,
      showCancel: false,
      success: function(res) {
        wx.redirectTo({
          url: '../index/index'
        })
      }
    })
  },
  getList: function(res) {
    //console.log(res)
    let list = res.data.data.list;
    console.log(list)
    let menu = [];
    let programInfo = {};
    for (let i in list) {
      programInfo = {
        name: list[i].name,
        sequence: list[i].sequence,
        actors: list[i].actors
      }
      menu.push(programInfo);
    }
    this.setData({
      listData: menu
    })
  },


  /**
   * 生命周期函数--监听页面初次渲染完成
   */
  onReady: function() {

  },

  /**
   * 生命周期函数--监听页面显示
   */
  onShow: function() {

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