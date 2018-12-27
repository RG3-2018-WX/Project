var app = getApp()
Page({

  /**
   * 页面的初始数据
   */
  data: {
    listData: [
      {
      name:"a",
      time:"gal",
      activityID:1
    },
    {
      name:"a",
      time:"gal",
      activityID:2
    }],
    userInfo:{}
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function(options) {
    let UserInfo = app.globalData.userInfo;
    this.setData({
      userInfo:UserInfo
    })
    let that = this;
    wx.request({
      url:'https://668855.iterator-traits.com/api/u/activity/list?openId='+ UserInfo.OpenId,
      method:'GET',
      header:"",
      data:{
        openId:that.data.userInfo.OpenId
      },
      success:function(res)
      {
        console.log('successss')
        that.getList(res)
      },
      fail:function(err)
      {
        console.log('fail')
        console.log(err)
      }
    })
  },

  getList:function(res)
  {
    console.log(res)
    let list = res.data.data.list;
    console.log(list)
    let activityList = [];
    let activityInfo = {};
    for(let i in list)
    {
      console.log(i)
      activityInfo={
        name: list[i].name,
        activityID: list[i].activityId,
        startTime: list[i].startTime
      }
      activityList.push(activityInfo);
    }
    this.setData({
      listData:activityList
    })
  },
  bindNameTap: function(event) {
    let index = event.target.dataset.index;
    let that = this;
    let activityID = that.data.listData[index].activityID;
    app.globalData.activityID = activityID;
    wx.switchTab({
      url: '/pages/barrage/barrage'
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