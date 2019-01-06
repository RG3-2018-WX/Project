var app = getApp()
Page({

  /**
   * 页面的初始数据
   */
  data: {
    listData: [],
    userInfo: {}
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function(options) {
    let UserInfo = app.globalData.userInfo;
    this.setData({
      userInfo: UserInfo
    })
    let that = this;
    this.getdata();
  },

  getList: function(res) {
    console.log(res)
    let list = res.data.data.list;
    console.log(list)
    let activityList = [];
    let activityInfo = {};
    for (let i in list) {
      console.log(i)
      activityInfo = {
        name: list[i].name,
        activityID: list[i].activityId,
        startTime: list[i].startTime,
        signNum: list[i].sign
      }
      activityList.push(activityInfo);
    }
    this.setData({
      listData: activityList
    })
  },
  showNoActivity: function(wrongMsg) {
    let that = this
    wx.showModal({
      title: '无法获取活动列表',
      content: wrongMsg,
      showCancel: false,
    })
  },
  bindNameTap: function(event) {
    let index = event.target.dataset.index;
    let that = this;
    let activityID = that.data.listData[index].activityID;
    app.globalData.activityInfo.activityID = activityID;
    app.globalData.activityInfo.activityName = that.data.listData[index].name;
    app.globalData.activityInfo.signNum = that.data.listData[index].signNum;
    wx.switchTab({
      url: '/pages/barrage/barrage'
    })
  },
  addActivity: function() {
    let that = this
    wx.scanCode({
      success: function(res) {
        console.log(res)
        let activityID = res.result
        console.log(activityID)
        let OpenId = that.data.userInfo.OpenId
        wx.request({
          url: 'https://668855.iterator-traits.com/api/u/activity/user',
          method: 'POST',
          data: {
            openId: OpenId,
            activityId: activityID
          },
          success: function(res) {
            if (res.data.code != 0) {
              console.log(res)
              wx.showModal({
                title: '没有查询到该活动',
                content: res.data.msg,
                showCancel: false,
              })
            } else {
              wx.showToast({
                title: '已添加活动',
                icon: 'success',
              })
              wx.redirectTo({
              url: "../index/index"
            });
            }
          }
        })
      },
      fail: function(res) {
        wx.showModal({
          title: '扫码失败',
          showCancel: false,
        })
      }
    })
  },
  getdata: function() {
    let that = this
    wx.request({
      url: 'https://668855.iterator-traits.com/api/u/activity/list',
      method: 'GET',
      header: "",
      data: {
        openId: that.data.userInfo.OpenId
      },
      success: function(res) {
        console.log(res)
        if (res.data.code != 0) {
          console.log('no activity')
          that.showNoActivity(res.data.msg)

        } else {
          that.getList(res)
        }
        console.log('successss')
      },
      fail: function(err) {
        console.log('fail')
        console.log(err)
      }
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
    this.getdata()
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