var util = require('../../utils/util.js')
var app = getApp()
Page({
      /**
      页面的初始数据
      */
      data: {
        logged: false,
        userInfo: {}
      },

      /**
       * 生命周期函数--监听页面加载
       */
      onLoad: function(options) {},

      login: function(event) {
        if (this.data.logged) {
          return;
        }
        var that = this;
        if (event.detail.userInfo) {
          console.log('授权成功');
          console.log('获得的用户信息：', event.detail.userInfo);
          util.showBusy('正在登录');
          wx.checkSession({
            success: function() {
              console.log("checkSession")
              console.log("success")
              that.setData({
                logged: true,
                userInfo: event.detail.userInfo,
              })
              app.globalData.userInfo.nickName = that.data.userInfo.nickName;
              util.showSuccess('登录成功')
            },
            fail: function() {
              console.log('!checkSession')
          }})  
                      wx.login({
                success: function(res) {
                  console.log('login')
                  if (res.code) {
                    //发起网络请求
                    let code = res.code
                    wx.request({
                      url: 'https://api.weixin.qq.com/sns/jscode2session?appid=wxcfbe645b51a25f7d&secret=6086ca31959b59a5cc3cca72f2b16630&js_code=' + code + '&grant_type=authorization_code',
                      data: {},
                      method: 'GET',
                      header: {
                        'content-type': 'application/json'
                      },
                      success: function(res) {
                        console.log('login')
                        let openid = res.data.openid //返回openid
                        console.log(openid)
                        that.setData({
                          ['userInfo.OpenId']: openid
                        });
                        app.globalData.userInfo.OpenId = openid;
                        console.log(app.globalData.userInfo)
                      },
                      fail: function() {
                        console.log('...')
                      }
                    })
                  } else {
                    //用户按了拒绝按钮
                    wx.showModal({
                      title: '请求授权失败',
                      content: '将无法使用小程序，要转到设置界面去授权吗？',
                      success: function(res) {
                        if (res.confirm) {
                          wx.openSetting({
                            //重新获取用户信息
                          })
                        }
                      }
                    })
                  }
                }
              })
        }
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

          onTap: function() {
            wx.redirectTo({
              url: "../index/index"
            });
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