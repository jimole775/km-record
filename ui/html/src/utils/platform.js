import utils from '@/utils'
const win = window
export default {
  injectForIOSAndLowerAndroid () {
    /**
     *  vue-bridge-webview config
     *
     * @type {{bridgeWebViewDelay: number}}
     */
    var bridgeConfig = {
      bridgeWebViewDelay: 0.2 * 1000,
      callHandle: {}, // bridge android / ios
      silent: false
    }
    var bridgeStatusIsOk = false
    var $bridge = {
      registerHandler: function (name, callback) {
        if (bridgeConfig.silent) {
          console.log(name, ' register handler failure')
        }
      },
      callHandler: function (name, params, callback) {
        if (bridgeConfig.silent) {
          console.log(name, ' call handler webView failure')
        }
      }
    }
    var WVJBCallbacks = win.WVJBCallbacks
    var WebViewJavascriptBridge = win.WebViewJavascriptBridge
    // ============ device init operation start ===========
    function setupWebViewJavascriptBridge (callback) {
      bridgeStatusIsOk = false
      if (WebViewJavascriptBridge) {
        console.log('the bridge instance:', WebViewJavascriptBridge)
        return callback(WebViewJavascriptBridge)
      }
      if (WVJBCallbacks) {
        return WVJBCallbacks.push(callback)
      }
      WVJBCallbacks = [callback]

      var WVJBIframe = document.createElement('iframe')
      WVJBIframe.style.display = 'none'
      WVJBIframe.src = 'wvjbscheme://__BRIDGE_LOADED__'
      document.documentElement.appendChild(WVJBIframe)
      setTimeout(function () { document.documentElement.removeChild(WVJBIframe) }, 0)
    }

    function connectWebViewJavascriptBridge (callback) {
      if (WebViewJavascriptBridge) {
        callback(WebViewJavascriptBridge)
      } else {
        document.addEventListener('WebViewJavascriptBridgeReady', function () {
          callback(WebViewJavascriptBridge)
        }, false)
      }
    }

    /* device detect for ios/android */
    if (/(iPhone|iPad|iPod|iOS)/i.test(navigator.userAgent)) {
      setupWebViewJavascriptBridge(function (bridge) {
        console.log('bind bridge', bridge)
        $bridge = bridge
      })
    } else if (/(Android)/i.test(navigator.userAgent)) {
      connectWebViewJavascriptBridge(function (bridge) {
        $bridge = bridge
      })
    }

    // ==============device init operation end ============

    var VueBridgeWebView = {
      install: function (Vue) {
        console.log('vueWebView install!')
        Vue.prototype.$bridge = this
        Vue.bridge = this

        // config
        bridgeConfig.slient = Vue.config.slient
      },

      registerHandler: function (name, registerCallback) {
        if ($bridge['registerHandler']) {
          setTimeout(function () {
            $bridge.registerHandler(name, registerCallback)
          }, bridgeConfig.bridgeWebViewDelay)
        } else {
          console.log("don't built-in WebView invoking ", name, '{registerHandler}')
        }
      },

      callHandler: function (name, params, callback) {
        if ($bridge['callHandler']) {
          if (bridgeStatusIsOk) {
            $bridge.callHandler(name, params, function (data) {
              if (typeof callback === 'function') {
                callback(data)
              }
            })
          } else {
            var isFirstCallHandlerSuccess = false
            var count = 0
            var WebiewJavascriptTimer = setInterval(function () {
              if (!isFirstCallHandlerSuccess) {
                if (count > 25) {
                  clearInterval(WebiewJavascriptTimer)
                  return false
                }
                console.log('apply $bridge.callHandler in loop!')
                $bridge.callHandler(name, params, function (data) {
                  console.log('apply $bridge.callHandler callback!', typeof callback)
                  if (typeof callback === 'function') {
                    clearInterval(WebiewJavascriptTimer)
                    isFirstCallHandlerSuccess = true
                    bridgeStatusIsOk = true
                    callback(data)
                  }
                })
              }
              count++
            }, bridgeConfig.bridgeWebViewDelay)
          }
        } else {
          console.log("don't built-in WebView invoking ", name, '{callHandler}')
        }
      }
    }

    console.log('init: ', typeof win.exports, typeof win.define, win.Vue, VueBridgeWebView)
    if (typeof win.exports === 'object') {
      module.exports = VueBridgeWebView
    } else if (typeof win.define === 'function' && win.define.amd) {
      win.define([], function () { return VueBridgeWebView })
    } else if (win.Vue) {
      win.$bridge = VueBridgeWebView
      win.Vue.use(VueBridgeWebView)
    } else {
      win.$bridge = VueBridgeWebView
    }

    console.log('userAgent: ', navigator.userAgent)
    if (win.$bridge) {
      var u = navigator.userAgent
      var isIOS = !!u.match(/\(i[^;]+;( U;)? CPU.+Mac OS X/)
      if (isIOS) {
        console.log('run opp_get_userinfo in lib-bridge.js')
        win.$bridge.callHandler('opp_get_userinfo', {}, function () {})
      }
    }
  },
  injectForStandardAndroid () {
    
    const adapterName = 'App'

    if (window.RYMJSBRIDGE) {
      return
    }

    var app = new Adapter();
    var slice = Array.prototype.slice;
    var toString = Object.prototype.toString;
    var callindex = 0;


    /**
     * 调用Native接口适配层的构造器
     * @constructor
     */
    function Adapter () {
      var ua = navigator.userAgent.toUpperCase()
      this.IS_ANDROID = ua.indexOf("ANDROID") !== -1
      this.IS_IOS = ua.indexOf("IPHONE OS") !== -1
      this.IS_MOCK = ua.indexOf("MOCK") !== -1
      this.IS_ANYDOOR = ua.indexOf("ANYDOOR") !== -1
    }

    /**
     * 调用一个Native方法
     * @param {Array.<string>} name 方法名称
     * @param {}
     */
    Adapter.prototype.call = function (name) {
      // 获取传递给Native方法的参数
      var self = this
      var args = slice.call(arguments, 1)
      var methodName = name[name.length - 1]
      // && self.IS_ANYDOOR
      if (self.IS_ANDROID) {
        if (window.HostApp) {
          var newArguments = []
          var ps = []
          var param
          for (var i = 0; i < args.length; i++) {
            if (typeof args[i] === 'function') {
              var callbackName = methodName + 'Callback' + callindex
              window[callbackName] = args[i]
              newArguments.push(callbackName)
              callindex++
              console.log('im-h5 newArguments fun = ' + callbackName)
            } else if (typeof args[i] === 'object') {
              // newArguments.push(JSON.stringify(args[i]));
              console.log('im-h5 newArguments object = ' + JSON.stringify(args[i]))
              param = JSON.stringify(args[i])
              var paramLen = param.length
              var limitSize = 500

              if (paramLen > limitSize) {
                var i = 0
                do {
                  i++
                  if (paramLen > limitSize * i) {
                    ps.push(param.substring(limitSize * (i - 1), limitSize * i))
                  } else {
                    ps.push(param.substring(limitSize * (i - 1), paramLen))
                  }
                  console.log('im-h5 i = ' + i)
                } while (paramLen > limitSize * i)
                console.log('im-h5 ps = ' + ps)
              } else {
                // newArguments.push(args[i])
                newArguments.push(JSON.stringify(args[i]))
              }
              console.log('im-h5 newArguments other = ' + args[i])
            } else {
              newArguments.push(args[i])
            }
          }

          if (ps.length > 0) {
            var i = 0
            var splitArguments
            var methodParams = {
              method: methodName,
              size: ps.length,
              index: 0
              // md5: hex_md5(param),
            }

            // var md5_a = hex_md5(param)
            console.log('im-h5 param md5 = ' + md5_a + 'ori str = ' + param);
            console.log('im-h5 param = ' + md5_a);
            //  methodParams.method = methodName;
            //  methodParams.size = ps.length;
            for (; i < ps.length; i++) {
              methodParams.index = i;
              splitArguments = null;
              splitArguments = clone(newArguments);
              splitArguments.push(ps[i]);
              splitArguments.push(JSON.stringify(methodParams));
              console.log('im-h5 splitArguments = ' + splitArguments);
              HostApp['splitJoint'].apply(window.HostApp, splitArguments);
            }
          } else {
            try {
              console.log('im-h5 newArguments = ' + newArguments);
              console.log('im-h5 newArguments methodName = ' + methodName);
              HostApp[methodName].apply(window.HostApp, newArguments);
            } catch (e) {
              var params = slice.call(arguments, 0);
              setTimeout(function() {
                app['call'].apply(app, params);
              }, 300)
            }
          }
        } else {
          var params = slice.call(arguments, 0);
          setTimeout(function() {
            app['call'].apply(app, params);
          }, 1000)
        }
      } else if (self.IS_IOS && self.IS_ANYDOOR) {
        var newArguments = ''
        var tempArgument = []
        for (var i = 0; i < args.length; i++) {
          // tempArgument = args[i];
          if (typeof args[i] === 'function') {
            var callbackName = methodName + 'Callback' + callindex;
            window[callbackName] = args[i];
            tempArgument.push(callbackName);
            callindex++;
          } else {
            tempArgument.push(args[i]);
          }
        }
        callindex++;
        var iframe = document.createElement('iframe');
        console.log('tempArgument' + tempArgument);
        var _src =
          'callnative://' +
          methodName +
          '/' +
          encodeURIComponent(JSON.stringify(tempArgument)) +
          '/' +
          callindex;
        console.log(_src);
        iframe.src = _src;
        iframe.style.display = 'none';
        document.body.appendChild(iframe);
        iframe.parentNode.removeChild(iframe);
        iframe = null;
      } else {
        console.log('未知环境');
      }
    }

    /**
     * 调用物理返回按钮
     *
     * @return {undefined} 没有返回
     */
    Adapter.prototype.goBack = function() {
      if (this.IS_ANDROID && HostApp && HostApp.goBackOrForward) {
        this.call(["goBackOrForward"], function(res) {
            try {
                res = JSON.parse(res);
                var flag = res.result;
                if (flag == "true") {
                    console.log("success back");
                } else {
                    console.log("success error");
                }
            } catch (e) {

            }
        }, function(err) {
          console.log(err)
        }, -1)
      } else {
        history.back()
      }
    }

    
    window[adapterName] = window.RYMJSBRIDGE = app;
    window.$bridge = {}
    window.$bridge.callHandler = function(name, param, callback) {
      var fnName = name
      if (name == 'opp_request_encrypt') {
        fnName = 'encodeData';
      }
      if (param == null || param == undefined) {
        console.log('im-h5 callHandler param is null');
        param = {}
      }

      console.log('im-h5 callHandler fnName = ' + fnName);
      App.call([fnName],function(data) {
        console.log("im-h5 callHandler data = "+data)
        if (callback == null || callback == undefined) {
          console.log('im-h5 callHandler callback is null');
        } else {
          callback(data);
        }
      }, function(error){
        console.log("im-h5 error" + error)
      }, param
      )
    }
  },
  initialize () {
    const getParams = function (name) {
      const reg = new RegExp('[?&]' + name + '=([^&#]*)', 'i')
      const res = win.location.href.match(reg)
      if (res && res.length > 1) {
        return decodeURIComponent(res[1])
      }
      return ''
    }
    // Android 465以上版本使用 native.js
    // Android 465以下版本及IOS 使用 lib-jsbridge.js
    const ua = navigator.userAgent.toUpperCase()
    const isAndroid = ua.indexOf('ANDROID') !== -1
    const ttNative = getParams('tt_versionCode') > 465
    const iknowNative = getParams('app_type') === 'iknow' && getParams('tt_versionCode') > 40
    const isNative = ttNative || iknowNative
    console.log('initlialze:', navigator.userAgent, isAndroid, isNative)
    if (isAndroid && isNative) {
      this.injectForStandardAndroid()
    } else {
      this.injectForIOSAndLowerAndroid()
    }
  },
  closeWebview () {
    console.log('closeWebview: ', win.$bridge)
    if (win.$bridge && win.$bridge.callHandler) {
      win.$bridge.callHandler('closeWebview', {}, function (data) {
        console.debug('success ', data)
      })
    } else {
      window.close()
    }
  },
  closeWebviewForMo () {
    console.log('closeWebviewForMo: ', win.location.href)
    const query = utils.getParamsFromURL(win.location.href)
    if (query['returnPage'] && query['returnPage'] === 'mo') {
      this.closeWebview()
    }
  }
}
