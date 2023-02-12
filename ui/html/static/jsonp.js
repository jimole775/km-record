;(function () {
    var store;
    var router;
    var expose = function (name, value) {
        var kmrObject = window.__kmr__ || {};
        kmrObject[name] = value;
        window.__kmr__ = kmrObject;
    };
    var take = function (name) {
        var kmr = window.__kmr__ || {};
        return kmr[name];
    };
    var methods = {
        resize (w, h) {
            w = w ? w : 0;
            h = h ? h : 0;
            document.documentElement.style.width = w + 'px';
            document.documentElement.style.height = h + 'px';
        },
        send_data (data) {
            Object.keys(data).forEach((key) => {
                var val = data[key];
                if (Object.prototype.toString.call(val) === '[object Object]') {
                    window.sessionStorage[key] = JSON.stringify(val);
                } else {
                    window.sessionStorage[key] = val;
                }
            })
        },
        update_step (step) {
            if (!store) {
                store = take('store');
            }
            setTimeout(() => {
                store && store.dispatch('ACTION_SET_RECORD_STEP', step);
            }, 150)
        },
        modal_state (flag) {
            if (!store) {
                store = take('store');
            }
            setTimeout(() => {
                store && store.dispatch('ACTION_SET_CLIENT_FREEZING', flag);
            }, 150)
        }
    };
    expose('methods', methods)
})();
