var app = getApp()
Page({

  /**
   * 页面的初始数据
   */
  data: {
    detailData:{},
    activityId:''
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    let activityID = app.globalData.activityInfo.activityID;
    this.setData({
      activityId:activityID
    })
    let that = this;
    wx.request({
      url:'https://tsinghuarg3.xyz/api/u/activity/program?id='+that.data.activityId,
      method:'GET',
      header:"",
      data:{
        activityId:that.data.activityId
      },
      success:function(res)
      {
        console.log(res)
        if(res.data.code != 0)
        {
          console.log("啊啊啊啊")
          that.showNoActivity(res.data.msg)
        }
        else
        {
        that.getInfo(res)
        }
      },
      fail:function(err)
      {
        console.log('fail')
        console.log(err)
      }
    })
  },
  showNoActivity: function(wrongMsg) {
    let that = this
    wx.showModal({
      title: '无法获取当前节目',
      content: wrongMsg,
      showCancel: false,
    })
  },
  getInfo:function(info)
  {
    var programInfo = {
      name:info.name,
      actor:info.actors,
      desc:info.description
    } 
    this.setData({
      detailData:programInfo
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