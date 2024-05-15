(function() {
  "use strict";
  function _mergeNamespaces(n2, m2) {
    for (var i = 0; i < m2.length; i++) {
      const e2 = m2[i];
      if (typeof e2 !== "string" && !Array.isArray(e2)) {
        for (const k2 in e2) {
          if (k2 !== "default" && !(k2 in n2)) {
            const d2 = Object.getOwnPropertyDescriptor(e2, k2);
            if (d2) {
              Object.defineProperty(n2, k2, d2.get ? d2 : {
                enumerable: true,
                get: () => e2[k2]
              });
            }
          }
        }
      }
    }
    return Object.freeze(Object.defineProperty(n2, Symbol.toStringTag, { value: "Module" }));
  }
  var commonjsGlobal = typeof globalThis !== "undefined" ? globalThis : typeof window !== "undefined" ? window : typeof global !== "undefined" ? global : typeof self !== "undefined" ? self : {};
  function getDefaultExportFromCjs(x2) {
    return x2 && x2.__esModule && Object.prototype.hasOwnProperty.call(x2, "default") ? x2["default"] : x2;
  }
  var react = { exports: {} };
  var react_production_min = {};
  /**
   * @license React
   * react.production.min.js
   *
   * Copyright (c) Facebook, Inc. and its affiliates.
   *
   * This source code is licensed under the MIT license found in the
   * LICENSE file in the root directory of this source tree.
   */
  var l$2 = Symbol.for("react.element"), n$2 = Symbol.for("react.portal"), p$3 = Symbol.for("react.fragment"), q$3 = Symbol.for("react.strict_mode"), r$2 = Symbol.for("react.profiler"), t$2 = Symbol.for("react.provider"), u = Symbol.for("react.context"), v$3 = Symbol.for("react.forward_ref"), w$2 = Symbol.for("react.suspense"), x$2 = Symbol.for("react.memo"), y$2 = Symbol.for("react.lazy"), z$3 = Symbol.iterator;
  function A$3(a) {
    if (null === a || "object" !== typeof a)
      return null;
    a = z$3 && a[z$3] || a["@@iterator"];
    return "function" === typeof a ? a : null;
  }
  var B$2 = { isMounted: function() {
    return false;
  }, enqueueForceUpdate: function() {
  }, enqueueReplaceState: function() {
  }, enqueueSetState: function() {
  } }, C$2 = Object.assign, D$2 = {};
  function E$1(a, b2, e2) {
    this.props = a;
    this.context = b2;
    this.refs = D$2;
    this.updater = e2 || B$2;
  }
  E$1.prototype.isReactComponent = {};
  E$1.prototype.setState = function(a, b2) {
    if ("object" !== typeof a && "function" !== typeof a && null != a)
      throw Error("setState(...): takes an object of state variables to update or a function which returns an object of state variables.");
    this.updater.enqueueSetState(this, a, b2, "setState");
  };
  E$1.prototype.forceUpdate = function(a) {
    this.updater.enqueueForceUpdate(this, a, "forceUpdate");
  };
  function F$1() {
  }
  F$1.prototype = E$1.prototype;
  function G$2(a, b2, e2) {
    this.props = a;
    this.context = b2;
    this.refs = D$2;
    this.updater = e2 || B$2;
  }
  var H$2 = G$2.prototype = new F$1();
  H$2.constructor = G$2;
  C$2(H$2, E$1.prototype);
  H$2.isPureReactComponent = true;
  var I$2 = Array.isArray, J$1 = Object.prototype.hasOwnProperty, K$2 = { current: null }, L$2 = { key: true, ref: true, __self: true, __source: true };
  function M$2(a, b2, e2) {
    var d2, c2 = {}, k2 = null, h2 = null;
    if (null != b2)
      for (d2 in void 0 !== b2.ref && (h2 = b2.ref), void 0 !== b2.key && (k2 = "" + b2.key), b2)
        J$1.call(b2, d2) && !L$2.hasOwnProperty(d2) && (c2[d2] = b2[d2]);
    var g2 = arguments.length - 2;
    if (1 === g2)
      c2.children = e2;
    else if (1 < g2) {
      for (var f2 = Array(g2), m2 = 0; m2 < g2; m2++)
        f2[m2] = arguments[m2 + 2];
      c2.children = f2;
    }
    if (a && a.defaultProps)
      for (d2 in g2 = a.defaultProps, g2)
        void 0 === c2[d2] && (c2[d2] = g2[d2]);
    return { $$typeof: l$2, type: a, key: k2, ref: h2, props: c2, _owner: K$2.current };
  }
  function N$1(a, b2) {
    return { $$typeof: l$2, type: a.type, key: b2, ref: a.ref, props: a.props, _owner: a._owner };
  }
  function O$2(a) {
    return "object" === typeof a && null !== a && a.$$typeof === l$2;
  }
  function escape$2(a) {
    var b2 = { "=": "=0", ":": "=2" };
    return "$" + a.replace(/[=:]/g, function(a2) {
      return b2[a2];
    });
  }
  var P$1 = /\/+/g;
  function Q$2(a, b2) {
    return "object" === typeof a && null !== a && null != a.key ? escape$2("" + a.key) : b2.toString(36);
  }
  function R$2(a, b2, e2, d2, c2) {
    var k2 = typeof a;
    if ("undefined" === k2 || "boolean" === k2)
      a = null;
    var h2 = false;
    if (null === a)
      h2 = true;
    else
      switch (k2) {
        case "string":
        case "number":
          h2 = true;
          break;
        case "object":
          switch (a.$$typeof) {
            case l$2:
            case n$2:
              h2 = true;
          }
      }
    if (h2)
      return h2 = a, c2 = c2(h2), a = "" === d2 ? "." + Q$2(h2, 0) : d2, I$2(c2) ? (e2 = "", null != a && (e2 = a.replace(P$1, "$&/") + "/"), R$2(c2, b2, e2, "", function(a2) {
        return a2;
      })) : null != c2 && (O$2(c2) && (c2 = N$1(c2, e2 + (!c2.key || h2 && h2.key === c2.key ? "" : ("" + c2.key).replace(P$1, "$&/") + "/") + a)), b2.push(c2)), 1;
    h2 = 0;
    d2 = "" === d2 ? "." : d2 + ":";
    if (I$2(a))
      for (var g2 = 0; g2 < a.length; g2++) {
        k2 = a[g2];
        var f2 = d2 + Q$2(k2, g2);
        h2 += R$2(k2, b2, e2, f2, c2);
      }
    else if (f2 = A$3(a), "function" === typeof f2)
      for (a = f2.call(a), g2 = 0; !(k2 = a.next()).done; )
        k2 = k2.value, f2 = d2 + Q$2(k2, g2++), h2 += R$2(k2, b2, e2, f2, c2);
    else if ("object" === k2)
      throw b2 = String(a), Error("Objects are not valid as a React child (found: " + ("[object Object]" === b2 ? "object with keys {" + Object.keys(a).join(", ") + "}" : b2) + "). If you meant to render a collection of children, use an array instead.");
    return h2;
  }
  function S$2(a, b2, e2) {
    if (null == a)
      return a;
    var d2 = [], c2 = 0;
    R$2(a, d2, "", "", function(a2) {
      return b2.call(e2, a2, c2++);
    });
    return d2;
  }
  function T$2(a) {
    if (-1 === a._status) {
      var b2 = a._result;
      b2 = b2();
      b2.then(function(b3) {
        if (0 === a._status || -1 === a._status)
          a._status = 1, a._result = b3;
      }, function(b3) {
        if (0 === a._status || -1 === a._status)
          a._status = 2, a._result = b3;
      });
      -1 === a._status && (a._status = 0, a._result = b2);
    }
    if (1 === a._status)
      return a._result.default;
    throw a._result;
  }
  var U$2 = { current: null }, V$2 = { transition: null }, W$2 = { ReactCurrentDispatcher: U$2, ReactCurrentBatchConfig: V$2, ReactCurrentOwner: K$2 };
  function X$2() {
    throw Error("act(...) is not supported in production builds of React.");
  }
  react_production_min.Children = { map: S$2, forEach: function(a, b2, e2) {
    S$2(a, function() {
      b2.apply(this, arguments);
    }, e2);
  }, count: function(a) {
    var b2 = 0;
    S$2(a, function() {
      b2++;
    });
    return b2;
  }, toArray: function(a) {
    return S$2(a, function(a2) {
      return a2;
    }) || [];
  }, only: function(a) {
    if (!O$2(a))
      throw Error("React.Children.only expected to receive a single React element child.");
    return a;
  } };
  react_production_min.Component = E$1;
  react_production_min.Fragment = p$3;
  react_production_min.Profiler = r$2;
  react_production_min.PureComponent = G$2;
  react_production_min.StrictMode = q$3;
  react_production_min.Suspense = w$2;
  react_production_min.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED = W$2;
  react_production_min.act = X$2;
  react_production_min.cloneElement = function(a, b2, e2) {
    if (null === a || void 0 === a)
      throw Error("React.cloneElement(...): The argument must be a React element, but you passed " + a + ".");
    var d2 = C$2({}, a.props), c2 = a.key, k2 = a.ref, h2 = a._owner;
    if (null != b2) {
      void 0 !== b2.ref && (k2 = b2.ref, h2 = K$2.current);
      void 0 !== b2.key && (c2 = "" + b2.key);
      if (a.type && a.type.defaultProps)
        var g2 = a.type.defaultProps;
      for (f2 in b2)
        J$1.call(b2, f2) && !L$2.hasOwnProperty(f2) && (d2[f2] = void 0 === b2[f2] && void 0 !== g2 ? g2[f2] : b2[f2]);
    }
    var f2 = arguments.length - 2;
    if (1 === f2)
      d2.children = e2;
    else if (1 < f2) {
      g2 = Array(f2);
      for (var m2 = 0; m2 < f2; m2++)
        g2[m2] = arguments[m2 + 2];
      d2.children = g2;
    }
    return { $$typeof: l$2, type: a.type, key: c2, ref: k2, props: d2, _owner: h2 };
  };
  react_production_min.createContext = function(a) {
    a = { $$typeof: u, _currentValue: a, _currentValue2: a, _threadCount: 0, Provider: null, Consumer: null, _defaultValue: null, _globalName: null };
    a.Provider = { $$typeof: t$2, _context: a };
    return a.Consumer = a;
  };
  react_production_min.createElement = M$2;
  react_production_min.createFactory = function(a) {
    var b2 = M$2.bind(null, a);
    b2.type = a;
    return b2;
  };
  react_production_min.createRef = function() {
    return { current: null };
  };
  react_production_min.forwardRef = function(a) {
    return { $$typeof: v$3, render: a };
  };
  react_production_min.isValidElement = O$2;
  react_production_min.lazy = function(a) {
    return { $$typeof: y$2, _payload: { _status: -1, _result: a }, _init: T$2 };
  };
  react_production_min.memo = function(a, b2) {
    return { $$typeof: x$2, type: a, compare: void 0 === b2 ? null : b2 };
  };
  react_production_min.startTransition = function(a) {
    var b2 = V$2.transition;
    V$2.transition = {};
    try {
      a();
    } finally {
      V$2.transition = b2;
    }
  };
  react_production_min.unstable_act = X$2;
  react_production_min.useCallback = function(a, b2) {
    return U$2.current.useCallback(a, b2);
  };
  react_production_min.useContext = function(a) {
    return U$2.current.useContext(a);
  };
  react_production_min.useDebugValue = function() {
  };
  react_production_min.useDeferredValue = function(a) {
    return U$2.current.useDeferredValue(a);
  };
  react_production_min.useEffect = function(a, b2) {
    return U$2.current.useEffect(a, b2);
  };
  react_production_min.useId = function() {
    return U$2.current.useId();
  };
  react_production_min.useImperativeHandle = function(a, b2, e2) {
    return U$2.current.useImperativeHandle(a, b2, e2);
  };
  react_production_min.useInsertionEffect = function(a, b2) {
    return U$2.current.useInsertionEffect(a, b2);
  };
  react_production_min.useLayoutEffect = function(a, b2) {
    return U$2.current.useLayoutEffect(a, b2);
  };
  react_production_min.useMemo = function(a, b2) {
    return U$2.current.useMemo(a, b2);
  };
  react_production_min.useReducer = function(a, b2, e2) {
    return U$2.current.useReducer(a, b2, e2);
  };
  react_production_min.useRef = function(a) {
    return U$2.current.useRef(a);
  };
  react_production_min.useState = function(a) {
    return U$2.current.useState(a);
  };
  react_production_min.useSyncExternalStore = function(a, b2, e2) {
    return U$2.current.useSyncExternalStore(a, b2, e2);
  };
  react_production_min.useTransition = function() {
    return U$2.current.useTransition();
  };
  react_production_min.version = "18.3.1";
  {
    react.exports = react_production_min;
  }
  var reactExports = react.exports;
  const React = /* @__PURE__ */ getDefaultExportFromCjs(reactExports);
  const React$1 = /* @__PURE__ */ _mergeNamespaces({
    __proto__: null,
    default: React
  }, [reactExports]);
  var reactDom = { exports: {} };
  var reactDom_production_min = {};
  var scheduler = { exports: {} };
  var scheduler_production_min = {};
  /**
   * @license React
   * scheduler.production.min.js
   *
   * Copyright (c) Facebook, Inc. and its affiliates.
   *
   * This source code is licensed under the MIT license found in the
   * LICENSE file in the root directory of this source tree.
   */
  (function(exports) {
    function f2(a, b2) {
      var c2 = a.length;
      a.push(b2);
      a:
        for (; 0 < c2; ) {
          var d2 = c2 - 1 >>> 1, e2 = a[d2];
          if (0 < g2(e2, b2))
            a[d2] = b2, a[c2] = e2, c2 = d2;
          else
            break a;
        }
    }
    function h2(a) {
      return 0 === a.length ? null : a[0];
    }
    function k2(a) {
      if (0 === a.length)
        return null;
      var b2 = a[0], c2 = a.pop();
      if (c2 !== b2) {
        a[0] = c2;
        a:
          for (var d2 = 0, e2 = a.length, w2 = e2 >>> 1; d2 < w2; ) {
            var m2 = 2 * (d2 + 1) - 1, C2 = a[m2], n2 = m2 + 1, x2 = a[n2];
            if (0 > g2(C2, c2))
              n2 < e2 && 0 > g2(x2, C2) ? (a[d2] = x2, a[n2] = c2, d2 = n2) : (a[d2] = C2, a[m2] = c2, d2 = m2);
            else if (n2 < e2 && 0 > g2(x2, c2))
              a[d2] = x2, a[n2] = c2, d2 = n2;
            else
              break a;
          }
      }
      return b2;
    }
    function g2(a, b2) {
      var c2 = a.sortIndex - b2.sortIndex;
      return 0 !== c2 ? c2 : a.id - b2.id;
    }
    if ("object" === typeof performance && "function" === typeof performance.now) {
      var l2 = performance;
      exports.unstable_now = function() {
        return l2.now();
      };
    } else {
      var p2 = Date, q2 = p2.now();
      exports.unstable_now = function() {
        return p2.now() - q2;
      };
    }
    var r2 = [], t2 = [], u2 = 1, v2 = null, y2 = 3, z2 = false, A2 = false, B2 = false, D2 = "function" === typeof setTimeout ? setTimeout : null, E2 = "function" === typeof clearTimeout ? clearTimeout : null, F2 = "undefined" !== typeof setImmediate ? setImmediate : null;
    "undefined" !== typeof navigator && void 0 !== navigator.scheduling && void 0 !== navigator.scheduling.isInputPending && navigator.scheduling.isInputPending.bind(navigator.scheduling);
    function G2(a) {
      for (var b2 = h2(t2); null !== b2; ) {
        if (null === b2.callback)
          k2(t2);
        else if (b2.startTime <= a)
          k2(t2), b2.sortIndex = b2.expirationTime, f2(r2, b2);
        else
          break;
        b2 = h2(t2);
      }
    }
    function H2(a) {
      B2 = false;
      G2(a);
      if (!A2)
        if (null !== h2(r2))
          A2 = true, I2(J2);
        else {
          var b2 = h2(t2);
          null !== b2 && K2(H2, b2.startTime - a);
        }
    }
    function J2(a, b2) {
      A2 = false;
      B2 && (B2 = false, E2(L2), L2 = -1);
      z2 = true;
      var c2 = y2;
      try {
        G2(b2);
        for (v2 = h2(r2); null !== v2 && (!(v2.expirationTime > b2) || a && !M2()); ) {
          var d2 = v2.callback;
          if ("function" === typeof d2) {
            v2.callback = null;
            y2 = v2.priorityLevel;
            var e2 = d2(v2.expirationTime <= b2);
            b2 = exports.unstable_now();
            "function" === typeof e2 ? v2.callback = e2 : v2 === h2(r2) && k2(r2);
            G2(b2);
          } else
            k2(r2);
          v2 = h2(r2);
        }
        if (null !== v2)
          var w2 = true;
        else {
          var m2 = h2(t2);
          null !== m2 && K2(H2, m2.startTime - b2);
          w2 = false;
        }
        return w2;
      } finally {
        v2 = null, y2 = c2, z2 = false;
      }
    }
    var N2 = false, O2 = null, L2 = -1, P2 = 5, Q2 = -1;
    function M2() {
      return exports.unstable_now() - Q2 < P2 ? false : true;
    }
    function R2() {
      if (null !== O2) {
        var a = exports.unstable_now();
        Q2 = a;
        var b2 = true;
        try {
          b2 = O2(true, a);
        } finally {
          b2 ? S2() : (N2 = false, O2 = null);
        }
      } else
        N2 = false;
    }
    var S2;
    if ("function" === typeof F2)
      S2 = function() {
        F2(R2);
      };
    else if ("undefined" !== typeof MessageChannel) {
      var T2 = new MessageChannel(), U2 = T2.port2;
      T2.port1.onmessage = R2;
      S2 = function() {
        U2.postMessage(null);
      };
    } else
      S2 = function() {
        D2(R2, 0);
      };
    function I2(a) {
      O2 = a;
      N2 || (N2 = true, S2());
    }
    function K2(a, b2) {
      L2 = D2(function() {
        a(exports.unstable_now());
      }, b2);
    }
    exports.unstable_IdlePriority = 5;
    exports.unstable_ImmediatePriority = 1;
    exports.unstable_LowPriority = 4;
    exports.unstable_NormalPriority = 3;
    exports.unstable_Profiling = null;
    exports.unstable_UserBlockingPriority = 2;
    exports.unstable_cancelCallback = function(a) {
      a.callback = null;
    };
    exports.unstable_continueExecution = function() {
      A2 || z2 || (A2 = true, I2(J2));
    };
    exports.unstable_forceFrameRate = function(a) {
      0 > a || 125 < a ? console.error("forceFrameRate takes a positive int between 0 and 125, forcing frame rates higher than 125 fps is not supported") : P2 = 0 < a ? Math.floor(1e3 / a) : 5;
    };
    exports.unstable_getCurrentPriorityLevel = function() {
      return y2;
    };
    exports.unstable_getFirstCallbackNode = function() {
      return h2(r2);
    };
    exports.unstable_next = function(a) {
      switch (y2) {
        case 1:
        case 2:
        case 3:
          var b2 = 3;
          break;
        default:
          b2 = y2;
      }
      var c2 = y2;
      y2 = b2;
      try {
        return a();
      } finally {
        y2 = c2;
      }
    };
    exports.unstable_pauseExecution = function() {
    };
    exports.unstable_requestPaint = function() {
    };
    exports.unstable_runWithPriority = function(a, b2) {
      switch (a) {
        case 1:
        case 2:
        case 3:
        case 4:
        case 5:
          break;
        default:
          a = 3;
      }
      var c2 = y2;
      y2 = a;
      try {
        return b2();
      } finally {
        y2 = c2;
      }
    };
    exports.unstable_scheduleCallback = function(a, b2, c2) {
      var d2 = exports.unstable_now();
      "object" === typeof c2 && null !== c2 ? (c2 = c2.delay, c2 = "number" === typeof c2 && 0 < c2 ? d2 + c2 : d2) : c2 = d2;
      switch (a) {
        case 1:
          var e2 = -1;
          break;
        case 2:
          e2 = 250;
          break;
        case 5:
          e2 = 1073741823;
          break;
        case 4:
          e2 = 1e4;
          break;
        default:
          e2 = 5e3;
      }
      e2 = c2 + e2;
      a = { id: u2++, callback: b2, priorityLevel: a, startTime: c2, expirationTime: e2, sortIndex: -1 };
      c2 > d2 ? (a.sortIndex = c2, f2(t2, a), null === h2(r2) && a === h2(t2) && (B2 ? (E2(L2), L2 = -1) : B2 = true, K2(H2, c2 - d2))) : (a.sortIndex = e2, f2(r2, a), A2 || z2 || (A2 = true, I2(J2)));
      return a;
    };
    exports.unstable_shouldYield = M2;
    exports.unstable_wrapCallback = function(a) {
      var b2 = y2;
      return function() {
        var c2 = y2;
        y2 = b2;
        try {
          return a.apply(this, arguments);
        } finally {
          y2 = c2;
        }
      };
    };
  })(scheduler_production_min);
  {
    scheduler.exports = scheduler_production_min;
  }
  var schedulerExports = scheduler.exports;
  /**
   * @license React
   * react-dom.production.min.js
   *
   * Copyright (c) Facebook, Inc. and its affiliates.
   *
   * This source code is licensed under the MIT license found in the
   * LICENSE file in the root directory of this source tree.
   */
  var aa = reactExports, ca = schedulerExports;
  function p$2(a) {
    for (var b2 = "https://reactjs.org/docs/error-decoder.html?invariant=" + a, c2 = 1; c2 < arguments.length; c2++)
      b2 += "&args[]=" + encodeURIComponent(arguments[c2]);
    return "Minified React error #" + a + "; visit " + b2 + " for the full message or use the non-minified dev environment for full errors and additional helpful warnings.";
  }
  var da = /* @__PURE__ */ new Set(), ea = {};
  function fa(a, b2) {
    ha(a, b2);
    ha(a + "Capture", b2);
  }
  function ha(a, b2) {
    ea[a] = b2;
    for (a = 0; a < b2.length; a++)
      da.add(b2[a]);
  }
  var ia = !("undefined" === typeof window || "undefined" === typeof window.document || "undefined" === typeof window.document.createElement), ja = Object.prototype.hasOwnProperty, ka = /^[:A-Z_a-z\u00C0-\u00D6\u00D8-\u00F6\u00F8-\u02FF\u0370-\u037D\u037F-\u1FFF\u200C-\u200D\u2070-\u218F\u2C00-\u2FEF\u3001-\uD7FF\uF900-\uFDCF\uFDF0-\uFFFD][:A-Z_a-z\u00C0-\u00D6\u00D8-\u00F6\u00F8-\u02FF\u0370-\u037D\u037F-\u1FFF\u200C-\u200D\u2070-\u218F\u2C00-\u2FEF\u3001-\uD7FF\uF900-\uFDCF\uFDF0-\uFFFD\-.0-9\u00B7\u0300-\u036F\u203F-\u2040]*$/, la = {}, ma = {};
  function oa(a) {
    if (ja.call(ma, a))
      return true;
    if (ja.call(la, a))
      return false;
    if (ka.test(a))
      return ma[a] = true;
    la[a] = true;
    return false;
  }
  function pa(a, b2, c2, d2) {
    if (null !== c2 && 0 === c2.type)
      return false;
    switch (typeof b2) {
      case "function":
      case "symbol":
        return true;
      case "boolean":
        if (d2)
          return false;
        if (null !== c2)
          return !c2.acceptsBooleans;
        a = a.toLowerCase().slice(0, 5);
        return "data-" !== a && "aria-" !== a;
      default:
        return false;
    }
  }
  function qa(a, b2, c2, d2) {
    if (null === b2 || "undefined" === typeof b2 || pa(a, b2, c2, d2))
      return true;
    if (d2)
      return false;
    if (null !== c2)
      switch (c2.type) {
        case 3:
          return !b2;
        case 4:
          return false === b2;
        case 5:
          return isNaN(b2);
        case 6:
          return isNaN(b2) || 1 > b2;
      }
    return false;
  }
  function v$2(a, b2, c2, d2, e2, f2, g2) {
    this.acceptsBooleans = 2 === b2 || 3 === b2 || 4 === b2;
    this.attributeName = d2;
    this.attributeNamespace = e2;
    this.mustUseProperty = c2;
    this.propertyName = a;
    this.type = b2;
    this.sanitizeURL = f2;
    this.removeEmptyString = g2;
  }
  var z$2 = {};
  "children dangerouslySetInnerHTML defaultValue defaultChecked innerHTML suppressContentEditableWarning suppressHydrationWarning style".split(" ").forEach(function(a) {
    z$2[a] = new v$2(a, 0, false, a, null, false, false);
  });
  [["acceptCharset", "accept-charset"], ["className", "class"], ["htmlFor", "for"], ["httpEquiv", "http-equiv"]].forEach(function(a) {
    var b2 = a[0];
    z$2[b2] = new v$2(b2, 1, false, a[1], null, false, false);
  });
  ["contentEditable", "draggable", "spellCheck", "value"].forEach(function(a) {
    z$2[a] = new v$2(a, 2, false, a.toLowerCase(), null, false, false);
  });
  ["autoReverse", "externalResourcesRequired", "focusable", "preserveAlpha"].forEach(function(a) {
    z$2[a] = new v$2(a, 2, false, a, null, false, false);
  });
  "allowFullScreen async autoFocus autoPlay controls default defer disabled disablePictureInPicture disableRemotePlayback formNoValidate hidden loop noModule noValidate open playsInline readOnly required reversed scoped seamless itemScope".split(" ").forEach(function(a) {
    z$2[a] = new v$2(a, 3, false, a.toLowerCase(), null, false, false);
  });
  ["checked", "multiple", "muted", "selected"].forEach(function(a) {
    z$2[a] = new v$2(a, 3, true, a, null, false, false);
  });
  ["capture", "download"].forEach(function(a) {
    z$2[a] = new v$2(a, 4, false, a, null, false, false);
  });
  ["cols", "rows", "size", "span"].forEach(function(a) {
    z$2[a] = new v$2(a, 6, false, a, null, false, false);
  });
  ["rowSpan", "start"].forEach(function(a) {
    z$2[a] = new v$2(a, 5, false, a.toLowerCase(), null, false, false);
  });
  var ra = /[\-:]([a-z])/g;
  function sa(a) {
    return a[1].toUpperCase();
  }
  "accent-height alignment-baseline arabic-form baseline-shift cap-height clip-path clip-rule color-interpolation color-interpolation-filters color-profile color-rendering dominant-baseline enable-background fill-opacity fill-rule flood-color flood-opacity font-family font-size font-size-adjust font-stretch font-style font-variant font-weight glyph-name glyph-orientation-horizontal glyph-orientation-vertical horiz-adv-x horiz-origin-x image-rendering letter-spacing lighting-color marker-end marker-mid marker-start overline-position overline-thickness paint-order panose-1 pointer-events rendering-intent shape-rendering stop-color stop-opacity strikethrough-position strikethrough-thickness stroke-dasharray stroke-dashoffset stroke-linecap stroke-linejoin stroke-miterlimit stroke-opacity stroke-width text-anchor text-decoration text-rendering underline-position underline-thickness unicode-bidi unicode-range units-per-em v-alphabetic v-hanging v-ideographic v-mathematical vector-effect vert-adv-y vert-origin-x vert-origin-y word-spacing writing-mode xmlns:xlink x-height".split(" ").forEach(function(a) {
    var b2 = a.replace(
      ra,
      sa
    );
    z$2[b2] = new v$2(b2, 1, false, a, null, false, false);
  });
  "xlink:actuate xlink:arcrole xlink:role xlink:show xlink:title xlink:type".split(" ").forEach(function(a) {
    var b2 = a.replace(ra, sa);
    z$2[b2] = new v$2(b2, 1, false, a, "http://www.w3.org/1999/xlink", false, false);
  });
  ["xml:base", "xml:lang", "xml:space"].forEach(function(a) {
    var b2 = a.replace(ra, sa);
    z$2[b2] = new v$2(b2, 1, false, a, "http://www.w3.org/XML/1998/namespace", false, false);
  });
  ["tabIndex", "crossOrigin"].forEach(function(a) {
    z$2[a] = new v$2(a, 1, false, a.toLowerCase(), null, false, false);
  });
  z$2.xlinkHref = new v$2("xlinkHref", 1, false, "xlink:href", "http://www.w3.org/1999/xlink", true, false);
  ["src", "href", "action", "formAction"].forEach(function(a) {
    z$2[a] = new v$2(a, 1, false, a.toLowerCase(), null, true, true);
  });
  function ta(a, b2, c2, d2) {
    var e2 = z$2.hasOwnProperty(b2) ? z$2[b2] : null;
    if (null !== e2 ? 0 !== e2.type : d2 || !(2 < b2.length) || "o" !== b2[0] && "O" !== b2[0] || "n" !== b2[1] && "N" !== b2[1])
      qa(b2, c2, e2, d2) && (c2 = null), d2 || null === e2 ? oa(b2) && (null === c2 ? a.removeAttribute(b2) : a.setAttribute(b2, "" + c2)) : e2.mustUseProperty ? a[e2.propertyName] = null === c2 ? 3 === e2.type ? false : "" : c2 : (b2 = e2.attributeName, d2 = e2.attributeNamespace, null === c2 ? a.removeAttribute(b2) : (e2 = e2.type, c2 = 3 === e2 || 4 === e2 && true === c2 ? "" : "" + c2, d2 ? a.setAttributeNS(d2, b2, c2) : a.setAttribute(b2, c2)));
  }
  var ua = aa.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED, va = Symbol.for("react.element"), wa = Symbol.for("react.portal"), ya = Symbol.for("react.fragment"), za = Symbol.for("react.strict_mode"), Aa = Symbol.for("react.profiler"), Ba = Symbol.for("react.provider"), Ca = Symbol.for("react.context"), Da = Symbol.for("react.forward_ref"), Ea = Symbol.for("react.suspense"), Fa = Symbol.for("react.suspense_list"), Ga = Symbol.for("react.memo"), Ha = Symbol.for("react.lazy");
  var Ia = Symbol.for("react.offscreen");
  var Ja = Symbol.iterator;
  function Ka(a) {
    if (null === a || "object" !== typeof a)
      return null;
    a = Ja && a[Ja] || a["@@iterator"];
    return "function" === typeof a ? a : null;
  }
  var A$2 = Object.assign, La;
  function Ma(a) {
    if (void 0 === La)
      try {
        throw Error();
      } catch (c2) {
        var b2 = c2.stack.trim().match(/\n( *(at )?)/);
        La = b2 && b2[1] || "";
      }
    return "\n" + La + a;
  }
  var Na = false;
  function Oa(a, b2) {
    if (!a || Na)
      return "";
    Na = true;
    var c2 = Error.prepareStackTrace;
    Error.prepareStackTrace = void 0;
    try {
      if (b2)
        if (b2 = function() {
          throw Error();
        }, Object.defineProperty(b2.prototype, "props", { set: function() {
          throw Error();
        } }), "object" === typeof Reflect && Reflect.construct) {
          try {
            Reflect.construct(b2, []);
          } catch (l2) {
            var d2 = l2;
          }
          Reflect.construct(a, [], b2);
        } else {
          try {
            b2.call();
          } catch (l2) {
            d2 = l2;
          }
          a.call(b2.prototype);
        }
      else {
        try {
          throw Error();
        } catch (l2) {
          d2 = l2;
        }
        a();
      }
    } catch (l2) {
      if (l2 && d2 && "string" === typeof l2.stack) {
        for (var e2 = l2.stack.split("\n"), f2 = d2.stack.split("\n"), g2 = e2.length - 1, h2 = f2.length - 1; 1 <= g2 && 0 <= h2 && e2[g2] !== f2[h2]; )
          h2--;
        for (; 1 <= g2 && 0 <= h2; g2--, h2--)
          if (e2[g2] !== f2[h2]) {
            if (1 !== g2 || 1 !== h2) {
              do
                if (g2--, h2--, 0 > h2 || e2[g2] !== f2[h2]) {
                  var k2 = "\n" + e2[g2].replace(" at new ", " at ");
                  a.displayName && k2.includes("<anonymous>") && (k2 = k2.replace("<anonymous>", a.displayName));
                  return k2;
                }
              while (1 <= g2 && 0 <= h2);
            }
            break;
          }
      }
    } finally {
      Na = false, Error.prepareStackTrace = c2;
    }
    return (a = a ? a.displayName || a.name : "") ? Ma(a) : "";
  }
  function Pa(a) {
    switch (a.tag) {
      case 5:
        return Ma(a.type);
      case 16:
        return Ma("Lazy");
      case 13:
        return Ma("Suspense");
      case 19:
        return Ma("SuspenseList");
      case 0:
      case 2:
      case 15:
        return a = Oa(a.type, false), a;
      case 11:
        return a = Oa(a.type.render, false), a;
      case 1:
        return a = Oa(a.type, true), a;
      default:
        return "";
    }
  }
  function Qa(a) {
    if (null == a)
      return null;
    if ("function" === typeof a)
      return a.displayName || a.name || null;
    if ("string" === typeof a)
      return a;
    switch (a) {
      case ya:
        return "Fragment";
      case wa:
        return "Portal";
      case Aa:
        return "Profiler";
      case za:
        return "StrictMode";
      case Ea:
        return "Suspense";
      case Fa:
        return "SuspenseList";
    }
    if ("object" === typeof a)
      switch (a.$$typeof) {
        case Ca:
          return (a.displayName || "Context") + ".Consumer";
        case Ba:
          return (a._context.displayName || "Context") + ".Provider";
        case Da:
          var b2 = a.render;
          a = a.displayName;
          a || (a = b2.displayName || b2.name || "", a = "" !== a ? "ForwardRef(" + a + ")" : "ForwardRef");
          return a;
        case Ga:
          return b2 = a.displayName || null, null !== b2 ? b2 : Qa(a.type) || "Memo";
        case Ha:
          b2 = a._payload;
          a = a._init;
          try {
            return Qa(a(b2));
          } catch (c2) {
          }
      }
    return null;
  }
  function Ra(a) {
    var b2 = a.type;
    switch (a.tag) {
      case 24:
        return "Cache";
      case 9:
        return (b2.displayName || "Context") + ".Consumer";
      case 10:
        return (b2._context.displayName || "Context") + ".Provider";
      case 18:
        return "DehydratedFragment";
      case 11:
        return a = b2.render, a = a.displayName || a.name || "", b2.displayName || ("" !== a ? "ForwardRef(" + a + ")" : "ForwardRef");
      case 7:
        return "Fragment";
      case 5:
        return b2;
      case 4:
        return "Portal";
      case 3:
        return "Root";
      case 6:
        return "Text";
      case 16:
        return Qa(b2);
      case 8:
        return b2 === za ? "StrictMode" : "Mode";
      case 22:
        return "Offscreen";
      case 12:
        return "Profiler";
      case 21:
        return "Scope";
      case 13:
        return "Suspense";
      case 19:
        return "SuspenseList";
      case 25:
        return "TracingMarker";
      case 1:
      case 0:
      case 17:
      case 2:
      case 14:
      case 15:
        if ("function" === typeof b2)
          return b2.displayName || b2.name || null;
        if ("string" === typeof b2)
          return b2;
    }
    return null;
  }
  function Sa(a) {
    switch (typeof a) {
      case "boolean":
      case "number":
      case "string":
      case "undefined":
        return a;
      case "object":
        return a;
      default:
        return "";
    }
  }
  function Ta(a) {
    var b2 = a.type;
    return (a = a.nodeName) && "input" === a.toLowerCase() && ("checkbox" === b2 || "radio" === b2);
  }
  function Ua(a) {
    var b2 = Ta(a) ? "checked" : "value", c2 = Object.getOwnPropertyDescriptor(a.constructor.prototype, b2), d2 = "" + a[b2];
    if (!a.hasOwnProperty(b2) && "undefined" !== typeof c2 && "function" === typeof c2.get && "function" === typeof c2.set) {
      var e2 = c2.get, f2 = c2.set;
      Object.defineProperty(a, b2, { configurable: true, get: function() {
        return e2.call(this);
      }, set: function(a2) {
        d2 = "" + a2;
        f2.call(this, a2);
      } });
      Object.defineProperty(a, b2, { enumerable: c2.enumerable });
      return { getValue: function() {
        return d2;
      }, setValue: function(a2) {
        d2 = "" + a2;
      }, stopTracking: function() {
        a._valueTracker = null;
        delete a[b2];
      } };
    }
  }
  function Va(a) {
    a._valueTracker || (a._valueTracker = Ua(a));
  }
  function Wa(a) {
    if (!a)
      return false;
    var b2 = a._valueTracker;
    if (!b2)
      return true;
    var c2 = b2.getValue();
    var d2 = "";
    a && (d2 = Ta(a) ? a.checked ? "true" : "false" : a.value);
    a = d2;
    return a !== c2 ? (b2.setValue(a), true) : false;
  }
  function Xa(a) {
    a = a || ("undefined" !== typeof document ? document : void 0);
    if ("undefined" === typeof a)
      return null;
    try {
      return a.activeElement || a.body;
    } catch (b2) {
      return a.body;
    }
  }
  function Ya(a, b2) {
    var c2 = b2.checked;
    return A$2({}, b2, { defaultChecked: void 0, defaultValue: void 0, value: void 0, checked: null != c2 ? c2 : a._wrapperState.initialChecked });
  }
  function Za(a, b2) {
    var c2 = null == b2.defaultValue ? "" : b2.defaultValue, d2 = null != b2.checked ? b2.checked : b2.defaultChecked;
    c2 = Sa(null != b2.value ? b2.value : c2);
    a._wrapperState = { initialChecked: d2, initialValue: c2, controlled: "checkbox" === b2.type || "radio" === b2.type ? null != b2.checked : null != b2.value };
  }
  function ab(a, b2) {
    b2 = b2.checked;
    null != b2 && ta(a, "checked", b2, false);
  }
  function bb(a, b2) {
    ab(a, b2);
    var c2 = Sa(b2.value), d2 = b2.type;
    if (null != c2)
      if ("number" === d2) {
        if (0 === c2 && "" === a.value || a.value != c2)
          a.value = "" + c2;
      } else
        a.value !== "" + c2 && (a.value = "" + c2);
    else if ("submit" === d2 || "reset" === d2) {
      a.removeAttribute("value");
      return;
    }
    b2.hasOwnProperty("value") ? cb(a, b2.type, c2) : b2.hasOwnProperty("defaultValue") && cb(a, b2.type, Sa(b2.defaultValue));
    null == b2.checked && null != b2.defaultChecked && (a.defaultChecked = !!b2.defaultChecked);
  }
  function db(a, b2, c2) {
    if (b2.hasOwnProperty("value") || b2.hasOwnProperty("defaultValue")) {
      var d2 = b2.type;
      if (!("submit" !== d2 && "reset" !== d2 || void 0 !== b2.value && null !== b2.value))
        return;
      b2 = "" + a._wrapperState.initialValue;
      c2 || b2 === a.value || (a.value = b2);
      a.defaultValue = b2;
    }
    c2 = a.name;
    "" !== c2 && (a.name = "");
    a.defaultChecked = !!a._wrapperState.initialChecked;
    "" !== c2 && (a.name = c2);
  }
  function cb(a, b2, c2) {
    if ("number" !== b2 || Xa(a.ownerDocument) !== a)
      null == c2 ? a.defaultValue = "" + a._wrapperState.initialValue : a.defaultValue !== "" + c2 && (a.defaultValue = "" + c2);
  }
  var eb = Array.isArray;
  function fb(a, b2, c2, d2) {
    a = a.options;
    if (b2) {
      b2 = {};
      for (var e2 = 0; e2 < c2.length; e2++)
        b2["$" + c2[e2]] = true;
      for (c2 = 0; c2 < a.length; c2++)
        e2 = b2.hasOwnProperty("$" + a[c2].value), a[c2].selected !== e2 && (a[c2].selected = e2), e2 && d2 && (a[c2].defaultSelected = true);
    } else {
      c2 = "" + Sa(c2);
      b2 = null;
      for (e2 = 0; e2 < a.length; e2++) {
        if (a[e2].value === c2) {
          a[e2].selected = true;
          d2 && (a[e2].defaultSelected = true);
          return;
        }
        null !== b2 || a[e2].disabled || (b2 = a[e2]);
      }
      null !== b2 && (b2.selected = true);
    }
  }
  function gb(a, b2) {
    if (null != b2.dangerouslySetInnerHTML)
      throw Error(p$2(91));
    return A$2({}, b2, { value: void 0, defaultValue: void 0, children: "" + a._wrapperState.initialValue });
  }
  function hb(a, b2) {
    var c2 = b2.value;
    if (null == c2) {
      c2 = b2.children;
      b2 = b2.defaultValue;
      if (null != c2) {
        if (null != b2)
          throw Error(p$2(92));
        if (eb(c2)) {
          if (1 < c2.length)
            throw Error(p$2(93));
          c2 = c2[0];
        }
        b2 = c2;
      }
      null == b2 && (b2 = "");
      c2 = b2;
    }
    a._wrapperState = { initialValue: Sa(c2) };
  }
  function ib(a, b2) {
    var c2 = Sa(b2.value), d2 = Sa(b2.defaultValue);
    null != c2 && (c2 = "" + c2, c2 !== a.value && (a.value = c2), null == b2.defaultValue && a.defaultValue !== c2 && (a.defaultValue = c2));
    null != d2 && (a.defaultValue = "" + d2);
  }
  function jb(a) {
    var b2 = a.textContent;
    b2 === a._wrapperState.initialValue && "" !== b2 && null !== b2 && (a.value = b2);
  }
  function kb(a) {
    switch (a) {
      case "svg":
        return "http://www.w3.org/2000/svg";
      case "math":
        return "http://www.w3.org/1998/Math/MathML";
      default:
        return "http://www.w3.org/1999/xhtml";
    }
  }
  function lb(a, b2) {
    return null == a || "http://www.w3.org/1999/xhtml" === a ? kb(b2) : "http://www.w3.org/2000/svg" === a && "foreignObject" === b2 ? "http://www.w3.org/1999/xhtml" : a;
  }
  var mb, nb = function(a) {
    return "undefined" !== typeof MSApp && MSApp.execUnsafeLocalFunction ? function(b2, c2, d2, e2) {
      MSApp.execUnsafeLocalFunction(function() {
        return a(b2, c2, d2, e2);
      });
    } : a;
  }(function(a, b2) {
    if ("http://www.w3.org/2000/svg" !== a.namespaceURI || "innerHTML" in a)
      a.innerHTML = b2;
    else {
      mb = mb || document.createElement("div");
      mb.innerHTML = "<svg>" + b2.valueOf().toString() + "</svg>";
      for (b2 = mb.firstChild; a.firstChild; )
        a.removeChild(a.firstChild);
      for (; b2.firstChild; )
        a.appendChild(b2.firstChild);
    }
  });
  function ob(a, b2) {
    if (b2) {
      var c2 = a.firstChild;
      if (c2 && c2 === a.lastChild && 3 === c2.nodeType) {
        c2.nodeValue = b2;
        return;
      }
    }
    a.textContent = b2;
  }
  var pb = {
    animationIterationCount: true,
    aspectRatio: true,
    borderImageOutset: true,
    borderImageSlice: true,
    borderImageWidth: true,
    boxFlex: true,
    boxFlexGroup: true,
    boxOrdinalGroup: true,
    columnCount: true,
    columns: true,
    flex: true,
    flexGrow: true,
    flexPositive: true,
    flexShrink: true,
    flexNegative: true,
    flexOrder: true,
    gridArea: true,
    gridRow: true,
    gridRowEnd: true,
    gridRowSpan: true,
    gridRowStart: true,
    gridColumn: true,
    gridColumnEnd: true,
    gridColumnSpan: true,
    gridColumnStart: true,
    fontWeight: true,
    lineClamp: true,
    lineHeight: true,
    opacity: true,
    order: true,
    orphans: true,
    tabSize: true,
    widows: true,
    zIndex: true,
    zoom: true,
    fillOpacity: true,
    floodOpacity: true,
    stopOpacity: true,
    strokeDasharray: true,
    strokeDashoffset: true,
    strokeMiterlimit: true,
    strokeOpacity: true,
    strokeWidth: true
  }, qb = ["Webkit", "ms", "Moz", "O"];
  Object.keys(pb).forEach(function(a) {
    qb.forEach(function(b2) {
      b2 = b2 + a.charAt(0).toUpperCase() + a.substring(1);
      pb[b2] = pb[a];
    });
  });
  function rb(a, b2, c2) {
    return null == b2 || "boolean" === typeof b2 || "" === b2 ? "" : c2 || "number" !== typeof b2 || 0 === b2 || pb.hasOwnProperty(a) && pb[a] ? ("" + b2).trim() : b2 + "px";
  }
  function sb(a, b2) {
    a = a.style;
    for (var c2 in b2)
      if (b2.hasOwnProperty(c2)) {
        var d2 = 0 === c2.indexOf("--"), e2 = rb(c2, b2[c2], d2);
        "float" === c2 && (c2 = "cssFloat");
        d2 ? a.setProperty(c2, e2) : a[c2] = e2;
      }
  }
  var tb = A$2({ menuitem: true }, { area: true, base: true, br: true, col: true, embed: true, hr: true, img: true, input: true, keygen: true, link: true, meta: true, param: true, source: true, track: true, wbr: true });
  function ub(a, b2) {
    if (b2) {
      if (tb[a] && (null != b2.children || null != b2.dangerouslySetInnerHTML))
        throw Error(p$2(137, a));
      if (null != b2.dangerouslySetInnerHTML) {
        if (null != b2.children)
          throw Error(p$2(60));
        if ("object" !== typeof b2.dangerouslySetInnerHTML || !("__html" in b2.dangerouslySetInnerHTML))
          throw Error(p$2(61));
      }
      if (null != b2.style && "object" !== typeof b2.style)
        throw Error(p$2(62));
    }
  }
  function vb(a, b2) {
    if (-1 === a.indexOf("-"))
      return "string" === typeof b2.is;
    switch (a) {
      case "annotation-xml":
      case "color-profile":
      case "font-face":
      case "font-face-src":
      case "font-face-uri":
      case "font-face-format":
      case "font-face-name":
      case "missing-glyph":
        return false;
      default:
        return true;
    }
  }
  var wb = null;
  function xb(a) {
    a = a.target || a.srcElement || window;
    a.correspondingUseElement && (a = a.correspondingUseElement);
    return 3 === a.nodeType ? a.parentNode : a;
  }
  var yb = null, zb = null, Ab = null;
  function Bb(a) {
    if (a = Cb(a)) {
      if ("function" !== typeof yb)
        throw Error(p$2(280));
      var b2 = a.stateNode;
      b2 && (b2 = Db(b2), yb(a.stateNode, a.type, b2));
    }
  }
  function Eb(a) {
    zb ? Ab ? Ab.push(a) : Ab = [a] : zb = a;
  }
  function Fb() {
    if (zb) {
      var a = zb, b2 = Ab;
      Ab = zb = null;
      Bb(a);
      if (b2)
        for (a = 0; a < b2.length; a++)
          Bb(b2[a]);
    }
  }
  function Gb(a, b2) {
    return a(b2);
  }
  function Hb() {
  }
  var Ib = false;
  function Jb(a, b2, c2) {
    if (Ib)
      return a(b2, c2);
    Ib = true;
    try {
      return Gb(a, b2, c2);
    } finally {
      if (Ib = false, null !== zb || null !== Ab)
        Hb(), Fb();
    }
  }
  function Kb(a, b2) {
    var c2 = a.stateNode;
    if (null === c2)
      return null;
    var d2 = Db(c2);
    if (null === d2)
      return null;
    c2 = d2[b2];
    a:
      switch (b2) {
        case "onClick":
        case "onClickCapture":
        case "onDoubleClick":
        case "onDoubleClickCapture":
        case "onMouseDown":
        case "onMouseDownCapture":
        case "onMouseMove":
        case "onMouseMoveCapture":
        case "onMouseUp":
        case "onMouseUpCapture":
        case "onMouseEnter":
          (d2 = !d2.disabled) || (a = a.type, d2 = !("button" === a || "input" === a || "select" === a || "textarea" === a));
          a = !d2;
          break a;
        default:
          a = false;
      }
    if (a)
      return null;
    if (c2 && "function" !== typeof c2)
      throw Error(p$2(231, b2, typeof c2));
    return c2;
  }
  var Lb = false;
  if (ia)
    try {
      var Mb = {};
      Object.defineProperty(Mb, "passive", { get: function() {
        Lb = true;
      } });
      window.addEventListener("test", Mb, Mb);
      window.removeEventListener("test", Mb, Mb);
    } catch (a) {
      Lb = false;
    }
  function Nb(a, b2, c2, d2, e2, f2, g2, h2, k2) {
    var l2 = Array.prototype.slice.call(arguments, 3);
    try {
      b2.apply(c2, l2);
    } catch (m2) {
      this.onError(m2);
    }
  }
  var Ob = false, Pb = null, Qb = false, Rb = null, Sb = { onError: function(a) {
    Ob = true;
    Pb = a;
  } };
  function Tb(a, b2, c2, d2, e2, f2, g2, h2, k2) {
    Ob = false;
    Pb = null;
    Nb.apply(Sb, arguments);
  }
  function Ub(a, b2, c2, d2, e2, f2, g2, h2, k2) {
    Tb.apply(this, arguments);
    if (Ob) {
      if (Ob) {
        var l2 = Pb;
        Ob = false;
        Pb = null;
      } else
        throw Error(p$2(198));
      Qb || (Qb = true, Rb = l2);
    }
  }
  function Vb(a) {
    var b2 = a, c2 = a;
    if (a.alternate)
      for (; b2.return; )
        b2 = b2.return;
    else {
      a = b2;
      do
        b2 = a, 0 !== (b2.flags & 4098) && (c2 = b2.return), a = b2.return;
      while (a);
    }
    return 3 === b2.tag ? c2 : null;
  }
  function Wb(a) {
    if (13 === a.tag) {
      var b2 = a.memoizedState;
      null === b2 && (a = a.alternate, null !== a && (b2 = a.memoizedState));
      if (null !== b2)
        return b2.dehydrated;
    }
    return null;
  }
  function Xb(a) {
    if (Vb(a) !== a)
      throw Error(p$2(188));
  }
  function Yb(a) {
    var b2 = a.alternate;
    if (!b2) {
      b2 = Vb(a);
      if (null === b2)
        throw Error(p$2(188));
      return b2 !== a ? null : a;
    }
    for (var c2 = a, d2 = b2; ; ) {
      var e2 = c2.return;
      if (null === e2)
        break;
      var f2 = e2.alternate;
      if (null === f2) {
        d2 = e2.return;
        if (null !== d2) {
          c2 = d2;
          continue;
        }
        break;
      }
      if (e2.child === f2.child) {
        for (f2 = e2.child; f2; ) {
          if (f2 === c2)
            return Xb(e2), a;
          if (f2 === d2)
            return Xb(e2), b2;
          f2 = f2.sibling;
        }
        throw Error(p$2(188));
      }
      if (c2.return !== d2.return)
        c2 = e2, d2 = f2;
      else {
        for (var g2 = false, h2 = e2.child; h2; ) {
          if (h2 === c2) {
            g2 = true;
            c2 = e2;
            d2 = f2;
            break;
          }
          if (h2 === d2) {
            g2 = true;
            d2 = e2;
            c2 = f2;
            break;
          }
          h2 = h2.sibling;
        }
        if (!g2) {
          for (h2 = f2.child; h2; ) {
            if (h2 === c2) {
              g2 = true;
              c2 = f2;
              d2 = e2;
              break;
            }
            if (h2 === d2) {
              g2 = true;
              d2 = f2;
              c2 = e2;
              break;
            }
            h2 = h2.sibling;
          }
          if (!g2)
            throw Error(p$2(189));
        }
      }
      if (c2.alternate !== d2)
        throw Error(p$2(190));
    }
    if (3 !== c2.tag)
      throw Error(p$2(188));
    return c2.stateNode.current === c2 ? a : b2;
  }
  function Zb(a) {
    a = Yb(a);
    return null !== a ? $b(a) : null;
  }
  function $b(a) {
    if (5 === a.tag || 6 === a.tag)
      return a;
    for (a = a.child; null !== a; ) {
      var b2 = $b(a);
      if (null !== b2)
        return b2;
      a = a.sibling;
    }
    return null;
  }
  var ac = ca.unstable_scheduleCallback, bc = ca.unstable_cancelCallback, cc = ca.unstable_shouldYield, dc = ca.unstable_requestPaint, B$1 = ca.unstable_now, ec = ca.unstable_getCurrentPriorityLevel, fc = ca.unstable_ImmediatePriority, gc = ca.unstable_UserBlockingPriority, hc = ca.unstable_NormalPriority, ic = ca.unstable_LowPriority, jc = ca.unstable_IdlePriority, kc = null, lc = null;
  function mc(a) {
    if (lc && "function" === typeof lc.onCommitFiberRoot)
      try {
        lc.onCommitFiberRoot(kc, a, void 0, 128 === (a.current.flags & 128));
      } catch (b2) {
      }
  }
  var oc = Math.clz32 ? Math.clz32 : nc, pc = Math.log, qc = Math.LN2;
  function nc(a) {
    a >>>= 0;
    return 0 === a ? 32 : 31 - (pc(a) / qc | 0) | 0;
  }
  var rc = 64, sc = 4194304;
  function tc(a) {
    switch (a & -a) {
      case 1:
        return 1;
      case 2:
        return 2;
      case 4:
        return 4;
      case 8:
        return 8;
      case 16:
        return 16;
      case 32:
        return 32;
      case 64:
      case 128:
      case 256:
      case 512:
      case 1024:
      case 2048:
      case 4096:
      case 8192:
      case 16384:
      case 32768:
      case 65536:
      case 131072:
      case 262144:
      case 524288:
      case 1048576:
      case 2097152:
        return a & 4194240;
      case 4194304:
      case 8388608:
      case 16777216:
      case 33554432:
      case 67108864:
        return a & 130023424;
      case 134217728:
        return 134217728;
      case 268435456:
        return 268435456;
      case 536870912:
        return 536870912;
      case 1073741824:
        return 1073741824;
      default:
        return a;
    }
  }
  function uc(a, b2) {
    var c2 = a.pendingLanes;
    if (0 === c2)
      return 0;
    var d2 = 0, e2 = a.suspendedLanes, f2 = a.pingedLanes, g2 = c2 & 268435455;
    if (0 !== g2) {
      var h2 = g2 & ~e2;
      0 !== h2 ? d2 = tc(h2) : (f2 &= g2, 0 !== f2 && (d2 = tc(f2)));
    } else
      g2 = c2 & ~e2, 0 !== g2 ? d2 = tc(g2) : 0 !== f2 && (d2 = tc(f2));
    if (0 === d2)
      return 0;
    if (0 !== b2 && b2 !== d2 && 0 === (b2 & e2) && (e2 = d2 & -d2, f2 = b2 & -b2, e2 >= f2 || 16 === e2 && 0 !== (f2 & 4194240)))
      return b2;
    0 !== (d2 & 4) && (d2 |= c2 & 16);
    b2 = a.entangledLanes;
    if (0 !== b2)
      for (a = a.entanglements, b2 &= d2; 0 < b2; )
        c2 = 31 - oc(b2), e2 = 1 << c2, d2 |= a[c2], b2 &= ~e2;
    return d2;
  }
  function vc(a, b2) {
    switch (a) {
      case 1:
      case 2:
      case 4:
        return b2 + 250;
      case 8:
      case 16:
      case 32:
      case 64:
      case 128:
      case 256:
      case 512:
      case 1024:
      case 2048:
      case 4096:
      case 8192:
      case 16384:
      case 32768:
      case 65536:
      case 131072:
      case 262144:
      case 524288:
      case 1048576:
      case 2097152:
        return b2 + 5e3;
      case 4194304:
      case 8388608:
      case 16777216:
      case 33554432:
      case 67108864:
        return -1;
      case 134217728:
      case 268435456:
      case 536870912:
      case 1073741824:
        return -1;
      default:
        return -1;
    }
  }
  function wc(a, b2) {
    for (var c2 = a.suspendedLanes, d2 = a.pingedLanes, e2 = a.expirationTimes, f2 = a.pendingLanes; 0 < f2; ) {
      var g2 = 31 - oc(f2), h2 = 1 << g2, k2 = e2[g2];
      if (-1 === k2) {
        if (0 === (h2 & c2) || 0 !== (h2 & d2))
          e2[g2] = vc(h2, b2);
      } else
        k2 <= b2 && (a.expiredLanes |= h2);
      f2 &= ~h2;
    }
  }
  function xc(a) {
    a = a.pendingLanes & -1073741825;
    return 0 !== a ? a : a & 1073741824 ? 1073741824 : 0;
  }
  function yc() {
    var a = rc;
    rc <<= 1;
    0 === (rc & 4194240) && (rc = 64);
    return a;
  }
  function zc(a) {
    for (var b2 = [], c2 = 0; 31 > c2; c2++)
      b2.push(a);
    return b2;
  }
  function Ac(a, b2, c2) {
    a.pendingLanes |= b2;
    536870912 !== b2 && (a.suspendedLanes = 0, a.pingedLanes = 0);
    a = a.eventTimes;
    b2 = 31 - oc(b2);
    a[b2] = c2;
  }
  function Bc(a, b2) {
    var c2 = a.pendingLanes & ~b2;
    a.pendingLanes = b2;
    a.suspendedLanes = 0;
    a.pingedLanes = 0;
    a.expiredLanes &= b2;
    a.mutableReadLanes &= b2;
    a.entangledLanes &= b2;
    b2 = a.entanglements;
    var d2 = a.eventTimes;
    for (a = a.expirationTimes; 0 < c2; ) {
      var e2 = 31 - oc(c2), f2 = 1 << e2;
      b2[e2] = 0;
      d2[e2] = -1;
      a[e2] = -1;
      c2 &= ~f2;
    }
  }
  function Cc(a, b2) {
    var c2 = a.entangledLanes |= b2;
    for (a = a.entanglements; c2; ) {
      var d2 = 31 - oc(c2), e2 = 1 << d2;
      e2 & b2 | a[d2] & b2 && (a[d2] |= b2);
      c2 &= ~e2;
    }
  }
  var C$1 = 0;
  function Dc(a) {
    a &= -a;
    return 1 < a ? 4 < a ? 0 !== (a & 268435455) ? 16 : 536870912 : 4 : 1;
  }
  var Ec, Fc, Gc, Hc, Ic, Jc = false, Kc = [], Lc = null, Mc = null, Nc = null, Oc = /* @__PURE__ */ new Map(), Pc = /* @__PURE__ */ new Map(), Qc = [], Rc = "mousedown mouseup touchcancel touchend touchstart auxclick dblclick pointercancel pointerdown pointerup dragend dragstart drop compositionend compositionstart keydown keypress keyup input textInput copy cut paste click change contextmenu reset submit".split(" ");
  function Sc(a, b2) {
    switch (a) {
      case "focusin":
      case "focusout":
        Lc = null;
        break;
      case "dragenter":
      case "dragleave":
        Mc = null;
        break;
      case "mouseover":
      case "mouseout":
        Nc = null;
        break;
      case "pointerover":
      case "pointerout":
        Oc.delete(b2.pointerId);
        break;
      case "gotpointercapture":
      case "lostpointercapture":
        Pc.delete(b2.pointerId);
    }
  }
  function Tc(a, b2, c2, d2, e2, f2) {
    if (null === a || a.nativeEvent !== f2)
      return a = { blockedOn: b2, domEventName: c2, eventSystemFlags: d2, nativeEvent: f2, targetContainers: [e2] }, null !== b2 && (b2 = Cb(b2), null !== b2 && Fc(b2)), a;
    a.eventSystemFlags |= d2;
    b2 = a.targetContainers;
    null !== e2 && -1 === b2.indexOf(e2) && b2.push(e2);
    return a;
  }
  function Uc(a, b2, c2, d2, e2) {
    switch (b2) {
      case "focusin":
        return Lc = Tc(Lc, a, b2, c2, d2, e2), true;
      case "dragenter":
        return Mc = Tc(Mc, a, b2, c2, d2, e2), true;
      case "mouseover":
        return Nc = Tc(Nc, a, b2, c2, d2, e2), true;
      case "pointerover":
        var f2 = e2.pointerId;
        Oc.set(f2, Tc(Oc.get(f2) || null, a, b2, c2, d2, e2));
        return true;
      case "gotpointercapture":
        return f2 = e2.pointerId, Pc.set(f2, Tc(Pc.get(f2) || null, a, b2, c2, d2, e2)), true;
    }
    return false;
  }
  function Vc(a) {
    var b2 = Wc(a.target);
    if (null !== b2) {
      var c2 = Vb(b2);
      if (null !== c2) {
        if (b2 = c2.tag, 13 === b2) {
          if (b2 = Wb(c2), null !== b2) {
            a.blockedOn = b2;
            Ic(a.priority, function() {
              Gc(c2);
            });
            return;
          }
        } else if (3 === b2 && c2.stateNode.current.memoizedState.isDehydrated) {
          a.blockedOn = 3 === c2.tag ? c2.stateNode.containerInfo : null;
          return;
        }
      }
    }
    a.blockedOn = null;
  }
  function Xc(a) {
    if (null !== a.blockedOn)
      return false;
    for (var b2 = a.targetContainers; 0 < b2.length; ) {
      var c2 = Yc(a.domEventName, a.eventSystemFlags, b2[0], a.nativeEvent);
      if (null === c2) {
        c2 = a.nativeEvent;
        var d2 = new c2.constructor(c2.type, c2);
        wb = d2;
        c2.target.dispatchEvent(d2);
        wb = null;
      } else
        return b2 = Cb(c2), null !== b2 && Fc(b2), a.blockedOn = c2, false;
      b2.shift();
    }
    return true;
  }
  function Zc(a, b2, c2) {
    Xc(a) && c2.delete(b2);
  }
  function $c() {
    Jc = false;
    null !== Lc && Xc(Lc) && (Lc = null);
    null !== Mc && Xc(Mc) && (Mc = null);
    null !== Nc && Xc(Nc) && (Nc = null);
    Oc.forEach(Zc);
    Pc.forEach(Zc);
  }
  function ad(a, b2) {
    a.blockedOn === b2 && (a.blockedOn = null, Jc || (Jc = true, ca.unstable_scheduleCallback(ca.unstable_NormalPriority, $c)));
  }
  function bd(a) {
    function b2(b3) {
      return ad(b3, a);
    }
    if (0 < Kc.length) {
      ad(Kc[0], a);
      for (var c2 = 1; c2 < Kc.length; c2++) {
        var d2 = Kc[c2];
        d2.blockedOn === a && (d2.blockedOn = null);
      }
    }
    null !== Lc && ad(Lc, a);
    null !== Mc && ad(Mc, a);
    null !== Nc && ad(Nc, a);
    Oc.forEach(b2);
    Pc.forEach(b2);
    for (c2 = 0; c2 < Qc.length; c2++)
      d2 = Qc[c2], d2.blockedOn === a && (d2.blockedOn = null);
    for (; 0 < Qc.length && (c2 = Qc[0], null === c2.blockedOn); )
      Vc(c2), null === c2.blockedOn && Qc.shift();
  }
  var cd = ua.ReactCurrentBatchConfig, dd = true;
  function ed(a, b2, c2, d2) {
    var e2 = C$1, f2 = cd.transition;
    cd.transition = null;
    try {
      C$1 = 1, fd(a, b2, c2, d2);
    } finally {
      C$1 = e2, cd.transition = f2;
    }
  }
  function gd(a, b2, c2, d2) {
    var e2 = C$1, f2 = cd.transition;
    cd.transition = null;
    try {
      C$1 = 4, fd(a, b2, c2, d2);
    } finally {
      C$1 = e2, cd.transition = f2;
    }
  }
  function fd(a, b2, c2, d2) {
    if (dd) {
      var e2 = Yc(a, b2, c2, d2);
      if (null === e2)
        hd(a, b2, d2, id$2, c2), Sc(a, d2);
      else if (Uc(e2, a, b2, c2, d2))
        d2.stopPropagation();
      else if (Sc(a, d2), b2 & 4 && -1 < Rc.indexOf(a)) {
        for (; null !== e2; ) {
          var f2 = Cb(e2);
          null !== f2 && Ec(f2);
          f2 = Yc(a, b2, c2, d2);
          null === f2 && hd(a, b2, d2, id$2, c2);
          if (f2 === e2)
            break;
          e2 = f2;
        }
        null !== e2 && d2.stopPropagation();
      } else
        hd(a, b2, d2, null, c2);
    }
  }
  var id$2 = null;
  function Yc(a, b2, c2, d2) {
    id$2 = null;
    a = xb(d2);
    a = Wc(a);
    if (null !== a)
      if (b2 = Vb(a), null === b2)
        a = null;
      else if (c2 = b2.tag, 13 === c2) {
        a = Wb(b2);
        if (null !== a)
          return a;
        a = null;
      } else if (3 === c2) {
        if (b2.stateNode.current.memoizedState.isDehydrated)
          return 3 === b2.tag ? b2.stateNode.containerInfo : null;
        a = null;
      } else
        b2 !== a && (a = null);
    id$2 = a;
    return null;
  }
  function jd(a) {
    switch (a) {
      case "cancel":
      case "click":
      case "close":
      case "contextmenu":
      case "copy":
      case "cut":
      case "auxclick":
      case "dblclick":
      case "dragend":
      case "dragstart":
      case "drop":
      case "focusin":
      case "focusout":
      case "input":
      case "invalid":
      case "keydown":
      case "keypress":
      case "keyup":
      case "mousedown":
      case "mouseup":
      case "paste":
      case "pause":
      case "play":
      case "pointercancel":
      case "pointerdown":
      case "pointerup":
      case "ratechange":
      case "reset":
      case "resize":
      case "seeked":
      case "submit":
      case "touchcancel":
      case "touchend":
      case "touchstart":
      case "volumechange":
      case "change":
      case "selectionchange":
      case "textInput":
      case "compositionstart":
      case "compositionend":
      case "compositionupdate":
      case "beforeblur":
      case "afterblur":
      case "beforeinput":
      case "blur":
      case "fullscreenchange":
      case "focus":
      case "hashchange":
      case "popstate":
      case "select":
      case "selectstart":
        return 1;
      case "drag":
      case "dragenter":
      case "dragexit":
      case "dragleave":
      case "dragover":
      case "mousemove":
      case "mouseout":
      case "mouseover":
      case "pointermove":
      case "pointerout":
      case "pointerover":
      case "scroll":
      case "toggle":
      case "touchmove":
      case "wheel":
      case "mouseenter":
      case "mouseleave":
      case "pointerenter":
      case "pointerleave":
        return 4;
      case "message":
        switch (ec()) {
          case fc:
            return 1;
          case gc:
            return 4;
          case hc:
          case ic:
            return 16;
          case jc:
            return 536870912;
          default:
            return 16;
        }
      default:
        return 16;
    }
  }
  var kd = null, ld = null, md = null;
  function nd() {
    if (md)
      return md;
    var a, b2 = ld, c2 = b2.length, d2, e2 = "value" in kd ? kd.value : kd.textContent, f2 = e2.length;
    for (a = 0; a < c2 && b2[a] === e2[a]; a++)
      ;
    var g2 = c2 - a;
    for (d2 = 1; d2 <= g2 && b2[c2 - d2] === e2[f2 - d2]; d2++)
      ;
    return md = e2.slice(a, 1 < d2 ? 1 - d2 : void 0);
  }
  function od(a) {
    var b2 = a.keyCode;
    "charCode" in a ? (a = a.charCode, 0 === a && 13 === b2 && (a = 13)) : a = b2;
    10 === a && (a = 13);
    return 32 <= a || 13 === a ? a : 0;
  }
  function pd() {
    return true;
  }
  function qd() {
    return false;
  }
  function rd(a) {
    function b2(b3, d2, e2, f2, g2) {
      this._reactName = b3;
      this._targetInst = e2;
      this.type = d2;
      this.nativeEvent = f2;
      this.target = g2;
      this.currentTarget = null;
      for (var c2 in a)
        a.hasOwnProperty(c2) && (b3 = a[c2], this[c2] = b3 ? b3(f2) : f2[c2]);
      this.isDefaultPrevented = (null != f2.defaultPrevented ? f2.defaultPrevented : false === f2.returnValue) ? pd : qd;
      this.isPropagationStopped = qd;
      return this;
    }
    A$2(b2.prototype, { preventDefault: function() {
      this.defaultPrevented = true;
      var a2 = this.nativeEvent;
      a2 && (a2.preventDefault ? a2.preventDefault() : "unknown" !== typeof a2.returnValue && (a2.returnValue = false), this.isDefaultPrevented = pd);
    }, stopPropagation: function() {
      var a2 = this.nativeEvent;
      a2 && (a2.stopPropagation ? a2.stopPropagation() : "unknown" !== typeof a2.cancelBubble && (a2.cancelBubble = true), this.isPropagationStopped = pd);
    }, persist: function() {
    }, isPersistent: pd });
    return b2;
  }
  var sd = { eventPhase: 0, bubbles: 0, cancelable: 0, timeStamp: function(a) {
    return a.timeStamp || Date.now();
  }, defaultPrevented: 0, isTrusted: 0 }, td = rd(sd), ud = A$2({}, sd, { view: 0, detail: 0 }), vd = rd(ud), wd, xd, yd, Ad = A$2({}, ud, { screenX: 0, screenY: 0, clientX: 0, clientY: 0, pageX: 0, pageY: 0, ctrlKey: 0, shiftKey: 0, altKey: 0, metaKey: 0, getModifierState: zd, button: 0, buttons: 0, relatedTarget: function(a) {
    return void 0 === a.relatedTarget ? a.fromElement === a.srcElement ? a.toElement : a.fromElement : a.relatedTarget;
  }, movementX: function(a) {
    if ("movementX" in a)
      return a.movementX;
    a !== yd && (yd && "mousemove" === a.type ? (wd = a.screenX - yd.screenX, xd = a.screenY - yd.screenY) : xd = wd = 0, yd = a);
    return wd;
  }, movementY: function(a) {
    return "movementY" in a ? a.movementY : xd;
  } }), Bd = rd(Ad), Cd = A$2({}, Ad, { dataTransfer: 0 }), Dd = rd(Cd), Ed = A$2({}, ud, { relatedTarget: 0 }), Fd = rd(Ed), Gd = A$2({}, sd, { animationName: 0, elapsedTime: 0, pseudoElement: 0 }), Hd = rd(Gd), Id = A$2({}, sd, { clipboardData: function(a) {
    return "clipboardData" in a ? a.clipboardData : window.clipboardData;
  } }), Jd = rd(Id), Kd = A$2({}, sd, { data: 0 }), Ld = rd(Kd), Md = {
    Esc: "Escape",
    Spacebar: " ",
    Left: "ArrowLeft",
    Up: "ArrowUp",
    Right: "ArrowRight",
    Down: "ArrowDown",
    Del: "Delete",
    Win: "OS",
    Menu: "ContextMenu",
    Apps: "ContextMenu",
    Scroll: "ScrollLock",
    MozPrintableKey: "Unidentified"
  }, Nd = {
    8: "Backspace",
    9: "Tab",
    12: "Clear",
    13: "Enter",
    16: "Shift",
    17: "Control",
    18: "Alt",
    19: "Pause",
    20: "CapsLock",
    27: "Escape",
    32: " ",
    33: "PageUp",
    34: "PageDown",
    35: "End",
    36: "Home",
    37: "ArrowLeft",
    38: "ArrowUp",
    39: "ArrowRight",
    40: "ArrowDown",
    45: "Insert",
    46: "Delete",
    112: "F1",
    113: "F2",
    114: "F3",
    115: "F4",
    116: "F5",
    117: "F6",
    118: "F7",
    119: "F8",
    120: "F9",
    121: "F10",
    122: "F11",
    123: "F12",
    144: "NumLock",
    145: "ScrollLock",
    224: "Meta"
  }, Od = { Alt: "altKey", Control: "ctrlKey", Meta: "metaKey", Shift: "shiftKey" };
  function Pd(a) {
    var b2 = this.nativeEvent;
    return b2.getModifierState ? b2.getModifierState(a) : (a = Od[a]) ? !!b2[a] : false;
  }
  function zd() {
    return Pd;
  }
  var Qd = A$2({}, ud, { key: function(a) {
    if (a.key) {
      var b2 = Md[a.key] || a.key;
      if ("Unidentified" !== b2)
        return b2;
    }
    return "keypress" === a.type ? (a = od(a), 13 === a ? "Enter" : String.fromCharCode(a)) : "keydown" === a.type || "keyup" === a.type ? Nd[a.keyCode] || "Unidentified" : "";
  }, code: 0, location: 0, ctrlKey: 0, shiftKey: 0, altKey: 0, metaKey: 0, repeat: 0, locale: 0, getModifierState: zd, charCode: function(a) {
    return "keypress" === a.type ? od(a) : 0;
  }, keyCode: function(a) {
    return "keydown" === a.type || "keyup" === a.type ? a.keyCode : 0;
  }, which: function(a) {
    return "keypress" === a.type ? od(a) : "keydown" === a.type || "keyup" === a.type ? a.keyCode : 0;
  } }), Rd = rd(Qd), Sd = A$2({}, Ad, { pointerId: 0, width: 0, height: 0, pressure: 0, tangentialPressure: 0, tiltX: 0, tiltY: 0, twist: 0, pointerType: 0, isPrimary: 0 }), Td$1 = rd(Sd), Ud = A$2({}, ud, { touches: 0, targetTouches: 0, changedTouches: 0, altKey: 0, metaKey: 0, ctrlKey: 0, shiftKey: 0, getModifierState: zd }), Vd = rd(Ud), Wd = A$2({}, sd, { propertyName: 0, elapsedTime: 0, pseudoElement: 0 }), Xd = rd(Wd), Yd = A$2({}, Ad, {
    deltaX: function(a) {
      return "deltaX" in a ? a.deltaX : "wheelDeltaX" in a ? -a.wheelDeltaX : 0;
    },
    deltaY: function(a) {
      return "deltaY" in a ? a.deltaY : "wheelDeltaY" in a ? -a.wheelDeltaY : "wheelDelta" in a ? -a.wheelDelta : 0;
    },
    deltaZ: 0,
    deltaMode: 0
  }), Zd = rd(Yd), $d = [9, 13, 27, 32], ae$1 = ia && "CompositionEvent" in window, be$1 = null;
  ia && "documentMode" in document && (be$1 = document.documentMode);
  var ce$1 = ia && "TextEvent" in window && !be$1, de = ia && (!ae$1 || be$1 && 8 < be$1 && 11 >= be$1), ee$1 = String.fromCharCode(32), fe$1 = false;
  function ge$1(a, b2) {
    switch (a) {
      case "keyup":
        return -1 !== $d.indexOf(b2.keyCode);
      case "keydown":
        return 229 !== b2.keyCode;
      case "keypress":
      case "mousedown":
      case "focusout":
        return true;
      default:
        return false;
    }
  }
  function he$1(a) {
    a = a.detail;
    return "object" === typeof a && "data" in a ? a.data : null;
  }
  var ie$1 = false;
  function je$1(a, b2) {
    switch (a) {
      case "compositionend":
        return he$1(b2);
      case "keypress":
        if (32 !== b2.which)
          return null;
        fe$1 = true;
        return ee$1;
      case "textInput":
        return a = b2.data, a === ee$1 && fe$1 ? null : a;
      default:
        return null;
    }
  }
  function ke$1(a, b2) {
    if (ie$1)
      return "compositionend" === a || !ae$1 && ge$1(a, b2) ? (a = nd(), md = ld = kd = null, ie$1 = false, a) : null;
    switch (a) {
      case "paste":
        return null;
      case "keypress":
        if (!(b2.ctrlKey || b2.altKey || b2.metaKey) || b2.ctrlKey && b2.altKey) {
          if (b2.char && 1 < b2.char.length)
            return b2.char;
          if (b2.which)
            return String.fromCharCode(b2.which);
        }
        return null;
      case "compositionend":
        return de && "ko" !== b2.locale ? null : b2.data;
      default:
        return null;
    }
  }
  var le$1 = { color: true, date: true, datetime: true, "datetime-local": true, email: true, month: true, number: true, password: true, range: true, search: true, tel: true, text: true, time: true, url: true, week: true };
  function me(a) {
    var b2 = a && a.nodeName && a.nodeName.toLowerCase();
    return "input" === b2 ? !!le$1[a.type] : "textarea" === b2 ? true : false;
  }
  function ne$1(a, b2, c2, d2) {
    Eb(d2);
    b2 = oe$1(b2, "onChange");
    0 < b2.length && (c2 = new td("onChange", "change", null, c2, d2), a.push({ event: c2, listeners: b2 }));
  }
  var pe = null, qe$1 = null;
  function re$1(a) {
    se$1(a, 0);
  }
  function te$1(a) {
    var b2 = ue$1(a);
    if (Wa(b2))
      return a;
  }
  function ve$1(a, b2) {
    if ("change" === a)
      return b2;
  }
  var we$1 = false;
  if (ia) {
    var xe$1;
    if (ia) {
      var ye$1 = "oninput" in document;
      if (!ye$1) {
        var ze = document.createElement("div");
        ze.setAttribute("oninput", "return;");
        ye$1 = "function" === typeof ze.oninput;
      }
      xe$1 = ye$1;
    } else
      xe$1 = false;
    we$1 = xe$1 && (!document.documentMode || 9 < document.documentMode);
  }
  function Ae$1() {
    pe && (pe.detachEvent("onpropertychange", Be), qe$1 = pe = null);
  }
  function Be(a) {
    if ("value" === a.propertyName && te$1(qe$1)) {
      var b2 = [];
      ne$1(b2, qe$1, a, xb(a));
      Jb(re$1, b2);
    }
  }
  function Ce$1(a, b2, c2) {
    "focusin" === a ? (Ae$1(), pe = b2, qe$1 = c2, pe.attachEvent("onpropertychange", Be)) : "focusout" === a && Ae$1();
  }
  function De$1(a) {
    if ("selectionchange" === a || "keyup" === a || "keydown" === a)
      return te$1(qe$1);
  }
  function Ee$1(a, b2) {
    if ("click" === a)
      return te$1(b2);
  }
  function Fe$1(a, b2) {
    if ("input" === a || "change" === a)
      return te$1(b2);
  }
  function Ge(a, b2) {
    return a === b2 && (0 !== a || 1 / a === 1 / b2) || a !== a && b2 !== b2;
  }
  var He$1 = "function" === typeof Object.is ? Object.is : Ge;
  function Ie$1(a, b2) {
    if (He$1(a, b2))
      return true;
    if ("object" !== typeof a || null === a || "object" !== typeof b2 || null === b2)
      return false;
    var c2 = Object.keys(a), d2 = Object.keys(b2);
    if (c2.length !== d2.length)
      return false;
    for (d2 = 0; d2 < c2.length; d2++) {
      var e2 = c2[d2];
      if (!ja.call(b2, e2) || !He$1(a[e2], b2[e2]))
        return false;
    }
    return true;
  }
  function Je$1(a) {
    for (; a && a.firstChild; )
      a = a.firstChild;
    return a;
  }
  function Ke$1(a, b2) {
    var c2 = Je$1(a);
    a = 0;
    for (var d2; c2; ) {
      if (3 === c2.nodeType) {
        d2 = a + c2.textContent.length;
        if (a <= b2 && d2 >= b2)
          return { node: c2, offset: b2 - a };
        a = d2;
      }
      a: {
        for (; c2; ) {
          if (c2.nextSibling) {
            c2 = c2.nextSibling;
            break a;
          }
          c2 = c2.parentNode;
        }
        c2 = void 0;
      }
      c2 = Je$1(c2);
    }
  }
  function Le$1(a, b2) {
    return a && b2 ? a === b2 ? true : a && 3 === a.nodeType ? false : b2 && 3 === b2.nodeType ? Le$1(a, b2.parentNode) : "contains" in a ? a.contains(b2) : a.compareDocumentPosition ? !!(a.compareDocumentPosition(b2) & 16) : false : false;
  }
  function Me$1() {
    for (var a = window, b2 = Xa(); b2 instanceof a.HTMLIFrameElement; ) {
      try {
        var c2 = "string" === typeof b2.contentWindow.location.href;
      } catch (d2) {
        c2 = false;
      }
      if (c2)
        a = b2.contentWindow;
      else
        break;
      b2 = Xa(a.document);
    }
    return b2;
  }
  function Ne$1(a) {
    var b2 = a && a.nodeName && a.nodeName.toLowerCase();
    return b2 && ("input" === b2 && ("text" === a.type || "search" === a.type || "tel" === a.type || "url" === a.type || "password" === a.type) || "textarea" === b2 || "true" === a.contentEditable);
  }
  function Oe$1(a) {
    var b2 = Me$1(), c2 = a.focusedElem, d2 = a.selectionRange;
    if (b2 !== c2 && c2 && c2.ownerDocument && Le$1(c2.ownerDocument.documentElement, c2)) {
      if (null !== d2 && Ne$1(c2)) {
        if (b2 = d2.start, a = d2.end, void 0 === a && (a = b2), "selectionStart" in c2)
          c2.selectionStart = b2, c2.selectionEnd = Math.min(a, c2.value.length);
        else if (a = (b2 = c2.ownerDocument || document) && b2.defaultView || window, a.getSelection) {
          a = a.getSelection();
          var e2 = c2.textContent.length, f2 = Math.min(d2.start, e2);
          d2 = void 0 === d2.end ? f2 : Math.min(d2.end, e2);
          !a.extend && f2 > d2 && (e2 = d2, d2 = f2, f2 = e2);
          e2 = Ke$1(c2, f2);
          var g2 = Ke$1(
            c2,
            d2
          );
          e2 && g2 && (1 !== a.rangeCount || a.anchorNode !== e2.node || a.anchorOffset !== e2.offset || a.focusNode !== g2.node || a.focusOffset !== g2.offset) && (b2 = b2.createRange(), b2.setStart(e2.node, e2.offset), a.removeAllRanges(), f2 > d2 ? (a.addRange(b2), a.extend(g2.node, g2.offset)) : (b2.setEnd(g2.node, g2.offset), a.addRange(b2)));
        }
      }
      b2 = [];
      for (a = c2; a = a.parentNode; )
        1 === a.nodeType && b2.push({ element: a, left: a.scrollLeft, top: a.scrollTop });
      "function" === typeof c2.focus && c2.focus();
      for (c2 = 0; c2 < b2.length; c2++)
        a = b2[c2], a.element.scrollLeft = a.left, a.element.scrollTop = a.top;
    }
  }
  var Pe$1 = ia && "documentMode" in document && 11 >= document.documentMode, Qe$1 = null, Re$1 = null, Se$1 = null, Te$1 = false;
  function Ue$1(a, b2, c2) {
    var d2 = c2.window === c2 ? c2.document : 9 === c2.nodeType ? c2 : c2.ownerDocument;
    Te$1 || null == Qe$1 || Qe$1 !== Xa(d2) || (d2 = Qe$1, "selectionStart" in d2 && Ne$1(d2) ? d2 = { start: d2.selectionStart, end: d2.selectionEnd } : (d2 = (d2.ownerDocument && d2.ownerDocument.defaultView || window).getSelection(), d2 = { anchorNode: d2.anchorNode, anchorOffset: d2.anchorOffset, focusNode: d2.focusNode, focusOffset: d2.focusOffset }), Se$1 && Ie$1(Se$1, d2) || (Se$1 = d2, d2 = oe$1(Re$1, "onSelect"), 0 < d2.length && (b2 = new td("onSelect", "select", null, b2, c2), a.push({ event: b2, listeners: d2 }), b2.target = Qe$1)));
  }
  function Ve$1(a, b2) {
    var c2 = {};
    c2[a.toLowerCase()] = b2.toLowerCase();
    c2["Webkit" + a] = "webkit" + b2;
    c2["Moz" + a] = "moz" + b2;
    return c2;
  }
  var We$1 = { animationend: Ve$1("Animation", "AnimationEnd"), animationiteration: Ve$1("Animation", "AnimationIteration"), animationstart: Ve$1("Animation", "AnimationStart"), transitionend: Ve$1("Transition", "TransitionEnd") }, Xe$1 = {}, Ye$1 = {};
  ia && (Ye$1 = document.createElement("div").style, "AnimationEvent" in window || (delete We$1.animationend.animation, delete We$1.animationiteration.animation, delete We$1.animationstart.animation), "TransitionEvent" in window || delete We$1.transitionend.transition);
  function Ze$1(a) {
    if (Xe$1[a])
      return Xe$1[a];
    if (!We$1[a])
      return a;
    var b2 = We$1[a], c2;
    for (c2 in b2)
      if (b2.hasOwnProperty(c2) && c2 in Ye$1)
        return Xe$1[a] = b2[c2];
    return a;
  }
  var $e$1 = Ze$1("animationend"), af = Ze$1("animationiteration"), bf = Ze$1("animationstart"), cf = Ze$1("transitionend"), df = /* @__PURE__ */ new Map(), ef = "abort auxClick cancel canPlay canPlayThrough click close contextMenu copy cut drag dragEnd dragEnter dragExit dragLeave dragOver dragStart drop durationChange emptied encrypted ended error gotPointerCapture input invalid keyDown keyPress keyUp load loadedData loadedMetadata loadStart lostPointerCapture mouseDown mouseMove mouseOut mouseOver mouseUp paste pause play playing pointerCancel pointerDown pointerMove pointerOut pointerOver pointerUp progress rateChange reset resize seeked seeking stalled submit suspend timeUpdate touchCancel touchEnd touchStart volumeChange scroll toggle touchMove waiting wheel".split(" ");
  function ff(a, b2) {
    df.set(a, b2);
    fa(b2, [a]);
  }
  for (var gf = 0; gf < ef.length; gf++) {
    var hf = ef[gf], jf = hf.toLowerCase(), kf = hf[0].toUpperCase() + hf.slice(1);
    ff(jf, "on" + kf);
  }
  ff($e$1, "onAnimationEnd");
  ff(af, "onAnimationIteration");
  ff(bf, "onAnimationStart");
  ff("dblclick", "onDoubleClick");
  ff("focusin", "onFocus");
  ff("focusout", "onBlur");
  ff(cf, "onTransitionEnd");
  ha("onMouseEnter", ["mouseout", "mouseover"]);
  ha("onMouseLeave", ["mouseout", "mouseover"]);
  ha("onPointerEnter", ["pointerout", "pointerover"]);
  ha("onPointerLeave", ["pointerout", "pointerover"]);
  fa("onChange", "change click focusin focusout input keydown keyup selectionchange".split(" "));
  fa("onSelect", "focusout contextmenu dragend focusin keydown keyup mousedown mouseup selectionchange".split(" "));
  fa("onBeforeInput", ["compositionend", "keypress", "textInput", "paste"]);
  fa("onCompositionEnd", "compositionend focusout keydown keypress keyup mousedown".split(" "));
  fa("onCompositionStart", "compositionstart focusout keydown keypress keyup mousedown".split(" "));
  fa("onCompositionUpdate", "compositionupdate focusout keydown keypress keyup mousedown".split(" "));
  var lf = "abort canplay canplaythrough durationchange emptied encrypted ended error loadeddata loadedmetadata loadstart pause play playing progress ratechange resize seeked seeking stalled suspend timeupdate volumechange waiting".split(" "), mf = new Set("cancel close invalid load scroll toggle".split(" ").concat(lf));
  function nf(a, b2, c2) {
    var d2 = a.type || "unknown-event";
    a.currentTarget = c2;
    Ub(d2, b2, void 0, a);
    a.currentTarget = null;
  }
  function se$1(a, b2) {
    b2 = 0 !== (b2 & 4);
    for (var c2 = 0; c2 < a.length; c2++) {
      var d2 = a[c2], e2 = d2.event;
      d2 = d2.listeners;
      a: {
        var f2 = void 0;
        if (b2)
          for (var g2 = d2.length - 1; 0 <= g2; g2--) {
            var h2 = d2[g2], k2 = h2.instance, l2 = h2.currentTarget;
            h2 = h2.listener;
            if (k2 !== f2 && e2.isPropagationStopped())
              break a;
            nf(e2, h2, l2);
            f2 = k2;
          }
        else
          for (g2 = 0; g2 < d2.length; g2++) {
            h2 = d2[g2];
            k2 = h2.instance;
            l2 = h2.currentTarget;
            h2 = h2.listener;
            if (k2 !== f2 && e2.isPropagationStopped())
              break a;
            nf(e2, h2, l2);
            f2 = k2;
          }
      }
    }
    if (Qb)
      throw a = Rb, Qb = false, Rb = null, a;
  }
  function D$1(a, b2) {
    var c2 = b2[of];
    void 0 === c2 && (c2 = b2[of] = /* @__PURE__ */ new Set());
    var d2 = a + "__bubble";
    c2.has(d2) || (pf(b2, a, 2, false), c2.add(d2));
  }
  function qf(a, b2, c2) {
    var d2 = 0;
    b2 && (d2 |= 4);
    pf(c2, a, d2, b2);
  }
  var rf = "_reactListening" + Math.random().toString(36).slice(2);
  function sf(a) {
    if (!a[rf]) {
      a[rf] = true;
      da.forEach(function(b3) {
        "selectionchange" !== b3 && (mf.has(b3) || qf(b3, false, a), qf(b3, true, a));
      });
      var b2 = 9 === a.nodeType ? a : a.ownerDocument;
      null === b2 || b2[rf] || (b2[rf] = true, qf("selectionchange", false, b2));
    }
  }
  function pf(a, b2, c2, d2) {
    switch (jd(b2)) {
      case 1:
        var e2 = ed;
        break;
      case 4:
        e2 = gd;
        break;
      default:
        e2 = fd;
    }
    c2 = e2.bind(null, b2, c2, a);
    e2 = void 0;
    !Lb || "touchstart" !== b2 && "touchmove" !== b2 && "wheel" !== b2 || (e2 = true);
    d2 ? void 0 !== e2 ? a.addEventListener(b2, c2, { capture: true, passive: e2 }) : a.addEventListener(b2, c2, true) : void 0 !== e2 ? a.addEventListener(b2, c2, { passive: e2 }) : a.addEventListener(b2, c2, false);
  }
  function hd(a, b2, c2, d2, e2) {
    var f2 = d2;
    if (0 === (b2 & 1) && 0 === (b2 & 2) && null !== d2)
      a:
        for (; ; ) {
          if (null === d2)
            return;
          var g2 = d2.tag;
          if (3 === g2 || 4 === g2) {
            var h2 = d2.stateNode.containerInfo;
            if (h2 === e2 || 8 === h2.nodeType && h2.parentNode === e2)
              break;
            if (4 === g2)
              for (g2 = d2.return; null !== g2; ) {
                var k2 = g2.tag;
                if (3 === k2 || 4 === k2) {
                  if (k2 = g2.stateNode.containerInfo, k2 === e2 || 8 === k2.nodeType && k2.parentNode === e2)
                    return;
                }
                g2 = g2.return;
              }
            for (; null !== h2; ) {
              g2 = Wc(h2);
              if (null === g2)
                return;
              k2 = g2.tag;
              if (5 === k2 || 6 === k2) {
                d2 = f2 = g2;
                continue a;
              }
              h2 = h2.parentNode;
            }
          }
          d2 = d2.return;
        }
    Jb(function() {
      var d3 = f2, e3 = xb(c2), g3 = [];
      a: {
        var h3 = df.get(a);
        if (void 0 !== h3) {
          var k3 = td, n2 = a;
          switch (a) {
            case "keypress":
              if (0 === od(c2))
                break a;
            case "keydown":
            case "keyup":
              k3 = Rd;
              break;
            case "focusin":
              n2 = "focus";
              k3 = Fd;
              break;
            case "focusout":
              n2 = "blur";
              k3 = Fd;
              break;
            case "beforeblur":
            case "afterblur":
              k3 = Fd;
              break;
            case "click":
              if (2 === c2.button)
                break a;
            case "auxclick":
            case "dblclick":
            case "mousedown":
            case "mousemove":
            case "mouseup":
            case "mouseout":
            case "mouseover":
            case "contextmenu":
              k3 = Bd;
              break;
            case "drag":
            case "dragend":
            case "dragenter":
            case "dragexit":
            case "dragleave":
            case "dragover":
            case "dragstart":
            case "drop":
              k3 = Dd;
              break;
            case "touchcancel":
            case "touchend":
            case "touchmove":
            case "touchstart":
              k3 = Vd;
              break;
            case $e$1:
            case af:
            case bf:
              k3 = Hd;
              break;
            case cf:
              k3 = Xd;
              break;
            case "scroll":
              k3 = vd;
              break;
            case "wheel":
              k3 = Zd;
              break;
            case "copy":
            case "cut":
            case "paste":
              k3 = Jd;
              break;
            case "gotpointercapture":
            case "lostpointercapture":
            case "pointercancel":
            case "pointerdown":
            case "pointermove":
            case "pointerout":
            case "pointerover":
            case "pointerup":
              k3 = Td$1;
          }
          var t2 = 0 !== (b2 & 4), J2 = !t2 && "scroll" === a, x2 = t2 ? null !== h3 ? h3 + "Capture" : null : h3;
          t2 = [];
          for (var w2 = d3, u2; null !== w2; ) {
            u2 = w2;
            var F2 = u2.stateNode;
            5 === u2.tag && null !== F2 && (u2 = F2, null !== x2 && (F2 = Kb(w2, x2), null != F2 && t2.push(tf(w2, F2, u2))));
            if (J2)
              break;
            w2 = w2.return;
          }
          0 < t2.length && (h3 = new k3(h3, n2, null, c2, e3), g3.push({ event: h3, listeners: t2 }));
        }
      }
      if (0 === (b2 & 7)) {
        a: {
          h3 = "mouseover" === a || "pointerover" === a;
          k3 = "mouseout" === a || "pointerout" === a;
          if (h3 && c2 !== wb && (n2 = c2.relatedTarget || c2.fromElement) && (Wc(n2) || n2[uf]))
            break a;
          if (k3 || h3) {
            h3 = e3.window === e3 ? e3 : (h3 = e3.ownerDocument) ? h3.defaultView || h3.parentWindow : window;
            if (k3) {
              if (n2 = c2.relatedTarget || c2.toElement, k3 = d3, n2 = n2 ? Wc(n2) : null, null !== n2 && (J2 = Vb(n2), n2 !== J2 || 5 !== n2.tag && 6 !== n2.tag))
                n2 = null;
            } else
              k3 = null, n2 = d3;
            if (k3 !== n2) {
              t2 = Bd;
              F2 = "onMouseLeave";
              x2 = "onMouseEnter";
              w2 = "mouse";
              if ("pointerout" === a || "pointerover" === a)
                t2 = Td$1, F2 = "onPointerLeave", x2 = "onPointerEnter", w2 = "pointer";
              J2 = null == k3 ? h3 : ue$1(k3);
              u2 = null == n2 ? h3 : ue$1(n2);
              h3 = new t2(F2, w2 + "leave", k3, c2, e3);
              h3.target = J2;
              h3.relatedTarget = u2;
              F2 = null;
              Wc(e3) === d3 && (t2 = new t2(x2, w2 + "enter", n2, c2, e3), t2.target = u2, t2.relatedTarget = J2, F2 = t2);
              J2 = F2;
              if (k3 && n2)
                b: {
                  t2 = k3;
                  x2 = n2;
                  w2 = 0;
                  for (u2 = t2; u2; u2 = vf(u2))
                    w2++;
                  u2 = 0;
                  for (F2 = x2; F2; F2 = vf(F2))
                    u2++;
                  for (; 0 < w2 - u2; )
                    t2 = vf(t2), w2--;
                  for (; 0 < u2 - w2; )
                    x2 = vf(x2), u2--;
                  for (; w2--; ) {
                    if (t2 === x2 || null !== x2 && t2 === x2.alternate)
                      break b;
                    t2 = vf(t2);
                    x2 = vf(x2);
                  }
                  t2 = null;
                }
              else
                t2 = null;
              null !== k3 && wf(g3, h3, k3, t2, false);
              null !== n2 && null !== J2 && wf(g3, J2, n2, t2, true);
            }
          }
        }
        a: {
          h3 = d3 ? ue$1(d3) : window;
          k3 = h3.nodeName && h3.nodeName.toLowerCase();
          if ("select" === k3 || "input" === k3 && "file" === h3.type)
            var na = ve$1;
          else if (me(h3))
            if (we$1)
              na = Fe$1;
            else {
              na = De$1;
              var xa = Ce$1;
            }
          else
            (k3 = h3.nodeName) && "input" === k3.toLowerCase() && ("checkbox" === h3.type || "radio" === h3.type) && (na = Ee$1);
          if (na && (na = na(a, d3))) {
            ne$1(g3, na, c2, e3);
            break a;
          }
          xa && xa(a, h3, d3);
          "focusout" === a && (xa = h3._wrapperState) && xa.controlled && "number" === h3.type && cb(h3, "number", h3.value);
        }
        xa = d3 ? ue$1(d3) : window;
        switch (a) {
          case "focusin":
            if (me(xa) || "true" === xa.contentEditable)
              Qe$1 = xa, Re$1 = d3, Se$1 = null;
            break;
          case "focusout":
            Se$1 = Re$1 = Qe$1 = null;
            break;
          case "mousedown":
            Te$1 = true;
            break;
          case "contextmenu":
          case "mouseup":
          case "dragend":
            Te$1 = false;
            Ue$1(g3, c2, e3);
            break;
          case "selectionchange":
            if (Pe$1)
              break;
          case "keydown":
          case "keyup":
            Ue$1(g3, c2, e3);
        }
        var $a;
        if (ae$1)
          b: {
            switch (a) {
              case "compositionstart":
                var ba = "onCompositionStart";
                break b;
              case "compositionend":
                ba = "onCompositionEnd";
                break b;
              case "compositionupdate":
                ba = "onCompositionUpdate";
                break b;
            }
            ba = void 0;
          }
        else
          ie$1 ? ge$1(a, c2) && (ba = "onCompositionEnd") : "keydown" === a && 229 === c2.keyCode && (ba = "onCompositionStart");
        ba && (de && "ko" !== c2.locale && (ie$1 || "onCompositionStart" !== ba ? "onCompositionEnd" === ba && ie$1 && ($a = nd()) : (kd = e3, ld = "value" in kd ? kd.value : kd.textContent, ie$1 = true)), xa = oe$1(d3, ba), 0 < xa.length && (ba = new Ld(ba, a, null, c2, e3), g3.push({ event: ba, listeners: xa }), $a ? ba.data = $a : ($a = he$1(c2), null !== $a && (ba.data = $a))));
        if ($a = ce$1 ? je$1(a, c2) : ke$1(a, c2))
          d3 = oe$1(d3, "onBeforeInput"), 0 < d3.length && (e3 = new Ld("onBeforeInput", "beforeinput", null, c2, e3), g3.push({ event: e3, listeners: d3 }), e3.data = $a);
      }
      se$1(g3, b2);
    });
  }
  function tf(a, b2, c2) {
    return { instance: a, listener: b2, currentTarget: c2 };
  }
  function oe$1(a, b2) {
    for (var c2 = b2 + "Capture", d2 = []; null !== a; ) {
      var e2 = a, f2 = e2.stateNode;
      5 === e2.tag && null !== f2 && (e2 = f2, f2 = Kb(a, c2), null != f2 && d2.unshift(tf(a, f2, e2)), f2 = Kb(a, b2), null != f2 && d2.push(tf(a, f2, e2)));
      a = a.return;
    }
    return d2;
  }
  function vf(a) {
    if (null === a)
      return null;
    do
      a = a.return;
    while (a && 5 !== a.tag);
    return a ? a : null;
  }
  function wf(a, b2, c2, d2, e2) {
    for (var f2 = b2._reactName, g2 = []; null !== c2 && c2 !== d2; ) {
      var h2 = c2, k2 = h2.alternate, l2 = h2.stateNode;
      if (null !== k2 && k2 === d2)
        break;
      5 === h2.tag && null !== l2 && (h2 = l2, e2 ? (k2 = Kb(c2, f2), null != k2 && g2.unshift(tf(c2, k2, h2))) : e2 || (k2 = Kb(c2, f2), null != k2 && g2.push(tf(c2, k2, h2))));
      c2 = c2.return;
    }
    0 !== g2.length && a.push({ event: b2, listeners: g2 });
  }
  var xf = /\r\n?/g, yf = /\u0000|\uFFFD/g;
  function zf(a) {
    return ("string" === typeof a ? a : "" + a).replace(xf, "\n").replace(yf, "");
  }
  function Af(a, b2, c2) {
    b2 = zf(b2);
    if (zf(a) !== b2 && c2)
      throw Error(p$2(425));
  }
  function Bf() {
  }
  var Cf = null, Df = null;
  function Ef(a, b2) {
    return "textarea" === a || "noscript" === a || "string" === typeof b2.children || "number" === typeof b2.children || "object" === typeof b2.dangerouslySetInnerHTML && null !== b2.dangerouslySetInnerHTML && null != b2.dangerouslySetInnerHTML.__html;
  }
  var Ff = "function" === typeof setTimeout ? setTimeout : void 0, Gf = "function" === typeof clearTimeout ? clearTimeout : void 0, Hf = "function" === typeof Promise ? Promise : void 0, Jf = "function" === typeof queueMicrotask ? queueMicrotask : "undefined" !== typeof Hf ? function(a) {
    return Hf.resolve(null).then(a).catch(If);
  } : Ff;
  function If(a) {
    setTimeout(function() {
      throw a;
    });
  }
  function Kf(a, b2) {
    var c2 = b2, d2 = 0;
    do {
      var e2 = c2.nextSibling;
      a.removeChild(c2);
      if (e2 && 8 === e2.nodeType)
        if (c2 = e2.data, "/$" === c2) {
          if (0 === d2) {
            a.removeChild(e2);
            bd(b2);
            return;
          }
          d2--;
        } else
          "$" !== c2 && "$?" !== c2 && "$!" !== c2 || d2++;
      c2 = e2;
    } while (c2);
    bd(b2);
  }
  function Lf(a) {
    for (; null != a; a = a.nextSibling) {
      var b2 = a.nodeType;
      if (1 === b2 || 3 === b2)
        break;
      if (8 === b2) {
        b2 = a.data;
        if ("$" === b2 || "$!" === b2 || "$?" === b2)
          break;
        if ("/$" === b2)
          return null;
      }
    }
    return a;
  }
  function Mf(a) {
    a = a.previousSibling;
    for (var b2 = 0; a; ) {
      if (8 === a.nodeType) {
        var c2 = a.data;
        if ("$" === c2 || "$!" === c2 || "$?" === c2) {
          if (0 === b2)
            return a;
          b2--;
        } else
          "/$" === c2 && b2++;
      }
      a = a.previousSibling;
    }
    return null;
  }
  var Nf = Math.random().toString(36).slice(2), Of = "__reactFiber$" + Nf, Pf = "__reactProps$" + Nf, uf = "__reactContainer$" + Nf, of = "__reactEvents$" + Nf, Qf = "__reactListeners$" + Nf, Rf = "__reactHandles$" + Nf;
  function Wc(a) {
    var b2 = a[Of];
    if (b2)
      return b2;
    for (var c2 = a.parentNode; c2; ) {
      if (b2 = c2[uf] || c2[Of]) {
        c2 = b2.alternate;
        if (null !== b2.child || null !== c2 && null !== c2.child)
          for (a = Mf(a); null !== a; ) {
            if (c2 = a[Of])
              return c2;
            a = Mf(a);
          }
        return b2;
      }
      a = c2;
      c2 = a.parentNode;
    }
    return null;
  }
  function Cb(a) {
    a = a[Of] || a[uf];
    return !a || 5 !== a.tag && 6 !== a.tag && 13 !== a.tag && 3 !== a.tag ? null : a;
  }
  function ue$1(a) {
    if (5 === a.tag || 6 === a.tag)
      return a.stateNode;
    throw Error(p$2(33));
  }
  function Db(a) {
    return a[Pf] || null;
  }
  var Sf = [], Tf = -1;
  function Uf(a) {
    return { current: a };
  }
  function E(a) {
    0 > Tf || (a.current = Sf[Tf], Sf[Tf] = null, Tf--);
  }
  function G$1(a, b2) {
    Tf++;
    Sf[Tf] = a.current;
    a.current = b2;
  }
  var Vf = {}, H$1 = Uf(Vf), Wf = Uf(false), Xf = Vf;
  function Yf(a, b2) {
    var c2 = a.type.contextTypes;
    if (!c2)
      return Vf;
    var d2 = a.stateNode;
    if (d2 && d2.__reactInternalMemoizedUnmaskedChildContext === b2)
      return d2.__reactInternalMemoizedMaskedChildContext;
    var e2 = {}, f2;
    for (f2 in c2)
      e2[f2] = b2[f2];
    d2 && (a = a.stateNode, a.__reactInternalMemoizedUnmaskedChildContext = b2, a.__reactInternalMemoizedMaskedChildContext = e2);
    return e2;
  }
  function Zf(a) {
    a = a.childContextTypes;
    return null !== a && void 0 !== a;
  }
  function $f() {
    E(Wf);
    E(H$1);
  }
  function ag(a, b2, c2) {
    if (H$1.current !== Vf)
      throw Error(p$2(168));
    G$1(H$1, b2);
    G$1(Wf, c2);
  }
  function bg(a, b2, c2) {
    var d2 = a.stateNode;
    b2 = b2.childContextTypes;
    if ("function" !== typeof d2.getChildContext)
      return c2;
    d2 = d2.getChildContext();
    for (var e2 in d2)
      if (!(e2 in b2))
        throw Error(p$2(108, Ra(a) || "Unknown", e2));
    return A$2({}, c2, d2);
  }
  function cg(a) {
    a = (a = a.stateNode) && a.__reactInternalMemoizedMergedChildContext || Vf;
    Xf = H$1.current;
    G$1(H$1, a);
    G$1(Wf, Wf.current);
    return true;
  }
  function dg(a, b2, c2) {
    var d2 = a.stateNode;
    if (!d2)
      throw Error(p$2(169));
    c2 ? (a = bg(a, b2, Xf), d2.__reactInternalMemoizedMergedChildContext = a, E(Wf), E(H$1), G$1(H$1, a)) : E(Wf);
    G$1(Wf, c2);
  }
  var eg = null, fg = false, gg = false;
  function hg(a) {
    null === eg ? eg = [a] : eg.push(a);
  }
  function ig(a) {
    fg = true;
    hg(a);
  }
  function jg() {
    if (!gg && null !== eg) {
      gg = true;
      var a = 0, b2 = C$1;
      try {
        var c2 = eg;
        for (C$1 = 1; a < c2.length; a++) {
          var d2 = c2[a];
          do
            d2 = d2(true);
          while (null !== d2);
        }
        eg = null;
        fg = false;
      } catch (e2) {
        throw null !== eg && (eg = eg.slice(a + 1)), ac(fc, jg), e2;
      } finally {
        C$1 = b2, gg = false;
      }
    }
    return null;
  }
  var kg = [], lg = 0, mg = null, ng = 0, og = [], pg = 0, qg = null, rg = 1, sg = "";
  function tg(a, b2) {
    kg[lg++] = ng;
    kg[lg++] = mg;
    mg = a;
    ng = b2;
  }
  function ug(a, b2, c2) {
    og[pg++] = rg;
    og[pg++] = sg;
    og[pg++] = qg;
    qg = a;
    var d2 = rg;
    a = sg;
    var e2 = 32 - oc(d2) - 1;
    d2 &= ~(1 << e2);
    c2 += 1;
    var f2 = 32 - oc(b2) + e2;
    if (30 < f2) {
      var g2 = e2 - e2 % 5;
      f2 = (d2 & (1 << g2) - 1).toString(32);
      d2 >>= g2;
      e2 -= g2;
      rg = 1 << 32 - oc(b2) + e2 | c2 << e2 | d2;
      sg = f2 + a;
    } else
      rg = 1 << f2 | c2 << e2 | d2, sg = a;
  }
  function vg(a) {
    null !== a.return && (tg(a, 1), ug(a, 1, 0));
  }
  function wg(a) {
    for (; a === mg; )
      mg = kg[--lg], kg[lg] = null, ng = kg[--lg], kg[lg] = null;
    for (; a === qg; )
      qg = og[--pg], og[pg] = null, sg = og[--pg], og[pg] = null, rg = og[--pg], og[pg] = null;
  }
  var xg = null, yg = null, I$1 = false, zg = null;
  function Ag(a, b2) {
    var c2 = Bg(5, null, null, 0);
    c2.elementType = "DELETED";
    c2.stateNode = b2;
    c2.return = a;
    b2 = a.deletions;
    null === b2 ? (a.deletions = [c2], a.flags |= 16) : b2.push(c2);
  }
  function Cg(a, b2) {
    switch (a.tag) {
      case 5:
        var c2 = a.type;
        b2 = 1 !== b2.nodeType || c2.toLowerCase() !== b2.nodeName.toLowerCase() ? null : b2;
        return null !== b2 ? (a.stateNode = b2, xg = a, yg = Lf(b2.firstChild), true) : false;
      case 6:
        return b2 = "" === a.pendingProps || 3 !== b2.nodeType ? null : b2, null !== b2 ? (a.stateNode = b2, xg = a, yg = null, true) : false;
      case 13:
        return b2 = 8 !== b2.nodeType ? null : b2, null !== b2 ? (c2 = null !== qg ? { id: rg, overflow: sg } : null, a.memoizedState = { dehydrated: b2, treeContext: c2, retryLane: 1073741824 }, c2 = Bg(18, null, null, 0), c2.stateNode = b2, c2.return = a, a.child = c2, xg = a, yg = null, true) : false;
      default:
        return false;
    }
  }
  function Dg(a) {
    return 0 !== (a.mode & 1) && 0 === (a.flags & 128);
  }
  function Eg(a) {
    if (I$1) {
      var b2 = yg;
      if (b2) {
        var c2 = b2;
        if (!Cg(a, b2)) {
          if (Dg(a))
            throw Error(p$2(418));
          b2 = Lf(c2.nextSibling);
          var d2 = xg;
          b2 && Cg(a, b2) ? Ag(d2, c2) : (a.flags = a.flags & -4097 | 2, I$1 = false, xg = a);
        }
      } else {
        if (Dg(a))
          throw Error(p$2(418));
        a.flags = a.flags & -4097 | 2;
        I$1 = false;
        xg = a;
      }
    }
  }
  function Fg(a) {
    for (a = a.return; null !== a && 5 !== a.tag && 3 !== a.tag && 13 !== a.tag; )
      a = a.return;
    xg = a;
  }
  function Gg(a) {
    if (a !== xg)
      return false;
    if (!I$1)
      return Fg(a), I$1 = true, false;
    var b2;
    (b2 = 3 !== a.tag) && !(b2 = 5 !== a.tag) && (b2 = a.type, b2 = "head" !== b2 && "body" !== b2 && !Ef(a.type, a.memoizedProps));
    if (b2 && (b2 = yg)) {
      if (Dg(a))
        throw Hg(), Error(p$2(418));
      for (; b2; )
        Ag(a, b2), b2 = Lf(b2.nextSibling);
    }
    Fg(a);
    if (13 === a.tag) {
      a = a.memoizedState;
      a = null !== a ? a.dehydrated : null;
      if (!a)
        throw Error(p$2(317));
      a: {
        a = a.nextSibling;
        for (b2 = 0; a; ) {
          if (8 === a.nodeType) {
            var c2 = a.data;
            if ("/$" === c2) {
              if (0 === b2) {
                yg = Lf(a.nextSibling);
                break a;
              }
              b2--;
            } else
              "$" !== c2 && "$!" !== c2 && "$?" !== c2 || b2++;
          }
          a = a.nextSibling;
        }
        yg = null;
      }
    } else
      yg = xg ? Lf(a.stateNode.nextSibling) : null;
    return true;
  }
  function Hg() {
    for (var a = yg; a; )
      a = Lf(a.nextSibling);
  }
  function Ig() {
    yg = xg = null;
    I$1 = false;
  }
  function Jg(a) {
    null === zg ? zg = [a] : zg.push(a);
  }
  var Kg = ua.ReactCurrentBatchConfig;
  function Lg(a, b2, c2) {
    a = c2.ref;
    if (null !== a && "function" !== typeof a && "object" !== typeof a) {
      if (c2._owner) {
        c2 = c2._owner;
        if (c2) {
          if (1 !== c2.tag)
            throw Error(p$2(309));
          var d2 = c2.stateNode;
        }
        if (!d2)
          throw Error(p$2(147, a));
        var e2 = d2, f2 = "" + a;
        if (null !== b2 && null !== b2.ref && "function" === typeof b2.ref && b2.ref._stringRef === f2)
          return b2.ref;
        b2 = function(a2) {
          var b3 = e2.refs;
          null === a2 ? delete b3[f2] : b3[f2] = a2;
        };
        b2._stringRef = f2;
        return b2;
      }
      if ("string" !== typeof a)
        throw Error(p$2(284));
      if (!c2._owner)
        throw Error(p$2(290, a));
    }
    return a;
  }
  function Mg(a, b2) {
    a = Object.prototype.toString.call(b2);
    throw Error(p$2(31, "[object Object]" === a ? "object with keys {" + Object.keys(b2).join(", ") + "}" : a));
  }
  function Ng(a) {
    var b2 = a._init;
    return b2(a._payload);
  }
  function Og(a) {
    function b2(b3, c3) {
      if (a) {
        var d3 = b3.deletions;
        null === d3 ? (b3.deletions = [c3], b3.flags |= 16) : d3.push(c3);
      }
    }
    function c2(c3, d3) {
      if (!a)
        return null;
      for (; null !== d3; )
        b2(c3, d3), d3 = d3.sibling;
      return null;
    }
    function d2(a2, b3) {
      for (a2 = /* @__PURE__ */ new Map(); null !== b3; )
        null !== b3.key ? a2.set(b3.key, b3) : a2.set(b3.index, b3), b3 = b3.sibling;
      return a2;
    }
    function e2(a2, b3) {
      a2 = Pg(a2, b3);
      a2.index = 0;
      a2.sibling = null;
      return a2;
    }
    function f2(b3, c3, d3) {
      b3.index = d3;
      if (!a)
        return b3.flags |= 1048576, c3;
      d3 = b3.alternate;
      if (null !== d3)
        return d3 = d3.index, d3 < c3 ? (b3.flags |= 2, c3) : d3;
      b3.flags |= 2;
      return c3;
    }
    function g2(b3) {
      a && null === b3.alternate && (b3.flags |= 2);
      return b3;
    }
    function h2(a2, b3, c3, d3) {
      if (null === b3 || 6 !== b3.tag)
        return b3 = Qg(c3, a2.mode, d3), b3.return = a2, b3;
      b3 = e2(b3, c3);
      b3.return = a2;
      return b3;
    }
    function k2(a2, b3, c3, d3) {
      var f3 = c3.type;
      if (f3 === ya)
        return m2(a2, b3, c3.props.children, d3, c3.key);
      if (null !== b3 && (b3.elementType === f3 || "object" === typeof f3 && null !== f3 && f3.$$typeof === Ha && Ng(f3) === b3.type))
        return d3 = e2(b3, c3.props), d3.ref = Lg(a2, b3, c3), d3.return = a2, d3;
      d3 = Rg(c3.type, c3.key, c3.props, null, a2.mode, d3);
      d3.ref = Lg(a2, b3, c3);
      d3.return = a2;
      return d3;
    }
    function l2(a2, b3, c3, d3) {
      if (null === b3 || 4 !== b3.tag || b3.stateNode.containerInfo !== c3.containerInfo || b3.stateNode.implementation !== c3.implementation)
        return b3 = Sg(c3, a2.mode, d3), b3.return = a2, b3;
      b3 = e2(b3, c3.children || []);
      b3.return = a2;
      return b3;
    }
    function m2(a2, b3, c3, d3, f3) {
      if (null === b3 || 7 !== b3.tag)
        return b3 = Tg(c3, a2.mode, d3, f3), b3.return = a2, b3;
      b3 = e2(b3, c3);
      b3.return = a2;
      return b3;
    }
    function q2(a2, b3, c3) {
      if ("string" === typeof b3 && "" !== b3 || "number" === typeof b3)
        return b3 = Qg("" + b3, a2.mode, c3), b3.return = a2, b3;
      if ("object" === typeof b3 && null !== b3) {
        switch (b3.$$typeof) {
          case va:
            return c3 = Rg(b3.type, b3.key, b3.props, null, a2.mode, c3), c3.ref = Lg(a2, null, b3), c3.return = a2, c3;
          case wa:
            return b3 = Sg(b3, a2.mode, c3), b3.return = a2, b3;
          case Ha:
            var d3 = b3._init;
            return q2(a2, d3(b3._payload), c3);
        }
        if (eb(b3) || Ka(b3))
          return b3 = Tg(b3, a2.mode, c3, null), b3.return = a2, b3;
        Mg(a2, b3);
      }
      return null;
    }
    function r2(a2, b3, c3, d3) {
      var e3 = null !== b3 ? b3.key : null;
      if ("string" === typeof c3 && "" !== c3 || "number" === typeof c3)
        return null !== e3 ? null : h2(a2, b3, "" + c3, d3);
      if ("object" === typeof c3 && null !== c3) {
        switch (c3.$$typeof) {
          case va:
            return c3.key === e3 ? k2(a2, b3, c3, d3) : null;
          case wa:
            return c3.key === e3 ? l2(a2, b3, c3, d3) : null;
          case Ha:
            return e3 = c3._init, r2(
              a2,
              b3,
              e3(c3._payload),
              d3
            );
        }
        if (eb(c3) || Ka(c3))
          return null !== e3 ? null : m2(a2, b3, c3, d3, null);
        Mg(a2, c3);
      }
      return null;
    }
    function y2(a2, b3, c3, d3, e3) {
      if ("string" === typeof d3 && "" !== d3 || "number" === typeof d3)
        return a2 = a2.get(c3) || null, h2(b3, a2, "" + d3, e3);
      if ("object" === typeof d3 && null !== d3) {
        switch (d3.$$typeof) {
          case va:
            return a2 = a2.get(null === d3.key ? c3 : d3.key) || null, k2(b3, a2, d3, e3);
          case wa:
            return a2 = a2.get(null === d3.key ? c3 : d3.key) || null, l2(b3, a2, d3, e3);
          case Ha:
            var f3 = d3._init;
            return y2(a2, b3, c3, f3(d3._payload), e3);
        }
        if (eb(d3) || Ka(d3))
          return a2 = a2.get(c3) || null, m2(b3, a2, d3, e3, null);
        Mg(b3, d3);
      }
      return null;
    }
    function n2(e3, g3, h3, k3) {
      for (var l3 = null, m3 = null, u2 = g3, w2 = g3 = 0, x2 = null; null !== u2 && w2 < h3.length; w2++) {
        u2.index > w2 ? (x2 = u2, u2 = null) : x2 = u2.sibling;
        var n3 = r2(e3, u2, h3[w2], k3);
        if (null === n3) {
          null === u2 && (u2 = x2);
          break;
        }
        a && u2 && null === n3.alternate && b2(e3, u2);
        g3 = f2(n3, g3, w2);
        null === m3 ? l3 = n3 : m3.sibling = n3;
        m3 = n3;
        u2 = x2;
      }
      if (w2 === h3.length)
        return c2(e3, u2), I$1 && tg(e3, w2), l3;
      if (null === u2) {
        for (; w2 < h3.length; w2++)
          u2 = q2(e3, h3[w2], k3), null !== u2 && (g3 = f2(u2, g3, w2), null === m3 ? l3 = u2 : m3.sibling = u2, m3 = u2);
        I$1 && tg(e3, w2);
        return l3;
      }
      for (u2 = d2(e3, u2); w2 < h3.length; w2++)
        x2 = y2(u2, e3, w2, h3[w2], k3), null !== x2 && (a && null !== x2.alternate && u2.delete(null === x2.key ? w2 : x2.key), g3 = f2(x2, g3, w2), null === m3 ? l3 = x2 : m3.sibling = x2, m3 = x2);
      a && u2.forEach(function(a2) {
        return b2(e3, a2);
      });
      I$1 && tg(e3, w2);
      return l3;
    }
    function t2(e3, g3, h3, k3) {
      var l3 = Ka(h3);
      if ("function" !== typeof l3)
        throw Error(p$2(150));
      h3 = l3.call(h3);
      if (null == h3)
        throw Error(p$2(151));
      for (var u2 = l3 = null, m3 = g3, w2 = g3 = 0, x2 = null, n3 = h3.next(); null !== m3 && !n3.done; w2++, n3 = h3.next()) {
        m3.index > w2 ? (x2 = m3, m3 = null) : x2 = m3.sibling;
        var t3 = r2(e3, m3, n3.value, k3);
        if (null === t3) {
          null === m3 && (m3 = x2);
          break;
        }
        a && m3 && null === t3.alternate && b2(e3, m3);
        g3 = f2(t3, g3, w2);
        null === u2 ? l3 = t3 : u2.sibling = t3;
        u2 = t3;
        m3 = x2;
      }
      if (n3.done)
        return c2(
          e3,
          m3
        ), I$1 && tg(e3, w2), l3;
      if (null === m3) {
        for (; !n3.done; w2++, n3 = h3.next())
          n3 = q2(e3, n3.value, k3), null !== n3 && (g3 = f2(n3, g3, w2), null === u2 ? l3 = n3 : u2.sibling = n3, u2 = n3);
        I$1 && tg(e3, w2);
        return l3;
      }
      for (m3 = d2(e3, m3); !n3.done; w2++, n3 = h3.next())
        n3 = y2(m3, e3, w2, n3.value, k3), null !== n3 && (a && null !== n3.alternate && m3.delete(null === n3.key ? w2 : n3.key), g3 = f2(n3, g3, w2), null === u2 ? l3 = n3 : u2.sibling = n3, u2 = n3);
      a && m3.forEach(function(a2) {
        return b2(e3, a2);
      });
      I$1 && tg(e3, w2);
      return l3;
    }
    function J2(a2, d3, f3, h3) {
      "object" === typeof f3 && null !== f3 && f3.type === ya && null === f3.key && (f3 = f3.props.children);
      if ("object" === typeof f3 && null !== f3) {
        switch (f3.$$typeof) {
          case va:
            a: {
              for (var k3 = f3.key, l3 = d3; null !== l3; ) {
                if (l3.key === k3) {
                  k3 = f3.type;
                  if (k3 === ya) {
                    if (7 === l3.tag) {
                      c2(a2, l3.sibling);
                      d3 = e2(l3, f3.props.children);
                      d3.return = a2;
                      a2 = d3;
                      break a;
                    }
                  } else if (l3.elementType === k3 || "object" === typeof k3 && null !== k3 && k3.$$typeof === Ha && Ng(k3) === l3.type) {
                    c2(a2, l3.sibling);
                    d3 = e2(l3, f3.props);
                    d3.ref = Lg(a2, l3, f3);
                    d3.return = a2;
                    a2 = d3;
                    break a;
                  }
                  c2(a2, l3);
                  break;
                } else
                  b2(a2, l3);
                l3 = l3.sibling;
              }
              f3.type === ya ? (d3 = Tg(f3.props.children, a2.mode, h3, f3.key), d3.return = a2, a2 = d3) : (h3 = Rg(f3.type, f3.key, f3.props, null, a2.mode, h3), h3.ref = Lg(a2, d3, f3), h3.return = a2, a2 = h3);
            }
            return g2(a2);
          case wa:
            a: {
              for (l3 = f3.key; null !== d3; ) {
                if (d3.key === l3)
                  if (4 === d3.tag && d3.stateNode.containerInfo === f3.containerInfo && d3.stateNode.implementation === f3.implementation) {
                    c2(a2, d3.sibling);
                    d3 = e2(d3, f3.children || []);
                    d3.return = a2;
                    a2 = d3;
                    break a;
                  } else {
                    c2(a2, d3);
                    break;
                  }
                else
                  b2(a2, d3);
                d3 = d3.sibling;
              }
              d3 = Sg(f3, a2.mode, h3);
              d3.return = a2;
              a2 = d3;
            }
            return g2(a2);
          case Ha:
            return l3 = f3._init, J2(a2, d3, l3(f3._payload), h3);
        }
        if (eb(f3))
          return n2(a2, d3, f3, h3);
        if (Ka(f3))
          return t2(a2, d3, f3, h3);
        Mg(a2, f3);
      }
      return "string" === typeof f3 && "" !== f3 || "number" === typeof f3 ? (f3 = "" + f3, null !== d3 && 6 === d3.tag ? (c2(a2, d3.sibling), d3 = e2(d3, f3), d3.return = a2, a2 = d3) : (c2(a2, d3), d3 = Qg(f3, a2.mode, h3), d3.return = a2, a2 = d3), g2(a2)) : c2(a2, d3);
    }
    return J2;
  }
  var Ug = Og(true), Vg = Og(false), Wg = Uf(null), Xg = null, Yg = null, Zg = null;
  function $g() {
    Zg = Yg = Xg = null;
  }
  function ah(a) {
    var b2 = Wg.current;
    E(Wg);
    a._currentValue = b2;
  }
  function bh(a, b2, c2) {
    for (; null !== a; ) {
      var d2 = a.alternate;
      (a.childLanes & b2) !== b2 ? (a.childLanes |= b2, null !== d2 && (d2.childLanes |= b2)) : null !== d2 && (d2.childLanes & b2) !== b2 && (d2.childLanes |= b2);
      if (a === c2)
        break;
      a = a.return;
    }
  }
  function ch(a, b2) {
    Xg = a;
    Zg = Yg = null;
    a = a.dependencies;
    null !== a && null !== a.firstContext && (0 !== (a.lanes & b2) && (dh = true), a.firstContext = null);
  }
  function eh(a) {
    var b2 = a._currentValue;
    if (Zg !== a)
      if (a = { context: a, memoizedValue: b2, next: null }, null === Yg) {
        if (null === Xg)
          throw Error(p$2(308));
        Yg = a;
        Xg.dependencies = { lanes: 0, firstContext: a };
      } else
        Yg = Yg.next = a;
    return b2;
  }
  var fh = null;
  function gh(a) {
    null === fh ? fh = [a] : fh.push(a);
  }
  function hh(a, b2, c2, d2) {
    var e2 = b2.interleaved;
    null === e2 ? (c2.next = c2, gh(b2)) : (c2.next = e2.next, e2.next = c2);
    b2.interleaved = c2;
    return ih(a, d2);
  }
  function ih(a, b2) {
    a.lanes |= b2;
    var c2 = a.alternate;
    null !== c2 && (c2.lanes |= b2);
    c2 = a;
    for (a = a.return; null !== a; )
      a.childLanes |= b2, c2 = a.alternate, null !== c2 && (c2.childLanes |= b2), c2 = a, a = a.return;
    return 3 === c2.tag ? c2.stateNode : null;
  }
  var jh = false;
  function kh(a) {
    a.updateQueue = { baseState: a.memoizedState, firstBaseUpdate: null, lastBaseUpdate: null, shared: { pending: null, interleaved: null, lanes: 0 }, effects: null };
  }
  function lh(a, b2) {
    a = a.updateQueue;
    b2.updateQueue === a && (b2.updateQueue = { baseState: a.baseState, firstBaseUpdate: a.firstBaseUpdate, lastBaseUpdate: a.lastBaseUpdate, shared: a.shared, effects: a.effects });
  }
  function mh(a, b2) {
    return { eventTime: a, lane: b2, tag: 0, payload: null, callback: null, next: null };
  }
  function nh(a, b2, c2) {
    var d2 = a.updateQueue;
    if (null === d2)
      return null;
    d2 = d2.shared;
    if (0 !== (K$1 & 2)) {
      var e2 = d2.pending;
      null === e2 ? b2.next = b2 : (b2.next = e2.next, e2.next = b2);
      d2.pending = b2;
      return ih(a, c2);
    }
    e2 = d2.interleaved;
    null === e2 ? (b2.next = b2, gh(d2)) : (b2.next = e2.next, e2.next = b2);
    d2.interleaved = b2;
    return ih(a, c2);
  }
  function oh(a, b2, c2) {
    b2 = b2.updateQueue;
    if (null !== b2 && (b2 = b2.shared, 0 !== (c2 & 4194240))) {
      var d2 = b2.lanes;
      d2 &= a.pendingLanes;
      c2 |= d2;
      b2.lanes = c2;
      Cc(a, c2);
    }
  }
  function ph(a, b2) {
    var c2 = a.updateQueue, d2 = a.alternate;
    if (null !== d2 && (d2 = d2.updateQueue, c2 === d2)) {
      var e2 = null, f2 = null;
      c2 = c2.firstBaseUpdate;
      if (null !== c2) {
        do {
          var g2 = { eventTime: c2.eventTime, lane: c2.lane, tag: c2.tag, payload: c2.payload, callback: c2.callback, next: null };
          null === f2 ? e2 = f2 = g2 : f2 = f2.next = g2;
          c2 = c2.next;
        } while (null !== c2);
        null === f2 ? e2 = f2 = b2 : f2 = f2.next = b2;
      } else
        e2 = f2 = b2;
      c2 = { baseState: d2.baseState, firstBaseUpdate: e2, lastBaseUpdate: f2, shared: d2.shared, effects: d2.effects };
      a.updateQueue = c2;
      return;
    }
    a = c2.lastBaseUpdate;
    null === a ? c2.firstBaseUpdate = b2 : a.next = b2;
    c2.lastBaseUpdate = b2;
  }
  function qh(a, b2, c2, d2) {
    var e2 = a.updateQueue;
    jh = false;
    var f2 = e2.firstBaseUpdate, g2 = e2.lastBaseUpdate, h2 = e2.shared.pending;
    if (null !== h2) {
      e2.shared.pending = null;
      var k2 = h2, l2 = k2.next;
      k2.next = null;
      null === g2 ? f2 = l2 : g2.next = l2;
      g2 = k2;
      var m2 = a.alternate;
      null !== m2 && (m2 = m2.updateQueue, h2 = m2.lastBaseUpdate, h2 !== g2 && (null === h2 ? m2.firstBaseUpdate = l2 : h2.next = l2, m2.lastBaseUpdate = k2));
    }
    if (null !== f2) {
      var q2 = e2.baseState;
      g2 = 0;
      m2 = l2 = k2 = null;
      h2 = f2;
      do {
        var r2 = h2.lane, y2 = h2.eventTime;
        if ((d2 & r2) === r2) {
          null !== m2 && (m2 = m2.next = {
            eventTime: y2,
            lane: 0,
            tag: h2.tag,
            payload: h2.payload,
            callback: h2.callback,
            next: null
          });
          a: {
            var n2 = a, t2 = h2;
            r2 = b2;
            y2 = c2;
            switch (t2.tag) {
              case 1:
                n2 = t2.payload;
                if ("function" === typeof n2) {
                  q2 = n2.call(y2, q2, r2);
                  break a;
                }
                q2 = n2;
                break a;
              case 3:
                n2.flags = n2.flags & -65537 | 128;
              case 0:
                n2 = t2.payload;
                r2 = "function" === typeof n2 ? n2.call(y2, q2, r2) : n2;
                if (null === r2 || void 0 === r2)
                  break a;
                q2 = A$2({}, q2, r2);
                break a;
              case 2:
                jh = true;
            }
          }
          null !== h2.callback && 0 !== h2.lane && (a.flags |= 64, r2 = e2.effects, null === r2 ? e2.effects = [h2] : r2.push(h2));
        } else
          y2 = { eventTime: y2, lane: r2, tag: h2.tag, payload: h2.payload, callback: h2.callback, next: null }, null === m2 ? (l2 = m2 = y2, k2 = q2) : m2 = m2.next = y2, g2 |= r2;
        h2 = h2.next;
        if (null === h2)
          if (h2 = e2.shared.pending, null === h2)
            break;
          else
            r2 = h2, h2 = r2.next, r2.next = null, e2.lastBaseUpdate = r2, e2.shared.pending = null;
      } while (1);
      null === m2 && (k2 = q2);
      e2.baseState = k2;
      e2.firstBaseUpdate = l2;
      e2.lastBaseUpdate = m2;
      b2 = e2.shared.interleaved;
      if (null !== b2) {
        e2 = b2;
        do
          g2 |= e2.lane, e2 = e2.next;
        while (e2 !== b2);
      } else
        null === f2 && (e2.shared.lanes = 0);
      rh |= g2;
      a.lanes = g2;
      a.memoizedState = q2;
    }
  }
  function sh(a, b2, c2) {
    a = b2.effects;
    b2.effects = null;
    if (null !== a)
      for (b2 = 0; b2 < a.length; b2++) {
        var d2 = a[b2], e2 = d2.callback;
        if (null !== e2) {
          d2.callback = null;
          d2 = c2;
          if ("function" !== typeof e2)
            throw Error(p$2(191, e2));
          e2.call(d2);
        }
      }
  }
  var th = {}, uh = Uf(th), vh$1 = Uf(th), wh = Uf(th);
  function xh(a) {
    if (a === th)
      throw Error(p$2(174));
    return a;
  }
  function yh(a, b2) {
    G$1(wh, b2);
    G$1(vh$1, a);
    G$1(uh, th);
    a = b2.nodeType;
    switch (a) {
      case 9:
      case 11:
        b2 = (b2 = b2.documentElement) ? b2.namespaceURI : lb(null, "");
        break;
      default:
        a = 8 === a ? b2.parentNode : b2, b2 = a.namespaceURI || null, a = a.tagName, b2 = lb(b2, a);
    }
    E(uh);
    G$1(uh, b2);
  }
  function zh() {
    E(uh);
    E(vh$1);
    E(wh);
  }
  function Ah(a) {
    xh(wh.current);
    var b2 = xh(uh.current);
    var c2 = lb(b2, a.type);
    b2 !== c2 && (G$1(vh$1, a), G$1(uh, c2));
  }
  function Bh(a) {
    vh$1.current === a && (E(uh), E(vh$1));
  }
  var L$1 = Uf(0);
  function Ch(a) {
    for (var b2 = a; null !== b2; ) {
      if (13 === b2.tag) {
        var c2 = b2.memoizedState;
        if (null !== c2 && (c2 = c2.dehydrated, null === c2 || "$?" === c2.data || "$!" === c2.data))
          return b2;
      } else if (19 === b2.tag && void 0 !== b2.memoizedProps.revealOrder) {
        if (0 !== (b2.flags & 128))
          return b2;
      } else if (null !== b2.child) {
        b2.child.return = b2;
        b2 = b2.child;
        continue;
      }
      if (b2 === a)
        break;
      for (; null === b2.sibling; ) {
        if (null === b2.return || b2.return === a)
          return null;
        b2 = b2.return;
      }
      b2.sibling.return = b2.return;
      b2 = b2.sibling;
    }
    return null;
  }
  var Dh = [];
  function Eh() {
    for (var a = 0; a < Dh.length; a++)
      Dh[a]._workInProgressVersionPrimary = null;
    Dh.length = 0;
  }
  var Fh = ua.ReactCurrentDispatcher, Gh = ua.ReactCurrentBatchConfig, Hh = 0, M$1 = null, N = null, O$1 = null, Ih = false, Jh = false, Kh = 0, Lh = 0;
  function P() {
    throw Error(p$2(321));
  }
  function Mh(a, b2) {
    if (null === b2)
      return false;
    for (var c2 = 0; c2 < b2.length && c2 < a.length; c2++)
      if (!He$1(a[c2], b2[c2]))
        return false;
    return true;
  }
  function Nh(a, b2, c2, d2, e2, f2) {
    Hh = f2;
    M$1 = b2;
    b2.memoizedState = null;
    b2.updateQueue = null;
    b2.lanes = 0;
    Fh.current = null === a || null === a.memoizedState ? Oh : Ph;
    a = c2(d2, e2);
    if (Jh) {
      f2 = 0;
      do {
        Jh = false;
        Kh = 0;
        if (25 <= f2)
          throw Error(p$2(301));
        f2 += 1;
        O$1 = N = null;
        b2.updateQueue = null;
        Fh.current = Qh;
        a = c2(d2, e2);
      } while (Jh);
    }
    Fh.current = Rh;
    b2 = null !== N && null !== N.next;
    Hh = 0;
    O$1 = N = M$1 = null;
    Ih = false;
    if (b2)
      throw Error(p$2(300));
    return a;
  }
  function Sh() {
    var a = 0 !== Kh;
    Kh = 0;
    return a;
  }
  function Th$1() {
    var a = { memoizedState: null, baseState: null, baseQueue: null, queue: null, next: null };
    null === O$1 ? M$1.memoizedState = O$1 = a : O$1 = O$1.next = a;
    return O$1;
  }
  function Uh() {
    if (null === N) {
      var a = M$1.alternate;
      a = null !== a ? a.memoizedState : null;
    } else
      a = N.next;
    var b2 = null === O$1 ? M$1.memoizedState : O$1.next;
    if (null !== b2)
      O$1 = b2, N = a;
    else {
      if (null === a)
        throw Error(p$2(310));
      N = a;
      a = { memoizedState: N.memoizedState, baseState: N.baseState, baseQueue: N.baseQueue, queue: N.queue, next: null };
      null === O$1 ? M$1.memoizedState = O$1 = a : O$1 = O$1.next = a;
    }
    return O$1;
  }
  function Vh(a, b2) {
    return "function" === typeof b2 ? b2(a) : b2;
  }
  function Wh(a) {
    var b2 = Uh(), c2 = b2.queue;
    if (null === c2)
      throw Error(p$2(311));
    c2.lastRenderedReducer = a;
    var d2 = N, e2 = d2.baseQueue, f2 = c2.pending;
    if (null !== f2) {
      if (null !== e2) {
        var g2 = e2.next;
        e2.next = f2.next;
        f2.next = g2;
      }
      d2.baseQueue = e2 = f2;
      c2.pending = null;
    }
    if (null !== e2) {
      f2 = e2.next;
      d2 = d2.baseState;
      var h2 = g2 = null, k2 = null, l2 = f2;
      do {
        var m2 = l2.lane;
        if ((Hh & m2) === m2)
          null !== k2 && (k2 = k2.next = { lane: 0, action: l2.action, hasEagerState: l2.hasEagerState, eagerState: l2.eagerState, next: null }), d2 = l2.hasEagerState ? l2.eagerState : a(d2, l2.action);
        else {
          var q2 = {
            lane: m2,
            action: l2.action,
            hasEagerState: l2.hasEagerState,
            eagerState: l2.eagerState,
            next: null
          };
          null === k2 ? (h2 = k2 = q2, g2 = d2) : k2 = k2.next = q2;
          M$1.lanes |= m2;
          rh |= m2;
        }
        l2 = l2.next;
      } while (null !== l2 && l2 !== f2);
      null === k2 ? g2 = d2 : k2.next = h2;
      He$1(d2, b2.memoizedState) || (dh = true);
      b2.memoizedState = d2;
      b2.baseState = g2;
      b2.baseQueue = k2;
      c2.lastRenderedState = d2;
    }
    a = c2.interleaved;
    if (null !== a) {
      e2 = a;
      do
        f2 = e2.lane, M$1.lanes |= f2, rh |= f2, e2 = e2.next;
      while (e2 !== a);
    } else
      null === e2 && (c2.lanes = 0);
    return [b2.memoizedState, c2.dispatch];
  }
  function Xh(a) {
    var b2 = Uh(), c2 = b2.queue;
    if (null === c2)
      throw Error(p$2(311));
    c2.lastRenderedReducer = a;
    var d2 = c2.dispatch, e2 = c2.pending, f2 = b2.memoizedState;
    if (null !== e2) {
      c2.pending = null;
      var g2 = e2 = e2.next;
      do
        f2 = a(f2, g2.action), g2 = g2.next;
      while (g2 !== e2);
      He$1(f2, b2.memoizedState) || (dh = true);
      b2.memoizedState = f2;
      null === b2.baseQueue && (b2.baseState = f2);
      c2.lastRenderedState = f2;
    }
    return [f2, d2];
  }
  function Yh() {
  }
  function Zh(a, b2) {
    var c2 = M$1, d2 = Uh(), e2 = b2(), f2 = !He$1(d2.memoizedState, e2);
    f2 && (d2.memoizedState = e2, dh = true);
    d2 = d2.queue;
    $h(ai.bind(null, c2, d2, a), [a]);
    if (d2.getSnapshot !== b2 || f2 || null !== O$1 && O$1.memoizedState.tag & 1) {
      c2.flags |= 2048;
      bi(9, ci.bind(null, c2, d2, e2, b2), void 0, null);
      if (null === Q$1)
        throw Error(p$2(349));
      0 !== (Hh & 30) || di(c2, b2, e2);
    }
    return e2;
  }
  function di(a, b2, c2) {
    a.flags |= 16384;
    a = { getSnapshot: b2, value: c2 };
    b2 = M$1.updateQueue;
    null === b2 ? (b2 = { lastEffect: null, stores: null }, M$1.updateQueue = b2, b2.stores = [a]) : (c2 = b2.stores, null === c2 ? b2.stores = [a] : c2.push(a));
  }
  function ci(a, b2, c2, d2) {
    b2.value = c2;
    b2.getSnapshot = d2;
    ei(b2) && fi(a);
  }
  function ai(a, b2, c2) {
    return c2(function() {
      ei(b2) && fi(a);
    });
  }
  function ei(a) {
    var b2 = a.getSnapshot;
    a = a.value;
    try {
      var c2 = b2();
      return !He$1(a, c2);
    } catch (d2) {
      return true;
    }
  }
  function fi(a) {
    var b2 = ih(a, 1);
    null !== b2 && gi(b2, a, 1, -1);
  }
  function hi(a) {
    var b2 = Th$1();
    "function" === typeof a && (a = a());
    b2.memoizedState = b2.baseState = a;
    a = { pending: null, interleaved: null, lanes: 0, dispatch: null, lastRenderedReducer: Vh, lastRenderedState: a };
    b2.queue = a;
    a = a.dispatch = ii.bind(null, M$1, a);
    return [b2.memoizedState, a];
  }
  function bi(a, b2, c2, d2) {
    a = { tag: a, create: b2, destroy: c2, deps: d2, next: null };
    b2 = M$1.updateQueue;
    null === b2 ? (b2 = { lastEffect: null, stores: null }, M$1.updateQueue = b2, b2.lastEffect = a.next = a) : (c2 = b2.lastEffect, null === c2 ? b2.lastEffect = a.next = a : (d2 = c2.next, c2.next = a, a.next = d2, b2.lastEffect = a));
    return a;
  }
  function ji() {
    return Uh().memoizedState;
  }
  function ki(a, b2, c2, d2) {
    var e2 = Th$1();
    M$1.flags |= a;
    e2.memoizedState = bi(1 | b2, c2, void 0, void 0 === d2 ? null : d2);
  }
  function li(a, b2, c2, d2) {
    var e2 = Uh();
    d2 = void 0 === d2 ? null : d2;
    var f2 = void 0;
    if (null !== N) {
      var g2 = N.memoizedState;
      f2 = g2.destroy;
      if (null !== d2 && Mh(d2, g2.deps)) {
        e2.memoizedState = bi(b2, c2, f2, d2);
        return;
      }
    }
    M$1.flags |= a;
    e2.memoizedState = bi(1 | b2, c2, f2, d2);
  }
  function mi(a, b2) {
    return ki(8390656, 8, a, b2);
  }
  function $h(a, b2) {
    return li(2048, 8, a, b2);
  }
  function ni(a, b2) {
    return li(4, 2, a, b2);
  }
  function oi(a, b2) {
    return li(4, 4, a, b2);
  }
  function pi(a, b2) {
    if ("function" === typeof b2)
      return a = a(), b2(a), function() {
        b2(null);
      };
    if (null !== b2 && void 0 !== b2)
      return a = a(), b2.current = a, function() {
        b2.current = null;
      };
  }
  function qi(a, b2, c2) {
    c2 = null !== c2 && void 0 !== c2 ? c2.concat([a]) : null;
    return li(4, 4, pi.bind(null, b2, a), c2);
  }
  function ri() {
  }
  function si(a, b2) {
    var c2 = Uh();
    b2 = void 0 === b2 ? null : b2;
    var d2 = c2.memoizedState;
    if (null !== d2 && null !== b2 && Mh(b2, d2[1]))
      return d2[0];
    c2.memoizedState = [a, b2];
    return a;
  }
  function ti(a, b2) {
    var c2 = Uh();
    b2 = void 0 === b2 ? null : b2;
    var d2 = c2.memoizedState;
    if (null !== d2 && null !== b2 && Mh(b2, d2[1]))
      return d2[0];
    a = a();
    c2.memoizedState = [a, b2];
    return a;
  }
  function ui(a, b2, c2) {
    if (0 === (Hh & 21))
      return a.baseState && (a.baseState = false, dh = true), a.memoizedState = c2;
    He$1(c2, b2) || (c2 = yc(), M$1.lanes |= c2, rh |= c2, a.baseState = true);
    return b2;
  }
  function vi(a, b2) {
    var c2 = C$1;
    C$1 = 0 !== c2 && 4 > c2 ? c2 : 4;
    a(true);
    var d2 = Gh.transition;
    Gh.transition = {};
    try {
      a(false), b2();
    } finally {
      C$1 = c2, Gh.transition = d2;
    }
  }
  function wi() {
    return Uh().memoizedState;
  }
  function xi(a, b2, c2) {
    var d2 = yi(a);
    c2 = { lane: d2, action: c2, hasEagerState: false, eagerState: null, next: null };
    if (zi(a))
      Ai(b2, c2);
    else if (c2 = hh(a, b2, c2, d2), null !== c2) {
      var e2 = R$1();
      gi(c2, a, d2, e2);
      Bi(c2, b2, d2);
    }
  }
  function ii(a, b2, c2) {
    var d2 = yi(a), e2 = { lane: d2, action: c2, hasEagerState: false, eagerState: null, next: null };
    if (zi(a))
      Ai(b2, e2);
    else {
      var f2 = a.alternate;
      if (0 === a.lanes && (null === f2 || 0 === f2.lanes) && (f2 = b2.lastRenderedReducer, null !== f2))
        try {
          var g2 = b2.lastRenderedState, h2 = f2(g2, c2);
          e2.hasEagerState = true;
          e2.eagerState = h2;
          if (He$1(h2, g2)) {
            var k2 = b2.interleaved;
            null === k2 ? (e2.next = e2, gh(b2)) : (e2.next = k2.next, k2.next = e2);
            b2.interleaved = e2;
            return;
          }
        } catch (l2) {
        } finally {
        }
      c2 = hh(a, b2, e2, d2);
      null !== c2 && (e2 = R$1(), gi(c2, a, d2, e2), Bi(c2, b2, d2));
    }
  }
  function zi(a) {
    var b2 = a.alternate;
    return a === M$1 || null !== b2 && b2 === M$1;
  }
  function Ai(a, b2) {
    Jh = Ih = true;
    var c2 = a.pending;
    null === c2 ? b2.next = b2 : (b2.next = c2.next, c2.next = b2);
    a.pending = b2;
  }
  function Bi(a, b2, c2) {
    if (0 !== (c2 & 4194240)) {
      var d2 = b2.lanes;
      d2 &= a.pendingLanes;
      c2 |= d2;
      b2.lanes = c2;
      Cc(a, c2);
    }
  }
  var Rh = { readContext: eh, useCallback: P, useContext: P, useEffect: P, useImperativeHandle: P, useInsertionEffect: P, useLayoutEffect: P, useMemo: P, useReducer: P, useRef: P, useState: P, useDebugValue: P, useDeferredValue: P, useTransition: P, useMutableSource: P, useSyncExternalStore: P, useId: P, unstable_isNewReconciler: false }, Oh = { readContext: eh, useCallback: function(a, b2) {
    Th$1().memoizedState = [a, void 0 === b2 ? null : b2];
    return a;
  }, useContext: eh, useEffect: mi, useImperativeHandle: function(a, b2, c2) {
    c2 = null !== c2 && void 0 !== c2 ? c2.concat([a]) : null;
    return ki(
      4194308,
      4,
      pi.bind(null, b2, a),
      c2
    );
  }, useLayoutEffect: function(a, b2) {
    return ki(4194308, 4, a, b2);
  }, useInsertionEffect: function(a, b2) {
    return ki(4, 2, a, b2);
  }, useMemo: function(a, b2) {
    var c2 = Th$1();
    b2 = void 0 === b2 ? null : b2;
    a = a();
    c2.memoizedState = [a, b2];
    return a;
  }, useReducer: function(a, b2, c2) {
    var d2 = Th$1();
    b2 = void 0 !== c2 ? c2(b2) : b2;
    d2.memoizedState = d2.baseState = b2;
    a = { pending: null, interleaved: null, lanes: 0, dispatch: null, lastRenderedReducer: a, lastRenderedState: b2 };
    d2.queue = a;
    a = a.dispatch = xi.bind(null, M$1, a);
    return [d2.memoizedState, a];
  }, useRef: function(a) {
    var b2 = Th$1();
    a = { current: a };
    return b2.memoizedState = a;
  }, useState: hi, useDebugValue: ri, useDeferredValue: function(a) {
    return Th$1().memoizedState = a;
  }, useTransition: function() {
    var a = hi(false), b2 = a[0];
    a = vi.bind(null, a[1]);
    Th$1().memoizedState = a;
    return [b2, a];
  }, useMutableSource: function() {
  }, useSyncExternalStore: function(a, b2, c2) {
    var d2 = M$1, e2 = Th$1();
    if (I$1) {
      if (void 0 === c2)
        throw Error(p$2(407));
      c2 = c2();
    } else {
      c2 = b2();
      if (null === Q$1)
        throw Error(p$2(349));
      0 !== (Hh & 30) || di(d2, b2, c2);
    }
    e2.memoizedState = c2;
    var f2 = { value: c2, getSnapshot: b2 };
    e2.queue = f2;
    mi(ai.bind(
      null,
      d2,
      f2,
      a
    ), [a]);
    d2.flags |= 2048;
    bi(9, ci.bind(null, d2, f2, c2, b2), void 0, null);
    return c2;
  }, useId: function() {
    var a = Th$1(), b2 = Q$1.identifierPrefix;
    if (I$1) {
      var c2 = sg;
      var d2 = rg;
      c2 = (d2 & ~(1 << 32 - oc(d2) - 1)).toString(32) + c2;
      b2 = ":" + b2 + "R" + c2;
      c2 = Kh++;
      0 < c2 && (b2 += "H" + c2.toString(32));
      b2 += ":";
    } else
      c2 = Lh++, b2 = ":" + b2 + "r" + c2.toString(32) + ":";
    return a.memoizedState = b2;
  }, unstable_isNewReconciler: false }, Ph = {
    readContext: eh,
    useCallback: si,
    useContext: eh,
    useEffect: $h,
    useImperativeHandle: qi,
    useInsertionEffect: ni,
    useLayoutEffect: oi,
    useMemo: ti,
    useReducer: Wh,
    useRef: ji,
    useState: function() {
      return Wh(Vh);
    },
    useDebugValue: ri,
    useDeferredValue: function(a) {
      var b2 = Uh();
      return ui(b2, N.memoizedState, a);
    },
    useTransition: function() {
      var a = Wh(Vh)[0], b2 = Uh().memoizedState;
      return [a, b2];
    },
    useMutableSource: Yh,
    useSyncExternalStore: Zh,
    useId: wi,
    unstable_isNewReconciler: false
  }, Qh = { readContext: eh, useCallback: si, useContext: eh, useEffect: $h, useImperativeHandle: qi, useInsertionEffect: ni, useLayoutEffect: oi, useMemo: ti, useReducer: Xh, useRef: ji, useState: function() {
    return Xh(Vh);
  }, useDebugValue: ri, useDeferredValue: function(a) {
    var b2 = Uh();
    return null === N ? b2.memoizedState = a : ui(b2, N.memoizedState, a);
  }, useTransition: function() {
    var a = Xh(Vh)[0], b2 = Uh().memoizedState;
    return [a, b2];
  }, useMutableSource: Yh, useSyncExternalStore: Zh, useId: wi, unstable_isNewReconciler: false };
  function Ci(a, b2) {
    if (a && a.defaultProps) {
      b2 = A$2({}, b2);
      a = a.defaultProps;
      for (var c2 in a)
        void 0 === b2[c2] && (b2[c2] = a[c2]);
      return b2;
    }
    return b2;
  }
  function Di(a, b2, c2, d2) {
    b2 = a.memoizedState;
    c2 = c2(d2, b2);
    c2 = null === c2 || void 0 === c2 ? b2 : A$2({}, b2, c2);
    a.memoizedState = c2;
    0 === a.lanes && (a.updateQueue.baseState = c2);
  }
  var Ei = { isMounted: function(a) {
    return (a = a._reactInternals) ? Vb(a) === a : false;
  }, enqueueSetState: function(a, b2, c2) {
    a = a._reactInternals;
    var d2 = R$1(), e2 = yi(a), f2 = mh(d2, e2);
    f2.payload = b2;
    void 0 !== c2 && null !== c2 && (f2.callback = c2);
    b2 = nh(a, f2, e2);
    null !== b2 && (gi(b2, a, e2, d2), oh(b2, a, e2));
  }, enqueueReplaceState: function(a, b2, c2) {
    a = a._reactInternals;
    var d2 = R$1(), e2 = yi(a), f2 = mh(d2, e2);
    f2.tag = 1;
    f2.payload = b2;
    void 0 !== c2 && null !== c2 && (f2.callback = c2);
    b2 = nh(a, f2, e2);
    null !== b2 && (gi(b2, a, e2, d2), oh(b2, a, e2));
  }, enqueueForceUpdate: function(a, b2) {
    a = a._reactInternals;
    var c2 = R$1(), d2 = yi(a), e2 = mh(c2, d2);
    e2.tag = 2;
    void 0 !== b2 && null !== b2 && (e2.callback = b2);
    b2 = nh(a, e2, d2);
    null !== b2 && (gi(b2, a, d2, c2), oh(b2, a, d2));
  } };
  function Fi(a, b2, c2, d2, e2, f2, g2) {
    a = a.stateNode;
    return "function" === typeof a.shouldComponentUpdate ? a.shouldComponentUpdate(d2, f2, g2) : b2.prototype && b2.prototype.isPureReactComponent ? !Ie$1(c2, d2) || !Ie$1(e2, f2) : true;
  }
  function Gi(a, b2, c2) {
    var d2 = false, e2 = Vf;
    var f2 = b2.contextType;
    "object" === typeof f2 && null !== f2 ? f2 = eh(f2) : (e2 = Zf(b2) ? Xf : H$1.current, d2 = b2.contextTypes, f2 = (d2 = null !== d2 && void 0 !== d2) ? Yf(a, e2) : Vf);
    b2 = new b2(c2, f2);
    a.memoizedState = null !== b2.state && void 0 !== b2.state ? b2.state : null;
    b2.updater = Ei;
    a.stateNode = b2;
    b2._reactInternals = a;
    d2 && (a = a.stateNode, a.__reactInternalMemoizedUnmaskedChildContext = e2, a.__reactInternalMemoizedMaskedChildContext = f2);
    return b2;
  }
  function Hi(a, b2, c2, d2) {
    a = b2.state;
    "function" === typeof b2.componentWillReceiveProps && b2.componentWillReceiveProps(c2, d2);
    "function" === typeof b2.UNSAFE_componentWillReceiveProps && b2.UNSAFE_componentWillReceiveProps(c2, d2);
    b2.state !== a && Ei.enqueueReplaceState(b2, b2.state, null);
  }
  function Ii(a, b2, c2, d2) {
    var e2 = a.stateNode;
    e2.props = c2;
    e2.state = a.memoizedState;
    e2.refs = {};
    kh(a);
    var f2 = b2.contextType;
    "object" === typeof f2 && null !== f2 ? e2.context = eh(f2) : (f2 = Zf(b2) ? Xf : H$1.current, e2.context = Yf(a, f2));
    e2.state = a.memoizedState;
    f2 = b2.getDerivedStateFromProps;
    "function" === typeof f2 && (Di(a, b2, f2, c2), e2.state = a.memoizedState);
    "function" === typeof b2.getDerivedStateFromProps || "function" === typeof e2.getSnapshotBeforeUpdate || "function" !== typeof e2.UNSAFE_componentWillMount && "function" !== typeof e2.componentWillMount || (b2 = e2.state, "function" === typeof e2.componentWillMount && e2.componentWillMount(), "function" === typeof e2.UNSAFE_componentWillMount && e2.UNSAFE_componentWillMount(), b2 !== e2.state && Ei.enqueueReplaceState(e2, e2.state, null), qh(a, c2, e2, d2), e2.state = a.memoizedState);
    "function" === typeof e2.componentDidMount && (a.flags |= 4194308);
  }
  function Ji(a, b2) {
    try {
      var c2 = "", d2 = b2;
      do
        c2 += Pa(d2), d2 = d2.return;
      while (d2);
      var e2 = c2;
    } catch (f2) {
      e2 = "\nError generating stack: " + f2.message + "\n" + f2.stack;
    }
    return { value: a, source: b2, stack: e2, digest: null };
  }
  function Ki(a, b2, c2) {
    return { value: a, source: null, stack: null != c2 ? c2 : null, digest: null != b2 ? b2 : null };
  }
  function Li(a, b2) {
    try {
      console.error(b2.value);
    } catch (c2) {
      setTimeout(function() {
        throw c2;
      });
    }
  }
  var Mi = "function" === typeof WeakMap ? WeakMap : Map;
  function Ni(a, b2, c2) {
    c2 = mh(-1, c2);
    c2.tag = 3;
    c2.payload = { element: null };
    var d2 = b2.value;
    c2.callback = function() {
      Oi || (Oi = true, Pi = d2);
      Li(a, b2);
    };
    return c2;
  }
  function Qi(a, b2, c2) {
    c2 = mh(-1, c2);
    c2.tag = 3;
    var d2 = a.type.getDerivedStateFromError;
    if ("function" === typeof d2) {
      var e2 = b2.value;
      c2.payload = function() {
        return d2(e2);
      };
      c2.callback = function() {
        Li(a, b2);
      };
    }
    var f2 = a.stateNode;
    null !== f2 && "function" === typeof f2.componentDidCatch && (c2.callback = function() {
      Li(a, b2);
      "function" !== typeof d2 && (null === Ri ? Ri = /* @__PURE__ */ new Set([this]) : Ri.add(this));
      var c3 = b2.stack;
      this.componentDidCatch(b2.value, { componentStack: null !== c3 ? c3 : "" });
    });
    return c2;
  }
  function Si(a, b2, c2) {
    var d2 = a.pingCache;
    if (null === d2) {
      d2 = a.pingCache = new Mi();
      var e2 = /* @__PURE__ */ new Set();
      d2.set(b2, e2);
    } else
      e2 = d2.get(b2), void 0 === e2 && (e2 = /* @__PURE__ */ new Set(), d2.set(b2, e2));
    e2.has(c2) || (e2.add(c2), a = Ti.bind(null, a, b2, c2), b2.then(a, a));
  }
  function Ui(a) {
    do {
      var b2;
      if (b2 = 13 === a.tag)
        b2 = a.memoizedState, b2 = null !== b2 ? null !== b2.dehydrated ? true : false : true;
      if (b2)
        return a;
      a = a.return;
    } while (null !== a);
    return null;
  }
  function Vi(a, b2, c2, d2, e2) {
    if (0 === (a.mode & 1))
      return a === b2 ? a.flags |= 65536 : (a.flags |= 128, c2.flags |= 131072, c2.flags &= -52805, 1 === c2.tag && (null === c2.alternate ? c2.tag = 17 : (b2 = mh(-1, 1), b2.tag = 2, nh(c2, b2, 1))), c2.lanes |= 1), a;
    a.flags |= 65536;
    a.lanes = e2;
    return a;
  }
  var Wi = ua.ReactCurrentOwner, dh = false;
  function Xi(a, b2, c2, d2) {
    b2.child = null === a ? Vg(b2, null, c2, d2) : Ug(b2, a.child, c2, d2);
  }
  function Yi(a, b2, c2, d2, e2) {
    c2 = c2.render;
    var f2 = b2.ref;
    ch(b2, e2);
    d2 = Nh(a, b2, c2, d2, f2, e2);
    c2 = Sh();
    if (null !== a && !dh)
      return b2.updateQueue = a.updateQueue, b2.flags &= -2053, a.lanes &= ~e2, Zi(a, b2, e2);
    I$1 && c2 && vg(b2);
    b2.flags |= 1;
    Xi(a, b2, d2, e2);
    return b2.child;
  }
  function $i(a, b2, c2, d2, e2) {
    if (null === a) {
      var f2 = c2.type;
      if ("function" === typeof f2 && !aj(f2) && void 0 === f2.defaultProps && null === c2.compare && void 0 === c2.defaultProps)
        return b2.tag = 15, b2.type = f2, bj(a, b2, f2, d2, e2);
      a = Rg(c2.type, null, d2, b2, b2.mode, e2);
      a.ref = b2.ref;
      a.return = b2;
      return b2.child = a;
    }
    f2 = a.child;
    if (0 === (a.lanes & e2)) {
      var g2 = f2.memoizedProps;
      c2 = c2.compare;
      c2 = null !== c2 ? c2 : Ie$1;
      if (c2(g2, d2) && a.ref === b2.ref)
        return Zi(a, b2, e2);
    }
    b2.flags |= 1;
    a = Pg(f2, d2);
    a.ref = b2.ref;
    a.return = b2;
    return b2.child = a;
  }
  function bj(a, b2, c2, d2, e2) {
    if (null !== a) {
      var f2 = a.memoizedProps;
      if (Ie$1(f2, d2) && a.ref === b2.ref)
        if (dh = false, b2.pendingProps = d2 = f2, 0 !== (a.lanes & e2))
          0 !== (a.flags & 131072) && (dh = true);
        else
          return b2.lanes = a.lanes, Zi(a, b2, e2);
    }
    return cj(a, b2, c2, d2, e2);
  }
  function dj(a, b2, c2) {
    var d2 = b2.pendingProps, e2 = d2.children, f2 = null !== a ? a.memoizedState : null;
    if ("hidden" === d2.mode)
      if (0 === (b2.mode & 1))
        b2.memoizedState = { baseLanes: 0, cachePool: null, transitions: null }, G$1(ej, fj), fj |= c2;
      else {
        if (0 === (c2 & 1073741824))
          return a = null !== f2 ? f2.baseLanes | c2 : c2, b2.lanes = b2.childLanes = 1073741824, b2.memoizedState = { baseLanes: a, cachePool: null, transitions: null }, b2.updateQueue = null, G$1(ej, fj), fj |= a, null;
        b2.memoizedState = { baseLanes: 0, cachePool: null, transitions: null };
        d2 = null !== f2 ? f2.baseLanes : c2;
        G$1(ej, fj);
        fj |= d2;
      }
    else
      null !== f2 ? (d2 = f2.baseLanes | c2, b2.memoizedState = null) : d2 = c2, G$1(ej, fj), fj |= d2;
    Xi(a, b2, e2, c2);
    return b2.child;
  }
  function gj(a, b2) {
    var c2 = b2.ref;
    if (null === a && null !== c2 || null !== a && a.ref !== c2)
      b2.flags |= 512, b2.flags |= 2097152;
  }
  function cj(a, b2, c2, d2, e2) {
    var f2 = Zf(c2) ? Xf : H$1.current;
    f2 = Yf(b2, f2);
    ch(b2, e2);
    c2 = Nh(a, b2, c2, d2, f2, e2);
    d2 = Sh();
    if (null !== a && !dh)
      return b2.updateQueue = a.updateQueue, b2.flags &= -2053, a.lanes &= ~e2, Zi(a, b2, e2);
    I$1 && d2 && vg(b2);
    b2.flags |= 1;
    Xi(a, b2, c2, e2);
    return b2.child;
  }
  function hj(a, b2, c2, d2, e2) {
    if (Zf(c2)) {
      var f2 = true;
      cg(b2);
    } else
      f2 = false;
    ch(b2, e2);
    if (null === b2.stateNode)
      ij(a, b2), Gi(b2, c2, d2), Ii(b2, c2, d2, e2), d2 = true;
    else if (null === a) {
      var g2 = b2.stateNode, h2 = b2.memoizedProps;
      g2.props = h2;
      var k2 = g2.context, l2 = c2.contextType;
      "object" === typeof l2 && null !== l2 ? l2 = eh(l2) : (l2 = Zf(c2) ? Xf : H$1.current, l2 = Yf(b2, l2));
      var m2 = c2.getDerivedStateFromProps, q2 = "function" === typeof m2 || "function" === typeof g2.getSnapshotBeforeUpdate;
      q2 || "function" !== typeof g2.UNSAFE_componentWillReceiveProps && "function" !== typeof g2.componentWillReceiveProps || (h2 !== d2 || k2 !== l2) && Hi(b2, g2, d2, l2);
      jh = false;
      var r2 = b2.memoizedState;
      g2.state = r2;
      qh(b2, d2, g2, e2);
      k2 = b2.memoizedState;
      h2 !== d2 || r2 !== k2 || Wf.current || jh ? ("function" === typeof m2 && (Di(b2, c2, m2, d2), k2 = b2.memoizedState), (h2 = jh || Fi(b2, c2, h2, d2, r2, k2, l2)) ? (q2 || "function" !== typeof g2.UNSAFE_componentWillMount && "function" !== typeof g2.componentWillMount || ("function" === typeof g2.componentWillMount && g2.componentWillMount(), "function" === typeof g2.UNSAFE_componentWillMount && g2.UNSAFE_componentWillMount()), "function" === typeof g2.componentDidMount && (b2.flags |= 4194308)) : ("function" === typeof g2.componentDidMount && (b2.flags |= 4194308), b2.memoizedProps = d2, b2.memoizedState = k2), g2.props = d2, g2.state = k2, g2.context = l2, d2 = h2) : ("function" === typeof g2.componentDidMount && (b2.flags |= 4194308), d2 = false);
    } else {
      g2 = b2.stateNode;
      lh(a, b2);
      h2 = b2.memoizedProps;
      l2 = b2.type === b2.elementType ? h2 : Ci(b2.type, h2);
      g2.props = l2;
      q2 = b2.pendingProps;
      r2 = g2.context;
      k2 = c2.contextType;
      "object" === typeof k2 && null !== k2 ? k2 = eh(k2) : (k2 = Zf(c2) ? Xf : H$1.current, k2 = Yf(b2, k2));
      var y2 = c2.getDerivedStateFromProps;
      (m2 = "function" === typeof y2 || "function" === typeof g2.getSnapshotBeforeUpdate) || "function" !== typeof g2.UNSAFE_componentWillReceiveProps && "function" !== typeof g2.componentWillReceiveProps || (h2 !== q2 || r2 !== k2) && Hi(b2, g2, d2, k2);
      jh = false;
      r2 = b2.memoizedState;
      g2.state = r2;
      qh(b2, d2, g2, e2);
      var n2 = b2.memoizedState;
      h2 !== q2 || r2 !== n2 || Wf.current || jh ? ("function" === typeof y2 && (Di(b2, c2, y2, d2), n2 = b2.memoizedState), (l2 = jh || Fi(b2, c2, l2, d2, r2, n2, k2) || false) ? (m2 || "function" !== typeof g2.UNSAFE_componentWillUpdate && "function" !== typeof g2.componentWillUpdate || ("function" === typeof g2.componentWillUpdate && g2.componentWillUpdate(d2, n2, k2), "function" === typeof g2.UNSAFE_componentWillUpdate && g2.UNSAFE_componentWillUpdate(d2, n2, k2)), "function" === typeof g2.componentDidUpdate && (b2.flags |= 4), "function" === typeof g2.getSnapshotBeforeUpdate && (b2.flags |= 1024)) : ("function" !== typeof g2.componentDidUpdate || h2 === a.memoizedProps && r2 === a.memoizedState || (b2.flags |= 4), "function" !== typeof g2.getSnapshotBeforeUpdate || h2 === a.memoizedProps && r2 === a.memoizedState || (b2.flags |= 1024), b2.memoizedProps = d2, b2.memoizedState = n2), g2.props = d2, g2.state = n2, g2.context = k2, d2 = l2) : ("function" !== typeof g2.componentDidUpdate || h2 === a.memoizedProps && r2 === a.memoizedState || (b2.flags |= 4), "function" !== typeof g2.getSnapshotBeforeUpdate || h2 === a.memoizedProps && r2 === a.memoizedState || (b2.flags |= 1024), d2 = false);
    }
    return jj(a, b2, c2, d2, f2, e2);
  }
  function jj(a, b2, c2, d2, e2, f2) {
    gj(a, b2);
    var g2 = 0 !== (b2.flags & 128);
    if (!d2 && !g2)
      return e2 && dg(b2, c2, false), Zi(a, b2, f2);
    d2 = b2.stateNode;
    Wi.current = b2;
    var h2 = g2 && "function" !== typeof c2.getDerivedStateFromError ? null : d2.render();
    b2.flags |= 1;
    null !== a && g2 ? (b2.child = Ug(b2, a.child, null, f2), b2.child = Ug(b2, null, h2, f2)) : Xi(a, b2, h2, f2);
    b2.memoizedState = d2.state;
    e2 && dg(b2, c2, true);
    return b2.child;
  }
  function kj(a) {
    var b2 = a.stateNode;
    b2.pendingContext ? ag(a, b2.pendingContext, b2.pendingContext !== b2.context) : b2.context && ag(a, b2.context, false);
    yh(a, b2.containerInfo);
  }
  function lj(a, b2, c2, d2, e2) {
    Ig();
    Jg(e2);
    b2.flags |= 256;
    Xi(a, b2, c2, d2);
    return b2.child;
  }
  var mj = { dehydrated: null, treeContext: null, retryLane: 0 };
  function nj(a) {
    return { baseLanes: a, cachePool: null, transitions: null };
  }
  function oj(a, b2, c2) {
    var d2 = b2.pendingProps, e2 = L$1.current, f2 = false, g2 = 0 !== (b2.flags & 128), h2;
    (h2 = g2) || (h2 = null !== a && null === a.memoizedState ? false : 0 !== (e2 & 2));
    if (h2)
      f2 = true, b2.flags &= -129;
    else if (null === a || null !== a.memoizedState)
      e2 |= 1;
    G$1(L$1, e2 & 1);
    if (null === a) {
      Eg(b2);
      a = b2.memoizedState;
      if (null !== a && (a = a.dehydrated, null !== a))
        return 0 === (b2.mode & 1) ? b2.lanes = 1 : "$!" === a.data ? b2.lanes = 8 : b2.lanes = 1073741824, null;
      g2 = d2.children;
      a = d2.fallback;
      return f2 ? (d2 = b2.mode, f2 = b2.child, g2 = { mode: "hidden", children: g2 }, 0 === (d2 & 1) && null !== f2 ? (f2.childLanes = 0, f2.pendingProps = g2) : f2 = pj(g2, d2, 0, null), a = Tg(a, d2, c2, null), f2.return = b2, a.return = b2, f2.sibling = a, b2.child = f2, b2.child.memoizedState = nj(c2), b2.memoizedState = mj, a) : qj(b2, g2);
    }
    e2 = a.memoizedState;
    if (null !== e2 && (h2 = e2.dehydrated, null !== h2))
      return rj(a, b2, g2, d2, h2, e2, c2);
    if (f2) {
      f2 = d2.fallback;
      g2 = b2.mode;
      e2 = a.child;
      h2 = e2.sibling;
      var k2 = { mode: "hidden", children: d2.children };
      0 === (g2 & 1) && b2.child !== e2 ? (d2 = b2.child, d2.childLanes = 0, d2.pendingProps = k2, b2.deletions = null) : (d2 = Pg(e2, k2), d2.subtreeFlags = e2.subtreeFlags & 14680064);
      null !== h2 ? f2 = Pg(h2, f2) : (f2 = Tg(f2, g2, c2, null), f2.flags |= 2);
      f2.return = b2;
      d2.return = b2;
      d2.sibling = f2;
      b2.child = d2;
      d2 = f2;
      f2 = b2.child;
      g2 = a.child.memoizedState;
      g2 = null === g2 ? nj(c2) : { baseLanes: g2.baseLanes | c2, cachePool: null, transitions: g2.transitions };
      f2.memoizedState = g2;
      f2.childLanes = a.childLanes & ~c2;
      b2.memoizedState = mj;
      return d2;
    }
    f2 = a.child;
    a = f2.sibling;
    d2 = Pg(f2, { mode: "visible", children: d2.children });
    0 === (b2.mode & 1) && (d2.lanes = c2);
    d2.return = b2;
    d2.sibling = null;
    null !== a && (c2 = b2.deletions, null === c2 ? (b2.deletions = [a], b2.flags |= 16) : c2.push(a));
    b2.child = d2;
    b2.memoizedState = null;
    return d2;
  }
  function qj(a, b2) {
    b2 = pj({ mode: "visible", children: b2 }, a.mode, 0, null);
    b2.return = a;
    return a.child = b2;
  }
  function sj(a, b2, c2, d2) {
    null !== d2 && Jg(d2);
    Ug(b2, a.child, null, c2);
    a = qj(b2, b2.pendingProps.children);
    a.flags |= 2;
    b2.memoizedState = null;
    return a;
  }
  function rj(a, b2, c2, d2, e2, f2, g2) {
    if (c2) {
      if (b2.flags & 256)
        return b2.flags &= -257, d2 = Ki(Error(p$2(422))), sj(a, b2, g2, d2);
      if (null !== b2.memoizedState)
        return b2.child = a.child, b2.flags |= 128, null;
      f2 = d2.fallback;
      e2 = b2.mode;
      d2 = pj({ mode: "visible", children: d2.children }, e2, 0, null);
      f2 = Tg(f2, e2, g2, null);
      f2.flags |= 2;
      d2.return = b2;
      f2.return = b2;
      d2.sibling = f2;
      b2.child = d2;
      0 !== (b2.mode & 1) && Ug(b2, a.child, null, g2);
      b2.child.memoizedState = nj(g2);
      b2.memoizedState = mj;
      return f2;
    }
    if (0 === (b2.mode & 1))
      return sj(a, b2, g2, null);
    if ("$!" === e2.data) {
      d2 = e2.nextSibling && e2.nextSibling.dataset;
      if (d2)
        var h2 = d2.dgst;
      d2 = h2;
      f2 = Error(p$2(419));
      d2 = Ki(f2, d2, void 0);
      return sj(a, b2, g2, d2);
    }
    h2 = 0 !== (g2 & a.childLanes);
    if (dh || h2) {
      d2 = Q$1;
      if (null !== d2) {
        switch (g2 & -g2) {
          case 4:
            e2 = 2;
            break;
          case 16:
            e2 = 8;
            break;
          case 64:
          case 128:
          case 256:
          case 512:
          case 1024:
          case 2048:
          case 4096:
          case 8192:
          case 16384:
          case 32768:
          case 65536:
          case 131072:
          case 262144:
          case 524288:
          case 1048576:
          case 2097152:
          case 4194304:
          case 8388608:
          case 16777216:
          case 33554432:
          case 67108864:
            e2 = 32;
            break;
          case 536870912:
            e2 = 268435456;
            break;
          default:
            e2 = 0;
        }
        e2 = 0 !== (e2 & (d2.suspendedLanes | g2)) ? 0 : e2;
        0 !== e2 && e2 !== f2.retryLane && (f2.retryLane = e2, ih(a, e2), gi(d2, a, e2, -1));
      }
      tj();
      d2 = Ki(Error(p$2(421)));
      return sj(a, b2, g2, d2);
    }
    if ("$?" === e2.data)
      return b2.flags |= 128, b2.child = a.child, b2 = uj.bind(null, a), e2._reactRetry = b2, null;
    a = f2.treeContext;
    yg = Lf(e2.nextSibling);
    xg = b2;
    I$1 = true;
    zg = null;
    null !== a && (og[pg++] = rg, og[pg++] = sg, og[pg++] = qg, rg = a.id, sg = a.overflow, qg = b2);
    b2 = qj(b2, d2.children);
    b2.flags |= 4096;
    return b2;
  }
  function vj(a, b2, c2) {
    a.lanes |= b2;
    var d2 = a.alternate;
    null !== d2 && (d2.lanes |= b2);
    bh(a.return, b2, c2);
  }
  function wj(a, b2, c2, d2, e2) {
    var f2 = a.memoizedState;
    null === f2 ? a.memoizedState = { isBackwards: b2, rendering: null, renderingStartTime: 0, last: d2, tail: c2, tailMode: e2 } : (f2.isBackwards = b2, f2.rendering = null, f2.renderingStartTime = 0, f2.last = d2, f2.tail = c2, f2.tailMode = e2);
  }
  function xj(a, b2, c2) {
    var d2 = b2.pendingProps, e2 = d2.revealOrder, f2 = d2.tail;
    Xi(a, b2, d2.children, c2);
    d2 = L$1.current;
    if (0 !== (d2 & 2))
      d2 = d2 & 1 | 2, b2.flags |= 128;
    else {
      if (null !== a && 0 !== (a.flags & 128))
        a:
          for (a = b2.child; null !== a; ) {
            if (13 === a.tag)
              null !== a.memoizedState && vj(a, c2, b2);
            else if (19 === a.tag)
              vj(a, c2, b2);
            else if (null !== a.child) {
              a.child.return = a;
              a = a.child;
              continue;
            }
            if (a === b2)
              break a;
            for (; null === a.sibling; ) {
              if (null === a.return || a.return === b2)
                break a;
              a = a.return;
            }
            a.sibling.return = a.return;
            a = a.sibling;
          }
      d2 &= 1;
    }
    G$1(L$1, d2);
    if (0 === (b2.mode & 1))
      b2.memoizedState = null;
    else
      switch (e2) {
        case "forwards":
          c2 = b2.child;
          for (e2 = null; null !== c2; )
            a = c2.alternate, null !== a && null === Ch(a) && (e2 = c2), c2 = c2.sibling;
          c2 = e2;
          null === c2 ? (e2 = b2.child, b2.child = null) : (e2 = c2.sibling, c2.sibling = null);
          wj(b2, false, e2, c2, f2);
          break;
        case "backwards":
          c2 = null;
          e2 = b2.child;
          for (b2.child = null; null !== e2; ) {
            a = e2.alternate;
            if (null !== a && null === Ch(a)) {
              b2.child = e2;
              break;
            }
            a = e2.sibling;
            e2.sibling = c2;
            c2 = e2;
            e2 = a;
          }
          wj(b2, true, c2, null, f2);
          break;
        case "together":
          wj(b2, false, null, null, void 0);
          break;
        default:
          b2.memoizedState = null;
      }
    return b2.child;
  }
  function ij(a, b2) {
    0 === (b2.mode & 1) && null !== a && (a.alternate = null, b2.alternate = null, b2.flags |= 2);
  }
  function Zi(a, b2, c2) {
    null !== a && (b2.dependencies = a.dependencies);
    rh |= b2.lanes;
    if (0 === (c2 & b2.childLanes))
      return null;
    if (null !== a && b2.child !== a.child)
      throw Error(p$2(153));
    if (null !== b2.child) {
      a = b2.child;
      c2 = Pg(a, a.pendingProps);
      b2.child = c2;
      for (c2.return = b2; null !== a.sibling; )
        a = a.sibling, c2 = c2.sibling = Pg(a, a.pendingProps), c2.return = b2;
      c2.sibling = null;
    }
    return b2.child;
  }
  function yj(a, b2, c2) {
    switch (b2.tag) {
      case 3:
        kj(b2);
        Ig();
        break;
      case 5:
        Ah(b2);
        break;
      case 1:
        Zf(b2.type) && cg(b2);
        break;
      case 4:
        yh(b2, b2.stateNode.containerInfo);
        break;
      case 10:
        var d2 = b2.type._context, e2 = b2.memoizedProps.value;
        G$1(Wg, d2._currentValue);
        d2._currentValue = e2;
        break;
      case 13:
        d2 = b2.memoizedState;
        if (null !== d2) {
          if (null !== d2.dehydrated)
            return G$1(L$1, L$1.current & 1), b2.flags |= 128, null;
          if (0 !== (c2 & b2.child.childLanes))
            return oj(a, b2, c2);
          G$1(L$1, L$1.current & 1);
          a = Zi(a, b2, c2);
          return null !== a ? a.sibling : null;
        }
        G$1(L$1, L$1.current & 1);
        break;
      case 19:
        d2 = 0 !== (c2 & b2.childLanes);
        if (0 !== (a.flags & 128)) {
          if (d2)
            return xj(a, b2, c2);
          b2.flags |= 128;
        }
        e2 = b2.memoizedState;
        null !== e2 && (e2.rendering = null, e2.tail = null, e2.lastEffect = null);
        G$1(L$1, L$1.current);
        if (d2)
          break;
        else
          return null;
      case 22:
      case 23:
        return b2.lanes = 0, dj(a, b2, c2);
    }
    return Zi(a, b2, c2);
  }
  var zj, Aj, Bj, Cj;
  zj = function(a, b2) {
    for (var c2 = b2.child; null !== c2; ) {
      if (5 === c2.tag || 6 === c2.tag)
        a.appendChild(c2.stateNode);
      else if (4 !== c2.tag && null !== c2.child) {
        c2.child.return = c2;
        c2 = c2.child;
        continue;
      }
      if (c2 === b2)
        break;
      for (; null === c2.sibling; ) {
        if (null === c2.return || c2.return === b2)
          return;
        c2 = c2.return;
      }
      c2.sibling.return = c2.return;
      c2 = c2.sibling;
    }
  };
  Aj = function() {
  };
  Bj = function(a, b2, c2, d2) {
    var e2 = a.memoizedProps;
    if (e2 !== d2) {
      a = b2.stateNode;
      xh(uh.current);
      var f2 = null;
      switch (c2) {
        case "input":
          e2 = Ya(a, e2);
          d2 = Ya(a, d2);
          f2 = [];
          break;
        case "select":
          e2 = A$2({}, e2, { value: void 0 });
          d2 = A$2({}, d2, { value: void 0 });
          f2 = [];
          break;
        case "textarea":
          e2 = gb(a, e2);
          d2 = gb(a, d2);
          f2 = [];
          break;
        default:
          "function" !== typeof e2.onClick && "function" === typeof d2.onClick && (a.onclick = Bf);
      }
      ub(c2, d2);
      var g2;
      c2 = null;
      for (l2 in e2)
        if (!d2.hasOwnProperty(l2) && e2.hasOwnProperty(l2) && null != e2[l2])
          if ("style" === l2) {
            var h2 = e2[l2];
            for (g2 in h2)
              h2.hasOwnProperty(g2) && (c2 || (c2 = {}), c2[g2] = "");
          } else
            "dangerouslySetInnerHTML" !== l2 && "children" !== l2 && "suppressContentEditableWarning" !== l2 && "suppressHydrationWarning" !== l2 && "autoFocus" !== l2 && (ea.hasOwnProperty(l2) ? f2 || (f2 = []) : (f2 = f2 || []).push(l2, null));
      for (l2 in d2) {
        var k2 = d2[l2];
        h2 = null != e2 ? e2[l2] : void 0;
        if (d2.hasOwnProperty(l2) && k2 !== h2 && (null != k2 || null != h2))
          if ("style" === l2)
            if (h2) {
              for (g2 in h2)
                !h2.hasOwnProperty(g2) || k2 && k2.hasOwnProperty(g2) || (c2 || (c2 = {}), c2[g2] = "");
              for (g2 in k2)
                k2.hasOwnProperty(g2) && h2[g2] !== k2[g2] && (c2 || (c2 = {}), c2[g2] = k2[g2]);
            } else
              c2 || (f2 || (f2 = []), f2.push(
                l2,
                c2
              )), c2 = k2;
          else
            "dangerouslySetInnerHTML" === l2 ? (k2 = k2 ? k2.__html : void 0, h2 = h2 ? h2.__html : void 0, null != k2 && h2 !== k2 && (f2 = f2 || []).push(l2, k2)) : "children" === l2 ? "string" !== typeof k2 && "number" !== typeof k2 || (f2 = f2 || []).push(l2, "" + k2) : "suppressContentEditableWarning" !== l2 && "suppressHydrationWarning" !== l2 && (ea.hasOwnProperty(l2) ? (null != k2 && "onScroll" === l2 && D$1("scroll", a), f2 || h2 === k2 || (f2 = [])) : (f2 = f2 || []).push(l2, k2));
      }
      c2 && (f2 = f2 || []).push("style", c2);
      var l2 = f2;
      if (b2.updateQueue = l2)
        b2.flags |= 4;
    }
  };
  Cj = function(a, b2, c2, d2) {
    c2 !== d2 && (b2.flags |= 4);
  };
  function Dj(a, b2) {
    if (!I$1)
      switch (a.tailMode) {
        case "hidden":
          b2 = a.tail;
          for (var c2 = null; null !== b2; )
            null !== b2.alternate && (c2 = b2), b2 = b2.sibling;
          null === c2 ? a.tail = null : c2.sibling = null;
          break;
        case "collapsed":
          c2 = a.tail;
          for (var d2 = null; null !== c2; )
            null !== c2.alternate && (d2 = c2), c2 = c2.sibling;
          null === d2 ? b2 || null === a.tail ? a.tail = null : a.tail.sibling = null : d2.sibling = null;
      }
  }
  function S$1(a) {
    var b2 = null !== a.alternate && a.alternate.child === a.child, c2 = 0, d2 = 0;
    if (b2)
      for (var e2 = a.child; null !== e2; )
        c2 |= e2.lanes | e2.childLanes, d2 |= e2.subtreeFlags & 14680064, d2 |= e2.flags & 14680064, e2.return = a, e2 = e2.sibling;
    else
      for (e2 = a.child; null !== e2; )
        c2 |= e2.lanes | e2.childLanes, d2 |= e2.subtreeFlags, d2 |= e2.flags, e2.return = a, e2 = e2.sibling;
    a.subtreeFlags |= d2;
    a.childLanes = c2;
    return b2;
  }
  function Ej(a, b2, c2) {
    var d2 = b2.pendingProps;
    wg(b2);
    switch (b2.tag) {
      case 2:
      case 16:
      case 15:
      case 0:
      case 11:
      case 7:
      case 8:
      case 12:
      case 9:
      case 14:
        return S$1(b2), null;
      case 1:
        return Zf(b2.type) && $f(), S$1(b2), null;
      case 3:
        d2 = b2.stateNode;
        zh();
        E(Wf);
        E(H$1);
        Eh();
        d2.pendingContext && (d2.context = d2.pendingContext, d2.pendingContext = null);
        if (null === a || null === a.child)
          Gg(b2) ? b2.flags |= 4 : null === a || a.memoizedState.isDehydrated && 0 === (b2.flags & 256) || (b2.flags |= 1024, null !== zg && (Fj(zg), zg = null));
        Aj(a, b2);
        S$1(b2);
        return null;
      case 5:
        Bh(b2);
        var e2 = xh(wh.current);
        c2 = b2.type;
        if (null !== a && null != b2.stateNode)
          Bj(a, b2, c2, d2, e2), a.ref !== b2.ref && (b2.flags |= 512, b2.flags |= 2097152);
        else {
          if (!d2) {
            if (null === b2.stateNode)
              throw Error(p$2(166));
            S$1(b2);
            return null;
          }
          a = xh(uh.current);
          if (Gg(b2)) {
            d2 = b2.stateNode;
            c2 = b2.type;
            var f2 = b2.memoizedProps;
            d2[Of] = b2;
            d2[Pf] = f2;
            a = 0 !== (b2.mode & 1);
            switch (c2) {
              case "dialog":
                D$1("cancel", d2);
                D$1("close", d2);
                break;
              case "iframe":
              case "object":
              case "embed":
                D$1("load", d2);
                break;
              case "video":
              case "audio":
                for (e2 = 0; e2 < lf.length; e2++)
                  D$1(lf[e2], d2);
                break;
              case "source":
                D$1("error", d2);
                break;
              case "img":
              case "image":
              case "link":
                D$1(
                  "error",
                  d2
                );
                D$1("load", d2);
                break;
              case "details":
                D$1("toggle", d2);
                break;
              case "input":
                Za(d2, f2);
                D$1("invalid", d2);
                break;
              case "select":
                d2._wrapperState = { wasMultiple: !!f2.multiple };
                D$1("invalid", d2);
                break;
              case "textarea":
                hb(d2, f2), D$1("invalid", d2);
            }
            ub(c2, f2);
            e2 = null;
            for (var g2 in f2)
              if (f2.hasOwnProperty(g2)) {
                var h2 = f2[g2];
                "children" === g2 ? "string" === typeof h2 ? d2.textContent !== h2 && (true !== f2.suppressHydrationWarning && Af(d2.textContent, h2, a), e2 = ["children", h2]) : "number" === typeof h2 && d2.textContent !== "" + h2 && (true !== f2.suppressHydrationWarning && Af(
                  d2.textContent,
                  h2,
                  a
                ), e2 = ["children", "" + h2]) : ea.hasOwnProperty(g2) && null != h2 && "onScroll" === g2 && D$1("scroll", d2);
              }
            switch (c2) {
              case "input":
                Va(d2);
                db(d2, f2, true);
                break;
              case "textarea":
                Va(d2);
                jb(d2);
                break;
              case "select":
              case "option":
                break;
              default:
                "function" === typeof f2.onClick && (d2.onclick = Bf);
            }
            d2 = e2;
            b2.updateQueue = d2;
            null !== d2 && (b2.flags |= 4);
          } else {
            g2 = 9 === e2.nodeType ? e2 : e2.ownerDocument;
            "http://www.w3.org/1999/xhtml" === a && (a = kb(c2));
            "http://www.w3.org/1999/xhtml" === a ? "script" === c2 ? (a = g2.createElement("div"), a.innerHTML = "<script><\/script>", a = a.removeChild(a.firstChild)) : "string" === typeof d2.is ? a = g2.createElement(c2, { is: d2.is }) : (a = g2.createElement(c2), "select" === c2 && (g2 = a, d2.multiple ? g2.multiple = true : d2.size && (g2.size = d2.size))) : a = g2.createElementNS(a, c2);
            a[Of] = b2;
            a[Pf] = d2;
            zj(a, b2, false, false);
            b2.stateNode = a;
            a: {
              g2 = vb(c2, d2);
              switch (c2) {
                case "dialog":
                  D$1("cancel", a);
                  D$1("close", a);
                  e2 = d2;
                  break;
                case "iframe":
                case "object":
                case "embed":
                  D$1("load", a);
                  e2 = d2;
                  break;
                case "video":
                case "audio":
                  for (e2 = 0; e2 < lf.length; e2++)
                    D$1(lf[e2], a);
                  e2 = d2;
                  break;
                case "source":
                  D$1("error", a);
                  e2 = d2;
                  break;
                case "img":
                case "image":
                case "link":
                  D$1(
                    "error",
                    a
                  );
                  D$1("load", a);
                  e2 = d2;
                  break;
                case "details":
                  D$1("toggle", a);
                  e2 = d2;
                  break;
                case "input":
                  Za(a, d2);
                  e2 = Ya(a, d2);
                  D$1("invalid", a);
                  break;
                case "option":
                  e2 = d2;
                  break;
                case "select":
                  a._wrapperState = { wasMultiple: !!d2.multiple };
                  e2 = A$2({}, d2, { value: void 0 });
                  D$1("invalid", a);
                  break;
                case "textarea":
                  hb(a, d2);
                  e2 = gb(a, d2);
                  D$1("invalid", a);
                  break;
                default:
                  e2 = d2;
              }
              ub(c2, e2);
              h2 = e2;
              for (f2 in h2)
                if (h2.hasOwnProperty(f2)) {
                  var k2 = h2[f2];
                  "style" === f2 ? sb(a, k2) : "dangerouslySetInnerHTML" === f2 ? (k2 = k2 ? k2.__html : void 0, null != k2 && nb(a, k2)) : "children" === f2 ? "string" === typeof k2 ? ("textarea" !== c2 || "" !== k2) && ob(a, k2) : "number" === typeof k2 && ob(a, "" + k2) : "suppressContentEditableWarning" !== f2 && "suppressHydrationWarning" !== f2 && "autoFocus" !== f2 && (ea.hasOwnProperty(f2) ? null != k2 && "onScroll" === f2 && D$1("scroll", a) : null != k2 && ta(a, f2, k2, g2));
                }
              switch (c2) {
                case "input":
                  Va(a);
                  db(a, d2, false);
                  break;
                case "textarea":
                  Va(a);
                  jb(a);
                  break;
                case "option":
                  null != d2.value && a.setAttribute("value", "" + Sa(d2.value));
                  break;
                case "select":
                  a.multiple = !!d2.multiple;
                  f2 = d2.value;
                  null != f2 ? fb(a, !!d2.multiple, f2, false) : null != d2.defaultValue && fb(
                    a,
                    !!d2.multiple,
                    d2.defaultValue,
                    true
                  );
                  break;
                default:
                  "function" === typeof e2.onClick && (a.onclick = Bf);
              }
              switch (c2) {
                case "button":
                case "input":
                case "select":
                case "textarea":
                  d2 = !!d2.autoFocus;
                  break a;
                case "img":
                  d2 = true;
                  break a;
                default:
                  d2 = false;
              }
            }
            d2 && (b2.flags |= 4);
          }
          null !== b2.ref && (b2.flags |= 512, b2.flags |= 2097152);
        }
        S$1(b2);
        return null;
      case 6:
        if (a && null != b2.stateNode)
          Cj(a, b2, a.memoizedProps, d2);
        else {
          if ("string" !== typeof d2 && null === b2.stateNode)
            throw Error(p$2(166));
          c2 = xh(wh.current);
          xh(uh.current);
          if (Gg(b2)) {
            d2 = b2.stateNode;
            c2 = b2.memoizedProps;
            d2[Of] = b2;
            if (f2 = d2.nodeValue !== c2) {
              if (a = xg, null !== a)
                switch (a.tag) {
                  case 3:
                    Af(d2.nodeValue, c2, 0 !== (a.mode & 1));
                    break;
                  case 5:
                    true !== a.memoizedProps.suppressHydrationWarning && Af(d2.nodeValue, c2, 0 !== (a.mode & 1));
                }
            }
            f2 && (b2.flags |= 4);
          } else
            d2 = (9 === c2.nodeType ? c2 : c2.ownerDocument).createTextNode(d2), d2[Of] = b2, b2.stateNode = d2;
        }
        S$1(b2);
        return null;
      case 13:
        E(L$1);
        d2 = b2.memoizedState;
        if (null === a || null !== a.memoizedState && null !== a.memoizedState.dehydrated) {
          if (I$1 && null !== yg && 0 !== (b2.mode & 1) && 0 === (b2.flags & 128))
            Hg(), Ig(), b2.flags |= 98560, f2 = false;
          else if (f2 = Gg(b2), null !== d2 && null !== d2.dehydrated) {
            if (null === a) {
              if (!f2)
                throw Error(p$2(318));
              f2 = b2.memoizedState;
              f2 = null !== f2 ? f2.dehydrated : null;
              if (!f2)
                throw Error(p$2(317));
              f2[Of] = b2;
            } else
              Ig(), 0 === (b2.flags & 128) && (b2.memoizedState = null), b2.flags |= 4;
            S$1(b2);
            f2 = false;
          } else
            null !== zg && (Fj(zg), zg = null), f2 = true;
          if (!f2)
            return b2.flags & 65536 ? b2 : null;
        }
        if (0 !== (b2.flags & 128))
          return b2.lanes = c2, b2;
        d2 = null !== d2;
        d2 !== (null !== a && null !== a.memoizedState) && d2 && (b2.child.flags |= 8192, 0 !== (b2.mode & 1) && (null === a || 0 !== (L$1.current & 1) ? 0 === T$1 && (T$1 = 3) : tj()));
        null !== b2.updateQueue && (b2.flags |= 4);
        S$1(b2);
        return null;
      case 4:
        return zh(), Aj(a, b2), null === a && sf(b2.stateNode.containerInfo), S$1(b2), null;
      case 10:
        return ah(b2.type._context), S$1(b2), null;
      case 17:
        return Zf(b2.type) && $f(), S$1(b2), null;
      case 19:
        E(L$1);
        f2 = b2.memoizedState;
        if (null === f2)
          return S$1(b2), null;
        d2 = 0 !== (b2.flags & 128);
        g2 = f2.rendering;
        if (null === g2)
          if (d2)
            Dj(f2, false);
          else {
            if (0 !== T$1 || null !== a && 0 !== (a.flags & 128))
              for (a = b2.child; null !== a; ) {
                g2 = Ch(a);
                if (null !== g2) {
                  b2.flags |= 128;
                  Dj(f2, false);
                  d2 = g2.updateQueue;
                  null !== d2 && (b2.updateQueue = d2, b2.flags |= 4);
                  b2.subtreeFlags = 0;
                  d2 = c2;
                  for (c2 = b2.child; null !== c2; )
                    f2 = c2, a = d2, f2.flags &= 14680066, g2 = f2.alternate, null === g2 ? (f2.childLanes = 0, f2.lanes = a, f2.child = null, f2.subtreeFlags = 0, f2.memoizedProps = null, f2.memoizedState = null, f2.updateQueue = null, f2.dependencies = null, f2.stateNode = null) : (f2.childLanes = g2.childLanes, f2.lanes = g2.lanes, f2.child = g2.child, f2.subtreeFlags = 0, f2.deletions = null, f2.memoizedProps = g2.memoizedProps, f2.memoizedState = g2.memoizedState, f2.updateQueue = g2.updateQueue, f2.type = g2.type, a = g2.dependencies, f2.dependencies = null === a ? null : { lanes: a.lanes, firstContext: a.firstContext }), c2 = c2.sibling;
                  G$1(L$1, L$1.current & 1 | 2);
                  return b2.child;
                }
                a = a.sibling;
              }
            null !== f2.tail && B$1() > Gj && (b2.flags |= 128, d2 = true, Dj(f2, false), b2.lanes = 4194304);
          }
        else {
          if (!d2)
            if (a = Ch(g2), null !== a) {
              if (b2.flags |= 128, d2 = true, c2 = a.updateQueue, null !== c2 && (b2.updateQueue = c2, b2.flags |= 4), Dj(f2, true), null === f2.tail && "hidden" === f2.tailMode && !g2.alternate && !I$1)
                return S$1(b2), null;
            } else
              2 * B$1() - f2.renderingStartTime > Gj && 1073741824 !== c2 && (b2.flags |= 128, d2 = true, Dj(f2, false), b2.lanes = 4194304);
          f2.isBackwards ? (g2.sibling = b2.child, b2.child = g2) : (c2 = f2.last, null !== c2 ? c2.sibling = g2 : b2.child = g2, f2.last = g2);
        }
        if (null !== f2.tail)
          return b2 = f2.tail, f2.rendering = b2, f2.tail = b2.sibling, f2.renderingStartTime = B$1(), b2.sibling = null, c2 = L$1.current, G$1(L$1, d2 ? c2 & 1 | 2 : c2 & 1), b2;
        S$1(b2);
        return null;
      case 22:
      case 23:
        return Hj(), d2 = null !== b2.memoizedState, null !== a && null !== a.memoizedState !== d2 && (b2.flags |= 8192), d2 && 0 !== (b2.mode & 1) ? 0 !== (fj & 1073741824) && (S$1(b2), b2.subtreeFlags & 6 && (b2.flags |= 8192)) : S$1(b2), null;
      case 24:
        return null;
      case 25:
        return null;
    }
    throw Error(p$2(156, b2.tag));
  }
  function Ij(a, b2) {
    wg(b2);
    switch (b2.tag) {
      case 1:
        return Zf(b2.type) && $f(), a = b2.flags, a & 65536 ? (b2.flags = a & -65537 | 128, b2) : null;
      case 3:
        return zh(), E(Wf), E(H$1), Eh(), a = b2.flags, 0 !== (a & 65536) && 0 === (a & 128) ? (b2.flags = a & -65537 | 128, b2) : null;
      case 5:
        return Bh(b2), null;
      case 13:
        E(L$1);
        a = b2.memoizedState;
        if (null !== a && null !== a.dehydrated) {
          if (null === b2.alternate)
            throw Error(p$2(340));
          Ig();
        }
        a = b2.flags;
        return a & 65536 ? (b2.flags = a & -65537 | 128, b2) : null;
      case 19:
        return E(L$1), null;
      case 4:
        return zh(), null;
      case 10:
        return ah(b2.type._context), null;
      case 22:
      case 23:
        return Hj(), null;
      case 24:
        return null;
      default:
        return null;
    }
  }
  var Jj = false, U$1 = false, Kj = "function" === typeof WeakSet ? WeakSet : Set, V$1 = null;
  function Lj(a, b2) {
    var c2 = a.ref;
    if (null !== c2)
      if ("function" === typeof c2)
        try {
          c2(null);
        } catch (d2) {
          W$1(a, b2, d2);
        }
      else
        c2.current = null;
  }
  function Mj(a, b2, c2) {
    try {
      c2();
    } catch (d2) {
      W$1(a, b2, d2);
    }
  }
  var Nj = false;
  function Oj(a, b2) {
    Cf = dd;
    a = Me$1();
    if (Ne$1(a)) {
      if ("selectionStart" in a)
        var c2 = { start: a.selectionStart, end: a.selectionEnd };
      else
        a: {
          c2 = (c2 = a.ownerDocument) && c2.defaultView || window;
          var d2 = c2.getSelection && c2.getSelection();
          if (d2 && 0 !== d2.rangeCount) {
            c2 = d2.anchorNode;
            var e2 = d2.anchorOffset, f2 = d2.focusNode;
            d2 = d2.focusOffset;
            try {
              c2.nodeType, f2.nodeType;
            } catch (F2) {
              c2 = null;
              break a;
            }
            var g2 = 0, h2 = -1, k2 = -1, l2 = 0, m2 = 0, q2 = a, r2 = null;
            b:
              for (; ; ) {
                for (var y2; ; ) {
                  q2 !== c2 || 0 !== e2 && 3 !== q2.nodeType || (h2 = g2 + e2);
                  q2 !== f2 || 0 !== d2 && 3 !== q2.nodeType || (k2 = g2 + d2);
                  3 === q2.nodeType && (g2 += q2.nodeValue.length);
                  if (null === (y2 = q2.firstChild))
                    break;
                  r2 = q2;
                  q2 = y2;
                }
                for (; ; ) {
                  if (q2 === a)
                    break b;
                  r2 === c2 && ++l2 === e2 && (h2 = g2);
                  r2 === f2 && ++m2 === d2 && (k2 = g2);
                  if (null !== (y2 = q2.nextSibling))
                    break;
                  q2 = r2;
                  r2 = q2.parentNode;
                }
                q2 = y2;
              }
            c2 = -1 === h2 || -1 === k2 ? null : { start: h2, end: k2 };
          } else
            c2 = null;
        }
      c2 = c2 || { start: 0, end: 0 };
    } else
      c2 = null;
    Df = { focusedElem: a, selectionRange: c2 };
    dd = false;
    for (V$1 = b2; null !== V$1; )
      if (b2 = V$1, a = b2.child, 0 !== (b2.subtreeFlags & 1028) && null !== a)
        a.return = b2, V$1 = a;
      else
        for (; null !== V$1; ) {
          b2 = V$1;
          try {
            var n2 = b2.alternate;
            if (0 !== (b2.flags & 1024))
              switch (b2.tag) {
                case 0:
                case 11:
                case 15:
                  break;
                case 1:
                  if (null !== n2) {
                    var t2 = n2.memoizedProps, J2 = n2.memoizedState, x2 = b2.stateNode, w2 = x2.getSnapshotBeforeUpdate(b2.elementType === b2.type ? t2 : Ci(b2.type, t2), J2);
                    x2.__reactInternalSnapshotBeforeUpdate = w2;
                  }
                  break;
                case 3:
                  var u2 = b2.stateNode.containerInfo;
                  1 === u2.nodeType ? u2.textContent = "" : 9 === u2.nodeType && u2.documentElement && u2.removeChild(u2.documentElement);
                  break;
                case 5:
                case 6:
                case 4:
                case 17:
                  break;
                default:
                  throw Error(p$2(163));
              }
          } catch (F2) {
            W$1(b2, b2.return, F2);
          }
          a = b2.sibling;
          if (null !== a) {
            a.return = b2.return;
            V$1 = a;
            break;
          }
          V$1 = b2.return;
        }
    n2 = Nj;
    Nj = false;
    return n2;
  }
  function Pj(a, b2, c2) {
    var d2 = b2.updateQueue;
    d2 = null !== d2 ? d2.lastEffect : null;
    if (null !== d2) {
      var e2 = d2 = d2.next;
      do {
        if ((e2.tag & a) === a) {
          var f2 = e2.destroy;
          e2.destroy = void 0;
          void 0 !== f2 && Mj(b2, c2, f2);
        }
        e2 = e2.next;
      } while (e2 !== d2);
    }
  }
  function Qj(a, b2) {
    b2 = b2.updateQueue;
    b2 = null !== b2 ? b2.lastEffect : null;
    if (null !== b2) {
      var c2 = b2 = b2.next;
      do {
        if ((c2.tag & a) === a) {
          var d2 = c2.create;
          c2.destroy = d2();
        }
        c2 = c2.next;
      } while (c2 !== b2);
    }
  }
  function Rj(a) {
    var b2 = a.ref;
    if (null !== b2) {
      var c2 = a.stateNode;
      switch (a.tag) {
        case 5:
          a = c2;
          break;
        default:
          a = c2;
      }
      "function" === typeof b2 ? b2(a) : b2.current = a;
    }
  }
  function Sj(a) {
    var b2 = a.alternate;
    null !== b2 && (a.alternate = null, Sj(b2));
    a.child = null;
    a.deletions = null;
    a.sibling = null;
    5 === a.tag && (b2 = a.stateNode, null !== b2 && (delete b2[Of], delete b2[Pf], delete b2[of], delete b2[Qf], delete b2[Rf]));
    a.stateNode = null;
    a.return = null;
    a.dependencies = null;
    a.memoizedProps = null;
    a.memoizedState = null;
    a.pendingProps = null;
    a.stateNode = null;
    a.updateQueue = null;
  }
  function Tj(a) {
    return 5 === a.tag || 3 === a.tag || 4 === a.tag;
  }
  function Uj(a) {
    a:
      for (; ; ) {
        for (; null === a.sibling; ) {
          if (null === a.return || Tj(a.return))
            return null;
          a = a.return;
        }
        a.sibling.return = a.return;
        for (a = a.sibling; 5 !== a.tag && 6 !== a.tag && 18 !== a.tag; ) {
          if (a.flags & 2)
            continue a;
          if (null === a.child || 4 === a.tag)
            continue a;
          else
            a.child.return = a, a = a.child;
        }
        if (!(a.flags & 2))
          return a.stateNode;
      }
  }
  function Vj(a, b2, c2) {
    var d2 = a.tag;
    if (5 === d2 || 6 === d2)
      a = a.stateNode, b2 ? 8 === c2.nodeType ? c2.parentNode.insertBefore(a, b2) : c2.insertBefore(a, b2) : (8 === c2.nodeType ? (b2 = c2.parentNode, b2.insertBefore(a, c2)) : (b2 = c2, b2.appendChild(a)), c2 = c2._reactRootContainer, null !== c2 && void 0 !== c2 || null !== b2.onclick || (b2.onclick = Bf));
    else if (4 !== d2 && (a = a.child, null !== a))
      for (Vj(a, b2, c2), a = a.sibling; null !== a; )
        Vj(a, b2, c2), a = a.sibling;
  }
  function Wj(a, b2, c2) {
    var d2 = a.tag;
    if (5 === d2 || 6 === d2)
      a = a.stateNode, b2 ? c2.insertBefore(a, b2) : c2.appendChild(a);
    else if (4 !== d2 && (a = a.child, null !== a))
      for (Wj(a, b2, c2), a = a.sibling; null !== a; )
        Wj(a, b2, c2), a = a.sibling;
  }
  var X$1 = null, Xj = false;
  function Yj(a, b2, c2) {
    for (c2 = c2.child; null !== c2; )
      Zj(a, b2, c2), c2 = c2.sibling;
  }
  function Zj(a, b2, c2) {
    if (lc && "function" === typeof lc.onCommitFiberUnmount)
      try {
        lc.onCommitFiberUnmount(kc, c2);
      } catch (h2) {
      }
    switch (c2.tag) {
      case 5:
        U$1 || Lj(c2, b2);
      case 6:
        var d2 = X$1, e2 = Xj;
        X$1 = null;
        Yj(a, b2, c2);
        X$1 = d2;
        Xj = e2;
        null !== X$1 && (Xj ? (a = X$1, c2 = c2.stateNode, 8 === a.nodeType ? a.parentNode.removeChild(c2) : a.removeChild(c2)) : X$1.removeChild(c2.stateNode));
        break;
      case 18:
        null !== X$1 && (Xj ? (a = X$1, c2 = c2.stateNode, 8 === a.nodeType ? Kf(a.parentNode, c2) : 1 === a.nodeType && Kf(a, c2), bd(a)) : Kf(X$1, c2.stateNode));
        break;
      case 4:
        d2 = X$1;
        e2 = Xj;
        X$1 = c2.stateNode.containerInfo;
        Xj = true;
        Yj(a, b2, c2);
        X$1 = d2;
        Xj = e2;
        break;
      case 0:
      case 11:
      case 14:
      case 15:
        if (!U$1 && (d2 = c2.updateQueue, null !== d2 && (d2 = d2.lastEffect, null !== d2))) {
          e2 = d2 = d2.next;
          do {
            var f2 = e2, g2 = f2.destroy;
            f2 = f2.tag;
            void 0 !== g2 && (0 !== (f2 & 2) ? Mj(c2, b2, g2) : 0 !== (f2 & 4) && Mj(c2, b2, g2));
            e2 = e2.next;
          } while (e2 !== d2);
        }
        Yj(a, b2, c2);
        break;
      case 1:
        if (!U$1 && (Lj(c2, b2), d2 = c2.stateNode, "function" === typeof d2.componentWillUnmount))
          try {
            d2.props = c2.memoizedProps, d2.state = c2.memoizedState, d2.componentWillUnmount();
          } catch (h2) {
            W$1(c2, b2, h2);
          }
        Yj(a, b2, c2);
        break;
      case 21:
        Yj(a, b2, c2);
        break;
      case 22:
        c2.mode & 1 ? (U$1 = (d2 = U$1) || null !== c2.memoizedState, Yj(a, b2, c2), U$1 = d2) : Yj(a, b2, c2);
        break;
      default:
        Yj(a, b2, c2);
    }
  }
  function ak(a) {
    var b2 = a.updateQueue;
    if (null !== b2) {
      a.updateQueue = null;
      var c2 = a.stateNode;
      null === c2 && (c2 = a.stateNode = new Kj());
      b2.forEach(function(b3) {
        var d2 = bk.bind(null, a, b3);
        c2.has(b3) || (c2.add(b3), b3.then(d2, d2));
      });
    }
  }
  function ck(a, b2) {
    var c2 = b2.deletions;
    if (null !== c2)
      for (var d2 = 0; d2 < c2.length; d2++) {
        var e2 = c2[d2];
        try {
          var f2 = a, g2 = b2, h2 = g2;
          a:
            for (; null !== h2; ) {
              switch (h2.tag) {
                case 5:
                  X$1 = h2.stateNode;
                  Xj = false;
                  break a;
                case 3:
                  X$1 = h2.stateNode.containerInfo;
                  Xj = true;
                  break a;
                case 4:
                  X$1 = h2.stateNode.containerInfo;
                  Xj = true;
                  break a;
              }
              h2 = h2.return;
            }
          if (null === X$1)
            throw Error(p$2(160));
          Zj(f2, g2, e2);
          X$1 = null;
          Xj = false;
          var k2 = e2.alternate;
          null !== k2 && (k2.return = null);
          e2.return = null;
        } catch (l2) {
          W$1(e2, b2, l2);
        }
      }
    if (b2.subtreeFlags & 12854)
      for (b2 = b2.child; null !== b2; )
        dk(b2, a), b2 = b2.sibling;
  }
  function dk(a, b2) {
    var c2 = a.alternate, d2 = a.flags;
    switch (a.tag) {
      case 0:
      case 11:
      case 14:
      case 15:
        ck(b2, a);
        ek(a);
        if (d2 & 4) {
          try {
            Pj(3, a, a.return), Qj(3, a);
          } catch (t2) {
            W$1(a, a.return, t2);
          }
          try {
            Pj(5, a, a.return);
          } catch (t2) {
            W$1(a, a.return, t2);
          }
        }
        break;
      case 1:
        ck(b2, a);
        ek(a);
        d2 & 512 && null !== c2 && Lj(c2, c2.return);
        break;
      case 5:
        ck(b2, a);
        ek(a);
        d2 & 512 && null !== c2 && Lj(c2, c2.return);
        if (a.flags & 32) {
          var e2 = a.stateNode;
          try {
            ob(e2, "");
          } catch (t2) {
            W$1(a, a.return, t2);
          }
        }
        if (d2 & 4 && (e2 = a.stateNode, null != e2)) {
          var f2 = a.memoizedProps, g2 = null !== c2 ? c2.memoizedProps : f2, h2 = a.type, k2 = a.updateQueue;
          a.updateQueue = null;
          if (null !== k2)
            try {
              "input" === h2 && "radio" === f2.type && null != f2.name && ab(e2, f2);
              vb(h2, g2);
              var l2 = vb(h2, f2);
              for (g2 = 0; g2 < k2.length; g2 += 2) {
                var m2 = k2[g2], q2 = k2[g2 + 1];
                "style" === m2 ? sb(e2, q2) : "dangerouslySetInnerHTML" === m2 ? nb(e2, q2) : "children" === m2 ? ob(e2, q2) : ta(e2, m2, q2, l2);
              }
              switch (h2) {
                case "input":
                  bb(e2, f2);
                  break;
                case "textarea":
                  ib(e2, f2);
                  break;
                case "select":
                  var r2 = e2._wrapperState.wasMultiple;
                  e2._wrapperState.wasMultiple = !!f2.multiple;
                  var y2 = f2.value;
                  null != y2 ? fb(e2, !!f2.multiple, y2, false) : r2 !== !!f2.multiple && (null != f2.defaultValue ? fb(
                    e2,
                    !!f2.multiple,
                    f2.defaultValue,
                    true
                  ) : fb(e2, !!f2.multiple, f2.multiple ? [] : "", false));
              }
              e2[Pf] = f2;
            } catch (t2) {
              W$1(a, a.return, t2);
            }
        }
        break;
      case 6:
        ck(b2, a);
        ek(a);
        if (d2 & 4) {
          if (null === a.stateNode)
            throw Error(p$2(162));
          e2 = a.stateNode;
          f2 = a.memoizedProps;
          try {
            e2.nodeValue = f2;
          } catch (t2) {
            W$1(a, a.return, t2);
          }
        }
        break;
      case 3:
        ck(b2, a);
        ek(a);
        if (d2 & 4 && null !== c2 && c2.memoizedState.isDehydrated)
          try {
            bd(b2.containerInfo);
          } catch (t2) {
            W$1(a, a.return, t2);
          }
        break;
      case 4:
        ck(b2, a);
        ek(a);
        break;
      case 13:
        ck(b2, a);
        ek(a);
        e2 = a.child;
        e2.flags & 8192 && (f2 = null !== e2.memoizedState, e2.stateNode.isHidden = f2, !f2 || null !== e2.alternate && null !== e2.alternate.memoizedState || (fk = B$1()));
        d2 & 4 && ak(a);
        break;
      case 22:
        m2 = null !== c2 && null !== c2.memoizedState;
        a.mode & 1 ? (U$1 = (l2 = U$1) || m2, ck(b2, a), U$1 = l2) : ck(b2, a);
        ek(a);
        if (d2 & 8192) {
          l2 = null !== a.memoizedState;
          if ((a.stateNode.isHidden = l2) && !m2 && 0 !== (a.mode & 1))
            for (V$1 = a, m2 = a.child; null !== m2; ) {
              for (q2 = V$1 = m2; null !== V$1; ) {
                r2 = V$1;
                y2 = r2.child;
                switch (r2.tag) {
                  case 0:
                  case 11:
                  case 14:
                  case 15:
                    Pj(4, r2, r2.return);
                    break;
                  case 1:
                    Lj(r2, r2.return);
                    var n2 = r2.stateNode;
                    if ("function" === typeof n2.componentWillUnmount) {
                      d2 = r2;
                      c2 = r2.return;
                      try {
                        b2 = d2, n2.props = b2.memoizedProps, n2.state = b2.memoizedState, n2.componentWillUnmount();
                      } catch (t2) {
                        W$1(d2, c2, t2);
                      }
                    }
                    break;
                  case 5:
                    Lj(r2, r2.return);
                    break;
                  case 22:
                    if (null !== r2.memoizedState) {
                      gk(q2);
                      continue;
                    }
                }
                null !== y2 ? (y2.return = r2, V$1 = y2) : gk(q2);
              }
              m2 = m2.sibling;
            }
          a:
            for (m2 = null, q2 = a; ; ) {
              if (5 === q2.tag) {
                if (null === m2) {
                  m2 = q2;
                  try {
                    e2 = q2.stateNode, l2 ? (f2 = e2.style, "function" === typeof f2.setProperty ? f2.setProperty("display", "none", "important") : f2.display = "none") : (h2 = q2.stateNode, k2 = q2.memoizedProps.style, g2 = void 0 !== k2 && null !== k2 && k2.hasOwnProperty("display") ? k2.display : null, h2.style.display = rb("display", g2));
                  } catch (t2) {
                    W$1(a, a.return, t2);
                  }
                }
              } else if (6 === q2.tag) {
                if (null === m2)
                  try {
                    q2.stateNode.nodeValue = l2 ? "" : q2.memoizedProps;
                  } catch (t2) {
                    W$1(a, a.return, t2);
                  }
              } else if ((22 !== q2.tag && 23 !== q2.tag || null === q2.memoizedState || q2 === a) && null !== q2.child) {
                q2.child.return = q2;
                q2 = q2.child;
                continue;
              }
              if (q2 === a)
                break a;
              for (; null === q2.sibling; ) {
                if (null === q2.return || q2.return === a)
                  break a;
                m2 === q2 && (m2 = null);
                q2 = q2.return;
              }
              m2 === q2 && (m2 = null);
              q2.sibling.return = q2.return;
              q2 = q2.sibling;
            }
        }
        break;
      case 19:
        ck(b2, a);
        ek(a);
        d2 & 4 && ak(a);
        break;
      case 21:
        break;
      default:
        ck(
          b2,
          a
        ), ek(a);
    }
  }
  function ek(a) {
    var b2 = a.flags;
    if (b2 & 2) {
      try {
        a: {
          for (var c2 = a.return; null !== c2; ) {
            if (Tj(c2)) {
              var d2 = c2;
              break a;
            }
            c2 = c2.return;
          }
          throw Error(p$2(160));
        }
        switch (d2.tag) {
          case 5:
            var e2 = d2.stateNode;
            d2.flags & 32 && (ob(e2, ""), d2.flags &= -33);
            var f2 = Uj(a);
            Wj(a, f2, e2);
            break;
          case 3:
          case 4:
            var g2 = d2.stateNode.containerInfo, h2 = Uj(a);
            Vj(a, h2, g2);
            break;
          default:
            throw Error(p$2(161));
        }
      } catch (k2) {
        W$1(a, a.return, k2);
      }
      a.flags &= -3;
    }
    b2 & 4096 && (a.flags &= -4097);
  }
  function hk(a, b2, c2) {
    V$1 = a;
    ik(a);
  }
  function ik(a, b2, c2) {
    for (var d2 = 0 !== (a.mode & 1); null !== V$1; ) {
      var e2 = V$1, f2 = e2.child;
      if (22 === e2.tag && d2) {
        var g2 = null !== e2.memoizedState || Jj;
        if (!g2) {
          var h2 = e2.alternate, k2 = null !== h2 && null !== h2.memoizedState || U$1;
          h2 = Jj;
          var l2 = U$1;
          Jj = g2;
          if ((U$1 = k2) && !l2)
            for (V$1 = e2; null !== V$1; )
              g2 = V$1, k2 = g2.child, 22 === g2.tag && null !== g2.memoizedState ? jk(e2) : null !== k2 ? (k2.return = g2, V$1 = k2) : jk(e2);
          for (; null !== f2; )
            V$1 = f2, ik(f2), f2 = f2.sibling;
          V$1 = e2;
          Jj = h2;
          U$1 = l2;
        }
        kk(a);
      } else
        0 !== (e2.subtreeFlags & 8772) && null !== f2 ? (f2.return = e2, V$1 = f2) : kk(a);
    }
  }
  function kk(a) {
    for (; null !== V$1; ) {
      var b2 = V$1;
      if (0 !== (b2.flags & 8772)) {
        var c2 = b2.alternate;
        try {
          if (0 !== (b2.flags & 8772))
            switch (b2.tag) {
              case 0:
              case 11:
              case 15:
                U$1 || Qj(5, b2);
                break;
              case 1:
                var d2 = b2.stateNode;
                if (b2.flags & 4 && !U$1)
                  if (null === c2)
                    d2.componentDidMount();
                  else {
                    var e2 = b2.elementType === b2.type ? c2.memoizedProps : Ci(b2.type, c2.memoizedProps);
                    d2.componentDidUpdate(e2, c2.memoizedState, d2.__reactInternalSnapshotBeforeUpdate);
                  }
                var f2 = b2.updateQueue;
                null !== f2 && sh(b2, f2, d2);
                break;
              case 3:
                var g2 = b2.updateQueue;
                if (null !== g2) {
                  c2 = null;
                  if (null !== b2.child)
                    switch (b2.child.tag) {
                      case 5:
                        c2 = b2.child.stateNode;
                        break;
                      case 1:
                        c2 = b2.child.stateNode;
                    }
                  sh(b2, g2, c2);
                }
                break;
              case 5:
                var h2 = b2.stateNode;
                if (null === c2 && b2.flags & 4) {
                  c2 = h2;
                  var k2 = b2.memoizedProps;
                  switch (b2.type) {
                    case "button":
                    case "input":
                    case "select":
                    case "textarea":
                      k2.autoFocus && c2.focus();
                      break;
                    case "img":
                      k2.src && (c2.src = k2.src);
                  }
                }
                break;
              case 6:
                break;
              case 4:
                break;
              case 12:
                break;
              case 13:
                if (null === b2.memoizedState) {
                  var l2 = b2.alternate;
                  if (null !== l2) {
                    var m2 = l2.memoizedState;
                    if (null !== m2) {
                      var q2 = m2.dehydrated;
                      null !== q2 && bd(q2);
                    }
                  }
                }
                break;
              case 19:
              case 17:
              case 21:
              case 22:
              case 23:
              case 25:
                break;
              default:
                throw Error(p$2(163));
            }
          U$1 || b2.flags & 512 && Rj(b2);
        } catch (r2) {
          W$1(b2, b2.return, r2);
        }
      }
      if (b2 === a) {
        V$1 = null;
        break;
      }
      c2 = b2.sibling;
      if (null !== c2) {
        c2.return = b2.return;
        V$1 = c2;
        break;
      }
      V$1 = b2.return;
    }
  }
  function gk(a) {
    for (; null !== V$1; ) {
      var b2 = V$1;
      if (b2 === a) {
        V$1 = null;
        break;
      }
      var c2 = b2.sibling;
      if (null !== c2) {
        c2.return = b2.return;
        V$1 = c2;
        break;
      }
      V$1 = b2.return;
    }
  }
  function jk(a) {
    for (; null !== V$1; ) {
      var b2 = V$1;
      try {
        switch (b2.tag) {
          case 0:
          case 11:
          case 15:
            var c2 = b2.return;
            try {
              Qj(4, b2);
            } catch (k2) {
              W$1(b2, c2, k2);
            }
            break;
          case 1:
            var d2 = b2.stateNode;
            if ("function" === typeof d2.componentDidMount) {
              var e2 = b2.return;
              try {
                d2.componentDidMount();
              } catch (k2) {
                W$1(b2, e2, k2);
              }
            }
            var f2 = b2.return;
            try {
              Rj(b2);
            } catch (k2) {
              W$1(b2, f2, k2);
            }
            break;
          case 5:
            var g2 = b2.return;
            try {
              Rj(b2);
            } catch (k2) {
              W$1(b2, g2, k2);
            }
        }
      } catch (k2) {
        W$1(b2, b2.return, k2);
      }
      if (b2 === a) {
        V$1 = null;
        break;
      }
      var h2 = b2.sibling;
      if (null !== h2) {
        h2.return = b2.return;
        V$1 = h2;
        break;
      }
      V$1 = b2.return;
    }
  }
  var lk = Math.ceil, mk = ua.ReactCurrentDispatcher, nk = ua.ReactCurrentOwner, ok = ua.ReactCurrentBatchConfig, K$1 = 0, Q$1 = null, Y$1 = null, Z$1 = 0, fj = 0, ej = Uf(0), T$1 = 0, pk = null, rh = 0, qk = 0, rk = 0, sk = null, tk = null, fk = 0, Gj = Infinity, uk = null, Oi = false, Pi = null, Ri = null, vk = false, wk = null, xk = 0, yk = 0, zk = null, Ak = -1, Bk = 0;
  function R$1() {
    return 0 !== (K$1 & 6) ? B$1() : -1 !== Ak ? Ak : Ak = B$1();
  }
  function yi(a) {
    if (0 === (a.mode & 1))
      return 1;
    if (0 !== (K$1 & 2) && 0 !== Z$1)
      return Z$1 & -Z$1;
    if (null !== Kg.transition)
      return 0 === Bk && (Bk = yc()), Bk;
    a = C$1;
    if (0 !== a)
      return a;
    a = window.event;
    a = void 0 === a ? 16 : jd(a.type);
    return a;
  }
  function gi(a, b2, c2, d2) {
    if (50 < yk)
      throw yk = 0, zk = null, Error(p$2(185));
    Ac(a, c2, d2);
    if (0 === (K$1 & 2) || a !== Q$1)
      a === Q$1 && (0 === (K$1 & 2) && (qk |= c2), 4 === T$1 && Ck(a, Z$1)), Dk(a, d2), 1 === c2 && 0 === K$1 && 0 === (b2.mode & 1) && (Gj = B$1() + 500, fg && jg());
  }
  function Dk(a, b2) {
    var c2 = a.callbackNode;
    wc(a, b2);
    var d2 = uc(a, a === Q$1 ? Z$1 : 0);
    if (0 === d2)
      null !== c2 && bc(c2), a.callbackNode = null, a.callbackPriority = 0;
    else if (b2 = d2 & -d2, a.callbackPriority !== b2) {
      null != c2 && bc(c2);
      if (1 === b2)
        0 === a.tag ? ig(Ek.bind(null, a)) : hg(Ek.bind(null, a)), Jf(function() {
          0 === (K$1 & 6) && jg();
        }), c2 = null;
      else {
        switch (Dc(d2)) {
          case 1:
            c2 = fc;
            break;
          case 4:
            c2 = gc;
            break;
          case 16:
            c2 = hc;
            break;
          case 536870912:
            c2 = jc;
            break;
          default:
            c2 = hc;
        }
        c2 = Fk(c2, Gk.bind(null, a));
      }
      a.callbackPriority = b2;
      a.callbackNode = c2;
    }
  }
  function Gk(a, b2) {
    Ak = -1;
    Bk = 0;
    if (0 !== (K$1 & 6))
      throw Error(p$2(327));
    var c2 = a.callbackNode;
    if (Hk() && a.callbackNode !== c2)
      return null;
    var d2 = uc(a, a === Q$1 ? Z$1 : 0);
    if (0 === d2)
      return null;
    if (0 !== (d2 & 30) || 0 !== (d2 & a.expiredLanes) || b2)
      b2 = Ik(a, d2);
    else {
      b2 = d2;
      var e2 = K$1;
      K$1 |= 2;
      var f2 = Jk();
      if (Q$1 !== a || Z$1 !== b2)
        uk = null, Gj = B$1() + 500, Kk(a, b2);
      do
        try {
          Lk();
          break;
        } catch (h2) {
          Mk(a, h2);
        }
      while (1);
      $g();
      mk.current = f2;
      K$1 = e2;
      null !== Y$1 ? b2 = 0 : (Q$1 = null, Z$1 = 0, b2 = T$1);
    }
    if (0 !== b2) {
      2 === b2 && (e2 = xc(a), 0 !== e2 && (d2 = e2, b2 = Nk(a, e2)));
      if (1 === b2)
        throw c2 = pk, Kk(a, 0), Ck(a, d2), Dk(a, B$1()), c2;
      if (6 === b2)
        Ck(a, d2);
      else {
        e2 = a.current.alternate;
        if (0 === (d2 & 30) && !Ok(e2) && (b2 = Ik(a, d2), 2 === b2 && (f2 = xc(a), 0 !== f2 && (d2 = f2, b2 = Nk(a, f2))), 1 === b2))
          throw c2 = pk, Kk(a, 0), Ck(a, d2), Dk(a, B$1()), c2;
        a.finishedWork = e2;
        a.finishedLanes = d2;
        switch (b2) {
          case 0:
          case 1:
            throw Error(p$2(345));
          case 2:
            Pk(a, tk, uk);
            break;
          case 3:
            Ck(a, d2);
            if ((d2 & 130023424) === d2 && (b2 = fk + 500 - B$1(), 10 < b2)) {
              if (0 !== uc(a, 0))
                break;
              e2 = a.suspendedLanes;
              if ((e2 & d2) !== d2) {
                R$1();
                a.pingedLanes |= a.suspendedLanes & e2;
                break;
              }
              a.timeoutHandle = Ff(Pk.bind(null, a, tk, uk), b2);
              break;
            }
            Pk(a, tk, uk);
            break;
          case 4:
            Ck(a, d2);
            if ((d2 & 4194240) === d2)
              break;
            b2 = a.eventTimes;
            for (e2 = -1; 0 < d2; ) {
              var g2 = 31 - oc(d2);
              f2 = 1 << g2;
              g2 = b2[g2];
              g2 > e2 && (e2 = g2);
              d2 &= ~f2;
            }
            d2 = e2;
            d2 = B$1() - d2;
            d2 = (120 > d2 ? 120 : 480 > d2 ? 480 : 1080 > d2 ? 1080 : 1920 > d2 ? 1920 : 3e3 > d2 ? 3e3 : 4320 > d2 ? 4320 : 1960 * lk(d2 / 1960)) - d2;
            if (10 < d2) {
              a.timeoutHandle = Ff(Pk.bind(null, a, tk, uk), d2);
              break;
            }
            Pk(a, tk, uk);
            break;
          case 5:
            Pk(a, tk, uk);
            break;
          default:
            throw Error(p$2(329));
        }
      }
    }
    Dk(a, B$1());
    return a.callbackNode === c2 ? Gk.bind(null, a) : null;
  }
  function Nk(a, b2) {
    var c2 = sk;
    a.current.memoizedState.isDehydrated && (Kk(a, b2).flags |= 256);
    a = Ik(a, b2);
    2 !== a && (b2 = tk, tk = c2, null !== b2 && Fj(b2));
    return a;
  }
  function Fj(a) {
    null === tk ? tk = a : tk.push.apply(tk, a);
  }
  function Ok(a) {
    for (var b2 = a; ; ) {
      if (b2.flags & 16384) {
        var c2 = b2.updateQueue;
        if (null !== c2 && (c2 = c2.stores, null !== c2))
          for (var d2 = 0; d2 < c2.length; d2++) {
            var e2 = c2[d2], f2 = e2.getSnapshot;
            e2 = e2.value;
            try {
              if (!He$1(f2(), e2))
                return false;
            } catch (g2) {
              return false;
            }
          }
      }
      c2 = b2.child;
      if (b2.subtreeFlags & 16384 && null !== c2)
        c2.return = b2, b2 = c2;
      else {
        if (b2 === a)
          break;
        for (; null === b2.sibling; ) {
          if (null === b2.return || b2.return === a)
            return true;
          b2 = b2.return;
        }
        b2.sibling.return = b2.return;
        b2 = b2.sibling;
      }
    }
    return true;
  }
  function Ck(a, b2) {
    b2 &= ~rk;
    b2 &= ~qk;
    a.suspendedLanes |= b2;
    a.pingedLanes &= ~b2;
    for (a = a.expirationTimes; 0 < b2; ) {
      var c2 = 31 - oc(b2), d2 = 1 << c2;
      a[c2] = -1;
      b2 &= ~d2;
    }
  }
  function Ek(a) {
    if (0 !== (K$1 & 6))
      throw Error(p$2(327));
    Hk();
    var b2 = uc(a, 0);
    if (0 === (b2 & 1))
      return Dk(a, B$1()), null;
    var c2 = Ik(a, b2);
    if (0 !== a.tag && 2 === c2) {
      var d2 = xc(a);
      0 !== d2 && (b2 = d2, c2 = Nk(a, d2));
    }
    if (1 === c2)
      throw c2 = pk, Kk(a, 0), Ck(a, b2), Dk(a, B$1()), c2;
    if (6 === c2)
      throw Error(p$2(345));
    a.finishedWork = a.current.alternate;
    a.finishedLanes = b2;
    Pk(a, tk, uk);
    Dk(a, B$1());
    return null;
  }
  function Qk(a, b2) {
    var c2 = K$1;
    K$1 |= 1;
    try {
      return a(b2);
    } finally {
      K$1 = c2, 0 === K$1 && (Gj = B$1() + 500, fg && jg());
    }
  }
  function Rk(a) {
    null !== wk && 0 === wk.tag && 0 === (K$1 & 6) && Hk();
    var b2 = K$1;
    K$1 |= 1;
    var c2 = ok.transition, d2 = C$1;
    try {
      if (ok.transition = null, C$1 = 1, a)
        return a();
    } finally {
      C$1 = d2, ok.transition = c2, K$1 = b2, 0 === (K$1 & 6) && jg();
    }
  }
  function Hj() {
    fj = ej.current;
    E(ej);
  }
  function Kk(a, b2) {
    a.finishedWork = null;
    a.finishedLanes = 0;
    var c2 = a.timeoutHandle;
    -1 !== c2 && (a.timeoutHandle = -1, Gf(c2));
    if (null !== Y$1)
      for (c2 = Y$1.return; null !== c2; ) {
        var d2 = c2;
        wg(d2);
        switch (d2.tag) {
          case 1:
            d2 = d2.type.childContextTypes;
            null !== d2 && void 0 !== d2 && $f();
            break;
          case 3:
            zh();
            E(Wf);
            E(H$1);
            Eh();
            break;
          case 5:
            Bh(d2);
            break;
          case 4:
            zh();
            break;
          case 13:
            E(L$1);
            break;
          case 19:
            E(L$1);
            break;
          case 10:
            ah(d2.type._context);
            break;
          case 22:
          case 23:
            Hj();
        }
        c2 = c2.return;
      }
    Q$1 = a;
    Y$1 = a = Pg(a.current, null);
    Z$1 = fj = b2;
    T$1 = 0;
    pk = null;
    rk = qk = rh = 0;
    tk = sk = null;
    if (null !== fh) {
      for (b2 = 0; b2 < fh.length; b2++)
        if (c2 = fh[b2], d2 = c2.interleaved, null !== d2) {
          c2.interleaved = null;
          var e2 = d2.next, f2 = c2.pending;
          if (null !== f2) {
            var g2 = f2.next;
            f2.next = e2;
            d2.next = g2;
          }
          c2.pending = d2;
        }
      fh = null;
    }
    return a;
  }
  function Mk(a, b2) {
    do {
      var c2 = Y$1;
      try {
        $g();
        Fh.current = Rh;
        if (Ih) {
          for (var d2 = M$1.memoizedState; null !== d2; ) {
            var e2 = d2.queue;
            null !== e2 && (e2.pending = null);
            d2 = d2.next;
          }
          Ih = false;
        }
        Hh = 0;
        O$1 = N = M$1 = null;
        Jh = false;
        Kh = 0;
        nk.current = null;
        if (null === c2 || null === c2.return) {
          T$1 = 1;
          pk = b2;
          Y$1 = null;
          break;
        }
        a: {
          var f2 = a, g2 = c2.return, h2 = c2, k2 = b2;
          b2 = Z$1;
          h2.flags |= 32768;
          if (null !== k2 && "object" === typeof k2 && "function" === typeof k2.then) {
            var l2 = k2, m2 = h2, q2 = m2.tag;
            if (0 === (m2.mode & 1) && (0 === q2 || 11 === q2 || 15 === q2)) {
              var r2 = m2.alternate;
              r2 ? (m2.updateQueue = r2.updateQueue, m2.memoizedState = r2.memoizedState, m2.lanes = r2.lanes) : (m2.updateQueue = null, m2.memoizedState = null);
            }
            var y2 = Ui(g2);
            if (null !== y2) {
              y2.flags &= -257;
              Vi(y2, g2, h2, f2, b2);
              y2.mode & 1 && Si(f2, l2, b2);
              b2 = y2;
              k2 = l2;
              var n2 = b2.updateQueue;
              if (null === n2) {
                var t2 = /* @__PURE__ */ new Set();
                t2.add(k2);
                b2.updateQueue = t2;
              } else
                n2.add(k2);
              break a;
            } else {
              if (0 === (b2 & 1)) {
                Si(f2, l2, b2);
                tj();
                break a;
              }
              k2 = Error(p$2(426));
            }
          } else if (I$1 && h2.mode & 1) {
            var J2 = Ui(g2);
            if (null !== J2) {
              0 === (J2.flags & 65536) && (J2.flags |= 256);
              Vi(J2, g2, h2, f2, b2);
              Jg(Ji(k2, h2));
              break a;
            }
          }
          f2 = k2 = Ji(k2, h2);
          4 !== T$1 && (T$1 = 2);
          null === sk ? sk = [f2] : sk.push(f2);
          f2 = g2;
          do {
            switch (f2.tag) {
              case 3:
                f2.flags |= 65536;
                b2 &= -b2;
                f2.lanes |= b2;
                var x2 = Ni(f2, k2, b2);
                ph(f2, x2);
                break a;
              case 1:
                h2 = k2;
                var w2 = f2.type, u2 = f2.stateNode;
                if (0 === (f2.flags & 128) && ("function" === typeof w2.getDerivedStateFromError || null !== u2 && "function" === typeof u2.componentDidCatch && (null === Ri || !Ri.has(u2)))) {
                  f2.flags |= 65536;
                  b2 &= -b2;
                  f2.lanes |= b2;
                  var F2 = Qi(f2, h2, b2);
                  ph(f2, F2);
                  break a;
                }
            }
            f2 = f2.return;
          } while (null !== f2);
        }
        Sk(c2);
      } catch (na) {
        b2 = na;
        Y$1 === c2 && null !== c2 && (Y$1 = c2 = c2.return);
        continue;
      }
      break;
    } while (1);
  }
  function Jk() {
    var a = mk.current;
    mk.current = Rh;
    return null === a ? Rh : a;
  }
  function tj() {
    if (0 === T$1 || 3 === T$1 || 2 === T$1)
      T$1 = 4;
    null === Q$1 || 0 === (rh & 268435455) && 0 === (qk & 268435455) || Ck(Q$1, Z$1);
  }
  function Ik(a, b2) {
    var c2 = K$1;
    K$1 |= 2;
    var d2 = Jk();
    if (Q$1 !== a || Z$1 !== b2)
      uk = null, Kk(a, b2);
    do
      try {
        Tk();
        break;
      } catch (e2) {
        Mk(a, e2);
      }
    while (1);
    $g();
    K$1 = c2;
    mk.current = d2;
    if (null !== Y$1)
      throw Error(p$2(261));
    Q$1 = null;
    Z$1 = 0;
    return T$1;
  }
  function Tk() {
    for (; null !== Y$1; )
      Uk(Y$1);
  }
  function Lk() {
    for (; null !== Y$1 && !cc(); )
      Uk(Y$1);
  }
  function Uk(a) {
    var b2 = Vk(a.alternate, a, fj);
    a.memoizedProps = a.pendingProps;
    null === b2 ? Sk(a) : Y$1 = b2;
    nk.current = null;
  }
  function Sk(a) {
    var b2 = a;
    do {
      var c2 = b2.alternate;
      a = b2.return;
      if (0 === (b2.flags & 32768)) {
        if (c2 = Ej(c2, b2, fj), null !== c2) {
          Y$1 = c2;
          return;
        }
      } else {
        c2 = Ij(c2, b2);
        if (null !== c2) {
          c2.flags &= 32767;
          Y$1 = c2;
          return;
        }
        if (null !== a)
          a.flags |= 32768, a.subtreeFlags = 0, a.deletions = null;
        else {
          T$1 = 6;
          Y$1 = null;
          return;
        }
      }
      b2 = b2.sibling;
      if (null !== b2) {
        Y$1 = b2;
        return;
      }
      Y$1 = b2 = a;
    } while (null !== b2);
    0 === T$1 && (T$1 = 5);
  }
  function Pk(a, b2, c2) {
    var d2 = C$1, e2 = ok.transition;
    try {
      ok.transition = null, C$1 = 1, Wk(a, b2, c2, d2);
    } finally {
      ok.transition = e2, C$1 = d2;
    }
    return null;
  }
  function Wk(a, b2, c2, d2) {
    do
      Hk();
    while (null !== wk);
    if (0 !== (K$1 & 6))
      throw Error(p$2(327));
    c2 = a.finishedWork;
    var e2 = a.finishedLanes;
    if (null === c2)
      return null;
    a.finishedWork = null;
    a.finishedLanes = 0;
    if (c2 === a.current)
      throw Error(p$2(177));
    a.callbackNode = null;
    a.callbackPriority = 0;
    var f2 = c2.lanes | c2.childLanes;
    Bc(a, f2);
    a === Q$1 && (Y$1 = Q$1 = null, Z$1 = 0);
    0 === (c2.subtreeFlags & 2064) && 0 === (c2.flags & 2064) || vk || (vk = true, Fk(hc, function() {
      Hk();
      return null;
    }));
    f2 = 0 !== (c2.flags & 15990);
    if (0 !== (c2.subtreeFlags & 15990) || f2) {
      f2 = ok.transition;
      ok.transition = null;
      var g2 = C$1;
      C$1 = 1;
      var h2 = K$1;
      K$1 |= 4;
      nk.current = null;
      Oj(a, c2);
      dk(c2, a);
      Oe$1(Df);
      dd = !!Cf;
      Df = Cf = null;
      a.current = c2;
      hk(c2);
      dc();
      K$1 = h2;
      C$1 = g2;
      ok.transition = f2;
    } else
      a.current = c2;
    vk && (vk = false, wk = a, xk = e2);
    f2 = a.pendingLanes;
    0 === f2 && (Ri = null);
    mc(c2.stateNode);
    Dk(a, B$1());
    if (null !== b2)
      for (d2 = a.onRecoverableError, c2 = 0; c2 < b2.length; c2++)
        e2 = b2[c2], d2(e2.value, { componentStack: e2.stack, digest: e2.digest });
    if (Oi)
      throw Oi = false, a = Pi, Pi = null, a;
    0 !== (xk & 1) && 0 !== a.tag && Hk();
    f2 = a.pendingLanes;
    0 !== (f2 & 1) ? a === zk ? yk++ : (yk = 0, zk = a) : yk = 0;
    jg();
    return null;
  }
  function Hk() {
    if (null !== wk) {
      var a = Dc(xk), b2 = ok.transition, c2 = C$1;
      try {
        ok.transition = null;
        C$1 = 16 > a ? 16 : a;
        if (null === wk)
          var d2 = false;
        else {
          a = wk;
          wk = null;
          xk = 0;
          if (0 !== (K$1 & 6))
            throw Error(p$2(331));
          var e2 = K$1;
          K$1 |= 4;
          for (V$1 = a.current; null !== V$1; ) {
            var f2 = V$1, g2 = f2.child;
            if (0 !== (V$1.flags & 16)) {
              var h2 = f2.deletions;
              if (null !== h2) {
                for (var k2 = 0; k2 < h2.length; k2++) {
                  var l2 = h2[k2];
                  for (V$1 = l2; null !== V$1; ) {
                    var m2 = V$1;
                    switch (m2.tag) {
                      case 0:
                      case 11:
                      case 15:
                        Pj(8, m2, f2);
                    }
                    var q2 = m2.child;
                    if (null !== q2)
                      q2.return = m2, V$1 = q2;
                    else
                      for (; null !== V$1; ) {
                        m2 = V$1;
                        var r2 = m2.sibling, y2 = m2.return;
                        Sj(m2);
                        if (m2 === l2) {
                          V$1 = null;
                          break;
                        }
                        if (null !== r2) {
                          r2.return = y2;
                          V$1 = r2;
                          break;
                        }
                        V$1 = y2;
                      }
                  }
                }
                var n2 = f2.alternate;
                if (null !== n2) {
                  var t2 = n2.child;
                  if (null !== t2) {
                    n2.child = null;
                    do {
                      var J2 = t2.sibling;
                      t2.sibling = null;
                      t2 = J2;
                    } while (null !== t2);
                  }
                }
                V$1 = f2;
              }
            }
            if (0 !== (f2.subtreeFlags & 2064) && null !== g2)
              g2.return = f2, V$1 = g2;
            else
              b:
                for (; null !== V$1; ) {
                  f2 = V$1;
                  if (0 !== (f2.flags & 2048))
                    switch (f2.tag) {
                      case 0:
                      case 11:
                      case 15:
                        Pj(9, f2, f2.return);
                    }
                  var x2 = f2.sibling;
                  if (null !== x2) {
                    x2.return = f2.return;
                    V$1 = x2;
                    break b;
                  }
                  V$1 = f2.return;
                }
          }
          var w2 = a.current;
          for (V$1 = w2; null !== V$1; ) {
            g2 = V$1;
            var u2 = g2.child;
            if (0 !== (g2.subtreeFlags & 2064) && null !== u2)
              u2.return = g2, V$1 = u2;
            else
              b:
                for (g2 = w2; null !== V$1; ) {
                  h2 = V$1;
                  if (0 !== (h2.flags & 2048))
                    try {
                      switch (h2.tag) {
                        case 0:
                        case 11:
                        case 15:
                          Qj(9, h2);
                      }
                    } catch (na) {
                      W$1(h2, h2.return, na);
                    }
                  if (h2 === g2) {
                    V$1 = null;
                    break b;
                  }
                  var F2 = h2.sibling;
                  if (null !== F2) {
                    F2.return = h2.return;
                    V$1 = F2;
                    break b;
                  }
                  V$1 = h2.return;
                }
          }
          K$1 = e2;
          jg();
          if (lc && "function" === typeof lc.onPostCommitFiberRoot)
            try {
              lc.onPostCommitFiberRoot(kc, a);
            } catch (na) {
            }
          d2 = true;
        }
        return d2;
      } finally {
        C$1 = c2, ok.transition = b2;
      }
    }
    return false;
  }
  function Xk(a, b2, c2) {
    b2 = Ji(c2, b2);
    b2 = Ni(a, b2, 1);
    a = nh(a, b2, 1);
    b2 = R$1();
    null !== a && (Ac(a, 1, b2), Dk(a, b2));
  }
  function W$1(a, b2, c2) {
    if (3 === a.tag)
      Xk(a, a, c2);
    else
      for (; null !== b2; ) {
        if (3 === b2.tag) {
          Xk(b2, a, c2);
          break;
        } else if (1 === b2.tag) {
          var d2 = b2.stateNode;
          if ("function" === typeof b2.type.getDerivedStateFromError || "function" === typeof d2.componentDidCatch && (null === Ri || !Ri.has(d2))) {
            a = Ji(c2, a);
            a = Qi(b2, a, 1);
            b2 = nh(b2, a, 1);
            a = R$1();
            null !== b2 && (Ac(b2, 1, a), Dk(b2, a));
            break;
          }
        }
        b2 = b2.return;
      }
  }
  function Ti(a, b2, c2) {
    var d2 = a.pingCache;
    null !== d2 && d2.delete(b2);
    b2 = R$1();
    a.pingedLanes |= a.suspendedLanes & c2;
    Q$1 === a && (Z$1 & c2) === c2 && (4 === T$1 || 3 === T$1 && (Z$1 & 130023424) === Z$1 && 500 > B$1() - fk ? Kk(a, 0) : rk |= c2);
    Dk(a, b2);
  }
  function Yk(a, b2) {
    0 === b2 && (0 === (a.mode & 1) ? b2 = 1 : (b2 = sc, sc <<= 1, 0 === (sc & 130023424) && (sc = 4194304)));
    var c2 = R$1();
    a = ih(a, b2);
    null !== a && (Ac(a, b2, c2), Dk(a, c2));
  }
  function uj(a) {
    var b2 = a.memoizedState, c2 = 0;
    null !== b2 && (c2 = b2.retryLane);
    Yk(a, c2);
  }
  function bk(a, b2) {
    var c2 = 0;
    switch (a.tag) {
      case 13:
        var d2 = a.stateNode;
        var e2 = a.memoizedState;
        null !== e2 && (c2 = e2.retryLane);
        break;
      case 19:
        d2 = a.stateNode;
        break;
      default:
        throw Error(p$2(314));
    }
    null !== d2 && d2.delete(b2);
    Yk(a, c2);
  }
  var Vk;
  Vk = function(a, b2, c2) {
    if (null !== a)
      if (a.memoizedProps !== b2.pendingProps || Wf.current)
        dh = true;
      else {
        if (0 === (a.lanes & c2) && 0 === (b2.flags & 128))
          return dh = false, yj(a, b2, c2);
        dh = 0 !== (a.flags & 131072) ? true : false;
      }
    else
      dh = false, I$1 && 0 !== (b2.flags & 1048576) && ug(b2, ng, b2.index);
    b2.lanes = 0;
    switch (b2.tag) {
      case 2:
        var d2 = b2.type;
        ij(a, b2);
        a = b2.pendingProps;
        var e2 = Yf(b2, H$1.current);
        ch(b2, c2);
        e2 = Nh(null, b2, d2, a, e2, c2);
        var f2 = Sh();
        b2.flags |= 1;
        "object" === typeof e2 && null !== e2 && "function" === typeof e2.render && void 0 === e2.$$typeof ? (b2.tag = 1, b2.memoizedState = null, b2.updateQueue = null, Zf(d2) ? (f2 = true, cg(b2)) : f2 = false, b2.memoizedState = null !== e2.state && void 0 !== e2.state ? e2.state : null, kh(b2), e2.updater = Ei, b2.stateNode = e2, e2._reactInternals = b2, Ii(b2, d2, a, c2), b2 = jj(null, b2, d2, true, f2, c2)) : (b2.tag = 0, I$1 && f2 && vg(b2), Xi(null, b2, e2, c2), b2 = b2.child);
        return b2;
      case 16:
        d2 = b2.elementType;
        a: {
          ij(a, b2);
          a = b2.pendingProps;
          e2 = d2._init;
          d2 = e2(d2._payload);
          b2.type = d2;
          e2 = b2.tag = Zk(d2);
          a = Ci(d2, a);
          switch (e2) {
            case 0:
              b2 = cj(null, b2, d2, a, c2);
              break a;
            case 1:
              b2 = hj(null, b2, d2, a, c2);
              break a;
            case 11:
              b2 = Yi(null, b2, d2, a, c2);
              break a;
            case 14:
              b2 = $i(null, b2, d2, Ci(d2.type, a), c2);
              break a;
          }
          throw Error(p$2(
            306,
            d2,
            ""
          ));
        }
        return b2;
      case 0:
        return d2 = b2.type, e2 = b2.pendingProps, e2 = b2.elementType === d2 ? e2 : Ci(d2, e2), cj(a, b2, d2, e2, c2);
      case 1:
        return d2 = b2.type, e2 = b2.pendingProps, e2 = b2.elementType === d2 ? e2 : Ci(d2, e2), hj(a, b2, d2, e2, c2);
      case 3:
        a: {
          kj(b2);
          if (null === a)
            throw Error(p$2(387));
          d2 = b2.pendingProps;
          f2 = b2.memoizedState;
          e2 = f2.element;
          lh(a, b2);
          qh(b2, d2, null, c2);
          var g2 = b2.memoizedState;
          d2 = g2.element;
          if (f2.isDehydrated)
            if (f2 = { element: d2, isDehydrated: false, cache: g2.cache, pendingSuspenseBoundaries: g2.pendingSuspenseBoundaries, transitions: g2.transitions }, b2.updateQueue.baseState = f2, b2.memoizedState = f2, b2.flags & 256) {
              e2 = Ji(Error(p$2(423)), b2);
              b2 = lj(a, b2, d2, c2, e2);
              break a;
            } else if (d2 !== e2) {
              e2 = Ji(Error(p$2(424)), b2);
              b2 = lj(a, b2, d2, c2, e2);
              break a;
            } else
              for (yg = Lf(b2.stateNode.containerInfo.firstChild), xg = b2, I$1 = true, zg = null, c2 = Vg(b2, null, d2, c2), b2.child = c2; c2; )
                c2.flags = c2.flags & -3 | 4096, c2 = c2.sibling;
          else {
            Ig();
            if (d2 === e2) {
              b2 = Zi(a, b2, c2);
              break a;
            }
            Xi(a, b2, d2, c2);
          }
          b2 = b2.child;
        }
        return b2;
      case 5:
        return Ah(b2), null === a && Eg(b2), d2 = b2.type, e2 = b2.pendingProps, f2 = null !== a ? a.memoizedProps : null, g2 = e2.children, Ef(d2, e2) ? g2 = null : null !== f2 && Ef(d2, f2) && (b2.flags |= 32), gj(a, b2), Xi(a, b2, g2, c2), b2.child;
      case 6:
        return null === a && Eg(b2), null;
      case 13:
        return oj(a, b2, c2);
      case 4:
        return yh(b2, b2.stateNode.containerInfo), d2 = b2.pendingProps, null === a ? b2.child = Ug(b2, null, d2, c2) : Xi(a, b2, d2, c2), b2.child;
      case 11:
        return d2 = b2.type, e2 = b2.pendingProps, e2 = b2.elementType === d2 ? e2 : Ci(d2, e2), Yi(a, b2, d2, e2, c2);
      case 7:
        return Xi(a, b2, b2.pendingProps, c2), b2.child;
      case 8:
        return Xi(a, b2, b2.pendingProps.children, c2), b2.child;
      case 12:
        return Xi(a, b2, b2.pendingProps.children, c2), b2.child;
      case 10:
        a: {
          d2 = b2.type._context;
          e2 = b2.pendingProps;
          f2 = b2.memoizedProps;
          g2 = e2.value;
          G$1(Wg, d2._currentValue);
          d2._currentValue = g2;
          if (null !== f2)
            if (He$1(f2.value, g2)) {
              if (f2.children === e2.children && !Wf.current) {
                b2 = Zi(a, b2, c2);
                break a;
              }
            } else
              for (f2 = b2.child, null !== f2 && (f2.return = b2); null !== f2; ) {
                var h2 = f2.dependencies;
                if (null !== h2) {
                  g2 = f2.child;
                  for (var k2 = h2.firstContext; null !== k2; ) {
                    if (k2.context === d2) {
                      if (1 === f2.tag) {
                        k2 = mh(-1, c2 & -c2);
                        k2.tag = 2;
                        var l2 = f2.updateQueue;
                        if (null !== l2) {
                          l2 = l2.shared;
                          var m2 = l2.pending;
                          null === m2 ? k2.next = k2 : (k2.next = m2.next, m2.next = k2);
                          l2.pending = k2;
                        }
                      }
                      f2.lanes |= c2;
                      k2 = f2.alternate;
                      null !== k2 && (k2.lanes |= c2);
                      bh(
                        f2.return,
                        c2,
                        b2
                      );
                      h2.lanes |= c2;
                      break;
                    }
                    k2 = k2.next;
                  }
                } else if (10 === f2.tag)
                  g2 = f2.type === b2.type ? null : f2.child;
                else if (18 === f2.tag) {
                  g2 = f2.return;
                  if (null === g2)
                    throw Error(p$2(341));
                  g2.lanes |= c2;
                  h2 = g2.alternate;
                  null !== h2 && (h2.lanes |= c2);
                  bh(g2, c2, b2);
                  g2 = f2.sibling;
                } else
                  g2 = f2.child;
                if (null !== g2)
                  g2.return = f2;
                else
                  for (g2 = f2; null !== g2; ) {
                    if (g2 === b2) {
                      g2 = null;
                      break;
                    }
                    f2 = g2.sibling;
                    if (null !== f2) {
                      f2.return = g2.return;
                      g2 = f2;
                      break;
                    }
                    g2 = g2.return;
                  }
                f2 = g2;
              }
          Xi(a, b2, e2.children, c2);
          b2 = b2.child;
        }
        return b2;
      case 9:
        return e2 = b2.type, d2 = b2.pendingProps.children, ch(b2, c2), e2 = eh(e2), d2 = d2(e2), b2.flags |= 1, Xi(a, b2, d2, c2), b2.child;
      case 14:
        return d2 = b2.type, e2 = Ci(d2, b2.pendingProps), e2 = Ci(d2.type, e2), $i(a, b2, d2, e2, c2);
      case 15:
        return bj(a, b2, b2.type, b2.pendingProps, c2);
      case 17:
        return d2 = b2.type, e2 = b2.pendingProps, e2 = b2.elementType === d2 ? e2 : Ci(d2, e2), ij(a, b2), b2.tag = 1, Zf(d2) ? (a = true, cg(b2)) : a = false, ch(b2, c2), Gi(b2, d2, e2), Ii(b2, d2, e2, c2), jj(null, b2, d2, true, a, c2);
      case 19:
        return xj(a, b2, c2);
      case 22:
        return dj(a, b2, c2);
    }
    throw Error(p$2(156, b2.tag));
  };
  function Fk(a, b2) {
    return ac(a, b2);
  }
  function $k(a, b2, c2, d2) {
    this.tag = a;
    this.key = c2;
    this.sibling = this.child = this.return = this.stateNode = this.type = this.elementType = null;
    this.index = 0;
    this.ref = null;
    this.pendingProps = b2;
    this.dependencies = this.memoizedState = this.updateQueue = this.memoizedProps = null;
    this.mode = d2;
    this.subtreeFlags = this.flags = 0;
    this.deletions = null;
    this.childLanes = this.lanes = 0;
    this.alternate = null;
  }
  function Bg(a, b2, c2, d2) {
    return new $k(a, b2, c2, d2);
  }
  function aj(a) {
    a = a.prototype;
    return !(!a || !a.isReactComponent);
  }
  function Zk(a) {
    if ("function" === typeof a)
      return aj(a) ? 1 : 0;
    if (void 0 !== a && null !== a) {
      a = a.$$typeof;
      if (a === Da)
        return 11;
      if (a === Ga)
        return 14;
    }
    return 2;
  }
  function Pg(a, b2) {
    var c2 = a.alternate;
    null === c2 ? (c2 = Bg(a.tag, b2, a.key, a.mode), c2.elementType = a.elementType, c2.type = a.type, c2.stateNode = a.stateNode, c2.alternate = a, a.alternate = c2) : (c2.pendingProps = b2, c2.type = a.type, c2.flags = 0, c2.subtreeFlags = 0, c2.deletions = null);
    c2.flags = a.flags & 14680064;
    c2.childLanes = a.childLanes;
    c2.lanes = a.lanes;
    c2.child = a.child;
    c2.memoizedProps = a.memoizedProps;
    c2.memoizedState = a.memoizedState;
    c2.updateQueue = a.updateQueue;
    b2 = a.dependencies;
    c2.dependencies = null === b2 ? null : { lanes: b2.lanes, firstContext: b2.firstContext };
    c2.sibling = a.sibling;
    c2.index = a.index;
    c2.ref = a.ref;
    return c2;
  }
  function Rg(a, b2, c2, d2, e2, f2) {
    var g2 = 2;
    d2 = a;
    if ("function" === typeof a)
      aj(a) && (g2 = 1);
    else if ("string" === typeof a)
      g2 = 5;
    else
      a:
        switch (a) {
          case ya:
            return Tg(c2.children, e2, f2, b2);
          case za:
            g2 = 8;
            e2 |= 8;
            break;
          case Aa:
            return a = Bg(12, c2, b2, e2 | 2), a.elementType = Aa, a.lanes = f2, a;
          case Ea:
            return a = Bg(13, c2, b2, e2), a.elementType = Ea, a.lanes = f2, a;
          case Fa:
            return a = Bg(19, c2, b2, e2), a.elementType = Fa, a.lanes = f2, a;
          case Ia:
            return pj(c2, e2, f2, b2);
          default:
            if ("object" === typeof a && null !== a)
              switch (a.$$typeof) {
                case Ba:
                  g2 = 10;
                  break a;
                case Ca:
                  g2 = 9;
                  break a;
                case Da:
                  g2 = 11;
                  break a;
                case Ga:
                  g2 = 14;
                  break a;
                case Ha:
                  g2 = 16;
                  d2 = null;
                  break a;
              }
            throw Error(p$2(130, null == a ? a : typeof a, ""));
        }
    b2 = Bg(g2, c2, b2, e2);
    b2.elementType = a;
    b2.type = d2;
    b2.lanes = f2;
    return b2;
  }
  function Tg(a, b2, c2, d2) {
    a = Bg(7, a, d2, b2);
    a.lanes = c2;
    return a;
  }
  function pj(a, b2, c2, d2) {
    a = Bg(22, a, d2, b2);
    a.elementType = Ia;
    a.lanes = c2;
    a.stateNode = { isHidden: false };
    return a;
  }
  function Qg(a, b2, c2) {
    a = Bg(6, a, null, b2);
    a.lanes = c2;
    return a;
  }
  function Sg(a, b2, c2) {
    b2 = Bg(4, null !== a.children ? a.children : [], a.key, b2);
    b2.lanes = c2;
    b2.stateNode = { containerInfo: a.containerInfo, pendingChildren: null, implementation: a.implementation };
    return b2;
  }
  function al(a, b2, c2, d2, e2) {
    this.tag = b2;
    this.containerInfo = a;
    this.finishedWork = this.pingCache = this.current = this.pendingChildren = null;
    this.timeoutHandle = -1;
    this.callbackNode = this.pendingContext = this.context = null;
    this.callbackPriority = 0;
    this.eventTimes = zc(0);
    this.expirationTimes = zc(-1);
    this.entangledLanes = this.finishedLanes = this.mutableReadLanes = this.expiredLanes = this.pingedLanes = this.suspendedLanes = this.pendingLanes = 0;
    this.entanglements = zc(0);
    this.identifierPrefix = d2;
    this.onRecoverableError = e2;
    this.mutableSourceEagerHydrationData = null;
  }
  function bl(a, b2, c2, d2, e2, f2, g2, h2, k2) {
    a = new al(a, b2, c2, h2, k2);
    1 === b2 ? (b2 = 1, true === f2 && (b2 |= 8)) : b2 = 0;
    f2 = Bg(3, null, null, b2);
    a.current = f2;
    f2.stateNode = a;
    f2.memoizedState = { element: d2, isDehydrated: c2, cache: null, transitions: null, pendingSuspenseBoundaries: null };
    kh(f2);
    return a;
  }
  function cl(a, b2, c2) {
    var d2 = 3 < arguments.length && void 0 !== arguments[3] ? arguments[3] : null;
    return { $$typeof: wa, key: null == d2 ? null : "" + d2, children: a, containerInfo: b2, implementation: c2 };
  }
  function dl(a) {
    if (!a)
      return Vf;
    a = a._reactInternals;
    a: {
      if (Vb(a) !== a || 1 !== a.tag)
        throw Error(p$2(170));
      var b2 = a;
      do {
        switch (b2.tag) {
          case 3:
            b2 = b2.stateNode.context;
            break a;
          case 1:
            if (Zf(b2.type)) {
              b2 = b2.stateNode.__reactInternalMemoizedMergedChildContext;
              break a;
            }
        }
        b2 = b2.return;
      } while (null !== b2);
      throw Error(p$2(171));
    }
    if (1 === a.tag) {
      var c2 = a.type;
      if (Zf(c2))
        return bg(a, c2, b2);
    }
    return b2;
  }
  function el(a, b2, c2, d2, e2, f2, g2, h2, k2) {
    a = bl(c2, d2, true, a, e2, f2, g2, h2, k2);
    a.context = dl(null);
    c2 = a.current;
    d2 = R$1();
    e2 = yi(c2);
    f2 = mh(d2, e2);
    f2.callback = void 0 !== b2 && null !== b2 ? b2 : null;
    nh(c2, f2, e2);
    a.current.lanes = e2;
    Ac(a, e2, d2);
    Dk(a, d2);
    return a;
  }
  function fl(a, b2, c2, d2) {
    var e2 = b2.current, f2 = R$1(), g2 = yi(e2);
    c2 = dl(c2);
    null === b2.context ? b2.context = c2 : b2.pendingContext = c2;
    b2 = mh(f2, g2);
    b2.payload = { element: a };
    d2 = void 0 === d2 ? null : d2;
    null !== d2 && (b2.callback = d2);
    a = nh(e2, b2, g2);
    null !== a && (gi(a, e2, g2, f2), oh(a, e2, g2));
    return g2;
  }
  function gl(a) {
    a = a.current;
    if (!a.child)
      return null;
    switch (a.child.tag) {
      case 5:
        return a.child.stateNode;
      default:
        return a.child.stateNode;
    }
  }
  function hl(a, b2) {
    a = a.memoizedState;
    if (null !== a && null !== a.dehydrated) {
      var c2 = a.retryLane;
      a.retryLane = 0 !== c2 && c2 < b2 ? c2 : b2;
    }
  }
  function il(a, b2) {
    hl(a, b2);
    (a = a.alternate) && hl(a, b2);
  }
  function jl() {
    return null;
  }
  var kl = "function" === typeof reportError ? reportError : function(a) {
    console.error(a);
  };
  function ll(a) {
    this._internalRoot = a;
  }
  ml.prototype.render = ll.prototype.render = function(a) {
    var b2 = this._internalRoot;
    if (null === b2)
      throw Error(p$2(409));
    fl(a, b2, null, null);
  };
  ml.prototype.unmount = ll.prototype.unmount = function() {
    var a = this._internalRoot;
    if (null !== a) {
      this._internalRoot = null;
      var b2 = a.containerInfo;
      Rk(function() {
        fl(null, a, null, null);
      });
      b2[uf] = null;
    }
  };
  function ml(a) {
    this._internalRoot = a;
  }
  ml.prototype.unstable_scheduleHydration = function(a) {
    if (a) {
      var b2 = Hc();
      a = { blockedOn: null, target: a, priority: b2 };
      for (var c2 = 0; c2 < Qc.length && 0 !== b2 && b2 < Qc[c2].priority; c2++)
        ;
      Qc.splice(c2, 0, a);
      0 === c2 && Vc(a);
    }
  };
  function nl(a) {
    return !(!a || 1 !== a.nodeType && 9 !== a.nodeType && 11 !== a.nodeType);
  }
  function ol(a) {
    return !(!a || 1 !== a.nodeType && 9 !== a.nodeType && 11 !== a.nodeType && (8 !== a.nodeType || " react-mount-point-unstable " !== a.nodeValue));
  }
  function pl() {
  }
  function ql(a, b2, c2, d2, e2) {
    if (e2) {
      if ("function" === typeof d2) {
        var f2 = d2;
        d2 = function() {
          var a2 = gl(g2);
          f2.call(a2);
        };
      }
      var g2 = el(b2, d2, a, 0, null, false, false, "", pl);
      a._reactRootContainer = g2;
      a[uf] = g2.current;
      sf(8 === a.nodeType ? a.parentNode : a);
      Rk();
      return g2;
    }
    for (; e2 = a.lastChild; )
      a.removeChild(e2);
    if ("function" === typeof d2) {
      var h2 = d2;
      d2 = function() {
        var a2 = gl(k2);
        h2.call(a2);
      };
    }
    var k2 = bl(a, 0, false, null, null, false, false, "", pl);
    a._reactRootContainer = k2;
    a[uf] = k2.current;
    sf(8 === a.nodeType ? a.parentNode : a);
    Rk(function() {
      fl(b2, k2, c2, d2);
    });
    return k2;
  }
  function rl(a, b2, c2, d2, e2) {
    var f2 = c2._reactRootContainer;
    if (f2) {
      var g2 = f2;
      if ("function" === typeof e2) {
        var h2 = e2;
        e2 = function() {
          var a2 = gl(g2);
          h2.call(a2);
        };
      }
      fl(b2, g2, a, e2);
    } else
      g2 = ql(c2, b2, a, e2, d2);
    return gl(g2);
  }
  Ec = function(a) {
    switch (a.tag) {
      case 3:
        var b2 = a.stateNode;
        if (b2.current.memoizedState.isDehydrated) {
          var c2 = tc(b2.pendingLanes);
          0 !== c2 && (Cc(b2, c2 | 1), Dk(b2, B$1()), 0 === (K$1 & 6) && (Gj = B$1() + 500, jg()));
        }
        break;
      case 13:
        Rk(function() {
          var b3 = ih(a, 1);
          if (null !== b3) {
            var c3 = R$1();
            gi(b3, a, 1, c3);
          }
        }), il(a, 1);
    }
  };
  Fc = function(a) {
    if (13 === a.tag) {
      var b2 = ih(a, 134217728);
      if (null !== b2) {
        var c2 = R$1();
        gi(b2, a, 134217728, c2);
      }
      il(a, 134217728);
    }
  };
  Gc = function(a) {
    if (13 === a.tag) {
      var b2 = yi(a), c2 = ih(a, b2);
      if (null !== c2) {
        var d2 = R$1();
        gi(c2, a, b2, d2);
      }
      il(a, b2);
    }
  };
  Hc = function() {
    return C$1;
  };
  Ic = function(a, b2) {
    var c2 = C$1;
    try {
      return C$1 = a, b2();
    } finally {
      C$1 = c2;
    }
  };
  yb = function(a, b2, c2) {
    switch (b2) {
      case "input":
        bb(a, c2);
        b2 = c2.name;
        if ("radio" === c2.type && null != b2) {
          for (c2 = a; c2.parentNode; )
            c2 = c2.parentNode;
          c2 = c2.querySelectorAll("input[name=" + JSON.stringify("" + b2) + '][type="radio"]');
          for (b2 = 0; b2 < c2.length; b2++) {
            var d2 = c2[b2];
            if (d2 !== a && d2.form === a.form) {
              var e2 = Db(d2);
              if (!e2)
                throw Error(p$2(90));
              Wa(d2);
              bb(d2, e2);
            }
          }
        }
        break;
      case "textarea":
        ib(a, c2);
        break;
      case "select":
        b2 = c2.value, null != b2 && fb(a, !!c2.multiple, b2, false);
    }
  };
  Gb = Qk;
  Hb = Rk;
  var sl = { usingClientEntryPoint: false, Events: [Cb, ue$1, Db, Eb, Fb, Qk] }, tl = { findFiberByHostInstance: Wc, bundleType: 0, version: "18.3.1", rendererPackageName: "react-dom" };
  var ul = { bundleType: tl.bundleType, version: tl.version, rendererPackageName: tl.rendererPackageName, rendererConfig: tl.rendererConfig, overrideHookState: null, overrideHookStateDeletePath: null, overrideHookStateRenamePath: null, overrideProps: null, overridePropsDeletePath: null, overridePropsRenamePath: null, setErrorHandler: null, setSuspenseHandler: null, scheduleUpdate: null, currentDispatcherRef: ua.ReactCurrentDispatcher, findHostInstanceByFiber: function(a) {
    a = Zb(a);
    return null === a ? null : a.stateNode;
  }, findFiberByHostInstance: tl.findFiberByHostInstance || jl, findHostInstancesForRefresh: null, scheduleRefresh: null, scheduleRoot: null, setRefreshHandler: null, getCurrentFiber: null, reconcilerVersion: "18.3.1-next-f1338f8080-20240426" };
  if ("undefined" !== typeof __REACT_DEVTOOLS_GLOBAL_HOOK__) {
    var vl = __REACT_DEVTOOLS_GLOBAL_HOOK__;
    if (!vl.isDisabled && vl.supportsFiber)
      try {
        kc = vl.inject(ul), lc = vl;
      } catch (a) {
      }
  }
  reactDom_production_min.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED = sl;
  reactDom_production_min.createPortal = function(a, b2) {
    var c2 = 2 < arguments.length && void 0 !== arguments[2] ? arguments[2] : null;
    if (!nl(b2))
      throw Error(p$2(200));
    return cl(a, b2, null, c2);
  };
  reactDom_production_min.createRoot = function(a, b2) {
    if (!nl(a))
      throw Error(p$2(299));
    var c2 = false, d2 = "", e2 = kl;
    null !== b2 && void 0 !== b2 && (true === b2.unstable_strictMode && (c2 = true), void 0 !== b2.identifierPrefix && (d2 = b2.identifierPrefix), void 0 !== b2.onRecoverableError && (e2 = b2.onRecoverableError));
    b2 = bl(a, 1, false, null, null, c2, false, d2, e2);
    a[uf] = b2.current;
    sf(8 === a.nodeType ? a.parentNode : a);
    return new ll(b2);
  };
  reactDom_production_min.findDOMNode = function(a) {
    if (null == a)
      return null;
    if (1 === a.nodeType)
      return a;
    var b2 = a._reactInternals;
    if (void 0 === b2) {
      if ("function" === typeof a.render)
        throw Error(p$2(188));
      a = Object.keys(a).join(",");
      throw Error(p$2(268, a));
    }
    a = Zb(b2);
    a = null === a ? null : a.stateNode;
    return a;
  };
  reactDom_production_min.flushSync = function(a) {
    return Rk(a);
  };
  reactDom_production_min.hydrate = function(a, b2, c2) {
    if (!ol(b2))
      throw Error(p$2(200));
    return rl(null, a, b2, true, c2);
  };
  reactDom_production_min.hydrateRoot = function(a, b2, c2) {
    if (!nl(a))
      throw Error(p$2(405));
    var d2 = null != c2 && c2.hydratedSources || null, e2 = false, f2 = "", g2 = kl;
    null !== c2 && void 0 !== c2 && (true === c2.unstable_strictMode && (e2 = true), void 0 !== c2.identifierPrefix && (f2 = c2.identifierPrefix), void 0 !== c2.onRecoverableError && (g2 = c2.onRecoverableError));
    b2 = el(b2, null, a, 1, null != c2 ? c2 : null, e2, false, f2, g2);
    a[uf] = b2.current;
    sf(a);
    if (d2)
      for (a = 0; a < d2.length; a++)
        c2 = d2[a], e2 = c2._getVersion, e2 = e2(c2._source), null == b2.mutableSourceEagerHydrationData ? b2.mutableSourceEagerHydrationData = [c2, e2] : b2.mutableSourceEagerHydrationData.push(
          c2,
          e2
        );
    return new ml(b2);
  };
  reactDom_production_min.render = function(a, b2, c2) {
    if (!ol(b2))
      throw Error(p$2(200));
    return rl(null, a, b2, false, c2);
  };
  reactDom_production_min.unmountComponentAtNode = function(a) {
    if (!ol(a))
      throw Error(p$2(40));
    return a._reactRootContainer ? (Rk(function() {
      rl(null, null, a, false, function() {
        a._reactRootContainer = null;
        a[uf] = null;
      });
    }), true) : false;
  };
  reactDom_production_min.unstable_batchedUpdates = Qk;
  reactDom_production_min.unstable_renderSubtreeIntoContainer = function(a, b2, c2, d2) {
    if (!ol(c2))
      throw Error(p$2(200));
    if (null == a || void 0 === a._reactInternals)
      throw Error(p$2(38));
    return rl(a, b2, c2, false, d2);
  };
  reactDom_production_min.version = "18.3.1-next-f1338f8080-20240426";
  function checkDCE() {
    if (typeof __REACT_DEVTOOLS_GLOBAL_HOOK__ === "undefined" || typeof __REACT_DEVTOOLS_GLOBAL_HOOK__.checkDCE !== "function") {
      return;
    }
    try {
      __REACT_DEVTOOLS_GLOBAL_HOOK__.checkDCE(checkDCE);
    } catch (err) {
      console.error(err);
    }
  }
  {
    checkDCE();
    reactDom.exports = reactDom_production_min;
  }
  var reactDomExports = reactDom.exports;
  const ReactDOM = /* @__PURE__ */ getDefaultExportFromCjs(reactDomExports);
  var jsxRuntime = { exports: {} };
  var reactJsxRuntime_production_min = {};
  /**
   * @license React
   * react-jsx-runtime.production.min.js
   *
   * Copyright (c) Facebook, Inc. and its affiliates.
   *
   * This source code is licensed under the MIT license found in the
   * LICENSE file in the root directory of this source tree.
   */
  var f$2 = reactExports, k$2 = Symbol.for("react.element"), l$1 = Symbol.for("react.fragment"), m$2 = Object.prototype.hasOwnProperty, n$1 = f$2.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, p$1 = { key: true, ref: true, __self: true, __source: true };
  function q$2(c2, a, g2) {
    var b2, d2 = {}, e2 = null, h2 = null;
    void 0 !== g2 && (e2 = "" + g2);
    void 0 !== a.key && (e2 = "" + a.key);
    void 0 !== a.ref && (h2 = a.ref);
    for (b2 in a)
      m$2.call(a, b2) && !p$1.hasOwnProperty(b2) && (d2[b2] = a[b2]);
    if (c2 && c2.defaultProps)
      for (b2 in a = c2.defaultProps, a)
        void 0 === d2[b2] && (d2[b2] = a[b2]);
    return { $$typeof: k$2, type: c2, key: e2, ref: h2, props: d2, _owner: n$1.current };
  }
  reactJsxRuntime_production_min.Fragment = l$1;
  reactJsxRuntime_production_min.jsx = q$2;
  reactJsxRuntime_production_min.jsxs = q$2;
  {
    jsxRuntime.exports = reactJsxRuntime_production_min;
  }
  var jsxRuntimeExports = jsxRuntime.exports;
  function sheetForTag(tag) {
    if (tag.sheet) {
      return tag.sheet;
    }
    for (var i = 0; i < document.styleSheets.length; i++) {
      if (document.styleSheets[i].ownerNode === tag) {
        return document.styleSheets[i];
      }
    }
  }
  function createStyleElement(options) {
    var tag = document.createElement("style");
    tag.setAttribute("data-emotion", options.key);
    if (options.nonce !== void 0) {
      tag.setAttribute("nonce", options.nonce);
    }
    tag.appendChild(document.createTextNode(""));
    tag.setAttribute("data-s", "");
    return tag;
  }
  var StyleSheet = /* @__PURE__ */ function() {
    function StyleSheet2(options) {
      var _this = this;
      this._insertTag = function(tag) {
        var before;
        if (_this.tags.length === 0) {
          if (_this.insertionPoint) {
            before = _this.insertionPoint.nextSibling;
          } else if (_this.prepend) {
            before = _this.container.firstChild;
          } else {
            before = _this.before;
          }
        } else {
          before = _this.tags[_this.tags.length - 1].nextSibling;
        }
        _this.container.insertBefore(tag, before);
        _this.tags.push(tag);
      };
      this.isSpeedy = options.speedy === void 0 ? true : options.speedy;
      this.tags = [];
      this.ctr = 0;
      this.nonce = options.nonce;
      this.key = options.key;
      this.container = options.container;
      this.prepend = options.prepend;
      this.insertionPoint = options.insertionPoint;
      this.before = null;
    }
    var _proto = StyleSheet2.prototype;
    _proto.hydrate = function hydrate(nodes) {
      nodes.forEach(this._insertTag);
    };
    _proto.insert = function insert(rule) {
      if (this.ctr % (this.isSpeedy ? 65e3 : 1) === 0) {
        this._insertTag(createStyleElement(this));
      }
      var tag = this.tags[this.tags.length - 1];
      if (this.isSpeedy) {
        var sheet = sheetForTag(tag);
        try {
          sheet.insertRule(rule, sheet.cssRules.length);
        } catch (e2) {
        }
      } else {
        tag.appendChild(document.createTextNode(rule));
      }
      this.ctr++;
    };
    _proto.flush = function flush() {
      this.tags.forEach(function(tag) {
        return tag.parentNode && tag.parentNode.removeChild(tag);
      });
      this.tags = [];
      this.ctr = 0;
    };
    return StyleSheet2;
  }();
  var MS$1 = "-ms-";
  var MOZ$1 = "-moz-";
  var WEBKIT$1 = "-webkit-";
  var COMMENT$1 = "comm";
  var RULESET$1 = "rule";
  var DECLARATION$1 = "decl";
  var IMPORT$1 = "@import";
  var KEYFRAMES$1 = "@keyframes";
  var LAYER$1 = "@layer";
  var abs$1 = Math.abs;
  var from$1 = String.fromCharCode;
  var assign$1 = Object.assign;
  function hash$2(value, length2) {
    return charat$1(value, 0) ^ 45 ? (((length2 << 2 ^ charat$1(value, 0)) << 2 ^ charat$1(value, 1)) << 2 ^ charat$1(value, 2)) << 2 ^ charat$1(value, 3) : 0;
  }
  function trim$1(value) {
    return value.trim();
  }
  function match$1(value, pattern) {
    return (value = pattern.exec(value)) ? value[0] : value;
  }
  function replace$1(value, pattern, replacement) {
    return value.replace(pattern, replacement);
  }
  function indexof$1(value, search) {
    return value.indexOf(search);
  }
  function charat$1(value, index) {
    return value.charCodeAt(index) | 0;
  }
  function substr$1(value, begin, end) {
    return value.slice(begin, end);
  }
  function strlen$1(value) {
    return value.length;
  }
  function sizeof$1(value) {
    return value.length;
  }
  function append$1(value, array) {
    return array.push(value), value;
  }
  function combine$1(array, callback) {
    return array.map(callback).join("");
  }
  var line$1 = 1;
  var column$1 = 1;
  var length$1 = 0;
  var position$2 = 0;
  var character$1 = 0;
  var characters$1 = "";
  function node$1(value, root, parent, type, props, children, length2) {
    return { value, root, parent, type, props, children, line: line$1, column: column$1, length: length2, return: "" };
  }
  function copy$1(root, props) {
    return assign$1(node$1("", null, null, "", null, null, 0), root, { length: -root.length }, props);
  }
  function char$1() {
    return character$1;
  }
  function prev$1() {
    character$1 = position$2 > 0 ? charat$1(characters$1, --position$2) : 0;
    if (column$1--, character$1 === 10)
      column$1 = 1, line$1--;
    return character$1;
  }
  function next$1() {
    character$1 = position$2 < length$1 ? charat$1(characters$1, position$2++) : 0;
    if (column$1++, character$1 === 10)
      column$1 = 1, line$1++;
    return character$1;
  }
  function peek$1() {
    return charat$1(characters$1, position$2);
  }
  function caret$1() {
    return position$2;
  }
  function slice$1(begin, end) {
    return substr$1(characters$1, begin, end);
  }
  function token$1(type) {
    switch (type) {
      case 0:
      case 9:
      case 10:
      case 13:
      case 32:
        return 5;
      case 33:
      case 43:
      case 44:
      case 47:
      case 62:
      case 64:
      case 126:
      case 59:
      case 123:
      case 125:
        return 4;
      case 58:
        return 3;
      case 34:
      case 39:
      case 40:
      case 91:
        return 2;
      case 41:
      case 93:
        return 1;
    }
    return 0;
  }
  function alloc$1(value) {
    return line$1 = column$1 = 1, length$1 = strlen$1(characters$1 = value), position$2 = 0, [];
  }
  function dealloc$1(value) {
    return characters$1 = "", value;
  }
  function delimit$1(type) {
    return trim$1(slice$1(position$2 - 1, delimiter$1(type === 91 ? type + 2 : type === 40 ? type + 1 : type)));
  }
  function whitespace$1(type) {
    while (character$1 = peek$1())
      if (character$1 < 33)
        next$1();
      else
        break;
    return token$1(type) > 2 || token$1(character$1) > 3 ? "" : " ";
  }
  function escaping$1(index, count) {
    while (--count && next$1())
      if (character$1 < 48 || character$1 > 102 || character$1 > 57 && character$1 < 65 || character$1 > 70 && character$1 < 97)
        break;
    return slice$1(index, caret$1() + (count < 6 && peek$1() == 32 && next$1() == 32));
  }
  function delimiter$1(type) {
    while (next$1())
      switch (character$1) {
        case type:
          return position$2;
        case 34:
        case 39:
          if (type !== 34 && type !== 39)
            delimiter$1(character$1);
          break;
        case 40:
          if (type === 41)
            delimiter$1(type);
          break;
        case 92:
          next$1();
          break;
      }
    return position$2;
  }
  function commenter$1(type, index) {
    while (next$1())
      if (type + character$1 === 47 + 10)
        break;
      else if (type + character$1 === 42 + 42 && peek$1() === 47)
        break;
    return "/*" + slice$1(index, position$2 - 1) + "*" + from$1(type === 47 ? type : next$1());
  }
  function identifier$1(index) {
    while (!token$1(peek$1()))
      next$1();
    return slice$1(index, position$2);
  }
  function compile$1(value) {
    return dealloc$1(parse$1("", null, null, null, [""], value = alloc$1(value), 0, [0], value));
  }
  function parse$1(value, root, parent, rule, rules, rulesets, pseudo, points, declarations) {
    var index = 0;
    var offset = 0;
    var length2 = pseudo;
    var atrule = 0;
    var property = 0;
    var previous = 0;
    var variable = 1;
    var scanning = 1;
    var ampersand = 1;
    var character2 = 0;
    var type = "";
    var props = rules;
    var children = rulesets;
    var reference = rule;
    var characters2 = type;
    while (scanning)
      switch (previous = character2, character2 = next$1()) {
        case 40:
          if (previous != 108 && charat$1(characters2, length2 - 1) == 58) {
            if (indexof$1(characters2 += replace$1(delimit$1(character2), "&", "&\f"), "&\f") != -1)
              ampersand = -1;
            break;
          }
        case 34:
        case 39:
        case 91:
          characters2 += delimit$1(character2);
          break;
        case 9:
        case 10:
        case 13:
        case 32:
          characters2 += whitespace$1(previous);
          break;
        case 92:
          characters2 += escaping$1(caret$1() - 1, 7);
          continue;
        case 47:
          switch (peek$1()) {
            case 42:
            case 47:
              append$1(comment$1(commenter$1(next$1(), caret$1()), root, parent), declarations);
              break;
            default:
              characters2 += "/";
          }
          break;
        case 123 * variable:
          points[index++] = strlen$1(characters2) * ampersand;
        case 125 * variable:
        case 59:
        case 0:
          switch (character2) {
            case 0:
            case 125:
              scanning = 0;
            case 59 + offset:
              if (ampersand == -1)
                characters2 = replace$1(characters2, /\f/g, "");
              if (property > 0 && strlen$1(characters2) - length2)
                append$1(property > 32 ? declaration$1(characters2 + ";", rule, parent, length2 - 1) : declaration$1(replace$1(characters2, " ", "") + ";", rule, parent, length2 - 2), declarations);
              break;
            case 59:
              characters2 += ";";
            default:
              append$1(reference = ruleset$1(characters2, root, parent, index, offset, rules, points, type, props = [], children = [], length2), rulesets);
              if (character2 === 123)
                if (offset === 0)
                  parse$1(characters2, root, reference, reference, props, rulesets, length2, points, children);
                else
                  switch (atrule === 99 && charat$1(characters2, 3) === 110 ? 100 : atrule) {
                    case 100:
                    case 108:
                    case 109:
                    case 115:
                      parse$1(value, reference, reference, rule && append$1(ruleset$1(value, reference, reference, 0, 0, rules, points, type, rules, props = [], length2), children), rules, children, length2, points, rule ? props : children);
                      break;
                    default:
                      parse$1(characters2, reference, reference, reference, [""], children, 0, points, children);
                  }
          }
          index = offset = property = 0, variable = ampersand = 1, type = characters2 = "", length2 = pseudo;
          break;
        case 58:
          length2 = 1 + strlen$1(characters2), property = previous;
        default:
          if (variable < 1) {
            if (character2 == 123)
              --variable;
            else if (character2 == 125 && variable++ == 0 && prev$1() == 125)
              continue;
          }
          switch (characters2 += from$1(character2), character2 * variable) {
            case 38:
              ampersand = offset > 0 ? 1 : (characters2 += "\f", -1);
              break;
            case 44:
              points[index++] = (strlen$1(characters2) - 1) * ampersand, ampersand = 1;
              break;
            case 64:
              if (peek$1() === 45)
                characters2 += delimit$1(next$1());
              atrule = peek$1(), offset = length2 = strlen$1(type = characters2 += identifier$1(caret$1())), character2++;
              break;
            case 45:
              if (previous === 45 && strlen$1(characters2) == 2)
                variable = 0;
          }
      }
    return rulesets;
  }
  function ruleset$1(value, root, parent, index, offset, rules, points, type, props, children, length2) {
    var post = offset - 1;
    var rule = offset === 0 ? rules : [""];
    var size2 = sizeof$1(rule);
    for (var i = 0, j2 = 0, k2 = 0; i < index; ++i)
      for (var x2 = 0, y2 = substr$1(value, post + 1, post = abs$1(j2 = points[i])), z2 = value; x2 < size2; ++x2)
        if (z2 = trim$1(j2 > 0 ? rule[x2] + " " + y2 : replace$1(y2, /&\f/g, rule[x2])))
          props[k2++] = z2;
    return node$1(value, root, parent, offset === 0 ? RULESET$1 : type, props, children, length2);
  }
  function comment$1(value, root, parent) {
    return node$1(value, root, parent, COMMENT$1, from$1(char$1()), substr$1(value, 2, -2), 0);
  }
  function declaration$1(value, root, parent, length2) {
    return node$1(value, root, parent, DECLARATION$1, substr$1(value, 0, length2), substr$1(value, length2 + 1, -1), length2);
  }
  function serialize$1(children, callback) {
    var output = "";
    var length2 = sizeof$1(children);
    for (var i = 0; i < length2; i++)
      output += callback(children[i], i, children, callback) || "";
    return output;
  }
  function stringify$1(element, index, children, callback) {
    switch (element.type) {
      case LAYER$1:
        if (element.children.length)
          break;
      case IMPORT$1:
      case DECLARATION$1:
        return element.return = element.return || element.value;
      case COMMENT$1:
        return "";
      case KEYFRAMES$1:
        return element.return = element.value + "{" + serialize$1(element.children, callback) + "}";
      case RULESET$1:
        element.value = element.props.join(",");
    }
    return strlen$1(children = serialize$1(element.children, callback)) ? element.return = element.value + "{" + children + "}" : "";
  }
  function middleware$1(collection) {
    var length2 = sizeof$1(collection);
    return function(element, index, children, callback) {
      var output = "";
      for (var i = 0; i < length2; i++)
        output += collection[i](element, index, children, callback) || "";
      return output;
    };
  }
  function rulesheet$1(callback) {
    return function(element) {
      if (!element.root) {
        if (element = element.return)
          callback(element);
      }
    };
  }
  var weakMemoize = function weakMemoize2(func) {
    var cache = /* @__PURE__ */ new WeakMap();
    return function(arg) {
      if (cache.has(arg)) {
        return cache.get(arg);
      }
      var ret = func(arg);
      cache.set(arg, ret);
      return ret;
    };
  };
  function memoize$2(fn) {
    var cache = /* @__PURE__ */ Object.create(null);
    return function(arg) {
      if (cache[arg] === void 0)
        cache[arg] = fn(arg);
      return cache[arg];
    };
  }
  var identifierWithPointTracking = function identifierWithPointTracking2(begin, points, index) {
    var previous = 0;
    var character2 = 0;
    while (true) {
      previous = character2;
      character2 = peek$1();
      if (previous === 38 && character2 === 12) {
        points[index] = 1;
      }
      if (token$1(character2)) {
        break;
      }
      next$1();
    }
    return slice$1(begin, position$2);
  };
  var toRules = function toRules2(parsed, points) {
    var index = -1;
    var character2 = 44;
    do {
      switch (token$1(character2)) {
        case 0:
          if (character2 === 38 && peek$1() === 12) {
            points[index] = 1;
          }
          parsed[index] += identifierWithPointTracking(position$2 - 1, points, index);
          break;
        case 2:
          parsed[index] += delimit$1(character2);
          break;
        case 4:
          if (character2 === 44) {
            parsed[++index] = peek$1() === 58 ? "&\f" : "";
            points[index] = parsed[index].length;
            break;
          }
        default:
          parsed[index] += from$1(character2);
      }
    } while (character2 = next$1());
    return parsed;
  };
  var getRules = function getRules2(value, points) {
    return dealloc$1(toRules(alloc$1(value), points));
  };
  var fixedElements = /* @__PURE__ */ new WeakMap();
  var compat = function compat2(element) {
    if (element.type !== "rule" || !element.parent || // positive .length indicates that this rule contains pseudo
    // negative .length indicates that this rule has been already prefixed
    element.length < 1) {
      return;
    }
    var value = element.value, parent = element.parent;
    var isImplicitRule = element.column === parent.column && element.line === parent.line;
    while (parent.type !== "rule") {
      parent = parent.parent;
      if (!parent)
        return;
    }
    if (element.props.length === 1 && value.charCodeAt(0) !== 58 && !fixedElements.get(parent)) {
      return;
    }
    if (isImplicitRule) {
      return;
    }
    fixedElements.set(element, true);
    var points = [];
    var rules = getRules(value, points);
    var parentRules = parent.props;
    for (var i = 0, k2 = 0; i < rules.length; i++) {
      for (var j2 = 0; j2 < parentRules.length; j2++, k2++) {
        element.props[k2] = points[i] ? rules[i].replace(/&\f/g, parentRules[j2]) : parentRules[j2] + " " + rules[i];
      }
    }
  };
  var removeLabel = function removeLabel2(element) {
    if (element.type === "decl") {
      var value = element.value;
      if (
        // charcode for l
        value.charCodeAt(0) === 108 && // charcode for b
        value.charCodeAt(2) === 98
      ) {
        element["return"] = "";
        element.value = "";
      }
    }
  };
  function prefix$1(value, length2) {
    switch (hash$2(value, length2)) {
      case 5103:
        return WEBKIT$1 + "print-" + value + value;
      case 5737:
      case 4201:
      case 3177:
      case 3433:
      case 1641:
      case 4457:
      case 2921:
      case 5572:
      case 6356:
      case 5844:
      case 3191:
      case 6645:
      case 3005:
      case 6391:
      case 5879:
      case 5623:
      case 6135:
      case 4599:
      case 4855:
      case 4215:
      case 6389:
      case 5109:
      case 5365:
      case 5621:
      case 3829:
        return WEBKIT$1 + value + value;
      case 5349:
      case 4246:
      case 4810:
      case 6968:
      case 2756:
        return WEBKIT$1 + value + MOZ$1 + value + MS$1 + value + value;
      case 6828:
      case 4268:
        return WEBKIT$1 + value + MS$1 + value + value;
      case 6165:
        return WEBKIT$1 + value + MS$1 + "flex-" + value + value;
      case 5187:
        return WEBKIT$1 + value + replace$1(value, /(\w+).+(:[^]+)/, WEBKIT$1 + "box-$1$2" + MS$1 + "flex-$1$2") + value;
      case 5443:
        return WEBKIT$1 + value + MS$1 + "flex-item-" + replace$1(value, /flex-|-self/, "") + value;
      case 4675:
        return WEBKIT$1 + value + MS$1 + "flex-line-pack" + replace$1(value, /align-content|flex-|-self/, "") + value;
      case 5548:
        return WEBKIT$1 + value + MS$1 + replace$1(value, "shrink", "negative") + value;
      case 5292:
        return WEBKIT$1 + value + MS$1 + replace$1(value, "basis", "preferred-size") + value;
      case 6060:
        return WEBKIT$1 + "box-" + replace$1(value, "-grow", "") + WEBKIT$1 + value + MS$1 + replace$1(value, "grow", "positive") + value;
      case 4554:
        return WEBKIT$1 + replace$1(value, /([^-])(transform)/g, "$1" + WEBKIT$1 + "$2") + value;
      case 6187:
        return replace$1(replace$1(replace$1(value, /(zoom-|grab)/, WEBKIT$1 + "$1"), /(image-set)/, WEBKIT$1 + "$1"), value, "") + value;
      case 5495:
      case 3959:
        return replace$1(value, /(image-set\([^]*)/, WEBKIT$1 + "$1$`$1");
      case 4968:
        return replace$1(replace$1(value, /(.+:)(flex-)?(.*)/, WEBKIT$1 + "box-pack:$3" + MS$1 + "flex-pack:$3"), /s.+-b[^;]+/, "justify") + WEBKIT$1 + value + value;
      case 4095:
      case 3583:
      case 4068:
      case 2532:
        return replace$1(value, /(.+)-inline(.+)/, WEBKIT$1 + "$1$2") + value;
      case 8116:
      case 7059:
      case 5753:
      case 5535:
      case 5445:
      case 5701:
      case 4933:
      case 4677:
      case 5533:
      case 5789:
      case 5021:
      case 4765:
        if (strlen$1(value) - 1 - length2 > 6)
          switch (charat$1(value, length2 + 1)) {
            case 109:
              if (charat$1(value, length2 + 4) !== 45)
                break;
            case 102:
              return replace$1(value, /(.+:)(.+)-([^]+)/, "$1" + WEBKIT$1 + "$2-$3$1" + MOZ$1 + (charat$1(value, length2 + 3) == 108 ? "$3" : "$2-$3")) + value;
            case 115:
              return ~indexof$1(value, "stretch") ? prefix$1(replace$1(value, "stretch", "fill-available"), length2) + value : value;
          }
        break;
      case 4949:
        if (charat$1(value, length2 + 1) !== 115)
          break;
      case 6444:
        switch (charat$1(value, strlen$1(value) - 3 - (~indexof$1(value, "!important") && 10))) {
          case 107:
            return replace$1(value, ":", ":" + WEBKIT$1) + value;
          case 101:
            return replace$1(value, /(.+:)([^;!]+)(;|!.+)?/, "$1" + WEBKIT$1 + (charat$1(value, 14) === 45 ? "inline-" : "") + "box$3$1" + WEBKIT$1 + "$2$3$1" + MS$1 + "$2box$3") + value;
        }
        break;
      case 5936:
        switch (charat$1(value, length2 + 11)) {
          case 114:
            return WEBKIT$1 + value + MS$1 + replace$1(value, /[svh]\w+-[tblr]{2}/, "tb") + value;
          case 108:
            return WEBKIT$1 + value + MS$1 + replace$1(value, /[svh]\w+-[tblr]{2}/, "tb-rl") + value;
          case 45:
            return WEBKIT$1 + value + MS$1 + replace$1(value, /[svh]\w+-[tblr]{2}/, "lr") + value;
        }
        return WEBKIT$1 + value + MS$1 + value + value;
    }
    return value;
  }
  var prefixer$1 = function prefixer2(element, index, children, callback) {
    if (element.length > -1) {
      if (!element["return"])
        switch (element.type) {
          case DECLARATION$1:
            element["return"] = prefix$1(element.value, element.length);
            break;
          case KEYFRAMES$1:
            return serialize$1([copy$1(element, {
              value: replace$1(element.value, "@", "@" + WEBKIT$1)
            })], callback);
          case RULESET$1:
            if (element.length)
              return combine$1(element.props, function(value) {
                switch (match$1(value, /(::plac\w+|:read-\w+)/)) {
                  case ":read-only":
                  case ":read-write":
                    return serialize$1([copy$1(element, {
                      props: [replace$1(value, /:(read-\w+)/, ":" + MOZ$1 + "$1")]
                    })], callback);
                  case "::placeholder":
                    return serialize$1([copy$1(element, {
                      props: [replace$1(value, /:(plac\w+)/, ":" + WEBKIT$1 + "input-$1")]
                    }), copy$1(element, {
                      props: [replace$1(value, /:(plac\w+)/, ":" + MOZ$1 + "$1")]
                    }), copy$1(element, {
                      props: [replace$1(value, /:(plac\w+)/, MS$1 + "input-$1")]
                    })], callback);
                }
                return "";
              });
        }
    }
  };
  var defaultStylisPlugins = [prefixer$1];
  var createCache = function createCache2(options) {
    var key = options.key;
    if (key === "css") {
      var ssrStyles = document.querySelectorAll("style[data-emotion]:not([data-s])");
      Array.prototype.forEach.call(ssrStyles, function(node2) {
        var dataEmotionAttribute = node2.getAttribute("data-emotion");
        if (dataEmotionAttribute.indexOf(" ") === -1) {
          return;
        }
        document.head.appendChild(node2);
        node2.setAttribute("data-s", "");
      });
    }
    var stylisPlugins = options.stylisPlugins || defaultStylisPlugins;
    var inserted = {};
    var container2;
    var nodesToHydrate = [];
    {
      container2 = options.container || document.head;
      Array.prototype.forEach.call(
        // this means we will ignore elements which don't have a space in them which
        // means that the style elements we're looking at are only Emotion 11 server-rendered style elements
        document.querySelectorAll('style[data-emotion^="' + key + ' "]'),
        function(node2) {
          var attrib = node2.getAttribute("data-emotion").split(" ");
          for (var i = 1; i < attrib.length; i++) {
            inserted[attrib[i]] = true;
          }
          nodesToHydrate.push(node2);
        }
      );
    }
    var _insert;
    var omnipresentPlugins = [compat, removeLabel];
    {
      var currentSheet;
      var finalizingPlugins = [stringify$1, rulesheet$1(function(rule) {
        currentSheet.insert(rule);
      })];
      var serializer = middleware$1(omnipresentPlugins.concat(stylisPlugins, finalizingPlugins));
      var stylis = function stylis2(styles2) {
        return serialize$1(compile$1(styles2), serializer);
      };
      _insert = function insert(selector, serialized, sheet, shouldCache) {
        currentSheet = sheet;
        stylis(selector ? selector + "{" + serialized.styles + "}" : serialized.styles);
        if (shouldCache) {
          cache.inserted[serialized.name] = true;
        }
      };
    }
    var cache = {
      key,
      sheet: new StyleSheet({
        key,
        container: container2,
        nonce: options.nonce,
        speedy: options.speedy,
        prepend: options.prepend,
        insertionPoint: options.insertionPoint
      }),
      nonce: options.nonce,
      inserted,
      registered: {},
      insert: _insert
    };
    cache.sheet.hydrate(nodesToHydrate);
    return cache;
  };
  function _extends() {
    _extends = Object.assign ? Object.assign.bind() : function(target) {
      for (var i = 1; i < arguments.length; i++) {
        var source = arguments[i];
        for (var key in source) {
          if (Object.prototype.hasOwnProperty.call(source, key)) {
            target[key] = source[key];
          }
        }
      }
      return target;
    };
    return _extends.apply(this, arguments);
  }
  var reactIs$1 = { exports: {} };
  var reactIs_production_min = {};
  /** @license React v16.13.1
   * react-is.production.min.js
   *
   * Copyright (c) Facebook, Inc. and its affiliates.
   *
   * This source code is licensed under the MIT license found in the
   * LICENSE file in the root directory of this source tree.
   */
  var b = "function" === typeof Symbol && Symbol.for, c = b ? Symbol.for("react.element") : 60103, d = b ? Symbol.for("react.portal") : 60106, e = b ? Symbol.for("react.fragment") : 60107, f$1 = b ? Symbol.for("react.strict_mode") : 60108, g$1 = b ? Symbol.for("react.profiler") : 60114, h = b ? Symbol.for("react.provider") : 60109, k$1 = b ? Symbol.for("react.context") : 60110, l = b ? Symbol.for("react.async_mode") : 60111, m$1 = b ? Symbol.for("react.concurrent_mode") : 60111, n = b ? Symbol.for("react.forward_ref") : 60112, p = b ? Symbol.for("react.suspense") : 60113, q$1 = b ? Symbol.for("react.suspense_list") : 60120, r$1 = b ? Symbol.for("react.memo") : 60115, t$1 = b ? Symbol.for("react.lazy") : 60116, v$1 = b ? Symbol.for("react.block") : 60121, w$1 = b ? Symbol.for("react.fundamental") : 60117, x$1 = b ? Symbol.for("react.responder") : 60118, y$1 = b ? Symbol.for("react.scope") : 60119;
  function z$1(a) {
    if ("object" === typeof a && null !== a) {
      var u2 = a.$$typeof;
      switch (u2) {
        case c:
          switch (a = a.type, a) {
            case l:
            case m$1:
            case e:
            case g$1:
            case f$1:
            case p:
              return a;
            default:
              switch (a = a && a.$$typeof, a) {
                case k$1:
                case n:
                case t$1:
                case r$1:
                case h:
                  return a;
                default:
                  return u2;
              }
          }
        case d:
          return u2;
      }
    }
  }
  function A$1(a) {
    return z$1(a) === m$1;
  }
  reactIs_production_min.AsyncMode = l;
  reactIs_production_min.ConcurrentMode = m$1;
  reactIs_production_min.ContextConsumer = k$1;
  reactIs_production_min.ContextProvider = h;
  reactIs_production_min.Element = c;
  reactIs_production_min.ForwardRef = n;
  reactIs_production_min.Fragment = e;
  reactIs_production_min.Lazy = t$1;
  reactIs_production_min.Memo = r$1;
  reactIs_production_min.Portal = d;
  reactIs_production_min.Profiler = g$1;
  reactIs_production_min.StrictMode = f$1;
  reactIs_production_min.Suspense = p;
  reactIs_production_min.isAsyncMode = function(a) {
    return A$1(a) || z$1(a) === l;
  };
  reactIs_production_min.isConcurrentMode = A$1;
  reactIs_production_min.isContextConsumer = function(a) {
    return z$1(a) === k$1;
  };
  reactIs_production_min.isContextProvider = function(a) {
    return z$1(a) === h;
  };
  reactIs_production_min.isElement = function(a) {
    return "object" === typeof a && null !== a && a.$$typeof === c;
  };
  reactIs_production_min.isForwardRef = function(a) {
    return z$1(a) === n;
  };
  reactIs_production_min.isFragment = function(a) {
    return z$1(a) === e;
  };
  reactIs_production_min.isLazy = function(a) {
    return z$1(a) === t$1;
  };
  reactIs_production_min.isMemo = function(a) {
    return z$1(a) === r$1;
  };
  reactIs_production_min.isPortal = function(a) {
    return z$1(a) === d;
  };
  reactIs_production_min.isProfiler = function(a) {
    return z$1(a) === g$1;
  };
  reactIs_production_min.isStrictMode = function(a) {
    return z$1(a) === f$1;
  };
  reactIs_production_min.isSuspense = function(a) {
    return z$1(a) === p;
  };
  reactIs_production_min.isValidElementType = function(a) {
    return "string" === typeof a || "function" === typeof a || a === e || a === m$1 || a === g$1 || a === f$1 || a === p || a === q$1 || "object" === typeof a && null !== a && (a.$$typeof === t$1 || a.$$typeof === r$1 || a.$$typeof === h || a.$$typeof === k$1 || a.$$typeof === n || a.$$typeof === w$1 || a.$$typeof === x$1 || a.$$typeof === y$1 || a.$$typeof === v$1);
  };
  reactIs_production_min.typeOf = z$1;
  {
    reactIs$1.exports = reactIs_production_min;
  }
  var reactIsExports = reactIs$1.exports;
  var reactIs = reactIsExports;
  var FORWARD_REF_STATICS = {
    "$$typeof": true,
    render: true,
    defaultProps: true,
    displayName: true,
    propTypes: true
  };
  var MEMO_STATICS = {
    "$$typeof": true,
    compare: true,
    defaultProps: true,
    displayName: true,
    propTypes: true,
    type: true
  };
  var TYPE_STATICS = {};
  TYPE_STATICS[reactIs.ForwardRef] = FORWARD_REF_STATICS;
  TYPE_STATICS[reactIs.Memo] = MEMO_STATICS;
  var isBrowser$1 = true;
  function getRegisteredStyles(registered, registeredStyles, classNames2) {
    var rawClassName = "";
    classNames2.split(" ").forEach(function(className) {
      if (registered[className] !== void 0) {
        registeredStyles.push(registered[className] + ";");
      } else {
        rawClassName += className + " ";
      }
    });
    return rawClassName;
  }
  var registerStyles = function registerStyles2(cache, serialized, isStringTag) {
    var className = cache.key + "-" + serialized.name;
    if (
      // we only need to add the styles to the registered cache if the
      // class name could be used further down
      // the tree but if it's a string tag, we know it won't
      // so we don't have to add it to registered cache.
      // this improves memory usage since we can avoid storing the whole style string
      (isStringTag === false || // we need to always store it if we're in compat mode and
      // in node since emotion-server relies on whether a style is in
      // the registered cache to know whether a style is global or not
      // also, note that this check will be dead code eliminated in the browser
      isBrowser$1 === false) && cache.registered[className] === void 0
    ) {
      cache.registered[className] = serialized.styles;
    }
  };
  var insertStyles = function insertStyles2(cache, serialized, isStringTag) {
    registerStyles(cache, serialized, isStringTag);
    var className = cache.key + "-" + serialized.name;
    if (cache.inserted[serialized.name] === void 0) {
      var current = serialized;
      do {
        cache.insert(serialized === current ? "." + className : "", current, cache.sheet, true);
        current = current.next;
      } while (current !== void 0);
    }
  };
  function murmur2(str) {
    var h2 = 0;
    var k2, i = 0, len = str.length;
    for (; len >= 4; ++i, len -= 4) {
      k2 = str.charCodeAt(i) & 255 | (str.charCodeAt(++i) & 255) << 8 | (str.charCodeAt(++i) & 255) << 16 | (str.charCodeAt(++i) & 255) << 24;
      k2 = /* Math.imul(k, m): */
      (k2 & 65535) * 1540483477 + ((k2 >>> 16) * 59797 << 16);
      k2 ^= /* k >>> r: */
      k2 >>> 24;
      h2 = /* Math.imul(k, m): */
      (k2 & 65535) * 1540483477 + ((k2 >>> 16) * 59797 << 16) ^ /* Math.imul(h, m): */
      (h2 & 65535) * 1540483477 + ((h2 >>> 16) * 59797 << 16);
    }
    switch (len) {
      case 3:
        h2 ^= (str.charCodeAt(i + 2) & 255) << 16;
      case 2:
        h2 ^= (str.charCodeAt(i + 1) & 255) << 8;
      case 1:
        h2 ^= str.charCodeAt(i) & 255;
        h2 = /* Math.imul(h, m): */
        (h2 & 65535) * 1540483477 + ((h2 >>> 16) * 59797 << 16);
    }
    h2 ^= h2 >>> 13;
    h2 = /* Math.imul(h, m): */
    (h2 & 65535) * 1540483477 + ((h2 >>> 16) * 59797 << 16);
    return ((h2 ^ h2 >>> 15) >>> 0).toString(36);
  }
  var unitlessKeys = {
    animationIterationCount: 1,
    aspectRatio: 1,
    borderImageOutset: 1,
    borderImageSlice: 1,
    borderImageWidth: 1,
    boxFlex: 1,
    boxFlexGroup: 1,
    boxOrdinalGroup: 1,
    columnCount: 1,
    columns: 1,
    flex: 1,
    flexGrow: 1,
    flexPositive: 1,
    flexShrink: 1,
    flexNegative: 1,
    flexOrder: 1,
    gridRow: 1,
    gridRowEnd: 1,
    gridRowSpan: 1,
    gridRowStart: 1,
    gridColumn: 1,
    gridColumnEnd: 1,
    gridColumnSpan: 1,
    gridColumnStart: 1,
    msGridRow: 1,
    msGridRowSpan: 1,
    msGridColumn: 1,
    msGridColumnSpan: 1,
    fontWeight: 1,
    lineHeight: 1,
    opacity: 1,
    order: 1,
    orphans: 1,
    tabSize: 1,
    widows: 1,
    zIndex: 1,
    zoom: 1,
    WebkitLineClamp: 1,
    // SVG-related properties
    fillOpacity: 1,
    floodOpacity: 1,
    stopOpacity: 1,
    strokeDasharray: 1,
    strokeDashoffset: 1,
    strokeMiterlimit: 1,
    strokeOpacity: 1,
    strokeWidth: 1
  };
  var hyphenateRegex = /[A-Z]|^ms/g;
  var animationRegex = /_EMO_([^_]+?)_([^]*?)_EMO_/g;
  var isCustomProperty = function isCustomProperty2(property) {
    return property.charCodeAt(1) === 45;
  };
  var isProcessableValue = function isProcessableValue2(value) {
    return value != null && typeof value !== "boolean";
  };
  var processStyleName = /* @__PURE__ */ memoize$2(function(styleName) {
    return isCustomProperty(styleName) ? styleName : styleName.replace(hyphenateRegex, "-$&").toLowerCase();
  });
  var processStyleValue = function processStyleValue2(key, value) {
    switch (key) {
      case "animation":
      case "animationName": {
        if (typeof value === "string") {
          return value.replace(animationRegex, function(match2, p1, p2) {
            cursor = {
              name: p1,
              styles: p2,
              next: cursor
            };
            return p1;
          });
        }
      }
    }
    if (unitlessKeys[key] !== 1 && !isCustomProperty(key) && typeof value === "number" && value !== 0) {
      return value + "px";
    }
    return value;
  };
  var noComponentSelectorMessage = "Component selectors can only be used in conjunction with @emotion/babel-plugin, the swc Emotion plugin, or another Emotion-aware compiler transform.";
  function handleInterpolation(mergedProps, registered, interpolation) {
    if (interpolation == null) {
      return "";
    }
    if (interpolation.__emotion_styles !== void 0) {
      return interpolation;
    }
    switch (typeof interpolation) {
      case "boolean": {
        return "";
      }
      case "object": {
        if (interpolation.anim === 1) {
          cursor = {
            name: interpolation.name,
            styles: interpolation.styles,
            next: cursor
          };
          return interpolation.name;
        }
        if (interpolation.styles !== void 0) {
          var next2 = interpolation.next;
          if (next2 !== void 0) {
            while (next2 !== void 0) {
              cursor = {
                name: next2.name,
                styles: next2.styles,
                next: cursor
              };
              next2 = next2.next;
            }
          }
          var styles2 = interpolation.styles + ";";
          return styles2;
        }
        return createStringFromObject(mergedProps, registered, interpolation);
      }
      case "function": {
        if (mergedProps !== void 0) {
          var previousCursor = cursor;
          var result = interpolation(mergedProps);
          cursor = previousCursor;
          return handleInterpolation(mergedProps, registered, result);
        }
        break;
      }
    }
    if (registered == null) {
      return interpolation;
    }
    var cached = registered[interpolation];
    return cached !== void 0 ? cached : interpolation;
  }
  function createStringFromObject(mergedProps, registered, obj) {
    var string = "";
    if (Array.isArray(obj)) {
      for (var i = 0; i < obj.length; i++) {
        string += handleInterpolation(mergedProps, registered, obj[i]) + ";";
      }
    } else {
      for (var _key in obj) {
        var value = obj[_key];
        if (typeof value !== "object") {
          if (registered != null && registered[value] !== void 0) {
            string += _key + "{" + registered[value] + "}";
          } else if (isProcessableValue(value)) {
            string += processStyleName(_key) + ":" + processStyleValue(_key, value) + ";";
          }
        } else {
          if (_key === "NO_COMPONENT_SELECTOR" && false) {
            throw new Error(noComponentSelectorMessage);
          }
          if (Array.isArray(value) && typeof value[0] === "string" && (registered == null || registered[value[0]] === void 0)) {
            for (var _i = 0; _i < value.length; _i++) {
              if (isProcessableValue(value[_i])) {
                string += processStyleName(_key) + ":" + processStyleValue(_key, value[_i]) + ";";
              }
            }
          } else {
            var interpolated = handleInterpolation(mergedProps, registered, value);
            switch (_key) {
              case "animation":
              case "animationName": {
                string += processStyleName(_key) + ":" + interpolated + ";";
                break;
              }
              default: {
                string += _key + "{" + interpolated + "}";
              }
            }
          }
        }
      }
    }
    return string;
  }
  var labelPattern = /label:\s*([^\s;\n{]+)\s*(;|$)/g;
  var cursor;
  var serializeStyles = function serializeStyles2(args, registered, mergedProps) {
    if (args.length === 1 && typeof args[0] === "object" && args[0] !== null && args[0].styles !== void 0) {
      return args[0];
    }
    var stringMode = true;
    var styles2 = "";
    cursor = void 0;
    var strings = args[0];
    if (strings == null || strings.raw === void 0) {
      stringMode = false;
      styles2 += handleInterpolation(mergedProps, registered, strings);
    } else {
      styles2 += strings[0];
    }
    for (var i = 1; i < args.length; i++) {
      styles2 += handleInterpolation(mergedProps, registered, args[i]);
      if (stringMode) {
        styles2 += strings[i];
      }
    }
    labelPattern.lastIndex = 0;
    var identifierName = "";
    var match2;
    while ((match2 = labelPattern.exec(styles2)) !== null) {
      identifierName += "-" + // $FlowFixMe we know it's not null
      match2[1];
    }
    var name = murmur2(styles2) + identifierName;
    return {
      name,
      styles: styles2,
      next: cursor
    };
  };
  var syncFallback = function syncFallback2(create) {
    return create();
  };
  var useInsertionEffect = React$1["useInsertionEffect"] ? React$1["useInsertionEffect"] : false;
  var useInsertionEffectAlwaysWithSyncFallback = useInsertionEffect || syncFallback;
  var useInsertionEffectWithLayoutFallback = useInsertionEffect || reactExports.useLayoutEffect;
  var EmotionCacheContext = /* @__PURE__ */ reactExports.createContext(
    // we're doing this to avoid preconstruct's dead code elimination in this one case
    // because this module is primarily intended for the browser and node
    // but it's also required in react native and similar environments sometimes
    // and we could have a special build just for that
    // but this is much easier and the native packages
    // might use a different theme context in the future anyway
    typeof HTMLElement !== "undefined" ? /* @__PURE__ */ createCache({
      key: "css"
    }) : null
  );
  EmotionCacheContext.Provider;
  var withEmotionCache = function withEmotionCache2(func) {
    return /* @__PURE__ */ reactExports.forwardRef(function(props, ref) {
      var cache = reactExports.useContext(EmotionCacheContext);
      return func(props, cache, ref);
    });
  };
  var ThemeContext = /* @__PURE__ */ reactExports.createContext({});
  var getTheme$1 = function getTheme2(outerTheme, theme2) {
    if (typeof theme2 === "function") {
      var mergedTheme = theme2(outerTheme);
      return mergedTheme;
    }
    return _extends({}, outerTheme, theme2);
  };
  var createCacheWithTheme = /* @__PURE__ */ weakMemoize(function(outerTheme) {
    return weakMemoize(function(theme2) {
      return getTheme$1(outerTheme, theme2);
    });
  });
  var ThemeProvider$1 = function ThemeProvider2(props) {
    var theme2 = reactExports.useContext(ThemeContext);
    if (props.theme !== theme2) {
      theme2 = createCacheWithTheme(theme2)(props.theme);
    }
    return /* @__PURE__ */ reactExports.createElement(ThemeContext.Provider, {
      value: theme2
    }, props.children);
  };
  var Global = /* @__PURE__ */ withEmotionCache(function(props, cache) {
    var styles2 = props.styles;
    var serialized = serializeStyles([styles2], void 0, reactExports.useContext(ThemeContext));
    var sheetRef = reactExports.useRef();
    useInsertionEffectWithLayoutFallback(function() {
      var key = cache.key + "-global";
      var sheet = new cache.sheet.constructor({
        key,
        nonce: cache.sheet.nonce,
        container: cache.sheet.container,
        speedy: cache.sheet.isSpeedy
      });
      var rehydrating = false;
      var node2 = document.querySelector('style[data-emotion="' + key + " " + serialized.name + '"]');
      if (cache.sheet.tags.length) {
        sheet.before = cache.sheet.tags[0];
      }
      if (node2 !== null) {
        rehydrating = true;
        node2.setAttribute("data-emotion", key);
        sheet.hydrate([node2]);
      }
      sheetRef.current = [sheet, rehydrating];
      return function() {
        sheet.flush();
      };
    }, [cache]);
    useInsertionEffectWithLayoutFallback(function() {
      var sheetRefCurrent = sheetRef.current;
      var sheet = sheetRefCurrent[0], rehydrating = sheetRefCurrent[1];
      if (rehydrating) {
        sheetRefCurrent[1] = false;
        return;
      }
      if (serialized.next !== void 0) {
        insertStyles(cache, serialized.next, true);
      }
      if (sheet.tags.length) {
        var element = sheet.tags[sheet.tags.length - 1].nextElementSibling;
        sheet.before = element;
        sheet.flush();
      }
      cache.insert("", serialized, sheet, false);
    }, [cache, serialized.name]);
    return null;
  });
  function css$2() {
    for (var _len = arguments.length, args = new Array(_len), _key = 0; _key < _len; _key++) {
      args[_key] = arguments[_key];
    }
    return serializeStyles(args);
  }
  var keyframes$1 = function keyframes2() {
    var insertable = css$2.apply(void 0, arguments);
    var name = "animation-" + insertable.name;
    return {
      name,
      styles: "@keyframes " + name + "{" + insertable.styles + "}",
      anim: 1,
      toString: function toString() {
        return "_EMO_" + this.name + "_" + this.styles + "_EMO_";
      }
    };
  };
  var css$1 = String.raw;
  var vhPolyfill = css$1`
  :root,
  :host {
    --chakra-vh: 100vh;
  }

  @supports (height: -webkit-fill-available) {
    :root,
    :host {
      --chakra-vh: -webkit-fill-available;
    }
  }

  @supports (height: -moz-fill-available) {
    :root,
    :host {
      --chakra-vh: -moz-fill-available;
    }
  }

  @supports (height: 100dvh) {
    :root,
    :host {
      --chakra-vh: 100dvh;
    }
  }
`;
  var CSSPolyfill = () => /* @__PURE__ */ jsxRuntimeExports.jsx(Global, { styles: vhPolyfill });
  var CSSReset = ({ scope = "" }) => /* @__PURE__ */ jsxRuntimeExports.jsx(
    Global,
    {
      styles: css$1`
      html {
        line-height: 1.5;
        -webkit-text-size-adjust: 100%;
        font-family: system-ui, sans-serif;
        -webkit-font-smoothing: antialiased;
        text-rendering: optimizeLegibility;
        -moz-osx-font-smoothing: grayscale;
        touch-action: manipulation;
      }

      body {
        position: relative;
        min-height: 100%;
        margin: 0;
        font-feature-settings: "kern";
      }

      ${scope} :where(*, *::before, *::after) {
        border-width: 0;
        border-style: solid;
        box-sizing: border-box;
        word-wrap: break-word;
      }

      main {
        display: block;
      }

      ${scope} hr {
        border-top-width: 1px;
        box-sizing: content-box;
        height: 0;
        overflow: visible;
      }

      ${scope} :where(pre, code, kbd,samp) {
        font-family: SFMono-Regular, Menlo, Monaco, Consolas, monospace;
        font-size: 1em;
      }

      ${scope} a {
        background-color: transparent;
        color: inherit;
        text-decoration: inherit;
      }

      ${scope} abbr[title] {
        border-bottom: none;
        text-decoration: underline;
        -webkit-text-decoration: underline dotted;
        text-decoration: underline dotted;
      }

      ${scope} :where(b, strong) {
        font-weight: bold;
      }

      ${scope} small {
        font-size: 80%;
      }

      ${scope} :where(sub,sup) {
        font-size: 75%;
        line-height: 0;
        position: relative;
        vertical-align: baseline;
      }

      ${scope} sub {
        bottom: -0.25em;
      }

      ${scope} sup {
        top: -0.5em;
      }

      ${scope} img {
        border-style: none;
      }

      ${scope} :where(button, input, optgroup, select, textarea) {
        font-family: inherit;
        font-size: 100%;
        line-height: 1.15;
        margin: 0;
      }

      ${scope} :where(button, input) {
        overflow: visible;
      }

      ${scope} :where(button, select) {
        text-transform: none;
      }

      ${scope} :where(
          button::-moz-focus-inner,
          [type="button"]::-moz-focus-inner,
          [type="reset"]::-moz-focus-inner,
          [type="submit"]::-moz-focus-inner
        ) {
        border-style: none;
        padding: 0;
      }

      ${scope} fieldset {
        padding: 0.35em 0.75em 0.625em;
      }

      ${scope} legend {
        box-sizing: border-box;
        color: inherit;
        display: table;
        max-width: 100%;
        padding: 0;
        white-space: normal;
      }

      ${scope} progress {
        vertical-align: baseline;
      }

      ${scope} textarea {
        overflow: auto;
      }

      ${scope} :where([type="checkbox"], [type="radio"]) {
        box-sizing: border-box;
        padding: 0;
      }

      ${scope} input[type="number"]::-webkit-inner-spin-button,
      ${scope} input[type="number"]::-webkit-outer-spin-button {
        -webkit-appearance: none !important;
      }

      ${scope} input[type="number"] {
        -moz-appearance: textfield;
      }

      ${scope} input[type="search"] {
        -webkit-appearance: textfield;
        outline-offset: -2px;
      }

      ${scope} input[type="search"]::-webkit-search-decoration {
        -webkit-appearance: none !important;
      }

      ${scope} ::-webkit-file-upload-button {
        -webkit-appearance: button;
        font: inherit;
      }

      ${scope} details {
        display: block;
      }

      ${scope} summary {
        display: list-item;
      }

      template {
        display: none;
      }

      [hidden] {
        display: none !important;
      }

      ${scope} :where(
          blockquote,
          dl,
          dd,
          h1,
          h2,
          h3,
          h4,
          h5,
          h6,
          hr,
          figure,
          p,
          pre
        ) {
        margin: 0;
      }

      ${scope} button {
        background: transparent;
        padding: 0;
      }

      ${scope} fieldset {
        margin: 0;
        padding: 0;
      }

      ${scope} :where(ol, ul) {
        margin: 0;
        padding: 0;
      }

      ${scope} textarea {
        resize: vertical;
      }

      ${scope} :where(button, [role="button"]) {
        cursor: pointer;
      }

      ${scope} button::-moz-focus-inner {
        border: 0 !important;
      }

      ${scope} table {
        border-collapse: collapse;
      }

      ${scope} :where(h1, h2, h3, h4, h5, h6) {
        font-size: inherit;
        font-weight: inherit;
      }

      ${scope} :where(button, input, optgroup, select, textarea) {
        padding: 0;
        line-height: inherit;
        color: inherit;
      }

      ${scope} :where(img, svg, video, canvas, audio, iframe, embed, object) {
        display: block;
      }

      ${scope} :where(img, video) {
        max-width: 100%;
        height: auto;
      }

      [data-js-focus-visible]
        :focus:not([data-focus-visible-added]):not(
          [data-focus-visible-disabled]
        ) {
        outline: none;
        box-shadow: none;
      }

      ${scope} select::-ms-expand {
        display: none;
      }

      ${vhPolyfill}
    `
    }
  );
  function getErrorMessage(hook, provider) {
    return `${hook} returned \`undefined\`. Seems you forgot to wrap component within ${provider}`;
  }
  function createContext$1(options = {}) {
    const {
      name,
      strict = true,
      hookName = "useContext",
      providerName = "Provider",
      errorMessage,
      defaultValue
    } = options;
    const Context = reactExports.createContext(defaultValue);
    Context.displayName = name;
    function useContext() {
      var _a4;
      const context = reactExports.useContext(Context);
      if (!context && strict) {
        const error = new Error(
          errorMessage != null ? errorMessage : getErrorMessage(hookName, providerName)
        );
        error.name = "ContextError";
        (_a4 = Error.captureStackTrace) == null ? void 0 : _a4.call(Error, error, useContext);
        throw error;
      }
      return context;
    }
    return [Context.Provider, useContext, Context];
  }
  var [PortalManagerContextProvider, usePortalManager] = createContext$1({
    strict: false,
    name: "PortalManagerContext"
  });
  function PortalManager(props) {
    const { children, zIndex } = props;
    return /* @__PURE__ */ jsxRuntimeExports.jsx(PortalManagerContextProvider, { value: { zIndex }, children });
  }
  PortalManager.displayName = "PortalManager";
  var useSafeLayoutEffect = Boolean(globalThis == null ? void 0 : globalThis.document) ? reactExports.useLayoutEffect : reactExports.useEffect;
  var [PortalContextProvider, usePortalContext] = createContext$1({
    strict: false,
    name: "PortalContext"
  });
  var PORTAL_CLASSNAME = "chakra-portal";
  var PORTAL_SELECTOR = `.chakra-portal`;
  var Container = (props) => /* @__PURE__ */ jsxRuntimeExports.jsx(
    "div",
    {
      className: "chakra-portal-zIndex",
      style: {
        position: "absolute",
        zIndex: props.zIndex,
        top: 0,
        left: 0,
        right: 0
        // NB: Don't add `bottom: 0`, it makes the entire app unusable
        // @see https://github.com/chakra-ui/chakra-ui/issues/3201
      },
      children: props.children
    }
  );
  var DefaultPortal = (props) => {
    const { appendToParentPortal, children } = props;
    const [tempNode, setTempNode] = reactExports.useState(null);
    const portal = reactExports.useRef(null);
    const [, forceUpdate] = reactExports.useState({});
    reactExports.useEffect(() => forceUpdate({}), []);
    const parentPortal = usePortalContext();
    const manager = usePortalManager();
    useSafeLayoutEffect(() => {
      if (!tempNode)
        return;
      const doc = tempNode.ownerDocument;
      const host = appendToParentPortal ? parentPortal != null ? parentPortal : doc.body : doc.body;
      if (!host)
        return;
      portal.current = doc.createElement("div");
      portal.current.className = PORTAL_CLASSNAME;
      host.appendChild(portal.current);
      forceUpdate({});
      const portalNode = portal.current;
      return () => {
        if (host.contains(portalNode)) {
          host.removeChild(portalNode);
        }
      };
    }, [tempNode]);
    const _children = (manager == null ? void 0 : manager.zIndex) ? /* @__PURE__ */ jsxRuntimeExports.jsx(Container, { zIndex: manager == null ? void 0 : manager.zIndex, children }) : children;
    return portal.current ? reactDomExports.createPortal(
      /* @__PURE__ */ jsxRuntimeExports.jsx(PortalContextProvider, { value: portal.current, children: _children }),
      portal.current
    ) : /* @__PURE__ */ jsxRuntimeExports.jsx(
      "span",
      {
        ref: (el2) => {
          if (el2)
            setTempNode(el2);
        }
      }
    );
  };
  var ContainerPortal = (props) => {
    const { children, containerRef, appendToParentPortal } = props;
    const containerEl = containerRef.current;
    const host = containerEl != null ? containerEl : typeof window !== "undefined" ? document.body : void 0;
    const portal = reactExports.useMemo(() => {
      const node2 = containerEl == null ? void 0 : containerEl.ownerDocument.createElement("div");
      if (node2)
        node2.className = PORTAL_CLASSNAME;
      return node2;
    }, [containerEl]);
    const [, forceUpdate] = reactExports.useState({});
    useSafeLayoutEffect(() => forceUpdate({}), []);
    useSafeLayoutEffect(() => {
      if (!portal || !host)
        return;
      host.appendChild(portal);
      return () => {
        host.removeChild(portal);
      };
    }, [portal, host]);
    if (host && portal) {
      return reactDomExports.createPortal(
        /* @__PURE__ */ jsxRuntimeExports.jsx(PortalContextProvider, { value: appendToParentPortal ? portal : null, children }),
        portal
      );
    }
    return null;
  };
  function Portal(props) {
    const portalProps = {
      appendToParentPortal: true,
      ...props
    };
    const { containerRef, ...rest } = portalProps;
    return containerRef ? /* @__PURE__ */ jsxRuntimeExports.jsx(ContainerPortal, { containerRef, ...rest }) : /* @__PURE__ */ jsxRuntimeExports.jsx(DefaultPortal, { ...rest });
  }
  Portal.className = PORTAL_CLASSNAME;
  Portal.selector = PORTAL_SELECTOR;
  Portal.displayName = "Portal";
  function useTheme() {
    const theme2 = reactExports.useContext(
      ThemeContext
    );
    if (!theme2) {
      throw Error(
        "useTheme: `theme` is undefined. Seems you forgot to wrap your app in `<ChakraProvider />` or `<ThemeProvider />`"
      );
    }
    return theme2;
  }
  var ColorModeContext = reactExports.createContext({});
  ColorModeContext.displayName = "ColorModeContext";
  function useColorMode() {
    const context = reactExports.useContext(ColorModeContext);
    if (context === void 0) {
      throw new Error("useColorMode must be used within a ColorModeProvider");
    }
    return context;
  }
  var classNames = {
    light: "chakra-ui-light",
    dark: "chakra-ui-dark"
  };
  function getColorModeUtils(options = {}) {
    const { preventTransition = true } = options;
    const utils = {
      setDataset: (value) => {
        const cleanup = preventTransition ? utils.preventTransition() : void 0;
        document.documentElement.dataset.theme = value;
        document.documentElement.style.colorScheme = value;
        cleanup == null ? void 0 : cleanup();
      },
      setClassName(dark) {
        document.body.classList.add(dark ? classNames.dark : classNames.light);
        document.body.classList.remove(dark ? classNames.light : classNames.dark);
      },
      query() {
        return window.matchMedia("(prefers-color-scheme: dark)");
      },
      getSystemTheme(fallback) {
        var _a4;
        const dark = (_a4 = utils.query().matches) != null ? _a4 : fallback === "dark";
        return dark ? "dark" : "light";
      },
      addListener(fn) {
        const mql = utils.query();
        const listener = (e2) => {
          fn(e2.matches ? "dark" : "light");
        };
        if (typeof mql.addListener === "function")
          mql.addListener(listener);
        else
          mql.addEventListener("change", listener);
        return () => {
          if (typeof mql.removeListener === "function")
            mql.removeListener(listener);
          else
            mql.removeEventListener("change", listener);
        };
      },
      preventTransition() {
        const css2 = document.createElement("style");
        css2.appendChild(
          document.createTextNode(
            `*{-webkit-transition:none!important;-moz-transition:none!important;-o-transition:none!important;-ms-transition:none!important;transition:none!important}`
          )
        );
        document.head.appendChild(css2);
        return () => {
          (() => window.getComputedStyle(document.body))();
          requestAnimationFrame(() => {
            requestAnimationFrame(() => {
              document.head.removeChild(css2);
            });
          });
        };
      }
    };
    return utils;
  }
  var STORAGE_KEY = "chakra-ui-color-mode";
  function createLocalStorageManager(key) {
    return {
      ssr: false,
      type: "localStorage",
      get(init) {
        if (!(globalThis == null ? void 0 : globalThis.document))
          return init;
        let value;
        try {
          value = localStorage.getItem(key) || init;
        } catch (e2) {
        }
        return value || init;
      },
      set(value) {
        try {
          localStorage.setItem(key, value);
        } catch (e2) {
        }
      }
    };
  }
  var localStorageManager = createLocalStorageManager(STORAGE_KEY);
  var noop$1 = () => {
  };
  function getTheme(manager, fallback) {
    return manager.type === "cookie" && manager.ssr ? manager.get(fallback) : fallback;
  }
  function ColorModeProvider(props) {
    const {
      value,
      children,
      options: {
        useSystemColorMode,
        initialColorMode,
        disableTransitionOnChange
      } = {},
      colorModeManager = localStorageManager
    } = props;
    const defaultColorMode = initialColorMode === "dark" ? "dark" : "light";
    const [colorMode, rawSetColorMode] = reactExports.useState(
      () => getTheme(colorModeManager, defaultColorMode)
    );
    const [resolvedColorMode, setResolvedColorMode] = reactExports.useState(
      () => getTheme(colorModeManager)
    );
    const { getSystemTheme, setClassName, setDataset, addListener } = reactExports.useMemo(
      () => getColorModeUtils({ preventTransition: disableTransitionOnChange }),
      [disableTransitionOnChange]
    );
    const resolvedValue = initialColorMode === "system" && !colorMode ? resolvedColorMode : colorMode;
    const setColorMode = reactExports.useCallback(
      (value2) => {
        const resolved = value2 === "system" ? getSystemTheme() : value2;
        rawSetColorMode(resolved);
        setClassName(resolved === "dark");
        setDataset(resolved);
        colorModeManager.set(resolved);
      },
      [colorModeManager, getSystemTheme, setClassName, setDataset]
    );
    useSafeLayoutEffect(() => {
      if (initialColorMode === "system") {
        setResolvedColorMode(getSystemTheme());
      }
    }, []);
    reactExports.useEffect(() => {
      const managerValue = colorModeManager.get();
      if (managerValue) {
        setColorMode(managerValue);
        return;
      }
      if (initialColorMode === "system") {
        setColorMode("system");
        return;
      }
      setColorMode(defaultColorMode);
    }, [colorModeManager, defaultColorMode, initialColorMode, setColorMode]);
    const toggleColorMode = reactExports.useCallback(() => {
      setColorMode(resolvedValue === "dark" ? "light" : "dark");
    }, [resolvedValue, setColorMode]);
    reactExports.useEffect(() => {
      if (!useSystemColorMode)
        return;
      return addListener(setColorMode);
    }, [useSystemColorMode, addListener, setColorMode]);
    const context = reactExports.useMemo(
      () => ({
        colorMode: value != null ? value : resolvedValue,
        toggleColorMode: value ? noop$1 : toggleColorMode,
        setColorMode: value ? noop$1 : setColorMode,
        forced: value !== void 0
      }),
      [resolvedValue, toggleColorMode, setColorMode, value]
    );
    return /* @__PURE__ */ jsxRuntimeExports.jsx(ColorModeContext.Provider, { value: context, children });
  }
  ColorModeProvider.displayName = "ColorModeProvider";
  function useChakra() {
    const colorModeResult = useColorMode();
    const theme2 = useTheme();
    return { ...colorModeResult, theme: theme2 };
  }
  var cx = (...classNames2) => classNames2.filter(Boolean).join(" ");
  function isObject(value) {
    const type = typeof value;
    return value != null && (type === "object" || type === "function") && !Array.isArray(value);
  }
  function runIfFn$2(valueOrFn, ...args) {
    return isFunction$3(valueOrFn) ? valueOrFn(...args) : valueOrFn;
  }
  var isFunction$3 = (value) => typeof value === "function";
  var dataAttr = (condition) => condition ? "" : void 0;
  var ariaAttr = (condition) => condition ? true : void 0;
  function callAllHandlers(...fns) {
    return function func(event) {
      fns.some((fn) => {
        fn == null ? void 0 : fn(event);
        return event == null ? void 0 : event.defaultPrevented;
      });
    };
  }
  var lodash_mergewith = { exports: {} };
  lodash_mergewith.exports;
  (function(module, exports) {
    var LARGE_ARRAY_SIZE = 200;
    var HASH_UNDEFINED = "__lodash_hash_undefined__";
    var HOT_COUNT = 800, HOT_SPAN = 16;
    var MAX_SAFE_INTEGER = 9007199254740991;
    var argsTag = "[object Arguments]", arrayTag = "[object Array]", asyncTag = "[object AsyncFunction]", boolTag = "[object Boolean]", dateTag = "[object Date]", errorTag = "[object Error]", funcTag = "[object Function]", genTag = "[object GeneratorFunction]", mapTag = "[object Map]", numberTag = "[object Number]", nullTag = "[object Null]", objectTag = "[object Object]", proxyTag = "[object Proxy]", regexpTag = "[object RegExp]", setTag = "[object Set]", stringTag = "[object String]", undefinedTag = "[object Undefined]", weakMapTag = "[object WeakMap]";
    var arrayBufferTag = "[object ArrayBuffer]", dataViewTag = "[object DataView]", float32Tag = "[object Float32Array]", float64Tag = "[object Float64Array]", int8Tag = "[object Int8Array]", int16Tag = "[object Int16Array]", int32Tag = "[object Int32Array]", uint8Tag = "[object Uint8Array]", uint8ClampedTag = "[object Uint8ClampedArray]", uint16Tag = "[object Uint16Array]", uint32Tag = "[object Uint32Array]";
    var reRegExpChar = /[\\^$.*+?()[\]{}|]/g;
    var reIsHostCtor = /^\[object .+?Constructor\]$/;
    var reIsUint = /^(?:0|[1-9]\d*)$/;
    var typedArrayTags = {};
    typedArrayTags[float32Tag] = typedArrayTags[float64Tag] = typedArrayTags[int8Tag] = typedArrayTags[int16Tag] = typedArrayTags[int32Tag] = typedArrayTags[uint8Tag] = typedArrayTags[uint8ClampedTag] = typedArrayTags[uint16Tag] = typedArrayTags[uint32Tag] = true;
    typedArrayTags[argsTag] = typedArrayTags[arrayTag] = typedArrayTags[arrayBufferTag] = typedArrayTags[boolTag] = typedArrayTags[dataViewTag] = typedArrayTags[dateTag] = typedArrayTags[errorTag] = typedArrayTags[funcTag] = typedArrayTags[mapTag] = typedArrayTags[numberTag] = typedArrayTags[objectTag] = typedArrayTags[regexpTag] = typedArrayTags[setTag] = typedArrayTags[stringTag] = typedArrayTags[weakMapTag] = false;
    var freeGlobal = typeof commonjsGlobal == "object" && commonjsGlobal && commonjsGlobal.Object === Object && commonjsGlobal;
    var freeSelf = typeof self == "object" && self && self.Object === Object && self;
    var root = freeGlobal || freeSelf || Function("return this")();
    var freeExports = exports && !exports.nodeType && exports;
    var freeModule = freeExports && true && module && !module.nodeType && module;
    var moduleExports = freeModule && freeModule.exports === freeExports;
    var freeProcess = moduleExports && freeGlobal.process;
    var nodeUtil = function() {
      try {
        var types = freeModule && freeModule.require && freeModule.require("util").types;
        if (types) {
          return types;
        }
        return freeProcess && freeProcess.binding && freeProcess.binding("util");
      } catch (e2) {
      }
    }();
    var nodeIsTypedArray = nodeUtil && nodeUtil.isTypedArray;
    function apply(func, thisArg, args) {
      switch (args.length) {
        case 0:
          return func.call(thisArg);
        case 1:
          return func.call(thisArg, args[0]);
        case 2:
          return func.call(thisArg, args[0], args[1]);
        case 3:
          return func.call(thisArg, args[0], args[1], args[2]);
      }
      return func.apply(thisArg, args);
    }
    function baseTimes(n2, iteratee) {
      var index = -1, result = Array(n2);
      while (++index < n2) {
        result[index] = iteratee(index);
      }
      return result;
    }
    function baseUnary(func) {
      return function(value) {
        return func(value);
      };
    }
    function getValue(object, key) {
      return object == null ? void 0 : object[key];
    }
    function overArg(func, transform2) {
      return function(arg) {
        return func(transform2(arg));
      };
    }
    var arrayProto = Array.prototype, funcProto = Function.prototype, objectProto = Object.prototype;
    var coreJsData = root["__core-js_shared__"];
    var funcToString = funcProto.toString;
    var hasOwnProperty = objectProto.hasOwnProperty;
    var maskSrcKey = function() {
      var uid = /[^.]+$/.exec(coreJsData && coreJsData.keys && coreJsData.keys.IE_PROTO || "");
      return uid ? "Symbol(src)_1." + uid : "";
    }();
    var nativeObjectToString = objectProto.toString;
    var objectCtorString = funcToString.call(Object);
    var reIsNative = RegExp(
      "^" + funcToString.call(hasOwnProperty).replace(reRegExpChar, "\\$&").replace(/hasOwnProperty|(function).*?(?=\\\()| for .+?(?=\\\])/g, "$1.*?") + "$"
    );
    var Buffer = moduleExports ? root.Buffer : void 0, Symbol2 = root.Symbol, Uint8Array = root.Uint8Array;
    Buffer ? Buffer.allocUnsafe : void 0;
    var getPrototype = overArg(Object.getPrototypeOf, Object), objectCreate = Object.create, propertyIsEnumerable = objectProto.propertyIsEnumerable, splice = arrayProto.splice, symToStringTag = Symbol2 ? Symbol2.toStringTag : void 0;
    var defineProperty = function() {
      try {
        var func = getNative(Object, "defineProperty");
        func({}, "", {});
        return func;
      } catch (e2) {
      }
    }();
    var nativeIsBuffer = Buffer ? Buffer.isBuffer : void 0, nativeMax = Math.max, nativeNow = Date.now;
    var Map2 = getNative(root, "Map"), nativeCreate = getNative(Object, "create");
    var baseCreate = /* @__PURE__ */ function() {
      function object() {
      }
      return function(proto) {
        if (!isObject2(proto)) {
          return {};
        }
        if (objectCreate) {
          return objectCreate(proto);
        }
        object.prototype = proto;
        var result = new object();
        object.prototype = void 0;
        return result;
      };
    }();
    function Hash(entries) {
      var index = -1, length2 = entries == null ? 0 : entries.length;
      this.clear();
      while (++index < length2) {
        var entry = entries[index];
        this.set(entry[0], entry[1]);
      }
    }
    function hashClear() {
      this.__data__ = nativeCreate ? nativeCreate(null) : {};
      this.size = 0;
    }
    function hashDelete(key) {
      var result = this.has(key) && delete this.__data__[key];
      this.size -= result ? 1 : 0;
      return result;
    }
    function hashGet(key) {
      var data = this.__data__;
      if (nativeCreate) {
        var result = data[key];
        return result === HASH_UNDEFINED ? void 0 : result;
      }
      return hasOwnProperty.call(data, key) ? data[key] : void 0;
    }
    function hashHas(key) {
      var data = this.__data__;
      return nativeCreate ? data[key] !== void 0 : hasOwnProperty.call(data, key);
    }
    function hashSet(key, value) {
      var data = this.__data__;
      this.size += this.has(key) ? 0 : 1;
      data[key] = nativeCreate && value === void 0 ? HASH_UNDEFINED : value;
      return this;
    }
    Hash.prototype.clear = hashClear;
    Hash.prototype["delete"] = hashDelete;
    Hash.prototype.get = hashGet;
    Hash.prototype.has = hashHas;
    Hash.prototype.set = hashSet;
    function ListCache(entries) {
      var index = -1, length2 = entries == null ? 0 : entries.length;
      this.clear();
      while (++index < length2) {
        var entry = entries[index];
        this.set(entry[0], entry[1]);
      }
    }
    function listCacheClear() {
      this.__data__ = [];
      this.size = 0;
    }
    function listCacheDelete(key) {
      var data = this.__data__, index = assocIndexOf(data, key);
      if (index < 0) {
        return false;
      }
      var lastIndex = data.length - 1;
      if (index == lastIndex) {
        data.pop();
      } else {
        splice.call(data, index, 1);
      }
      --this.size;
      return true;
    }
    function listCacheGet(key) {
      var data = this.__data__, index = assocIndexOf(data, key);
      return index < 0 ? void 0 : data[index][1];
    }
    function listCacheHas(key) {
      return assocIndexOf(this.__data__, key) > -1;
    }
    function listCacheSet(key, value) {
      var data = this.__data__, index = assocIndexOf(data, key);
      if (index < 0) {
        ++this.size;
        data.push([key, value]);
      } else {
        data[index][1] = value;
      }
      return this;
    }
    ListCache.prototype.clear = listCacheClear;
    ListCache.prototype["delete"] = listCacheDelete;
    ListCache.prototype.get = listCacheGet;
    ListCache.prototype.has = listCacheHas;
    ListCache.prototype.set = listCacheSet;
    function MapCache(entries) {
      var index = -1, length2 = entries == null ? 0 : entries.length;
      this.clear();
      while (++index < length2) {
        var entry = entries[index];
        this.set(entry[0], entry[1]);
      }
    }
    function mapCacheClear() {
      this.size = 0;
      this.__data__ = {
        "hash": new Hash(),
        "map": new (Map2 || ListCache)(),
        "string": new Hash()
      };
    }
    function mapCacheDelete(key) {
      var result = getMapData(this, key)["delete"](key);
      this.size -= result ? 1 : 0;
      return result;
    }
    function mapCacheGet(key) {
      return getMapData(this, key).get(key);
    }
    function mapCacheHas(key) {
      return getMapData(this, key).has(key);
    }
    function mapCacheSet(key, value) {
      var data = getMapData(this, key), size2 = data.size;
      data.set(key, value);
      this.size += data.size == size2 ? 0 : 1;
      return this;
    }
    MapCache.prototype.clear = mapCacheClear;
    MapCache.prototype["delete"] = mapCacheDelete;
    MapCache.prototype.get = mapCacheGet;
    MapCache.prototype.has = mapCacheHas;
    MapCache.prototype.set = mapCacheSet;
    function Stack(entries) {
      var data = this.__data__ = new ListCache(entries);
      this.size = data.size;
    }
    function stackClear() {
      this.__data__ = new ListCache();
      this.size = 0;
    }
    function stackDelete(key) {
      var data = this.__data__, result = data["delete"](key);
      this.size = data.size;
      return result;
    }
    function stackGet(key) {
      return this.__data__.get(key);
    }
    function stackHas(key) {
      return this.__data__.has(key);
    }
    function stackSet(key, value) {
      var data = this.__data__;
      if (data instanceof ListCache) {
        var pairs = data.__data__;
        if (!Map2 || pairs.length < LARGE_ARRAY_SIZE - 1) {
          pairs.push([key, value]);
          this.size = ++data.size;
          return this;
        }
        data = this.__data__ = new MapCache(pairs);
      }
      data.set(key, value);
      this.size = data.size;
      return this;
    }
    Stack.prototype.clear = stackClear;
    Stack.prototype["delete"] = stackDelete;
    Stack.prototype.get = stackGet;
    Stack.prototype.has = stackHas;
    Stack.prototype.set = stackSet;
    function arrayLikeKeys(value, inherited) {
      var isArr = isArray(value), isArg = !isArr && isArguments(value), isBuff = !isArr && !isArg && isBuffer(value), isType = !isArr && !isArg && !isBuff && isTypedArray(value), skipIndexes = isArr || isArg || isBuff || isType, result = skipIndexes ? baseTimes(value.length, String) : [], length2 = result.length;
      for (var key in value) {
        if (!(skipIndexes && // Safari 9 has enumerable `arguments.length` in strict mode.
        (key == "length" || // Node.js 0.10 has enumerable non-index properties on buffers.
        isBuff && (key == "offset" || key == "parent") || // PhantomJS 2 has enumerable non-index properties on typed arrays.
        isType && (key == "buffer" || key == "byteLength" || key == "byteOffset") || // Skip index properties.
        isIndex(key, length2)))) {
          result.push(key);
        }
      }
      return result;
    }
    function assignMergeValue(object, key, value) {
      if (value !== void 0 && !eq(object[key], value) || value === void 0 && !(key in object)) {
        baseAssignValue(object, key, value);
      }
    }
    function assignValue(object, key, value) {
      var objValue = object[key];
      if (!(hasOwnProperty.call(object, key) && eq(objValue, value)) || value === void 0 && !(key in object)) {
        baseAssignValue(object, key, value);
      }
    }
    function assocIndexOf(array, key) {
      var length2 = array.length;
      while (length2--) {
        if (eq(array[length2][0], key)) {
          return length2;
        }
      }
      return -1;
    }
    function baseAssignValue(object, key, value) {
      if (key == "__proto__" && defineProperty) {
        defineProperty(object, key, {
          "configurable": true,
          "enumerable": true,
          "value": value,
          "writable": true
        });
      } else {
        object[key] = value;
      }
    }
    var baseFor = createBaseFor();
    function baseGetTag(value) {
      if (value == null) {
        return value === void 0 ? undefinedTag : nullTag;
      }
      return symToStringTag && symToStringTag in Object(value) ? getRawTag(value) : objectToString(value);
    }
    function baseIsArguments(value) {
      return isObjectLike(value) && baseGetTag(value) == argsTag;
    }
    function baseIsNative(value) {
      if (!isObject2(value) || isMasked(value)) {
        return false;
      }
      var pattern = isFunction2(value) ? reIsNative : reIsHostCtor;
      return pattern.test(toSource(value));
    }
    function baseIsTypedArray(value) {
      return isObjectLike(value) && isLength(value.length) && !!typedArrayTags[baseGetTag(value)];
    }
    function baseKeysIn(object) {
      if (!isObject2(object)) {
        return nativeKeysIn(object);
      }
      var isProto = isPrototype(object), result = [];
      for (var key in object) {
        if (!(key == "constructor" && (isProto || !hasOwnProperty.call(object, key)))) {
          result.push(key);
        }
      }
      return result;
    }
    function baseMerge(object, source, srcIndex, customizer, stack) {
      if (object === source) {
        return;
      }
      baseFor(source, function(srcValue, key) {
        stack || (stack = new Stack());
        if (isObject2(srcValue)) {
          baseMergeDeep(object, source, key, srcIndex, baseMerge, customizer, stack);
        } else {
          var newValue = customizer ? customizer(safeGet(object, key), srcValue, key + "", object, source, stack) : void 0;
          if (newValue === void 0) {
            newValue = srcValue;
          }
          assignMergeValue(object, key, newValue);
        }
      }, keysIn);
    }
    function baseMergeDeep(object, source, key, srcIndex, mergeFunc, customizer, stack) {
      var objValue = safeGet(object, key), srcValue = safeGet(source, key), stacked = stack.get(srcValue);
      if (stacked) {
        assignMergeValue(object, key, stacked);
        return;
      }
      var newValue = customizer ? customizer(objValue, srcValue, key + "", object, source, stack) : void 0;
      var isCommon = newValue === void 0;
      if (isCommon) {
        var isArr = isArray(srcValue), isBuff = !isArr && isBuffer(srcValue), isTyped = !isArr && !isBuff && isTypedArray(srcValue);
        newValue = srcValue;
        if (isArr || isBuff || isTyped) {
          if (isArray(objValue)) {
            newValue = objValue;
          } else if (isArrayLikeObject(objValue)) {
            newValue = copyArray(objValue);
          } else if (isBuff) {
            isCommon = false;
            newValue = cloneBuffer(srcValue);
          } else if (isTyped) {
            isCommon = false;
            newValue = cloneTypedArray(srcValue);
          } else {
            newValue = [];
          }
        } else if (isPlainObject(srcValue) || isArguments(srcValue)) {
          newValue = objValue;
          if (isArguments(objValue)) {
            newValue = toPlainObject(objValue);
          } else if (!isObject2(objValue) || isFunction2(objValue)) {
            newValue = initCloneObject(srcValue);
          }
        } else {
          isCommon = false;
        }
      }
      if (isCommon) {
        stack.set(srcValue, newValue);
        mergeFunc(newValue, srcValue, srcIndex, customizer, stack);
        stack["delete"](srcValue);
      }
      assignMergeValue(object, key, newValue);
    }
    function baseRest(func, start) {
      return setToString(overRest(func, start, identity), func + "");
    }
    var baseSetToString = !defineProperty ? identity : function(func, string) {
      return defineProperty(func, "toString", {
        "configurable": true,
        "enumerable": false,
        "value": constant(string),
        "writable": true
      });
    };
    function cloneBuffer(buffer, isDeep) {
      {
        return buffer.slice();
      }
    }
    function cloneArrayBuffer(arrayBuffer) {
      var result = new arrayBuffer.constructor(arrayBuffer.byteLength);
      new Uint8Array(result).set(new Uint8Array(arrayBuffer));
      return result;
    }
    function cloneTypedArray(typedArray, isDeep) {
      var buffer = cloneArrayBuffer(typedArray.buffer);
      return new typedArray.constructor(buffer, typedArray.byteOffset, typedArray.length);
    }
    function copyArray(source, array) {
      var index = -1, length2 = source.length;
      array || (array = Array(length2));
      while (++index < length2) {
        array[index] = source[index];
      }
      return array;
    }
    function copyObject(source, props, object, customizer) {
      var isNew = !object;
      object || (object = {});
      var index = -1, length2 = props.length;
      while (++index < length2) {
        var key = props[index];
        var newValue = void 0;
        if (newValue === void 0) {
          newValue = source[key];
        }
        if (isNew) {
          baseAssignValue(object, key, newValue);
        } else {
          assignValue(object, key, newValue);
        }
      }
      return object;
    }
    function createAssigner(assigner) {
      return baseRest(function(object, sources) {
        var index = -1, length2 = sources.length, customizer = length2 > 1 ? sources[length2 - 1] : void 0, guard2 = length2 > 2 ? sources[2] : void 0;
        customizer = assigner.length > 3 && typeof customizer == "function" ? (length2--, customizer) : void 0;
        if (guard2 && isIterateeCall(sources[0], sources[1], guard2)) {
          customizer = length2 < 3 ? void 0 : customizer;
          length2 = 1;
        }
        object = Object(object);
        while (++index < length2) {
          var source = sources[index];
          if (source) {
            assigner(object, source, index, customizer);
          }
        }
        return object;
      });
    }
    function createBaseFor(fromRight) {
      return function(object, iteratee, keysFunc) {
        var index = -1, iterable = Object(object), props = keysFunc(object), length2 = props.length;
        while (length2--) {
          var key = props[++index];
          if (iteratee(iterable[key], key, iterable) === false) {
            break;
          }
        }
        return object;
      };
    }
    function getMapData(map, key) {
      var data = map.__data__;
      return isKeyable(key) ? data[typeof key == "string" ? "string" : "hash"] : data.map;
    }
    function getNative(object, key) {
      var value = getValue(object, key);
      return baseIsNative(value) ? value : void 0;
    }
    function getRawTag(value) {
      var isOwn = hasOwnProperty.call(value, symToStringTag), tag = value[symToStringTag];
      try {
        value[symToStringTag] = void 0;
        var unmasked = true;
      } catch (e2) {
      }
      var result = nativeObjectToString.call(value);
      if (unmasked) {
        if (isOwn) {
          value[symToStringTag] = tag;
        } else {
          delete value[symToStringTag];
        }
      }
      return result;
    }
    function initCloneObject(object) {
      return typeof object.constructor == "function" && !isPrototype(object) ? baseCreate(getPrototype(object)) : {};
    }
    function isIndex(value, length2) {
      var type = typeof value;
      length2 = length2 == null ? MAX_SAFE_INTEGER : length2;
      return !!length2 && (type == "number" || type != "symbol" && reIsUint.test(value)) && (value > -1 && value % 1 == 0 && value < length2);
    }
    function isIterateeCall(value, index, object) {
      if (!isObject2(object)) {
        return false;
      }
      var type = typeof index;
      if (type == "number" ? isArrayLike(object) && isIndex(index, object.length) : type == "string" && index in object) {
        return eq(object[index], value);
      }
      return false;
    }
    function isKeyable(value) {
      var type = typeof value;
      return type == "string" || type == "number" || type == "symbol" || type == "boolean" ? value !== "__proto__" : value === null;
    }
    function isMasked(func) {
      return !!maskSrcKey && maskSrcKey in func;
    }
    function isPrototype(value) {
      var Ctor = value && value.constructor, proto = typeof Ctor == "function" && Ctor.prototype || objectProto;
      return value === proto;
    }
    function nativeKeysIn(object) {
      var result = [];
      if (object != null) {
        for (var key in Object(object)) {
          result.push(key);
        }
      }
      return result;
    }
    function objectToString(value) {
      return nativeObjectToString.call(value);
    }
    function overRest(func, start, transform2) {
      start = nativeMax(start === void 0 ? func.length - 1 : start, 0);
      return function() {
        var args = arguments, index = -1, length2 = nativeMax(args.length - start, 0), array = Array(length2);
        while (++index < length2) {
          array[index] = args[start + index];
        }
        index = -1;
        var otherArgs = Array(start + 1);
        while (++index < start) {
          otherArgs[index] = args[index];
        }
        otherArgs[start] = transform2(array);
        return apply(func, this, otherArgs);
      };
    }
    function safeGet(object, key) {
      if (key === "constructor" && typeof object[key] === "function") {
        return;
      }
      if (key == "__proto__") {
        return;
      }
      return object[key];
    }
    var setToString = shortOut(baseSetToString);
    function shortOut(func) {
      var count = 0, lastCalled = 0;
      return function() {
        var stamp = nativeNow(), remaining = HOT_SPAN - (stamp - lastCalled);
        lastCalled = stamp;
        if (remaining > 0) {
          if (++count >= HOT_COUNT) {
            return arguments[0];
          }
        } else {
          count = 0;
        }
        return func.apply(void 0, arguments);
      };
    }
    function toSource(func) {
      if (func != null) {
        try {
          return funcToString.call(func);
        } catch (e2) {
        }
        try {
          return func + "";
        } catch (e2) {
        }
      }
      return "";
    }
    function eq(value, other) {
      return value === other || value !== value && other !== other;
    }
    var isArguments = baseIsArguments(/* @__PURE__ */ function() {
      return arguments;
    }()) ? baseIsArguments : function(value) {
      return isObjectLike(value) && hasOwnProperty.call(value, "callee") && !propertyIsEnumerable.call(value, "callee");
    };
    var isArray = Array.isArray;
    function isArrayLike(value) {
      return value != null && isLength(value.length) && !isFunction2(value);
    }
    function isArrayLikeObject(value) {
      return isObjectLike(value) && isArrayLike(value);
    }
    var isBuffer = nativeIsBuffer || stubFalse;
    function isFunction2(value) {
      if (!isObject2(value)) {
        return false;
      }
      var tag = baseGetTag(value);
      return tag == funcTag || tag == genTag || tag == asyncTag || tag == proxyTag;
    }
    function isLength(value) {
      return typeof value == "number" && value > -1 && value % 1 == 0 && value <= MAX_SAFE_INTEGER;
    }
    function isObject2(value) {
      var type = typeof value;
      return value != null && (type == "object" || type == "function");
    }
    function isObjectLike(value) {
      return value != null && typeof value == "object";
    }
    function isPlainObject(value) {
      if (!isObjectLike(value) || baseGetTag(value) != objectTag) {
        return false;
      }
      var proto = getPrototype(value);
      if (proto === null) {
        return true;
      }
      var Ctor = hasOwnProperty.call(proto, "constructor") && proto.constructor;
      return typeof Ctor == "function" && Ctor instanceof Ctor && funcToString.call(Ctor) == objectCtorString;
    }
    var isTypedArray = nodeIsTypedArray ? baseUnary(nodeIsTypedArray) : baseIsTypedArray;
    function toPlainObject(value) {
      return copyObject(value, keysIn(value));
    }
    function keysIn(object) {
      return isArrayLike(object) ? arrayLikeKeys(object) : baseKeysIn(object);
    }
    var mergeWith2 = createAssigner(function(object, source, srcIndex, customizer) {
      baseMerge(object, source, srcIndex, customizer);
    });
    function constant(value) {
      return function() {
        return value;
      };
    }
    function identity(value) {
      return value;
    }
    function stubFalse() {
      return false;
    }
    module.exports = mergeWith2;
  })(lodash_mergewith, lodash_mergewith.exports);
  var lodash_mergewithExports = lodash_mergewith.exports;
  const mergeWith = /* @__PURE__ */ getDefaultExportFromCjs(lodash_mergewithExports);
  var isImportant = (value) => /!(important)?$/.test(value);
  var withoutImportant = (value) => typeof value === "string" ? value.replace(/!(important)?$/, "").trim() : value;
  var tokenToCSSVar = (scale2, value) => (theme2) => {
    const valueStr = String(value);
    const important = isImportant(valueStr);
    const valueWithoutImportant = withoutImportant(valueStr);
    const key = scale2 ? `${scale2}.${valueWithoutImportant}` : valueWithoutImportant;
    let transformed = isObject(theme2.__cssMap) && key in theme2.__cssMap ? theme2.__cssMap[key].varRef : value;
    transformed = withoutImportant(transformed);
    return important ? `${transformed} !important` : transformed;
  };
  function createTransform(options) {
    const { scale: scale2, transform: transform2, compose } = options;
    const fn = (value, theme2) => {
      var _a4;
      const _value = tokenToCSSVar(scale2, value)(theme2);
      let result = (_a4 = transform2 == null ? void 0 : transform2(_value, theme2)) != null ? _a4 : _value;
      if (compose) {
        result = compose(result, theme2);
      }
      return result;
    };
    return fn;
  }
  var pipe$2 = (...fns) => (v2) => fns.reduce((a, b2) => b2(a), v2);
  function toConfig(scale2, transform2) {
    return (property) => {
      const result = { property, scale: scale2 };
      result.transform = createTransform({
        scale: scale2,
        transform: transform2
      });
      return result;
    };
  }
  var getRtl = ({ rtl, ltr }) => (theme2) => theme2.direction === "rtl" ? rtl : ltr;
  function logical(options) {
    const { property, scale: scale2, transform: transform2 } = options;
    return {
      scale: scale2,
      property: getRtl(property),
      transform: scale2 ? createTransform({
        scale: scale2,
        compose: transform2
      }) : transform2
    };
  }
  var transformTemplate = [
    "rotate(var(--chakra-rotate, 0))",
    "scaleX(var(--chakra-scale-x, 1))",
    "scaleY(var(--chakra-scale-y, 1))",
    "skewX(var(--chakra-skew-x, 0))",
    "skewY(var(--chakra-skew-y, 0))"
  ];
  function getTransformTemplate() {
    return [
      "translateX(var(--chakra-translate-x, 0))",
      "translateY(var(--chakra-translate-y, 0))",
      ...transformTemplate
    ].join(" ");
  }
  function getTransformGpuTemplate() {
    return [
      "translate3d(var(--chakra-translate-x, 0), var(--chakra-translate-y, 0), 0)",
      ...transformTemplate
    ].join(" ");
  }
  var filterTemplate = {
    "--chakra-blur": "var(--chakra-empty,/*!*/ /*!*/)",
    "--chakra-brightness": "var(--chakra-empty,/*!*/ /*!*/)",
    "--chakra-contrast": "var(--chakra-empty,/*!*/ /*!*/)",
    "--chakra-grayscale": "var(--chakra-empty,/*!*/ /*!*/)",
    "--chakra-hue-rotate": "var(--chakra-empty,/*!*/ /*!*/)",
    "--chakra-invert": "var(--chakra-empty,/*!*/ /*!*/)",
    "--chakra-saturate": "var(--chakra-empty,/*!*/ /*!*/)",
    "--chakra-sepia": "var(--chakra-empty,/*!*/ /*!*/)",
    "--chakra-drop-shadow": "var(--chakra-empty,/*!*/ /*!*/)",
    filter: [
      "var(--chakra-blur)",
      "var(--chakra-brightness)",
      "var(--chakra-contrast)",
      "var(--chakra-grayscale)",
      "var(--chakra-hue-rotate)",
      "var(--chakra-invert)",
      "var(--chakra-saturate)",
      "var(--chakra-sepia)",
      "var(--chakra-drop-shadow)"
    ].join(" ")
  };
  var backdropFilterTemplate = {
    backdropFilter: [
      "var(--chakra-backdrop-blur)",
      "var(--chakra-backdrop-brightness)",
      "var(--chakra-backdrop-contrast)",
      "var(--chakra-backdrop-grayscale)",
      "var(--chakra-backdrop-hue-rotate)",
      "var(--chakra-backdrop-invert)",
      "var(--chakra-backdrop-opacity)",
      "var(--chakra-backdrop-saturate)",
      "var(--chakra-backdrop-sepia)"
    ].join(" "),
    "--chakra-backdrop-blur": "var(--chakra-empty,/*!*/ /*!*/)",
    "--chakra-backdrop-brightness": "var(--chakra-empty,/*!*/ /*!*/)",
    "--chakra-backdrop-contrast": "var(--chakra-empty,/*!*/ /*!*/)",
    "--chakra-backdrop-grayscale": "var(--chakra-empty,/*!*/ /*!*/)",
    "--chakra-backdrop-hue-rotate": "var(--chakra-empty,/*!*/ /*!*/)",
    "--chakra-backdrop-invert": "var(--chakra-empty,/*!*/ /*!*/)",
    "--chakra-backdrop-opacity": "var(--chakra-empty,/*!*/ /*!*/)",
    "--chakra-backdrop-saturate": "var(--chakra-empty,/*!*/ /*!*/)",
    "--chakra-backdrop-sepia": "var(--chakra-empty,/*!*/ /*!*/)"
  };
  function getRingTemplate(value) {
    return {
      "--chakra-ring-offset-shadow": `var(--chakra-ring-inset) 0 0 0 var(--chakra-ring-offset-width) var(--chakra-ring-offset-color)`,
      "--chakra-ring-shadow": `var(--chakra-ring-inset) 0 0 0 calc(var(--chakra-ring-width) + var(--chakra-ring-offset-width)) var(--chakra-ring-color)`,
      "--chakra-ring-width": value,
      boxShadow: [
        `var(--chakra-ring-offset-shadow)`,
        `var(--chakra-ring-shadow)`,
        `var(--chakra-shadow, 0 0 #0000)`
      ].join(", ")
    };
  }
  var flexDirectionTemplate = {
    "row-reverse": {
      space: "--chakra-space-x-reverse",
      divide: "--chakra-divide-x-reverse"
    },
    "column-reverse": {
      space: "--chakra-space-y-reverse",
      divide: "--chakra-divide-y-reverse"
    }
  };
  var directionMap = {
    "to-t": "to top",
    "to-tr": "to top right",
    "to-r": "to right",
    "to-br": "to bottom right",
    "to-b": "to bottom",
    "to-bl": "to bottom left",
    "to-l": "to left",
    "to-tl": "to top left"
  };
  var valueSet = new Set(Object.values(directionMap));
  var globalSet = /* @__PURE__ */ new Set([
    "none",
    "-moz-initial",
    "inherit",
    "initial",
    "revert",
    "unset"
  ]);
  var trimSpace = (str) => str.trim();
  function parseGradient(value, theme2) {
    if (value == null || globalSet.has(value))
      return value;
    const prevent = isCSSFunction(value) || globalSet.has(value);
    if (!prevent)
      return `url('${value}')`;
    const regex = /(^[a-z-A-Z]+)\((.*)\)/g;
    const results = regex.exec(value);
    const type = results == null ? void 0 : results[1];
    const values = results == null ? void 0 : results[2];
    if (!type || !values)
      return value;
    const _type = type.includes("-gradient") ? type : `${type}-gradient`;
    const [maybeDirection, ...stops] = values.split(",").map(trimSpace).filter(Boolean);
    if ((stops == null ? void 0 : stops.length) === 0)
      return value;
    const direction2 = maybeDirection in directionMap ? directionMap[maybeDirection] : maybeDirection;
    stops.unshift(direction2);
    const _values = stops.map((stop) => {
      if (valueSet.has(stop))
        return stop;
      const firstStop = stop.indexOf(" ");
      const [_color, _stop] = firstStop !== -1 ? [stop.substr(0, firstStop), stop.substr(firstStop + 1)] : [stop];
      const _stopOrFunc = isCSSFunction(_stop) ? _stop : _stop && _stop.split(" ");
      const key = `colors.${_color}`;
      const color2 = key in theme2.__cssMap ? theme2.__cssMap[key].varRef : _color;
      return _stopOrFunc ? [
        color2,
        ...Array.isArray(_stopOrFunc) ? _stopOrFunc : [_stopOrFunc]
      ].join(" ") : color2;
    });
    return `${_type}(${_values.join(", ")})`;
  }
  var isCSSFunction = (value) => {
    return typeof value === "string" && value.includes("(") && value.includes(")");
  };
  var gradientTransform = (value, theme2) => parseGradient(value, theme2 != null ? theme2 : {});
  function isCssVar(value) {
    return /^var\(--.+\)$/.test(value);
  }
  var analyzeCSSValue = (value) => {
    const num = parseFloat(value.toString());
    const unit = value.toString().replace(String(num), "");
    return { unitless: !unit, value: num, unit };
  };
  var wrap = (str) => (value) => `${str}(${value})`;
  var transformFunctions = {
    filter(value) {
      return value !== "auto" ? value : filterTemplate;
    },
    backdropFilter(value) {
      return value !== "auto" ? value : backdropFilterTemplate;
    },
    ring(value) {
      return getRingTemplate(transformFunctions.px(value));
    },
    bgClip(value) {
      return value === "text" ? { color: "transparent", backgroundClip: "text" } : { backgroundClip: value };
    },
    transform(value) {
      if (value === "auto")
        return getTransformTemplate();
      if (value === "auto-gpu")
        return getTransformGpuTemplate();
      return value;
    },
    vh(value) {
      return value === "$100vh" ? "var(--chakra-vh)" : value;
    },
    px(value) {
      if (value == null)
        return value;
      const { unitless } = analyzeCSSValue(value);
      return unitless || typeof value === "number" ? `${value}px` : value;
    },
    fraction(value) {
      return !(typeof value === "number") || value > 1 ? value : `${value * 100}%`;
    },
    float(value, theme2) {
      const map = { left: "right", right: "left" };
      return theme2.direction === "rtl" ? map[value] : value;
    },
    degree(value) {
      if (isCssVar(value) || value == null)
        return value;
      const unitless = typeof value === "string" && !value.endsWith("deg");
      return typeof value === "number" || unitless ? `${value}deg` : value;
    },
    gradient: gradientTransform,
    blur: wrap("blur"),
    opacity: wrap("opacity"),
    brightness: wrap("brightness"),
    contrast: wrap("contrast"),
    dropShadow: wrap("drop-shadow"),
    grayscale: wrap("grayscale"),
    hueRotate: (value) => wrap("hue-rotate")(transformFunctions.degree(value)),
    invert: wrap("invert"),
    saturate: wrap("saturate"),
    sepia: wrap("sepia"),
    bgImage(value) {
      if (value == null)
        return value;
      const prevent = isCSSFunction(value) || globalSet.has(value);
      return !prevent ? `url(${value})` : value;
    },
    outline(value) {
      const isNoneOrZero = String(value) === "0" || String(value) === "none";
      return value !== null && isNoneOrZero ? { outline: "2px solid transparent", outlineOffset: "2px" } : { outline: value };
    },
    flexDirection(value) {
      var _a4;
      const { space: space2, divide: divide2 } = (_a4 = flexDirectionTemplate[value]) != null ? _a4 : {};
      const result = { flexDirection: value };
      if (space2)
        result[space2] = 1;
      if (divide2)
        result[divide2] = 1;
      return result;
    }
  };
  var t = {
    borderWidths: toConfig("borderWidths"),
    borderStyles: toConfig("borderStyles"),
    colors: toConfig("colors"),
    borders: toConfig("borders"),
    gradients: toConfig("gradients", transformFunctions.gradient),
    radii: toConfig("radii", transformFunctions.px),
    space: toConfig("space", pipe$2(transformFunctions.vh, transformFunctions.px)),
    spaceT: toConfig("space", pipe$2(transformFunctions.vh, transformFunctions.px)),
    degreeT(property) {
      return { property, transform: transformFunctions.degree };
    },
    prop(property, scale2, transform2) {
      return {
        property,
        scale: scale2,
        ...scale2 && {
          transform: createTransform({ scale: scale2, transform: transform2 })
        }
      };
    },
    propT(property, transform2) {
      return { property, transform: transform2 };
    },
    sizes: toConfig("sizes", pipe$2(transformFunctions.vh, transformFunctions.px)),
    sizesT: toConfig("sizes", pipe$2(transformFunctions.vh, transformFunctions.fraction)),
    shadows: toConfig("shadows"),
    logical,
    blur: toConfig("blur", transformFunctions.blur)
  };
  var background = {
    background: t.colors("background"),
    backgroundColor: t.colors("backgroundColor"),
    backgroundImage: t.gradients("backgroundImage"),
    backgroundSize: true,
    backgroundPosition: true,
    backgroundRepeat: true,
    backgroundAttachment: true,
    backgroundClip: { transform: transformFunctions.bgClip },
    bgSize: t.prop("backgroundSize"),
    bgPosition: t.prop("backgroundPosition"),
    bg: t.colors("background"),
    bgColor: t.colors("backgroundColor"),
    bgPos: t.prop("backgroundPosition"),
    bgRepeat: t.prop("backgroundRepeat"),
    bgAttachment: t.prop("backgroundAttachment"),
    bgGradient: t.gradients("backgroundImage"),
    bgClip: { transform: transformFunctions.bgClip }
  };
  Object.assign(background, {
    bgImage: background.backgroundImage,
    bgImg: background.backgroundImage
  });
  var border = {
    border: t.borders("border"),
    borderWidth: t.borderWidths("borderWidth"),
    borderStyle: t.borderStyles("borderStyle"),
    borderColor: t.colors("borderColor"),
    borderRadius: t.radii("borderRadius"),
    borderTop: t.borders("borderTop"),
    borderBlockStart: t.borders("borderBlockStart"),
    borderTopLeftRadius: t.radii("borderTopLeftRadius"),
    borderStartStartRadius: t.logical({
      scale: "radii",
      property: {
        ltr: "borderTopLeftRadius",
        rtl: "borderTopRightRadius"
      }
    }),
    borderEndStartRadius: t.logical({
      scale: "radii",
      property: {
        ltr: "borderBottomLeftRadius",
        rtl: "borderBottomRightRadius"
      }
    }),
    borderTopRightRadius: t.radii("borderTopRightRadius"),
    borderStartEndRadius: t.logical({
      scale: "radii",
      property: {
        ltr: "borderTopRightRadius",
        rtl: "borderTopLeftRadius"
      }
    }),
    borderEndEndRadius: t.logical({
      scale: "radii",
      property: {
        ltr: "borderBottomRightRadius",
        rtl: "borderBottomLeftRadius"
      }
    }),
    borderRight: t.borders("borderRight"),
    borderInlineEnd: t.borders("borderInlineEnd"),
    borderBottom: t.borders("borderBottom"),
    borderBlockEnd: t.borders("borderBlockEnd"),
    borderBottomLeftRadius: t.radii("borderBottomLeftRadius"),
    borderBottomRightRadius: t.radii("borderBottomRightRadius"),
    borderLeft: t.borders("borderLeft"),
    borderInlineStart: {
      property: "borderInlineStart",
      scale: "borders"
    },
    borderInlineStartRadius: t.logical({
      scale: "radii",
      property: {
        ltr: ["borderTopLeftRadius", "borderBottomLeftRadius"],
        rtl: ["borderTopRightRadius", "borderBottomRightRadius"]
      }
    }),
    borderInlineEndRadius: t.logical({
      scale: "radii",
      property: {
        ltr: ["borderTopRightRadius", "borderBottomRightRadius"],
        rtl: ["borderTopLeftRadius", "borderBottomLeftRadius"]
      }
    }),
    borderX: t.borders(["borderLeft", "borderRight"]),
    borderInline: t.borders("borderInline"),
    borderY: t.borders(["borderTop", "borderBottom"]),
    borderBlock: t.borders("borderBlock"),
    borderTopWidth: t.borderWidths("borderTopWidth"),
    borderBlockStartWidth: t.borderWidths("borderBlockStartWidth"),
    borderTopColor: t.colors("borderTopColor"),
    borderBlockStartColor: t.colors("borderBlockStartColor"),
    borderTopStyle: t.borderStyles("borderTopStyle"),
    borderBlockStartStyle: t.borderStyles("borderBlockStartStyle"),
    borderBottomWidth: t.borderWidths("borderBottomWidth"),
    borderBlockEndWidth: t.borderWidths("borderBlockEndWidth"),
    borderBottomColor: t.colors("borderBottomColor"),
    borderBlockEndColor: t.colors("borderBlockEndColor"),
    borderBottomStyle: t.borderStyles("borderBottomStyle"),
    borderBlockEndStyle: t.borderStyles("borderBlockEndStyle"),
    borderLeftWidth: t.borderWidths("borderLeftWidth"),
    borderInlineStartWidth: t.borderWidths("borderInlineStartWidth"),
    borderLeftColor: t.colors("borderLeftColor"),
    borderInlineStartColor: t.colors("borderInlineStartColor"),
    borderLeftStyle: t.borderStyles("borderLeftStyle"),
    borderInlineStartStyle: t.borderStyles("borderInlineStartStyle"),
    borderRightWidth: t.borderWidths("borderRightWidth"),
    borderInlineEndWidth: t.borderWidths("borderInlineEndWidth"),
    borderRightColor: t.colors("borderRightColor"),
    borderInlineEndColor: t.colors("borderInlineEndColor"),
    borderRightStyle: t.borderStyles("borderRightStyle"),
    borderInlineEndStyle: t.borderStyles("borderInlineEndStyle"),
    borderTopRadius: t.radii(["borderTopLeftRadius", "borderTopRightRadius"]),
    borderBottomRadius: t.radii([
      "borderBottomLeftRadius",
      "borderBottomRightRadius"
    ]),
    borderLeftRadius: t.radii(["borderTopLeftRadius", "borderBottomLeftRadius"]),
    borderRightRadius: t.radii([
      "borderTopRightRadius",
      "borderBottomRightRadius"
    ])
  };
  Object.assign(border, {
    rounded: border.borderRadius,
    roundedTop: border.borderTopRadius,
    roundedTopLeft: border.borderTopLeftRadius,
    roundedTopRight: border.borderTopRightRadius,
    roundedTopStart: border.borderStartStartRadius,
    roundedTopEnd: border.borderStartEndRadius,
    roundedBottom: border.borderBottomRadius,
    roundedBottomLeft: border.borderBottomLeftRadius,
    roundedBottomRight: border.borderBottomRightRadius,
    roundedBottomStart: border.borderEndStartRadius,
    roundedBottomEnd: border.borderEndEndRadius,
    roundedLeft: border.borderLeftRadius,
    roundedRight: border.borderRightRadius,
    roundedStart: border.borderInlineStartRadius,
    roundedEnd: border.borderInlineEndRadius,
    borderStart: border.borderInlineStart,
    borderEnd: border.borderInlineEnd,
    borderTopStartRadius: border.borderStartStartRadius,
    borderTopEndRadius: border.borderStartEndRadius,
    borderBottomStartRadius: border.borderEndStartRadius,
    borderBottomEndRadius: border.borderEndEndRadius,
    borderStartRadius: border.borderInlineStartRadius,
    borderEndRadius: border.borderInlineEndRadius,
    borderStartWidth: border.borderInlineStartWidth,
    borderEndWidth: border.borderInlineEndWidth,
    borderStartColor: border.borderInlineStartColor,
    borderEndColor: border.borderInlineEndColor,
    borderStartStyle: border.borderInlineStartStyle,
    borderEndStyle: border.borderInlineEndStyle
  });
  var color$1 = {
    color: t.colors("color"),
    textColor: t.colors("color"),
    fill: t.colors("fill"),
    stroke: t.colors("stroke")
  };
  var effect = {
    boxShadow: t.shadows("boxShadow"),
    mixBlendMode: true,
    blendMode: t.prop("mixBlendMode"),
    backgroundBlendMode: true,
    bgBlendMode: t.prop("backgroundBlendMode"),
    opacity: true
  };
  Object.assign(effect, {
    shadow: effect.boxShadow
  });
  var filter$2 = {
    filter: { transform: transformFunctions.filter },
    blur: t.blur("--chakra-blur"),
    brightness: t.propT("--chakra-brightness", transformFunctions.brightness),
    contrast: t.propT("--chakra-contrast", transformFunctions.contrast),
    hueRotate: t.propT("--chakra-hue-rotate", transformFunctions.hueRotate),
    invert: t.propT("--chakra-invert", transformFunctions.invert),
    saturate: t.propT("--chakra-saturate", transformFunctions.saturate),
    dropShadow: t.propT("--chakra-drop-shadow", transformFunctions.dropShadow),
    backdropFilter: { transform: transformFunctions.backdropFilter },
    backdropBlur: t.blur("--chakra-backdrop-blur"),
    backdropBrightness: t.propT(
      "--chakra-backdrop-brightness",
      transformFunctions.brightness
    ),
    backdropContrast: t.propT("--chakra-backdrop-contrast", transformFunctions.contrast),
    backdropHueRotate: t.propT(
      "--chakra-backdrop-hue-rotate",
      transformFunctions.hueRotate
    ),
    backdropInvert: t.propT("--chakra-backdrop-invert", transformFunctions.invert),
    backdropSaturate: t.propT("--chakra-backdrop-saturate", transformFunctions.saturate)
  };
  var flexbox = {
    alignItems: true,
    alignContent: true,
    justifyItems: true,
    justifyContent: true,
    flexWrap: true,
    flexDirection: { transform: transformFunctions.flexDirection },
    flex: true,
    flexFlow: true,
    flexGrow: true,
    flexShrink: true,
    flexBasis: t.sizes("flexBasis"),
    justifySelf: true,
    alignSelf: true,
    order: true,
    placeItems: true,
    placeContent: true,
    placeSelf: true,
    gap: t.space("gap"),
    rowGap: t.space("rowGap"),
    columnGap: t.space("columnGap")
  };
  Object.assign(flexbox, {
    flexDir: flexbox.flexDirection
  });
  var grid = {
    gridGap: t.space("gridGap"),
    gridColumnGap: t.space("gridColumnGap"),
    gridRowGap: t.space("gridRowGap"),
    gridColumn: true,
    gridRow: true,
    gridAutoFlow: true,
    gridAutoColumns: true,
    gridColumnStart: true,
    gridColumnEnd: true,
    gridRowStart: true,
    gridRowEnd: true,
    gridAutoRows: true,
    gridTemplate: true,
    gridTemplateColumns: true,
    gridTemplateRows: true,
    gridTemplateAreas: true,
    gridArea: true
  };
  var interactivity = {
    appearance: true,
    cursor: true,
    resize: true,
    userSelect: true,
    pointerEvents: true,
    outline: { transform: transformFunctions.outline },
    outlineOffset: true,
    outlineColor: t.colors("outlineColor")
  };
  var layout$1 = {
    width: t.sizesT("width"),
    inlineSize: t.sizesT("inlineSize"),
    height: t.sizes("height"),
    blockSize: t.sizes("blockSize"),
    boxSize: t.sizes(["width", "height"]),
    minWidth: t.sizes("minWidth"),
    minInlineSize: t.sizes("minInlineSize"),
    minHeight: t.sizes("minHeight"),
    minBlockSize: t.sizes("minBlockSize"),
    maxWidth: t.sizes("maxWidth"),
    maxInlineSize: t.sizes("maxInlineSize"),
    maxHeight: t.sizes("maxHeight"),
    maxBlockSize: t.sizes("maxBlockSize"),
    overflow: true,
    overflowX: true,
    overflowY: true,
    overscrollBehavior: true,
    overscrollBehaviorX: true,
    overscrollBehaviorY: true,
    display: true,
    aspectRatio: true,
    hideFrom: {
      scale: "breakpoints",
      transform: (value, theme2) => {
        var _a4, _b3, _c2;
        const breakpoint = (_c2 = (_b3 = (_a4 = theme2.__breakpoints) == null ? void 0 : _a4.get(value)) == null ? void 0 : _b3.minW) != null ? _c2 : value;
        const mq = `@media screen and (min-width: ${breakpoint})`;
        return { [mq]: { display: "none" } };
      }
    },
    hideBelow: {
      scale: "breakpoints",
      transform: (value, theme2) => {
        var _a4, _b3, _c2;
        const breakpoint = (_c2 = (_b3 = (_a4 = theme2.__breakpoints) == null ? void 0 : _a4.get(value)) == null ? void 0 : _b3._minW) != null ? _c2 : value;
        const mq = `@media screen and (max-width: ${breakpoint})`;
        return { [mq]: { display: "none" } };
      }
    },
    verticalAlign: true,
    boxSizing: true,
    boxDecorationBreak: true,
    float: t.propT("float", transformFunctions.float),
    objectFit: true,
    objectPosition: true,
    visibility: true,
    isolation: true
  };
  Object.assign(layout$1, {
    w: layout$1.width,
    h: layout$1.height,
    minW: layout$1.minWidth,
    maxW: layout$1.maxWidth,
    minH: layout$1.minHeight,
    maxH: layout$1.maxHeight,
    overscroll: layout$1.overscrollBehavior,
    overscrollX: layout$1.overscrollBehaviorX,
    overscrollY: layout$1.overscrollBehaviorY
  });
  var list = {
    listStyleType: true,
    listStylePosition: true,
    listStylePos: t.prop("listStylePosition"),
    listStyleImage: true,
    listStyleImg: t.prop("listStyleImage")
  };
  function get$1(obj, path, fallback, index) {
    const key = typeof path === "string" ? path.split(".") : [path];
    for (index = 0; index < key.length; index += 1) {
      if (!obj)
        break;
      obj = obj[key[index]];
    }
    return obj === void 0 ? fallback : obj;
  }
  var memoize$1 = (fn) => {
    const cache = /* @__PURE__ */ new WeakMap();
    const memoizedFn = (obj, path, fallback, index) => {
      if (typeof obj === "undefined") {
        return fn(obj, path, fallback);
      }
      if (!cache.has(obj)) {
        cache.set(obj, /* @__PURE__ */ new Map());
      }
      const map = cache.get(obj);
      if (map.has(path)) {
        return map.get(path);
      }
      const value = fn(obj, path, fallback, index);
      map.set(path, value);
      return value;
    };
    return memoizedFn;
  };
  var memoizedGet$1 = memoize$1(get$1);
  var srOnly = {
    border: "0px",
    clip: "rect(0, 0, 0, 0)",
    width: "1px",
    height: "1px",
    margin: "-1px",
    padding: "0px",
    overflow: "hidden",
    whiteSpace: "nowrap",
    position: "absolute"
  };
  var srFocusable = {
    position: "static",
    width: "auto",
    height: "auto",
    clip: "auto",
    padding: "0",
    margin: "0",
    overflow: "visible",
    whiteSpace: "normal"
  };
  var getWithPriority = (theme2, key, styles2) => {
    const result = {};
    const obj = memoizedGet$1(theme2, key, {});
    for (const prop in obj) {
      const isInStyles = prop in styles2 && styles2[prop] != null;
      if (!isInStyles)
        result[prop] = obj[prop];
    }
    return result;
  };
  var others = {
    srOnly: {
      transform(value) {
        if (value === true)
          return srOnly;
        if (value === "focusable")
          return srFocusable;
        return {};
      }
    },
    layerStyle: {
      processResult: true,
      transform: (value, theme2, styles2) => getWithPriority(theme2, `layerStyles.${value}`, styles2)
    },
    textStyle: {
      processResult: true,
      transform: (value, theme2, styles2) => getWithPriority(theme2, `textStyles.${value}`, styles2)
    },
    apply: {
      processResult: true,
      transform: (value, theme2, styles2) => getWithPriority(theme2, value, styles2)
    }
  };
  var position$1 = {
    position: true,
    pos: t.prop("position"),
    zIndex: t.prop("zIndex", "zIndices"),
    inset: t.spaceT("inset"),
    insetX: t.spaceT(["left", "right"]),
    insetInline: t.spaceT("insetInline"),
    insetY: t.spaceT(["top", "bottom"]),
    insetBlock: t.spaceT("insetBlock"),
    top: t.spaceT("top"),
    insetBlockStart: t.spaceT("insetBlockStart"),
    bottom: t.spaceT("bottom"),
    insetBlockEnd: t.spaceT("insetBlockEnd"),
    left: t.spaceT("left"),
    insetInlineStart: t.logical({
      scale: "space",
      property: { ltr: "left", rtl: "right" }
    }),
    right: t.spaceT("right"),
    insetInlineEnd: t.logical({
      scale: "space",
      property: { ltr: "right", rtl: "left" }
    })
  };
  Object.assign(position$1, {
    insetStart: position$1.insetInlineStart,
    insetEnd: position$1.insetInlineEnd
  });
  var ring = {
    ring: { transform: transformFunctions.ring },
    ringColor: t.colors("--chakra-ring-color"),
    ringOffset: t.prop("--chakra-ring-offset-width"),
    ringOffsetColor: t.colors("--chakra-ring-offset-color"),
    ringInset: t.prop("--chakra-ring-inset")
  };
  var space = {
    margin: t.spaceT("margin"),
    marginTop: t.spaceT("marginTop"),
    marginBlockStart: t.spaceT("marginBlockStart"),
    marginRight: t.spaceT("marginRight"),
    marginInlineEnd: t.spaceT("marginInlineEnd"),
    marginBottom: t.spaceT("marginBottom"),
    marginBlockEnd: t.spaceT("marginBlockEnd"),
    marginLeft: t.spaceT("marginLeft"),
    marginInlineStart: t.spaceT("marginInlineStart"),
    marginX: t.spaceT(["marginInlineStart", "marginInlineEnd"]),
    marginInline: t.spaceT("marginInline"),
    marginY: t.spaceT(["marginTop", "marginBottom"]),
    marginBlock: t.spaceT("marginBlock"),
    padding: t.space("padding"),
    paddingTop: t.space("paddingTop"),
    paddingBlockStart: t.space("paddingBlockStart"),
    paddingRight: t.space("paddingRight"),
    paddingBottom: t.space("paddingBottom"),
    paddingBlockEnd: t.space("paddingBlockEnd"),
    paddingLeft: t.space("paddingLeft"),
    paddingInlineStart: t.space("paddingInlineStart"),
    paddingInlineEnd: t.space("paddingInlineEnd"),
    paddingX: t.space(["paddingInlineStart", "paddingInlineEnd"]),
    paddingInline: t.space("paddingInline"),
    paddingY: t.space(["paddingTop", "paddingBottom"]),
    paddingBlock: t.space("paddingBlock")
  };
  Object.assign(space, {
    m: space.margin,
    mt: space.marginTop,
    mr: space.marginRight,
    me: space.marginInlineEnd,
    marginEnd: space.marginInlineEnd,
    mb: space.marginBottom,
    ml: space.marginLeft,
    ms: space.marginInlineStart,
    marginStart: space.marginInlineStart,
    mx: space.marginX,
    my: space.marginY,
    p: space.padding,
    pt: space.paddingTop,
    py: space.paddingY,
    px: space.paddingX,
    pb: space.paddingBottom,
    pl: space.paddingLeft,
    ps: space.paddingInlineStart,
    paddingStart: space.paddingInlineStart,
    pr: space.paddingRight,
    pe: space.paddingInlineEnd,
    paddingEnd: space.paddingInlineEnd
  });
  var textDecoration = {
    textDecorationColor: t.colors("textDecorationColor"),
    textDecoration: true,
    textDecor: { property: "textDecoration" },
    textDecorationLine: true,
    textDecorationStyle: true,
    textDecorationThickness: true,
    textUnderlineOffset: true,
    textShadow: t.shadows("textShadow")
  };
  var transform = {
    clipPath: true,
    transform: t.propT("transform", transformFunctions.transform),
    transformOrigin: true,
    translateX: t.spaceT("--chakra-translate-x"),
    translateY: t.spaceT("--chakra-translate-y"),
    skewX: t.degreeT("--chakra-skew-x"),
    skewY: t.degreeT("--chakra-skew-y"),
    scaleX: t.prop("--chakra-scale-x"),
    scaleY: t.prop("--chakra-scale-y"),
    scale: t.prop(["--chakra-scale-x", "--chakra-scale-y"]),
    rotate: t.degreeT("--chakra-rotate")
  };
  var transition$1 = {
    transition: true,
    transitionDelay: true,
    animation: true,
    willChange: true,
    transitionDuration: t.prop("transitionDuration", "transition.duration"),
    transitionProperty: t.prop("transitionProperty", "transition.property"),
    transitionTimingFunction: t.prop(
      "transitionTimingFunction",
      "transition.easing"
    )
  };
  var typography$1 = {
    fontFamily: t.prop("fontFamily", "fonts"),
    fontSize: t.prop("fontSize", "fontSizes", transformFunctions.px),
    fontWeight: t.prop("fontWeight", "fontWeights"),
    lineHeight: t.prop("lineHeight", "lineHeights"),
    letterSpacing: t.prop("letterSpacing", "letterSpacings"),
    textAlign: true,
    fontStyle: true,
    textIndent: true,
    wordBreak: true,
    overflowWrap: true,
    textOverflow: true,
    textTransform: true,
    whiteSpace: true,
    isTruncated: {
      transform(value) {
        if (value === true) {
          return {
            overflow: "hidden",
            textOverflow: "ellipsis",
            whiteSpace: "nowrap"
          };
        }
      }
    },
    noOfLines: {
      static: {
        overflow: "hidden",
        textOverflow: "ellipsis",
        display: "-webkit-box",
        WebkitBoxOrient: "vertical",
        //@ts-ignore
        WebkitLineClamp: "var(--chakra-line-clamp)"
      },
      property: "--chakra-line-clamp"
    }
  };
  var scroll = {
    scrollBehavior: true,
    scrollSnapAlign: true,
    scrollSnapStop: true,
    scrollSnapType: true,
    // scroll margin
    scrollMargin: t.spaceT("scrollMargin"),
    scrollMarginTop: t.spaceT("scrollMarginTop"),
    scrollMarginBottom: t.spaceT("scrollMarginBottom"),
    scrollMarginLeft: t.spaceT("scrollMarginLeft"),
    scrollMarginRight: t.spaceT("scrollMarginRight"),
    scrollMarginX: t.spaceT(["scrollMarginLeft", "scrollMarginRight"]),
    scrollMarginY: t.spaceT(["scrollMarginTop", "scrollMarginBottom"]),
    // scroll padding
    scrollPadding: t.spaceT("scrollPadding"),
    scrollPaddingTop: t.spaceT("scrollPaddingTop"),
    scrollPaddingBottom: t.spaceT("scrollPaddingBottom"),
    scrollPaddingLeft: t.spaceT("scrollPaddingLeft"),
    scrollPaddingRight: t.spaceT("scrollPaddingRight"),
    scrollPaddingX: t.spaceT(["scrollPaddingLeft", "scrollPaddingRight"]),
    scrollPaddingY: t.spaceT(["scrollPaddingTop", "scrollPaddingBottom"])
  };
  function resolveReference(operand) {
    if (isObject(operand) && operand.reference) {
      return operand.reference;
    }
    return String(operand);
  }
  var toExpression = (operator, ...operands) => operands.map(resolveReference).join(` ${operator} `).replace(/calc/g, "");
  var add$1 = (...operands) => `calc(${toExpression("+", ...operands)})`;
  var subtract$1 = (...operands) => `calc(${toExpression("-", ...operands)})`;
  var multiply$1 = (...operands) => `calc(${toExpression("*", ...operands)})`;
  var divide$1 = (...operands) => `calc(${toExpression("/", ...operands)})`;
  var negate$1 = (x2) => {
    const value = resolveReference(x2);
    if (value != null && !Number.isNaN(parseFloat(value))) {
      return String(value).startsWith("-") ? String(value).slice(1) : `-${value}`;
    }
    return multiply$1(value, -1);
  };
  var calc$1 = Object.assign(
    (x2) => ({
      add: (...operands) => calc$1(add$1(x2, ...operands)),
      subtract: (...operands) => calc$1(subtract$1(x2, ...operands)),
      multiply: (...operands) => calc$1(multiply$1(x2, ...operands)),
      divide: (...operands) => calc$1(divide$1(x2, ...operands)),
      negate: () => calc$1(negate$1(x2)),
      toString: () => x2.toString()
    }),
    {
      add: add$1,
      subtract: subtract$1,
      multiply: multiply$1,
      divide: divide$1,
      negate: negate$1
    }
  );
  function replaceWhiteSpace$1(value, replaceValue = "-") {
    return value.replace(/\s+/g, replaceValue);
  }
  function escape$1(value) {
    const valueStr = replaceWhiteSpace$1(value.toString());
    return escapeSymbol(escapeDot(valueStr));
  }
  function escapeDot(value) {
    if (value.includes("\\."))
      return value;
    const isDecimal2 = !Number.isInteger(parseFloat(value.toString()));
    return isDecimal2 ? value.replace(".", `\\.`) : value;
  }
  function escapeSymbol(value) {
    return value.replace(/[!-,/:-@[-^`{-~]/g, "\\$&");
  }
  function addPrefix$1(value, prefix2 = "") {
    return [prefix2, value].filter(Boolean).join("-");
  }
  function toVarReference(name, fallback) {
    return `var(${name}${fallback ? `, ${fallback}` : ""})`;
  }
  function toVarDefinition(value, prefix2 = "") {
    return escape$1(`--${addPrefix$1(value, prefix2)}`);
  }
  function cssVar$1(name, fallback, cssVarPrefix) {
    const cssVariable = toVarDefinition(name, cssVarPrefix);
    return {
      variable: cssVariable,
      reference: toVarReference(cssVariable, fallback)
    };
  }
  function defineCssVars(scope, keys2) {
    const vars2 = {};
    for (const key of keys2) {
      if (Array.isArray(key)) {
        const [name, fallback] = key;
        vars2[name] = cssVar$1(`${scope}-${name}`, fallback);
        continue;
      }
      vars2[key] = cssVar$1(`${scope}-${key}`);
    }
    return vars2;
  }
  function getLastItem(array) {
    const length2 = array == null ? 0 : array.length;
    return length2 ? array[length2 - 1] : void 0;
  }
  function analyzeCSSValue2(value) {
    const num = parseFloat(value.toString());
    const unit = value.toString().replace(String(num), "");
    return { unitless: !unit, value: num, unit };
  }
  function px$1(value) {
    if (value == null)
      return value;
    const { unitless } = analyzeCSSValue2(value);
    return unitless || typeof value === "number" ? `${value}px` : value;
  }
  var sortByBreakpointValue = (a, b2) => parseInt(a[1], 10) > parseInt(b2[1], 10) ? 1 : -1;
  var sortBps = (breakpoints2) => Object.fromEntries(Object.entries(breakpoints2).sort(sortByBreakpointValue));
  function normalize(breakpoints2) {
    const sorted = sortBps(breakpoints2);
    return Object.assign(Object.values(sorted), sorted);
  }
  function keys(breakpoints2) {
    const value = Object.keys(sortBps(breakpoints2));
    return new Set(value);
  }
  function subtract2(value) {
    var _a4;
    if (!value)
      return value;
    value = (_a4 = px$1(value)) != null ? _a4 : value;
    const OFFSET = -0.02;
    return typeof value === "number" ? `${value + OFFSET}` : value.replace(/(\d+\.?\d*)/u, (m2) => `${parseFloat(m2) + OFFSET}`);
  }
  function toMediaQueryString(min, max) {
    const query = ["@media screen"];
    if (min)
      query.push("and", `(min-width: ${px$1(min)})`);
    if (max)
      query.push("and", `(max-width: ${px$1(max)})`);
    return query.join(" ");
  }
  function analyzeBreakpoints(breakpoints2) {
    var _a4;
    if (!breakpoints2)
      return null;
    breakpoints2.base = (_a4 = breakpoints2.base) != null ? _a4 : "0px";
    const normalized = normalize(breakpoints2);
    const queries = Object.entries(breakpoints2).sort(sortByBreakpointValue).map(([breakpoint, minW], index, entry) => {
      var _a22;
      let [, maxW] = (_a22 = entry[index + 1]) != null ? _a22 : [];
      maxW = parseFloat(maxW) > 0 ? subtract2(maxW) : void 0;
      return {
        _minW: subtract2(minW),
        breakpoint,
        minW,
        maxW,
        maxWQuery: toMediaQueryString(null, maxW),
        minWQuery: toMediaQueryString(minW),
        minMaxQuery: toMediaQueryString(minW, maxW)
      };
    });
    const _keys = keys(breakpoints2);
    const _keysArr = Array.from(_keys.values());
    return {
      keys: _keys,
      normalized,
      isResponsive(test2) {
        const keys2 = Object.keys(test2);
        return keys2.length > 0 && keys2.every((key) => _keys.has(key));
      },
      asObject: sortBps(breakpoints2),
      asArray: normalize(breakpoints2),
      details: queries,
      get(key) {
        return queries.find((q2) => q2.breakpoint === key);
      },
      media: [
        null,
        ...normalized.map((minW) => toMediaQueryString(minW)).slice(1)
      ],
      /**
       * Converts the object responsive syntax to array syntax
       *
       * @example
       * toArrayValue({ base: 1, sm: 2, md: 3 }) // => [1, 2, 3]
       */
      toArrayValue(test2) {
        if (!isObject(test2)) {
          throw new Error("toArrayValue: value must be an object");
        }
        const result = _keysArr.map((bp) => {
          var _a22;
          return (_a22 = test2[bp]) != null ? _a22 : null;
        });
        while (getLastItem(result) === null) {
          result.pop();
        }
        return result;
      },
      /**
       * Converts the array responsive syntax to object syntax
       *
       * @example
       * toObjectValue([1, 2, 3]) // => { base: 1, sm: 2, md: 3 }
       */
      toObjectValue(test2) {
        if (!Array.isArray(test2)) {
          throw new Error("toObjectValue: value must be an array");
        }
        return test2.reduce((acc, value, index) => {
          const key = _keysArr[index];
          if (key != null && value != null)
            acc[key] = value;
          return acc;
        }, {});
      }
    };
  }
  var state = {
    hover: (str, post) => `${str}:hover ${post}, ${str}[data-hover] ${post}`,
    focus: (str, post) => `${str}:focus ${post}, ${str}[data-focus] ${post}`,
    focusVisible: (str, post) => `${str}:focus-visible ${post}`,
    focusWithin: (str, post) => `${str}:focus-within ${post}`,
    active: (str, post) => `${str}:active ${post}, ${str}[data-active] ${post}`,
    disabled: (str, post) => `${str}:disabled ${post}, ${str}[data-disabled] ${post}`,
    invalid: (str, post) => `${str}:invalid ${post}, ${str}[data-invalid] ${post}`,
    checked: (str, post) => `${str}:checked ${post}, ${str}[data-checked] ${post}`,
    indeterminate: (str, post) => `${str}:indeterminate ${post}, ${str}[aria-checked=mixed] ${post}, ${str}[data-indeterminate] ${post}`,
    readOnly: (str, post) => `${str}:read-only ${post}, ${str}[readonly] ${post}, ${str}[data-read-only] ${post}`,
    expanded: (str, post) => `${str}:read-only ${post}, ${str}[aria-expanded=true] ${post}, ${str}[data-expanded] ${post}`,
    placeholderShown: (str, post) => `${str}:placeholder-shown ${post}`
  };
  var toGroup = (fn) => merge((v2) => fn(v2, "&"), "[role=group]", "[data-group]", ".group");
  var toPeer = (fn) => merge((v2) => fn(v2, "~ &"), "[data-peer]", ".peer");
  var merge = (fn, ...selectors) => selectors.map(fn).join(", ");
  var pseudoSelectors = {
    /**
     * Styles for CSS selector `&:hover`
     */
    _hover: "&:hover, &[data-hover]",
    /**
     * Styles for CSS Selector `&:active`
     */
    _active: "&:active, &[data-active]",
    /**
     * Styles for CSS selector `&:focus`
     *
     */
    _focus: "&:focus, &[data-focus]",
    /**
     * Styles for the highlighted state.
     */
    _highlighted: "&[data-highlighted]",
    /**
     * Styles to apply when a child of this element has received focus
     * - CSS Selector `&:focus-within`
     */
    _focusWithin: "&:focus-within",
    /**
     * Styles to apply when this element has received focus via tabbing
     * - CSS Selector `&:focus-visible`
     */
    _focusVisible: "&:focus-visible, &[data-focus-visible]",
    /**
     * Styles to apply when this element is disabled. The passed styles are applied to these CSS selectors:
     * - `&[aria-disabled=true]`
     * - `&:disabled`
     * - `&[data-disabled]`
     * - `&[disabled]`
     */
    _disabled: "&:disabled, &[disabled], &[aria-disabled=true], &[data-disabled]",
    /**
     * Styles for CSS Selector `&:readonly`
     */
    _readOnly: "&[aria-readonly=true], &[readonly], &[data-readonly]",
    /**
     * Styles for CSS selector `&::before`
     *
     * NOTE:When using this, ensure the `content` is wrapped in a backtick.
     * @example
     * ```jsx
     * <Box _before={{content:`""` }}/>
     * ```
     */
    _before: "&::before",
    /**
     * Styles for CSS selector `&::after`
     *
     * NOTE:When using this, ensure the `content` is wrapped in a backtick.
     * @example
     * ```jsx
     * <Box _after={{content:`""` }}/>
     * ```
     */
    _after: "&::after",
    /**
     * Styles for CSS selector `&:empty`
     */
    _empty: "&:empty",
    /**
     * Styles to apply when the ARIA attribute `aria-expanded` is `true`
     * - CSS selector `&[aria-expanded=true]`
     */
    _expanded: "&[aria-expanded=true], &[data-expanded]",
    /**
     * Styles to apply when the ARIA attribute `aria-checked` is `true`
     * - CSS selector `&[aria-checked=true]`
     */
    _checked: "&[aria-checked=true], &[data-checked]",
    /**
     * Styles to apply when the ARIA attribute `aria-grabbed` is `true`
     * - CSS selector `&[aria-grabbed=true]`
     */
    _grabbed: "&[aria-grabbed=true], &[data-grabbed]",
    /**
     * Styles for CSS Selector `&[aria-pressed=true]`
     * Typically used to style the current "pressed" state of toggle buttons
     */
    _pressed: "&[aria-pressed=true], &[data-pressed]",
    /**
     * Styles to apply when the ARIA attribute `aria-invalid` is `true`
     * - CSS selector `&[aria-invalid=true]`
     */
    _invalid: "&[aria-invalid=true], &[data-invalid]",
    /**
     * Styles for the valid state
     * - CSS selector `&[data-valid], &[data-state=valid]`
     */
    _valid: "&[data-valid], &[data-state=valid]",
    /**
     * Styles for CSS Selector `&[aria-busy=true]` or `&[data-loading=true]`.
     * Useful for styling loading states
     */
    _loading: "&[data-loading], &[aria-busy=true]",
    /**
     * Styles to apply when the ARIA attribute `aria-selected` is `true`
     *
     * - CSS selector `&[aria-selected=true]`
     */
    _selected: "&[aria-selected=true], &[data-selected]",
    /**
     * Styles for CSS Selector `[hidden=true]`
     */
    _hidden: "&[hidden], &[data-hidden]",
    /**
     * Styles for CSS Selector `&:-webkit-autofill`
     */
    _autofill: "&:-webkit-autofill",
    /**
     * Styles for CSS Selector `&:nth-child(even)`
     */
    _even: "&:nth-of-type(even)",
    /**
     * Styles for CSS Selector `&:nth-child(odd)`
     */
    _odd: "&:nth-of-type(odd)",
    /**
     * Styles for CSS Selector `&:first-of-type`
     */
    _first: "&:first-of-type",
    /**
     * Styles for CSS selector `&::first-letter`
     *
     * NOTE: This selector is only applied for block-level elements and not preceded by an image or table.
     * @example
     * ```jsx
     * <Text _firstLetter={{ textDecoration: 'underline' }}>Once upon a time</Text>
     * ```
     */
    _firstLetter: "&::first-letter",
    /**
     * Styles for CSS Selector `&:last-of-type`
     */
    _last: "&:last-of-type",
    /**
     * Styles for CSS Selector `&:not(:first-of-type)`
     */
    _notFirst: "&:not(:first-of-type)",
    /**
     * Styles for CSS Selector `&:not(:last-of-type)`
     */
    _notLast: "&:not(:last-of-type)",
    /**
     * Styles for CSS Selector `&:visited`
     */
    _visited: "&:visited",
    /**
     * Used to style the active link in a navigation
     * Styles for CSS Selector `&[aria-current=page]`
     */
    _activeLink: "&[aria-current=page]",
    /**
     * Used to style the current step within a process
     * Styles for CSS Selector `&[aria-current=step]`
     */
    _activeStep: "&[aria-current=step]",
    /**
     * Styles to apply when the ARIA attribute `aria-checked` is `mixed`
     * - CSS selector `&[aria-checked=mixed]`
     */
    _indeterminate: "&:indeterminate, &[aria-checked=mixed], &[data-indeterminate]",
    /**
     * Styles to apply when a parent element with `.group`, `data-group` or `role=group` is hovered
     */
    _groupHover: toGroup(state.hover),
    /**
     * Styles to apply when a sibling element with `.peer` or `data-peer` is hovered
     */
    _peerHover: toPeer(state.hover),
    /**
     * Styles to apply when a parent element with `.group`, `data-group` or `role=group` is focused
     */
    _groupFocus: toGroup(state.focus),
    /**
     * Styles to apply when a sibling element with `.peer` or `data-peer` is focused
     */
    _peerFocus: toPeer(state.focus),
    /**
     * Styles to apply when a parent element with `.group`, `data-group` or `role=group` has visible focus
     */
    _groupFocusVisible: toGroup(state.focusVisible),
    /**
     * Styles to apply when a sibling element with `.peer`or `data-peer` has visible focus
     */
    _peerFocusVisible: toPeer(state.focusVisible),
    /**
     * Styles to apply when a parent element with `.group`, `data-group` or `role=group` is active
     */
    _groupActive: toGroup(state.active),
    /**
     * Styles to apply when a sibling element with `.peer` or `data-peer` is active
     */
    _peerActive: toPeer(state.active),
    /**
     * Styles to apply when a parent element with `.group`, `data-group` or `role=group` is disabled
     */
    _groupDisabled: toGroup(state.disabled),
    /**
     *  Styles to apply when a sibling element with `.peer` or `data-peer` is disabled
     */
    _peerDisabled: toPeer(state.disabled),
    /**
     *  Styles to apply when a parent element with `.group`, `data-group` or `role=group` is invalid
     */
    _groupInvalid: toGroup(state.invalid),
    /**
     *  Styles to apply when a sibling element with `.peer` or `data-peer` is invalid
     */
    _peerInvalid: toPeer(state.invalid),
    /**
     * Styles to apply when a parent element with `.group`, `data-group` or `role=group` is checked
     */
    _groupChecked: toGroup(state.checked),
    /**
     * Styles to apply when a sibling element with `.peer` or `data-peer` is checked
     */
    _peerChecked: toPeer(state.checked),
    /**
     *  Styles to apply when a parent element with `.group`, `data-group` or `role=group` has focus within
     */
    _groupFocusWithin: toGroup(state.focusWithin),
    /**
     *  Styles to apply when a sibling element with `.peer` or `data-peer` has focus within
     */
    _peerFocusWithin: toPeer(state.focusWithin),
    /**
     * Styles to apply when a sibling element with `.peer` or `data-peer` has placeholder shown
     */
    _peerPlaceholderShown: toPeer(state.placeholderShown),
    /**
     * Styles for CSS Selector `&::placeholder`.
     */
    _placeholder: "&::placeholder",
    /**
     * Styles for CSS Selector `&:placeholder-shown`.
     */
    _placeholderShown: "&:placeholder-shown",
    /**
     * Styles for CSS Selector `&:fullscreen`.
     */
    _fullScreen: "&:fullscreen",
    /**
     * Styles for CSS Selector `&::selection`
     */
    _selection: "&::selection",
    /**
     * Styles for CSS Selector `[dir=rtl] &`
     * It is applied when a parent element or this element has `dir="rtl"`
     */
    _rtl: "[dir=rtl] &, &[dir=rtl]",
    /**
     * Styles for CSS Selector `[dir=ltr] &`
     * It is applied when a parent element or this element has `dir="ltr"`
     */
    _ltr: "[dir=ltr] &, &[dir=ltr]",
    /**
     * Styles for CSS Selector `@media (prefers-color-scheme: dark)`
     * It is used when the user has requested the system use a light or dark color theme.
     */
    _mediaDark: "@media (prefers-color-scheme: dark)",
    /**
     * Styles for CSS Selector `@media (prefers-reduced-motion: reduce)`
     * It is used when the user has requested the system to reduce the amount of animations.
     */
    _mediaReduceMotion: "@media (prefers-reduced-motion: reduce)",
    /**
     * Styles for when `data-theme` is applied to any parent of
     * this component or element.
     */
    _dark: ".chakra-ui-dark &:not([data-theme]),[data-theme=dark] &:not([data-theme]),&[data-theme=dark]",
    /**
     * Styles for when `data-theme` is applied to any parent of
     * this component or element.
     */
    _light: ".chakra-ui-light &:not([data-theme]),[data-theme=light] &:not([data-theme]),&[data-theme=light]",
    /**
     * Styles for the CSS Selector `&[data-orientation=horizontal]`
     */
    _horizontal: "&[data-orientation=horizontal]",
    /**
     * Styles for the CSS Selector `&[data-orientation=vertical]`
     */
    _vertical: "&[data-orientation=vertical]"
  };
  var pseudoPropNames = Object.keys(
    pseudoSelectors
  );
  function tokenToCssVar(token2, prefix2) {
    return cssVar$1(String(token2).replace(/\./g, "-"), void 0, prefix2);
  }
  function createThemeVars(flatTokens, options) {
    let cssVars = {};
    const cssMap = {};
    for (const [token2, tokenValue] of Object.entries(flatTokens)) {
      const { isSemantic, value } = tokenValue;
      const { variable, reference } = tokenToCssVar(token2, options == null ? void 0 : options.cssVarPrefix);
      if (!isSemantic) {
        if (token2.startsWith("space")) {
          const keys2 = token2.split(".");
          const [firstKey, ...referenceKeys] = keys2;
          const negativeLookupKey = `${firstKey}.-${referenceKeys.join(".")}`;
          const negativeValue = calc$1.negate(value);
          const negatedReference = calc$1.negate(reference);
          cssMap[negativeLookupKey] = {
            value: negativeValue,
            var: variable,
            varRef: negatedReference
          };
        }
        cssVars[variable] = value;
        cssMap[token2] = {
          value,
          var: variable,
          varRef: reference
        };
        continue;
      }
      const lookupToken = (maybeToken) => {
        const scale2 = String(token2).split(".")[0];
        const withScale = [scale2, maybeToken].join(".");
        const resolvedTokenValue = flatTokens[withScale];
        if (!resolvedTokenValue)
          return maybeToken;
        const { reference: reference2 } = tokenToCssVar(withScale, options == null ? void 0 : options.cssVarPrefix);
        return reference2;
      };
      const normalizedValue = isObject(value) ? value : { default: value };
      cssVars = mergeWith(
        cssVars,
        Object.entries(normalizedValue).reduce(
          (acc, [conditionAlias, conditionValue]) => {
            var _a4, _b3;
            if (!conditionValue)
              return acc;
            const tokenReference = lookupToken(`${conditionValue}`);
            if (conditionAlias === "default") {
              acc[variable] = tokenReference;
              return acc;
            }
            const conditionSelector = (_b3 = (_a4 = pseudoSelectors) == null ? void 0 : _a4[conditionAlias]) != null ? _b3 : conditionAlias;
            acc[conditionSelector] = { [variable]: tokenReference };
            return acc;
          },
          {}
        )
      );
      cssMap[token2] = {
        value: reference,
        var: variable,
        varRef: reference
      };
    }
    return {
      cssVars,
      cssMap
    };
  }
  function omit$1(object, keysToOmit = []) {
    const clone = Object.assign({}, object);
    for (const key of keysToOmit) {
      if (key in clone) {
        delete clone[key];
      }
    }
    return clone;
  }
  function pick(object, keysToPick) {
    const result = {};
    for (const key of keysToPick) {
      if (key in object) {
        result[key] = object[key];
      }
    }
    return result;
  }
  function isObject5(value) {
    return typeof value === "object" && value != null && !Array.isArray(value);
  }
  function walkObject(target, predicate, options = {}) {
    const { stop, getKey } = options;
    function inner(value, path = []) {
      var _a4;
      if (isObject5(value) || Array.isArray(value)) {
        const result = {};
        for (const [prop, child] of Object.entries(value)) {
          const key = (_a4 = getKey == null ? void 0 : getKey(prop)) != null ? _a4 : prop;
          const childPath = [...path, key];
          if (stop == null ? void 0 : stop(value, childPath)) {
            return predicate(value, path);
          }
          result[key] = inner(child, childPath);
        }
        return result;
      }
      return predicate(value, path);
    }
    return inner(target);
  }
  var tokens = [
    "colors",
    "borders",
    "borderWidths",
    "borderStyles",
    "fonts",
    "fontSizes",
    "fontWeights",
    "gradients",
    "letterSpacings",
    "lineHeights",
    "radii",
    "space",
    "shadows",
    "sizes",
    "zIndices",
    "transition",
    "blur",
    "breakpoints"
  ];
  function extractTokens(theme2) {
    const _tokens = tokens;
    return pick(theme2, _tokens);
  }
  function extractSemanticTokens(theme2) {
    return theme2.semanticTokens;
  }
  function omitVars(rawTheme) {
    const { __cssMap, __cssVars, __breakpoints, ...cleanTheme } = rawTheme;
    return cleanTheme;
  }
  var isSemanticCondition = (key) => pseudoPropNames.includes(key) || "default" === key;
  function flattenTokens({
    tokens: tokens2,
    semanticTokens: semanticTokens2
  }) {
    const result = {};
    walkObject(tokens2, (value, path) => {
      if (value == null)
        return;
      result[path.join(".")] = { isSemantic: false, value };
    });
    walkObject(
      semanticTokens2,
      (value, path) => {
        if (value == null)
          return;
        result[path.join(".")] = { isSemantic: true, value };
      },
      {
        stop: (value) => Object.keys(value).every(isSemanticCondition)
      }
    );
    return result;
  }
  function toCSSVar(rawTheme) {
    var _a4;
    const theme2 = omitVars(rawTheme);
    const tokens2 = extractTokens(theme2);
    const semanticTokens2 = extractSemanticTokens(theme2);
    const flatTokens = flattenTokens({ tokens: tokens2, semanticTokens: semanticTokens2 });
    const cssVarPrefix = (_a4 = theme2.config) == null ? void 0 : _a4.cssVarPrefix;
    const {
      /**
       * This is more like a dictionary of tokens users will type `green.500`,
       * and their equivalent css variable.
       */
      cssMap,
      /**
       * The extracted css variables will be stored here, and used in
       * the emotion's <Global/> component to attach variables to `:root`
       */
      cssVars
    } = createThemeVars(flatTokens, { cssVarPrefix });
    const defaultCssVars = {
      "--chakra-ring-inset": "var(--chakra-empty,/*!*/ /*!*/)",
      "--chakra-ring-offset-width": "0px",
      "--chakra-ring-offset-color": "#fff",
      "--chakra-ring-color": "rgba(66, 153, 225, 0.6)",
      "--chakra-ring-offset-shadow": "0 0 #0000",
      "--chakra-ring-shadow": "0 0 #0000",
      "--chakra-space-x-reverse": "0",
      "--chakra-space-y-reverse": "0"
    };
    Object.assign(theme2, {
      __cssVars: { ...defaultCssVars, ...cssVars },
      __cssMap: cssMap,
      __breakpoints: analyzeBreakpoints(theme2.breakpoints)
    });
    return theme2;
  }
  var systemProps = mergeWith(
    {},
    background,
    border,
    color$1,
    flexbox,
    layout$1,
    filter$2,
    ring,
    interactivity,
    grid,
    others,
    position$1,
    effect,
    space,
    scroll,
    typography$1,
    textDecoration,
    transform,
    list,
    transition$1
  );
  Object.assign({}, space, layout$1, flexbox, grid, position$1);
  var propNames = [...Object.keys(systemProps), ...pseudoPropNames];
  var styleProps = { ...systemProps, ...pseudoSelectors };
  var isStyleProp = (prop) => prop in styleProps;
  var expandResponsive = (styles2) => (theme2) => {
    if (!theme2.__breakpoints)
      return styles2;
    const { isResponsive, toArrayValue, media: medias } = theme2.__breakpoints;
    const computedStyles = {};
    for (const key in styles2) {
      let value = runIfFn$2(styles2[key], theme2);
      if (value == null)
        continue;
      value = isObject(value) && isResponsive(value) ? toArrayValue(value) : value;
      if (!Array.isArray(value)) {
        computedStyles[key] = value;
        continue;
      }
      const queries = value.slice(0, medias.length).length;
      for (let index = 0; index < queries; index += 1) {
        const media = medias == null ? void 0 : medias[index];
        if (!media) {
          computedStyles[key] = value[index];
          continue;
        }
        computedStyles[media] = computedStyles[media] || {};
        if (value[index] == null) {
          continue;
        }
        computedStyles[media][key] = value[index];
      }
    }
    return computedStyles;
  };
  function splitByComma(value) {
    const chunks = [];
    let chunk = "";
    let inParens = false;
    for (let i = 0; i < value.length; i++) {
      const char2 = value[i];
      if (char2 === "(") {
        inParens = true;
        chunk += char2;
      } else if (char2 === ")") {
        inParens = false;
        chunk += char2;
      } else if (char2 === "," && !inParens) {
        chunks.push(chunk);
        chunk = "";
      } else {
        chunk += char2;
      }
    }
    chunk = chunk.trim();
    if (chunk) {
      chunks.push(chunk);
    }
    return chunks;
  }
  function isCssVar2(value) {
    return /^var\(--.+\)$/.test(value);
  }
  var isCSSVariableTokenValue = (key, value) => key.startsWith("--") && typeof value === "string" && !isCssVar2(value);
  var resolveTokenValue = (theme2, value) => {
    var _a4, _b3;
    if (value == null)
      return value;
    const getVar = (val) => {
      var _a22, _b22;
      return (_b22 = (_a22 = theme2.__cssMap) == null ? void 0 : _a22[val]) == null ? void 0 : _b22.varRef;
    };
    const getValue = (val) => {
      var _a22;
      return (_a22 = getVar(val)) != null ? _a22 : val;
    };
    const [tokenValue, fallbackValue] = splitByComma(value);
    value = (_b3 = (_a4 = getVar(tokenValue)) != null ? _a4 : getValue(fallbackValue)) != null ? _b3 : getValue(value);
    return value;
  };
  function getCss(options) {
    const { configs = {}, pseudos = {}, theme: theme2 } = options;
    const css2 = (stylesOrFn, nested = false) => {
      var _a4, _b3, _c2;
      const _styles = runIfFn$2(stylesOrFn, theme2);
      const styles2 = expandResponsive(_styles)(theme2);
      let computedStyles = {};
      for (let key in styles2) {
        const valueOrFn = styles2[key];
        let value = runIfFn$2(valueOrFn, theme2);
        if (key in pseudos) {
          key = pseudos[key];
        }
        if (isCSSVariableTokenValue(key, value)) {
          value = resolveTokenValue(theme2, value);
        }
        let config2 = configs[key];
        if (config2 === true) {
          config2 = { property: key };
        }
        if (isObject(value)) {
          computedStyles[key] = (_a4 = computedStyles[key]) != null ? _a4 : {};
          computedStyles[key] = mergeWith(
            {},
            computedStyles[key],
            css2(value, true)
          );
          continue;
        }
        let rawValue = (_c2 = (_b3 = config2 == null ? void 0 : config2.transform) == null ? void 0 : _b3.call(config2, value, theme2, _styles)) != null ? _c2 : value;
        rawValue = (config2 == null ? void 0 : config2.processResult) ? css2(rawValue, true) : rawValue;
        const configProperty = runIfFn$2(config2 == null ? void 0 : config2.property, theme2);
        if (!nested && (config2 == null ? void 0 : config2.static)) {
          const staticStyles = runIfFn$2(config2.static, theme2);
          computedStyles = mergeWith({}, computedStyles, staticStyles);
        }
        if (configProperty && Array.isArray(configProperty)) {
          for (const property of configProperty) {
            computedStyles[property] = rawValue;
          }
          continue;
        }
        if (configProperty) {
          if (configProperty === "&" && isObject(rawValue)) {
            computedStyles = mergeWith({}, computedStyles, rawValue);
          } else {
            computedStyles[configProperty] = rawValue;
          }
          continue;
        }
        if (isObject(rawValue)) {
          computedStyles = mergeWith({}, computedStyles, rawValue);
          continue;
        }
        computedStyles[key] = rawValue;
      }
      return computedStyles;
    };
    return css2;
  }
  var css = (styles2) => (theme2) => {
    const cssFn = getCss({
      theme: theme2,
      pseudos: pseudoSelectors,
      configs: systemProps
    });
    return cssFn(styles2);
  };
  function defineStyle(styles2) {
    return styles2;
  }
  function defineStyleConfig(config2) {
    return config2;
  }
  function createMultiStyleConfigHelpers(parts) {
    return {
      definePartsStyle(config2) {
        return config2;
      },
      defineMultiStyleConfig(config2) {
        return { parts, ...config2 };
      }
    };
  }
  function normalize2(value, toArray) {
    if (Array.isArray(value))
      return value;
    if (isObject(value))
      return toArray(value);
    if (value != null)
      return [value];
  }
  function getNextIndex(values, i) {
    for (let j2 = i + 1; j2 < values.length; j2++) {
      if (values[j2] != null)
        return j2;
    }
    return -1;
  }
  function createResolver(theme2) {
    const breakpointUtil = theme2.__breakpoints;
    return function resolver(config2, prop, value, props) {
      var _a4, _b3;
      if (!breakpointUtil)
        return;
      const result = {};
      const normalized = normalize2(value, breakpointUtil.toArrayValue);
      if (!normalized)
        return result;
      const len = normalized.length;
      const isSingle = len === 1;
      const isMultipart = !!config2.parts;
      for (let i = 0; i < len; i++) {
        const key = breakpointUtil.details[i];
        const nextKey = breakpointUtil.details[getNextIndex(normalized, i)];
        const query = toMediaQueryString(key.minW, nextKey == null ? void 0 : nextKey._minW);
        const styles2 = runIfFn$2((_a4 = config2[prop]) == null ? void 0 : _a4[normalized[i]], props);
        if (!styles2)
          continue;
        if (isMultipart) {
          (_b3 = config2.parts) == null ? void 0 : _b3.forEach((part) => {
            mergeWith(result, {
              [part]: isSingle ? styles2[part] : { [query]: styles2[part] }
            });
          });
          continue;
        }
        if (!isMultipart) {
          if (isSingle)
            mergeWith(result, styles2);
          else
            result[query] = styles2;
          continue;
        }
        result[query] = styles2;
      }
      return result;
    };
  }
  function resolveStyleConfig(config2) {
    return (props) => {
      var _a4;
      const { variant, size: size2, theme: theme2 } = props;
      const recipe = createResolver(theme2);
      return mergeWith(
        {},
        runIfFn$2((_a4 = config2.baseStyle) != null ? _a4 : {}, props),
        recipe(config2, "sizes", size2, props),
        recipe(config2, "variants", variant, props)
      );
    };
  }
  function omitThemingProps(props) {
    return omit$1(props, ["styleConfig", "size", "variant", "colorScheme"]);
  }
  var requiredChakraThemeKeys = [
    "borders",
    "breakpoints",
    "colors",
    "components",
    "config",
    "direction",
    "fonts",
    "fontSizes",
    "fontWeights",
    "letterSpacings",
    "lineHeights",
    "radii",
    "shadows",
    "sizes",
    "space",
    "styles",
    "transition",
    "zIndices"
  ];
  function isChakraTheme(unit) {
    if (!isObject(unit)) {
      return false;
    }
    return requiredChakraThemeKeys.every(
      (propertyName) => Object.prototype.hasOwnProperty.call(unit, propertyName)
    );
  }
  var transitionProperty = {
    common: "background-color, border-color, color, fill, stroke, opacity, box-shadow, transform",
    colors: "background-color, border-color, color, fill, stroke",
    dimensions: "width, height",
    position: "left, right, top, bottom",
    background: "background-color, background-image, background-position"
  };
  var transitionTimingFunction = {
    "ease-in": "cubic-bezier(0.4, 0, 1, 1)",
    "ease-out": "cubic-bezier(0, 0, 0.2, 1)",
    "ease-in-out": "cubic-bezier(0.4, 0, 0.2, 1)"
  };
  var transitionDuration = {
    "ultra-fast": "50ms",
    faster: "100ms",
    fast: "150ms",
    normal: "200ms",
    slow: "300ms",
    slower: "400ms",
    "ultra-slow": "500ms"
  };
  var transition = {
    property: transitionProperty,
    easing: transitionTimingFunction,
    duration: transitionDuration
  };
  var transition_default = transition;
  var zIndices = {
    hide: -1,
    auto: "auto",
    base: 0,
    docked: 10,
    dropdown: 1e3,
    sticky: 1100,
    banner: 1200,
    overlay: 1300,
    modal: 1400,
    popover: 1500,
    skipLink: 1600,
    toast: 1700,
    tooltip: 1800
  };
  var z_index_default = zIndices;
  var borders$1 = {
    none: 0,
    "1px": "1px solid",
    "2px": "2px solid",
    "4px": "4px solid",
    "8px": "8px solid"
  };
  var borders_default = borders$1;
  var breakpoints = {
    base: "0em",
    sm: "30em",
    md: "48em",
    lg: "62em",
    xl: "80em",
    "2xl": "96em"
  };
  var breakpoints_default = breakpoints;
  var colors = {
    transparent: "transparent",
    current: "currentColor",
    black: "#000000",
    white: "#FFFFFF",
    whiteAlpha: {
      50: "rgba(255, 255, 255, 0.04)",
      100: "rgba(255, 255, 255, 0.06)",
      200: "rgba(255, 255, 255, 0.08)",
      300: "rgba(255, 255, 255, 0.16)",
      400: "rgba(255, 255, 255, 0.24)",
      500: "rgba(255, 255, 255, 0.36)",
      600: "rgba(255, 255, 255, 0.48)",
      700: "rgba(255, 255, 255, 0.64)",
      800: "rgba(255, 255, 255, 0.80)",
      900: "rgba(255, 255, 255, 0.92)"
    },
    blackAlpha: {
      50: "rgba(0, 0, 0, 0.04)",
      100: "rgba(0, 0, 0, 0.06)",
      200: "rgba(0, 0, 0, 0.08)",
      300: "rgba(0, 0, 0, 0.16)",
      400: "rgba(0, 0, 0, 0.24)",
      500: "rgba(0, 0, 0, 0.36)",
      600: "rgba(0, 0, 0, 0.48)",
      700: "rgba(0, 0, 0, 0.64)",
      800: "rgba(0, 0, 0, 0.80)",
      900: "rgba(0, 0, 0, 0.92)"
    },
    gray: {
      50: "#F7FAFC",
      100: "#EDF2F7",
      200: "#E2E8F0",
      300: "#CBD5E0",
      400: "#A0AEC0",
      500: "#718096",
      600: "#4A5568",
      700: "#2D3748",
      800: "#1A202C",
      900: "#171923"
    },
    red: {
      50: "#FFF5F5",
      100: "#FED7D7",
      200: "#FEB2B2",
      300: "#FC8181",
      400: "#F56565",
      500: "#E53E3E",
      600: "#C53030",
      700: "#9B2C2C",
      800: "#822727",
      900: "#63171B"
    },
    orange: {
      50: "#FFFAF0",
      100: "#FEEBC8",
      200: "#FBD38D",
      300: "#F6AD55",
      400: "#ED8936",
      500: "#DD6B20",
      600: "#C05621",
      700: "#9C4221",
      800: "#7B341E",
      900: "#652B19"
    },
    yellow: {
      50: "#FFFFF0",
      100: "#FEFCBF",
      200: "#FAF089",
      300: "#F6E05E",
      400: "#ECC94B",
      500: "#D69E2E",
      600: "#B7791F",
      700: "#975A16",
      800: "#744210",
      900: "#5F370E"
    },
    green: {
      50: "#F0FFF4",
      100: "#C6F6D5",
      200: "#9AE6B4",
      300: "#68D391",
      400: "#48BB78",
      500: "#38A169",
      600: "#2F855A",
      700: "#276749",
      800: "#22543D",
      900: "#1C4532"
    },
    teal: {
      50: "#E6FFFA",
      100: "#B2F5EA",
      200: "#81E6D9",
      300: "#4FD1C5",
      400: "#38B2AC",
      500: "#319795",
      600: "#2C7A7B",
      700: "#285E61",
      800: "#234E52",
      900: "#1D4044"
    },
    blue: {
      50: "#ebf8ff",
      100: "#bee3f8",
      200: "#90cdf4",
      300: "#63b3ed",
      400: "#4299e1",
      500: "#3182ce",
      600: "#2b6cb0",
      700: "#2c5282",
      800: "#2a4365",
      900: "#1A365D"
    },
    cyan: {
      50: "#EDFDFD",
      100: "#C4F1F9",
      200: "#9DECF9",
      300: "#76E4F7",
      400: "#0BC5EA",
      500: "#00B5D8",
      600: "#00A3C4",
      700: "#0987A0",
      800: "#086F83",
      900: "#065666"
    },
    purple: {
      50: "#FAF5FF",
      100: "#E9D8FD",
      200: "#D6BCFA",
      300: "#B794F4",
      400: "#9F7AEA",
      500: "#805AD5",
      600: "#6B46C1",
      700: "#553C9A",
      800: "#44337A",
      900: "#322659"
    },
    pink: {
      50: "#FFF5F7",
      100: "#FED7E2",
      200: "#FBB6CE",
      300: "#F687B3",
      400: "#ED64A6",
      500: "#D53F8C",
      600: "#B83280",
      700: "#97266D",
      800: "#702459",
      900: "#521B41"
    },
    linkedin: {
      50: "#E8F4F9",
      100: "#CFEDFB",
      200: "#9BDAF3",
      300: "#68C7EC",
      400: "#34B3E4",
      500: "#00A0DC",
      600: "#008CC9",
      700: "#0077B5",
      800: "#005E93",
      900: "#004471"
    },
    facebook: {
      50: "#E8F4F9",
      100: "#D9DEE9",
      200: "#B7C2DA",
      300: "#6482C0",
      400: "#4267B2",
      500: "#385898",
      600: "#314E89",
      700: "#29487D",
      800: "#223B67",
      900: "#1E355B"
    },
    messenger: {
      50: "#D0E6FF",
      100: "#B9DAFF",
      200: "#A2CDFF",
      300: "#7AB8FF",
      400: "#2E90FF",
      500: "#0078FF",
      600: "#0063D1",
      700: "#0052AC",
      800: "#003C7E",
      900: "#002C5C"
    },
    whatsapp: {
      50: "#dffeec",
      100: "#b9f5d0",
      200: "#90edb3",
      300: "#65e495",
      400: "#3cdd78",
      500: "#22c35e",
      600: "#179848",
      700: "#0c6c33",
      800: "#01421c",
      900: "#001803"
    },
    twitter: {
      50: "#E5F4FD",
      100: "#C8E9FB",
      200: "#A8DCFA",
      300: "#83CDF7",
      400: "#57BBF5",
      500: "#1DA1F2",
      600: "#1A94DA",
      700: "#1681BF",
      800: "#136B9E",
      900: "#0D4D71"
    },
    telegram: {
      50: "#E3F2F9",
      100: "#C5E4F3",
      200: "#A2D4EC",
      300: "#7AC1E4",
      400: "#47A9DA",
      500: "#0088CC",
      600: "#007AB8",
      700: "#006BA1",
      800: "#005885",
      900: "#003F5E"
    }
  };
  var colors_default = colors;
  var radii = {
    none: "0",
    sm: "0.125rem",
    base: "0.25rem",
    md: "0.375rem",
    lg: "0.5rem",
    xl: "0.75rem",
    "2xl": "1rem",
    "3xl": "1.5rem",
    full: "9999px"
  };
  var radius_default = radii;
  var shadows = {
    xs: "0 0 0 1px rgba(0, 0, 0, 0.05)",
    sm: "0 1px 2px 0 rgba(0, 0, 0, 0.05)",
    base: "0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06)",
    md: "0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)",
    lg: "0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05)",
    xl: "0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04)",
    "2xl": "0 25px 50px -12px rgba(0, 0, 0, 0.25)",
    outline: "0 0 0 3px rgba(66, 153, 225, 0.6)",
    inner: "inset 0 2px 4px 0 rgba(0,0,0,0.06)",
    none: "none",
    "dark-lg": "rgba(0, 0, 0, 0.1) 0px 0px 0px 1px, rgba(0, 0, 0, 0.2) 0px 5px 10px, rgba(0, 0, 0, 0.4) 0px 15px 40px"
  };
  var shadows_default = shadows;
  var blur = {
    none: 0,
    sm: "4px",
    base: "8px",
    md: "12px",
    lg: "16px",
    xl: "24px",
    "2xl": "40px",
    "3xl": "64px"
  };
  var blur_default = blur;
  var typography = {
    letterSpacings: {
      tighter: "-0.05em",
      tight: "-0.025em",
      normal: "0",
      wide: "0.025em",
      wider: "0.05em",
      widest: "0.1em"
    },
    lineHeights: {
      normal: "normal",
      none: 1,
      shorter: 1.25,
      short: 1.375,
      base: 1.5,
      tall: 1.625,
      taller: "2",
      "3": ".75rem",
      "4": "1rem",
      "5": "1.25rem",
      "6": "1.5rem",
      "7": "1.75rem",
      "8": "2rem",
      "9": "2.25rem",
      "10": "2.5rem"
    },
    fontWeights: {
      hairline: 100,
      thin: 200,
      light: 300,
      normal: 400,
      medium: 500,
      semibold: 600,
      bold: 700,
      extrabold: 800,
      black: 900
    },
    fonts: {
      heading: `-apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif, "Apple Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol"`,
      body: `-apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif, "Apple Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol"`,
      mono: `SFMono-Regular,Menlo,Monaco,Consolas,"Liberation Mono","Courier New",monospace`
    },
    fontSizes: {
      "3xs": "0.45rem",
      "2xs": "0.625rem",
      xs: "0.75rem",
      sm: "0.875rem",
      md: "1rem",
      lg: "1.125rem",
      xl: "1.25rem",
      "2xl": "1.5rem",
      "3xl": "1.875rem",
      "4xl": "2.25rem",
      "5xl": "3rem",
      "6xl": "3.75rem",
      "7xl": "4.5rem",
      "8xl": "6rem",
      "9xl": "8rem"
    }
  };
  var typography_default = typography;
  var spacing = {
    px: "1px",
    0.5: "0.125rem",
    1: "0.25rem",
    1.5: "0.375rem",
    2: "0.5rem",
    2.5: "0.625rem",
    3: "0.75rem",
    3.5: "0.875rem",
    4: "1rem",
    5: "1.25rem",
    6: "1.5rem",
    7: "1.75rem",
    8: "2rem",
    9: "2.25rem",
    10: "2.5rem",
    12: "3rem",
    14: "3.5rem",
    16: "4rem",
    20: "5rem",
    24: "6rem",
    28: "7rem",
    32: "8rem",
    36: "9rem",
    40: "10rem",
    44: "11rem",
    48: "12rem",
    52: "13rem",
    56: "14rem",
    60: "15rem",
    64: "16rem",
    72: "18rem",
    80: "20rem",
    96: "24rem"
  };
  var largeSizes = {
    max: "max-content",
    min: "min-content",
    full: "100%",
    "3xs": "14rem",
    "2xs": "16rem",
    xs: "20rem",
    sm: "24rem",
    md: "28rem",
    lg: "32rem",
    xl: "36rem",
    "2xl": "42rem",
    "3xl": "48rem",
    "4xl": "56rem",
    "5xl": "64rem",
    "6xl": "72rem",
    "7xl": "80rem",
    "8xl": "90rem",
    prose: "60ch"
  };
  var container = {
    sm: "640px",
    md: "768px",
    lg: "1024px",
    xl: "1280px"
  };
  var sizes$m = {
    ...spacing,
    ...largeSizes,
    container
  };
  var sizes_default = sizes$m;
  var foundations = {
    breakpoints: breakpoints_default,
    zIndices: z_index_default,
    radii: radius_default,
    blur: blur_default,
    colors: colors_default,
    ...typography_default,
    sizes: sizes_default,
    shadows: shadows_default,
    space: spacing,
    borders: borders_default,
    transition: transition_default
  };
  var { defineMultiStyleConfig: defineMultiStyleConfig$p, definePartsStyle: definePartsStyle$p } = createMultiStyleConfigHelpers([
    "stepper",
    "step",
    "title",
    "description",
    "indicator",
    "separator",
    "icon",
    "number"
  ]);
  var $size$4 = cssVar$1("stepper-indicator-size");
  var $iconSize = cssVar$1("stepper-icon-size");
  var $titleFontSize = cssVar$1("stepper-title-font-size");
  var $descFontSize = cssVar$1("stepper-description-font-size");
  var $accentColor = cssVar$1("stepper-accent-color");
  var baseStyle$F = definePartsStyle$p(({ colorScheme: c2 }) => ({
    stepper: {
      display: "flex",
      justifyContent: "space-between",
      gap: "4",
      "&[data-orientation=vertical]": {
        flexDirection: "column",
        alignItems: "flex-start"
      },
      "&[data-orientation=horizontal]": {
        flexDirection: "row",
        alignItems: "center"
      },
      [$accentColor.variable]: `colors.${c2}.500`,
      _dark: {
        [$accentColor.variable]: `colors.${c2}.200`
      }
    },
    title: {
      fontSize: $titleFontSize.reference,
      fontWeight: "medium"
    },
    description: {
      fontSize: $descFontSize.reference,
      color: "chakra-subtle-text"
    },
    number: {
      fontSize: $titleFontSize.reference
    },
    step: {
      flexShrink: 0,
      position: "relative",
      display: "flex",
      gap: "2",
      "&[data-orientation=horizontal]": {
        alignItems: "center"
      },
      flex: "1",
      "&:last-of-type:not([data-stretch])": {
        flex: "initial"
      }
    },
    icon: {
      flexShrink: 0,
      width: $iconSize.reference,
      height: $iconSize.reference
    },
    indicator: {
      flexShrink: 0,
      borderRadius: "full",
      width: $size$4.reference,
      height: $size$4.reference,
      display: "flex",
      justifyContent: "center",
      alignItems: "center",
      "&[data-status=active]": {
        borderWidth: "2px",
        borderColor: $accentColor.reference
      },
      "&[data-status=complete]": {
        bg: $accentColor.reference,
        color: "chakra-inverse-text"
      },
      "&[data-status=incomplete]": {
        borderWidth: "2px"
      }
    },
    separator: {
      bg: "chakra-border-color",
      flex: "1",
      "&[data-status=complete]": {
        bg: $accentColor.reference
      },
      "&[data-orientation=horizontal]": {
        width: "100%",
        height: "2px",
        marginStart: "2"
      },
      "&[data-orientation=vertical]": {
        width: "2px",
        position: "absolute",
        height: "100%",
        maxHeight: `calc(100% - ${$size$4.reference} - 8px)`,
        top: `calc(${$size$4.reference} + 4px)`,
        insetStart: `calc(${$size$4.reference} / 2 - 1px)`
      }
    }
  }));
  var stepperTheme = defineMultiStyleConfig$p({
    baseStyle: baseStyle$F,
    sizes: {
      xs: definePartsStyle$p({
        stepper: {
          [$size$4.variable]: "sizes.4",
          [$iconSize.variable]: "sizes.3",
          [$titleFontSize.variable]: "fontSizes.xs",
          [$descFontSize.variable]: "fontSizes.xs"
        }
      }),
      sm: definePartsStyle$p({
        stepper: {
          [$size$4.variable]: "sizes.6",
          [$iconSize.variable]: "sizes.4",
          [$titleFontSize.variable]: "fontSizes.sm",
          [$descFontSize.variable]: "fontSizes.xs"
        }
      }),
      md: definePartsStyle$p({
        stepper: {
          [$size$4.variable]: "sizes.8",
          [$iconSize.variable]: "sizes.5",
          [$titleFontSize.variable]: "fontSizes.md",
          [$descFontSize.variable]: "fontSizes.sm"
        }
      }),
      lg: definePartsStyle$p({
        stepper: {
          [$size$4.variable]: "sizes.10",
          [$iconSize.variable]: "sizes.6",
          [$titleFontSize.variable]: "fontSizes.lg",
          [$descFontSize.variable]: "fontSizes.md"
        }
      })
    },
    defaultProps: {
      size: "md",
      colorScheme: "blue"
    }
  });
  function anatomy(name, map = {}) {
    let called = false;
    function assert() {
      if (!called) {
        called = true;
        return;
      }
      throw new Error(
        "[anatomy] .part(...) should only be called once. Did you mean to use .extend(...) ?"
      );
    }
    function parts(...values) {
      assert();
      for (const part of values) {
        map[part] = toPart(part);
      }
      return anatomy(name, map);
    }
    function extend(...parts2) {
      for (const part of parts2) {
        if (part in map)
          continue;
        map[part] = toPart(part);
      }
      return anatomy(name, map);
    }
    function selectors() {
      const value = Object.fromEntries(
        Object.entries(map).map(([key, part]) => [key, part.selector])
      );
      return value;
    }
    function classnames() {
      const value = Object.fromEntries(
        Object.entries(map).map(([key, part]) => [key, part.className])
      );
      return value;
    }
    function toPart(part) {
      const el2 = ["container", "root"].includes(part != null ? part : "") ? [name] : [name, part];
      const attr = el2.filter(Boolean).join("__");
      const className = `chakra-${attr}`;
      const partObj = {
        className,
        selector: `.${className}`,
        toString: () => part
      };
      return partObj;
    }
    const __type = {};
    return {
      parts,
      toPart,
      extend,
      selectors,
      classnames,
      get keys() {
        return Object.keys(map);
      },
      __type
    };
  }
  var accordionAnatomy = anatomy("accordion").parts("root", "container", "button", "panel").extend("icon");
  var alertAnatomy = anatomy("alert").parts("title", "description", "container").extend("icon", "spinner");
  var avatarAnatomy = anatomy("avatar").parts("label", "badge", "container").extend("excessLabel", "group");
  var breadcrumbAnatomy = anatomy("breadcrumb").parts("link", "item", "container").extend("separator");
  anatomy("button").parts();
  var checkboxAnatomy = anatomy("checkbox").parts("control", "icon", "container").extend("label");
  anatomy("progress").parts("track", "filledTrack").extend("label");
  var drawerAnatomy = anatomy("drawer").parts("overlay", "dialogContainer", "dialog").extend("header", "closeButton", "body", "footer");
  var editableAnatomy = anatomy("editable").parts(
    "preview",
    "input",
    "textarea"
  );
  var formAnatomy = anatomy("form").parts(
    "container",
    "requiredIndicator",
    "helperText"
  );
  var formErrorAnatomy = anatomy("formError").parts("text", "icon");
  var inputAnatomy = anatomy("input").parts(
    "addon",
    "field",
    "element",
    "group"
  );
  var listAnatomy = anatomy("list").parts("container", "item", "icon");
  var menuAnatomy = anatomy("menu").parts("button", "list", "item").extend("groupTitle", "icon", "command", "divider");
  var modalAnatomy = anatomy("modal").parts("overlay", "dialogContainer", "dialog").extend("header", "closeButton", "body", "footer");
  var numberInputAnatomy = anatomy("numberinput").parts(
    "root",
    "field",
    "stepperGroup",
    "stepper"
  );
  anatomy("pininput").parts("field");
  var popoverAnatomy = anatomy("popover").parts("content", "header", "body", "footer").extend("popper", "arrow", "closeButton");
  var progressAnatomy = anatomy("progress").parts(
    "label",
    "filledTrack",
    "track"
  );
  var radioAnatomy = anatomy("radio").parts(
    "container",
    "control",
    "label"
  );
  var selectAnatomy = anatomy("select").parts("field", "icon");
  var sliderAnatomy = anatomy("slider").parts(
    "container",
    "track",
    "thumb",
    "filledTrack",
    "mark"
  );
  var statAnatomy = anatomy("stat").parts(
    "container",
    "label",
    "helpText",
    "number",
    "icon"
  );
  var switchAnatomy = anatomy("switch").parts(
    "container",
    "track",
    "thumb",
    "label"
  );
  var tableAnatomy = anatomy("table").parts(
    "table",
    "thead",
    "tbody",
    "tr",
    "th",
    "td",
    "tfoot",
    "caption"
  );
  var tabsAnatomy = anatomy("tabs").parts(
    "root",
    "tab",
    "tablist",
    "tabpanel",
    "tabpanels",
    "indicator"
  );
  var tagAnatomy = anatomy("tag").parts(
    "container",
    "label",
    "closeButton"
  );
  var cardAnatomy = anatomy("card").parts(
    "container",
    "header",
    "body",
    "footer"
  );
  anatomy("stepper").parts(
    "stepper",
    "step",
    "title",
    "description",
    "indicator",
    "separator",
    "icon",
    "number"
  );
  function guard(low, high, value) {
    return Math.min(Math.max(low, value), high);
  }
  class ColorError extends Error {
    constructor(color2) {
      super(`Failed to parse color: "${color2}"`);
    }
  }
  var ColorError$1 = ColorError;
  function parseToRgba(color2) {
    if (typeof color2 !== "string")
      throw new ColorError$1(color2);
    if (color2.trim().toLowerCase() === "transparent")
      return [0, 0, 0, 0];
    let normalizedColor = color2.trim();
    normalizedColor = namedColorRegex.test(color2) ? nameToHex(color2) : color2;
    const reducedHexMatch = reducedHexRegex.exec(normalizedColor);
    if (reducedHexMatch) {
      const arr = Array.from(reducedHexMatch).slice(1);
      return [...arr.slice(0, 3).map((x2) => parseInt(r(x2, 2), 16)), parseInt(r(arr[3] || "f", 2), 16) / 255];
    }
    const hexMatch = hexRegex.exec(normalizedColor);
    if (hexMatch) {
      const arr = Array.from(hexMatch).slice(1);
      return [...arr.slice(0, 3).map((x2) => parseInt(x2, 16)), parseInt(arr[3] || "ff", 16) / 255];
    }
    const rgbaMatch = rgbaRegex.exec(normalizedColor);
    if (rgbaMatch) {
      const arr = Array.from(rgbaMatch).slice(1);
      return [...arr.slice(0, 3).map((x2) => parseInt(x2, 10)), parseFloat(arr[3] || "1")];
    }
    const hslaMatch = hslaRegex.exec(normalizedColor);
    if (hslaMatch) {
      const [h2, s, l2, a] = Array.from(hslaMatch).slice(1).map(parseFloat);
      if (guard(0, 100, s) !== s)
        throw new ColorError$1(color2);
      if (guard(0, 100, l2) !== l2)
        throw new ColorError$1(color2);
      return [...hslToRgb(h2, s, l2), Number.isNaN(a) ? 1 : a];
    }
    throw new ColorError$1(color2);
  }
  function hash$1(str) {
    let hash2 = 5381;
    let i = str.length;
    while (i) {
      hash2 = hash2 * 33 ^ str.charCodeAt(--i);
    }
    return (hash2 >>> 0) % 2341;
  }
  const colorToInt = (x2) => parseInt(x2.replace(/_/g, ""), 36);
  const compressedColorMap = "1q29ehhb 1n09sgk7 1kl1ekf_ _yl4zsno 16z9eiv3 1p29lhp8 _bd9zg04 17u0____ _iw9zhe5 _to73___ _r45e31e _7l6g016 _jh8ouiv _zn3qba8 1jy4zshs 11u87k0u 1ro9yvyo 1aj3xael 1gz9zjz0 _3w8l4xo 1bf1ekf_ _ke3v___ _4rrkb__ 13j776yz _646mbhl _nrjr4__ _le6mbhl 1n37ehkb _m75f91n _qj3bzfz 1939yygw 11i5z6x8 _1k5f8xs 1509441m 15t5lwgf _ae2th1n _tg1ugcv 1lp1ugcv 16e14up_ _h55rw7n _ny9yavn _7a11xb_ 1ih442g9 _pv442g9 1mv16xof 14e6y7tu 1oo9zkds 17d1cisi _4v9y70f _y98m8kc 1019pq0v 12o9zda8 _348j4f4 1et50i2o _8epa8__ _ts6senj 1o350i2o 1mi9eiuo 1259yrp0 1ln80gnw _632xcoy 1cn9zldc _f29edu4 1n490c8q _9f9ziet 1b94vk74 _m49zkct 1kz6s73a 1eu9dtog _q58s1rz 1dy9sjiq __u89jo3 _aj5nkwg _ld89jo3 13h9z6wx _qa9z2ii _l119xgq _bs5arju 1hj4nwk9 1qt4nwk9 1ge6wau6 14j9zlcw 11p1edc_ _ms1zcxe _439shk6 _jt9y70f _754zsow 1la40eju _oq5p___ _x279qkz 1fa5r3rv _yd2d9ip _424tcku _8y1di2_ _zi2uabw _yy7rn9h 12yz980_ __39ljp6 1b59zg0x _n39zfzp 1fy9zest _b33k___ _hp9wq92 1il50hz4 _io472ub _lj9z3eo 19z9ykg0 _8t8iu3a 12b9bl4a 1ak5yw0o _896v4ku _tb8k8lv _s59zi6t _c09ze0p 1lg80oqn 1id9z8wb _238nba5 1kq6wgdi _154zssg _tn3zk49 _da9y6tc 1sg7cv4f _r12jvtt 1gq5fmkz 1cs9rvci _lp9jn1c _xw1tdnb 13f9zje6 16f6973h _vo7ir40 _bt5arjf _rc45e4t _hr4e100 10v4e100 _hc9zke2 _w91egv_ _sj2r1kk 13c87yx8 _vqpds__ _ni8ggk8 _tj9yqfb 1ia2j4r4 _7x9b10u 1fc9ld4j 1eq9zldr _5j9lhpx _ez9zl6o _md61fzm".split(" ").reduce((acc, next2) => {
    const key = colorToInt(next2.substring(0, 3));
    const hex2 = colorToInt(next2.substring(3)).toString(16);
    let prefix2 = "";
    for (let i = 0; i < 6 - hex2.length; i++) {
      prefix2 += "0";
    }
    acc[key] = `${prefix2}${hex2}`;
    return acc;
  }, {});
  function nameToHex(color2) {
    const normalizedColorName = color2.toLowerCase().trim();
    const result = compressedColorMap[hash$1(normalizedColorName)];
    if (!result)
      throw new ColorError$1(color2);
    return `#${result}`;
  }
  const r = (str, amount) => Array.from(Array(amount)).map(() => str).join("");
  const reducedHexRegex = new RegExp(`^#${r("([a-f0-9])", 3)}([a-f0-9])?$`, "i");
  const hexRegex = new RegExp(`^#${r("([a-f0-9]{2})", 3)}([a-f0-9]{2})?$`, "i");
  const rgbaRegex = new RegExp(`^rgba?\\(\\s*(\\d+)\\s*${r(",\\s*(\\d+)\\s*", 2)}(?:,\\s*([\\d.]+))?\\s*\\)$`, "i");
  const hslaRegex = /^hsla?\(\s*([\d.]+)\s*,\s*([\d.]+)%\s*,\s*([\d.]+)%(?:\s*,\s*([\d.]+))?\s*\)$/i;
  const namedColorRegex = /^[a-z]+$/i;
  const roundColor = (color2) => {
    return Math.round(color2 * 255);
  };
  const hslToRgb = (hue, saturation, lightness) => {
    let l2 = lightness / 100;
    if (saturation === 0) {
      return [l2, l2, l2].map(roundColor);
    }
    const huePrime = (hue % 360 + 360) % 360 / 60;
    const chroma = (1 - Math.abs(2 * l2 - 1)) * (saturation / 100);
    const secondComponent = chroma * (1 - Math.abs(huePrime % 2 - 1));
    let red = 0;
    let green = 0;
    let blue = 0;
    if (huePrime >= 0 && huePrime < 1) {
      red = chroma;
      green = secondComponent;
    } else if (huePrime >= 1 && huePrime < 2) {
      red = secondComponent;
      green = chroma;
    } else if (huePrime >= 2 && huePrime < 3) {
      green = chroma;
      blue = secondComponent;
    } else if (huePrime >= 3 && huePrime < 4) {
      green = secondComponent;
      blue = chroma;
    } else if (huePrime >= 4 && huePrime < 5) {
      red = secondComponent;
      blue = chroma;
    } else if (huePrime >= 5 && huePrime < 6) {
      red = chroma;
      blue = secondComponent;
    }
    const lightnessModification = l2 - chroma / 2;
    const finalRed = red + lightnessModification;
    const finalGreen = green + lightnessModification;
    const finalBlue = blue + lightnessModification;
    return [finalRed, finalGreen, finalBlue].map(roundColor);
  };
  function rgba$1(red, green, blue, alpha2) {
    return `rgba(${guard(0, 255, red).toFixed()}, ${guard(0, 255, green).toFixed()}, ${guard(0, 255, blue).toFixed()}, ${parseFloat(guard(0, 1, alpha2).toFixed(3))})`;
  }
  function transparentize$1(color2, amount) {
    const [r2, g2, b2, a] = parseToRgba(color2);
    return rgba$1(r2, g2, b2, a - amount);
  }
  function toHex(color2) {
    const [r2, g2, b2, a] = parseToRgba(color2);
    let hex2 = (x2) => {
      const h2 = guard(0, 255, x2).toString(16);
      return h2.length === 1 ? `0${h2}` : h2;
    };
    return `#${hex2(r2)}${hex2(g2)}${hex2(b2)}${a < 1 ? hex2(Math.round(a * 255)) : ""}`;
  }
  function dlv_es_default(t2, e2, l2, n2, r2) {
    for (e2 = e2.split ? e2.split(".") : e2, n2 = 0; n2 < e2.length; n2++)
      t2 = t2 ? t2[e2[n2]] : r2;
    return t2 === r2 ? l2 : t2;
  }
  var isEmptyObject = (obj) => Object.keys(obj).length === 0;
  var getColor = (theme2, color2, fallback) => {
    const hex2 = dlv_es_default(theme2, `colors.${color2}`, color2);
    try {
      toHex(hex2);
      return hex2;
    } catch {
      return fallback != null ? fallback : "#000000";
    }
  };
  var getBrightness = (color2) => {
    const [r2, g2, b2] = parseToRgba(color2);
    return (r2 * 299 + g2 * 587 + b2 * 114) / 1e3;
  };
  var tone = (color2) => (theme2) => {
    const hex2 = getColor(theme2, color2);
    const brightness = getBrightness(hex2);
    const isDark2 = brightness < 128;
    return isDark2 ? "dark" : "light";
  };
  var isDark = (color2) => (theme2) => tone(color2)(theme2) === "dark";
  var transparentize = (color2, opacity) => (theme2) => {
    const raw = getColor(theme2, color2);
    return transparentize$1(raw, 1 - opacity);
  };
  function generateStripe(size2 = "1rem", color2 = "rgba(255, 255, 255, 0.15)") {
    return {
      backgroundImage: `linear-gradient(
    45deg,
    ${color2} 25%,
    transparent 25%,
    transparent 50%,
    ${color2} 50%,
    ${color2} 75%,
    transparent 75%,
    transparent
  )`,
      backgroundSize: `${size2} ${size2}`
    };
  }
  var randomHex = () => `#${Math.floor(Math.random() * 16777215).toString(16).padEnd(6, "0")}`;
  function randomColor(opts) {
    const fallback = randomHex();
    if (!opts || isEmptyObject(opts)) {
      return fallback;
    }
    if (opts.string && opts.colors) {
      return randomColorFromList(opts.string, opts.colors);
    }
    if (opts.string && !opts.colors) {
      return randomColorFromString(opts.string);
    }
    if (opts.colors && !opts.string) {
      return randomFromList(opts.colors);
    }
    return fallback;
  }
  function randomColorFromString(str) {
    let hash2 = 0;
    if (str.length === 0)
      return hash2.toString();
    for (let i = 0; i < str.length; i += 1) {
      hash2 = str.charCodeAt(i) + ((hash2 << 5) - hash2);
      hash2 = hash2 & hash2;
    }
    let color2 = "#";
    for (let j2 = 0; j2 < 3; j2 += 1) {
      const value = hash2 >> j2 * 8 & 255;
      color2 += `00${value.toString(16)}`.substr(-2);
    }
    return color2;
  }
  function randomColorFromList(str, list2) {
    let index = 0;
    if (str.length === 0)
      return list2[0];
    for (let i = 0; i < str.length; i += 1) {
      index = str.charCodeAt(i) + ((index << 5) - index);
      index = index & index;
    }
    index = (index % list2.length + list2.length) % list2.length;
    return list2[index];
  }
  function randomFromList(list2) {
    return list2[Math.floor(Math.random() * list2.length)];
  }
  function mode(light, dark) {
    return (props) => props.colorMode === "dark" ? dark : light;
  }
  function orient(options) {
    const { orientation, vertical, horizontal } = options;
    if (!orientation)
      return {};
    return orientation === "vertical" ? vertical : horizontal;
  }
  function toRef(operand) {
    if (isObject(operand) && operand.reference) {
      return operand.reference;
    }
    return String(operand);
  }
  var toExpr = (operator, ...operands) => operands.map(toRef).join(` ${operator} `).replace(/calc/g, "");
  var add = (...operands) => `calc(${toExpr("+", ...operands)})`;
  var subtract = (...operands) => `calc(${toExpr("-", ...operands)})`;
  var multiply = (...operands) => `calc(${toExpr("*", ...operands)})`;
  var divide = (...operands) => `calc(${toExpr("/", ...operands)})`;
  var negate = (x2) => {
    const value = toRef(x2);
    if (value != null && !Number.isNaN(parseFloat(value))) {
      return String(value).startsWith("-") ? String(value).slice(1) : `-${value}`;
    }
    return multiply(value, -1);
  };
  var calc = Object.assign(
    (x2) => ({
      add: (...operands) => calc(add(x2, ...operands)),
      subtract: (...operands) => calc(subtract(x2, ...operands)),
      multiply: (...operands) => calc(multiply(x2, ...operands)),
      divide: (...operands) => calc(divide(x2, ...operands)),
      negate: () => calc(negate(x2)),
      toString: () => x2.toString()
    }),
    {
      add,
      subtract,
      multiply,
      divide,
      negate
    }
  );
  function isDecimal(value) {
    return !Number.isInteger(parseFloat(value.toString()));
  }
  function replaceWhiteSpace(value, replaceValue = "-") {
    return value.replace(/\s+/g, replaceValue);
  }
  function escape(value) {
    const valueStr = replaceWhiteSpace(value.toString());
    if (valueStr.includes("\\."))
      return value;
    return isDecimal(value) ? valueStr.replace(".", `\\.`) : value;
  }
  function addPrefix(value, prefix2 = "") {
    return [prefix2, escape(value)].filter(Boolean).join("-");
  }
  function toVarRef(name, fallback) {
    return `var(${escape(name)}${fallback ? `, ${fallback}` : ""})`;
  }
  function toVar(value, prefix2 = "") {
    return `--${addPrefix(value, prefix2)}`;
  }
  function cssVar(name, options) {
    const cssVariable = toVar(name, void 0);
    return {
      variable: cssVariable,
      reference: toVarRef(cssVariable, getFallback(void 0))
    };
  }
  function getFallback(fallback) {
    if (typeof fallback === "string")
      return fallback;
    return fallback == null ? void 0 : fallback.reference;
  }
  var { defineMultiStyleConfig: defineMultiStyleConfig$o, definePartsStyle: definePartsStyle$o } = createMultiStyleConfigHelpers(switchAnatomy.keys);
  var $width = cssVar("switch-track-width");
  var $height$1 = cssVar("switch-track-height");
  var $diff = cssVar("switch-track-diff");
  var diffValue = calc.subtract($width, $height$1);
  var $translateX = cssVar("switch-thumb-x");
  var $bg$f = cssVar("switch-bg");
  var baseStyleTrack$2 = defineStyle((props) => {
    const { colorScheme: c2 } = props;
    return {
      borderRadius: "full",
      p: "0.5",
      width: [$width.reference],
      height: [$height$1.reference],
      transitionProperty: "common",
      transitionDuration: "fast",
      [$bg$f.variable]: "colors.gray.300",
      _dark: {
        [$bg$f.variable]: "colors.whiteAlpha.400"
      },
      _focusVisible: {
        boxShadow: "outline"
      },
      _disabled: {
        opacity: 0.4,
        cursor: "not-allowed"
      },
      _checked: {
        [$bg$f.variable]: `colors.${c2}.500`,
        _dark: {
          [$bg$f.variable]: `colors.${c2}.200`
        }
      },
      bg: $bg$f.reference
    };
  });
  var baseStyleThumb$1 = defineStyle({
    bg: "white",
    transitionProperty: "transform",
    transitionDuration: "normal",
    borderRadius: "inherit",
    width: [$height$1.reference],
    height: [$height$1.reference],
    _checked: {
      transform: `translateX(${$translateX.reference})`
    }
  });
  var baseStyle$E = definePartsStyle$o((props) => ({
    container: {
      [$diff.variable]: diffValue,
      [$translateX.variable]: $diff.reference,
      _rtl: {
        [$translateX.variable]: calc($diff).negate().toString()
      }
    },
    track: baseStyleTrack$2(props),
    thumb: baseStyleThumb$1
  }));
  var sizes$l = {
    sm: definePartsStyle$o({
      container: {
        [$width.variable]: "1.375rem",
        [$height$1.variable]: "sizes.3"
      }
    }),
    md: definePartsStyle$o({
      container: {
        [$width.variable]: "1.875rem",
        [$height$1.variable]: "sizes.4"
      }
    }),
    lg: definePartsStyle$o({
      container: {
        [$width.variable]: "2.875rem",
        [$height$1.variable]: "sizes.6"
      }
    })
  };
  var switchTheme = defineMultiStyleConfig$o({
    baseStyle: baseStyle$E,
    sizes: sizes$l,
    defaultProps: {
      size: "md",
      colorScheme: "blue"
    }
  });
  var { defineMultiStyleConfig: defineMultiStyleConfig$n, definePartsStyle: definePartsStyle$n } = createMultiStyleConfigHelpers(tableAnatomy.keys);
  var baseStyle$D = definePartsStyle$n({
    table: {
      fontVariantNumeric: "lining-nums tabular-nums",
      borderCollapse: "collapse",
      width: "full"
    },
    th: {
      fontFamily: "heading",
      fontWeight: "bold",
      textTransform: "uppercase",
      letterSpacing: "wider",
      textAlign: "start"
    },
    td: {
      textAlign: "start"
    },
    caption: {
      mt: 4,
      fontFamily: "heading",
      textAlign: "center",
      fontWeight: "medium"
    }
  });
  var numericStyles = defineStyle({
    "&[data-is-numeric=true]": {
      textAlign: "end"
    }
  });
  var variantSimple = definePartsStyle$n((props) => {
    const { colorScheme: c2 } = props;
    return {
      th: {
        color: mode("gray.600", "gray.400")(props),
        borderBottom: "1px",
        borderColor: mode(`${c2}.100`, `${c2}.700`)(props),
        ...numericStyles
      },
      td: {
        borderBottom: "1px",
        borderColor: mode(`${c2}.100`, `${c2}.700`)(props),
        ...numericStyles
      },
      caption: {
        color: mode("gray.600", "gray.100")(props)
      },
      tfoot: {
        tr: {
          "&:last-of-type": {
            th: { borderBottomWidth: 0 }
          }
        }
      }
    };
  });
  var variantStripe = definePartsStyle$n((props) => {
    const { colorScheme: c2 } = props;
    return {
      th: {
        color: mode("gray.600", "gray.400")(props),
        borderBottom: "1px",
        borderColor: mode(`${c2}.100`, `${c2}.700`)(props),
        ...numericStyles
      },
      td: {
        borderBottom: "1px",
        borderColor: mode(`${c2}.100`, `${c2}.700`)(props),
        ...numericStyles
      },
      caption: {
        color: mode("gray.600", "gray.100")(props)
      },
      tbody: {
        tr: {
          "&:nth-of-type(odd)": {
            "th, td": {
              borderBottomWidth: "1px",
              borderColor: mode(`${c2}.100`, `${c2}.700`)(props)
            },
            td: {
              background: mode(`${c2}.100`, `${c2}.700`)(props)
            }
          }
        }
      },
      tfoot: {
        tr: {
          "&:last-of-type": {
            th: { borderBottomWidth: 0 }
          }
        }
      }
    };
  });
  var variants$b = {
    simple: variantSimple,
    striped: variantStripe,
    unstyled: defineStyle({})
  };
  var sizes$k = {
    sm: definePartsStyle$n({
      th: {
        px: "4",
        py: "1",
        lineHeight: "4",
        fontSize: "xs"
      },
      td: {
        px: "4",
        py: "2",
        fontSize: "sm",
        lineHeight: "4"
      },
      caption: {
        px: "4",
        py: "2",
        fontSize: "xs"
      }
    }),
    md: definePartsStyle$n({
      th: {
        px: "6",
        py: "3",
        lineHeight: "4",
        fontSize: "xs"
      },
      td: {
        px: "6",
        py: "4",
        lineHeight: "5"
      },
      caption: {
        px: "6",
        py: "2",
        fontSize: "sm"
      }
    }),
    lg: definePartsStyle$n({
      th: {
        px: "8",
        py: "4",
        lineHeight: "5",
        fontSize: "sm"
      },
      td: {
        px: "8",
        py: "5",
        lineHeight: "6"
      },
      caption: {
        px: "6",
        py: "2",
        fontSize: "md"
      }
    })
  };
  var tableTheme = defineMultiStyleConfig$n({
    baseStyle: baseStyle$D,
    variants: variants$b,
    sizes: sizes$k,
    defaultProps: {
      variant: "simple",
      size: "md",
      colorScheme: "gray"
    }
  });
  var $fg$5 = cssVar$1("tabs-color");
  var $bg$e = cssVar$1("tabs-bg");
  var $border$3 = cssVar$1("tabs-border-color");
  var { defineMultiStyleConfig: defineMultiStyleConfig$m, definePartsStyle: definePartsStyle$m } = createMultiStyleConfigHelpers(tabsAnatomy.keys);
  var baseStyleRoot$1 = defineStyle((props) => {
    const { orientation } = props;
    return {
      display: orientation === "vertical" ? "flex" : "block"
    };
  });
  var baseStyleTab = defineStyle((props) => {
    const { isFitted } = props;
    return {
      flex: isFitted ? 1 : void 0,
      transitionProperty: "common",
      transitionDuration: "normal",
      _focusVisible: {
        zIndex: 1,
        boxShadow: "outline"
      },
      _disabled: {
        cursor: "not-allowed",
        opacity: 0.4
      }
    };
  });
  var baseStyleTablist = defineStyle((props) => {
    const { align = "start", orientation } = props;
    const alignments = {
      end: "flex-end",
      center: "center",
      start: "flex-start"
    };
    return {
      justifyContent: alignments[align],
      flexDirection: orientation === "vertical" ? "column" : "row"
    };
  });
  var baseStyleTabpanel = defineStyle({
    p: 4
  });
  var baseStyle$C = definePartsStyle$m((props) => ({
    root: baseStyleRoot$1(props),
    tab: baseStyleTab(props),
    tablist: baseStyleTablist(props),
    tabpanel: baseStyleTabpanel
  }));
  var sizes$j = {
    sm: definePartsStyle$m({
      tab: {
        py: 1,
        px: 4,
        fontSize: "sm"
      }
    }),
    md: definePartsStyle$m({
      tab: {
        fontSize: "md",
        py: 2,
        px: 4
      }
    }),
    lg: definePartsStyle$m({
      tab: {
        fontSize: "lg",
        py: 3,
        px: 4
      }
    })
  };
  var variantLine = definePartsStyle$m((props) => {
    const { colorScheme: c2, orientation } = props;
    const isVertical = orientation === "vertical";
    const borderProp = isVertical ? "borderStart" : "borderBottom";
    const marginProp = isVertical ? "marginStart" : "marginBottom";
    return {
      tablist: {
        [borderProp]: "2px solid",
        borderColor: "inherit"
      },
      tab: {
        [borderProp]: "2px solid",
        borderColor: "transparent",
        [marginProp]: "-2px",
        _selected: {
          [$fg$5.variable]: `colors.${c2}.600`,
          _dark: {
            [$fg$5.variable]: `colors.${c2}.300`
          },
          borderColor: "currentColor"
        },
        _active: {
          [$bg$e.variable]: "colors.gray.200",
          _dark: {
            [$bg$e.variable]: "colors.whiteAlpha.300"
          }
        },
        _disabled: {
          _active: { bg: "none" }
        },
        color: $fg$5.reference,
        bg: $bg$e.reference
      }
    };
  });
  var variantEnclosed = definePartsStyle$m((props) => {
    const { colorScheme: c2 } = props;
    return {
      tab: {
        borderTopRadius: "md",
        border: "1px solid",
        borderColor: "transparent",
        mb: "-1px",
        [$border$3.variable]: "transparent",
        _selected: {
          [$fg$5.variable]: `colors.${c2}.600`,
          [$border$3.variable]: `colors.white`,
          _dark: {
            [$fg$5.variable]: `colors.${c2}.300`,
            [$border$3.variable]: `colors.gray.800`
          },
          borderColor: "inherit",
          borderBottomColor: $border$3.reference
        },
        color: $fg$5.reference
      },
      tablist: {
        mb: "-1px",
        borderBottom: "1px solid",
        borderColor: "inherit"
      }
    };
  });
  var variantEnclosedColored = definePartsStyle$m((props) => {
    const { colorScheme: c2 } = props;
    return {
      tab: {
        border: "1px solid",
        borderColor: "inherit",
        [$bg$e.variable]: "colors.gray.50",
        _dark: {
          [$bg$e.variable]: "colors.whiteAlpha.50"
        },
        mb: "-1px",
        _notLast: {
          marginEnd: "-1px"
        },
        _selected: {
          [$bg$e.variable]: "colors.white",
          [$fg$5.variable]: `colors.${c2}.600`,
          _dark: {
            [$bg$e.variable]: "colors.gray.800",
            [$fg$5.variable]: `colors.${c2}.300`
          },
          borderColor: "inherit",
          borderTopColor: "currentColor",
          borderBottomColor: "transparent"
        },
        color: $fg$5.reference,
        bg: $bg$e.reference
      },
      tablist: {
        mb: "-1px",
        borderBottom: "1px solid",
        borderColor: "inherit"
      }
    };
  });
  var variantSoftRounded = definePartsStyle$m((props) => {
    const { colorScheme: c2, theme: theme2 } = props;
    return {
      tab: {
        borderRadius: "full",
        fontWeight: "semibold",
        color: "gray.600",
        _selected: {
          color: getColor(theme2, `${c2}.700`),
          bg: getColor(theme2, `${c2}.100`)
        }
      }
    };
  });
  var variantSolidRounded = definePartsStyle$m((props) => {
    const { colorScheme: c2 } = props;
    return {
      tab: {
        borderRadius: "full",
        fontWeight: "semibold",
        [$fg$5.variable]: "colors.gray.600",
        _dark: {
          [$fg$5.variable]: "inherit"
        },
        _selected: {
          [$fg$5.variable]: "colors.white",
          [$bg$e.variable]: `colors.${c2}.600`,
          _dark: {
            [$fg$5.variable]: "colors.gray.800",
            [$bg$e.variable]: `colors.${c2}.300`
          }
        },
        color: $fg$5.reference,
        bg: $bg$e.reference
      }
    };
  });
  var variantUnstyled$2 = definePartsStyle$m({});
  var variants$a = {
    line: variantLine,
    enclosed: variantEnclosed,
    "enclosed-colored": variantEnclosedColored,
    "soft-rounded": variantSoftRounded,
    "solid-rounded": variantSolidRounded,
    unstyled: variantUnstyled$2
  };
  var tabsTheme = defineMultiStyleConfig$m({
    baseStyle: baseStyle$C,
    sizes: sizes$j,
    variants: variants$a,
    defaultProps: {
      size: "md",
      variant: "line",
      colorScheme: "blue"
    }
  });
  var vars = defineCssVars("badge", ["bg", "color", "shadow"]);
  var baseStyle$B = defineStyle({
    px: 1,
    textTransform: "uppercase",
    fontSize: "xs",
    borderRadius: "sm",
    fontWeight: "bold",
    bg: vars.bg.reference,
    color: vars.color.reference,
    boxShadow: vars.shadow.reference
  });
  var variantSolid$3 = defineStyle((props) => {
    const { colorScheme: c2, theme: theme2 } = props;
    const dark = transparentize(`${c2}.500`, 0.6)(theme2);
    return {
      [vars.bg.variable]: `colors.${c2}.500`,
      [vars.color.variable]: `colors.white`,
      _dark: {
        [vars.bg.variable]: dark,
        [vars.color.variable]: `colors.whiteAlpha.800`
      }
    };
  });
  var variantSubtle$1 = defineStyle((props) => {
    const { colorScheme: c2, theme: theme2 } = props;
    const darkBg = transparentize(`${c2}.200`, 0.16)(theme2);
    return {
      [vars.bg.variable]: `colors.${c2}.100`,
      [vars.color.variable]: `colors.${c2}.800`,
      _dark: {
        [vars.bg.variable]: darkBg,
        [vars.color.variable]: `colors.${c2}.200`
      }
    };
  });
  var variantOutline$2 = defineStyle((props) => {
    const { colorScheme: c2, theme: theme2 } = props;
    const darkColor = transparentize(`${c2}.200`, 0.8)(theme2);
    return {
      [vars.color.variable]: `colors.${c2}.500`,
      _dark: {
        [vars.color.variable]: darkColor
      },
      [vars.shadow.variable]: `inset 0 0 0px 1px ${vars.color.reference}`
    };
  });
  var variants$9 = {
    solid: variantSolid$3,
    subtle: variantSubtle$1,
    outline: variantOutline$2
  };
  var badgeTheme = defineStyleConfig({
    baseStyle: baseStyle$B,
    variants: variants$9,
    defaultProps: {
      variant: "subtle",
      colorScheme: "gray"
    }
  });
  var { defineMultiStyleConfig: defineMultiStyleConfig$l, definePartsStyle: definePartsStyle$l } = createMultiStyleConfigHelpers(tagAnatomy.keys);
  var $bg$d = cssVar$1("tag-bg");
  var $color = cssVar$1("tag-color");
  var $shadow$3 = cssVar$1("tag-shadow");
  var $minH = cssVar$1("tag-min-height");
  var $minW = cssVar$1("tag-min-width");
  var $fontSize$1 = cssVar$1("tag-font-size");
  var $paddingX = cssVar$1("tag-padding-inline");
  var baseStyleContainer$4 = defineStyle({
    fontWeight: "medium",
    lineHeight: 1.2,
    outline: 0,
    [$color.variable]: vars.color.reference,
    [$bg$d.variable]: vars.bg.reference,
    [$shadow$3.variable]: vars.shadow.reference,
    color: $color.reference,
    bg: $bg$d.reference,
    boxShadow: $shadow$3.reference,
    borderRadius: "md",
    minH: $minH.reference,
    minW: $minW.reference,
    fontSize: $fontSize$1.reference,
    px: $paddingX.reference,
    _focusVisible: {
      [$shadow$3.variable]: "shadows.outline"
    }
  });
  var baseStyleLabel$4 = defineStyle({
    lineHeight: 1.2,
    overflow: "visible"
  });
  var baseStyleCloseButton$3 = defineStyle({
    fontSize: "lg",
    w: "5",
    h: "5",
    transitionProperty: "common",
    transitionDuration: "normal",
    borderRadius: "full",
    marginStart: "1.5",
    marginEnd: "-1",
    opacity: 0.5,
    _disabled: {
      opacity: 0.4
    },
    _focusVisible: {
      boxShadow: "outline",
      bg: "rgba(0, 0, 0, 0.14)"
    },
    _hover: {
      opacity: 0.8
    },
    _active: {
      opacity: 1
    }
  });
  var baseStyle$A = definePartsStyle$l({
    container: baseStyleContainer$4,
    label: baseStyleLabel$4,
    closeButton: baseStyleCloseButton$3
  });
  var sizes$i = {
    sm: definePartsStyle$l({
      container: {
        [$minH.variable]: "sizes.5",
        [$minW.variable]: "sizes.5",
        [$fontSize$1.variable]: "fontSizes.xs",
        [$paddingX.variable]: "space.2"
      },
      closeButton: {
        marginEnd: "-2px",
        marginStart: "0.35rem"
      }
    }),
    md: definePartsStyle$l({
      container: {
        [$minH.variable]: "sizes.6",
        [$minW.variable]: "sizes.6",
        [$fontSize$1.variable]: "fontSizes.sm",
        [$paddingX.variable]: "space.2"
      }
    }),
    lg: definePartsStyle$l({
      container: {
        [$minH.variable]: "sizes.8",
        [$minW.variable]: "sizes.8",
        [$fontSize$1.variable]: "fontSizes.md",
        [$paddingX.variable]: "space.3"
      }
    })
  };
  var variants$8 = {
    subtle: definePartsStyle$l((props) => {
      var _a4;
      return {
        container: (_a4 = badgeTheme.variants) == null ? void 0 : _a4.subtle(props)
      };
    }),
    solid: definePartsStyle$l((props) => {
      var _a4;
      return {
        container: (_a4 = badgeTheme.variants) == null ? void 0 : _a4.solid(props)
      };
    }),
    outline: definePartsStyle$l((props) => {
      var _a4;
      return {
        container: (_a4 = badgeTheme.variants) == null ? void 0 : _a4.outline(props)
      };
    })
  };
  var tagTheme = defineMultiStyleConfig$l({
    variants: variants$8,
    baseStyle: baseStyle$A,
    sizes: sizes$i,
    defaultProps: {
      size: "md",
      variant: "subtle",
      colorScheme: "gray"
    }
  });
  var { definePartsStyle: definePartsStyle$k, defineMultiStyleConfig: defineMultiStyleConfig$k } = createMultiStyleConfigHelpers(inputAnatomy.keys);
  var $height = cssVar$1("input-height");
  var $fontSize = cssVar$1("input-font-size");
  var $padding$1 = cssVar$1("input-padding");
  var $borderRadius = cssVar$1("input-border-radius");
  var baseStyle$z = definePartsStyle$k({
    addon: {
      height: $height.reference,
      fontSize: $fontSize.reference,
      px: $padding$1.reference,
      borderRadius: $borderRadius.reference
    },
    field: {
      width: "100%",
      height: $height.reference,
      fontSize: $fontSize.reference,
      px: $padding$1.reference,
      borderRadius: $borderRadius.reference,
      minWidth: 0,
      outline: 0,
      position: "relative",
      appearance: "none",
      transitionProperty: "common",
      transitionDuration: "normal",
      _disabled: {
        opacity: 0.4,
        cursor: "not-allowed"
      }
    }
  });
  var size = {
    lg: defineStyle({
      [$fontSize.variable]: "fontSizes.lg",
      [$padding$1.variable]: "space.4",
      [$borderRadius.variable]: "radii.md",
      [$height.variable]: "sizes.12"
    }),
    md: defineStyle({
      [$fontSize.variable]: "fontSizes.md",
      [$padding$1.variable]: "space.4",
      [$borderRadius.variable]: "radii.md",
      [$height.variable]: "sizes.10"
    }),
    sm: defineStyle({
      [$fontSize.variable]: "fontSizes.sm",
      [$padding$1.variable]: "space.3",
      [$borderRadius.variable]: "radii.sm",
      [$height.variable]: "sizes.8"
    }),
    xs: defineStyle({
      [$fontSize.variable]: "fontSizes.xs",
      [$padding$1.variable]: "space.2",
      [$borderRadius.variable]: "radii.sm",
      [$height.variable]: "sizes.6"
    })
  };
  var sizes$h = {
    lg: definePartsStyle$k({
      field: size.lg,
      group: size.lg
    }),
    md: definePartsStyle$k({
      field: size.md,
      group: size.md
    }),
    sm: definePartsStyle$k({
      field: size.sm,
      group: size.sm
    }),
    xs: definePartsStyle$k({
      field: size.xs,
      group: size.xs
    })
  };
  function getDefaults(props) {
    const { focusBorderColor: fc2, errorBorderColor: ec2 } = props;
    return {
      focusBorderColor: fc2 || mode("blue.500", "blue.300")(props),
      errorBorderColor: ec2 || mode("red.500", "red.300")(props)
    };
  }
  var variantOutline$1 = definePartsStyle$k((props) => {
    const { theme: theme2 } = props;
    const { focusBorderColor: fc2, errorBorderColor: ec2 } = getDefaults(props);
    return {
      field: {
        border: "1px solid",
        borderColor: "inherit",
        bg: "inherit",
        _hover: {
          borderColor: mode("gray.300", "whiteAlpha.400")(props)
        },
        _readOnly: {
          boxShadow: "none !important",
          userSelect: "all"
        },
        _invalid: {
          borderColor: getColor(theme2, ec2),
          boxShadow: `0 0 0 1px ${getColor(theme2, ec2)}`
        },
        _focusVisible: {
          zIndex: 1,
          borderColor: getColor(theme2, fc2),
          boxShadow: `0 0 0 1px ${getColor(theme2, fc2)}`
        }
      },
      addon: {
        border: "1px solid",
        borderColor: mode("inherit", "whiteAlpha.50")(props),
        bg: mode("gray.100", "whiteAlpha.300")(props)
      }
    };
  });
  var variantFilled = definePartsStyle$k((props) => {
    const { theme: theme2 } = props;
    const { focusBorderColor: fc2, errorBorderColor: ec2 } = getDefaults(props);
    return {
      field: {
        border: "2px solid",
        borderColor: "transparent",
        bg: mode("gray.100", "whiteAlpha.50")(props),
        _hover: {
          bg: mode("gray.200", "whiteAlpha.100")(props)
        },
        _readOnly: {
          boxShadow: "none !important",
          userSelect: "all"
        },
        _invalid: {
          borderColor: getColor(theme2, ec2)
        },
        _focusVisible: {
          bg: "transparent",
          borderColor: getColor(theme2, fc2)
        }
      },
      addon: {
        border: "2px solid",
        borderColor: "transparent",
        bg: mode("gray.100", "whiteAlpha.50")(props)
      }
    };
  });
  var variantFlushed = definePartsStyle$k((props) => {
    const { theme: theme2 } = props;
    const { focusBorderColor: fc2, errorBorderColor: ec2 } = getDefaults(props);
    return {
      field: {
        borderBottom: "1px solid",
        borderColor: "inherit",
        borderRadius: "0",
        px: "0",
        bg: "transparent",
        _readOnly: {
          boxShadow: "none !important",
          userSelect: "all"
        },
        _invalid: {
          borderColor: getColor(theme2, ec2),
          boxShadow: `0px 1px 0px 0px ${getColor(theme2, ec2)}`
        },
        _focusVisible: {
          borderColor: getColor(theme2, fc2),
          boxShadow: `0px 1px 0px 0px ${getColor(theme2, fc2)}`
        }
      },
      addon: {
        borderBottom: "2px solid",
        borderColor: "inherit",
        borderRadius: "0",
        px: "0",
        bg: "transparent"
      }
    };
  });
  var variantUnstyled$1 = definePartsStyle$k({
    field: {
      bg: "transparent",
      px: "0",
      height: "auto"
    },
    addon: {
      bg: "transparent",
      px: "0",
      height: "auto"
    }
  });
  var variants$7 = {
    outline: variantOutline$1,
    filled: variantFilled,
    flushed: variantFlushed,
    unstyled: variantUnstyled$1
  };
  var inputTheme = defineMultiStyleConfig$k({
    baseStyle: baseStyle$z,
    sizes: sizes$h,
    variants: variants$7,
    defaultProps: {
      size: "md",
      variant: "outline"
    }
  });
  var _a$3;
  var baseStyle$y = defineStyle({
    ...(_a$3 = inputTheme.baseStyle) == null ? void 0 : _a$3.field,
    paddingY: "2",
    minHeight: "20",
    lineHeight: "short",
    verticalAlign: "top"
  });
  var _a2$2, _b$2;
  var variants$6 = {
    outline: defineStyle(
      (props) => {
        var _a4, _b3;
        return (_b3 = (_a4 = inputTheme.variants) == null ? void 0 : _a4.outline(props).field) != null ? _b3 : {};
      }
    ),
    flushed: defineStyle(
      (props) => {
        var _a4, _b3;
        return (_b3 = (_a4 = inputTheme.variants) == null ? void 0 : _a4.flushed(props).field) != null ? _b3 : {};
      }
    ),
    filled: defineStyle(
      (props) => {
        var _a4, _b3;
        return (_b3 = (_a4 = inputTheme.variants) == null ? void 0 : _a4.filled(props).field) != null ? _b3 : {};
      }
    ),
    unstyled: (_b$2 = (_a2$2 = inputTheme.variants) == null ? void 0 : _a2$2.unstyled.field) != null ? _b$2 : {}
  };
  var _a3, _b2, _c$1, _d$1, _e$2, _f$1, _g$1, _h$1;
  var sizes$g = {
    xs: (_b2 = (_a3 = inputTheme.sizes) == null ? void 0 : _a3.xs.field) != null ? _b2 : {},
    sm: (_d$1 = (_c$1 = inputTheme.sizes) == null ? void 0 : _c$1.sm.field) != null ? _d$1 : {},
    md: (_f$1 = (_e$2 = inputTheme.sizes) == null ? void 0 : _e$2.md.field) != null ? _f$1 : {},
    lg: (_h$1 = (_g$1 = inputTheme.sizes) == null ? void 0 : _g$1.lg.field) != null ? _h$1 : {}
  };
  var textareaTheme = defineStyleConfig({
    baseStyle: baseStyle$y,
    sizes: sizes$g,
    variants: variants$6,
    defaultProps: {
      size: "md",
      variant: "outline"
    }
  });
  var $bg$c = cssVar("tooltip-bg");
  var $fg$4 = cssVar("tooltip-fg");
  var $arrowBg$1 = cssVar("popper-arrow-bg");
  var baseStyle$x = defineStyle({
    bg: $bg$c.reference,
    color: $fg$4.reference,
    [$bg$c.variable]: "colors.gray.700",
    [$fg$4.variable]: "colors.whiteAlpha.900",
    _dark: {
      [$bg$c.variable]: "colors.gray.300",
      [$fg$4.variable]: "colors.gray.900"
    },
    [$arrowBg$1.variable]: $bg$c.reference,
    px: "2",
    py: "0.5",
    borderRadius: "sm",
    fontWeight: "medium",
    fontSize: "sm",
    boxShadow: "md",
    maxW: "xs",
    zIndex: "tooltip"
  });
  var tooltipTheme = defineStyleConfig({
    baseStyle: baseStyle$x
  });
  var { defineMultiStyleConfig: defineMultiStyleConfig$j, definePartsStyle: definePartsStyle$j } = createMultiStyleConfigHelpers(progressAnatomy.keys);
  var filledStyle = defineStyle((props) => {
    const { colorScheme: c2, theme: t2, isIndeterminate, hasStripe } = props;
    const stripeStyle = mode(
      generateStripe(),
      generateStripe("1rem", "rgba(0,0,0,0.1)")
    )(props);
    const bgColor = mode(`${c2}.500`, `${c2}.200`)(props);
    const gradient = `linear-gradient(
    to right,
    transparent 0%,
    ${getColor(t2, bgColor)} 50%,
    transparent 100%
  )`;
    const addStripe = !isIndeterminate && hasStripe;
    return {
      ...addStripe && stripeStyle,
      ...isIndeterminate ? { bgImage: gradient } : { bgColor }
    };
  });
  var baseStyleLabel$3 = defineStyle({
    lineHeight: "1",
    fontSize: "0.25em",
    fontWeight: "bold",
    color: "white"
  });
  var baseStyleTrack$1 = defineStyle((props) => {
    return {
      bg: mode("gray.100", "whiteAlpha.300")(props)
    };
  });
  var baseStyleFilledTrack$1 = defineStyle((props) => {
    return {
      transitionProperty: "common",
      transitionDuration: "slow",
      ...filledStyle(props)
    };
  });
  var baseStyle$w = definePartsStyle$j((props) => ({
    label: baseStyleLabel$3,
    filledTrack: baseStyleFilledTrack$1(props),
    track: baseStyleTrack$1(props)
  }));
  var sizes$f = {
    xs: definePartsStyle$j({
      track: { h: "1" }
    }),
    sm: definePartsStyle$j({
      track: { h: "2" }
    }),
    md: definePartsStyle$j({
      track: { h: "3" }
    }),
    lg: definePartsStyle$j({
      track: { h: "4" }
    })
  };
  var progressTheme = defineMultiStyleConfig$j({
    sizes: sizes$f,
    baseStyle: baseStyle$w,
    defaultProps: {
      size: "md",
      colorScheme: "blue"
    }
  });
  var isFunction$2 = (value) => typeof value === "function";
  function runIfFn$1(valueOrFn, ...args) {
    return isFunction$2(valueOrFn) ? valueOrFn(...args) : valueOrFn;
  }
  var { definePartsStyle: definePartsStyle$i, defineMultiStyleConfig: defineMultiStyleConfig$i } = createMultiStyleConfigHelpers(checkboxAnatomy.keys);
  var $size$3 = cssVar$1("checkbox-size");
  var baseStyleControl$1 = defineStyle((props) => {
    const { colorScheme: c2 } = props;
    return {
      w: $size$3.reference,
      h: $size$3.reference,
      transitionProperty: "box-shadow",
      transitionDuration: "normal",
      border: "2px solid",
      borderRadius: "sm",
      borderColor: "inherit",
      color: "white",
      _checked: {
        bg: mode(`${c2}.500`, `${c2}.200`)(props),
        borderColor: mode(`${c2}.500`, `${c2}.200`)(props),
        color: mode("white", "gray.900")(props),
        _hover: {
          bg: mode(`${c2}.600`, `${c2}.300`)(props),
          borderColor: mode(`${c2}.600`, `${c2}.300`)(props)
        },
        _disabled: {
          borderColor: mode("gray.200", "transparent")(props),
          bg: mode("gray.200", "whiteAlpha.300")(props),
          color: mode("gray.500", "whiteAlpha.500")(props)
        }
      },
      _indeterminate: {
        bg: mode(`${c2}.500`, `${c2}.200`)(props),
        borderColor: mode(`${c2}.500`, `${c2}.200`)(props),
        color: mode("white", "gray.900")(props)
      },
      _disabled: {
        bg: mode("gray.100", "whiteAlpha.100")(props),
        borderColor: mode("gray.100", "transparent")(props)
      },
      _focusVisible: {
        boxShadow: "outline"
      },
      _invalid: {
        borderColor: mode("red.500", "red.300")(props)
      }
    };
  });
  var baseStyleContainer$3 = defineStyle({
    _disabled: { cursor: "not-allowed" }
  });
  var baseStyleLabel$2 = defineStyle({
    userSelect: "none",
    _disabled: { opacity: 0.4 }
  });
  var baseStyleIcon$6 = defineStyle({
    transitionProperty: "transform",
    transitionDuration: "normal"
  });
  var baseStyle$v = definePartsStyle$i((props) => ({
    icon: baseStyleIcon$6,
    container: baseStyleContainer$3,
    control: runIfFn$1(baseStyleControl$1, props),
    label: baseStyleLabel$2
  }));
  var sizes$e = {
    sm: definePartsStyle$i({
      control: { [$size$3.variable]: "sizes.3" },
      label: { fontSize: "sm" },
      icon: { fontSize: "3xs" }
    }),
    md: definePartsStyle$i({
      control: { [$size$3.variable]: "sizes.4" },
      label: { fontSize: "md" },
      icon: { fontSize: "2xs" }
    }),
    lg: definePartsStyle$i({
      control: { [$size$3.variable]: "sizes.5" },
      label: { fontSize: "lg" },
      icon: { fontSize: "2xs" }
    })
  };
  var checkboxTheme = defineMultiStyleConfig$i({
    baseStyle: baseStyle$v,
    sizes: sizes$e,
    defaultProps: {
      size: "md",
      colorScheme: "blue"
    }
  });
  var { defineMultiStyleConfig: defineMultiStyleConfig$h, definePartsStyle: definePartsStyle$h } = createMultiStyleConfigHelpers(radioAnatomy.keys);
  var baseStyleControl = defineStyle((props) => {
    var _a4;
    const controlStyle = (_a4 = runIfFn$1(checkboxTheme.baseStyle, props)) == null ? void 0 : _a4.control;
    return {
      ...controlStyle,
      borderRadius: "full",
      _checked: {
        ...controlStyle == null ? void 0 : controlStyle["_checked"],
        _before: {
          content: `""`,
          display: "inline-block",
          pos: "relative",
          w: "50%",
          h: "50%",
          borderRadius: "50%",
          bg: "currentColor"
        }
      }
    };
  });
  var baseStyle$u = definePartsStyle$h((props) => {
    var _a4, _b3, _c2, _d2;
    return {
      label: (_b3 = (_a4 = checkboxTheme).baseStyle) == null ? void 0 : _b3.call(_a4, props).label,
      container: (_d2 = (_c2 = checkboxTheme).baseStyle) == null ? void 0 : _d2.call(_c2, props).container,
      control: baseStyleControl(props)
    };
  });
  var sizes$d = {
    md: definePartsStyle$h({
      control: { w: "4", h: "4" },
      label: { fontSize: "md" }
    }),
    lg: definePartsStyle$h({
      control: { w: "5", h: "5" },
      label: { fontSize: "lg" }
    }),
    sm: definePartsStyle$h({
      control: { width: "3", height: "3" },
      label: { fontSize: "sm" }
    })
  };
  var radioTheme = defineMultiStyleConfig$h({
    baseStyle: baseStyle$u,
    sizes: sizes$d,
    defaultProps: {
      size: "md",
      colorScheme: "blue"
    }
  });
  var { defineMultiStyleConfig: defineMultiStyleConfig$g, definePartsStyle: definePartsStyle$g } = createMultiStyleConfigHelpers(selectAnatomy.keys);
  var $bg$b = cssVar$1("select-bg");
  var _a$2;
  var baseStyleField$1 = defineStyle({
    ...(_a$2 = inputTheme.baseStyle) == null ? void 0 : _a$2.field,
    appearance: "none",
    paddingBottom: "1px",
    lineHeight: "normal",
    bg: $bg$b.reference,
    [$bg$b.variable]: "colors.white",
    _dark: {
      [$bg$b.variable]: "colors.gray.700"
    },
    "> option, > optgroup": {
      bg: $bg$b.reference
    }
  });
  var baseStyleIcon$5 = defineStyle({
    width: "6",
    height: "100%",
    insetEnd: "2",
    position: "relative",
    color: "currentColor",
    fontSize: "xl",
    _disabled: {
      opacity: 0.5
    }
  });
  var baseStyle$t = definePartsStyle$g({
    field: baseStyleField$1,
    icon: baseStyleIcon$5
  });
  var iconSpacing = defineStyle({
    paddingInlineEnd: "8"
  });
  var _a2$1, _b$1, _c, _d, _e$1, _f, _g, _h;
  var sizes$c = {
    lg: {
      ...(_a2$1 = inputTheme.sizes) == null ? void 0 : _a2$1.lg,
      field: {
        ...(_b$1 = inputTheme.sizes) == null ? void 0 : _b$1.lg.field,
        ...iconSpacing
      }
    },
    md: {
      ...(_c = inputTheme.sizes) == null ? void 0 : _c.md,
      field: {
        ...(_d = inputTheme.sizes) == null ? void 0 : _d.md.field,
        ...iconSpacing
      }
    },
    sm: {
      ...(_e$1 = inputTheme.sizes) == null ? void 0 : _e$1.sm,
      field: {
        ...(_f = inputTheme.sizes) == null ? void 0 : _f.sm.field,
        ...iconSpacing
      }
    },
    xs: {
      ...(_g = inputTheme.sizes) == null ? void 0 : _g.xs,
      field: {
        ...(_h = inputTheme.sizes) == null ? void 0 : _h.xs.field,
        ...iconSpacing
      },
      icon: {
        insetEnd: "1"
      }
    }
  };
  var selectTheme = defineMultiStyleConfig$g({
    baseStyle: baseStyle$t,
    sizes: sizes$c,
    variants: inputTheme.variants,
    defaultProps: inputTheme.defaultProps
  });
  var $startColor = cssVar$1("skeleton-start-color");
  var $endColor = cssVar$1("skeleton-end-color");
  var baseStyle$s = defineStyle({
    [$startColor.variable]: "colors.gray.100",
    [$endColor.variable]: "colors.gray.400",
    _dark: {
      [$startColor.variable]: "colors.gray.800",
      [$endColor.variable]: "colors.gray.600"
    },
    background: $startColor.reference,
    borderColor: $endColor.reference,
    opacity: 0.7,
    borderRadius: "sm"
  });
  var skeletonTheme = defineStyleConfig({
    baseStyle: baseStyle$s
  });
  var $bg$a = cssVar$1("skip-link-bg");
  var baseStyle$r = defineStyle({
    borderRadius: "md",
    fontWeight: "semibold",
    _focusVisible: {
      boxShadow: "outline",
      padding: "4",
      position: "fixed",
      top: "6",
      insetStart: "6",
      [$bg$a.variable]: "colors.white",
      _dark: {
        [$bg$a.variable]: "colors.gray.700"
      },
      bg: $bg$a.reference
    }
  });
  var skipLinkTheme = defineStyleConfig({
    baseStyle: baseStyle$r
  });
  var { defineMultiStyleConfig: defineMultiStyleConfig$f, definePartsStyle: definePartsStyle$f } = createMultiStyleConfigHelpers(sliderAnatomy.keys);
  var $thumbSize = cssVar$1("slider-thumb-size");
  var $trackSize = cssVar$1("slider-track-size");
  var $bg$9 = cssVar$1("slider-bg");
  var baseStyleContainer$2 = defineStyle((props) => {
    const { orientation } = props;
    return {
      display: "inline-block",
      position: "relative",
      cursor: "pointer",
      _disabled: {
        opacity: 0.6,
        cursor: "default",
        pointerEvents: "none"
      },
      ...orient({
        orientation,
        vertical: { h: "100%" },
        horizontal: { w: "100%" }
      })
    };
  });
  var baseStyleTrack = defineStyle((props) => {
    const orientationStyles = orient({
      orientation: props.orientation,
      horizontal: { h: $trackSize.reference },
      vertical: { w: $trackSize.reference }
    });
    return {
      ...orientationStyles,
      overflow: "hidden",
      borderRadius: "sm",
      [$bg$9.variable]: "colors.gray.200",
      _dark: {
        [$bg$9.variable]: "colors.whiteAlpha.200"
      },
      _disabled: {
        [$bg$9.variable]: "colors.gray.300",
        _dark: {
          [$bg$9.variable]: "colors.whiteAlpha.300"
        }
      },
      bg: $bg$9.reference
    };
  });
  var baseStyleThumb = defineStyle((props) => {
    const { orientation } = props;
    const orientationStyle = orient({
      orientation,
      vertical: {
        left: "50%",
        transform: `translateX(-50%)`,
        _active: {
          transform: `translateX(-50%) scale(1.15)`
        }
      },
      horizontal: {
        top: "50%",
        transform: `translateY(-50%)`,
        _active: {
          transform: `translateY(-50%) scale(1.15)`
        }
      }
    });
    return {
      ...orientationStyle,
      w: $thumbSize.reference,
      h: $thumbSize.reference,
      display: "flex",
      alignItems: "center",
      justifyContent: "center",
      position: "absolute",
      outline: 0,
      zIndex: 1,
      borderRadius: "full",
      bg: "white",
      boxShadow: "base",
      border: "1px solid",
      borderColor: "transparent",
      transitionProperty: "transform",
      transitionDuration: "normal",
      _focusVisible: {
        boxShadow: "outline"
      },
      _disabled: {
        bg: "gray.300"
      }
    };
  });
  var baseStyleFilledTrack = defineStyle((props) => {
    const { colorScheme: c2 } = props;
    return {
      width: "inherit",
      height: "inherit",
      [$bg$9.variable]: `colors.${c2}.500`,
      _dark: {
        [$bg$9.variable]: `colors.${c2}.200`
      },
      bg: $bg$9.reference
    };
  });
  var baseStyle$q = definePartsStyle$f((props) => ({
    container: baseStyleContainer$2(props),
    track: baseStyleTrack(props),
    thumb: baseStyleThumb(props),
    filledTrack: baseStyleFilledTrack(props)
  }));
  var sizeLg = definePartsStyle$f({
    container: {
      [$thumbSize.variable]: `sizes.4`,
      [$trackSize.variable]: `sizes.1`
    }
  });
  var sizeMd = definePartsStyle$f({
    container: {
      [$thumbSize.variable]: `sizes.3.5`,
      [$trackSize.variable]: `sizes.1`
    }
  });
  var sizeSm = definePartsStyle$f({
    container: {
      [$thumbSize.variable]: `sizes.2.5`,
      [$trackSize.variable]: `sizes.0.5`
    }
  });
  var sizes$b = {
    lg: sizeLg,
    md: sizeMd,
    sm: sizeSm
  };
  var sliderTheme = defineMultiStyleConfig$f({
    baseStyle: baseStyle$q,
    sizes: sizes$b,
    defaultProps: {
      size: "md",
      colorScheme: "blue"
    }
  });
  var $size$2 = cssVar("spinner-size");
  var baseStyle$p = defineStyle({
    width: [$size$2.reference],
    height: [$size$2.reference]
  });
  var sizes$a = {
    xs: defineStyle({
      [$size$2.variable]: "sizes.3"
    }),
    sm: defineStyle({
      [$size$2.variable]: "sizes.4"
    }),
    md: defineStyle({
      [$size$2.variable]: "sizes.6"
    }),
    lg: defineStyle({
      [$size$2.variable]: "sizes.8"
    }),
    xl: defineStyle({
      [$size$2.variable]: "sizes.12"
    })
  };
  var spinnerTheme = defineStyleConfig({
    baseStyle: baseStyle$p,
    sizes: sizes$a,
    defaultProps: {
      size: "md"
    }
  });
  var { defineMultiStyleConfig: defineMultiStyleConfig$e, definePartsStyle: definePartsStyle$e } = createMultiStyleConfigHelpers(statAnatomy.keys);
  var baseStyleLabel$1 = defineStyle({
    fontWeight: "medium"
  });
  var baseStyleHelpText = defineStyle({
    opacity: 0.8,
    marginBottom: "2"
  });
  var baseStyleNumber = defineStyle({
    verticalAlign: "baseline",
    fontWeight: "semibold"
  });
  var baseStyleIcon$4 = defineStyle({
    marginEnd: 1,
    w: "3.5",
    h: "3.5",
    verticalAlign: "middle"
  });
  var baseStyle$o = definePartsStyle$e({
    container: {},
    label: baseStyleLabel$1,
    helpText: baseStyleHelpText,
    number: baseStyleNumber,
    icon: baseStyleIcon$4
  });
  var sizes$9 = {
    md: definePartsStyle$e({
      label: { fontSize: "sm" },
      helpText: { fontSize: "sm" },
      number: { fontSize: "2xl" }
    })
  };
  var statTheme = defineMultiStyleConfig$e({
    baseStyle: baseStyle$o,
    sizes: sizes$9,
    defaultProps: {
      size: "md"
    }
  });
  var $bg$8 = cssVar$1("kbd-bg");
  var baseStyle$n = defineStyle({
    [$bg$8.variable]: "colors.gray.100",
    _dark: {
      [$bg$8.variable]: "colors.whiteAlpha.100"
    },
    bg: $bg$8.reference,
    borderRadius: "md",
    borderWidth: "1px",
    borderBottomWidth: "3px",
    fontSize: "0.8em",
    fontWeight: "bold",
    lineHeight: "normal",
    px: "0.4em",
    whiteSpace: "nowrap"
  });
  var kbdTheme = defineStyleConfig({
    baseStyle: baseStyle$n
  });
  var baseStyle$m = defineStyle({
    transitionProperty: "common",
    transitionDuration: "fast",
    transitionTimingFunction: "ease-out",
    cursor: "pointer",
    textDecoration: "none",
    outline: "none",
    color: "inherit",
    _hover: {
      textDecoration: "underline"
    },
    _focusVisible: {
      boxShadow: "outline"
    }
  });
  var linkTheme = defineStyleConfig({
    baseStyle: baseStyle$m
  });
  var { defineMultiStyleConfig: defineMultiStyleConfig$d, definePartsStyle: definePartsStyle$d } = createMultiStyleConfigHelpers(listAnatomy.keys);
  var baseStyleIcon$3 = defineStyle({
    marginEnd: "2",
    display: "inline",
    verticalAlign: "text-bottom"
  });
  var baseStyle$l = definePartsStyle$d({
    icon: baseStyleIcon$3
  });
  var listTheme = defineMultiStyleConfig$d({
    baseStyle: baseStyle$l
  });
  var { defineMultiStyleConfig: defineMultiStyleConfig$c, definePartsStyle: definePartsStyle$c } = createMultiStyleConfigHelpers(menuAnatomy.keys);
  var $bg$7 = cssVar$1("menu-bg");
  var $shadow$2 = cssVar$1("menu-shadow");
  var baseStyleList = defineStyle({
    [$bg$7.variable]: "#fff",
    [$shadow$2.variable]: "shadows.sm",
    _dark: {
      [$bg$7.variable]: "colors.gray.700",
      [$shadow$2.variable]: "shadows.dark-lg"
    },
    color: "inherit",
    minW: "3xs",
    py: "2",
    zIndex: 1,
    borderRadius: "md",
    borderWidth: "1px",
    bg: $bg$7.reference,
    boxShadow: $shadow$2.reference
  });
  var baseStyleItem = defineStyle({
    py: "1.5",
    px: "3",
    transitionProperty: "background",
    transitionDuration: "ultra-fast",
    transitionTimingFunction: "ease-in",
    _focus: {
      [$bg$7.variable]: "colors.gray.100",
      _dark: {
        [$bg$7.variable]: "colors.whiteAlpha.100"
      }
    },
    _active: {
      [$bg$7.variable]: "colors.gray.200",
      _dark: {
        [$bg$7.variable]: "colors.whiteAlpha.200"
      }
    },
    _expanded: {
      [$bg$7.variable]: "colors.gray.100",
      _dark: {
        [$bg$7.variable]: "colors.whiteAlpha.100"
      }
    },
    _disabled: {
      opacity: 0.4,
      cursor: "not-allowed"
    },
    bg: $bg$7.reference
  });
  var baseStyleGroupTitle = defineStyle({
    mx: 4,
    my: 2,
    fontWeight: "semibold",
    fontSize: "sm"
  });
  var baseStyleIcon$2 = defineStyle({
    display: "inline-flex",
    alignItems: "center",
    justifyContent: "center",
    flexShrink: 0
  });
  var baseStyleCommand = defineStyle({
    opacity: 0.6
  });
  var baseStyleDivider = defineStyle({
    border: 0,
    borderBottom: "1px solid",
    borderColor: "inherit",
    my: "2",
    opacity: 0.6
  });
  var baseStyleButton$1 = defineStyle({
    transitionProperty: "common",
    transitionDuration: "normal"
  });
  var baseStyle$k = definePartsStyle$c({
    button: baseStyleButton$1,
    list: baseStyleList,
    item: baseStyleItem,
    groupTitle: baseStyleGroupTitle,
    icon: baseStyleIcon$2,
    command: baseStyleCommand,
    divider: baseStyleDivider
  });
  var menuTheme = defineMultiStyleConfig$c({
    baseStyle: baseStyle$k
  });
  var { defineMultiStyleConfig: defineMultiStyleConfig$b, definePartsStyle: definePartsStyle$b } = createMultiStyleConfigHelpers(modalAnatomy.keys);
  var $bg$6 = cssVar$1("modal-bg");
  var $shadow$1 = cssVar$1("modal-shadow");
  var baseStyleOverlay$1 = defineStyle({
    bg: "blackAlpha.600",
    zIndex: "modal"
  });
  var baseStyleDialogContainer$1 = defineStyle((props) => {
    const { isCentered, scrollBehavior } = props;
    return {
      display: "flex",
      zIndex: "modal",
      justifyContent: "center",
      alignItems: isCentered ? "center" : "flex-start",
      overflow: scrollBehavior === "inside" ? "hidden" : "auto",
      overscrollBehaviorY: "none"
    };
  });
  var baseStyleDialog$1 = defineStyle((props) => {
    const { isCentered, scrollBehavior } = props;
    return {
      borderRadius: "md",
      color: "inherit",
      my: isCentered ? "auto" : "16",
      mx: isCentered ? "auto" : void 0,
      zIndex: "modal",
      maxH: scrollBehavior === "inside" ? "calc(100% - 7.5rem)" : void 0,
      [$bg$6.variable]: "colors.white",
      [$shadow$1.variable]: "shadows.lg",
      _dark: {
        [$bg$6.variable]: "colors.gray.700",
        [$shadow$1.variable]: "shadows.dark-lg"
      },
      bg: $bg$6.reference,
      boxShadow: $shadow$1.reference
    };
  });
  var baseStyleHeader$2 = defineStyle({
    px: "6",
    py: "4",
    fontSize: "xl",
    fontWeight: "semibold"
  });
  var baseStyleCloseButton$2 = defineStyle({
    position: "absolute",
    top: "2",
    insetEnd: "3"
  });
  var baseStyleBody$2 = defineStyle((props) => {
    const { scrollBehavior } = props;
    return {
      px: "6",
      py: "2",
      flex: "1",
      overflow: scrollBehavior === "inside" ? "auto" : void 0
    };
  });
  var baseStyleFooter$2 = defineStyle({
    px: "6",
    py: "4"
  });
  var baseStyle$j = definePartsStyle$b((props) => ({
    overlay: baseStyleOverlay$1,
    dialogContainer: runIfFn$1(baseStyleDialogContainer$1, props),
    dialog: runIfFn$1(baseStyleDialog$1, props),
    header: baseStyleHeader$2,
    closeButton: baseStyleCloseButton$2,
    body: runIfFn$1(baseStyleBody$2, props),
    footer: baseStyleFooter$2
  }));
  function getSize$3(value) {
    if (value === "full") {
      return definePartsStyle$b({
        dialog: {
          maxW: "100vw",
          minH: "$100vh",
          my: "0",
          borderRadius: "0"
        }
      });
    }
    return definePartsStyle$b({
      dialog: { maxW: value }
    });
  }
  var sizes$8 = {
    xs: getSize$3("xs"),
    sm: getSize$3("sm"),
    md: getSize$3("md"),
    lg: getSize$3("lg"),
    xl: getSize$3("xl"),
    "2xl": getSize$3("2xl"),
    "3xl": getSize$3("3xl"),
    "4xl": getSize$3("4xl"),
    "5xl": getSize$3("5xl"),
    "6xl": getSize$3("6xl"),
    full: getSize$3("full")
  };
  var modalTheme = defineMultiStyleConfig$b({
    baseStyle: baseStyle$j,
    sizes: sizes$8,
    defaultProps: { size: "md" }
  });
  var { defineMultiStyleConfig: defineMultiStyleConfig$a, definePartsStyle: definePartsStyle$a } = createMultiStyleConfigHelpers(numberInputAnatomy.keys);
  var $stepperWidth = cssVar("number-input-stepper-width");
  var $inputPadding = cssVar("number-input-input-padding");
  var inputPaddingValue = calc($stepperWidth).add("0.5rem").toString();
  var $bg$5 = cssVar("number-input-bg");
  var $fg$3 = cssVar("number-input-color");
  var $border$2 = cssVar("number-input-border-color");
  var baseStyleRoot = defineStyle({
    [$stepperWidth.variable]: "sizes.6",
    [$inputPadding.variable]: inputPaddingValue
  });
  var baseStyleField = defineStyle(
    (props) => {
      var _a4, _b3;
      return (_b3 = (_a4 = runIfFn$1(inputTheme.baseStyle, props)) == null ? void 0 : _a4.field) != null ? _b3 : {};
    }
  );
  var baseStyleStepperGroup = defineStyle({
    width: $stepperWidth.reference
  });
  var baseStyleStepper = defineStyle({
    borderStart: "1px solid",
    borderStartColor: $border$2.reference,
    color: $fg$3.reference,
    bg: $bg$5.reference,
    [$fg$3.variable]: "colors.chakra-body-text",
    [$border$2.variable]: "colors.chakra-border-color",
    _dark: {
      [$fg$3.variable]: "colors.whiteAlpha.800",
      [$border$2.variable]: "colors.whiteAlpha.300"
    },
    _active: {
      [$bg$5.variable]: "colors.gray.200",
      _dark: {
        [$bg$5.variable]: "colors.whiteAlpha.300"
      }
    },
    _disabled: {
      opacity: 0.4,
      cursor: "not-allowed"
    }
  });
  var baseStyle$i = definePartsStyle$a((props) => {
    var _a4;
    return {
      root: baseStyleRoot,
      field: (_a4 = runIfFn$1(baseStyleField, props)) != null ? _a4 : {},
      stepperGroup: baseStyleStepperGroup,
      stepper: baseStyleStepper
    };
  });
  function getSize$2(size2) {
    var _a4, _b3, _c2;
    const sizeStyle = (_a4 = inputTheme.sizes) == null ? void 0 : _a4[size2];
    const radius = {
      lg: "md",
      md: "md",
      sm: "sm",
      xs: "sm"
    };
    const _fontSize = (_c2 = (_b3 = sizeStyle.field) == null ? void 0 : _b3.fontSize) != null ? _c2 : "md";
    const fontSize = typography_default.fontSizes[_fontSize];
    return definePartsStyle$a({
      field: {
        ...sizeStyle.field,
        paddingInlineEnd: $inputPadding.reference,
        verticalAlign: "top"
      },
      stepper: {
        fontSize: calc(fontSize).multiply(0.75).toString(),
        _first: {
          borderTopEndRadius: radius[size2]
        },
        _last: {
          borderBottomEndRadius: radius[size2],
          mt: "-1px",
          borderTopWidth: 1
        }
      }
    });
  }
  var sizes$7 = {
    xs: getSize$2("xs"),
    sm: getSize$2("sm"),
    md: getSize$2("md"),
    lg: getSize$2("lg")
  };
  var numberInputTheme = defineMultiStyleConfig$a({
    baseStyle: baseStyle$i,
    sizes: sizes$7,
    variants: inputTheme.variants,
    defaultProps: inputTheme.defaultProps
  });
  var _a$1;
  var baseStyle$h = defineStyle({
    ...(_a$1 = inputTheme.baseStyle) == null ? void 0 : _a$1.field,
    textAlign: "center"
  });
  var sizes$6 = {
    lg: defineStyle({
      fontSize: "lg",
      w: 12,
      h: 12,
      borderRadius: "md"
    }),
    md: defineStyle({
      fontSize: "md",
      w: 10,
      h: 10,
      borderRadius: "md"
    }),
    sm: defineStyle({
      fontSize: "sm",
      w: 8,
      h: 8,
      borderRadius: "sm"
    }),
    xs: defineStyle({
      fontSize: "xs",
      w: 6,
      h: 6,
      borderRadius: "sm"
    })
  };
  var _a2, _b;
  var variants$5 = {
    outline: defineStyle(
      (props) => {
        var _a32, _b22, _c2;
        return (_c2 = (_b22 = runIfFn$1((_a32 = inputTheme.variants) == null ? void 0 : _a32.outline, props)) == null ? void 0 : _b22.field) != null ? _c2 : {};
      }
    ),
    flushed: defineStyle(
      (props) => {
        var _a32, _b22, _c2;
        return (_c2 = (_b22 = runIfFn$1((_a32 = inputTheme.variants) == null ? void 0 : _a32.flushed, props)) == null ? void 0 : _b22.field) != null ? _c2 : {};
      }
    ),
    filled: defineStyle(
      (props) => {
        var _a32, _b22, _c2;
        return (_c2 = (_b22 = runIfFn$1((_a32 = inputTheme.variants) == null ? void 0 : _a32.filled, props)) == null ? void 0 : _b22.field) != null ? _c2 : {};
      }
    ),
    unstyled: (_b = (_a2 = inputTheme.variants) == null ? void 0 : _a2.unstyled.field) != null ? _b : {}
  };
  var pinInputTheme = defineStyleConfig({
    baseStyle: baseStyle$h,
    sizes: sizes$6,
    variants: variants$5,
    defaultProps: inputTheme.defaultProps
  });
  var { defineMultiStyleConfig: defineMultiStyleConfig$9, definePartsStyle: definePartsStyle$9 } = createMultiStyleConfigHelpers(popoverAnatomy.keys);
  var $popperBg = cssVar("popper-bg");
  var $arrowBg = cssVar("popper-arrow-bg");
  var $arrowShadowColor = cssVar("popper-arrow-shadow-color");
  var baseStylePopper = defineStyle({ zIndex: 10 });
  var baseStyleContent = defineStyle({
    [$popperBg.variable]: `colors.white`,
    bg: $popperBg.reference,
    [$arrowBg.variable]: $popperBg.reference,
    [$arrowShadowColor.variable]: `colors.gray.200`,
    _dark: {
      [$popperBg.variable]: `colors.gray.700`,
      [$arrowShadowColor.variable]: `colors.whiteAlpha.300`
    },
    width: "xs",
    border: "1px solid",
    borderColor: "inherit",
    borderRadius: "md",
    boxShadow: "sm",
    zIndex: "inherit",
    _focusVisible: {
      outline: 0,
      boxShadow: "outline"
    }
  });
  var baseStyleHeader$1 = defineStyle({
    px: 3,
    py: 2,
    borderBottomWidth: "1px"
  });
  var baseStyleBody$1 = defineStyle({
    px: 3,
    py: 2
  });
  var baseStyleFooter$1 = defineStyle({
    px: 3,
    py: 2,
    borderTopWidth: "1px"
  });
  var baseStyleCloseButton$1 = defineStyle({
    position: "absolute",
    borderRadius: "md",
    top: 1,
    insetEnd: 2,
    padding: 2
  });
  var baseStyle$g = definePartsStyle$9({
    popper: baseStylePopper,
    content: baseStyleContent,
    header: baseStyleHeader$1,
    body: baseStyleBody$1,
    footer: baseStyleFooter$1,
    closeButton: baseStyleCloseButton$1
  });
  var popoverTheme = defineMultiStyleConfig$9({
    baseStyle: baseStyle$g
  });
  var { definePartsStyle: definePartsStyle$8, defineMultiStyleConfig: defineMultiStyleConfig$8 } = createMultiStyleConfigHelpers(drawerAnatomy.keys);
  var $bg$4 = cssVar$1("drawer-bg");
  var $bs = cssVar$1("drawer-box-shadow");
  function getSize$1(value) {
    if (value === "full") {
      return definePartsStyle$8({
        dialog: { maxW: "100vw", h: "100vh" }
      });
    }
    return definePartsStyle$8({
      dialog: { maxW: value }
    });
  }
  var baseStyleOverlay = defineStyle({
    bg: "blackAlpha.600",
    zIndex: "modal"
  });
  var baseStyleDialogContainer = defineStyle({
    display: "flex",
    zIndex: "modal",
    justifyContent: "center"
  });
  var baseStyleDialog = defineStyle((props) => {
    const { isFullHeight } = props;
    return {
      ...isFullHeight && { height: "100vh" },
      zIndex: "modal",
      maxH: "100vh",
      color: "inherit",
      [$bg$4.variable]: "colors.white",
      [$bs.variable]: "shadows.lg",
      _dark: {
        [$bg$4.variable]: "colors.gray.700",
        [$bs.variable]: "shadows.dark-lg"
      },
      bg: $bg$4.reference,
      boxShadow: $bs.reference
    };
  });
  var baseStyleHeader = defineStyle({
    px: "6",
    py: "4",
    fontSize: "xl",
    fontWeight: "semibold"
  });
  var baseStyleCloseButton = defineStyle({
    position: "absolute",
    top: "2",
    insetEnd: "3"
  });
  var baseStyleBody = defineStyle({
    px: "6",
    py: "2",
    flex: "1",
    overflow: "auto"
  });
  var baseStyleFooter = defineStyle({
    px: "6",
    py: "4"
  });
  var baseStyle$f = definePartsStyle$8((props) => ({
    overlay: baseStyleOverlay,
    dialogContainer: baseStyleDialogContainer,
    dialog: runIfFn$1(baseStyleDialog, props),
    header: baseStyleHeader,
    closeButton: baseStyleCloseButton,
    body: baseStyleBody,
    footer: baseStyleFooter
  }));
  var sizes$5 = {
    xs: getSize$1("xs"),
    sm: getSize$1("md"),
    md: getSize$1("lg"),
    lg: getSize$1("2xl"),
    xl: getSize$1("4xl"),
    full: getSize$1("full")
  };
  var drawerTheme = defineMultiStyleConfig$8({
    baseStyle: baseStyle$f,
    sizes: sizes$5,
    defaultProps: {
      size: "xs"
    }
  });
  var { definePartsStyle: definePartsStyle$7, defineMultiStyleConfig: defineMultiStyleConfig$7 } = createMultiStyleConfigHelpers(editableAnatomy.keys);
  var baseStylePreview = defineStyle({
    borderRadius: "md",
    py: "1",
    transitionProperty: "common",
    transitionDuration: "normal"
  });
  var baseStyleInput = defineStyle({
    borderRadius: "md",
    py: "1",
    transitionProperty: "common",
    transitionDuration: "normal",
    width: "full",
    _focusVisible: { boxShadow: "outline" },
    _placeholder: { opacity: 0.6 }
  });
  var baseStyleTextarea = defineStyle({
    borderRadius: "md",
    py: "1",
    transitionProperty: "common",
    transitionDuration: "normal",
    width: "full",
    _focusVisible: { boxShadow: "outline" },
    _placeholder: { opacity: 0.6 }
  });
  var baseStyle$e = definePartsStyle$7({
    preview: baseStylePreview,
    input: baseStyleInput,
    textarea: baseStyleTextarea
  });
  var editableTheme = defineMultiStyleConfig$7({
    baseStyle: baseStyle$e
  });
  var { definePartsStyle: definePartsStyle$6, defineMultiStyleConfig: defineMultiStyleConfig$6 } = createMultiStyleConfigHelpers(formAnatomy.keys);
  var $fg$2 = cssVar$1("form-control-color");
  var baseStyleRequiredIndicator = defineStyle({
    marginStart: "1",
    [$fg$2.variable]: "colors.red.500",
    _dark: {
      [$fg$2.variable]: "colors.red.300"
    },
    color: $fg$2.reference
  });
  var baseStyleHelperText = defineStyle({
    mt: "2",
    [$fg$2.variable]: "colors.gray.600",
    _dark: {
      [$fg$2.variable]: "colors.whiteAlpha.600"
    },
    color: $fg$2.reference,
    lineHeight: "normal",
    fontSize: "sm"
  });
  var baseStyle$d = definePartsStyle$6({
    container: {
      width: "100%",
      position: "relative"
    },
    requiredIndicator: baseStyleRequiredIndicator,
    helperText: baseStyleHelperText
  });
  var formTheme = defineMultiStyleConfig$6({
    baseStyle: baseStyle$d
  });
  var { definePartsStyle: definePartsStyle$5, defineMultiStyleConfig: defineMultiStyleConfig$5 } = createMultiStyleConfigHelpers(formErrorAnatomy.keys);
  var $fg$1 = cssVar$1("form-error-color");
  var baseStyleText = defineStyle({
    [$fg$1.variable]: `colors.red.500`,
    _dark: {
      [$fg$1.variable]: `colors.red.300`
    },
    color: $fg$1.reference,
    mt: "2",
    fontSize: "sm",
    lineHeight: "normal"
  });
  var baseStyleIcon$1 = defineStyle({
    marginEnd: "0.5em",
    [$fg$1.variable]: `colors.red.500`,
    _dark: {
      [$fg$1.variable]: `colors.red.300`
    },
    color: $fg$1.reference
  });
  var baseStyle$c = definePartsStyle$5({
    text: baseStyleText,
    icon: baseStyleIcon$1
  });
  var formErrorTheme = defineMultiStyleConfig$5({
    baseStyle: baseStyle$c
  });
  var baseStyle$b = defineStyle({
    fontSize: "md",
    marginEnd: "3",
    mb: "2",
    fontWeight: "medium",
    transitionProperty: "common",
    transitionDuration: "normal",
    opacity: 1,
    _disabled: {
      opacity: 0.4
    }
  });
  var formLabelTheme = defineStyleConfig({
    baseStyle: baseStyle$b
  });
  var baseStyle$a = defineStyle({
    fontFamily: "heading",
    fontWeight: "bold"
  });
  var sizes$4 = {
    "4xl": defineStyle({
      fontSize: ["6xl", null, "7xl"],
      lineHeight: 1
    }),
    "3xl": defineStyle({
      fontSize: ["5xl", null, "6xl"],
      lineHeight: 1
    }),
    "2xl": defineStyle({
      fontSize: ["4xl", null, "5xl"],
      lineHeight: [1.2, null, 1]
    }),
    xl: defineStyle({
      fontSize: ["3xl", null, "4xl"],
      lineHeight: [1.33, null, 1.2]
    }),
    lg: defineStyle({
      fontSize: ["2xl", null, "3xl"],
      lineHeight: [1.33, null, 1.2]
    }),
    md: defineStyle({
      fontSize: "xl",
      lineHeight: 1.2
    }),
    sm: defineStyle({
      fontSize: "md",
      lineHeight: 1.2
    }),
    xs: defineStyle({
      fontSize: "sm",
      lineHeight: 1.2
    })
  };
  var headingTheme = defineStyleConfig({
    baseStyle: baseStyle$a,
    sizes: sizes$4,
    defaultProps: {
      size: "xl"
    }
  });
  var { defineMultiStyleConfig: defineMultiStyleConfig$4, definePartsStyle: definePartsStyle$4 } = createMultiStyleConfigHelpers(breadcrumbAnatomy.keys);
  var $decor = cssVar$1("breadcrumb-link-decor");
  var baseStyleLink = defineStyle({
    transitionProperty: "common",
    transitionDuration: "fast",
    transitionTimingFunction: "ease-out",
    outline: "none",
    color: "inherit",
    textDecoration: $decor.reference,
    [$decor.variable]: "none",
    "&:not([aria-current=page])": {
      cursor: "pointer",
      _hover: {
        [$decor.variable]: "underline"
      },
      _focusVisible: {
        boxShadow: "outline"
      }
    }
  });
  var baseStyle$9 = definePartsStyle$4({
    link: baseStyleLink
  });
  var breadcrumbTheme = defineMultiStyleConfig$4({
    baseStyle: baseStyle$9
  });
  var baseStyle$8 = defineStyle({
    lineHeight: "1.2",
    borderRadius: "md",
    fontWeight: "semibold",
    transitionProperty: "common",
    transitionDuration: "normal",
    _focusVisible: {
      boxShadow: "outline"
    },
    _disabled: {
      opacity: 0.4,
      cursor: "not-allowed",
      boxShadow: "none"
    },
    _hover: {
      _disabled: {
        bg: "initial"
      }
    }
  });
  var variantGhost = defineStyle((props) => {
    const { colorScheme: c2, theme: theme2 } = props;
    if (c2 === "gray") {
      return {
        color: mode(`gray.800`, `whiteAlpha.900`)(props),
        _hover: {
          bg: mode(`gray.100`, `whiteAlpha.200`)(props)
        },
        _active: { bg: mode(`gray.200`, `whiteAlpha.300`)(props) }
      };
    }
    const darkHoverBg = transparentize(`${c2}.200`, 0.12)(theme2);
    const darkActiveBg = transparentize(`${c2}.200`, 0.24)(theme2);
    return {
      color: mode(`${c2}.600`, `${c2}.200`)(props),
      bg: "transparent",
      _hover: {
        bg: mode(`${c2}.50`, darkHoverBg)(props)
      },
      _active: {
        bg: mode(`${c2}.100`, darkActiveBg)(props)
      }
    };
  });
  var variantOutline = defineStyle((props) => {
    const { colorScheme: c2 } = props;
    const borderColor = mode(`gray.200`, `whiteAlpha.300`)(props);
    return {
      border: "1px solid",
      borderColor: c2 === "gray" ? borderColor : "currentColor",
      ".chakra-button__group[data-attached][data-orientation=horizontal] > &:not(:last-of-type)": { marginEnd: "-1px" },
      ".chakra-button__group[data-attached][data-orientation=vertical] > &:not(:last-of-type)": { marginBottom: "-1px" },
      ...runIfFn$1(variantGhost, props)
    };
  });
  var accessibleColorMap = {
    yellow: {
      bg: "yellow.400",
      color: "black",
      hoverBg: "yellow.500",
      activeBg: "yellow.600"
    },
    cyan: {
      bg: "cyan.400",
      color: "black",
      hoverBg: "cyan.500",
      activeBg: "cyan.600"
    }
  };
  var variantSolid$2 = defineStyle((props) => {
    var _a4;
    const { colorScheme: c2 } = props;
    if (c2 === "gray") {
      const bg22 = mode(`gray.100`, `whiteAlpha.200`)(props);
      return {
        bg: bg22,
        color: mode(`gray.800`, `whiteAlpha.900`)(props),
        _hover: {
          bg: mode(`gray.200`, `whiteAlpha.300`)(props),
          _disabled: {
            bg: bg22
          }
        },
        _active: { bg: mode(`gray.300`, `whiteAlpha.400`)(props) }
      };
    }
    const {
      bg: bg2 = `${c2}.500`,
      color: color2 = "white",
      hoverBg = `${c2}.600`,
      activeBg = `${c2}.700`
    } = (_a4 = accessibleColorMap[c2]) != null ? _a4 : {};
    const background2 = mode(bg2, `${c2}.200`)(props);
    return {
      bg: background2,
      color: mode(color2, `gray.800`)(props),
      _hover: {
        bg: mode(hoverBg, `${c2}.300`)(props),
        _disabled: {
          bg: background2
        }
      },
      _active: { bg: mode(activeBg, `${c2}.400`)(props) }
    };
  });
  var variantLink = defineStyle((props) => {
    const { colorScheme: c2 } = props;
    return {
      padding: 0,
      height: "auto",
      lineHeight: "normal",
      verticalAlign: "baseline",
      color: mode(`${c2}.500`, `${c2}.200`)(props),
      _hover: {
        textDecoration: "underline",
        _disabled: {
          textDecoration: "none"
        }
      },
      _active: {
        color: mode(`${c2}.700`, `${c2}.500`)(props)
      }
    };
  });
  var variantUnstyled = defineStyle({
    bg: "none",
    color: "inherit",
    display: "inline",
    lineHeight: "inherit",
    m: "0",
    p: "0"
  });
  var variants$4 = {
    ghost: variantGhost,
    outline: variantOutline,
    solid: variantSolid$2,
    link: variantLink,
    unstyled: variantUnstyled
  };
  var sizes$3 = {
    lg: defineStyle({
      h: "12",
      minW: "12",
      fontSize: "lg",
      px: "6"
    }),
    md: defineStyle({
      h: "10",
      minW: "10",
      fontSize: "md",
      px: "4"
    }),
    sm: defineStyle({
      h: "8",
      minW: "8",
      fontSize: "sm",
      px: "3"
    }),
    xs: defineStyle({
      h: "6",
      minW: "6",
      fontSize: "xs",
      px: "2"
    })
  };
  var buttonTheme = defineStyleConfig({
    baseStyle: baseStyle$8,
    variants: variants$4,
    sizes: sizes$3,
    defaultProps: {
      variant: "solid",
      size: "md",
      colorScheme: "gray"
    }
  });
  var { definePartsStyle: definePartsStyle$3, defineMultiStyleConfig: defineMultiStyleConfig$3 } = createMultiStyleConfigHelpers(cardAnatomy.keys);
  var $bg$3 = cssVar$1("card-bg");
  var $padding = cssVar$1("card-padding");
  var $shadow = cssVar$1("card-shadow");
  var $radius = cssVar$1("card-radius");
  var $border$1 = cssVar$1("card-border-width", "0");
  var $borderColor = cssVar$1("card-border-color");
  var baseStyle$7 = definePartsStyle$3({
    container: {
      [$bg$3.variable]: "colors.chakra-body-bg",
      backgroundColor: $bg$3.reference,
      boxShadow: $shadow.reference,
      borderRadius: $radius.reference,
      color: "chakra-body-text",
      borderWidth: $border$1.reference,
      borderColor: $borderColor.reference
    },
    body: {
      padding: $padding.reference,
      flex: "1 1 0%"
    },
    header: {
      padding: $padding.reference
    },
    footer: {
      padding: $padding.reference
    }
  });
  var sizes$2 = {
    sm: definePartsStyle$3({
      container: {
        [$radius.variable]: "radii.base",
        [$padding.variable]: "space.3"
      }
    }),
    md: definePartsStyle$3({
      container: {
        [$radius.variable]: "radii.md",
        [$padding.variable]: "space.5"
      }
    }),
    lg: definePartsStyle$3({
      container: {
        [$radius.variable]: "radii.xl",
        [$padding.variable]: "space.7"
      }
    })
  };
  var variants$3 = {
    elevated: definePartsStyle$3({
      container: {
        [$shadow.variable]: "shadows.base",
        _dark: {
          [$bg$3.variable]: "colors.gray.700"
        }
      }
    }),
    outline: definePartsStyle$3({
      container: {
        [$border$1.variable]: "1px",
        [$borderColor.variable]: "colors.chakra-border-color"
      }
    }),
    filled: definePartsStyle$3({
      container: {
        [$bg$3.variable]: "colors.chakra-subtle-bg"
      }
    }),
    unstyled: {
      body: {
        [$padding.variable]: 0
      },
      header: {
        [$padding.variable]: 0
      },
      footer: {
        [$padding.variable]: 0
      }
    }
  };
  var cardTheme = defineMultiStyleConfig$3({
    baseStyle: baseStyle$7,
    variants: variants$3,
    sizes: sizes$2,
    defaultProps: {
      variant: "elevated",
      size: "md"
    }
  });
  var $size$1 = cssVar("close-button-size");
  var $bg$2 = cssVar("close-button-bg");
  var baseStyle$6 = defineStyle({
    w: [$size$1.reference],
    h: [$size$1.reference],
    borderRadius: "md",
    transitionProperty: "common",
    transitionDuration: "normal",
    _disabled: {
      opacity: 0.4,
      cursor: "not-allowed",
      boxShadow: "none"
    },
    _hover: {
      [$bg$2.variable]: "colors.blackAlpha.100",
      _dark: {
        [$bg$2.variable]: "colors.whiteAlpha.100"
      }
    },
    _active: {
      [$bg$2.variable]: "colors.blackAlpha.200",
      _dark: {
        [$bg$2.variable]: "colors.whiteAlpha.200"
      }
    },
    _focusVisible: {
      boxShadow: "outline"
    },
    bg: $bg$2.reference
  });
  var sizes$1 = {
    lg: defineStyle({
      [$size$1.variable]: "sizes.10",
      fontSize: "md"
    }),
    md: defineStyle({
      [$size$1.variable]: "sizes.8",
      fontSize: "xs"
    }),
    sm: defineStyle({
      [$size$1.variable]: "sizes.6",
      fontSize: "2xs"
    })
  };
  var closeButtonTheme = defineStyleConfig({
    baseStyle: baseStyle$6,
    sizes: sizes$1,
    defaultProps: {
      size: "md"
    }
  });
  var { variants: variants$2, defaultProps } = badgeTheme;
  var baseStyle$5 = defineStyle({
    fontFamily: "mono",
    fontSize: "sm",
    px: "0.2em",
    borderRadius: "sm",
    bg: vars.bg.reference,
    color: vars.color.reference,
    boxShadow: vars.shadow.reference
  });
  var codeTheme = defineStyleConfig({
    baseStyle: baseStyle$5,
    variants: variants$2,
    defaultProps
  });
  var baseStyle$4 = defineStyle({
    w: "100%",
    mx: "auto",
    maxW: "prose",
    px: "4"
  });
  var containerTheme = defineStyleConfig({
    baseStyle: baseStyle$4
  });
  var baseStyle$3 = defineStyle({
    opacity: 0.6,
    borderColor: "inherit"
  });
  var variantSolid$1 = defineStyle({
    borderStyle: "solid"
  });
  var variantDashed = defineStyle({
    borderStyle: "dashed"
  });
  var variants$1 = {
    solid: variantSolid$1,
    dashed: variantDashed
  };
  var dividerTheme = defineStyleConfig({
    baseStyle: baseStyle$3,
    variants: variants$1,
    defaultProps: {
      variant: "solid"
    }
  });
  var { definePartsStyle: definePartsStyle$2, defineMultiStyleConfig: defineMultiStyleConfig$2 } = createMultiStyleConfigHelpers(accordionAnatomy.keys);
  var baseStyleContainer$1 = defineStyle({
    borderTopWidth: "1px",
    borderColor: "inherit",
    _last: {
      borderBottomWidth: "1px"
    }
  });
  var baseStyleButton = defineStyle({
    transitionProperty: "common",
    transitionDuration: "normal",
    fontSize: "md",
    _focusVisible: {
      boxShadow: "outline"
    },
    _hover: {
      bg: "blackAlpha.50"
    },
    _disabled: {
      opacity: 0.4,
      cursor: "not-allowed"
    },
    px: "4",
    py: "2"
  });
  var baseStylePanel = defineStyle({
    pt: "2",
    px: "4",
    pb: "5"
  });
  var baseStyleIcon = defineStyle({
    fontSize: "1.25em"
  });
  var baseStyle$2 = definePartsStyle$2({
    container: baseStyleContainer$1,
    button: baseStyleButton,
    panel: baseStylePanel,
    icon: baseStyleIcon
  });
  var accordionTheme = defineMultiStyleConfig$2({ baseStyle: baseStyle$2 });
  var { definePartsStyle: definePartsStyle$1, defineMultiStyleConfig: defineMultiStyleConfig$1 } = createMultiStyleConfigHelpers(alertAnatomy.keys);
  var $fg = cssVar$1("alert-fg");
  var $bg$1 = cssVar$1("alert-bg");
  var baseStyle$1 = definePartsStyle$1({
    container: {
      bg: $bg$1.reference,
      px: "4",
      py: "3"
    },
    title: {
      fontWeight: "bold",
      lineHeight: "6",
      marginEnd: "2"
    },
    description: {
      lineHeight: "6"
    },
    icon: {
      color: $fg.reference,
      flexShrink: 0,
      marginEnd: "3",
      w: "5",
      h: "6"
    },
    spinner: {
      color: $fg.reference,
      flexShrink: 0,
      marginEnd: "3",
      w: "5",
      h: "5"
    }
  });
  function getBg(props) {
    const { theme: theme2, colorScheme: c2 } = props;
    const darkBg = transparentize(`${c2}.200`, 0.16)(theme2);
    return {
      light: `colors.${c2}.100`,
      dark: darkBg
    };
  }
  var variantSubtle = definePartsStyle$1((props) => {
    const { colorScheme: c2 } = props;
    const bg2 = getBg(props);
    return {
      container: {
        [$fg.variable]: `colors.${c2}.600`,
        [$bg$1.variable]: bg2.light,
        _dark: {
          [$fg.variable]: `colors.${c2}.200`,
          [$bg$1.variable]: bg2.dark
        }
      }
    };
  });
  var variantLeftAccent = definePartsStyle$1((props) => {
    const { colorScheme: c2 } = props;
    const bg2 = getBg(props);
    return {
      container: {
        [$fg.variable]: `colors.${c2}.600`,
        [$bg$1.variable]: bg2.light,
        _dark: {
          [$fg.variable]: `colors.${c2}.200`,
          [$bg$1.variable]: bg2.dark
        },
        paddingStart: "3",
        borderStartWidth: "4px",
        borderStartColor: $fg.reference
      }
    };
  });
  var variantTopAccent = definePartsStyle$1((props) => {
    const { colorScheme: c2 } = props;
    const bg2 = getBg(props);
    return {
      container: {
        [$fg.variable]: `colors.${c2}.600`,
        [$bg$1.variable]: bg2.light,
        _dark: {
          [$fg.variable]: `colors.${c2}.200`,
          [$bg$1.variable]: bg2.dark
        },
        pt: "2",
        borderTopWidth: "4px",
        borderTopColor: $fg.reference
      }
    };
  });
  var variantSolid = definePartsStyle$1((props) => {
    const { colorScheme: c2 } = props;
    return {
      container: {
        [$fg.variable]: `colors.white`,
        [$bg$1.variable]: `colors.${c2}.600`,
        _dark: {
          [$fg.variable]: `colors.gray.900`,
          [$bg$1.variable]: `colors.${c2}.200`
        },
        color: $fg.reference
      }
    };
  });
  var variants = {
    subtle: variantSubtle,
    "left-accent": variantLeftAccent,
    "top-accent": variantTopAccent,
    solid: variantSolid
  };
  var alertTheme = defineMultiStyleConfig$1({
    baseStyle: baseStyle$1,
    variants,
    defaultProps: {
      variant: "subtle",
      colorScheme: "blue"
    }
  });
  var { definePartsStyle, defineMultiStyleConfig } = createMultiStyleConfigHelpers(avatarAnatomy.keys);
  var $border = cssVar$1("avatar-border-color");
  var $bg = cssVar$1("avatar-bg");
  var $fs = cssVar$1("avatar-font-size");
  var $size = cssVar$1("avatar-size");
  var baseStyleBadge = defineStyle({
    borderRadius: "full",
    border: "0.2em solid",
    borderColor: $border.reference,
    [$border.variable]: "white",
    _dark: {
      [$border.variable]: "colors.gray.800"
    }
  });
  var baseStyleExcessLabel = defineStyle({
    bg: $bg.reference,
    fontSize: $fs.reference,
    width: $size.reference,
    height: $size.reference,
    lineHeight: "1",
    [$bg.variable]: "colors.gray.200",
    _dark: {
      [$bg.variable]: "colors.whiteAlpha.400"
    }
  });
  var baseStyleContainer = defineStyle((props) => {
    const { name, theme: theme2 } = props;
    const bg2 = name ? randomColor({ string: name }) : "colors.gray.400";
    const isBgDark = isDark(bg2)(theme2);
    let color2 = "white";
    if (!isBgDark)
      color2 = "gray.800";
    return {
      bg: $bg.reference,
      fontSize: $fs.reference,
      color: color2,
      borderColor: $border.reference,
      verticalAlign: "top",
      width: $size.reference,
      height: $size.reference,
      "&:not([data-loaded])": {
        [$bg.variable]: bg2
      },
      [$border.variable]: "colors.white",
      _dark: {
        [$border.variable]: "colors.gray.800"
      }
    };
  });
  var baseStyleLabel = defineStyle({
    fontSize: $fs.reference,
    lineHeight: "1"
  });
  var baseStyle = definePartsStyle((props) => ({
    badge: runIfFn$1(baseStyleBadge, props),
    excessLabel: runIfFn$1(baseStyleExcessLabel, props),
    container: runIfFn$1(baseStyleContainer, props),
    label: baseStyleLabel
  }));
  function getSize(size2) {
    const themeSize = size2 !== "100%" ? sizes_default[size2] : void 0;
    return definePartsStyle({
      container: {
        [$size.variable]: themeSize != null ? themeSize : size2,
        [$fs.variable]: `calc(${themeSize != null ? themeSize : size2} / 2.5)`
      },
      excessLabel: {
        [$size.variable]: themeSize != null ? themeSize : size2,
        [$fs.variable]: `calc(${themeSize != null ? themeSize : size2} / 2.5)`
      }
    });
  }
  var sizes = {
    "2xs": getSize(4),
    xs: getSize(6),
    sm: getSize(8),
    md: getSize(12),
    lg: getSize(16),
    xl: getSize(24),
    "2xl": getSize(32),
    full: getSize("100%")
  };
  var avatarTheme = defineMultiStyleConfig({
    baseStyle,
    sizes,
    defaultProps: {
      size: "md"
    }
  });
  var components = {
    Accordion: accordionTheme,
    Alert: alertTheme,
    Avatar: avatarTheme,
    Badge: badgeTheme,
    Breadcrumb: breadcrumbTheme,
    Button: buttonTheme,
    Checkbox: checkboxTheme,
    CloseButton: closeButtonTheme,
    Code: codeTheme,
    Container: containerTheme,
    Divider: dividerTheme,
    Drawer: drawerTheme,
    Editable: editableTheme,
    Form: formTheme,
    FormError: formErrorTheme,
    FormLabel: formLabelTheme,
    Heading: headingTheme,
    Input: inputTheme,
    Kbd: kbdTheme,
    Link: linkTheme,
    List: listTheme,
    Menu: menuTheme,
    Modal: modalTheme,
    NumberInput: numberInputTheme,
    PinInput: pinInputTheme,
    Popover: popoverTheme,
    Progress: progressTheme,
    Radio: radioTheme,
    Select: selectTheme,
    Skeleton: skeletonTheme,
    SkipLink: skipLinkTheme,
    Slider: sliderTheme,
    Spinner: spinnerTheme,
    Stat: statTheme,
    Switch: switchTheme,
    Table: tableTheme,
    Tabs: tabsTheme,
    Tag: tagTheme,
    Textarea: textareaTheme,
    Tooltip: tooltipTheme,
    Card: cardTheme,
    Stepper: stepperTheme
  };
  var semanticTokens = {
    colors: {
      "chakra-body-text": { _light: "gray.800", _dark: "whiteAlpha.900" },
      "chakra-body-bg": { _light: "white", _dark: "gray.800" },
      "chakra-border-color": { _light: "gray.200", _dark: "whiteAlpha.300" },
      "chakra-inverse-text": { _light: "white", _dark: "gray.800" },
      "chakra-subtle-bg": { _light: "gray.100", _dark: "gray.700" },
      "chakra-subtle-text": { _light: "gray.600", _dark: "gray.400" },
      "chakra-placeholder-color": { _light: "gray.500", _dark: "whiteAlpha.400" }
    }
  };
  var styles = {
    global: {
      body: {
        fontFamily: "body",
        color: "chakra-body-text",
        bg: "chakra-body-bg",
        transitionProperty: "background-color",
        transitionDuration: "normal",
        lineHeight: "base"
      },
      "*::placeholder": {
        color: "chakra-placeholder-color"
      },
      "*, *::before, &::after": {
        borderColor: "chakra-border-color"
      }
    }
  };
  var direction = "ltr";
  var config = {
    useSystemColorMode: false,
    initialColorMode: "light",
    cssVarPrefix: "chakra"
  };
  var theme = {
    semanticTokens,
    direction,
    ...foundations,
    components,
    styles,
    config
  };
  function isFunction$1(value) {
    return typeof value === "function";
  }
  function pipe$1(...fns) {
    return (v2) => fns.reduce((a, b2) => b2(a), v2);
  }
  var createExtendTheme = (theme2) => {
    return function extendTheme2(...extensions) {
      let overrides = [...extensions];
      let activeTheme = extensions[extensions.length - 1];
      if (isChakraTheme(activeTheme) && // this ensures backward compatibility
      // previously only `extendTheme(override, activeTheme?)` was allowed
      overrides.length > 1) {
        overrides = overrides.slice(0, overrides.length - 1);
      } else {
        activeTheme = theme2;
      }
      return pipe$1(
        ...overrides.map(
          (extension) => (prevTheme) => isFunction$1(extension) ? extension(prevTheme) : mergeThemeOverride(prevTheme, extension)
        )
      )(activeTheme);
    };
  };
  var extendTheme = createExtendTheme(theme);
  function mergeThemeOverride(...overrides) {
    return mergeWith({}, ...overrides, mergeThemeCustomizer);
  }
  function mergeThemeCustomizer(source, override, key, object) {
    if ((isFunction$1(source) || isFunction$1(override)) && Object.prototype.hasOwnProperty.call(object, key)) {
      return (...args) => {
        const sourceValue = isFunction$1(source) ? source(...args) : source;
        const overrideValue = isFunction$1(override) ? override(...args) : override;
        return mergeWith({}, sourceValue, overrideValue, mergeThemeCustomizer);
      };
    }
    return void 0;
  }
  function omit(object, keys2) {
    const result = {};
    Object.keys(object).forEach((key) => {
      if (keys2.includes(key))
        return;
      result[key] = object[key];
    });
    return result;
  }
  function get(obj, path, fallback, index) {
    const key = typeof path === "string" ? path.split(".") : [path];
    for (index = 0; index < key.length; index += 1) {
      if (!obj)
        break;
      obj = obj[key[index]];
    }
    return obj === void 0 ? fallback : obj;
  }
  var memoize = (fn) => {
    const cache = /* @__PURE__ */ new WeakMap();
    const memoizedFn = (obj, path, fallback, index) => {
      if (typeof obj === "undefined") {
        return fn(obj, path, fallback);
      }
      if (!cache.has(obj)) {
        cache.set(obj, /* @__PURE__ */ new Map());
      }
      const map = cache.get(obj);
      if (map.has(path)) {
        return map.get(path);
      }
      const value = fn(obj, path, fallback, index);
      map.set(path, value);
      return value;
    };
    return memoizedFn;
  };
  var memoizedGet = memoize(get);
  function objectFilter(object, fn) {
    const result = {};
    Object.keys(object).forEach((key) => {
      const value = object[key];
      const shouldPass = fn(value, key, object);
      if (shouldPass) {
        result[key] = value;
      }
    });
    return result;
  }
  var filterUndefined = (object) => objectFilter(object, (val) => val !== null && val !== void 0);
  function isFunction(value) {
    return typeof value === "function";
  }
  function runIfFn(valueOrFn, ...args) {
    return isFunction(valueOrFn) ? valueOrFn(...args) : valueOrFn;
  }
  var hasElementType = typeof Element !== "undefined";
  var hasMap = typeof Map === "function";
  var hasSet = typeof Set === "function";
  var hasArrayBuffer = typeof ArrayBuffer === "function" && !!ArrayBuffer.isView;
  function equal(a, b2) {
    if (a === b2)
      return true;
    if (a && b2 && typeof a == "object" && typeof b2 == "object") {
      if (a.constructor !== b2.constructor)
        return false;
      var length2, i, keys2;
      if (Array.isArray(a)) {
        length2 = a.length;
        if (length2 != b2.length)
          return false;
        for (i = length2; i-- !== 0; )
          if (!equal(a[i], b2[i]))
            return false;
        return true;
      }
      var it2;
      if (hasMap && a instanceof Map && b2 instanceof Map) {
        if (a.size !== b2.size)
          return false;
        it2 = a.entries();
        while (!(i = it2.next()).done)
          if (!b2.has(i.value[0]))
            return false;
        it2 = a.entries();
        while (!(i = it2.next()).done)
          if (!equal(i.value[1], b2.get(i.value[0])))
            return false;
        return true;
      }
      if (hasSet && a instanceof Set && b2 instanceof Set) {
        if (a.size !== b2.size)
          return false;
        it2 = a.entries();
        while (!(i = it2.next()).done)
          if (!b2.has(i.value[0]))
            return false;
        return true;
      }
      if (hasArrayBuffer && ArrayBuffer.isView(a) && ArrayBuffer.isView(b2)) {
        length2 = a.length;
        if (length2 != b2.length)
          return false;
        for (i = length2; i-- !== 0; )
          if (a[i] !== b2[i])
            return false;
        return true;
      }
      if (a.constructor === RegExp)
        return a.source === b2.source && a.flags === b2.flags;
      if (a.valueOf !== Object.prototype.valueOf && typeof a.valueOf === "function" && typeof b2.valueOf === "function")
        return a.valueOf() === b2.valueOf();
      if (a.toString !== Object.prototype.toString && typeof a.toString === "function" && typeof b2.toString === "function")
        return a.toString() === b2.toString();
      keys2 = Object.keys(a);
      length2 = keys2.length;
      if (length2 !== Object.keys(b2).length)
        return false;
      for (i = length2; i-- !== 0; )
        if (!Object.prototype.hasOwnProperty.call(b2, keys2[i]))
          return false;
      if (hasElementType && a instanceof Element)
        return false;
      for (i = length2; i-- !== 0; ) {
        if ((keys2[i] === "_owner" || keys2[i] === "__v" || keys2[i] === "__o") && a.$$typeof) {
          continue;
        }
        if (!equal(a[keys2[i]], b2[keys2[i]]))
          return false;
      }
      return true;
    }
    return a !== a && b2 !== b2;
  }
  var reactFastCompare = function isEqual2(a, b2) {
    try {
      return equal(a, b2);
    } catch (error) {
      if ((error.message || "").match(/stack|recursion/i)) {
        console.warn("react-fast-compare cannot handle circular refs");
        return false;
      }
      throw error;
    }
  };
  const isEqual = /* @__PURE__ */ getDefaultExportFromCjs(reactFastCompare);
  function useStyleConfigImpl(themeKey, props = {}) {
    var _a4;
    const { styleConfig: styleConfigProp, ...rest } = props;
    const { theme: theme2, colorMode } = useChakra();
    const themeStyleConfig = themeKey ? memoizedGet(theme2, `components.${themeKey}`) : void 0;
    const styleConfig = styleConfigProp || themeStyleConfig;
    const mergedProps = mergeWith(
      { theme: theme2, colorMode },
      (_a4 = styleConfig == null ? void 0 : styleConfig.defaultProps) != null ? _a4 : {},
      filterUndefined(omit(rest, ["children"]))
    );
    const stylesRef = reactExports.useRef({});
    if (styleConfig) {
      const getStyles = resolveStyleConfig(styleConfig);
      const styles2 = getStyles(mergedProps);
      const isStyleEqual = isEqual(stylesRef.current, styles2);
      if (!isStyleEqual) {
        stylesRef.current = styles2;
      }
    }
    return stylesRef.current;
  }
  function useStyleConfig(themeKey, props = {}) {
    return useStyleConfigImpl(themeKey, props);
  }
  function useMultiStyleConfig(themeKey, props = {}) {
    return useStyleConfigImpl(themeKey, props);
  }
  var allPropNames = /* @__PURE__ */ new Set([
    ...propNames,
    "textStyle",
    "layerStyle",
    "apply",
    "noOfLines",
    "focusBorderColor",
    "errorBorderColor",
    "as",
    "__css",
    "css",
    "sx"
  ]);
  var validHTMLProps = /* @__PURE__ */ new Set([
    "htmlWidth",
    "htmlHeight",
    "htmlSize",
    "htmlTranslate"
  ]);
  function shouldForwardProp(prop) {
    return validHTMLProps.has(prop) || !allPropNames.has(prop);
  }
  function assignAfter(target, ...sources) {
    if (target == null) {
      throw new TypeError("Cannot convert undefined or null to object");
    }
    const result = { ...target };
    for (const nextSource of sources) {
      if (nextSource == null)
        continue;
      for (const nextKey in nextSource) {
        if (!Object.prototype.hasOwnProperty.call(nextSource, nextKey))
          continue;
        if (nextKey in result)
          delete result[nextKey];
        result[nextKey] = nextSource[nextKey];
      }
    }
    return result;
  }
  var reactPropsRegex = /^((children|dangerouslySetInnerHTML|key|ref|autoFocus|defaultValue|defaultChecked|innerHTML|suppressContentEditableWarning|suppressHydrationWarning|valueLink|abbr|accept|acceptCharset|accessKey|action|allow|allowUserMedia|allowPaymentRequest|allowFullScreen|allowTransparency|alt|async|autoComplete|autoPlay|capture|cellPadding|cellSpacing|challenge|charSet|checked|cite|classID|className|cols|colSpan|content|contentEditable|contextMenu|controls|controlsList|coords|crossOrigin|data|dateTime|decoding|default|defer|dir|disabled|disablePictureInPicture|disableRemotePlayback|download|draggable|encType|enterKeyHint|form|formAction|formEncType|formMethod|formNoValidate|formTarget|frameBorder|headers|height|hidden|high|href|hrefLang|htmlFor|httpEquiv|id|inputMode|integrity|is|keyParams|keyType|kind|label|lang|list|loading|loop|low|marginHeight|marginWidth|max|maxLength|media|mediaGroup|method|min|minLength|multiple|muted|name|nonce|noValidate|open|optimum|pattern|placeholder|playsInline|poster|preload|profile|radioGroup|readOnly|referrerPolicy|rel|required|reversed|role|rows|rowSpan|sandbox|scope|scoped|scrolling|seamless|selected|shape|size|sizes|slot|span|spellCheck|src|srcDoc|srcLang|srcSet|start|step|style|summary|tabIndex|target|title|translate|type|useMap|value|width|wmode|wrap|about|datatype|inlist|prefix|property|resource|typeof|vocab|autoCapitalize|autoCorrect|autoSave|color|incremental|fallback|inert|itemProp|itemScope|itemType|itemID|itemRef|on|option|results|security|unselectable|accentHeight|accumulate|additive|alignmentBaseline|allowReorder|alphabetic|amplitude|arabicForm|ascent|attributeName|attributeType|autoReverse|azimuth|baseFrequency|baselineShift|baseProfile|bbox|begin|bias|by|calcMode|capHeight|clip|clipPathUnits|clipPath|clipRule|colorInterpolation|colorInterpolationFilters|colorProfile|colorRendering|contentScriptType|contentStyleType|cursor|cx|cy|d|decelerate|descent|diffuseConstant|direction|display|divisor|dominantBaseline|dur|dx|dy|edgeMode|elevation|enableBackground|end|exponent|externalResourcesRequired|fill|fillOpacity|fillRule|filter|filterRes|filterUnits|floodColor|floodOpacity|focusable|fontFamily|fontSize|fontSizeAdjust|fontStretch|fontStyle|fontVariant|fontWeight|format|from|fr|fx|fy|g1|g2|glyphName|glyphOrientationHorizontal|glyphOrientationVertical|glyphRef|gradientTransform|gradientUnits|hanging|horizAdvX|horizOriginX|ideographic|imageRendering|in|in2|intercept|k|k1|k2|k3|k4|kernelMatrix|kernelUnitLength|kerning|keyPoints|keySplines|keyTimes|lengthAdjust|letterSpacing|lightingColor|limitingConeAngle|local|markerEnd|markerMid|markerStart|markerHeight|markerUnits|markerWidth|mask|maskContentUnits|maskUnits|mathematical|mode|numOctaves|offset|opacity|operator|order|orient|orientation|origin|overflow|overlinePosition|overlineThickness|panose1|paintOrder|pathLength|patternContentUnits|patternTransform|patternUnits|pointerEvents|points|pointsAtX|pointsAtY|pointsAtZ|preserveAlpha|preserveAspectRatio|primitiveUnits|r|radius|refX|refY|renderingIntent|repeatCount|repeatDur|requiredExtensions|requiredFeatures|restart|result|rotate|rx|ry|scale|seed|shapeRendering|slope|spacing|specularConstant|specularExponent|speed|spreadMethod|startOffset|stdDeviation|stemh|stemv|stitchTiles|stopColor|stopOpacity|strikethroughPosition|strikethroughThickness|string|stroke|strokeDasharray|strokeDashoffset|strokeLinecap|strokeLinejoin|strokeMiterlimit|strokeOpacity|strokeWidth|surfaceScale|systemLanguage|tableValues|targetX|targetY|textAnchor|textDecoration|textRendering|textLength|to|transform|u1|u2|underlinePosition|underlineThickness|unicode|unicodeBidi|unicodeRange|unitsPerEm|vAlphabetic|vHanging|vIdeographic|vMathematical|values|vectorEffect|version|vertAdvY|vertOriginX|vertOriginY|viewBox|viewTarget|visibility|widths|wordSpacing|writingMode|x|xHeight|x1|x2|xChannelSelector|xlinkActuate|xlinkArcrole|xlinkHref|xlinkRole|xlinkShow|xlinkTitle|xlinkType|xmlBase|xmlns|xmlnsXlink|xmlLang|xmlSpace|y|y1|y2|yChannelSelector|z|zoomAndPan|for|class|autofocus)|(([Dd][Aa][Tt][Aa]|[Aa][Rr][Ii][Aa]|x)-.*))$/;
  var isPropValid = /* @__PURE__ */ memoize$2(
    function(prop) {
      return reactPropsRegex.test(prop) || prop.charCodeAt(0) === 111 && prop.charCodeAt(1) === 110 && prop.charCodeAt(2) < 91;
    }
    /* Z+1 */
  );
  var testOmitPropsOnStringTag = isPropValid;
  var testOmitPropsOnComponent = function testOmitPropsOnComponent2(key) {
    return key !== "theme";
  };
  var getDefaultShouldForwardProp = function getDefaultShouldForwardProp2(tag) {
    return typeof tag === "string" && // 96 is one less than the char code
    // for "a" so this is checking that
    // it's a lowercase character
    tag.charCodeAt(0) > 96 ? testOmitPropsOnStringTag : testOmitPropsOnComponent;
  };
  var composeShouldForwardProps = function composeShouldForwardProps2(tag, options, isReal) {
    var shouldForwardProp2;
    if (options) {
      var optionsShouldForwardProp = options.shouldForwardProp;
      shouldForwardProp2 = tag.__emotion_forwardProp && optionsShouldForwardProp ? function(propName) {
        return tag.__emotion_forwardProp(propName) && optionsShouldForwardProp(propName);
      } : optionsShouldForwardProp;
    }
    if (typeof shouldForwardProp2 !== "function" && isReal) {
      shouldForwardProp2 = tag.__emotion_forwardProp;
    }
    return shouldForwardProp2;
  };
  var Insertion = function Insertion2(_ref) {
    var cache = _ref.cache, serialized = _ref.serialized, isStringTag = _ref.isStringTag;
    registerStyles(cache, serialized, isStringTag);
    useInsertionEffectAlwaysWithSyncFallback(function() {
      return insertStyles(cache, serialized, isStringTag);
    });
    return null;
  };
  var createStyled = function createStyled2(tag, options) {
    var isReal = tag.__emotion_real === tag;
    var baseTag = isReal && tag.__emotion_base || tag;
    var identifierName;
    var targetClassName;
    if (options !== void 0) {
      identifierName = options.label;
      targetClassName = options.target;
    }
    var shouldForwardProp2 = composeShouldForwardProps(tag, options, isReal);
    var defaultShouldForwardProp = shouldForwardProp2 || getDefaultShouldForwardProp(baseTag);
    var shouldUseAs = !defaultShouldForwardProp("as");
    return function() {
      var args = arguments;
      var styles2 = isReal && tag.__emotion_styles !== void 0 ? tag.__emotion_styles.slice(0) : [];
      if (identifierName !== void 0) {
        styles2.push("label:" + identifierName + ";");
      }
      if (args[0] == null || args[0].raw === void 0) {
        styles2.push.apply(styles2, args);
      } else {
        styles2.push(args[0][0]);
        var len = args.length;
        var i = 1;
        for (; i < len; i++) {
          styles2.push(args[i], args[0][i]);
        }
      }
      var Styled = withEmotionCache(function(props, cache, ref) {
        var FinalTag = shouldUseAs && props.as || baseTag;
        var className = "";
        var classInterpolations = [];
        var mergedProps = props;
        if (props.theme == null) {
          mergedProps = {};
          for (var key in props) {
            mergedProps[key] = props[key];
          }
          mergedProps.theme = reactExports.useContext(ThemeContext);
        }
        if (typeof props.className === "string") {
          className = getRegisteredStyles(cache.registered, classInterpolations, props.className);
        } else if (props.className != null) {
          className = props.className + " ";
        }
        var serialized = serializeStyles(styles2.concat(classInterpolations), cache.registered, mergedProps);
        className += cache.key + "-" + serialized.name;
        if (targetClassName !== void 0) {
          className += " " + targetClassName;
        }
        var finalShouldForwardProp = shouldUseAs && shouldForwardProp2 === void 0 ? getDefaultShouldForwardProp(FinalTag) : defaultShouldForwardProp;
        var newProps = {};
        for (var _key in props) {
          if (shouldUseAs && _key === "as")
            continue;
          if (
            // $FlowFixMe
            finalShouldForwardProp(_key)
          ) {
            newProps[_key] = props[_key];
          }
        }
        newProps.className = className;
        newProps.ref = ref;
        return /* @__PURE__ */ reactExports.createElement(reactExports.Fragment, null, /* @__PURE__ */ reactExports.createElement(Insertion, {
          cache,
          serialized,
          isStringTag: typeof FinalTag === "string"
        }), /* @__PURE__ */ reactExports.createElement(FinalTag, newProps));
      });
      Styled.displayName = identifierName !== void 0 ? identifierName : "Styled(" + (typeof baseTag === "string" ? baseTag : baseTag.displayName || baseTag.name || "Component") + ")";
      Styled.defaultProps = tag.defaultProps;
      Styled.__emotion_real = Styled;
      Styled.__emotion_base = baseTag;
      Styled.__emotion_styles = styles2;
      Styled.__emotion_forwardProp = shouldForwardProp2;
      Object.defineProperty(Styled, "toString", {
        value: function value() {
          if (targetClassName === void 0 && false) {
            return "NO_COMPONENT_SELECTOR";
          }
          return "." + targetClassName;
        }
      });
      Styled.withComponent = function(nextTag, nextOptions) {
        return createStyled2(nextTag, _extends({}, options, nextOptions, {
          shouldForwardProp: composeShouldForwardProps(Styled, nextOptions, true)
        })).apply(void 0, styles2);
      };
      return Styled;
    };
  };
  var tags = [
    "a",
    "abbr",
    "address",
    "area",
    "article",
    "aside",
    "audio",
    "b",
    "base",
    "bdi",
    "bdo",
    "big",
    "blockquote",
    "body",
    "br",
    "button",
    "canvas",
    "caption",
    "cite",
    "code",
    "col",
    "colgroup",
    "data",
    "datalist",
    "dd",
    "del",
    "details",
    "dfn",
    "dialog",
    "div",
    "dl",
    "dt",
    "em",
    "embed",
    "fieldset",
    "figcaption",
    "figure",
    "footer",
    "form",
    "h1",
    "h2",
    "h3",
    "h4",
    "h5",
    "h6",
    "head",
    "header",
    "hgroup",
    "hr",
    "html",
    "i",
    "iframe",
    "img",
    "input",
    "ins",
    "kbd",
    "keygen",
    "label",
    "legend",
    "li",
    "link",
    "main",
    "map",
    "mark",
    "marquee",
    "menu",
    "menuitem",
    "meta",
    "meter",
    "nav",
    "noscript",
    "object",
    "ol",
    "optgroup",
    "option",
    "output",
    "p",
    "param",
    "picture",
    "pre",
    "progress",
    "q",
    "rp",
    "rt",
    "ruby",
    "s",
    "samp",
    "script",
    "section",
    "select",
    "small",
    "source",
    "span",
    "strong",
    "style",
    "sub",
    "summary",
    "sup",
    "table",
    "tbody",
    "td",
    "textarea",
    "tfoot",
    "th",
    "thead",
    "time",
    "title",
    "tr",
    "track",
    "u",
    "ul",
    "var",
    "video",
    "wbr",
    // SVG
    "circle",
    "clipPath",
    "defs",
    "ellipse",
    "foreignObject",
    "g",
    "image",
    "line",
    "linearGradient",
    "mask",
    "path",
    "pattern",
    "polygon",
    "polyline",
    "radialGradient",
    "rect",
    "stop",
    "svg",
    "text",
    "tspan"
  ];
  var newStyled = createStyled.bind();
  tags.forEach(function(tagName) {
    newStyled[tagName] = newStyled(tagName);
  });
  var _a;
  var emotion_styled = (_a = newStyled.default) != null ? _a : newStyled;
  var toCSSObject = ({ baseStyle: baseStyle2 }) => (props) => {
    const { theme: theme2, css: cssProp, __css, sx, ...rest } = props;
    const styleProps2 = objectFilter(rest, (_2, prop) => isStyleProp(prop));
    const finalBaseStyle = runIfFn(baseStyle2, props);
    const finalStyles = assignAfter(
      {},
      __css,
      finalBaseStyle,
      filterUndefined(styleProps2),
      sx
    );
    const computedCSS = css(finalStyles)(props.theme);
    return cssProp ? [computedCSS, cssProp] : computedCSS;
  };
  function styled(component, options) {
    const { baseStyle: baseStyle2, ...styledOptions } = options != null ? options : {};
    if (!styledOptions.shouldForwardProp) {
      styledOptions.shouldForwardProp = shouldForwardProp;
    }
    const styleObject = toCSSObject({ baseStyle: baseStyle2 });
    const Component = emotion_styled(
      component,
      styledOptions
    )(styleObject);
    const chakraComponent = React.forwardRef(function ChakraComponent(props, ref) {
      const { colorMode, forced } = useColorMode();
      return React.createElement(Component, {
        ref,
        "data-theme": forced ? colorMode : void 0,
        ...props
      });
    });
    return chakraComponent;
  }
  function factory() {
    const cache = /* @__PURE__ */ new Map();
    return new Proxy(styled, {
      /**
       * @example
       * const Div = chakra("div")
       * const WithChakra = chakra(AnotherComponent)
       */
      apply(target, thisArg, argArray) {
        return styled(...argArray);
      },
      /**
       * @example
       * <chakra.div />
       */
      get(_2, element) {
        if (!cache.has(element)) {
          cache.set(element, styled(element));
        }
        return cache.get(element);
      }
    });
  }
  var chakra = factory();
  function forwardRef(component) {
    return reactExports.forwardRef(component);
  }
  function createContext(options = {}) {
    const {
      strict = true,
      errorMessage = "useContext: `context` is undefined. Seems you forgot to wrap component within the Provider",
      name
    } = options;
    const Context = reactExports.createContext(void 0);
    Context.displayName = name;
    function useContext() {
      var _a4;
      const context = reactExports.useContext(Context);
      if (!context && strict) {
        const error = new Error(errorMessage);
        error.name = "ContextError";
        (_a4 = Error.captureStackTrace) == null ? void 0 : _a4.call(Error, error, useContext);
        throw error;
      }
      return context;
    }
    return [
      Context.Provider,
      useContext,
      Context
    ];
  }
  function ThemeProvider(props) {
    const { cssVarsRoot, theme: theme2, children } = props;
    const computedTheme = reactExports.useMemo(() => toCSSVar(theme2), [theme2]);
    return /* @__PURE__ */ jsxRuntimeExports.jsxs(ThemeProvider$1, { theme: computedTheme, children: [
      /* @__PURE__ */ jsxRuntimeExports.jsx(CSSVars, { root: cssVarsRoot }),
      children
    ] });
  }
  function CSSVars({ root = ":host, :root" }) {
    const selector = [root, `[data-theme]`].join(",");
    return /* @__PURE__ */ jsxRuntimeExports.jsx(Global, { styles: (theme2) => ({ [selector]: theme2.__cssVars }) });
  }
  createContext({
    name: "StylesContext",
    errorMessage: "useStyles: `styles` is undefined. Seems you forgot to wrap the components in `<StylesProvider />` "
  });
  function GlobalStyle() {
    const { colorMode } = useColorMode();
    return /* @__PURE__ */ jsxRuntimeExports.jsx(
      Global,
      {
        styles: (theme2) => {
          const styleObjectOrFn = memoizedGet(theme2, "styles.global");
          const globalStyles = runIfFn(styleObjectOrFn, { theme: theme2, colorMode });
          if (!globalStyles)
            return void 0;
          const styles2 = css(globalStyles)(theme2);
          return styles2;
        }
      }
    );
  }
  var EnvironmentContext = reactExports.createContext({
    getDocument() {
      return document;
    },
    getWindow() {
      return window;
    }
  });
  EnvironmentContext.displayName = "EnvironmentContext";
  function EnvironmentProvider(props) {
    const { children, environment: environmentProp, disabled } = props;
    const ref = reactExports.useRef(null);
    const context = reactExports.useMemo(() => {
      if (environmentProp)
        return environmentProp;
      return {
        getDocument: () => {
          var _a4, _b3;
          return (_b3 = (_a4 = ref.current) == null ? void 0 : _a4.ownerDocument) != null ? _b3 : document;
        },
        getWindow: () => {
          var _a4, _b3;
          return (_b3 = (_a4 = ref.current) == null ? void 0 : _a4.ownerDocument.defaultView) != null ? _b3 : window;
        }
      };
    }, [environmentProp]);
    const showSpan = !disabled || !environmentProp;
    return /* @__PURE__ */ jsxRuntimeExports.jsxs(EnvironmentContext.Provider, { value: context, children: [
      children,
      showSpan && /* @__PURE__ */ jsxRuntimeExports.jsx("span", { id: "__chakra_env", hidden: true, ref })
    ] });
  }
  EnvironmentProvider.displayName = "EnvironmentProvider";
  var ChakraProvider$1 = (props) => {
    const {
      children,
      colorModeManager,
      portalZIndex,
      resetScope,
      resetCSS = true,
      theme: theme2 = {},
      environment,
      cssVarsRoot,
      disableEnvironment,
      disableGlobalStyle
    } = props;
    const _children = /* @__PURE__ */ jsxRuntimeExports.jsx(
      EnvironmentProvider,
      {
        environment,
        disabled: disableEnvironment,
        children
      }
    );
    return /* @__PURE__ */ jsxRuntimeExports.jsx(ThemeProvider, { theme: theme2, cssVarsRoot, children: /* @__PURE__ */ jsxRuntimeExports.jsxs(
      ColorModeProvider,
      {
        colorModeManager,
        options: theme2.config,
        children: [
          resetCSS ? /* @__PURE__ */ jsxRuntimeExports.jsx(CSSReset, { scope: resetScope }) : /* @__PURE__ */ jsxRuntimeExports.jsx(CSSPolyfill, {}),
          !disableGlobalStyle && /* @__PURE__ */ jsxRuntimeExports.jsx(GlobalStyle, {}),
          portalZIndex ? /* @__PURE__ */ jsxRuntimeExports.jsx(PortalManager, { zIndex: portalZIndex, children: _children }) : _children
        ]
      }
    ) });
  };
  var findById = (arr, id2) => arr.find((toast) => toast.id === id2);
  function findToast(toasts, id2) {
    const position2 = getToastPosition(toasts, id2);
    const index = position2 ? toasts[position2].findIndex((toast) => toast.id === id2) : -1;
    return {
      position: position2,
      index
    };
  }
  function getToastPosition(toasts, id2) {
    for (const [position2, values] of Object.entries(toasts)) {
      if (findById(values, id2)) {
        return position2;
      }
    }
  }
  function getToastStyle(position2) {
    const isRighty = position2.includes("right");
    const isLefty = position2.includes("left");
    let alignItems = "center";
    if (isRighty)
      alignItems = "flex-end";
    if (isLefty)
      alignItems = "flex-start";
    return {
      display: "flex",
      flexDirection: "column",
      alignItems
    };
  }
  function getToastListStyle(position2) {
    const isTopOrBottom = position2 === "top" || position2 === "bottom";
    const margin = isTopOrBottom ? "0 auto" : void 0;
    const top = position2.includes("top") ? "env(safe-area-inset-top, 0px)" : void 0;
    const bottom = position2.includes("bottom") ? "env(safe-area-inset-bottom, 0px)" : void 0;
    const right = !position2.includes("left") ? "env(safe-area-inset-right, 0px)" : void 0;
    const left = !position2.includes("right") ? "env(safe-area-inset-left, 0px)" : void 0;
    return {
      position: "fixed",
      zIndex: "var(--toast-z-index, 5500)",
      pointerEvents: "none",
      display: "flex",
      flexDirection: "column",
      margin,
      top,
      bottom,
      right,
      left
    };
  }
  function useCallbackRef(callback, deps = []) {
    const callbackRef = reactExports.useRef(callback);
    reactExports.useEffect(() => {
      callbackRef.current = callback;
    });
    return reactExports.useCallback((...args) => {
      var _a4;
      return (_a4 = callbackRef.current) == null ? void 0 : _a4.call(callbackRef, ...args);
    }, deps);
  }
  function useTimeout(callback, delay2) {
    const fn = useCallbackRef(callback);
    reactExports.useEffect(() => {
      if (delay2 == null)
        return void 0;
      let timeoutId = null;
      timeoutId = window.setTimeout(() => {
        fn();
      }, delay2);
      return () => {
        if (timeoutId) {
          window.clearTimeout(timeoutId);
        }
      };
    }, [delay2, fn]);
  }
  function useUpdateEffect(callback, deps) {
    const renderCycleRef = reactExports.useRef(false);
    const effectCycleRef = reactExports.useRef(false);
    reactExports.useEffect(() => {
      const mounted = renderCycleRef.current;
      const run = mounted && effectCycleRef.current;
      if (run) {
        return callback();
      }
      effectCycleRef.current = true;
    }, deps);
    reactExports.useEffect(() => {
      renderCycleRef.current = true;
      return () => {
        renderCycleRef.current = false;
      };
    }, []);
  }
  const MotionConfigContext = reactExports.createContext({
    transformPagePoint: (p2) => p2,
    isStatic: false,
    reducedMotion: "never"
  });
  const MotionContext = reactExports.createContext({});
  const PresenceContext = reactExports.createContext(null);
  const isBrowser = typeof document !== "undefined";
  const useIsomorphicLayoutEffect = isBrowser ? reactExports.useLayoutEffect : reactExports.useEffect;
  const LazyContext = reactExports.createContext({ strict: false });
  const camelToDash = (str) => str.replace(/([a-z])([A-Z])/gu, "$1-$2").toLowerCase();
  const optimizedAppearDataId = "framerAppearId";
  const optimizedAppearDataAttribute = "data-" + camelToDash(optimizedAppearDataId);
  const MotionGlobalConfig = {
    skipAnimations: false,
    useManualTiming: false
  };
  class Queue {
    constructor() {
      this.order = [];
      this.scheduled = /* @__PURE__ */ new Set();
    }
    add(process2) {
      if (!this.scheduled.has(process2)) {
        this.scheduled.add(process2);
        this.order.push(process2);
        return true;
      }
    }
    remove(process2) {
      const index = this.order.indexOf(process2);
      if (index !== -1) {
        this.order.splice(index, 1);
        this.scheduled.delete(process2);
      }
    }
    clear() {
      this.order.length = 0;
      this.scheduled.clear();
    }
  }
  function createRenderStep(runNextFrame) {
    let thisFrame = new Queue();
    let nextFrame = new Queue();
    let numToRun = 0;
    let isProcessing = false;
    let flushNextFrame = false;
    const toKeepAlive = /* @__PURE__ */ new WeakSet();
    const step = {
      /**
       * Schedule a process to run on the next frame.
       */
      schedule: (callback, keepAlive = false, immediate = false) => {
        const addToCurrentFrame = immediate && isProcessing;
        const queue = addToCurrentFrame ? thisFrame : nextFrame;
        if (keepAlive)
          toKeepAlive.add(callback);
        if (queue.add(callback) && addToCurrentFrame && isProcessing) {
          numToRun = thisFrame.order.length;
        }
        return callback;
      },
      /**
       * Cancel the provided callback from running on the next frame.
       */
      cancel: (callback) => {
        nextFrame.remove(callback);
        toKeepAlive.delete(callback);
      },
      /**
       * Execute all schedule callbacks.
       */
      process: (frameData2) => {
        if (isProcessing) {
          flushNextFrame = true;
          return;
        }
        isProcessing = true;
        [thisFrame, nextFrame] = [nextFrame, thisFrame];
        nextFrame.clear();
        numToRun = thisFrame.order.length;
        if (numToRun) {
          for (let i = 0; i < numToRun; i++) {
            const callback = thisFrame.order[i];
            if (toKeepAlive.has(callback)) {
              step.schedule(callback);
              runNextFrame();
            }
            callback(frameData2);
          }
        }
        isProcessing = false;
        if (flushNextFrame) {
          flushNextFrame = false;
          step.process(frameData2);
        }
      }
    };
    return step;
  }
  const stepsOrder = [
    "read",
    // Read
    "resolveKeyframes",
    // Write/Read/Write/Read
    "update",
    // Compute
    "preRender",
    // Compute
    "render",
    // Write
    "postRender"
    // Compute
  ];
  const maxElapsed = 40;
  function createRenderBatcher(scheduleNextBatch, allowKeepAlive) {
    let runNextFrame = false;
    let useDefaultElapsed = true;
    const state2 = {
      delta: 0,
      timestamp: 0,
      isProcessing: false
    };
    const steps2 = stepsOrder.reduce((acc, key) => {
      acc[key] = createRenderStep(() => runNextFrame = true);
      return acc;
    }, {});
    const processStep = (stepId) => {
      steps2[stepId].process(state2);
    };
    const processBatch = () => {
      const timestamp = performance.now();
      runNextFrame = false;
      state2.delta = useDefaultElapsed ? 1e3 / 60 : Math.max(Math.min(timestamp - state2.timestamp, maxElapsed), 1);
      state2.timestamp = timestamp;
      state2.isProcessing = true;
      stepsOrder.forEach(processStep);
      state2.isProcessing = false;
      if (runNextFrame && allowKeepAlive) {
        useDefaultElapsed = false;
        scheduleNextBatch(processBatch);
      }
    };
    const wake = () => {
      runNextFrame = true;
      useDefaultElapsed = true;
      if (!state2.isProcessing) {
        scheduleNextBatch(processBatch);
      }
    };
    const schedule = stepsOrder.reduce((acc, key) => {
      const step = steps2[key];
      acc[key] = (process2, keepAlive = false, immediate = false) => {
        if (!runNextFrame)
          wake();
        return step.schedule(process2, keepAlive, immediate);
      };
      return acc;
    }, {});
    const cancel = (process2) => stepsOrder.forEach((key) => steps2[key].cancel(process2));
    return { schedule, cancel, state: state2, steps: steps2 };
  }
  const { schedule: microtask, cancel: cancelMicrotask } = createRenderBatcher(queueMicrotask, false);
  function useVisualElement(Component, visualState, props, createVisualElement) {
    const { visualElement: parent } = reactExports.useContext(MotionContext);
    const lazyContext = reactExports.useContext(LazyContext);
    const presenceContext = reactExports.useContext(PresenceContext);
    const reducedMotionConfig = reactExports.useContext(MotionConfigContext).reducedMotion;
    const visualElementRef = reactExports.useRef();
    createVisualElement = createVisualElement || lazyContext.renderer;
    if (!visualElementRef.current && createVisualElement) {
      visualElementRef.current = createVisualElement(Component, {
        visualState,
        parent,
        props,
        presenceContext,
        blockInitialAnimation: presenceContext ? presenceContext.initial === false : false,
        reducedMotionConfig
      });
    }
    const visualElement = visualElementRef.current;
    reactExports.useInsertionEffect(() => {
      visualElement && visualElement.update(props, presenceContext);
    });
    const wantsHandoff = reactExports.useRef(Boolean(props[optimizedAppearDataAttribute] && !window.HandoffComplete));
    useIsomorphicLayoutEffect(() => {
      if (!visualElement)
        return;
      microtask.postRender(visualElement.render);
      if (wantsHandoff.current && visualElement.animationState) {
        visualElement.animationState.animateChanges();
      }
    });
    reactExports.useEffect(() => {
      if (!visualElement)
        return;
      visualElement.updateFeatures();
      if (!wantsHandoff.current && visualElement.animationState) {
        visualElement.animationState.animateChanges();
      }
      if (wantsHandoff.current) {
        wantsHandoff.current = false;
        window.HandoffComplete = true;
      }
    });
    return visualElement;
  }
  function isRefObject(ref) {
    return ref && typeof ref === "object" && Object.prototype.hasOwnProperty.call(ref, "current");
  }
  function useMotionRef(visualState, visualElement, externalRef) {
    return reactExports.useCallback(
      (instance) => {
        instance && visualState.mount && visualState.mount(instance);
        if (visualElement) {
          instance ? visualElement.mount(instance) : visualElement.unmount();
        }
        if (externalRef) {
          if (typeof externalRef === "function") {
            externalRef(instance);
          } else if (isRefObject(externalRef)) {
            externalRef.current = instance;
          }
        }
      },
      /**
       * Only pass a new ref callback to React if we've received a visual element
       * factory. Otherwise we'll be mounting/remounting every time externalRef
       * or other dependencies change.
       */
      [visualElement]
    );
  }
  function isVariantLabel(v2) {
    return typeof v2 === "string" || Array.isArray(v2);
  }
  function isAnimationControls(v2) {
    return v2 !== null && typeof v2 === "object" && typeof v2.start === "function";
  }
  const variantPriorityOrder = [
    "animate",
    "whileInView",
    "whileFocus",
    "whileHover",
    "whileTap",
    "whileDrag",
    "exit"
  ];
  const variantProps = ["initial", ...variantPriorityOrder];
  function isControllingVariants(props) {
    return isAnimationControls(props.animate) || variantProps.some((name) => isVariantLabel(props[name]));
  }
  function isVariantNode(props) {
    return Boolean(isControllingVariants(props) || props.variants);
  }
  function getCurrentTreeVariants(props, context) {
    if (isControllingVariants(props)) {
      const { initial, animate } = props;
      return {
        initial: initial === false || isVariantLabel(initial) ? initial : void 0,
        animate: isVariantLabel(animate) ? animate : void 0
      };
    }
    return props.inherit !== false ? context : {};
  }
  function useCreateMotionContext(props) {
    const { initial, animate } = getCurrentTreeVariants(props, reactExports.useContext(MotionContext));
    return reactExports.useMemo(() => ({ initial, animate }), [variantLabelsAsDependency(initial), variantLabelsAsDependency(animate)]);
  }
  function variantLabelsAsDependency(prop) {
    return Array.isArray(prop) ? prop.join(" ") : prop;
  }
  const featureProps = {
    animation: [
      "animate",
      "variants",
      "whileHover",
      "whileTap",
      "exit",
      "whileInView",
      "whileFocus",
      "whileDrag"
    ],
    exit: ["exit"],
    drag: ["drag", "dragControls"],
    focus: ["whileFocus"],
    hover: ["whileHover", "onHoverStart", "onHoverEnd"],
    tap: ["whileTap", "onTap", "onTapStart", "onTapCancel"],
    pan: ["onPan", "onPanStart", "onPanSessionStart", "onPanEnd"],
    inView: ["whileInView", "onViewportEnter", "onViewportLeave"],
    layout: ["layout", "layoutId"]
  };
  const featureDefinitions = {};
  for (const key in featureProps) {
    featureDefinitions[key] = {
      isEnabled: (props) => featureProps[key].some((name) => !!props[name])
    };
  }
  function loadFeatures(features) {
    for (const key in features) {
      featureDefinitions[key] = {
        ...featureDefinitions[key],
        ...features[key]
      };
    }
  }
  const LayoutGroupContext = reactExports.createContext({});
  const SwitchLayoutGroupContext = reactExports.createContext({});
  const motionComponentSymbol = Symbol.for("motionComponentSymbol");
  function createMotionComponent({ preloadedFeatures: preloadedFeatures2, createVisualElement, useRender, useVisualState, Component }) {
    preloadedFeatures2 && loadFeatures(preloadedFeatures2);
    function MotionComponent(props, externalRef) {
      let MeasureLayout2;
      const configAndProps = {
        ...reactExports.useContext(MotionConfigContext),
        ...props,
        layoutId: useLayoutId(props)
      };
      const { isStatic } = configAndProps;
      const context = useCreateMotionContext(props);
      const visualState = useVisualState(props, isStatic);
      if (!isStatic && isBrowser) {
        context.visualElement = useVisualElement(Component, visualState, configAndProps, createVisualElement);
        const initialLayoutGroupConfig = reactExports.useContext(SwitchLayoutGroupContext);
        const isStrict = reactExports.useContext(LazyContext).strict;
        if (context.visualElement) {
          MeasureLayout2 = context.visualElement.loadFeatures(
            // Note: Pass the full new combined props to correctly re-render dynamic feature components.
            configAndProps,
            isStrict,
            preloadedFeatures2,
            initialLayoutGroupConfig
          );
        }
      }
      return jsxRuntimeExports.jsxs(MotionContext.Provider, { value: context, children: [MeasureLayout2 && context.visualElement ? jsxRuntimeExports.jsx(MeasureLayout2, { visualElement: context.visualElement, ...configAndProps }) : null, useRender(Component, props, useMotionRef(visualState, context.visualElement, externalRef), visualState, isStatic, context.visualElement)] });
    }
    const ForwardRefComponent = reactExports.forwardRef(MotionComponent);
    ForwardRefComponent[motionComponentSymbol] = Component;
    return ForwardRefComponent;
  }
  function useLayoutId({ layoutId }) {
    const layoutGroupId = reactExports.useContext(LayoutGroupContext).id;
    return layoutGroupId && layoutId !== void 0 ? layoutGroupId + "-" + layoutId : layoutId;
  }
  function createMotionProxy(createConfig) {
    function custom(Component, customMotionComponentConfig = {}) {
      return createMotionComponent(createConfig(Component, customMotionComponentConfig));
    }
    if (typeof Proxy === "undefined") {
      return custom;
    }
    const componentCache = /* @__PURE__ */ new Map();
    return new Proxy(custom, {
      /**
       * Called when `motion` is referenced with a prop: `motion.div`, `motion.input` etc.
       * The prop name is passed through as `key` and we can use that to generate a `motion`
       * DOM component with that name.
       */
      get: (_target, key) => {
        if (!componentCache.has(key)) {
          componentCache.set(key, custom(key));
        }
        return componentCache.get(key);
      }
    });
  }
  const lowercaseSVGElements = [
    "animate",
    "circle",
    "defs",
    "desc",
    "ellipse",
    "g",
    "image",
    "line",
    "filter",
    "marker",
    "mask",
    "metadata",
    "path",
    "pattern",
    "polygon",
    "polyline",
    "rect",
    "stop",
    "switch",
    "symbol",
    "svg",
    "text",
    "tspan",
    "use",
    "view"
  ];
  function isSVGComponent(Component) {
    if (
      /**
       * If it's not a string, it's a custom React component. Currently we only support
       * HTML custom React components.
       */
      typeof Component !== "string" || /**
       * If it contains a dash, the element is a custom HTML webcomponent.
       */
      Component.includes("-")
    ) {
      return false;
    } else if (
      /**
       * If it's in our list of lowercase SVG tags, it's an SVG component
       */
      lowercaseSVGElements.indexOf(Component) > -1 || /**
       * If it contains a capital letter, it's an SVG component
       */
      /[A-Z]/u.test(Component)
    ) {
      return true;
    }
    return false;
  }
  const scaleCorrectors = {};
  function addScaleCorrector(correctors) {
    Object.assign(scaleCorrectors, correctors);
  }
  const transformPropOrder = [
    "transformPerspective",
    "x",
    "y",
    "z",
    "translateX",
    "translateY",
    "translateZ",
    "scale",
    "scaleX",
    "scaleY",
    "rotate",
    "rotateX",
    "rotateY",
    "rotateZ",
    "skew",
    "skewX",
    "skewY"
  ];
  const transformProps = new Set(transformPropOrder);
  function isForcedMotionValue(key, { layout: layout2, layoutId }) {
    return transformProps.has(key) || key.startsWith("origin") || (layout2 || layoutId !== void 0) && (!!scaleCorrectors[key] || key === "opacity");
  }
  const isMotionValue = (value) => Boolean(value && value.getVelocity);
  const translateAlias = {
    x: "translateX",
    y: "translateY",
    z: "translateZ",
    transformPerspective: "perspective"
  };
  const numTransforms = transformPropOrder.length;
  function buildTransform(transform2, { enableHardwareAcceleration = true, allowTransformNone = true }, transformIsDefault, transformTemplate2) {
    let transformString = "";
    for (let i = 0; i < numTransforms; i++) {
      const key = transformPropOrder[i];
      if (transform2[key] !== void 0) {
        const transformName = translateAlias[key] || key;
        transformString += `${transformName}(${transform2[key]}) `;
      }
    }
    if (enableHardwareAcceleration && !transform2.z) {
      transformString += "translateZ(0)";
    }
    transformString = transformString.trim();
    if (transformTemplate2) {
      transformString = transformTemplate2(transform2, transformIsDefault ? "" : transformString);
    } else if (allowTransformNone && transformIsDefault) {
      transformString = "none";
    }
    return transformString;
  }
  const checkStringStartsWith = (token2) => (key) => typeof key === "string" && key.startsWith(token2);
  const isCSSVariableName = checkStringStartsWith("--");
  const startsAsVariableToken = checkStringStartsWith("var(--");
  const isCSSVariableToken = (value) => {
    const startsWithToken = startsAsVariableToken(value);
    if (!startsWithToken)
      return false;
    return singleCssVariableRegex.test(value.split("/*")[0].trim());
  };
  const singleCssVariableRegex = /var\(--(?:[\w-]+\s*|[\w-]+\s*,(?:\s*[^)(\s]|\s*\((?:[^)(]|\([^)(]*\))*\))+\s*)\)$/iu;
  const getValueAsType = (value, type) => {
    return type && typeof value === "number" ? type.transform(value) : value;
  };
  const clamp = (min, max, v2) => {
    if (v2 > max)
      return max;
    if (v2 < min)
      return min;
    return v2;
  };
  const number = {
    test: (v2) => typeof v2 === "number",
    parse: parseFloat,
    transform: (v2) => v2
  };
  const alpha = {
    ...number,
    transform: (v2) => clamp(0, 1, v2)
  };
  const scale = {
    ...number,
    default: 1
  };
  const sanitize = (v2) => Math.round(v2 * 1e5) / 1e5;
  const floatRegex = /-?(?:\d+(?:\.\d+)?|\.\d+)/gu;
  const colorRegex = /(?:#[\da-f]{3,8}|(?:rgb|hsl)a?\((?:-?[\d.]+%?[,\s]+){2}-?[\d.]+%?\s*(?:[,/]\s*)?(?:\b\d+(?:\.\d+)?|\.\d+)?%?\))/giu;
  const singleColorRegex = /^(?:#[\da-f]{3,8}|(?:rgb|hsl)a?\((?:-?[\d.]+%?[,\s]+){2}-?[\d.]+%?\s*(?:[,/]\s*)?(?:\b\d+(?:\.\d+)?|\.\d+)?%?\))$/iu;
  function isString(v2) {
    return typeof v2 === "string";
  }
  const createUnitType = (unit) => ({
    test: (v2) => isString(v2) && v2.endsWith(unit) && v2.split(" ").length === 1,
    parse: parseFloat,
    transform: (v2) => `${v2}${unit}`
  });
  const degrees = createUnitType("deg");
  const percent = createUnitType("%");
  const px = createUnitType("px");
  const vh = createUnitType("vh");
  const vw = createUnitType("vw");
  const progressPercentage = {
    ...percent,
    parse: (v2) => percent.parse(v2) / 100,
    transform: (v2) => percent.transform(v2 * 100)
  };
  const int = {
    ...number,
    transform: Math.round
  };
  const numberValueTypes = {
    // Border props
    borderWidth: px,
    borderTopWidth: px,
    borderRightWidth: px,
    borderBottomWidth: px,
    borderLeftWidth: px,
    borderRadius: px,
    radius: px,
    borderTopLeftRadius: px,
    borderTopRightRadius: px,
    borderBottomRightRadius: px,
    borderBottomLeftRadius: px,
    // Positioning props
    width: px,
    maxWidth: px,
    height: px,
    maxHeight: px,
    size: px,
    top: px,
    right: px,
    bottom: px,
    left: px,
    // Spacing props
    padding: px,
    paddingTop: px,
    paddingRight: px,
    paddingBottom: px,
    paddingLeft: px,
    margin: px,
    marginTop: px,
    marginRight: px,
    marginBottom: px,
    marginLeft: px,
    // Transform props
    rotate: degrees,
    rotateX: degrees,
    rotateY: degrees,
    rotateZ: degrees,
    scale,
    scaleX: scale,
    scaleY: scale,
    scaleZ: scale,
    skew: degrees,
    skewX: degrees,
    skewY: degrees,
    distance: px,
    translateX: px,
    translateY: px,
    translateZ: px,
    x: px,
    y: px,
    z: px,
    perspective: px,
    transformPerspective: px,
    opacity: alpha,
    originX: progressPercentage,
    originY: progressPercentage,
    originZ: px,
    // Misc
    zIndex: int,
    backgroundPositionX: px,
    backgroundPositionY: px,
    // SVG
    fillOpacity: alpha,
    strokeOpacity: alpha,
    numOctaves: int
  };
  function buildHTMLStyles(state2, latestValues, options, transformTemplate2) {
    const { style, vars: vars2, transform: transform2, transformOrigin } = state2;
    let hasTransform2 = false;
    let hasTransformOrigin = false;
    let transformIsNone = true;
    for (const key in latestValues) {
      const value = latestValues[key];
      if (isCSSVariableName(key)) {
        vars2[key] = value;
        continue;
      }
      const valueType = numberValueTypes[key];
      const valueAsType = getValueAsType(value, valueType);
      if (transformProps.has(key)) {
        hasTransform2 = true;
        transform2[key] = valueAsType;
        if (!transformIsNone)
          continue;
        if (value !== (valueType.default || 0))
          transformIsNone = false;
      } else if (key.startsWith("origin")) {
        hasTransformOrigin = true;
        transformOrigin[key] = valueAsType;
      } else {
        style[key] = valueAsType;
      }
    }
    if (!latestValues.transform) {
      if (hasTransform2 || transformTemplate2) {
        style.transform = buildTransform(state2.transform, options, transformIsNone, transformTemplate2);
      } else if (style.transform) {
        style.transform = "none";
      }
    }
    if (hasTransformOrigin) {
      const { originX = "50%", originY = "50%", originZ = 0 } = transformOrigin;
      style.transformOrigin = `${originX} ${originY} ${originZ}`;
    }
  }
  const createHtmlRenderState = () => ({
    style: {},
    transform: {},
    transformOrigin: {},
    vars: {}
  });
  function copyRawValuesOnly(target, source, props) {
    for (const key in source) {
      if (!isMotionValue(source[key]) && !isForcedMotionValue(key, props)) {
        target[key] = source[key];
      }
    }
  }
  function useInitialMotionValues({ transformTemplate: transformTemplate2 }, visualState, isStatic) {
    return reactExports.useMemo(() => {
      const state2 = createHtmlRenderState();
      buildHTMLStyles(state2, visualState, { enableHardwareAcceleration: !isStatic }, transformTemplate2);
      return Object.assign({}, state2.vars, state2.style);
    }, [visualState]);
  }
  function useStyle(props, visualState, isStatic) {
    const styleProp = props.style || {};
    const style = {};
    copyRawValuesOnly(style, styleProp, props);
    Object.assign(style, useInitialMotionValues(props, visualState, isStatic));
    return style;
  }
  function useHTMLProps(props, visualState, isStatic) {
    const htmlProps = {};
    const style = useStyle(props, visualState, isStatic);
    if (props.drag && props.dragListener !== false) {
      htmlProps.draggable = false;
      style.userSelect = style.WebkitUserSelect = style.WebkitTouchCallout = "none";
      style.touchAction = props.drag === true ? "none" : `pan-${props.drag === "x" ? "y" : "x"}`;
    }
    if (props.tabIndex === void 0 && (props.onTap || props.onTapStart || props.whileTap)) {
      htmlProps.tabIndex = 0;
    }
    htmlProps.style = style;
    return htmlProps;
  }
  const validMotionProps = /* @__PURE__ */ new Set([
    "animate",
    "exit",
    "variants",
    "initial",
    "style",
    "values",
    "variants",
    "transition",
    "transformTemplate",
    "custom",
    "inherit",
    "onBeforeLayoutMeasure",
    "onAnimationStart",
    "onAnimationComplete",
    "onUpdate",
    "onDragStart",
    "onDrag",
    "onDragEnd",
    "onMeasureDragConstraints",
    "onDirectionLock",
    "onDragTransitionEnd",
    "_dragX",
    "_dragY",
    "onHoverStart",
    "onHoverEnd",
    "onViewportEnter",
    "onViewportLeave",
    "globalTapTarget",
    "ignoreStrict",
    "viewport"
  ]);
  function isValidMotionProp(key) {
    return key.startsWith("while") || key.startsWith("drag") && key !== "draggable" || key.startsWith("layout") || key.startsWith("onTap") || key.startsWith("onPan") || key.startsWith("onLayout") || validMotionProps.has(key);
  }
  let shouldForward = (key) => !isValidMotionProp(key);
  function loadExternalIsValidProp(isValidProp) {
    if (!isValidProp)
      return;
    shouldForward = (key) => key.startsWith("on") ? !isValidMotionProp(key) : isValidProp(key);
  }
  try {
    loadExternalIsValidProp(require("@emotion/is-prop-valid").default);
  } catch (_a4) {
  }
  function filterProps(props, isDom, forwardMotionProps) {
    const filteredProps = {};
    for (const key in props) {
      if (key === "values" && typeof props.values === "object")
        continue;
      if (shouldForward(key) || forwardMotionProps === true && isValidMotionProp(key) || !isDom && !isValidMotionProp(key) || // If trying to use native HTML drag events, forward drag listeners
      props["draggable"] && key.startsWith("onDrag")) {
        filteredProps[key] = props[key];
      }
    }
    return filteredProps;
  }
  function calcOrigin$1(origin, offset, size2) {
    return typeof origin === "string" ? origin : px.transform(offset + size2 * origin);
  }
  function calcSVGTransformOrigin(dimensions, originX, originY) {
    const pxOriginX = calcOrigin$1(originX, dimensions.x, dimensions.width);
    const pxOriginY = calcOrigin$1(originY, dimensions.y, dimensions.height);
    return `${pxOriginX} ${pxOriginY}`;
  }
  const dashKeys = {
    offset: "stroke-dashoffset",
    array: "stroke-dasharray"
  };
  const camelKeys = {
    offset: "strokeDashoffset",
    array: "strokeDasharray"
  };
  function buildSVGPath(attrs, length2, spacing2 = 1, offset = 0, useDashCase = true) {
    attrs.pathLength = 1;
    const keys2 = useDashCase ? dashKeys : camelKeys;
    attrs[keys2.offset] = px.transform(-offset);
    const pathLength = px.transform(length2);
    const pathSpacing = px.transform(spacing2);
    attrs[keys2.array] = `${pathLength} ${pathSpacing}`;
  }
  function buildSVGAttrs(state2, {
    attrX,
    attrY,
    attrScale,
    originX,
    originY,
    pathLength,
    pathSpacing = 1,
    pathOffset = 0,
    // This is object creation, which we try to avoid per-frame.
    ...latest
  }, options, isSVGTag2, transformTemplate2) {
    buildHTMLStyles(state2, latest, options, transformTemplate2);
    if (isSVGTag2) {
      if (state2.style.viewBox) {
        state2.attrs.viewBox = state2.style.viewBox;
      }
      return;
    }
    state2.attrs = state2.style;
    state2.style = {};
    const { attrs, style, dimensions } = state2;
    if (attrs.transform) {
      if (dimensions)
        style.transform = attrs.transform;
      delete attrs.transform;
    }
    if (dimensions && (originX !== void 0 || originY !== void 0 || style.transform)) {
      style.transformOrigin = calcSVGTransformOrigin(dimensions, originX !== void 0 ? originX : 0.5, originY !== void 0 ? originY : 0.5);
    }
    if (attrX !== void 0)
      attrs.x = attrX;
    if (attrY !== void 0)
      attrs.y = attrY;
    if (attrScale !== void 0)
      attrs.scale = attrScale;
    if (pathLength !== void 0) {
      buildSVGPath(attrs, pathLength, pathSpacing, pathOffset, false);
    }
  }
  const createSvgRenderState = () => ({
    ...createHtmlRenderState(),
    attrs: {}
  });
  const isSVGTag = (tag) => typeof tag === "string" && tag.toLowerCase() === "svg";
  function useSVGProps(props, visualState, _isStatic, Component) {
    const visualProps = reactExports.useMemo(() => {
      const state2 = createSvgRenderState();
      buildSVGAttrs(state2, visualState, { enableHardwareAcceleration: false }, isSVGTag(Component), props.transformTemplate);
      return {
        ...state2.attrs,
        style: { ...state2.style }
      };
    }, [visualState]);
    if (props.style) {
      const rawStyles = {};
      copyRawValuesOnly(rawStyles, props.style, props);
      visualProps.style = { ...rawStyles, ...visualProps.style };
    }
    return visualProps;
  }
  function createUseRender(forwardMotionProps = false) {
    const useRender = (Component, props, ref, { latestValues }, isStatic) => {
      const useVisualProps = isSVGComponent(Component) ? useSVGProps : useHTMLProps;
      const visualProps = useVisualProps(props, latestValues, isStatic, Component);
      const filteredProps = filterProps(props, typeof Component === "string", forwardMotionProps);
      const elementProps = Component !== reactExports.Fragment ? { ...filteredProps, ...visualProps, ref } : {};
      const { children } = props;
      const renderedChildren = reactExports.useMemo(() => isMotionValue(children) ? children.get() : children, [children]);
      return reactExports.createElement(Component, {
        ...elementProps,
        children: renderedChildren
      });
    };
    return useRender;
  }
  function renderHTML(element, { style, vars: vars2 }, styleProp, projection) {
    Object.assign(element.style, style, projection && projection.getProjectionStyles(styleProp));
    for (const key in vars2) {
      element.style.setProperty(key, vars2[key]);
    }
  }
  const camelCaseAttributes = /* @__PURE__ */ new Set([
    "baseFrequency",
    "diffuseConstant",
    "kernelMatrix",
    "kernelUnitLength",
    "keySplines",
    "keyTimes",
    "limitingConeAngle",
    "markerHeight",
    "markerWidth",
    "numOctaves",
    "targetX",
    "targetY",
    "surfaceScale",
    "specularConstant",
    "specularExponent",
    "stdDeviation",
    "tableValues",
    "viewBox",
    "gradientTransform",
    "pathLength",
    "startOffset",
    "textLength",
    "lengthAdjust"
  ]);
  function renderSVG(element, renderState, _styleProp, projection) {
    renderHTML(element, renderState, void 0, projection);
    for (const key in renderState.attrs) {
      element.setAttribute(!camelCaseAttributes.has(key) ? camelToDash(key) : key, renderState.attrs[key]);
    }
  }
  function scrapeMotionValuesFromProps$1(props, prevProps, visualElement) {
    var _a4;
    const { style } = props;
    const newValues = {};
    for (const key in style) {
      if (isMotionValue(style[key]) || prevProps.style && isMotionValue(prevProps.style[key]) || isForcedMotionValue(key, props) || ((_a4 = visualElement === null || visualElement === void 0 ? void 0 : visualElement.getValue(key)) === null || _a4 === void 0 ? void 0 : _a4.liveStyle) !== void 0) {
        newValues[key] = style[key];
      }
    }
    return newValues;
  }
  function scrapeMotionValuesFromProps(props, prevProps, visualElement) {
    const newValues = scrapeMotionValuesFromProps$1(props, prevProps, visualElement);
    for (const key in props) {
      if (isMotionValue(props[key]) || isMotionValue(prevProps[key])) {
        const targetKey = transformPropOrder.indexOf(key) !== -1 ? "attr" + key.charAt(0).toUpperCase() + key.substring(1) : key;
        newValues[targetKey] = props[key];
      }
    }
    return newValues;
  }
  function resolveVariantFromProps(props, definition, custom, currentValues = {}, currentVelocity = {}) {
    if (typeof definition === "function") {
      definition = definition(custom !== void 0 ? custom : props.custom, currentValues, currentVelocity);
    }
    if (typeof definition === "string") {
      definition = props.variants && props.variants[definition];
    }
    if (typeof definition === "function") {
      definition = definition(custom !== void 0 ? custom : props.custom, currentValues, currentVelocity);
    }
    return definition;
  }
  function useConstant(init) {
    const ref = reactExports.useRef(null);
    if (ref.current === null) {
      ref.current = init();
    }
    return ref.current;
  }
  const isKeyframesTarget = (v2) => {
    return Array.isArray(v2);
  };
  const isCustomValue = (v2) => {
    return Boolean(v2 && typeof v2 === "object" && v2.mix && v2.toValue);
  };
  const resolveFinalValueInKeyframes = (v2) => {
    return isKeyframesTarget(v2) ? v2[v2.length - 1] || 0 : v2;
  };
  function resolveMotionValue(value) {
    const unwrappedValue = isMotionValue(value) ? value.get() : value;
    return isCustomValue(unwrappedValue) ? unwrappedValue.toValue() : unwrappedValue;
  }
  function makeState({ scrapeMotionValuesFromProps: scrapeMotionValuesFromProps2, createRenderState, onMount }, props, context, presenceContext) {
    const state2 = {
      latestValues: makeLatestValues(props, context, presenceContext, scrapeMotionValuesFromProps2),
      renderState: createRenderState()
    };
    if (onMount) {
      state2.mount = (instance) => onMount(props, instance, state2);
    }
    return state2;
  }
  const makeUseVisualState = (config2) => (props, isStatic) => {
    const context = reactExports.useContext(MotionContext);
    const presenceContext = reactExports.useContext(PresenceContext);
    const make = () => makeState(config2, props, context, presenceContext);
    return isStatic ? make() : useConstant(make);
  };
  function makeLatestValues(props, context, presenceContext, scrapeMotionValues) {
    const values = {};
    const motionValues = scrapeMotionValues(props, {});
    for (const key in motionValues) {
      values[key] = resolveMotionValue(motionValues[key]);
    }
    let { initial, animate } = props;
    const isControllingVariants$1 = isControllingVariants(props);
    const isVariantNode$1 = isVariantNode(props);
    if (context && isVariantNode$1 && !isControllingVariants$1 && props.inherit !== false) {
      if (initial === void 0)
        initial = context.initial;
      if (animate === void 0)
        animate = context.animate;
    }
    let isInitialAnimationBlocked = presenceContext ? presenceContext.initial === false : false;
    isInitialAnimationBlocked = isInitialAnimationBlocked || initial === false;
    const variantToSet = isInitialAnimationBlocked ? animate : initial;
    if (variantToSet && typeof variantToSet !== "boolean" && !isAnimationControls(variantToSet)) {
      const list2 = Array.isArray(variantToSet) ? variantToSet : [variantToSet];
      list2.forEach((definition) => {
        const resolved = resolveVariantFromProps(props, definition);
        if (!resolved)
          return;
        const { transitionEnd, transition: transition2, ...target } = resolved;
        for (const key in target) {
          let valueTarget = target[key];
          if (Array.isArray(valueTarget)) {
            const index = isInitialAnimationBlocked ? valueTarget.length - 1 : 0;
            valueTarget = valueTarget[index];
          }
          if (valueTarget !== null) {
            values[key] = valueTarget;
          }
        }
        for (const key in transitionEnd)
          values[key] = transitionEnd[key];
      });
    }
    return values;
  }
  const noop = (any) => any;
  const { schedule: frame, cancel: cancelFrame, state: frameData, steps } = createRenderBatcher(typeof requestAnimationFrame !== "undefined" ? requestAnimationFrame : noop, true);
  const svgMotionConfig = {
    useVisualState: makeUseVisualState({
      scrapeMotionValuesFromProps,
      createRenderState: createSvgRenderState,
      onMount: (props, instance, { renderState, latestValues }) => {
        frame.read(() => {
          try {
            renderState.dimensions = typeof instance.getBBox === "function" ? instance.getBBox() : instance.getBoundingClientRect();
          } catch (e2) {
            renderState.dimensions = {
              x: 0,
              y: 0,
              width: 0,
              height: 0
            };
          }
        });
        frame.render(() => {
          buildSVGAttrs(renderState, latestValues, { enableHardwareAcceleration: false }, isSVGTag(instance.tagName), props.transformTemplate);
          renderSVG(instance, renderState);
        });
      }
    })
  };
  const htmlMotionConfig = {
    useVisualState: makeUseVisualState({
      scrapeMotionValuesFromProps: scrapeMotionValuesFromProps$1,
      createRenderState: createHtmlRenderState
    })
  };
  function createDomMotionConfig(Component, { forwardMotionProps = false }, preloadedFeatures2, createVisualElement) {
    const baseConfig = isSVGComponent(Component) ? svgMotionConfig : htmlMotionConfig;
    return {
      ...baseConfig,
      preloadedFeatures: preloadedFeatures2,
      useRender: createUseRender(forwardMotionProps),
      createVisualElement,
      Component
    };
  }
  function addDomEvent(target, eventName, handler, options = { passive: true }) {
    target.addEventListener(eventName, handler, options);
    return () => target.removeEventListener(eventName, handler);
  }
  const isPrimaryPointer = (event) => {
    if (event.pointerType === "mouse") {
      return typeof event.button !== "number" || event.button <= 0;
    } else {
      return event.isPrimary !== false;
    }
  };
  function extractEventInfo(event, pointType = "page") {
    return {
      point: {
        x: event[`${pointType}X`],
        y: event[`${pointType}Y`]
      }
    };
  }
  const addPointerInfo = (handler) => {
    return (event) => isPrimaryPointer(event) && handler(event, extractEventInfo(event));
  };
  function addPointerEvent(target, eventName, handler, options) {
    return addDomEvent(target, eventName, addPointerInfo(handler), options);
  }
  const combineFunctions = (a, b2) => (v2) => b2(a(v2));
  const pipe = (...transformers) => transformers.reduce(combineFunctions);
  function createLock(name) {
    let lock = null;
    return () => {
      const openLock = () => {
        lock = null;
      };
      if (lock === null) {
        lock = name;
        return openLock;
      }
      return false;
    };
  }
  const globalHorizontalLock = createLock("dragHorizontal");
  const globalVerticalLock = createLock("dragVertical");
  function getGlobalLock(drag2) {
    let lock = false;
    if (drag2 === "y") {
      lock = globalVerticalLock();
    } else if (drag2 === "x") {
      lock = globalHorizontalLock();
    } else {
      const openHorizontal = globalHorizontalLock();
      const openVertical = globalVerticalLock();
      if (openHorizontal && openVertical) {
        lock = () => {
          openHorizontal();
          openVertical();
        };
      } else {
        if (openHorizontal)
          openHorizontal();
        if (openVertical)
          openVertical();
      }
    }
    return lock;
  }
  function isDragActive() {
    const openGestureLock = getGlobalLock(true);
    if (!openGestureLock)
      return true;
    openGestureLock();
    return false;
  }
  class Feature {
    constructor(node2) {
      this.isMounted = false;
      this.node = node2;
    }
    update() {
    }
  }
  function addHoverEvent(node2, isActive) {
    const eventName = isActive ? "pointerenter" : "pointerleave";
    const callbackName = isActive ? "onHoverStart" : "onHoverEnd";
    const handleEvent = (event, info) => {
      if (event.pointerType === "touch" || isDragActive())
        return;
      const props = node2.getProps();
      if (node2.animationState && props.whileHover) {
        node2.animationState.setActive("whileHover", isActive);
      }
      const callback = props[callbackName];
      if (callback) {
        frame.postRender(() => callback(event, info));
      }
    };
    return addPointerEvent(node2.current, eventName, handleEvent, {
      passive: !node2.getProps()[callbackName]
    });
  }
  class HoverGesture extends Feature {
    mount() {
      this.unmount = pipe(addHoverEvent(this.node, true), addHoverEvent(this.node, false));
    }
    unmount() {
    }
  }
  class FocusGesture extends Feature {
    constructor() {
      super(...arguments);
      this.isActive = false;
    }
    onFocus() {
      let isFocusVisible = false;
      try {
        isFocusVisible = this.node.current.matches(":focus-visible");
      } catch (e2) {
        isFocusVisible = true;
      }
      if (!isFocusVisible || !this.node.animationState)
        return;
      this.node.animationState.setActive("whileFocus", true);
      this.isActive = true;
    }
    onBlur() {
      if (!this.isActive || !this.node.animationState)
        return;
      this.node.animationState.setActive("whileFocus", false);
      this.isActive = false;
    }
    mount() {
      this.unmount = pipe(addDomEvent(this.node.current, "focus", () => this.onFocus()), addDomEvent(this.node.current, "blur", () => this.onBlur()));
    }
    unmount() {
    }
  }
  const isNodeOrChild = (parent, child) => {
    if (!child) {
      return false;
    } else if (parent === child) {
      return true;
    } else {
      return isNodeOrChild(parent, child.parentElement);
    }
  };
  function fireSyntheticPointerEvent(name, handler) {
    if (!handler)
      return;
    const syntheticPointerEvent = new PointerEvent("pointer" + name);
    handler(syntheticPointerEvent, extractEventInfo(syntheticPointerEvent));
  }
  class PressGesture extends Feature {
    constructor() {
      super(...arguments);
      this.removeStartListeners = noop;
      this.removeEndListeners = noop;
      this.removeAccessibleListeners = noop;
      this.startPointerPress = (startEvent, startInfo) => {
        if (this.isPressing)
          return;
        this.removeEndListeners();
        const props = this.node.getProps();
        const endPointerPress = (endEvent, endInfo) => {
          if (!this.checkPressEnd())
            return;
          const { onTap, onTapCancel, globalTapTarget } = this.node.getProps();
          const handler = !globalTapTarget && !isNodeOrChild(this.node.current, endEvent.target) ? onTapCancel : onTap;
          if (handler) {
            frame.update(() => handler(endEvent, endInfo));
          }
        };
        const removePointerUpListener = addPointerEvent(window, "pointerup", endPointerPress, {
          passive: !(props.onTap || props["onPointerUp"])
        });
        const removePointerCancelListener = addPointerEvent(window, "pointercancel", (cancelEvent, cancelInfo) => this.cancelPress(cancelEvent, cancelInfo), {
          passive: !(props.onTapCancel || props["onPointerCancel"])
        });
        this.removeEndListeners = pipe(removePointerUpListener, removePointerCancelListener);
        this.startPress(startEvent, startInfo);
      };
      this.startAccessiblePress = () => {
        const handleKeydown = (keydownEvent) => {
          if (keydownEvent.key !== "Enter" || this.isPressing)
            return;
          const handleKeyup = (keyupEvent) => {
            if (keyupEvent.key !== "Enter" || !this.checkPressEnd())
              return;
            fireSyntheticPointerEvent("up", (event, info) => {
              const { onTap } = this.node.getProps();
              if (onTap) {
                frame.postRender(() => onTap(event, info));
              }
            });
          };
          this.removeEndListeners();
          this.removeEndListeners = addDomEvent(this.node.current, "keyup", handleKeyup);
          fireSyntheticPointerEvent("down", (event, info) => {
            this.startPress(event, info);
          });
        };
        const removeKeydownListener = addDomEvent(this.node.current, "keydown", handleKeydown);
        const handleBlur = () => {
          if (!this.isPressing)
            return;
          fireSyntheticPointerEvent("cancel", (cancelEvent, cancelInfo) => this.cancelPress(cancelEvent, cancelInfo));
        };
        const removeBlurListener = addDomEvent(this.node.current, "blur", handleBlur);
        this.removeAccessibleListeners = pipe(removeKeydownListener, removeBlurListener);
      };
    }
    startPress(event, info) {
      this.isPressing = true;
      const { onTapStart, whileTap } = this.node.getProps();
      if (whileTap && this.node.animationState) {
        this.node.animationState.setActive("whileTap", true);
      }
      if (onTapStart) {
        frame.postRender(() => onTapStart(event, info));
      }
    }
    checkPressEnd() {
      this.removeEndListeners();
      this.isPressing = false;
      const props = this.node.getProps();
      if (props.whileTap && this.node.animationState) {
        this.node.animationState.setActive("whileTap", false);
      }
      return !isDragActive();
    }
    cancelPress(event, info) {
      if (!this.checkPressEnd())
        return;
      const { onTapCancel } = this.node.getProps();
      if (onTapCancel) {
        frame.postRender(() => onTapCancel(event, info));
      }
    }
    mount() {
      const props = this.node.getProps();
      const removePointerListener = addPointerEvent(props.globalTapTarget ? window : this.node.current, "pointerdown", this.startPointerPress, {
        passive: !(props.onTapStart || props["onPointerStart"])
      });
      const removeFocusListener = addDomEvent(this.node.current, "focus", this.startAccessiblePress);
      this.removeStartListeners = pipe(removePointerListener, removeFocusListener);
    }
    unmount() {
      this.removeStartListeners();
      this.removeEndListeners();
      this.removeAccessibleListeners();
    }
  }
  const observerCallbacks = /* @__PURE__ */ new WeakMap();
  const observers = /* @__PURE__ */ new WeakMap();
  const fireObserverCallback = (entry) => {
    const callback = observerCallbacks.get(entry.target);
    callback && callback(entry);
  };
  const fireAllObserverCallbacks = (entries) => {
    entries.forEach(fireObserverCallback);
  };
  function initIntersectionObserver({ root, ...options }) {
    const lookupRoot = root || document;
    if (!observers.has(lookupRoot)) {
      observers.set(lookupRoot, {});
    }
    const rootObservers = observers.get(lookupRoot);
    const key = JSON.stringify(options);
    if (!rootObservers[key]) {
      rootObservers[key] = new IntersectionObserver(fireAllObserverCallbacks, { root, ...options });
    }
    return rootObservers[key];
  }
  function observeIntersection(element, options, callback) {
    const rootInteresectionObserver = initIntersectionObserver(options);
    observerCallbacks.set(element, callback);
    rootInteresectionObserver.observe(element);
    return () => {
      observerCallbacks.delete(element);
      rootInteresectionObserver.unobserve(element);
    };
  }
  const thresholdNames = {
    some: 0,
    all: 1
  };
  class InViewFeature extends Feature {
    constructor() {
      super(...arguments);
      this.hasEnteredView = false;
      this.isInView = false;
    }
    startObserver() {
      this.unmount();
      const { viewport = {} } = this.node.getProps();
      const { root, margin: rootMargin, amount = "some", once } = viewport;
      const options = {
        root: root ? root.current : void 0,
        rootMargin,
        threshold: typeof amount === "number" ? amount : thresholdNames[amount]
      };
      const onIntersectionUpdate = (entry) => {
        const { isIntersecting } = entry;
        if (this.isInView === isIntersecting)
          return;
        this.isInView = isIntersecting;
        if (once && !isIntersecting && this.hasEnteredView) {
          return;
        } else if (isIntersecting) {
          this.hasEnteredView = true;
        }
        if (this.node.animationState) {
          this.node.animationState.setActive("whileInView", isIntersecting);
        }
        const { onViewportEnter, onViewportLeave } = this.node.getProps();
        const callback = isIntersecting ? onViewportEnter : onViewportLeave;
        callback && callback(entry);
      };
      return observeIntersection(this.node.current, options, onIntersectionUpdate);
    }
    mount() {
      this.startObserver();
    }
    update() {
      if (typeof IntersectionObserver === "undefined")
        return;
      const { props, prevProps } = this.node;
      const hasOptionsChanged = ["amount", "margin", "root"].some(hasViewportOptionChanged(props, prevProps));
      if (hasOptionsChanged) {
        this.startObserver();
      }
    }
    unmount() {
    }
  }
  function hasViewportOptionChanged({ viewport = {} }, { viewport: prevViewport = {} } = {}) {
    return (name) => viewport[name] !== prevViewport[name];
  }
  const gestureAnimations = {
    inView: {
      Feature: InViewFeature
    },
    tap: {
      Feature: PressGesture
    },
    focus: {
      Feature: FocusGesture
    },
    hover: {
      Feature: HoverGesture
    }
  };
  function shallowCompare(next2, prev2) {
    if (!Array.isArray(prev2))
      return false;
    const prevLength = prev2.length;
    if (prevLength !== next2.length)
      return false;
    for (let i = 0; i < prevLength; i++) {
      if (prev2[i] !== next2[i])
        return false;
    }
    return true;
  }
  function getCurrent(visualElement) {
    const current = {};
    visualElement.values.forEach((value, key) => current[key] = value.get());
    return current;
  }
  function getVelocity$1(visualElement) {
    const velocity = {};
    visualElement.values.forEach((value, key) => velocity[key] = value.getVelocity());
    return velocity;
  }
  function resolveVariant(visualElement, definition, custom) {
    const props = visualElement.getProps();
    return resolveVariantFromProps(props, definition, custom !== void 0 ? custom : props.custom, getCurrent(visualElement), getVelocity$1(visualElement));
  }
  const secondsToMilliseconds = (seconds) => seconds * 1e3;
  const millisecondsToSeconds = (milliseconds) => milliseconds / 1e3;
  const underDampedSpring = {
    type: "spring",
    stiffness: 500,
    damping: 25,
    restSpeed: 10
  };
  const criticallyDampedSpring = (target) => ({
    type: "spring",
    stiffness: 550,
    damping: target === 0 ? 2 * Math.sqrt(550) : 30,
    restSpeed: 10
  });
  const keyframesTransition = {
    type: "keyframes",
    duration: 0.8
  };
  const ease = {
    type: "keyframes",
    ease: [0.25, 0.1, 0.35, 1],
    duration: 0.3
  };
  const getDefaultTransition = (valueKey, { keyframes: keyframes2 }) => {
    if (keyframes2.length > 2) {
      return keyframesTransition;
    } else if (transformProps.has(valueKey)) {
      return valueKey.startsWith("scale") ? criticallyDampedSpring(keyframes2[1]) : underDampedSpring;
    }
    return ease;
  };
  function isTransitionDefined({ when, delay: _delay, delayChildren, staggerChildren, staggerDirection, repeat, repeatType, repeatDelay, from: from2, elapsed, ...transition2 }) {
    return !!Object.keys(transition2).length;
  }
  function getValueTransition(transition2, key) {
    return transition2[key] || transition2["default"] || transition2;
  }
  const isNotNull = (value) => value !== null;
  function getFinalKeyframe(keyframes2, { repeat, repeatType = "loop" }, finalKeyframe) {
    const resolvedKeyframes = keyframes2.filter(isNotNull);
    const index = repeat && repeatType !== "loop" && repeat % 2 === 1 ? 0 : resolvedKeyframes.length - 1;
    return !index || finalKeyframe === void 0 ? resolvedKeyframes[index] : finalKeyframe;
  }
  let now;
  function clearTime() {
    now = void 0;
  }
  const time = {
    now: () => {
      if (now === void 0) {
        time.set(frameData.isProcessing || MotionGlobalConfig.useManualTiming ? frameData.timestamp : performance.now());
      }
      return now;
    },
    set: (newTime) => {
      now = newTime;
      queueMicrotask(clearTime);
    }
  };
  const isZeroValueString = (v2) => /^0[^.\s]+$/u.test(v2);
  function isNone(value) {
    if (typeof value === "number") {
      return value === 0;
    } else if (value !== null) {
      return value === "none" || value === "0" || isZeroValueString(value);
    } else {
      return true;
    }
  }
  let invariant = noop;
  const isNumericalString = (v2) => /^-?(?:\d+(?:\.\d+)?|\.\d+)$/u.test(v2);
  const splitCSSVariableRegex = (
    // eslint-disable-next-line redos-detector/no-unsafe-regex -- false positive, as it can match a lot of words
    /^var\(--(?:([\w-]+)|([\w-]+), ?([a-zA-Z\d ()%#.,-]+))\)/u
  );
  function parseCSSVariable(current) {
    const match2 = splitCSSVariableRegex.exec(current);
    if (!match2)
      return [,];
    const [, token1, token2, fallback] = match2;
    return [`--${token1 !== null && token1 !== void 0 ? token1 : token2}`, fallback];
  }
  function getVariableValue(current, element, depth = 1) {
    const [token2, fallback] = parseCSSVariable(current);
    if (!token2)
      return;
    const resolved = window.getComputedStyle(element).getPropertyValue(token2);
    if (resolved) {
      const trimmed = resolved.trim();
      return isNumericalString(trimmed) ? parseFloat(trimmed) : trimmed;
    }
    return isCSSVariableToken(fallback) ? getVariableValue(fallback, element, depth + 1) : fallback;
  }
  const positionalKeys = /* @__PURE__ */ new Set([
    "width",
    "height",
    "top",
    "left",
    "right",
    "bottom",
    "x",
    "y",
    "translateX",
    "translateY"
  ]);
  const isNumOrPxType = (v2) => v2 === number || v2 === px;
  const getPosFromMatrix = (matrix, pos) => parseFloat(matrix.split(", ")[pos]);
  const getTranslateFromMatrix = (pos2, pos3) => (_bbox, { transform: transform2 }) => {
    if (transform2 === "none" || !transform2)
      return 0;
    const matrix3d = transform2.match(/^matrix3d\((.+)\)$/u);
    if (matrix3d) {
      return getPosFromMatrix(matrix3d[1], pos3);
    } else {
      const matrix = transform2.match(/^matrix\((.+)\)$/u);
      if (matrix) {
        return getPosFromMatrix(matrix[1], pos2);
      } else {
        return 0;
      }
    }
  };
  const transformKeys = /* @__PURE__ */ new Set(["x", "y", "z"]);
  const nonTranslationalTransformKeys = transformPropOrder.filter((key) => !transformKeys.has(key));
  function removeNonTranslationalTransform(visualElement) {
    const removedTransforms = [];
    nonTranslationalTransformKeys.forEach((key) => {
      const value = visualElement.getValue(key);
      if (value !== void 0) {
        removedTransforms.push([key, value.get()]);
        value.set(key.startsWith("scale") ? 1 : 0);
      }
    });
    return removedTransforms;
  }
  const positionalValues = {
    // Dimensions
    width: ({ x: x2 }, { paddingLeft = "0", paddingRight = "0" }) => x2.max - x2.min - parseFloat(paddingLeft) - parseFloat(paddingRight),
    height: ({ y: y2 }, { paddingTop = "0", paddingBottom = "0" }) => y2.max - y2.min - parseFloat(paddingTop) - parseFloat(paddingBottom),
    top: (_bbox, { top }) => parseFloat(top),
    left: (_bbox, { left }) => parseFloat(left),
    bottom: ({ y: y2 }, { top }) => parseFloat(top) + (y2.max - y2.min),
    right: ({ x: x2 }, { left }) => parseFloat(left) + (x2.max - x2.min),
    // Transform
    x: getTranslateFromMatrix(4, 13),
    y: getTranslateFromMatrix(5, 14)
  };
  positionalValues.translateX = positionalValues.x;
  positionalValues.translateY = positionalValues.y;
  const testValueType = (v2) => (type) => type.test(v2);
  const auto = {
    test: (v2) => v2 === "auto",
    parse: (v2) => v2
  };
  const dimensionValueTypes = [number, px, percent, degrees, vw, vh, auto];
  const findDimensionValueType = (v2) => dimensionValueTypes.find(testValueType(v2));
  const toResolve = /* @__PURE__ */ new Set();
  let isScheduled = false;
  let anyNeedsMeasurement = false;
  function measureAllKeyframes() {
    if (anyNeedsMeasurement) {
      const resolversToMeasure = Array.from(toResolve).filter((resolver) => resolver.needsMeasurement);
      const elementsToMeasure = new Set(resolversToMeasure.map((resolver) => resolver.element));
      const transformsToRestore = /* @__PURE__ */ new Map();
      elementsToMeasure.forEach((element) => {
        const removedTransforms = removeNonTranslationalTransform(element);
        if (!removedTransforms.length)
          return;
        transformsToRestore.set(element, removedTransforms);
        element.render();
      });
      resolversToMeasure.forEach((resolver) => resolver.measureInitialState());
      elementsToMeasure.forEach((element) => {
        element.render();
        const restore = transformsToRestore.get(element);
        if (restore) {
          restore.forEach(([key, value]) => {
            var _a4;
            (_a4 = element.getValue(key)) === null || _a4 === void 0 ? void 0 : _a4.set(value);
          });
        }
      });
      resolversToMeasure.forEach((resolver) => resolver.measureEndState());
      resolversToMeasure.forEach((resolver) => {
        if (resolver.suspendedScrollY !== void 0) {
          window.scrollTo(0, resolver.suspendedScrollY);
        }
      });
    }
    anyNeedsMeasurement = false;
    isScheduled = false;
    toResolve.forEach((resolver) => resolver.complete());
    toResolve.clear();
  }
  function readAllKeyframes() {
    toResolve.forEach((resolver) => {
      resolver.readKeyframes();
      if (resolver.needsMeasurement) {
        anyNeedsMeasurement = true;
      }
    });
  }
  function flushKeyframeResolvers() {
    readAllKeyframes();
    measureAllKeyframes();
  }
  class KeyframeResolver {
    constructor(unresolvedKeyframes, onComplete, name, motionValue2, element, isAsync = false) {
      this.isComplete = false;
      this.isAsync = false;
      this.needsMeasurement = false;
      this.isScheduled = false;
      this.unresolvedKeyframes = [...unresolvedKeyframes];
      this.onComplete = onComplete;
      this.name = name;
      this.motionValue = motionValue2;
      this.element = element;
      this.isAsync = isAsync;
    }
    scheduleResolve() {
      this.isScheduled = true;
      if (this.isAsync) {
        toResolve.add(this);
        if (!isScheduled) {
          isScheduled = true;
          frame.read(readAllKeyframes);
          frame.resolveKeyframes(measureAllKeyframes);
        }
      } else {
        this.readKeyframes();
        this.complete();
      }
    }
    readKeyframes() {
      const { unresolvedKeyframes, name, element, motionValue: motionValue2 } = this;
      for (let i = 0; i < unresolvedKeyframes.length; i++) {
        if (unresolvedKeyframes[i] === null) {
          if (i === 0) {
            const currentValue = motionValue2 === null || motionValue2 === void 0 ? void 0 : motionValue2.get();
            const finalKeyframe = unresolvedKeyframes[unresolvedKeyframes.length - 1];
            if (currentValue !== void 0) {
              unresolvedKeyframes[0] = currentValue;
            } else if (element && name) {
              const valueAsRead = element.readValue(name, finalKeyframe);
              if (valueAsRead !== void 0 && valueAsRead !== null) {
                unresolvedKeyframes[0] = valueAsRead;
              }
            }
            if (unresolvedKeyframes[0] === void 0) {
              unresolvedKeyframes[0] = finalKeyframe;
            }
            if (motionValue2 && currentValue === void 0) {
              motionValue2.set(unresolvedKeyframes[0]);
            }
          } else {
            unresolvedKeyframes[i] = unresolvedKeyframes[i - 1];
          }
        }
      }
    }
    setFinalKeyframe() {
    }
    measureInitialState() {
    }
    renderEndStyles() {
    }
    measureEndState() {
    }
    complete() {
      this.isComplete = true;
      this.onComplete(this.unresolvedKeyframes, this.finalKeyframe);
      toResolve.delete(this);
    }
    cancel() {
      if (!this.isComplete) {
        this.isScheduled = false;
        toResolve.delete(this);
      }
    }
    resume() {
      if (!this.isComplete)
        this.scheduleResolve();
    }
  }
  const isColorString = (type, testProp) => (v2) => {
    return Boolean(isString(v2) && singleColorRegex.test(v2) && v2.startsWith(type) || testProp && Object.prototype.hasOwnProperty.call(v2, testProp));
  };
  const splitColor = (aName, bName, cName) => (v2) => {
    if (!isString(v2))
      return v2;
    const [a, b2, c2, alpha2] = v2.match(floatRegex);
    return {
      [aName]: parseFloat(a),
      [bName]: parseFloat(b2),
      [cName]: parseFloat(c2),
      alpha: alpha2 !== void 0 ? parseFloat(alpha2) : 1
    };
  };
  const clampRgbUnit = (v2) => clamp(0, 255, v2);
  const rgbUnit = {
    ...number,
    transform: (v2) => Math.round(clampRgbUnit(v2))
  };
  const rgba = {
    test: isColorString("rgb", "red"),
    parse: splitColor("red", "green", "blue"),
    transform: ({ red, green, blue, alpha: alpha$1 = 1 }) => "rgba(" + rgbUnit.transform(red) + ", " + rgbUnit.transform(green) + ", " + rgbUnit.transform(blue) + ", " + sanitize(alpha.transform(alpha$1)) + ")"
  };
  function parseHex(v2) {
    let r2 = "";
    let g2 = "";
    let b2 = "";
    let a = "";
    if (v2.length > 5) {
      r2 = v2.substring(1, 3);
      g2 = v2.substring(3, 5);
      b2 = v2.substring(5, 7);
      a = v2.substring(7, 9);
    } else {
      r2 = v2.substring(1, 2);
      g2 = v2.substring(2, 3);
      b2 = v2.substring(3, 4);
      a = v2.substring(4, 5);
      r2 += r2;
      g2 += g2;
      b2 += b2;
      a += a;
    }
    return {
      red: parseInt(r2, 16),
      green: parseInt(g2, 16),
      blue: parseInt(b2, 16),
      alpha: a ? parseInt(a, 16) / 255 : 1
    };
  }
  const hex = {
    test: isColorString("#"),
    parse: parseHex,
    transform: rgba.transform
  };
  const hsla = {
    test: isColorString("hsl", "hue"),
    parse: splitColor("hue", "saturation", "lightness"),
    transform: ({ hue, saturation, lightness, alpha: alpha$1 = 1 }) => {
      return "hsla(" + Math.round(hue) + ", " + percent.transform(sanitize(saturation)) + ", " + percent.transform(sanitize(lightness)) + ", " + sanitize(alpha.transform(alpha$1)) + ")";
    }
  };
  const color = {
    test: (v2) => rgba.test(v2) || hex.test(v2) || hsla.test(v2),
    parse: (v2) => {
      if (rgba.test(v2)) {
        return rgba.parse(v2);
      } else if (hsla.test(v2)) {
        return hsla.parse(v2);
      } else {
        return hex.parse(v2);
      }
    },
    transform: (v2) => {
      return isString(v2) ? v2 : v2.hasOwnProperty("red") ? rgba.transform(v2) : hsla.transform(v2);
    }
  };
  function test(v2) {
    var _a4, _b3;
    return isNaN(v2) && isString(v2) && (((_a4 = v2.match(floatRegex)) === null || _a4 === void 0 ? void 0 : _a4.length) || 0) + (((_b3 = v2.match(colorRegex)) === null || _b3 === void 0 ? void 0 : _b3.length) || 0) > 0;
  }
  const NUMBER_TOKEN = "number";
  const COLOR_TOKEN = "color";
  const VAR_TOKEN = "var";
  const VAR_FUNCTION_TOKEN = "var(";
  const SPLIT_TOKEN = "${}";
  const complexRegex = /var\s*\(\s*--(?:[\w-]+\s*|[\w-]+\s*,(?:\s*[^)(\s]|\s*\((?:[^)(]|\([^)(]*\))*\))+\s*)\)|#[\da-f]{3,8}|(?:rgb|hsl)a?\((?:-?[\d.]+%?[,\s]+){2}-?[\d.]+%?\s*(?:[,/]\s*)?(?:\b\d+(?:\.\d+)?|\.\d+)?%?\)|-?(?:\d+(?:\.\d+)?|\.\d+)/giu;
  function analyseComplexValue(value) {
    const originalValue = value.toString();
    const values = [];
    const indexes = {
      color: [],
      number: [],
      var: []
    };
    const types = [];
    let i = 0;
    const tokenised = originalValue.replace(complexRegex, (parsedValue) => {
      if (color.test(parsedValue)) {
        indexes.color.push(i);
        types.push(COLOR_TOKEN);
        values.push(color.parse(parsedValue));
      } else if (parsedValue.startsWith(VAR_FUNCTION_TOKEN)) {
        indexes.var.push(i);
        types.push(VAR_TOKEN);
        values.push(parsedValue);
      } else {
        indexes.number.push(i);
        types.push(NUMBER_TOKEN);
        values.push(parseFloat(parsedValue));
      }
      ++i;
      return SPLIT_TOKEN;
    });
    const split = tokenised.split(SPLIT_TOKEN);
    return { values, split, indexes, types };
  }
  function parseComplexValue(v2) {
    return analyseComplexValue(v2).values;
  }
  function createTransformer(source) {
    const { split, types } = analyseComplexValue(source);
    const numSections = split.length;
    return (v2) => {
      let output = "";
      for (let i = 0; i < numSections; i++) {
        output += split[i];
        if (v2[i] !== void 0) {
          const type = types[i];
          if (type === NUMBER_TOKEN) {
            output += sanitize(v2[i]);
          } else if (type === COLOR_TOKEN) {
            output += color.transform(v2[i]);
          } else {
            output += v2[i];
          }
        }
      }
      return output;
    };
  }
  const convertNumbersToZero = (v2) => typeof v2 === "number" ? 0 : v2;
  function getAnimatableNone$1(v2) {
    const parsed = parseComplexValue(v2);
    const transformer = createTransformer(v2);
    return transformer(parsed.map(convertNumbersToZero));
  }
  const complex = {
    test,
    parse: parseComplexValue,
    createTransformer,
    getAnimatableNone: getAnimatableNone$1
  };
  const maxDefaults = /* @__PURE__ */ new Set(["brightness", "contrast", "saturate", "opacity"]);
  function applyDefaultFilter(v2) {
    const [name, value] = v2.slice(0, -1).split("(");
    if (name === "drop-shadow")
      return v2;
    const [number2] = value.match(floatRegex) || [];
    if (!number2)
      return v2;
    const unit = value.replace(number2, "");
    let defaultValue = maxDefaults.has(name) ? 1 : 0;
    if (number2 !== value)
      defaultValue *= 100;
    return name + "(" + defaultValue + unit + ")";
  }
  const functionRegex = /\b([a-z-]*)\(.*?\)/gu;
  const filter$1 = {
    ...complex,
    getAnimatableNone: (v2) => {
      const functions = v2.match(functionRegex);
      return functions ? functions.map(applyDefaultFilter).join(" ") : v2;
    }
  };
  const defaultValueTypes = {
    ...numberValueTypes,
    // Color props
    color,
    backgroundColor: color,
    outlineColor: color,
    fill: color,
    stroke: color,
    // Border props
    borderColor: color,
    borderTopColor: color,
    borderRightColor: color,
    borderBottomColor: color,
    borderLeftColor: color,
    filter: filter$1,
    WebkitFilter: filter$1
  };
  const getDefaultValueType = (key) => defaultValueTypes[key];
  function getAnimatableNone(key, value) {
    let defaultValueType = getDefaultValueType(key);
    if (defaultValueType !== filter$1)
      defaultValueType = complex;
    return defaultValueType.getAnimatableNone ? defaultValueType.getAnimatableNone(value) : void 0;
  }
  const invalidTemplates = /* @__PURE__ */ new Set(["auto", "none", "0"]);
  function makeNoneKeyframesAnimatable(unresolvedKeyframes, noneKeyframeIndexes, name) {
    let i = 0;
    let animatableTemplate = void 0;
    while (i < unresolvedKeyframes.length && !animatableTemplate) {
      const keyframe = unresolvedKeyframes[i];
      if (typeof keyframe === "string" && !invalidTemplates.has(keyframe) && analyseComplexValue(keyframe).values.length) {
        animatableTemplate = unresolvedKeyframes[i];
      }
      i++;
    }
    if (animatableTemplate && name) {
      for (const noneIndex of noneKeyframeIndexes) {
        unresolvedKeyframes[noneIndex] = getAnimatableNone(name, animatableTemplate);
      }
    }
  }
  class DOMKeyframesResolver extends KeyframeResolver {
    constructor(unresolvedKeyframes, onComplete, name, motionValue2) {
      super(unresolvedKeyframes, onComplete, name, motionValue2, motionValue2 === null || motionValue2 === void 0 ? void 0 : motionValue2.owner, true);
    }
    readKeyframes() {
      const { unresolvedKeyframes, element, name } = this;
      if (!element.current)
        return;
      super.readKeyframes();
      for (let i = 0; i < unresolvedKeyframes.length; i++) {
        const keyframe = unresolvedKeyframes[i];
        if (typeof keyframe === "string" && isCSSVariableToken(keyframe)) {
          const resolved = getVariableValue(keyframe, element.current);
          if (resolved !== void 0) {
            unresolvedKeyframes[i] = resolved;
          }
          if (i === unresolvedKeyframes.length - 1) {
            this.finalKeyframe = keyframe;
          }
        }
      }
      this.resolveNoneKeyframes();
      if (!positionalKeys.has(name) || unresolvedKeyframes.length !== 2) {
        return;
      }
      const [origin, target] = unresolvedKeyframes;
      const originType = findDimensionValueType(origin);
      const targetType = findDimensionValueType(target);
      if (originType === targetType)
        return;
      if (isNumOrPxType(originType) && isNumOrPxType(targetType)) {
        for (let i = 0; i < unresolvedKeyframes.length; i++) {
          const value = unresolvedKeyframes[i];
          if (typeof value === "string") {
            unresolvedKeyframes[i] = parseFloat(value);
          }
        }
      } else {
        this.needsMeasurement = true;
      }
    }
    resolveNoneKeyframes() {
      const { unresolvedKeyframes, name } = this;
      const noneKeyframeIndexes = [];
      for (let i = 0; i < unresolvedKeyframes.length; i++) {
        if (isNone(unresolvedKeyframes[i])) {
          noneKeyframeIndexes.push(i);
        }
      }
      if (noneKeyframeIndexes.length) {
        makeNoneKeyframesAnimatable(unresolvedKeyframes, noneKeyframeIndexes, name);
      }
    }
    measureInitialState() {
      const { element, unresolvedKeyframes, name } = this;
      if (!element.current)
        return;
      if (name === "height") {
        this.suspendedScrollY = window.pageYOffset;
      }
      this.measuredOrigin = positionalValues[name](element.measureViewportBox(), window.getComputedStyle(element.current));
      unresolvedKeyframes[0] = this.measuredOrigin;
      const measureKeyframe = unresolvedKeyframes[unresolvedKeyframes.length - 1];
      if (measureKeyframe !== void 0) {
        element.getValue(name, measureKeyframe).jump(measureKeyframe, false);
      }
    }
    measureEndState() {
      var _a4;
      const { element, name, unresolvedKeyframes } = this;
      if (!element.current)
        return;
      const value = element.getValue(name);
      value && value.jump(this.measuredOrigin, false);
      const finalKeyframeIndex = unresolvedKeyframes.length - 1;
      const finalKeyframe = unresolvedKeyframes[finalKeyframeIndex];
      unresolvedKeyframes[finalKeyframeIndex] = positionalValues[name](element.measureViewportBox(), window.getComputedStyle(element.current));
      if (finalKeyframe !== null && this.finalKeyframe === void 0) {
        this.finalKeyframe = finalKeyframe;
      }
      if ((_a4 = this.removedTransforms) === null || _a4 === void 0 ? void 0 : _a4.length) {
        this.removedTransforms.forEach(([unsetTransformName, unsetTransformValue]) => {
          element.getValue(unsetTransformName).set(unsetTransformValue);
        });
      }
      this.resolveNoneKeyframes();
    }
  }
  function memo(callback) {
    let result;
    return () => {
      if (result === void 0)
        result = callback();
      return result;
    };
  }
  const isAnimatable = (value, name) => {
    if (name === "zIndex")
      return false;
    if (typeof value === "number" || Array.isArray(value))
      return true;
    if (typeof value === "string" && // It's animatable if we have a string
    (complex.test(value) || value === "0") && // And it contains numbers and/or colors
    !value.startsWith("url(")) {
      return true;
    }
    return false;
  };
  function hasKeyframesChanged(keyframes2) {
    const current = keyframes2[0];
    if (keyframes2.length === 1)
      return true;
    for (let i = 0; i < keyframes2.length; i++) {
      if (keyframes2[i] !== current)
        return true;
    }
  }
  function canAnimate(keyframes2, name, type, velocity) {
    const originKeyframe = keyframes2[0];
    if (originKeyframe === null)
      return false;
    if (name === "display" || name === "visibility")
      return true;
    const targetKeyframe = keyframes2[keyframes2.length - 1];
    const isOriginAnimatable = isAnimatable(originKeyframe, name);
    const isTargetAnimatable = isAnimatable(targetKeyframe, name);
    if (!isOriginAnimatable || !isTargetAnimatable) {
      return false;
    }
    return hasKeyframesChanged(keyframes2) || type === "spring" && velocity;
  }
  class BaseAnimation {
    constructor({ autoplay = true, delay: delay2 = 0, type = "keyframes", repeat = 0, repeatDelay = 0, repeatType = "loop", ...options }) {
      this.isStopped = false;
      this.hasAttemptedResolve = false;
      this.options = {
        autoplay,
        delay: delay2,
        type,
        repeat,
        repeatDelay,
        repeatType,
        ...options
      };
      this.updateFinishedPromise();
    }
    /**
     * A getter for resolved data. If keyframes are not yet resolved, accessing
     * this.resolved will synchronously flush all pending keyframe resolvers.
     * This is a deoptimisation, but at its worst still batches read/writes.
     */
    get resolved() {
      if (!this._resolved && !this.hasAttemptedResolve) {
        flushKeyframeResolvers();
      }
      return this._resolved;
    }
    /**
     * A method to be called when the keyframes resolver completes. This method
     * will check if its possible to run the animation and, if not, skip it.
     * Otherwise, it will call initPlayback on the implementing class.
     */
    onKeyframesResolved(keyframes2, finalKeyframe) {
      this.hasAttemptedResolve = true;
      const { name, type, velocity, delay: delay2, onComplete, onUpdate, isGenerator } = this.options;
      if (!isGenerator && !canAnimate(keyframes2, name, type, velocity)) {
        if (!delay2) {
          onUpdate === null || onUpdate === void 0 ? void 0 : onUpdate(getFinalKeyframe(keyframes2, this.options, finalKeyframe));
          onComplete === null || onComplete === void 0 ? void 0 : onComplete();
          this.resolveFinishedPromise();
          return;
        } else {
          this.options.duration = 0;
        }
      }
      const resolvedAnimation = this.initPlayback(keyframes2, finalKeyframe);
      if (resolvedAnimation === false)
        return;
      this._resolved = {
        keyframes: keyframes2,
        finalKeyframe,
        ...resolvedAnimation
      };
      this.onPostResolved();
    }
    onPostResolved() {
    }
    /**
     * Allows the returned animation to be awaited or promise-chained. Currently
     * resolves when the animation finishes at all but in a future update could/should
     * reject if its cancels.
     */
    then(resolve, reject) {
      return this.currentFinishedPromise.then(resolve, reject);
    }
    updateFinishedPromise() {
      this.currentFinishedPromise = new Promise((resolve) => {
        this.resolveFinishedPromise = resolve;
      });
    }
  }
  function velocityPerSecond(velocity, frameDuration) {
    return frameDuration ? velocity * (1e3 / frameDuration) : 0;
  }
  const velocitySampleDuration = 5;
  function calcGeneratorVelocity(resolveValue, t2, current) {
    const prevT = Math.max(t2 - velocitySampleDuration, 0);
    return velocityPerSecond(current - resolveValue(prevT), t2 - prevT);
  }
  const safeMin = 1e-3;
  const minDuration = 0.01;
  const maxDuration$1 = 10;
  const minDamping = 0.05;
  const maxDamping = 1;
  function findSpring({ duration = 800, bounce = 0.25, velocity = 0, mass = 1 }) {
    let envelope;
    let derivative;
    let dampingRatio = 1 - bounce;
    dampingRatio = clamp(minDamping, maxDamping, dampingRatio);
    duration = clamp(minDuration, maxDuration$1, millisecondsToSeconds(duration));
    if (dampingRatio < 1) {
      envelope = (undampedFreq2) => {
        const exponentialDecay = undampedFreq2 * dampingRatio;
        const delta = exponentialDecay * duration;
        const a = exponentialDecay - velocity;
        const b2 = calcAngularFreq(undampedFreq2, dampingRatio);
        const c2 = Math.exp(-delta);
        return safeMin - a / b2 * c2;
      };
      derivative = (undampedFreq2) => {
        const exponentialDecay = undampedFreq2 * dampingRatio;
        const delta = exponentialDecay * duration;
        const d2 = delta * velocity + velocity;
        const e2 = Math.pow(dampingRatio, 2) * Math.pow(undampedFreq2, 2) * duration;
        const f2 = Math.exp(-delta);
        const g2 = calcAngularFreq(Math.pow(undampedFreq2, 2), dampingRatio);
        const factor = -envelope(undampedFreq2) + safeMin > 0 ? -1 : 1;
        return factor * ((d2 - e2) * f2) / g2;
      };
    } else {
      envelope = (undampedFreq2) => {
        const a = Math.exp(-undampedFreq2 * duration);
        const b2 = (undampedFreq2 - velocity) * duration + 1;
        return -safeMin + a * b2;
      };
      derivative = (undampedFreq2) => {
        const a = Math.exp(-undampedFreq2 * duration);
        const b2 = (velocity - undampedFreq2) * (duration * duration);
        return a * b2;
      };
    }
    const initialGuess = 5 / duration;
    const undampedFreq = approximateRoot(envelope, derivative, initialGuess);
    duration = secondsToMilliseconds(duration);
    if (isNaN(undampedFreq)) {
      return {
        stiffness: 100,
        damping: 10,
        duration
      };
    } else {
      const stiffness = Math.pow(undampedFreq, 2) * mass;
      return {
        stiffness,
        damping: dampingRatio * 2 * Math.sqrt(mass * stiffness),
        duration
      };
    }
  }
  const rootIterations = 12;
  function approximateRoot(envelope, derivative, initialGuess) {
    let result = initialGuess;
    for (let i = 1; i < rootIterations; i++) {
      result = result - envelope(result) / derivative(result);
    }
    return result;
  }
  function calcAngularFreq(undampedFreq, dampingRatio) {
    return undampedFreq * Math.sqrt(1 - dampingRatio * dampingRatio);
  }
  const durationKeys = ["duration", "bounce"];
  const physicsKeys = ["stiffness", "damping", "mass"];
  function isSpringType(options, keys2) {
    return keys2.some((key) => options[key] !== void 0);
  }
  function getSpringOptions(options) {
    let springOptions = {
      velocity: 0,
      stiffness: 100,
      damping: 10,
      mass: 1,
      isResolvedFromDuration: false,
      ...options
    };
    if (!isSpringType(options, physicsKeys) && isSpringType(options, durationKeys)) {
      const derived = findSpring(options);
      springOptions = {
        ...springOptions,
        ...derived,
        mass: 1
      };
      springOptions.isResolvedFromDuration = true;
    }
    return springOptions;
  }
  function spring({ keyframes: keyframes2, restDelta, restSpeed, ...options }) {
    const origin = keyframes2[0];
    const target = keyframes2[keyframes2.length - 1];
    const state2 = { done: false, value: origin };
    const { stiffness, damping, mass, duration, velocity, isResolvedFromDuration } = getSpringOptions({
      ...options,
      velocity: -millisecondsToSeconds(options.velocity || 0)
    });
    const initialVelocity = velocity || 0;
    const dampingRatio = damping / (2 * Math.sqrt(stiffness * mass));
    const initialDelta = target - origin;
    const undampedAngularFreq = millisecondsToSeconds(Math.sqrt(stiffness / mass));
    const isGranularScale = Math.abs(initialDelta) < 5;
    restSpeed || (restSpeed = isGranularScale ? 0.01 : 2);
    restDelta || (restDelta = isGranularScale ? 5e-3 : 0.5);
    let resolveSpring;
    if (dampingRatio < 1) {
      const angularFreq = calcAngularFreq(undampedAngularFreq, dampingRatio);
      resolveSpring = (t2) => {
        const envelope = Math.exp(-dampingRatio * undampedAngularFreq * t2);
        return target - envelope * ((initialVelocity + dampingRatio * undampedAngularFreq * initialDelta) / angularFreq * Math.sin(angularFreq * t2) + initialDelta * Math.cos(angularFreq * t2));
      };
    } else if (dampingRatio === 1) {
      resolveSpring = (t2) => target - Math.exp(-undampedAngularFreq * t2) * (initialDelta + (initialVelocity + undampedAngularFreq * initialDelta) * t2);
    } else {
      const dampedAngularFreq = undampedAngularFreq * Math.sqrt(dampingRatio * dampingRatio - 1);
      resolveSpring = (t2) => {
        const envelope = Math.exp(-dampingRatio * undampedAngularFreq * t2);
        const freqForT = Math.min(dampedAngularFreq * t2, 300);
        return target - envelope * ((initialVelocity + dampingRatio * undampedAngularFreq * initialDelta) * Math.sinh(freqForT) + dampedAngularFreq * initialDelta * Math.cosh(freqForT)) / dampedAngularFreq;
      };
    }
    return {
      calculatedDuration: isResolvedFromDuration ? duration || null : null,
      next: (t2) => {
        const current = resolveSpring(t2);
        if (!isResolvedFromDuration) {
          let currentVelocity = initialVelocity;
          if (t2 !== 0) {
            if (dampingRatio < 1) {
              currentVelocity = calcGeneratorVelocity(resolveSpring, t2, current);
            } else {
              currentVelocity = 0;
            }
          }
          const isBelowVelocityThreshold = Math.abs(currentVelocity) <= restSpeed;
          const isBelowDisplacementThreshold = Math.abs(target - current) <= restDelta;
          state2.done = isBelowVelocityThreshold && isBelowDisplacementThreshold;
        } else {
          state2.done = t2 >= duration;
        }
        state2.value = state2.done ? target : current;
        return state2;
      }
    };
  }
  function inertia({ keyframes: keyframes2, velocity = 0, power = 0.8, timeConstant = 325, bounceDamping = 10, bounceStiffness = 500, modifyTarget, min, max, restDelta = 0.5, restSpeed }) {
    const origin = keyframes2[0];
    const state2 = {
      done: false,
      value: origin
    };
    const isOutOfBounds = (v2) => min !== void 0 && v2 < min || max !== void 0 && v2 > max;
    const nearestBoundary = (v2) => {
      if (min === void 0)
        return max;
      if (max === void 0)
        return min;
      return Math.abs(min - v2) < Math.abs(max - v2) ? min : max;
    };
    let amplitude = power * velocity;
    const ideal = origin + amplitude;
    const target = modifyTarget === void 0 ? ideal : modifyTarget(ideal);
    if (target !== ideal)
      amplitude = target - origin;
    const calcDelta = (t2) => -amplitude * Math.exp(-t2 / timeConstant);
    const calcLatest = (t2) => target + calcDelta(t2);
    const applyFriction = (t2) => {
      const delta = calcDelta(t2);
      const latest = calcLatest(t2);
      state2.done = Math.abs(delta) <= restDelta;
      state2.value = state2.done ? target : latest;
    };
    let timeReachedBoundary;
    let spring$1;
    const checkCatchBoundary = (t2) => {
      if (!isOutOfBounds(state2.value))
        return;
      timeReachedBoundary = t2;
      spring$1 = spring({
        keyframes: [state2.value, nearestBoundary(state2.value)],
        velocity: calcGeneratorVelocity(calcLatest, t2, state2.value),
        // TODO: This should be passing * 1000
        damping: bounceDamping,
        stiffness: bounceStiffness,
        restDelta,
        restSpeed
      });
    };
    checkCatchBoundary(0);
    return {
      calculatedDuration: null,
      next: (t2) => {
        let hasUpdatedFrame = false;
        if (!spring$1 && timeReachedBoundary === void 0) {
          hasUpdatedFrame = true;
          applyFriction(t2);
          checkCatchBoundary(t2);
        }
        if (timeReachedBoundary !== void 0 && t2 >= timeReachedBoundary) {
          return spring$1.next(t2 - timeReachedBoundary);
        } else {
          !hasUpdatedFrame && applyFriction(t2);
          return state2;
        }
      }
    };
  }
  const calcBezier = (t2, a1, a2) => (((1 - 3 * a2 + 3 * a1) * t2 + (3 * a2 - 6 * a1)) * t2 + 3 * a1) * t2;
  const subdivisionPrecision = 1e-7;
  const subdivisionMaxIterations = 12;
  function binarySubdivide(x2, lowerBound, upperBound, mX1, mX2) {
    let currentX;
    let currentT;
    let i = 0;
    do {
      currentT = lowerBound + (upperBound - lowerBound) / 2;
      currentX = calcBezier(currentT, mX1, mX2) - x2;
      if (currentX > 0) {
        upperBound = currentT;
      } else {
        lowerBound = currentT;
      }
    } while (Math.abs(currentX) > subdivisionPrecision && ++i < subdivisionMaxIterations);
    return currentT;
  }
  function cubicBezier(mX1, mY1, mX2, mY2) {
    if (mX1 === mY1 && mX2 === mY2)
      return noop;
    const getTForX = (aX) => binarySubdivide(aX, 0, 1, mX1, mX2);
    return (t2) => t2 === 0 || t2 === 1 ? t2 : calcBezier(getTForX(t2), mY1, mY2);
  }
  const easeIn = cubicBezier(0.42, 0, 1, 1);
  const easeOut = cubicBezier(0, 0, 0.58, 1);
  const easeInOut = cubicBezier(0.42, 0, 0.58, 1);
  const isEasingArray = (ease2) => {
    return Array.isArray(ease2) && typeof ease2[0] !== "number";
  };
  const mirrorEasing = (easing) => (p2) => p2 <= 0.5 ? easing(2 * p2) / 2 : (2 - easing(2 * (1 - p2))) / 2;
  const reverseEasing = (easing) => (p2) => 1 - easing(1 - p2);
  const circIn = (p2) => 1 - Math.sin(Math.acos(p2));
  const circOut = reverseEasing(circIn);
  const circInOut = mirrorEasing(circIn);
  const backOut = cubicBezier(0.33, 1.53, 0.69, 0.99);
  const backIn = reverseEasing(backOut);
  const backInOut = mirrorEasing(backIn);
  const anticipate = (p2) => (p2 *= 2) < 1 ? 0.5 * backIn(p2) : 0.5 * (2 - Math.pow(2, -10 * (p2 - 1)));
  const easingLookup = {
    linear: noop,
    easeIn,
    easeInOut,
    easeOut,
    circIn,
    circInOut,
    circOut,
    backIn,
    backInOut,
    backOut,
    anticipate
  };
  const easingDefinitionToFunction = (definition) => {
    if (Array.isArray(definition)) {
      invariant(definition.length === 4);
      const [x1, y1, x2, y2] = definition;
      return cubicBezier(x1, y1, x2, y2);
    } else if (typeof definition === "string") {
      invariant(easingLookup[definition] !== void 0);
      return easingLookup[definition];
    }
    return definition;
  };
  const progress = (from2, to, value) => {
    const toFromDifference = to - from2;
    return toFromDifference === 0 ? 1 : (value - from2) / toFromDifference;
  };
  const mixNumber$1 = (from2, to, progress2) => {
    return from2 + (to - from2) * progress2;
  };
  function hueToRgb(p2, q2, t2) {
    if (t2 < 0)
      t2 += 1;
    if (t2 > 1)
      t2 -= 1;
    if (t2 < 1 / 6)
      return p2 + (q2 - p2) * 6 * t2;
    if (t2 < 1 / 2)
      return q2;
    if (t2 < 2 / 3)
      return p2 + (q2 - p2) * (2 / 3 - t2) * 6;
    return p2;
  }
  function hslaToRgba({ hue, saturation, lightness, alpha: alpha2 }) {
    hue /= 360;
    saturation /= 100;
    lightness /= 100;
    let red = 0;
    let green = 0;
    let blue = 0;
    if (!saturation) {
      red = green = blue = lightness;
    } else {
      const q2 = lightness < 0.5 ? lightness * (1 + saturation) : lightness + saturation - lightness * saturation;
      const p2 = 2 * lightness - q2;
      red = hueToRgb(p2, q2, hue + 1 / 3);
      green = hueToRgb(p2, q2, hue);
      blue = hueToRgb(p2, q2, hue - 1 / 3);
    }
    return {
      red: Math.round(red * 255),
      green: Math.round(green * 255),
      blue: Math.round(blue * 255),
      alpha: alpha2
    };
  }
  const mixLinearColor = (from2, to, v2) => {
    const fromExpo = from2 * from2;
    const expo = v2 * (to * to - fromExpo) + fromExpo;
    return expo < 0 ? 0 : Math.sqrt(expo);
  };
  const colorTypes = [hex, rgba, hsla];
  const getColorType = (v2) => colorTypes.find((type) => type.test(v2));
  function asRGBA(color2) {
    const type = getColorType(color2);
    let model = type.parse(color2);
    if (type === hsla) {
      model = hslaToRgba(model);
    }
    return model;
  }
  const mixColor = (from2, to) => {
    const fromRGBA = asRGBA(from2);
    const toRGBA = asRGBA(to);
    const blended = { ...fromRGBA };
    return (v2) => {
      blended.red = mixLinearColor(fromRGBA.red, toRGBA.red, v2);
      blended.green = mixLinearColor(fromRGBA.green, toRGBA.green, v2);
      blended.blue = mixLinearColor(fromRGBA.blue, toRGBA.blue, v2);
      blended.alpha = mixNumber$1(fromRGBA.alpha, toRGBA.alpha, v2);
      return rgba.transform(blended);
    };
  };
  const invisibleValues = /* @__PURE__ */ new Set(["none", "hidden"]);
  function mixVisibility(origin, target) {
    if (invisibleValues.has(origin)) {
      return (p2) => p2 <= 0 ? origin : target;
    } else {
      return (p2) => p2 >= 1 ? target : origin;
    }
  }
  function mixImmediate(a, b2) {
    return (p2) => p2 > 0 ? b2 : a;
  }
  function mixNumber(a, b2) {
    return (p2) => mixNumber$1(a, b2, p2);
  }
  function getMixer(a) {
    if (typeof a === "number") {
      return mixNumber;
    } else if (typeof a === "string") {
      return isCSSVariableToken(a) ? mixImmediate : color.test(a) ? mixColor : mixComplex;
    } else if (Array.isArray(a)) {
      return mixArray;
    } else if (typeof a === "object") {
      return color.test(a) ? mixColor : mixObject;
    }
    return mixImmediate;
  }
  function mixArray(a, b2) {
    const output = [...a];
    const numValues = output.length;
    const blendValue = a.map((v2, i) => getMixer(v2)(v2, b2[i]));
    return (p2) => {
      for (let i = 0; i < numValues; i++) {
        output[i] = blendValue[i](p2);
      }
      return output;
    };
  }
  function mixObject(a, b2) {
    const output = { ...a, ...b2 };
    const blendValue = {};
    for (const key in output) {
      if (a[key] !== void 0 && b2[key] !== void 0) {
        blendValue[key] = getMixer(a[key])(a[key], b2[key]);
      }
    }
    return (v2) => {
      for (const key in blendValue) {
        output[key] = blendValue[key](v2);
      }
      return output;
    };
  }
  function matchOrder(origin, target) {
    var _a4;
    const orderedOrigin = [];
    const pointers = { color: 0, var: 0, number: 0 };
    for (let i = 0; i < target.values.length; i++) {
      const type = target.types[i];
      const originIndex = origin.indexes[type][pointers[type]];
      const originValue = (_a4 = origin.values[originIndex]) !== null && _a4 !== void 0 ? _a4 : 0;
      orderedOrigin[i] = originValue;
      pointers[type]++;
    }
    return orderedOrigin;
  }
  const mixComplex = (origin, target) => {
    const template = complex.createTransformer(target);
    const originStats = analyseComplexValue(origin);
    const targetStats = analyseComplexValue(target);
    const canInterpolate = originStats.indexes.var.length === targetStats.indexes.var.length && originStats.indexes.color.length === targetStats.indexes.color.length && originStats.indexes.number.length >= targetStats.indexes.number.length;
    if (canInterpolate) {
      if (invisibleValues.has(origin) && !targetStats.values.length || invisibleValues.has(target) && !originStats.values.length) {
        return mixVisibility(origin, target);
      }
      return pipe(mixArray(matchOrder(originStats, targetStats), targetStats.values), template);
    } else {
      return mixImmediate(origin, target);
    }
  };
  function mix(from2, to, p2) {
    if (typeof from2 === "number" && typeof to === "number" && typeof p2 === "number") {
      return mixNumber$1(from2, to, p2);
    }
    const mixer = getMixer(from2);
    return mixer(from2, to);
  }
  function createMixers(output, ease2, customMixer) {
    const mixers = [];
    const mixerFactory = customMixer || mix;
    const numMixers = output.length - 1;
    for (let i = 0; i < numMixers; i++) {
      let mixer = mixerFactory(output[i], output[i + 1]);
      if (ease2) {
        const easingFunction = Array.isArray(ease2) ? ease2[i] || noop : ease2;
        mixer = pipe(easingFunction, mixer);
      }
      mixers.push(mixer);
    }
    return mixers;
  }
  function interpolate(input, output, { clamp: isClamp = true, ease: ease2, mixer } = {}) {
    const inputLength = input.length;
    invariant(inputLength === output.length);
    if (inputLength === 1)
      return () => output[0];
    if (inputLength === 2 && input[0] === input[1])
      return () => output[1];
    if (input[0] > input[inputLength - 1]) {
      input = [...input].reverse();
      output = [...output].reverse();
    }
    const mixers = createMixers(output, ease2, mixer);
    const numMixers = mixers.length;
    const interpolator = (v2) => {
      let i = 0;
      if (numMixers > 1) {
        for (; i < input.length - 2; i++) {
          if (v2 < input[i + 1])
            break;
        }
      }
      const progressInRange = progress(input[i], input[i + 1], v2);
      return mixers[i](progressInRange);
    };
    return isClamp ? (v2) => interpolator(clamp(input[0], input[inputLength - 1], v2)) : interpolator;
  }
  function fillOffset(offset, remaining) {
    const min = offset[offset.length - 1];
    for (let i = 1; i <= remaining; i++) {
      const offsetProgress = progress(0, remaining, i);
      offset.push(mixNumber$1(min, 1, offsetProgress));
    }
  }
  function defaultOffset(arr) {
    const offset = [0];
    fillOffset(offset, arr.length - 1);
    return offset;
  }
  function convertOffsetToTimes(offset, duration) {
    return offset.map((o) => o * duration);
  }
  function defaultEasing(values, easing) {
    return values.map(() => easing || easeInOut).splice(0, values.length - 1);
  }
  function keyframes({ duration = 300, keyframes: keyframeValues, times, ease: ease2 = "easeInOut" }) {
    const easingFunctions = isEasingArray(ease2) ? ease2.map(easingDefinitionToFunction) : easingDefinitionToFunction(ease2);
    const state2 = {
      done: false,
      value: keyframeValues[0]
    };
    const absoluteTimes = convertOffsetToTimes(
      // Only use the provided offsets if they're the correct length
      // TODO Maybe we should warn here if there's a length mismatch
      times && times.length === keyframeValues.length ? times : defaultOffset(keyframeValues),
      duration
    );
    const mapTimeToKeyframe = interpolate(absoluteTimes, keyframeValues, {
      ease: Array.isArray(easingFunctions) ? easingFunctions : defaultEasing(keyframeValues, easingFunctions)
    });
    return {
      calculatedDuration: duration,
      next: (t2) => {
        state2.value = mapTimeToKeyframe(t2);
        state2.done = t2 >= duration;
        return state2;
      }
    };
  }
  const maxGeneratorDuration = 2e4;
  function calcGeneratorDuration(generator) {
    let duration = 0;
    const timeStep = 50;
    let state2 = generator.next(duration);
    while (!state2.done && duration < maxGeneratorDuration) {
      duration += timeStep;
      state2 = generator.next(duration);
    }
    return duration >= maxGeneratorDuration ? Infinity : duration;
  }
  const frameloopDriver = (update) => {
    const passTimestamp = ({ timestamp }) => update(timestamp);
    return {
      start: () => frame.update(passTimestamp, true),
      stop: () => cancelFrame(passTimestamp),
      /**
       * If we're processing this frame we can use the
       * framelocked timestamp to keep things in sync.
       */
      now: () => frameData.isProcessing ? frameData.timestamp : time.now()
    };
  };
  const generators = {
    decay: inertia,
    inertia,
    tween: keyframes,
    keyframes,
    spring
  };
  const percentToProgress = (percent2) => percent2 / 100;
  class MainThreadAnimation extends BaseAnimation {
    constructor({ KeyframeResolver: KeyframeResolver$1 = KeyframeResolver, ...options }) {
      super(options);
      this.holdTime = null;
      this.startTime = null;
      this.cancelTime = null;
      this.currentTime = 0;
      this.playbackSpeed = 1;
      this.pendingPlayState = "running";
      this.state = "idle";
      this.stop = () => {
        this.resolver.cancel();
        this.isStopped = true;
        if (this.state === "idle")
          return;
        this.teardown();
        const { onStop } = this.options;
        onStop && onStop();
      };
      const { name, motionValue: motionValue2, keyframes: keyframes2 } = this.options;
      const onResolved = (resolvedKeyframes, finalKeyframe) => this.onKeyframesResolved(resolvedKeyframes, finalKeyframe);
      if (name && motionValue2 && motionValue2.owner) {
        this.resolver = motionValue2.owner.resolveKeyframes(keyframes2, onResolved, name, motionValue2);
      } else {
        this.resolver = new KeyframeResolver$1(keyframes2, onResolved, name, motionValue2);
      }
      this.resolver.scheduleResolve();
    }
    initPlayback(keyframes$12) {
      const { type = "keyframes", repeat = 0, repeatDelay = 0, repeatType, velocity = 0 } = this.options;
      const generatorFactory = generators[type] || keyframes;
      let mapPercentToKeyframes;
      let mirroredGenerator;
      if (generatorFactory !== keyframes && typeof keyframes$12[0] !== "number") {
        mapPercentToKeyframes = pipe(percentToProgress, mix(keyframes$12[0], keyframes$12[1]));
        keyframes$12 = [0, 100];
      }
      const generator = generatorFactory({ ...this.options, keyframes: keyframes$12 });
      if (repeatType === "mirror") {
        mirroredGenerator = generatorFactory({
          ...this.options,
          keyframes: [...keyframes$12].reverse(),
          velocity: -velocity
        });
      }
      if (generator.calculatedDuration === null) {
        generator.calculatedDuration = calcGeneratorDuration(generator);
      }
      const { calculatedDuration } = generator;
      const resolvedDuration = calculatedDuration + repeatDelay;
      const totalDuration = resolvedDuration * (repeat + 1) - repeatDelay;
      return {
        generator,
        mirroredGenerator,
        mapPercentToKeyframes,
        calculatedDuration,
        resolvedDuration,
        totalDuration
      };
    }
    onPostResolved() {
      const { autoplay = true } = this.options;
      this.play();
      if (this.pendingPlayState === "paused" || !autoplay) {
        this.pause();
      } else {
        this.state = this.pendingPlayState;
      }
    }
    tick(timestamp, sample = false) {
      const { resolved } = this;
      if (!resolved) {
        const { keyframes: keyframes3 } = this.options;
        return { done: true, value: keyframes3[keyframes3.length - 1] };
      }
      const { finalKeyframe, generator, mirroredGenerator, mapPercentToKeyframes, keyframes: keyframes2, calculatedDuration, totalDuration, resolvedDuration } = resolved;
      if (this.startTime === null)
        return generator.next(0);
      const { delay: delay2, repeat, repeatType, repeatDelay, onUpdate } = this.options;
      if (this.speed > 0) {
        this.startTime = Math.min(this.startTime, timestamp);
      } else if (this.speed < 0) {
        this.startTime = Math.min(timestamp - totalDuration / this.speed, this.startTime);
      }
      if (sample) {
        this.currentTime = timestamp;
      } else if (this.holdTime !== null) {
        this.currentTime = this.holdTime;
      } else {
        this.currentTime = Math.round(timestamp - this.startTime) * this.speed;
      }
      const timeWithoutDelay = this.currentTime - delay2 * (this.speed >= 0 ? 1 : -1);
      const isInDelayPhase = this.speed >= 0 ? timeWithoutDelay < 0 : timeWithoutDelay > totalDuration;
      this.currentTime = Math.max(timeWithoutDelay, 0);
      if (this.state === "finished" && this.holdTime === null) {
        this.currentTime = totalDuration;
      }
      let elapsed = this.currentTime;
      let frameGenerator = generator;
      if (repeat) {
        const progress2 = Math.min(this.currentTime, totalDuration) / resolvedDuration;
        let currentIteration = Math.floor(progress2);
        let iterationProgress = progress2 % 1;
        if (!iterationProgress && progress2 >= 1) {
          iterationProgress = 1;
        }
        iterationProgress === 1 && currentIteration--;
        currentIteration = Math.min(currentIteration, repeat + 1);
        const isOddIteration = Boolean(currentIteration % 2);
        if (isOddIteration) {
          if (repeatType === "reverse") {
            iterationProgress = 1 - iterationProgress;
            if (repeatDelay) {
              iterationProgress -= repeatDelay / resolvedDuration;
            }
          } else if (repeatType === "mirror") {
            frameGenerator = mirroredGenerator;
          }
        }
        elapsed = clamp(0, 1, iterationProgress) * resolvedDuration;
      }
      const state2 = isInDelayPhase ? { done: false, value: keyframes2[0] } : frameGenerator.next(elapsed);
      if (mapPercentToKeyframes) {
        state2.value = mapPercentToKeyframes(state2.value);
      }
      let { done } = state2;
      if (!isInDelayPhase && calculatedDuration !== null) {
        done = this.speed >= 0 ? this.currentTime >= totalDuration : this.currentTime <= 0;
      }
      const isAnimationFinished = this.holdTime === null && (this.state === "finished" || this.state === "running" && done);
      if (isAnimationFinished && finalKeyframe !== void 0) {
        state2.value = getFinalKeyframe(keyframes2, this.options, finalKeyframe);
      }
      if (onUpdate) {
        onUpdate(state2.value);
      }
      if (isAnimationFinished) {
        this.finish();
      }
      return state2;
    }
    get duration() {
      const { resolved } = this;
      return resolved ? millisecondsToSeconds(resolved.calculatedDuration) : 0;
    }
    get time() {
      return millisecondsToSeconds(this.currentTime);
    }
    set time(newTime) {
      newTime = secondsToMilliseconds(newTime);
      this.currentTime = newTime;
      if (this.holdTime !== null || this.speed === 0) {
        this.holdTime = newTime;
      } else if (this.driver) {
        this.startTime = this.driver.now() - newTime / this.speed;
      }
    }
    get speed() {
      return this.playbackSpeed;
    }
    set speed(newSpeed) {
      const hasChanged = this.playbackSpeed !== newSpeed;
      this.playbackSpeed = newSpeed;
      if (hasChanged) {
        this.time = millisecondsToSeconds(this.currentTime);
      }
    }
    play() {
      if (!this.resolver.isScheduled) {
        this.resolver.resume();
      }
      if (!this._resolved) {
        this.pendingPlayState = "running";
        return;
      }
      if (this.isStopped)
        return;
      const { driver = frameloopDriver, onPlay } = this.options;
      if (!this.driver) {
        this.driver = driver((timestamp) => this.tick(timestamp));
      }
      onPlay && onPlay();
      const now2 = this.driver.now();
      if (this.holdTime !== null) {
        this.startTime = now2 - this.holdTime;
      } else if (!this.startTime || this.state === "finished") {
        this.startTime = now2;
      }
      if (this.state === "finished") {
        this.updateFinishedPromise();
      }
      this.cancelTime = this.startTime;
      this.holdTime = null;
      this.state = "running";
      this.driver.start();
    }
    pause() {
      var _a4;
      if (!this._resolved) {
        this.pendingPlayState = "paused";
        return;
      }
      this.state = "paused";
      this.holdTime = (_a4 = this.currentTime) !== null && _a4 !== void 0 ? _a4 : 0;
    }
    complete() {
      if (this.state !== "running") {
        this.play();
      }
      this.pendingPlayState = this.state = "finished";
      this.holdTime = null;
    }
    finish() {
      this.teardown();
      this.state = "finished";
      const { onComplete } = this.options;
      onComplete && onComplete();
    }
    cancel() {
      if (this.cancelTime !== null) {
        this.tick(this.cancelTime);
      }
      this.teardown();
      this.updateFinishedPromise();
    }
    teardown() {
      this.state = "idle";
      this.stopDriver();
      this.resolveFinishedPromise();
      this.updateFinishedPromise();
      this.startTime = this.cancelTime = null;
      this.resolver.cancel();
    }
    stopDriver() {
      if (!this.driver)
        return;
      this.driver.stop();
      this.driver = void 0;
    }
    sample(time2) {
      this.startTime = 0;
      return this.tick(time2, true);
    }
  }
  const isBezierDefinition = (easing) => Array.isArray(easing) && typeof easing[0] === "number";
  function isWaapiSupportedEasing(easing) {
    return Boolean(!easing || typeof easing === "string" && easing in supportedWaapiEasing || isBezierDefinition(easing) || Array.isArray(easing) && easing.every(isWaapiSupportedEasing));
  }
  const cubicBezierAsString = ([a, b2, c2, d2]) => `cubic-bezier(${a}, ${b2}, ${c2}, ${d2})`;
  const supportedWaapiEasing = {
    linear: "linear",
    ease: "ease",
    easeIn: "ease-in",
    easeOut: "ease-out",
    easeInOut: "ease-in-out",
    circIn: cubicBezierAsString([0, 0.65, 0.55, 1]),
    circOut: cubicBezierAsString([0.55, 0, 1, 0.45]),
    backIn: cubicBezierAsString([0.31, 0.01, 0.66, -0.59]),
    backOut: cubicBezierAsString([0.33, 1.53, 0.69, 0.99])
  };
  function mapEasingToNativeEasingWithDefault(easing) {
    return mapEasingToNativeEasing(easing) || supportedWaapiEasing.easeOut;
  }
  function mapEasingToNativeEasing(easing) {
    if (!easing) {
      return void 0;
    } else if (isBezierDefinition(easing)) {
      return cubicBezierAsString(easing);
    } else if (Array.isArray(easing)) {
      return easing.map(mapEasingToNativeEasingWithDefault);
    } else {
      return supportedWaapiEasing[easing];
    }
  }
  function animateStyle(element, valueName, keyframes2, { delay: delay2 = 0, duration = 300, repeat = 0, repeatType = "loop", ease: ease2, times } = {}) {
    const keyframeOptions = { [valueName]: keyframes2 };
    if (times)
      keyframeOptions.offset = times;
    const easing = mapEasingToNativeEasing(ease2);
    if (Array.isArray(easing))
      keyframeOptions.easing = easing;
    return element.animate(keyframeOptions, {
      delay: delay2,
      duration,
      easing: !Array.isArray(easing) ? easing : "linear",
      fill: "both",
      iterations: repeat + 1,
      direction: repeatType === "reverse" ? "alternate" : "normal"
    });
  }
  const supportsWaapi = memo(() => Object.hasOwnProperty.call(Element.prototype, "animate"));
  const acceleratedValues = /* @__PURE__ */ new Set([
    "opacity",
    "clipPath",
    "filter",
    "transform"
    // TODO: Can be accelerated but currently disabled until https://issues.chromium.org/issues/41491098 is resolved
    // or until we implement support for linear() easing.
    // "background-color"
  ]);
  const sampleDelta = 10;
  const maxDuration = 2e4;
  function requiresPregeneratedKeyframes(options) {
    return options.type === "spring" || options.name === "backgroundColor" || !isWaapiSupportedEasing(options.ease);
  }
  function pregenerateKeyframes(keyframes2, options) {
    const sampleAnimation = new MainThreadAnimation({
      ...options,
      keyframes: keyframes2,
      repeat: 0,
      delay: 0,
      isGenerator: true
    });
    let state2 = { done: false, value: keyframes2[0] };
    const pregeneratedKeyframes = [];
    let t2 = 0;
    while (!state2.done && t2 < maxDuration) {
      state2 = sampleAnimation.sample(t2);
      pregeneratedKeyframes.push(state2.value);
      t2 += sampleDelta;
    }
    return {
      times: void 0,
      keyframes: pregeneratedKeyframes,
      duration: t2 - sampleDelta,
      ease: "linear"
    };
  }
  class AcceleratedAnimation extends BaseAnimation {
    constructor(options) {
      super(options);
      const { name, motionValue: motionValue2, keyframes: keyframes2 } = this.options;
      this.resolver = new DOMKeyframesResolver(keyframes2, (resolvedKeyframes, finalKeyframe) => this.onKeyframesResolved(resolvedKeyframes, finalKeyframe), name, motionValue2);
      this.resolver.scheduleResolve();
    }
    initPlayback(keyframes2, finalKeyframe) {
      var _a4;
      let { duration = 300, times, ease: ease2, type, motionValue: motionValue2, name } = this.options;
      if (!((_a4 = motionValue2.owner) === null || _a4 === void 0 ? void 0 : _a4.current)) {
        return false;
      }
      if (requiresPregeneratedKeyframes(this.options)) {
        const { onComplete, onUpdate, motionValue: motionValue3, ...options } = this.options;
        const pregeneratedAnimation = pregenerateKeyframes(keyframes2, options);
        keyframes2 = pregeneratedAnimation.keyframes;
        if (keyframes2.length === 1) {
          keyframes2[1] = keyframes2[0];
        }
        duration = pregeneratedAnimation.duration;
        times = pregeneratedAnimation.times;
        ease2 = pregeneratedAnimation.ease;
        type = "keyframes";
      }
      const animation = animateStyle(motionValue2.owner.current, name, keyframes2, { ...this.options, duration, times, ease: ease2 });
      animation.startTime = time.now();
      if (this.pendingTimeline) {
        animation.timeline = this.pendingTimeline;
        this.pendingTimeline = void 0;
      } else {
        animation.onfinish = () => {
          const { onComplete } = this.options;
          motionValue2.set(getFinalKeyframe(keyframes2, this.options, finalKeyframe));
          onComplete && onComplete();
          this.cancel();
          this.resolveFinishedPromise();
        };
      }
      return {
        animation,
        duration,
        times,
        type,
        ease: ease2,
        keyframes: keyframes2
      };
    }
    get duration() {
      const { resolved } = this;
      if (!resolved)
        return 0;
      const { duration } = resolved;
      return millisecondsToSeconds(duration);
    }
    get time() {
      const { resolved } = this;
      if (!resolved)
        return 0;
      const { animation } = resolved;
      return millisecondsToSeconds(animation.currentTime || 0);
    }
    set time(newTime) {
      const { resolved } = this;
      if (!resolved)
        return;
      const { animation } = resolved;
      animation.currentTime = secondsToMilliseconds(newTime);
    }
    get speed() {
      const { resolved } = this;
      if (!resolved)
        return 1;
      const { animation } = resolved;
      return animation.playbackRate;
    }
    set speed(newSpeed) {
      const { resolved } = this;
      if (!resolved)
        return;
      const { animation } = resolved;
      animation.playbackRate = newSpeed;
    }
    get state() {
      const { resolved } = this;
      if (!resolved)
        return "idle";
      const { animation } = resolved;
      return animation.playState;
    }
    /**
     * Replace the default DocumentTimeline with another AnimationTimeline.
     * Currently used for scroll animations.
     */
    attachTimeline(timeline) {
      if (!this._resolved) {
        this.pendingTimeline = timeline;
      } else {
        const { resolved } = this;
        if (!resolved)
          return noop;
        const { animation } = resolved;
        animation.timeline = timeline;
        animation.onfinish = null;
      }
      return noop;
    }
    play() {
      if (this.isStopped)
        return;
      const { resolved } = this;
      if (!resolved)
        return;
      const { animation } = resolved;
      if (animation.playState === "finished") {
        this.updateFinishedPromise();
      }
      animation.play();
    }
    pause() {
      const { resolved } = this;
      if (!resolved)
        return;
      const { animation } = resolved;
      animation.pause();
    }
    stop() {
      this.resolver.cancel();
      this.isStopped = true;
      if (this.state === "idle")
        return;
      const { resolved } = this;
      if (!resolved)
        return;
      const { animation, keyframes: keyframes2, duration, type, ease: ease2, times } = resolved;
      if (animation.playState === "idle" || animation.playState === "finished") {
        return;
      }
      if (this.time) {
        const { motionValue: motionValue2, onUpdate, onComplete, ...options } = this.options;
        const sampleAnimation = new MainThreadAnimation({
          ...options,
          keyframes: keyframes2,
          duration,
          type,
          ease: ease2,
          times,
          isGenerator: true
        });
        const sampleTime = secondsToMilliseconds(this.time);
        motionValue2.setWithVelocity(sampleAnimation.sample(sampleTime - sampleDelta).value, sampleAnimation.sample(sampleTime).value, sampleDelta);
      }
      this.cancel();
    }
    complete() {
      const { resolved } = this;
      if (!resolved)
        return;
      resolved.animation.finish();
    }
    cancel() {
      const { resolved } = this;
      if (!resolved)
        return;
      resolved.animation.cancel();
    }
    static supports(options) {
      const { motionValue: motionValue2, name, repeatDelay, repeatType, damping, type } = options;
      return supportsWaapi() && name && acceleratedValues.has(name) && motionValue2 && motionValue2.owner && motionValue2.owner.current instanceof HTMLElement && /**
       * If we're outputting values to onUpdate then we can't use WAAPI as there's
       * no way to read the value from WAAPI every frame.
       */
      !motionValue2.owner.getProps().onUpdate && !repeatDelay && repeatType !== "mirror" && damping !== 0 && type !== "inertia";
    }
  }
  const animateMotionValue = (name, value, target, transition2 = {}, element, isHandoff) => (onComplete) => {
    const valueTransition = getValueTransition(transition2, name) || {};
    const delay2 = valueTransition.delay || transition2.delay || 0;
    let { elapsed = 0 } = transition2;
    elapsed = elapsed - secondsToMilliseconds(delay2);
    let options = {
      keyframes: Array.isArray(target) ? target : [null, target],
      ease: "easeOut",
      velocity: value.getVelocity(),
      ...valueTransition,
      delay: -elapsed,
      onUpdate: (v2) => {
        value.set(v2);
        valueTransition.onUpdate && valueTransition.onUpdate(v2);
      },
      onComplete: () => {
        onComplete();
        valueTransition.onComplete && valueTransition.onComplete();
      },
      name,
      motionValue: value,
      element: isHandoff ? void 0 : element
    };
    if (!isTransitionDefined(valueTransition)) {
      options = {
        ...options,
        ...getDefaultTransition(name, options)
      };
    }
    if (options.duration) {
      options.duration = secondsToMilliseconds(options.duration);
    }
    if (options.repeatDelay) {
      options.repeatDelay = secondsToMilliseconds(options.repeatDelay);
    }
    if (options.from !== void 0) {
      options.keyframes[0] = options.from;
    }
    let shouldSkip = false;
    if (options.type === false || options.duration === 0 && !options.repeatDelay) {
      options.duration = 0;
      if (options.delay === 0) {
        shouldSkip = true;
      }
    }
    if (shouldSkip && !isHandoff && value.get() !== void 0) {
      const finalKeyframe = getFinalKeyframe(options.keyframes, valueTransition);
      if (finalKeyframe !== void 0) {
        frame.update(() => {
          options.onUpdate(finalKeyframe);
          options.onComplete();
        });
        return;
      }
    }
    if (!isHandoff && AcceleratedAnimation.supports(options)) {
      return new AcceleratedAnimation(options);
    } else {
      return new MainThreadAnimation(options);
    }
  };
  function isWillChangeMotionValue(value) {
    return Boolean(isMotionValue(value) && value.add);
  }
  function addUniqueItem(arr, item) {
    if (arr.indexOf(item) === -1)
      arr.push(item);
  }
  function removeItem(arr, item) {
    const index = arr.indexOf(item);
    if (index > -1)
      arr.splice(index, 1);
  }
  class SubscriptionManager {
    constructor() {
      this.subscriptions = [];
    }
    add(handler) {
      addUniqueItem(this.subscriptions, handler);
      return () => removeItem(this.subscriptions, handler);
    }
    notify(a, b2, c2) {
      const numSubscriptions = this.subscriptions.length;
      if (!numSubscriptions)
        return;
      if (numSubscriptions === 1) {
        this.subscriptions[0](a, b2, c2);
      } else {
        for (let i = 0; i < numSubscriptions; i++) {
          const handler = this.subscriptions[i];
          handler && handler(a, b2, c2);
        }
      }
    }
    getSize() {
      return this.subscriptions.length;
    }
    clear() {
      this.subscriptions.length = 0;
    }
  }
  const MAX_VELOCITY_DELTA = 30;
  const isFloat = (value) => {
    return !isNaN(parseFloat(value));
  };
  class MotionValue {
    /**
     * @param init - The initiating value
     * @param config - Optional configuration options
     *
     * -  `transformer`: A function to transform incoming values with.
     *
     * @internal
     */
    constructor(init, options = {}) {
      this.version = "11.2.0";
      this.canTrackVelocity = false;
      this.events = {};
      this.updateAndNotify = (v2, render = true) => {
        const currentTime = time.now();
        if (this.updatedAt !== currentTime) {
          this.setPrevFrameValue();
        }
        this.prev = this.current;
        this.setCurrent(v2);
        if (this.current !== this.prev && this.events.change) {
          this.events.change.notify(this.current);
        }
        if (render && this.events.renderRequest) {
          this.events.renderRequest.notify(this.current);
        }
      };
      this.hasAnimated = false;
      this.setCurrent(init);
      this.canTrackVelocity = isFloat(this.current);
      this.owner = options.owner;
    }
    setCurrent(current) {
      this.current = current;
      this.updatedAt = time.now();
    }
    setPrevFrameValue(prevFrameValue = this.current) {
      this.prevFrameValue = prevFrameValue;
      this.prevUpdatedAt = this.updatedAt;
    }
    /**
     * Adds a function that will be notified when the `MotionValue` is updated.
     *
     * It returns a function that, when called, will cancel the subscription.
     *
     * When calling `onChange` inside a React component, it should be wrapped with the
     * `useEffect` hook. As it returns an unsubscribe function, this should be returned
     * from the `useEffect` function to ensure you don't add duplicate subscribers..
     *
     * ```jsx
     * export const MyComponent = () => {
     *   const x = useMotionValue(0)
     *   const y = useMotionValue(0)
     *   const opacity = useMotionValue(1)
     *
     *   useEffect(() => {
     *     function updateOpacity() {
     *       const maxXY = Math.max(x.get(), y.get())
     *       const newOpacity = transform(maxXY, [0, 100], [1, 0])
     *       opacity.set(newOpacity)
     *     }
     *
     *     const unsubscribeX = x.on("change", updateOpacity)
     *     const unsubscribeY = y.on("change", updateOpacity)
     *
     *     return () => {
     *       unsubscribeX()
     *       unsubscribeY()
     *     }
     *   }, [])
     *
     *   return <motion.div style={{ x }} />
     * }
     * ```
     *
     * @param subscriber - A function that receives the latest value.
     * @returns A function that, when called, will cancel this subscription.
     *
     * @deprecated
     */
    onChange(subscription) {
      return this.on("change", subscription);
    }
    on(eventName, callback) {
      if (!this.events[eventName]) {
        this.events[eventName] = new SubscriptionManager();
      }
      const unsubscribe = this.events[eventName].add(callback);
      if (eventName === "change") {
        return () => {
          unsubscribe();
          frame.read(() => {
            if (!this.events.change.getSize()) {
              this.stop();
            }
          });
        };
      }
      return unsubscribe;
    }
    clearListeners() {
      for (const eventManagers in this.events) {
        this.events[eventManagers].clear();
      }
    }
    /**
     * Attaches a passive effect to the `MotionValue`.
     *
     * @internal
     */
    attach(passiveEffect, stopPassiveEffect) {
      this.passiveEffect = passiveEffect;
      this.stopPassiveEffect = stopPassiveEffect;
    }
    /**
     * Sets the state of the `MotionValue`.
     *
     * @remarks
     *
     * ```jsx
     * const x = useMotionValue(0)
     * x.set(10)
     * ```
     *
     * @param latest - Latest value to set.
     * @param render - Whether to notify render subscribers. Defaults to `true`
     *
     * @public
     */
    set(v2, render = true) {
      if (!render || !this.passiveEffect) {
        this.updateAndNotify(v2, render);
      } else {
        this.passiveEffect(v2, this.updateAndNotify);
      }
    }
    setWithVelocity(prev2, current, delta) {
      this.set(current);
      this.prev = void 0;
      this.prevFrameValue = prev2;
      this.prevUpdatedAt = this.updatedAt - delta;
    }
    /**
     * Set the state of the `MotionValue`, stopping any active animations,
     * effects, and resets velocity to `0`.
     */
    jump(v2, endAnimation = true) {
      this.updateAndNotify(v2);
      this.prev = v2;
      this.prevUpdatedAt = this.prevFrameValue = void 0;
      endAnimation && this.stop();
      if (this.stopPassiveEffect)
        this.stopPassiveEffect();
    }
    /**
     * Returns the latest state of `MotionValue`
     *
     * @returns - The latest state of `MotionValue`
     *
     * @public
     */
    get() {
      return this.current;
    }
    /**
     * @public
     */
    getPrevious() {
      return this.prev;
    }
    /**
     * Returns the latest velocity of `MotionValue`
     *
     * @returns - The latest velocity of `MotionValue`. Returns `0` if the state is non-numerical.
     *
     * @public
     */
    getVelocity() {
      const currentTime = time.now();
      if (!this.canTrackVelocity || this.prevFrameValue === void 0 || currentTime - this.updatedAt > MAX_VELOCITY_DELTA) {
        return 0;
      }
      const delta = Math.min(this.updatedAt - this.prevUpdatedAt, MAX_VELOCITY_DELTA);
      return velocityPerSecond(parseFloat(this.current) - parseFloat(this.prevFrameValue), delta);
    }
    /**
     * Registers a new animation to control this `MotionValue`. Only one
     * animation can drive a `MotionValue` at one time.
     *
     * ```jsx
     * value.start()
     * ```
     *
     * @param animation - A function that starts the provided animation
     *
     * @internal
     */
    start(startAnimation) {
      this.stop();
      return new Promise((resolve) => {
        this.hasAnimated = true;
        this.animation = startAnimation(resolve);
        if (this.events.animationStart) {
          this.events.animationStart.notify();
        }
      }).then(() => {
        if (this.events.animationComplete) {
          this.events.animationComplete.notify();
        }
        this.clearAnimation();
      });
    }
    /**
     * Stop the currently active animation.
     *
     * @public
     */
    stop() {
      if (this.animation) {
        this.animation.stop();
        if (this.events.animationCancel) {
          this.events.animationCancel.notify();
        }
      }
      this.clearAnimation();
    }
    /**
     * Returns `true` if this value is currently animating.
     *
     * @public
     */
    isAnimating() {
      return !!this.animation;
    }
    clearAnimation() {
      delete this.animation;
    }
    /**
     * Destroy and clean up subscribers to this `MotionValue`.
     *
     * The `MotionValue` hooks like `useMotionValue` and `useTransform` automatically
     * handle the lifecycle of the returned `MotionValue`, so this method is only necessary if you've manually
     * created a `MotionValue` via the `motionValue` function.
     *
     * @public
     */
    destroy() {
      this.clearListeners();
      this.stop();
      if (this.stopPassiveEffect) {
        this.stopPassiveEffect();
      }
    }
  }
  function motionValue(init, options) {
    return new MotionValue(init, options);
  }
  function setMotionValue(visualElement, key, value) {
    if (visualElement.hasValue(key)) {
      visualElement.getValue(key).set(value);
    } else {
      visualElement.addValue(key, motionValue(value));
    }
  }
  function setTarget(visualElement, definition) {
    const resolved = resolveVariant(visualElement, definition);
    let { transitionEnd = {}, transition: transition2 = {}, ...target } = resolved || {};
    target = { ...target, ...transitionEnd };
    for (const key in target) {
      const value = resolveFinalValueInKeyframes(target[key]);
      setMotionValue(visualElement, key, value);
    }
  }
  function shouldBlockAnimation({ protectedKeys, needsAnimating }, key) {
    const shouldBlock = protectedKeys.hasOwnProperty(key) && needsAnimating[key] !== true;
    needsAnimating[key] = false;
    return shouldBlock;
  }
  function animateTarget(visualElement, targetAndTransition, { delay: delay2 = 0, transitionOverride, type } = {}) {
    var _a4;
    let { transition: transition2 = visualElement.getDefaultTransition(), transitionEnd, ...target } = targetAndTransition;
    const willChange = visualElement.getValue("willChange");
    if (transitionOverride)
      transition2 = transitionOverride;
    const animations2 = [];
    const animationTypeState = type && visualElement.animationState && visualElement.animationState.getState()[type];
    for (const key in target) {
      const value = visualElement.getValue(key, (_a4 = visualElement.latestValues[key]) !== null && _a4 !== void 0 ? _a4 : null);
      const valueTarget = target[key];
      if (valueTarget === void 0 || animationTypeState && shouldBlockAnimation(animationTypeState, key)) {
        continue;
      }
      const valueTransition = {
        delay: delay2,
        elapsed: 0,
        ...getValueTransition(transition2 || {}, key)
      };
      let isHandoff = false;
      if (window.HandoffAppearAnimations) {
        const props = visualElement.getProps();
        const appearId = props[optimizedAppearDataAttribute];
        if (appearId) {
          const elapsed = window.HandoffAppearAnimations(appearId, key);
          if (elapsed !== null) {
            valueTransition.elapsed = elapsed;
            isHandoff = true;
          }
        }
      }
      value.start(animateMotionValue(key, value, valueTarget, visualElement.shouldReduceMotion && transformProps.has(key) ? { type: false } : valueTransition, visualElement, isHandoff));
      const animation = value.animation;
      if (animation) {
        if (isWillChangeMotionValue(willChange)) {
          willChange.add(key);
          animation.then(() => willChange.remove(key));
        }
        animations2.push(animation);
      }
    }
    if (transitionEnd) {
      Promise.all(animations2).then(() => {
        frame.update(() => {
          transitionEnd && setTarget(visualElement, transitionEnd);
        });
      });
    }
    return animations2;
  }
  function animateVariant(visualElement, variant, options = {}) {
    var _a4;
    const resolved = resolveVariant(visualElement, variant, options.type === "exit" ? (_a4 = visualElement.presenceContext) === null || _a4 === void 0 ? void 0 : _a4.custom : void 0);
    let { transition: transition2 = visualElement.getDefaultTransition() || {} } = resolved || {};
    if (options.transitionOverride) {
      transition2 = options.transitionOverride;
    }
    const getAnimation = resolved ? () => Promise.all(animateTarget(visualElement, resolved, options)) : () => Promise.resolve();
    const getChildAnimations = visualElement.variantChildren && visualElement.variantChildren.size ? (forwardDelay = 0) => {
      const { delayChildren = 0, staggerChildren, staggerDirection } = transition2;
      return animateChildren(visualElement, variant, delayChildren + forwardDelay, staggerChildren, staggerDirection, options);
    } : () => Promise.resolve();
    const { when } = transition2;
    if (when) {
      const [first, last] = when === "beforeChildren" ? [getAnimation, getChildAnimations] : [getChildAnimations, getAnimation];
      return first().then(() => last());
    } else {
      return Promise.all([getAnimation(), getChildAnimations(options.delay)]);
    }
  }
  function animateChildren(visualElement, variant, delayChildren = 0, staggerChildren = 0, staggerDirection = 1, options) {
    const animations2 = [];
    const maxStaggerDuration = (visualElement.variantChildren.size - 1) * staggerChildren;
    const generateStaggerDuration = staggerDirection === 1 ? (i = 0) => i * staggerChildren : (i = 0) => maxStaggerDuration - i * staggerChildren;
    Array.from(visualElement.variantChildren).sort(sortByTreeOrder).forEach((child, i) => {
      child.notify("AnimationStart", variant);
      animations2.push(animateVariant(child, variant, {
        ...options,
        delay: delayChildren + generateStaggerDuration(i)
      }).then(() => child.notify("AnimationComplete", variant)));
    });
    return Promise.all(animations2);
  }
  function sortByTreeOrder(a, b2) {
    return a.sortNodePosition(b2);
  }
  function animateVisualElement(visualElement, definition, options = {}) {
    visualElement.notify("AnimationStart", definition);
    let animation;
    if (Array.isArray(definition)) {
      const animations2 = definition.map((variant) => animateVariant(visualElement, variant, options));
      animation = Promise.all(animations2);
    } else if (typeof definition === "string") {
      animation = animateVariant(visualElement, definition, options);
    } else {
      const resolvedDefinition = typeof definition === "function" ? resolveVariant(visualElement, definition, options.custom) : definition;
      animation = Promise.all(animateTarget(visualElement, resolvedDefinition, options));
    }
    return animation.then(() => {
      frame.postRender(() => {
        visualElement.notify("AnimationComplete", definition);
      });
    });
  }
  const reversePriorityOrder = [...variantPriorityOrder].reverse();
  const numAnimationTypes = variantPriorityOrder.length;
  function animateList(visualElement) {
    return (animations2) => Promise.all(animations2.map(({ animation, options }) => animateVisualElement(visualElement, animation, options)));
  }
  function createAnimationState(visualElement) {
    let animate = animateList(visualElement);
    const state2 = createState();
    let isInitialRender = true;
    const buildResolvedTypeValues = (type) => (acc, definition) => {
      var _a4;
      const resolved = resolveVariant(visualElement, definition, type === "exit" ? (_a4 = visualElement.presenceContext) === null || _a4 === void 0 ? void 0 : _a4.custom : void 0);
      if (resolved) {
        const { transition: transition2, transitionEnd, ...target } = resolved;
        acc = { ...acc, ...target, ...transitionEnd };
      }
      return acc;
    };
    function setAnimateFunction(makeAnimator) {
      animate = makeAnimator(visualElement);
    }
    function animateChanges(changedActiveType) {
      const props = visualElement.getProps();
      const context = visualElement.getVariantContext(true) || {};
      const animations2 = [];
      const removedKeys = /* @__PURE__ */ new Set();
      let encounteredKeys = {};
      let removedVariantIndex = Infinity;
      for (let i = 0; i < numAnimationTypes; i++) {
        const type = reversePriorityOrder[i];
        const typeState = state2[type];
        const prop = props[type] !== void 0 ? props[type] : context[type];
        const propIsVariant = isVariantLabel(prop);
        const activeDelta = type === changedActiveType ? typeState.isActive : null;
        if (activeDelta === false)
          removedVariantIndex = i;
        let isInherited = prop === context[type] && prop !== props[type] && propIsVariant;
        if (isInherited && isInitialRender && visualElement.manuallyAnimateOnMount) {
          isInherited = false;
        }
        typeState.protectedKeys = { ...encounteredKeys };
        if (
          // If it isn't active and hasn't *just* been set as inactive
          !typeState.isActive && activeDelta === null || // If we didn't and don't have any defined prop for this animation type
          !prop && !typeState.prevProp || // Or if the prop doesn't define an animation
          isAnimationControls(prop) || typeof prop === "boolean"
        ) {
          continue;
        }
        const variantDidChange = checkVariantsDidChange(typeState.prevProp, prop);
        let shouldAnimateType = variantDidChange || // If we're making this variant active, we want to always make it active
        type === changedActiveType && typeState.isActive && !isInherited && propIsVariant || // If we removed a higher-priority variant (i is in reverse order)
        i > removedVariantIndex && propIsVariant;
        let handledRemovedValues = false;
        const definitionList = Array.isArray(prop) ? prop : [prop];
        let resolvedValues = definitionList.reduce(buildResolvedTypeValues(type), {});
        if (activeDelta === false)
          resolvedValues = {};
        const { prevResolvedValues = {} } = typeState;
        const allKeys = {
          ...prevResolvedValues,
          ...resolvedValues
        };
        const markToAnimate = (key) => {
          shouldAnimateType = true;
          if (removedKeys.has(key)) {
            handledRemovedValues = true;
            removedKeys.delete(key);
          }
          typeState.needsAnimating[key] = true;
          const motionValue2 = visualElement.getValue(key);
          if (motionValue2)
            motionValue2.liveStyle = false;
        };
        for (const key in allKeys) {
          const next2 = resolvedValues[key];
          const prev2 = prevResolvedValues[key];
          if (encounteredKeys.hasOwnProperty(key))
            continue;
          let valueHasChanged = false;
          if (isKeyframesTarget(next2) && isKeyframesTarget(prev2)) {
            valueHasChanged = !shallowCompare(next2, prev2);
          } else {
            valueHasChanged = next2 !== prev2;
          }
          if (valueHasChanged) {
            if (next2 !== void 0 && next2 !== null) {
              markToAnimate(key);
            } else {
              removedKeys.add(key);
            }
          } else if (next2 !== void 0 && removedKeys.has(key)) {
            markToAnimate(key);
          } else {
            typeState.protectedKeys[key] = true;
          }
        }
        typeState.prevProp = prop;
        typeState.prevResolvedValues = resolvedValues;
        if (typeState.isActive) {
          encounteredKeys = { ...encounteredKeys, ...resolvedValues };
        }
        if (isInitialRender && visualElement.blockInitialAnimation) {
          shouldAnimateType = false;
        }
        if (shouldAnimateType && (!isInherited || handledRemovedValues)) {
          animations2.push(...definitionList.map((animation) => ({
            animation,
            options: { type }
          })));
        }
      }
      if (removedKeys.size) {
        const fallbackAnimation = {};
        removedKeys.forEach((key) => {
          const fallbackTarget = visualElement.getBaseTarget(key);
          const motionValue2 = visualElement.getValue(key);
          if (motionValue2)
            motionValue2.liveStyle = true;
          fallbackAnimation[key] = fallbackTarget !== null && fallbackTarget !== void 0 ? fallbackTarget : null;
        });
        animations2.push({ animation: fallbackAnimation });
      }
      let shouldAnimate = Boolean(animations2.length);
      if (isInitialRender && (props.initial === false || props.initial === props.animate) && !visualElement.manuallyAnimateOnMount) {
        shouldAnimate = false;
      }
      isInitialRender = false;
      return shouldAnimate ? animate(animations2) : Promise.resolve();
    }
    function setActive(type, isActive) {
      var _a4;
      if (state2[type].isActive === isActive)
        return Promise.resolve();
      (_a4 = visualElement.variantChildren) === null || _a4 === void 0 ? void 0 : _a4.forEach((child) => {
        var _a5;
        return (_a5 = child.animationState) === null || _a5 === void 0 ? void 0 : _a5.setActive(type, isActive);
      });
      state2[type].isActive = isActive;
      const animations2 = animateChanges(type);
      for (const key in state2) {
        state2[key].protectedKeys = {};
      }
      return animations2;
    }
    return {
      animateChanges,
      setActive,
      setAnimateFunction,
      getState: () => state2
    };
  }
  function checkVariantsDidChange(prev2, next2) {
    if (typeof next2 === "string") {
      return next2 !== prev2;
    } else if (Array.isArray(next2)) {
      return !shallowCompare(next2, prev2);
    }
    return false;
  }
  function createTypeState(isActive = false) {
    return {
      isActive,
      protectedKeys: {},
      needsAnimating: {},
      prevResolvedValues: {}
    };
  }
  function createState() {
    return {
      animate: createTypeState(true),
      whileInView: createTypeState(),
      whileHover: createTypeState(),
      whileTap: createTypeState(),
      whileDrag: createTypeState(),
      whileFocus: createTypeState(),
      exit: createTypeState()
    };
  }
  class AnimationFeature extends Feature {
    /**
     * We dynamically generate the AnimationState manager as it contains a reference
     * to the underlying animation library. We only want to load that if we load this,
     * so people can optionally code split it out using the `m` component.
     */
    constructor(node2) {
      super(node2);
      node2.animationState || (node2.animationState = createAnimationState(node2));
    }
    updateAnimationControlsSubscription() {
      const { animate } = this.node.getProps();
      this.unmount();
      if (isAnimationControls(animate)) {
        this.unmount = animate.subscribe(this.node);
      }
    }
    /**
     * Subscribe any provided AnimationControls to the component's VisualElement
     */
    mount() {
      this.updateAnimationControlsSubscription();
    }
    update() {
      const { animate } = this.node.getProps();
      const { animate: prevAnimate } = this.node.prevProps || {};
      if (animate !== prevAnimate) {
        this.updateAnimationControlsSubscription();
      }
    }
    unmount() {
    }
  }
  let id$1 = 0;
  class ExitAnimationFeature extends Feature {
    constructor() {
      super(...arguments);
      this.id = id$1++;
    }
    update() {
      if (!this.node.presenceContext)
        return;
      const { isPresent: isPresent2, onExitComplete } = this.node.presenceContext;
      const { isPresent: prevIsPresent } = this.node.prevPresenceContext || {};
      if (!this.node.animationState || isPresent2 === prevIsPresent) {
        return;
      }
      const exitAnimation = this.node.animationState.setActive("exit", !isPresent2);
      if (onExitComplete && !isPresent2) {
        exitAnimation.then(() => onExitComplete(this.id));
      }
    }
    mount() {
      const { register } = this.node.presenceContext || {};
      if (register) {
        this.unmount = register(this.id);
      }
    }
    unmount() {
    }
  }
  const animations = {
    animation: {
      Feature: AnimationFeature
    },
    exit: {
      Feature: ExitAnimationFeature
    }
  };
  const distance = (a, b2) => Math.abs(a - b2);
  function distance2D(a, b2) {
    const xDelta = distance(a.x, b2.x);
    const yDelta = distance(a.y, b2.y);
    return Math.sqrt(xDelta ** 2 + yDelta ** 2);
  }
  class PanSession {
    constructor(event, handlers, { transformPagePoint, contextWindow, dragSnapToOrigin = false } = {}) {
      this.startEvent = null;
      this.lastMoveEvent = null;
      this.lastMoveEventInfo = null;
      this.handlers = {};
      this.contextWindow = window;
      this.updatePoint = () => {
        if (!(this.lastMoveEvent && this.lastMoveEventInfo))
          return;
        const info2 = getPanInfo(this.lastMoveEventInfo, this.history);
        const isPanStarted = this.startEvent !== null;
        const isDistancePastThreshold = distance2D(info2.offset, { x: 0, y: 0 }) >= 3;
        if (!isPanStarted && !isDistancePastThreshold)
          return;
        const { point: point2 } = info2;
        const { timestamp: timestamp2 } = frameData;
        this.history.push({ ...point2, timestamp: timestamp2 });
        const { onStart, onMove } = this.handlers;
        if (!isPanStarted) {
          onStart && onStart(this.lastMoveEvent, info2);
          this.startEvent = this.lastMoveEvent;
        }
        onMove && onMove(this.lastMoveEvent, info2);
      };
      this.handlePointerMove = (event2, info2) => {
        this.lastMoveEvent = event2;
        this.lastMoveEventInfo = transformPoint(info2, this.transformPagePoint);
        frame.update(this.updatePoint, true);
      };
      this.handlePointerUp = (event2, info2) => {
        this.end();
        const { onEnd, onSessionEnd, resumeAnimation } = this.handlers;
        if (this.dragSnapToOrigin)
          resumeAnimation && resumeAnimation();
        if (!(this.lastMoveEvent && this.lastMoveEventInfo))
          return;
        const panInfo = getPanInfo(event2.type === "pointercancel" ? this.lastMoveEventInfo : transformPoint(info2, this.transformPagePoint), this.history);
        if (this.startEvent && onEnd) {
          onEnd(event2, panInfo);
        }
        onSessionEnd && onSessionEnd(event2, panInfo);
      };
      if (!isPrimaryPointer(event))
        return;
      this.dragSnapToOrigin = dragSnapToOrigin;
      this.handlers = handlers;
      this.transformPagePoint = transformPagePoint;
      this.contextWindow = contextWindow || window;
      const info = extractEventInfo(event);
      const initialInfo = transformPoint(info, this.transformPagePoint);
      const { point } = initialInfo;
      const { timestamp } = frameData;
      this.history = [{ ...point, timestamp }];
      const { onSessionStart } = handlers;
      onSessionStart && onSessionStart(event, getPanInfo(initialInfo, this.history));
      this.removeListeners = pipe(addPointerEvent(this.contextWindow, "pointermove", this.handlePointerMove), addPointerEvent(this.contextWindow, "pointerup", this.handlePointerUp), addPointerEvent(this.contextWindow, "pointercancel", this.handlePointerUp));
    }
    updateHandlers(handlers) {
      this.handlers = handlers;
    }
    end() {
      this.removeListeners && this.removeListeners();
      cancelFrame(this.updatePoint);
    }
  }
  function transformPoint(info, transformPagePoint) {
    return transformPagePoint ? { point: transformPagePoint(info.point) } : info;
  }
  function subtractPoint(a, b2) {
    return { x: a.x - b2.x, y: a.y - b2.y };
  }
  function getPanInfo({ point }, history) {
    return {
      point,
      delta: subtractPoint(point, lastDevicePoint(history)),
      offset: subtractPoint(point, startDevicePoint(history)),
      velocity: getVelocity(history, 0.1)
    };
  }
  function startDevicePoint(history) {
    return history[0];
  }
  function lastDevicePoint(history) {
    return history[history.length - 1];
  }
  function getVelocity(history, timeDelta) {
    if (history.length < 2) {
      return { x: 0, y: 0 };
    }
    let i = history.length - 1;
    let timestampedPoint = null;
    const lastPoint = lastDevicePoint(history);
    while (i >= 0) {
      timestampedPoint = history[i];
      if (lastPoint.timestamp - timestampedPoint.timestamp > secondsToMilliseconds(timeDelta)) {
        break;
      }
      i--;
    }
    if (!timestampedPoint) {
      return { x: 0, y: 0 };
    }
    const time2 = millisecondsToSeconds(lastPoint.timestamp - timestampedPoint.timestamp);
    if (time2 === 0) {
      return { x: 0, y: 0 };
    }
    const currentVelocity = {
      x: (lastPoint.x - timestampedPoint.x) / time2,
      y: (lastPoint.y - timestampedPoint.y) / time2
    };
    if (currentVelocity.x === Infinity) {
      currentVelocity.x = 0;
    }
    if (currentVelocity.y === Infinity) {
      currentVelocity.y = 0;
    }
    return currentVelocity;
  }
  function calcLength(axis) {
    return axis.max - axis.min;
  }
  function isNear(value, target = 0, maxDistance = 0.01) {
    return Math.abs(value - target) <= maxDistance;
  }
  function calcAxisDelta(delta, source, target, origin = 0.5) {
    delta.origin = origin;
    delta.originPoint = mixNumber$1(source.min, source.max, delta.origin);
    delta.scale = calcLength(target) / calcLength(source);
    if (isNear(delta.scale, 1, 1e-4) || isNaN(delta.scale))
      delta.scale = 1;
    delta.translate = mixNumber$1(target.min, target.max, delta.origin) - delta.originPoint;
    if (isNear(delta.translate) || isNaN(delta.translate))
      delta.translate = 0;
  }
  function calcBoxDelta(delta, source, target, origin) {
    calcAxisDelta(delta.x, source.x, target.x, origin ? origin.originX : void 0);
    calcAxisDelta(delta.y, source.y, target.y, origin ? origin.originY : void 0);
  }
  function calcRelativeAxis(target, relative, parent) {
    target.min = parent.min + relative.min;
    target.max = target.min + calcLength(relative);
  }
  function calcRelativeBox(target, relative, parent) {
    calcRelativeAxis(target.x, relative.x, parent.x);
    calcRelativeAxis(target.y, relative.y, parent.y);
  }
  function calcRelativeAxisPosition(target, layout2, parent) {
    target.min = layout2.min - parent.min;
    target.max = target.min + calcLength(layout2);
  }
  function calcRelativePosition(target, layout2, parent) {
    calcRelativeAxisPosition(target.x, layout2.x, parent.x);
    calcRelativeAxisPosition(target.y, layout2.y, parent.y);
  }
  function applyConstraints(point, { min, max }, elastic) {
    if (min !== void 0 && point < min) {
      point = elastic ? mixNumber$1(min, point, elastic.min) : Math.max(point, min);
    } else if (max !== void 0 && point > max) {
      point = elastic ? mixNumber$1(max, point, elastic.max) : Math.min(point, max);
    }
    return point;
  }
  function calcRelativeAxisConstraints(axis, min, max) {
    return {
      min: min !== void 0 ? axis.min + min : void 0,
      max: max !== void 0 ? axis.max + max - (axis.max - axis.min) : void 0
    };
  }
  function calcRelativeConstraints(layoutBox, { top, left, bottom, right }) {
    return {
      x: calcRelativeAxisConstraints(layoutBox.x, left, right),
      y: calcRelativeAxisConstraints(layoutBox.y, top, bottom)
    };
  }
  function calcViewportAxisConstraints(layoutAxis, constraintsAxis) {
    let min = constraintsAxis.min - layoutAxis.min;
    let max = constraintsAxis.max - layoutAxis.max;
    if (constraintsAxis.max - constraintsAxis.min < layoutAxis.max - layoutAxis.min) {
      [min, max] = [max, min];
    }
    return { min, max };
  }
  function calcViewportConstraints(layoutBox, constraintsBox) {
    return {
      x: calcViewportAxisConstraints(layoutBox.x, constraintsBox.x),
      y: calcViewportAxisConstraints(layoutBox.y, constraintsBox.y)
    };
  }
  function calcOrigin(source, target) {
    let origin = 0.5;
    const sourceLength = calcLength(source);
    const targetLength = calcLength(target);
    if (targetLength > sourceLength) {
      origin = progress(target.min, target.max - sourceLength, source.min);
    } else if (sourceLength > targetLength) {
      origin = progress(source.min, source.max - targetLength, target.min);
    }
    return clamp(0, 1, origin);
  }
  function rebaseAxisConstraints(layout2, constraints) {
    const relativeConstraints = {};
    if (constraints.min !== void 0) {
      relativeConstraints.min = constraints.min - layout2.min;
    }
    if (constraints.max !== void 0) {
      relativeConstraints.max = constraints.max - layout2.min;
    }
    return relativeConstraints;
  }
  const defaultElastic = 0.35;
  function resolveDragElastic(dragElastic = defaultElastic) {
    if (dragElastic === false) {
      dragElastic = 0;
    } else if (dragElastic === true) {
      dragElastic = defaultElastic;
    }
    return {
      x: resolveAxisElastic(dragElastic, "left", "right"),
      y: resolveAxisElastic(dragElastic, "top", "bottom")
    };
  }
  function resolveAxisElastic(dragElastic, minLabel, maxLabel) {
    return {
      min: resolvePointElastic(dragElastic, minLabel),
      max: resolvePointElastic(dragElastic, maxLabel)
    };
  }
  function resolvePointElastic(dragElastic, label) {
    return typeof dragElastic === "number" ? dragElastic : dragElastic[label] || 0;
  }
  const createAxisDelta = () => ({
    translate: 0,
    scale: 1,
    origin: 0,
    originPoint: 0
  });
  const createDelta = () => ({
    x: createAxisDelta(),
    y: createAxisDelta()
  });
  const createAxis = () => ({ min: 0, max: 0 });
  const createBox = () => ({
    x: createAxis(),
    y: createAxis()
  });
  function eachAxis(callback) {
    return [callback("x"), callback("y")];
  }
  function convertBoundingBoxToBox({ top, left, right, bottom }) {
    return {
      x: { min: left, max: right },
      y: { min: top, max: bottom }
    };
  }
  function convertBoxToBoundingBox({ x: x2, y: y2 }) {
    return { top: y2.min, right: x2.max, bottom: y2.max, left: x2.min };
  }
  function transformBoxPoints(point, transformPoint2) {
    if (!transformPoint2)
      return point;
    const topLeft = transformPoint2({ x: point.left, y: point.top });
    const bottomRight = transformPoint2({ x: point.right, y: point.bottom });
    return {
      top: topLeft.y,
      left: topLeft.x,
      bottom: bottomRight.y,
      right: bottomRight.x
    };
  }
  function isIdentityScale(scale2) {
    return scale2 === void 0 || scale2 === 1;
  }
  function hasScale({ scale: scale2, scaleX, scaleY }) {
    return !isIdentityScale(scale2) || !isIdentityScale(scaleX) || !isIdentityScale(scaleY);
  }
  function hasTransform(values) {
    return hasScale(values) || has2DTranslate(values) || values.z || values.rotate || values.rotateX || values.rotateY || values.skewX || values.skewY;
  }
  function has2DTranslate(values) {
    return is2DTranslate(values.x) || is2DTranslate(values.y);
  }
  function is2DTranslate(value) {
    return value && value !== "0%";
  }
  function scalePoint(point, scale2, originPoint) {
    const distanceFromOrigin = point - originPoint;
    const scaled = scale2 * distanceFromOrigin;
    return originPoint + scaled;
  }
  function applyPointDelta(point, translate, scale2, originPoint, boxScale) {
    if (boxScale !== void 0) {
      point = scalePoint(point, boxScale, originPoint);
    }
    return scalePoint(point, scale2, originPoint) + translate;
  }
  function applyAxisDelta(axis, translate = 0, scale2 = 1, originPoint, boxScale) {
    axis.min = applyPointDelta(axis.min, translate, scale2, originPoint, boxScale);
    axis.max = applyPointDelta(axis.max, translate, scale2, originPoint, boxScale);
  }
  function applyBoxDelta(box, { x: x2, y: y2 }) {
    applyAxisDelta(box.x, x2.translate, x2.scale, x2.originPoint);
    applyAxisDelta(box.y, y2.translate, y2.scale, y2.originPoint);
  }
  function applyTreeDeltas(box, treeScale, treePath, isSharedTransition = false) {
    const treeLength = treePath.length;
    if (!treeLength)
      return;
    treeScale.x = treeScale.y = 1;
    let node2;
    let delta;
    for (let i = 0; i < treeLength; i++) {
      node2 = treePath[i];
      delta = node2.projectionDelta;
      const instance = node2.instance;
      if (instance && instance.style && instance.style.display === "contents") {
        continue;
      }
      if (isSharedTransition && node2.options.layoutScroll && node2.scroll && node2 !== node2.root) {
        transformBox(box, {
          x: -node2.scroll.offset.x,
          y: -node2.scroll.offset.y
        });
      }
      if (delta) {
        treeScale.x *= delta.x.scale;
        treeScale.y *= delta.y.scale;
        applyBoxDelta(box, delta);
      }
      if (isSharedTransition && hasTransform(node2.latestValues)) {
        transformBox(box, node2.latestValues);
      }
    }
    treeScale.x = snapToDefault(treeScale.x);
    treeScale.y = snapToDefault(treeScale.y);
  }
  function snapToDefault(scale2) {
    if (Number.isInteger(scale2))
      return scale2;
    return scale2 > 1.0000000000001 || scale2 < 0.999999999999 ? scale2 : 1;
  }
  function translateAxis(axis, distance2) {
    axis.min = axis.min + distance2;
    axis.max = axis.max + distance2;
  }
  function transformAxis(axis, transforms, [key, scaleKey, originKey]) {
    const axisOrigin = transforms[originKey] !== void 0 ? transforms[originKey] : 0.5;
    const originPoint = mixNumber$1(axis.min, axis.max, axisOrigin);
    applyAxisDelta(axis, transforms[key], transforms[scaleKey], originPoint, transforms.scale);
  }
  const xKeys$1 = ["x", "scaleX", "originX"];
  const yKeys$1 = ["y", "scaleY", "originY"];
  function transformBox(box, transform2) {
    transformAxis(box.x, transform2, xKeys$1);
    transformAxis(box.y, transform2, yKeys$1);
  }
  function measureViewportBox(instance, transformPoint2) {
    return convertBoundingBoxToBox(transformBoxPoints(instance.getBoundingClientRect(), transformPoint2));
  }
  function measurePageBox(element, rootProjectionNode2, transformPagePoint) {
    const viewportBox = measureViewportBox(element, transformPagePoint);
    const { scroll: scroll2 } = rootProjectionNode2;
    if (scroll2) {
      translateAxis(viewportBox.x, scroll2.offset.x);
      translateAxis(viewportBox.y, scroll2.offset.y);
    }
    return viewportBox;
  }
  const getContextWindow = ({ current }) => {
    return current ? current.ownerDocument.defaultView : null;
  };
  const elementDragControls = /* @__PURE__ */ new WeakMap();
  class VisualElementDragControls {
    constructor(visualElement) {
      this.openGlobalLock = null;
      this.isDragging = false;
      this.currentDirection = null;
      this.originPoint = { x: 0, y: 0 };
      this.constraints = false;
      this.hasMutatedConstraints = false;
      this.elastic = createBox();
      this.visualElement = visualElement;
    }
    start(originEvent, { snapToCursor = false } = {}) {
      const { presenceContext } = this.visualElement;
      if (presenceContext && presenceContext.isPresent === false)
        return;
      const onSessionStart = (event) => {
        const { dragSnapToOrigin: dragSnapToOrigin2 } = this.getProps();
        dragSnapToOrigin2 ? this.pauseAnimation() : this.stopAnimation();
        if (snapToCursor) {
          this.snapToCursor(extractEventInfo(event, "page").point);
        }
      };
      const onStart = (event, info) => {
        const { drag: drag2, dragPropagation, onDragStart } = this.getProps();
        if (drag2 && !dragPropagation) {
          if (this.openGlobalLock)
            this.openGlobalLock();
          this.openGlobalLock = getGlobalLock(drag2);
          if (!this.openGlobalLock)
            return;
        }
        this.isDragging = true;
        this.currentDirection = null;
        this.resolveConstraints();
        if (this.visualElement.projection) {
          this.visualElement.projection.isAnimationBlocked = true;
          this.visualElement.projection.target = void 0;
        }
        eachAxis((axis) => {
          let current = this.getAxisMotionValue(axis).get() || 0;
          if (percent.test(current)) {
            const { projection } = this.visualElement;
            if (projection && projection.layout) {
              const measuredAxis = projection.layout.layoutBox[axis];
              if (measuredAxis) {
                const length2 = calcLength(measuredAxis);
                current = length2 * (parseFloat(current) / 100);
              }
            }
          }
          this.originPoint[axis] = current;
        });
        if (onDragStart) {
          frame.postRender(() => onDragStart(event, info));
        }
        const { animationState } = this.visualElement;
        animationState && animationState.setActive("whileDrag", true);
      };
      const onMove = (event, info) => {
        const { dragPropagation, dragDirectionLock, onDirectionLock, onDrag } = this.getProps();
        if (!dragPropagation && !this.openGlobalLock)
          return;
        const { offset } = info;
        if (dragDirectionLock && this.currentDirection === null) {
          this.currentDirection = getCurrentDirection(offset);
          if (this.currentDirection !== null) {
            onDirectionLock && onDirectionLock(this.currentDirection);
          }
          return;
        }
        this.updateAxis("x", info.point, offset);
        this.updateAxis("y", info.point, offset);
        this.visualElement.render();
        onDrag && onDrag(event, info);
      };
      const onSessionEnd = (event, info) => this.stop(event, info);
      const resumeAnimation = () => eachAxis((axis) => {
        var _a4;
        return this.getAnimationState(axis) === "paused" && ((_a4 = this.getAxisMotionValue(axis).animation) === null || _a4 === void 0 ? void 0 : _a4.play());
      });
      const { dragSnapToOrigin } = this.getProps();
      this.panSession = new PanSession(originEvent, {
        onSessionStart,
        onStart,
        onMove,
        onSessionEnd,
        resumeAnimation
      }, {
        transformPagePoint: this.visualElement.getTransformPagePoint(),
        dragSnapToOrigin,
        contextWindow: getContextWindow(this.visualElement)
      });
    }
    stop(event, info) {
      const isDragging = this.isDragging;
      this.cancel();
      if (!isDragging)
        return;
      const { velocity } = info;
      this.startAnimation(velocity);
      const { onDragEnd } = this.getProps();
      if (onDragEnd) {
        frame.postRender(() => onDragEnd(event, info));
      }
    }
    cancel() {
      this.isDragging = false;
      const { projection, animationState } = this.visualElement;
      if (projection) {
        projection.isAnimationBlocked = false;
      }
      this.panSession && this.panSession.end();
      this.panSession = void 0;
      const { dragPropagation } = this.getProps();
      if (!dragPropagation && this.openGlobalLock) {
        this.openGlobalLock();
        this.openGlobalLock = null;
      }
      animationState && animationState.setActive("whileDrag", false);
    }
    updateAxis(axis, _point, offset) {
      const { drag: drag2 } = this.getProps();
      if (!offset || !shouldDrag(axis, drag2, this.currentDirection))
        return;
      const axisValue = this.getAxisMotionValue(axis);
      let next2 = this.originPoint[axis] + offset[axis];
      if (this.constraints && this.constraints[axis]) {
        next2 = applyConstraints(next2, this.constraints[axis], this.elastic[axis]);
      }
      axisValue.set(next2);
    }
    resolveConstraints() {
      var _a4;
      const { dragConstraints, dragElastic } = this.getProps();
      const layout2 = this.visualElement.projection && !this.visualElement.projection.layout ? this.visualElement.projection.measure(false) : (_a4 = this.visualElement.projection) === null || _a4 === void 0 ? void 0 : _a4.layout;
      const prevConstraints = this.constraints;
      if (dragConstraints && isRefObject(dragConstraints)) {
        if (!this.constraints) {
          this.constraints = this.resolveRefConstraints();
        }
      } else {
        if (dragConstraints && layout2) {
          this.constraints = calcRelativeConstraints(layout2.layoutBox, dragConstraints);
        } else {
          this.constraints = false;
        }
      }
      this.elastic = resolveDragElastic(dragElastic);
      if (prevConstraints !== this.constraints && layout2 && this.constraints && !this.hasMutatedConstraints) {
        eachAxis((axis) => {
          if (this.constraints !== false && this.getAxisMotionValue(axis)) {
            this.constraints[axis] = rebaseAxisConstraints(layout2.layoutBox[axis], this.constraints[axis]);
          }
        });
      }
    }
    resolveRefConstraints() {
      const { dragConstraints: constraints, onMeasureDragConstraints } = this.getProps();
      if (!constraints || !isRefObject(constraints))
        return false;
      const constraintsElement = constraints.current;
      const { projection } = this.visualElement;
      if (!projection || !projection.layout)
        return false;
      const constraintsBox = measurePageBox(constraintsElement, projection.root, this.visualElement.getTransformPagePoint());
      let measuredConstraints = calcViewportConstraints(projection.layout.layoutBox, constraintsBox);
      if (onMeasureDragConstraints) {
        const userConstraints = onMeasureDragConstraints(convertBoxToBoundingBox(measuredConstraints));
        this.hasMutatedConstraints = !!userConstraints;
        if (userConstraints) {
          measuredConstraints = convertBoundingBoxToBox(userConstraints);
        }
      }
      return measuredConstraints;
    }
    startAnimation(velocity) {
      const { drag: drag2, dragMomentum, dragElastic, dragTransition, dragSnapToOrigin, onDragTransitionEnd } = this.getProps();
      const constraints = this.constraints || {};
      const momentumAnimations = eachAxis((axis) => {
        if (!shouldDrag(axis, drag2, this.currentDirection)) {
          return;
        }
        let transition2 = constraints && constraints[axis] || {};
        if (dragSnapToOrigin)
          transition2 = { min: 0, max: 0 };
        const bounceStiffness = dragElastic ? 200 : 1e6;
        const bounceDamping = dragElastic ? 40 : 1e7;
        const inertia2 = {
          type: "inertia",
          velocity: dragMomentum ? velocity[axis] : 0,
          bounceStiffness,
          bounceDamping,
          timeConstant: 750,
          restDelta: 1,
          restSpeed: 10,
          ...dragTransition,
          ...transition2
        };
        return this.startAxisValueAnimation(axis, inertia2);
      });
      return Promise.all(momentumAnimations).then(onDragTransitionEnd);
    }
    startAxisValueAnimation(axis, transition2) {
      const axisValue = this.getAxisMotionValue(axis);
      return axisValue.start(animateMotionValue(axis, axisValue, 0, transition2, this.visualElement));
    }
    stopAnimation() {
      eachAxis((axis) => this.getAxisMotionValue(axis).stop());
    }
    pauseAnimation() {
      eachAxis((axis) => {
        var _a4;
        return (_a4 = this.getAxisMotionValue(axis).animation) === null || _a4 === void 0 ? void 0 : _a4.pause();
      });
    }
    getAnimationState(axis) {
      var _a4;
      return (_a4 = this.getAxisMotionValue(axis).animation) === null || _a4 === void 0 ? void 0 : _a4.state;
    }
    /**
     * Drag works differently depending on which props are provided.
     *
     * - If _dragX and _dragY are provided, we output the gesture delta directly to those motion values.
     * - Otherwise, we apply the delta to the x/y motion values.
     */
    getAxisMotionValue(axis) {
      const dragKey = `_drag${axis.toUpperCase()}`;
      const props = this.visualElement.getProps();
      const externalMotionValue = props[dragKey];
      return externalMotionValue ? externalMotionValue : this.visualElement.getValue(axis, (props.initial ? props.initial[axis] : void 0) || 0);
    }
    snapToCursor(point) {
      eachAxis((axis) => {
        const { drag: drag2 } = this.getProps();
        if (!shouldDrag(axis, drag2, this.currentDirection))
          return;
        const { projection } = this.visualElement;
        const axisValue = this.getAxisMotionValue(axis);
        if (projection && projection.layout) {
          const { min, max } = projection.layout.layoutBox[axis];
          axisValue.set(point[axis] - mixNumber$1(min, max, 0.5));
        }
      });
    }
    /**
     * When the viewport resizes we want to check if the measured constraints
     * have changed and, if so, reposition the element within those new constraints
     * relative to where it was before the resize.
     */
    scalePositionWithinConstraints() {
      if (!this.visualElement.current)
        return;
      const { drag: drag2, dragConstraints } = this.getProps();
      const { projection } = this.visualElement;
      if (!isRefObject(dragConstraints) || !projection || !this.constraints)
        return;
      this.stopAnimation();
      const boxProgress = { x: 0, y: 0 };
      eachAxis((axis) => {
        const axisValue = this.getAxisMotionValue(axis);
        if (axisValue && this.constraints !== false) {
          const latest = axisValue.get();
          boxProgress[axis] = calcOrigin({ min: latest, max: latest }, this.constraints[axis]);
        }
      });
      const { transformTemplate: transformTemplate2 } = this.visualElement.getProps();
      this.visualElement.current.style.transform = transformTemplate2 ? transformTemplate2({}, "") : "none";
      projection.root && projection.root.updateScroll();
      projection.updateLayout();
      this.resolveConstraints();
      eachAxis((axis) => {
        if (!shouldDrag(axis, drag2, null))
          return;
        const axisValue = this.getAxisMotionValue(axis);
        const { min, max } = this.constraints[axis];
        axisValue.set(mixNumber$1(min, max, boxProgress[axis]));
      });
    }
    addListeners() {
      if (!this.visualElement.current)
        return;
      elementDragControls.set(this.visualElement, this);
      const element = this.visualElement.current;
      const stopPointerListener = addPointerEvent(element, "pointerdown", (event) => {
        const { drag: drag2, dragListener = true } = this.getProps();
        drag2 && dragListener && this.start(event);
      });
      const measureDragConstraints = () => {
        const { dragConstraints } = this.getProps();
        if (isRefObject(dragConstraints)) {
          this.constraints = this.resolveRefConstraints();
        }
      };
      const { projection } = this.visualElement;
      const stopMeasureLayoutListener = projection.addEventListener("measure", measureDragConstraints);
      if (projection && !projection.layout) {
        projection.root && projection.root.updateScroll();
        projection.updateLayout();
      }
      measureDragConstraints();
      const stopResizeListener = addDomEvent(window, "resize", () => this.scalePositionWithinConstraints());
      const stopLayoutUpdateListener = projection.addEventListener("didUpdate", ({ delta, hasLayoutChanged }) => {
        if (this.isDragging && hasLayoutChanged) {
          eachAxis((axis) => {
            const motionValue2 = this.getAxisMotionValue(axis);
            if (!motionValue2)
              return;
            this.originPoint[axis] += delta[axis].translate;
            motionValue2.set(motionValue2.get() + delta[axis].translate);
          });
          this.visualElement.render();
        }
      });
      return () => {
        stopResizeListener();
        stopPointerListener();
        stopMeasureLayoutListener();
        stopLayoutUpdateListener && stopLayoutUpdateListener();
      };
    }
    getProps() {
      const props = this.visualElement.getProps();
      const { drag: drag2 = false, dragDirectionLock = false, dragPropagation = false, dragConstraints = false, dragElastic = defaultElastic, dragMomentum = true } = props;
      return {
        ...props,
        drag: drag2,
        dragDirectionLock,
        dragPropagation,
        dragConstraints,
        dragElastic,
        dragMomentum
      };
    }
  }
  function shouldDrag(direction2, drag2, currentDirection) {
    return (drag2 === true || drag2 === direction2) && (currentDirection === null || currentDirection === direction2);
  }
  function getCurrentDirection(offset, lockThreshold = 10) {
    let direction2 = null;
    if (Math.abs(offset.y) > lockThreshold) {
      direction2 = "y";
    } else if (Math.abs(offset.x) > lockThreshold) {
      direction2 = "x";
    }
    return direction2;
  }
  class DragGesture extends Feature {
    constructor(node2) {
      super(node2);
      this.removeGroupControls = noop;
      this.removeListeners = noop;
      this.controls = new VisualElementDragControls(node2);
    }
    mount() {
      const { dragControls } = this.node.getProps();
      if (dragControls) {
        this.removeGroupControls = dragControls.subscribe(this.controls);
      }
      this.removeListeners = this.controls.addListeners() || noop;
    }
    unmount() {
      this.removeGroupControls();
      this.removeListeners();
    }
  }
  const asyncHandler = (handler) => (event, info) => {
    if (handler) {
      frame.postRender(() => handler(event, info));
    }
  };
  class PanGesture extends Feature {
    constructor() {
      super(...arguments);
      this.removePointerDownListener = noop;
    }
    onPointerDown(pointerDownEvent) {
      this.session = new PanSession(pointerDownEvent, this.createPanHandlers(), {
        transformPagePoint: this.node.getTransformPagePoint(),
        contextWindow: getContextWindow(this.node)
      });
    }
    createPanHandlers() {
      const { onPanSessionStart, onPanStart, onPan, onPanEnd } = this.node.getProps();
      return {
        onSessionStart: asyncHandler(onPanSessionStart),
        onStart: asyncHandler(onPanStart),
        onMove: onPan,
        onEnd: (event, info) => {
          delete this.session;
          if (onPanEnd) {
            frame.postRender(() => onPanEnd(event, info));
          }
        }
      };
    }
    mount() {
      this.removePointerDownListener = addPointerEvent(this.node.current, "pointerdown", (event) => this.onPointerDown(event));
    }
    update() {
      this.session && this.session.updateHandlers(this.createPanHandlers());
    }
    unmount() {
      this.removePointerDownListener();
      this.session && this.session.end();
    }
  }
  function usePresence() {
    const context = reactExports.useContext(PresenceContext);
    if (context === null)
      return [true, null];
    const { isPresent: isPresent2, onExitComplete, register } = context;
    const id2 = reactExports.useId();
    reactExports.useEffect(() => register(id2), []);
    const safeToRemove = () => onExitComplete && onExitComplete(id2);
    return !isPresent2 && onExitComplete ? [false, safeToRemove] : [true];
  }
  function useIsPresent() {
    return isPresent(reactExports.useContext(PresenceContext));
  }
  function isPresent(context) {
    return context === null ? true : context.isPresent;
  }
  const globalProjectionState = {
    /**
     * Global flag as to whether the tree has animated since the last time
     * we resized the window
     */
    hasAnimatedSinceResize: true,
    /**
     * We set this to true once, on the first update. Any nodes added to the tree beyond that
     * update will be given a `data-projection-id` attribute.
     */
    hasEverUpdated: false
  };
  function pixelsToPercent(pixels, axis) {
    if (axis.max === axis.min)
      return 0;
    return pixels / (axis.max - axis.min) * 100;
  }
  const correctBorderRadius = {
    correct: (latest, node2) => {
      if (!node2.target)
        return latest;
      if (typeof latest === "string") {
        if (px.test(latest)) {
          latest = parseFloat(latest);
        } else {
          return latest;
        }
      }
      const x2 = pixelsToPercent(latest, node2.target.x);
      const y2 = pixelsToPercent(latest, node2.target.y);
      return `${x2}% ${y2}%`;
    }
  };
  const correctBoxShadow = {
    correct: (latest, { treeScale, projectionDelta }) => {
      const original = latest;
      const shadow = complex.parse(latest);
      if (shadow.length > 5)
        return original;
      const template = complex.createTransformer(latest);
      const offset = typeof shadow[0] !== "number" ? 1 : 0;
      const xScale = projectionDelta.x.scale * treeScale.x;
      const yScale = projectionDelta.y.scale * treeScale.y;
      shadow[0 + offset] /= xScale;
      shadow[1 + offset] /= yScale;
      const averageScale = mixNumber$1(xScale, yScale, 0.5);
      if (typeof shadow[2 + offset] === "number")
        shadow[2 + offset] /= averageScale;
      if (typeof shadow[3 + offset] === "number")
        shadow[3 + offset] /= averageScale;
      return template(shadow);
    }
  };
  class MeasureLayoutWithContext extends reactExports.Component {
    /**
     * This only mounts projection nodes for components that
     * need measuring, we might want to do it for all components
     * in order to incorporate transforms
     */
    componentDidMount() {
      const { visualElement, layoutGroup, switchLayoutGroup, layoutId } = this.props;
      const { projection } = visualElement;
      addScaleCorrector(defaultScaleCorrectors);
      if (projection) {
        if (layoutGroup.group)
          layoutGroup.group.add(projection);
        if (switchLayoutGroup && switchLayoutGroup.register && layoutId) {
          switchLayoutGroup.register(projection);
        }
        projection.root.didUpdate();
        projection.addEventListener("animationComplete", () => {
          this.safeToRemove();
        });
        projection.setOptions({
          ...projection.options,
          onExitComplete: () => this.safeToRemove()
        });
      }
      globalProjectionState.hasEverUpdated = true;
    }
    getSnapshotBeforeUpdate(prevProps) {
      const { layoutDependency, visualElement, drag: drag2, isPresent: isPresent2 } = this.props;
      const projection = visualElement.projection;
      if (!projection)
        return null;
      projection.isPresent = isPresent2;
      if (drag2 || prevProps.layoutDependency !== layoutDependency || layoutDependency === void 0) {
        projection.willUpdate();
      } else {
        this.safeToRemove();
      }
      if (prevProps.isPresent !== isPresent2) {
        if (isPresent2) {
          projection.promote();
        } else if (!projection.relegate()) {
          frame.postRender(() => {
            const stack = projection.getStack();
            if (!stack || !stack.members.length) {
              this.safeToRemove();
            }
          });
        }
      }
      return null;
    }
    componentDidUpdate() {
      const { projection } = this.props.visualElement;
      if (projection) {
        projection.root.didUpdate();
        microtask.postRender(() => {
          if (!projection.currentAnimation && projection.isLead()) {
            this.safeToRemove();
          }
        });
      }
    }
    componentWillUnmount() {
      const { visualElement, layoutGroup, switchLayoutGroup: promoteContext } = this.props;
      const { projection } = visualElement;
      if (projection) {
        projection.scheduleCheckAfterUnmount();
        if (layoutGroup && layoutGroup.group)
          layoutGroup.group.remove(projection);
        if (promoteContext && promoteContext.deregister)
          promoteContext.deregister(projection);
      }
    }
    safeToRemove() {
      const { safeToRemove } = this.props;
      safeToRemove && safeToRemove();
    }
    render() {
      return null;
    }
  }
  function MeasureLayout(props) {
    const [isPresent2, safeToRemove] = usePresence();
    const layoutGroup = reactExports.useContext(LayoutGroupContext);
    return jsxRuntimeExports.jsx(MeasureLayoutWithContext, { ...props, layoutGroup, switchLayoutGroup: reactExports.useContext(SwitchLayoutGroupContext), isPresent: isPresent2, safeToRemove });
  }
  const defaultScaleCorrectors = {
    borderRadius: {
      ...correctBorderRadius,
      applyTo: [
        "borderTopLeftRadius",
        "borderTopRightRadius",
        "borderBottomLeftRadius",
        "borderBottomRightRadius"
      ]
    },
    borderTopLeftRadius: correctBorderRadius,
    borderTopRightRadius: correctBorderRadius,
    borderBottomLeftRadius: correctBorderRadius,
    borderBottomRightRadius: correctBorderRadius,
    boxShadow: correctBoxShadow
  };
  const borders = ["TopLeft", "TopRight", "BottomLeft", "BottomRight"];
  const numBorders = borders.length;
  const asNumber = (value) => typeof value === "string" ? parseFloat(value) : value;
  const isPx = (value) => typeof value === "number" || px.test(value);
  function mixValues(target, follow, lead, progress2, shouldCrossfadeOpacity, isOnlyMember) {
    if (shouldCrossfadeOpacity) {
      target.opacity = mixNumber$1(
        0,
        // TODO Reinstate this if only child
        lead.opacity !== void 0 ? lead.opacity : 1,
        easeCrossfadeIn(progress2)
      );
      target.opacityExit = mixNumber$1(follow.opacity !== void 0 ? follow.opacity : 1, 0, easeCrossfadeOut(progress2));
    } else if (isOnlyMember) {
      target.opacity = mixNumber$1(follow.opacity !== void 0 ? follow.opacity : 1, lead.opacity !== void 0 ? lead.opacity : 1, progress2);
    }
    for (let i = 0; i < numBorders; i++) {
      const borderLabel = `border${borders[i]}Radius`;
      let followRadius = getRadius(follow, borderLabel);
      let leadRadius = getRadius(lead, borderLabel);
      if (followRadius === void 0 && leadRadius === void 0)
        continue;
      followRadius || (followRadius = 0);
      leadRadius || (leadRadius = 0);
      const canMix = followRadius === 0 || leadRadius === 0 || isPx(followRadius) === isPx(leadRadius);
      if (canMix) {
        target[borderLabel] = Math.max(mixNumber$1(asNumber(followRadius), asNumber(leadRadius), progress2), 0);
        if (percent.test(leadRadius) || percent.test(followRadius)) {
          target[borderLabel] += "%";
        }
      } else {
        target[borderLabel] = leadRadius;
      }
    }
    if (follow.rotate || lead.rotate) {
      target.rotate = mixNumber$1(follow.rotate || 0, lead.rotate || 0, progress2);
    }
  }
  function getRadius(values, radiusName) {
    return values[radiusName] !== void 0 ? values[radiusName] : values.borderRadius;
  }
  const easeCrossfadeIn = compress(0, 0.5, circOut);
  const easeCrossfadeOut = compress(0.5, 0.95, noop);
  function compress(min, max, easing) {
    return (p2) => {
      if (p2 < min)
        return 0;
      if (p2 > max)
        return 1;
      return easing(progress(min, max, p2));
    };
  }
  function copyAxisInto(axis, originAxis) {
    axis.min = originAxis.min;
    axis.max = originAxis.max;
  }
  function copyBoxInto(box, originBox) {
    copyAxisInto(box.x, originBox.x);
    copyAxisInto(box.y, originBox.y);
  }
  function removePointDelta(point, translate, scale2, originPoint, boxScale) {
    point -= translate;
    point = scalePoint(point, 1 / scale2, originPoint);
    if (boxScale !== void 0) {
      point = scalePoint(point, 1 / boxScale, originPoint);
    }
    return point;
  }
  function removeAxisDelta(axis, translate = 0, scale2 = 1, origin = 0.5, boxScale, originAxis = axis, sourceAxis = axis) {
    if (percent.test(translate)) {
      translate = parseFloat(translate);
      const relativeProgress = mixNumber$1(sourceAxis.min, sourceAxis.max, translate / 100);
      translate = relativeProgress - sourceAxis.min;
    }
    if (typeof translate !== "number")
      return;
    let originPoint = mixNumber$1(originAxis.min, originAxis.max, origin);
    if (axis === originAxis)
      originPoint -= translate;
    axis.min = removePointDelta(axis.min, translate, scale2, originPoint, boxScale);
    axis.max = removePointDelta(axis.max, translate, scale2, originPoint, boxScale);
  }
  function removeAxisTransforms(axis, transforms, [key, scaleKey, originKey], origin, sourceAxis) {
    removeAxisDelta(axis, transforms[key], transforms[scaleKey], transforms[originKey], transforms.scale, origin, sourceAxis);
  }
  const xKeys = ["x", "scaleX", "originX"];
  const yKeys = ["y", "scaleY", "originY"];
  function removeBoxTransforms(box, transforms, originBox, sourceBox) {
    removeAxisTransforms(box.x, transforms, xKeys, originBox ? originBox.x : void 0, sourceBox ? sourceBox.x : void 0);
    removeAxisTransforms(box.y, transforms, yKeys, originBox ? originBox.y : void 0, sourceBox ? sourceBox.y : void 0);
  }
  function isAxisDeltaZero(delta) {
    return delta.translate === 0 && delta.scale === 1;
  }
  function isDeltaZero(delta) {
    return isAxisDeltaZero(delta.x) && isAxisDeltaZero(delta.y);
  }
  function boxEquals(a, b2) {
    return a.x.min === b2.x.min && a.x.max === b2.x.max && a.y.min === b2.y.min && a.y.max === b2.y.max;
  }
  function boxEqualsRounded(a, b2) {
    return Math.round(a.x.min) === Math.round(b2.x.min) && Math.round(a.x.max) === Math.round(b2.x.max) && Math.round(a.y.min) === Math.round(b2.y.min) && Math.round(a.y.max) === Math.round(b2.y.max);
  }
  function aspectRatio(box) {
    return calcLength(box.x) / calcLength(box.y);
  }
  class NodeStack {
    constructor() {
      this.members = [];
    }
    add(node2) {
      addUniqueItem(this.members, node2);
      node2.scheduleRender();
    }
    remove(node2) {
      removeItem(this.members, node2);
      if (node2 === this.prevLead) {
        this.prevLead = void 0;
      }
      if (node2 === this.lead) {
        const prevLead = this.members[this.members.length - 1];
        if (prevLead) {
          this.promote(prevLead);
        }
      }
    }
    relegate(node2) {
      const indexOfNode = this.members.findIndex((member) => node2 === member);
      if (indexOfNode === 0)
        return false;
      let prevLead;
      for (let i = indexOfNode; i >= 0; i--) {
        const member = this.members[i];
        if (member.isPresent !== false) {
          prevLead = member;
          break;
        }
      }
      if (prevLead) {
        this.promote(prevLead);
        return true;
      } else {
        return false;
      }
    }
    promote(node2, preserveFollowOpacity) {
      const prevLead = this.lead;
      if (node2 === prevLead)
        return;
      this.prevLead = prevLead;
      this.lead = node2;
      node2.show();
      if (prevLead) {
        prevLead.instance && prevLead.scheduleRender();
        node2.scheduleRender();
        node2.resumeFrom = prevLead;
        if (preserveFollowOpacity) {
          node2.resumeFrom.preserveOpacity = true;
        }
        if (prevLead.snapshot) {
          node2.snapshot = prevLead.snapshot;
          node2.snapshot.latestValues = prevLead.animationValues || prevLead.latestValues;
        }
        if (node2.root && node2.root.isUpdating) {
          node2.isLayoutDirty = true;
        }
        const { crossfade } = node2.options;
        if (crossfade === false) {
          prevLead.hide();
        }
      }
    }
    exitAnimationComplete() {
      this.members.forEach((node2) => {
        const { options, resumingFrom } = node2;
        options.onExitComplete && options.onExitComplete();
        if (resumingFrom) {
          resumingFrom.options.onExitComplete && resumingFrom.options.onExitComplete();
        }
      });
    }
    scheduleRender() {
      this.members.forEach((node2) => {
        node2.instance && node2.scheduleRender(false);
      });
    }
    /**
     * Clear any leads that have been removed this render to prevent them from being
     * used in future animations and to prevent memory leaks
     */
    removeLeadSnapshot() {
      if (this.lead && this.lead.snapshot) {
        this.lead.snapshot = void 0;
      }
    }
  }
  function buildProjectionTransform(delta, treeScale, latestTransform) {
    let transform2 = "";
    const xTranslate = delta.x.translate / treeScale.x;
    const yTranslate = delta.y.translate / treeScale.y;
    const zTranslate = (latestTransform === null || latestTransform === void 0 ? void 0 : latestTransform.z) || 0;
    if (xTranslate || yTranslate || zTranslate) {
      transform2 = `translate3d(${xTranslate}px, ${yTranslate}px, ${zTranslate}px) `;
    }
    if (treeScale.x !== 1 || treeScale.y !== 1) {
      transform2 += `scale(${1 / treeScale.x}, ${1 / treeScale.y}) `;
    }
    if (latestTransform) {
      const { transformPerspective, rotate, rotateX, rotateY, skewX, skewY } = latestTransform;
      if (transformPerspective)
        transform2 = `perspective(${transformPerspective}px) ${transform2}`;
      if (rotate)
        transform2 += `rotate(${rotate}deg) `;
      if (rotateX)
        transform2 += `rotateX(${rotateX}deg) `;
      if (rotateY)
        transform2 += `rotateY(${rotateY}deg) `;
      if (skewX)
        transform2 += `skewX(${skewX}deg) `;
      if (skewY)
        transform2 += `skewY(${skewY}deg) `;
    }
    const elementScaleX = delta.x.scale * treeScale.x;
    const elementScaleY = delta.y.scale * treeScale.y;
    if (elementScaleX !== 1 || elementScaleY !== 1) {
      transform2 += `scale(${elementScaleX}, ${elementScaleY})`;
    }
    return transform2 || "none";
  }
  const compareByDepth = (a, b2) => a.depth - b2.depth;
  class FlatTree {
    constructor() {
      this.children = [];
      this.isDirty = false;
    }
    add(child) {
      addUniqueItem(this.children, child);
      this.isDirty = true;
    }
    remove(child) {
      removeItem(this.children, child);
      this.isDirty = true;
    }
    forEach(callback) {
      this.isDirty && this.children.sort(compareByDepth);
      this.isDirty = false;
      this.children.forEach(callback);
    }
  }
  function delay(callback, timeout) {
    const start = time.now();
    const checkElapsed = ({ timestamp }) => {
      const elapsed = timestamp - start;
      if (elapsed >= timeout) {
        cancelFrame(checkElapsed);
        callback(elapsed - timeout);
      }
    };
    frame.read(checkElapsed, true);
    return () => cancelFrame(checkElapsed);
  }
  function record(data) {
    if (window.MotionDebug) {
      window.MotionDebug.record(data);
    }
  }
  function isSVGElement(element) {
    return element instanceof SVGElement && element.tagName !== "svg";
  }
  function animateSingleValue(value, keyframes2, options) {
    const motionValue$1 = isMotionValue(value) ? value : motionValue(value);
    motionValue$1.start(animateMotionValue("", motionValue$1, keyframes2, options));
    return motionValue$1.animation;
  }
  const transformAxes = ["", "X", "Y", "Z"];
  const hiddenVisibility = { visibility: "hidden" };
  const animationTarget = 1e3;
  let id = 0;
  const projectionFrameData = {
    type: "projectionFrame",
    totalNodes: 0,
    resolvedTargetDeltas: 0,
    recalculatedProjection: 0
  };
  function resetDistortingTransform(key, visualElement, values, sharedAnimationValues) {
    const { latestValues } = visualElement;
    if (latestValues[key]) {
      values[key] = latestValues[key];
      visualElement.setStaticValue(key, 0);
      if (sharedAnimationValues) {
        sharedAnimationValues[key] = 0;
      }
    }
  }
  function createProjectionNode({ attachResizeListener, defaultParent, measureScroll, checkIsScrollRoot, resetTransform }) {
    return class ProjectionNode {
      constructor(latestValues = {}, parent = defaultParent === null || defaultParent === void 0 ? void 0 : defaultParent()) {
        this.id = id++;
        this.animationId = 0;
        this.children = /* @__PURE__ */ new Set();
        this.options = {};
        this.isTreeAnimating = false;
        this.isAnimationBlocked = false;
        this.isLayoutDirty = false;
        this.isProjectionDirty = false;
        this.isSharedProjectionDirty = false;
        this.isTransformDirty = false;
        this.updateManuallyBlocked = false;
        this.updateBlockedByResize = false;
        this.isUpdating = false;
        this.isSVG = false;
        this.needsReset = false;
        this.shouldResetTransform = false;
        this.treeScale = { x: 1, y: 1 };
        this.eventHandlers = /* @__PURE__ */ new Map();
        this.hasTreeAnimated = false;
        this.updateScheduled = false;
        this.projectionUpdateScheduled = false;
        this.checkUpdateFailed = () => {
          if (this.isUpdating) {
            this.isUpdating = false;
            this.clearAllSnapshots();
          }
        };
        this.updateProjection = () => {
          this.projectionUpdateScheduled = false;
          projectionFrameData.totalNodes = projectionFrameData.resolvedTargetDeltas = projectionFrameData.recalculatedProjection = 0;
          this.nodes.forEach(propagateDirtyNodes);
          this.nodes.forEach(resolveTargetDelta);
          this.nodes.forEach(calcProjection);
          this.nodes.forEach(cleanDirtyNodes);
          record(projectionFrameData);
        };
        this.hasProjected = false;
        this.isVisible = true;
        this.animationProgress = 0;
        this.sharedNodes = /* @__PURE__ */ new Map();
        this.latestValues = latestValues;
        this.root = parent ? parent.root || parent : this;
        this.path = parent ? [...parent.path, parent] : [];
        this.parent = parent;
        this.depth = parent ? parent.depth + 1 : 0;
        for (let i = 0; i < this.path.length; i++) {
          this.path[i].shouldResetTransform = true;
        }
        if (this.root === this)
          this.nodes = new FlatTree();
      }
      addEventListener(name, handler) {
        if (!this.eventHandlers.has(name)) {
          this.eventHandlers.set(name, new SubscriptionManager());
        }
        return this.eventHandlers.get(name).add(handler);
      }
      notifyListeners(name, ...args) {
        const subscriptionManager = this.eventHandlers.get(name);
        subscriptionManager && subscriptionManager.notify(...args);
      }
      hasListeners(name) {
        return this.eventHandlers.has(name);
      }
      /**
       * Lifecycles
       */
      mount(instance, isLayoutDirty = this.root.hasTreeAnimated) {
        if (this.instance)
          return;
        this.isSVG = isSVGElement(instance);
        this.instance = instance;
        const { layoutId, layout: layout2, visualElement } = this.options;
        if (visualElement && !visualElement.current) {
          visualElement.mount(instance);
        }
        this.root.nodes.add(this);
        this.parent && this.parent.children.add(this);
        if (isLayoutDirty && (layout2 || layoutId)) {
          this.isLayoutDirty = true;
        }
        if (attachResizeListener) {
          let cancelDelay;
          const resizeUnblockUpdate = () => this.root.updateBlockedByResize = false;
          attachResizeListener(instance, () => {
            this.root.updateBlockedByResize = true;
            cancelDelay && cancelDelay();
            cancelDelay = delay(resizeUnblockUpdate, 250);
            if (globalProjectionState.hasAnimatedSinceResize) {
              globalProjectionState.hasAnimatedSinceResize = false;
              this.nodes.forEach(finishAnimation);
            }
          });
        }
        if (layoutId) {
          this.root.registerSharedNode(layoutId, this);
        }
        if (this.options.animate !== false && visualElement && (layoutId || layout2)) {
          this.addEventListener("didUpdate", ({ delta, hasLayoutChanged, hasRelativeTargetChanged, layout: newLayout }) => {
            if (this.isTreeAnimationBlocked()) {
              this.target = void 0;
              this.relativeTarget = void 0;
              return;
            }
            const layoutTransition = this.options.transition || visualElement.getDefaultTransition() || defaultLayoutTransition;
            const { onLayoutAnimationStart, onLayoutAnimationComplete } = visualElement.getProps();
            const targetChanged = !this.targetLayout || !boxEqualsRounded(this.targetLayout, newLayout) || hasRelativeTargetChanged;
            const hasOnlyRelativeTargetChanged = !hasLayoutChanged && hasRelativeTargetChanged;
            if (this.options.layoutRoot || this.resumeFrom && this.resumeFrom.instance || hasOnlyRelativeTargetChanged || hasLayoutChanged && (targetChanged || !this.currentAnimation)) {
              if (this.resumeFrom) {
                this.resumingFrom = this.resumeFrom;
                this.resumingFrom.resumingFrom = void 0;
              }
              this.setAnimationOrigin(delta, hasOnlyRelativeTargetChanged);
              const animationOptions = {
                ...getValueTransition(layoutTransition, "layout"),
                onPlay: onLayoutAnimationStart,
                onComplete: onLayoutAnimationComplete
              };
              if (visualElement.shouldReduceMotion || this.options.layoutRoot) {
                animationOptions.delay = 0;
                animationOptions.type = false;
              }
              this.startAnimation(animationOptions);
            } else {
              if (!hasLayoutChanged) {
                finishAnimation(this);
              }
              if (this.isLead() && this.options.onExitComplete) {
                this.options.onExitComplete();
              }
            }
            this.targetLayout = newLayout;
          });
        }
      }
      unmount() {
        this.options.layoutId && this.willUpdate();
        this.root.nodes.remove(this);
        const stack = this.getStack();
        stack && stack.remove(this);
        this.parent && this.parent.children.delete(this);
        this.instance = void 0;
        cancelFrame(this.updateProjection);
      }
      // only on the root
      blockUpdate() {
        this.updateManuallyBlocked = true;
      }
      unblockUpdate() {
        this.updateManuallyBlocked = false;
      }
      isUpdateBlocked() {
        return this.updateManuallyBlocked || this.updateBlockedByResize;
      }
      isTreeAnimationBlocked() {
        return this.isAnimationBlocked || this.parent && this.parent.isTreeAnimationBlocked() || false;
      }
      // Note: currently only running on root node
      startUpdate() {
        if (this.isUpdateBlocked())
          return;
        this.isUpdating = true;
        this.nodes && this.nodes.forEach(resetSkewAndRotation);
        this.animationId++;
      }
      getTransformTemplate() {
        const { visualElement } = this.options;
        return visualElement && visualElement.getProps().transformTemplate;
      }
      willUpdate(shouldNotifyListeners = true) {
        this.root.hasTreeAnimated = true;
        if (this.root.isUpdateBlocked()) {
          this.options.onExitComplete && this.options.onExitComplete();
          return;
        }
        !this.root.isUpdating && this.root.startUpdate();
        if (this.isLayoutDirty)
          return;
        this.isLayoutDirty = true;
        for (let i = 0; i < this.path.length; i++) {
          const node2 = this.path[i];
          node2.shouldResetTransform = true;
          node2.updateScroll("snapshot");
          if (node2.options.layoutRoot) {
            node2.willUpdate(false);
          }
        }
        const { layoutId, layout: layout2 } = this.options;
        if (layoutId === void 0 && !layout2)
          return;
        const transformTemplate2 = this.getTransformTemplate();
        this.prevTransformTemplateValue = transformTemplate2 ? transformTemplate2(this.latestValues, "") : void 0;
        this.updateSnapshot();
        shouldNotifyListeners && this.notifyListeners("willUpdate");
      }
      update() {
        this.updateScheduled = false;
        const updateWasBlocked = this.isUpdateBlocked();
        if (updateWasBlocked) {
          this.unblockUpdate();
          this.clearAllSnapshots();
          this.nodes.forEach(clearMeasurements);
          return;
        }
        if (!this.isUpdating) {
          this.nodes.forEach(clearIsLayoutDirty);
        }
        this.isUpdating = false;
        if (window.HandoffCancelAllAnimations) {
          window.HandoffCancelAllAnimations();
        }
        this.nodes.forEach(resetTransformStyle);
        this.nodes.forEach(updateLayout);
        this.nodes.forEach(notifyLayoutUpdate);
        this.clearAllSnapshots();
        const now2 = time.now();
        frameData.delta = clamp(0, 1e3 / 60, now2 - frameData.timestamp);
        frameData.timestamp = now2;
        frameData.isProcessing = true;
        steps.update.process(frameData);
        steps.preRender.process(frameData);
        steps.render.process(frameData);
        frameData.isProcessing = false;
      }
      didUpdate() {
        if (!this.updateScheduled) {
          this.updateScheduled = true;
          microtask.read(() => this.update());
        }
      }
      clearAllSnapshots() {
        this.nodes.forEach(clearSnapshot);
        this.sharedNodes.forEach(removeLeadSnapshots);
      }
      scheduleUpdateProjection() {
        if (!this.projectionUpdateScheduled) {
          this.projectionUpdateScheduled = true;
          frame.preRender(this.updateProjection, false, true);
        }
      }
      scheduleCheckAfterUnmount() {
        frame.postRender(() => {
          if (this.isLayoutDirty) {
            this.root.didUpdate();
          } else {
            this.root.checkUpdateFailed();
          }
        });
      }
      /**
       * Update measurements
       */
      updateSnapshot() {
        if (this.snapshot || !this.instance)
          return;
        this.snapshot = this.measure();
      }
      updateLayout() {
        if (!this.instance)
          return;
        this.updateScroll();
        if (!(this.options.alwaysMeasureLayout && this.isLead()) && !this.isLayoutDirty) {
          return;
        }
        if (this.resumeFrom && !this.resumeFrom.instance) {
          for (let i = 0; i < this.path.length; i++) {
            const node2 = this.path[i];
            node2.updateScroll();
          }
        }
        const prevLayout = this.layout;
        this.layout = this.measure(false);
        this.layoutCorrected = createBox();
        this.isLayoutDirty = false;
        this.projectionDelta = void 0;
        this.notifyListeners("measure", this.layout.layoutBox);
        const { visualElement } = this.options;
        visualElement && visualElement.notify("LayoutMeasure", this.layout.layoutBox, prevLayout ? prevLayout.layoutBox : void 0);
      }
      updateScroll(phase = "measure") {
        let needsMeasurement = Boolean(this.options.layoutScroll && this.instance);
        if (this.scroll && this.scroll.animationId === this.root.animationId && this.scroll.phase === phase) {
          needsMeasurement = false;
        }
        if (needsMeasurement) {
          this.scroll = {
            animationId: this.root.animationId,
            phase,
            isRoot: checkIsScrollRoot(this.instance),
            offset: measureScroll(this.instance)
          };
        }
      }
      resetTransform() {
        if (!resetTransform)
          return;
        const isResetRequested = this.isLayoutDirty || this.shouldResetTransform;
        const hasProjection = this.projectionDelta && !isDeltaZero(this.projectionDelta);
        const transformTemplate2 = this.getTransformTemplate();
        const transformTemplateValue = transformTemplate2 ? transformTemplate2(this.latestValues, "") : void 0;
        const transformTemplateHasChanged = transformTemplateValue !== this.prevTransformTemplateValue;
        if (isResetRequested && (hasProjection || hasTransform(this.latestValues) || transformTemplateHasChanged)) {
          resetTransform(this.instance, transformTemplateValue);
          this.shouldResetTransform = false;
          this.scheduleRender();
        }
      }
      measure(removeTransform = true) {
        const pageBox = this.measurePageBox();
        let layoutBox = this.removeElementScroll(pageBox);
        if (removeTransform) {
          layoutBox = this.removeTransform(layoutBox);
        }
        roundBox(layoutBox);
        return {
          animationId: this.root.animationId,
          measuredBox: pageBox,
          layoutBox,
          latestValues: {},
          source: this.id
        };
      }
      measurePageBox() {
        const { visualElement } = this.options;
        if (!visualElement)
          return createBox();
        const box = visualElement.measureViewportBox();
        const { scroll: scroll2 } = this.root;
        if (scroll2) {
          translateAxis(box.x, scroll2.offset.x);
          translateAxis(box.y, scroll2.offset.y);
        }
        return box;
      }
      removeElementScroll(box) {
        const boxWithoutScroll = createBox();
        copyBoxInto(boxWithoutScroll, box);
        for (let i = 0; i < this.path.length; i++) {
          const node2 = this.path[i];
          const { scroll: scroll2, options } = node2;
          if (node2 !== this.root && scroll2 && options.layoutScroll) {
            if (scroll2.isRoot) {
              copyBoxInto(boxWithoutScroll, box);
              const { scroll: rootScroll } = this.root;
              if (rootScroll) {
                translateAxis(boxWithoutScroll.x, -rootScroll.offset.x);
                translateAxis(boxWithoutScroll.y, -rootScroll.offset.y);
              }
            }
            translateAxis(boxWithoutScroll.x, scroll2.offset.x);
            translateAxis(boxWithoutScroll.y, scroll2.offset.y);
          }
        }
        return boxWithoutScroll;
      }
      applyTransform(box, transformOnly = false) {
        const withTransforms = createBox();
        copyBoxInto(withTransforms, box);
        for (let i = 0; i < this.path.length; i++) {
          const node2 = this.path[i];
          if (!transformOnly && node2.options.layoutScroll && node2.scroll && node2 !== node2.root) {
            transformBox(withTransforms, {
              x: -node2.scroll.offset.x,
              y: -node2.scroll.offset.y
            });
          }
          if (!hasTransform(node2.latestValues))
            continue;
          transformBox(withTransforms, node2.latestValues);
        }
        if (hasTransform(this.latestValues)) {
          transformBox(withTransforms, this.latestValues);
        }
        return withTransforms;
      }
      removeTransform(box) {
        const boxWithoutTransform = createBox();
        copyBoxInto(boxWithoutTransform, box);
        for (let i = 0; i < this.path.length; i++) {
          const node2 = this.path[i];
          if (!node2.instance)
            continue;
          if (!hasTransform(node2.latestValues))
            continue;
          hasScale(node2.latestValues) && node2.updateSnapshot();
          const sourceBox = createBox();
          const nodeBox = node2.measurePageBox();
          copyBoxInto(sourceBox, nodeBox);
          removeBoxTransforms(boxWithoutTransform, node2.latestValues, node2.snapshot ? node2.snapshot.layoutBox : void 0, sourceBox);
        }
        if (hasTransform(this.latestValues)) {
          removeBoxTransforms(boxWithoutTransform, this.latestValues);
        }
        return boxWithoutTransform;
      }
      setTargetDelta(delta) {
        this.targetDelta = delta;
        this.root.scheduleUpdateProjection();
        this.isProjectionDirty = true;
      }
      setOptions(options) {
        this.options = {
          ...this.options,
          ...options,
          crossfade: options.crossfade !== void 0 ? options.crossfade : true
        };
      }
      clearMeasurements() {
        this.scroll = void 0;
        this.layout = void 0;
        this.snapshot = void 0;
        this.prevTransformTemplateValue = void 0;
        this.targetDelta = void 0;
        this.target = void 0;
        this.isLayoutDirty = false;
      }
      forceRelativeParentToResolveTarget() {
        if (!this.relativeParent)
          return;
        if (this.relativeParent.resolvedRelativeTargetAt !== frameData.timestamp) {
          this.relativeParent.resolveTargetDelta(true);
        }
      }
      resolveTargetDelta(forceRecalculation = false) {
        var _a4;
        const lead = this.getLead();
        this.isProjectionDirty || (this.isProjectionDirty = lead.isProjectionDirty);
        this.isTransformDirty || (this.isTransformDirty = lead.isTransformDirty);
        this.isSharedProjectionDirty || (this.isSharedProjectionDirty = lead.isSharedProjectionDirty);
        const isShared = Boolean(this.resumingFrom) || this !== lead;
        const canSkip = !(forceRecalculation || isShared && this.isSharedProjectionDirty || this.isProjectionDirty || ((_a4 = this.parent) === null || _a4 === void 0 ? void 0 : _a4.isProjectionDirty) || this.attemptToResolveRelativeTarget);
        if (canSkip)
          return;
        const { layout: layout2, layoutId } = this.options;
        if (!this.layout || !(layout2 || layoutId))
          return;
        this.resolvedRelativeTargetAt = frameData.timestamp;
        if (!this.targetDelta && !this.relativeTarget) {
          const relativeParent = this.getClosestProjectingParent();
          if (relativeParent && relativeParent.layout && this.animationProgress !== 1) {
            this.relativeParent = relativeParent;
            this.forceRelativeParentToResolveTarget();
            this.relativeTarget = createBox();
            this.relativeTargetOrigin = createBox();
            calcRelativePosition(this.relativeTargetOrigin, this.layout.layoutBox, relativeParent.layout.layoutBox);
            copyBoxInto(this.relativeTarget, this.relativeTargetOrigin);
          } else {
            this.relativeParent = this.relativeTarget = void 0;
          }
        }
        if (!this.relativeTarget && !this.targetDelta)
          return;
        if (!this.target) {
          this.target = createBox();
          this.targetWithTransforms = createBox();
        }
        if (this.relativeTarget && this.relativeTargetOrigin && this.relativeParent && this.relativeParent.target) {
          this.forceRelativeParentToResolveTarget();
          calcRelativeBox(this.target, this.relativeTarget, this.relativeParent.target);
        } else if (this.targetDelta) {
          if (Boolean(this.resumingFrom)) {
            this.target = this.applyTransform(this.layout.layoutBox);
          } else {
            copyBoxInto(this.target, this.layout.layoutBox);
          }
          applyBoxDelta(this.target, this.targetDelta);
        } else {
          copyBoxInto(this.target, this.layout.layoutBox);
        }
        if (this.attemptToResolveRelativeTarget) {
          this.attemptToResolveRelativeTarget = false;
          const relativeParent = this.getClosestProjectingParent();
          if (relativeParent && Boolean(relativeParent.resumingFrom) === Boolean(this.resumingFrom) && !relativeParent.options.layoutScroll && relativeParent.target && this.animationProgress !== 1) {
            this.relativeParent = relativeParent;
            this.forceRelativeParentToResolveTarget();
            this.relativeTarget = createBox();
            this.relativeTargetOrigin = createBox();
            calcRelativePosition(this.relativeTargetOrigin, this.target, relativeParent.target);
            copyBoxInto(this.relativeTarget, this.relativeTargetOrigin);
          } else {
            this.relativeParent = this.relativeTarget = void 0;
          }
        }
        projectionFrameData.resolvedTargetDeltas++;
      }
      getClosestProjectingParent() {
        if (!this.parent || hasScale(this.parent.latestValues) || has2DTranslate(this.parent.latestValues)) {
          return void 0;
        }
        if (this.parent.isProjecting()) {
          return this.parent;
        } else {
          return this.parent.getClosestProjectingParent();
        }
      }
      isProjecting() {
        return Boolean((this.relativeTarget || this.targetDelta || this.options.layoutRoot) && this.layout);
      }
      calcProjection() {
        var _a4;
        const lead = this.getLead();
        const isShared = Boolean(this.resumingFrom) || this !== lead;
        let canSkip = true;
        if (this.isProjectionDirty || ((_a4 = this.parent) === null || _a4 === void 0 ? void 0 : _a4.isProjectionDirty)) {
          canSkip = false;
        }
        if (isShared && (this.isSharedProjectionDirty || this.isTransformDirty)) {
          canSkip = false;
        }
        if (this.resolvedRelativeTargetAt === frameData.timestamp) {
          canSkip = false;
        }
        if (canSkip)
          return;
        const { layout: layout2, layoutId } = this.options;
        this.isTreeAnimating = Boolean(this.parent && this.parent.isTreeAnimating || this.currentAnimation || this.pendingAnimation);
        if (!this.isTreeAnimating) {
          this.targetDelta = this.relativeTarget = void 0;
        }
        if (!this.layout || !(layout2 || layoutId))
          return;
        copyBoxInto(this.layoutCorrected, this.layout.layoutBox);
        const prevTreeScaleX = this.treeScale.x;
        const prevTreeScaleY = this.treeScale.y;
        applyTreeDeltas(this.layoutCorrected, this.treeScale, this.path, isShared);
        if (lead.layout && !lead.target && (this.treeScale.x !== 1 || this.treeScale.y !== 1)) {
          lead.target = lead.layout.layoutBox;
          lead.targetWithTransforms = createBox();
        }
        const { target } = lead;
        if (!target) {
          if (this.projectionTransform) {
            this.projectionDelta = createDelta();
            this.projectionTransform = "none";
            this.scheduleRender();
          }
          return;
        }
        if (!this.projectionDelta) {
          this.projectionDelta = createDelta();
          this.projectionDeltaWithTransform = createDelta();
        }
        const prevProjectionTransform = this.projectionTransform;
        calcBoxDelta(this.projectionDelta, this.layoutCorrected, target, this.latestValues);
        this.projectionTransform = buildProjectionTransform(this.projectionDelta, this.treeScale);
        if (this.projectionTransform !== prevProjectionTransform || this.treeScale.x !== prevTreeScaleX || this.treeScale.y !== prevTreeScaleY) {
          this.hasProjected = true;
          this.scheduleRender();
          this.notifyListeners("projectionUpdate", target);
        }
        projectionFrameData.recalculatedProjection++;
      }
      hide() {
        this.isVisible = false;
      }
      show() {
        this.isVisible = true;
      }
      scheduleRender(notifyAll = true) {
        this.options.scheduleRender && this.options.scheduleRender();
        if (notifyAll) {
          const stack = this.getStack();
          stack && stack.scheduleRender();
        }
        if (this.resumingFrom && !this.resumingFrom.instance) {
          this.resumingFrom = void 0;
        }
      }
      setAnimationOrigin(delta, hasOnlyRelativeTargetChanged = false) {
        const snapshot = this.snapshot;
        const snapshotLatestValues = snapshot ? snapshot.latestValues : {};
        const mixedValues = { ...this.latestValues };
        const targetDelta = createDelta();
        if (!this.relativeParent || !this.relativeParent.options.layoutRoot) {
          this.relativeTarget = this.relativeTargetOrigin = void 0;
        }
        this.attemptToResolveRelativeTarget = !hasOnlyRelativeTargetChanged;
        const relativeLayout = createBox();
        const snapshotSource = snapshot ? snapshot.source : void 0;
        const layoutSource = this.layout ? this.layout.source : void 0;
        const isSharedLayoutAnimation = snapshotSource !== layoutSource;
        const stack = this.getStack();
        const isOnlyMember = !stack || stack.members.length <= 1;
        const shouldCrossfadeOpacity = Boolean(isSharedLayoutAnimation && !isOnlyMember && this.options.crossfade === true && !this.path.some(hasOpacityCrossfade));
        this.animationProgress = 0;
        let prevRelativeTarget;
        this.mixTargetDelta = (latest) => {
          const progress2 = latest / 1e3;
          mixAxisDelta(targetDelta.x, delta.x, progress2);
          mixAxisDelta(targetDelta.y, delta.y, progress2);
          this.setTargetDelta(targetDelta);
          if (this.relativeTarget && this.relativeTargetOrigin && this.layout && this.relativeParent && this.relativeParent.layout) {
            calcRelativePosition(relativeLayout, this.layout.layoutBox, this.relativeParent.layout.layoutBox);
            mixBox(this.relativeTarget, this.relativeTargetOrigin, relativeLayout, progress2);
            if (prevRelativeTarget && boxEquals(this.relativeTarget, prevRelativeTarget)) {
              this.isProjectionDirty = false;
            }
            if (!prevRelativeTarget)
              prevRelativeTarget = createBox();
            copyBoxInto(prevRelativeTarget, this.relativeTarget);
          }
          if (isSharedLayoutAnimation) {
            this.animationValues = mixedValues;
            mixValues(mixedValues, snapshotLatestValues, this.latestValues, progress2, shouldCrossfadeOpacity, isOnlyMember);
          }
          this.root.scheduleUpdateProjection();
          this.scheduleRender();
          this.animationProgress = progress2;
        };
        this.mixTargetDelta(this.options.layoutRoot ? 1e3 : 0);
      }
      startAnimation(options) {
        this.notifyListeners("animationStart");
        this.currentAnimation && this.currentAnimation.stop();
        if (this.resumingFrom && this.resumingFrom.currentAnimation) {
          this.resumingFrom.currentAnimation.stop();
        }
        if (this.pendingAnimation) {
          cancelFrame(this.pendingAnimation);
          this.pendingAnimation = void 0;
        }
        this.pendingAnimation = frame.update(() => {
          globalProjectionState.hasAnimatedSinceResize = true;
          this.currentAnimation = animateSingleValue(0, animationTarget, {
            ...options,
            onUpdate: (latest) => {
              this.mixTargetDelta(latest);
              options.onUpdate && options.onUpdate(latest);
            },
            onComplete: () => {
              options.onComplete && options.onComplete();
              this.completeAnimation();
            }
          });
          if (this.resumingFrom) {
            this.resumingFrom.currentAnimation = this.currentAnimation;
          }
          this.pendingAnimation = void 0;
        });
      }
      completeAnimation() {
        if (this.resumingFrom) {
          this.resumingFrom.currentAnimation = void 0;
          this.resumingFrom.preserveOpacity = void 0;
        }
        const stack = this.getStack();
        stack && stack.exitAnimationComplete();
        this.resumingFrom = this.currentAnimation = this.animationValues = void 0;
        this.notifyListeners("animationComplete");
      }
      finishAnimation() {
        if (this.currentAnimation) {
          this.mixTargetDelta && this.mixTargetDelta(animationTarget);
          this.currentAnimation.stop();
        }
        this.completeAnimation();
      }
      applyTransformsToTarget() {
        const lead = this.getLead();
        let { targetWithTransforms, target, layout: layout2, latestValues } = lead;
        if (!targetWithTransforms || !target || !layout2)
          return;
        if (this !== lead && this.layout && layout2 && shouldAnimatePositionOnly(this.options.animationType, this.layout.layoutBox, layout2.layoutBox)) {
          target = this.target || createBox();
          const xLength = calcLength(this.layout.layoutBox.x);
          target.x.min = lead.target.x.min;
          target.x.max = target.x.min + xLength;
          const yLength = calcLength(this.layout.layoutBox.y);
          target.y.min = lead.target.y.min;
          target.y.max = target.y.min + yLength;
        }
        copyBoxInto(targetWithTransforms, target);
        transformBox(targetWithTransforms, latestValues);
        calcBoxDelta(this.projectionDeltaWithTransform, this.layoutCorrected, targetWithTransforms, latestValues);
      }
      registerSharedNode(layoutId, node2) {
        if (!this.sharedNodes.has(layoutId)) {
          this.sharedNodes.set(layoutId, new NodeStack());
        }
        const stack = this.sharedNodes.get(layoutId);
        stack.add(node2);
        const config2 = node2.options.initialPromotionConfig;
        node2.promote({
          transition: config2 ? config2.transition : void 0,
          preserveFollowOpacity: config2 && config2.shouldPreserveFollowOpacity ? config2.shouldPreserveFollowOpacity(node2) : void 0
        });
      }
      isLead() {
        const stack = this.getStack();
        return stack ? stack.lead === this : true;
      }
      getLead() {
        var _a4;
        const { layoutId } = this.options;
        return layoutId ? ((_a4 = this.getStack()) === null || _a4 === void 0 ? void 0 : _a4.lead) || this : this;
      }
      getPrevLead() {
        var _a4;
        const { layoutId } = this.options;
        return layoutId ? (_a4 = this.getStack()) === null || _a4 === void 0 ? void 0 : _a4.prevLead : void 0;
      }
      getStack() {
        const { layoutId } = this.options;
        if (layoutId)
          return this.root.sharedNodes.get(layoutId);
      }
      promote({ needsReset, transition: transition2, preserveFollowOpacity } = {}) {
        const stack = this.getStack();
        if (stack)
          stack.promote(this, preserveFollowOpacity);
        if (needsReset) {
          this.projectionDelta = void 0;
          this.needsReset = true;
        }
        if (transition2)
          this.setOptions({ transition: transition2 });
      }
      relegate() {
        const stack = this.getStack();
        if (stack) {
          return stack.relegate(this);
        } else {
          return false;
        }
      }
      resetSkewAndRotation() {
        const { visualElement } = this.options;
        if (!visualElement)
          return;
        let hasDistortingTransform = false;
        const { latestValues } = visualElement;
        if (latestValues.z || latestValues.rotate || latestValues.rotateX || latestValues.rotateY || latestValues.rotateZ || latestValues.skewX || latestValues.skewY) {
          hasDistortingTransform = true;
        }
        if (!hasDistortingTransform)
          return;
        const resetValues = {};
        if (latestValues.z) {
          resetDistortingTransform("z", visualElement, resetValues, this.animationValues);
        }
        for (let i = 0; i < transformAxes.length; i++) {
          resetDistortingTransform(`rotate${transformAxes[i]}`, visualElement, resetValues, this.animationValues);
          resetDistortingTransform(`skew${transformAxes[i]}`, visualElement, resetValues, this.animationValues);
        }
        visualElement.render();
        for (const key in resetValues) {
          visualElement.setStaticValue(key, resetValues[key]);
          if (this.animationValues) {
            this.animationValues[key] = resetValues[key];
          }
        }
        visualElement.scheduleRender();
      }
      getProjectionStyles(styleProp) {
        var _a4, _b3;
        if (!this.instance || this.isSVG)
          return void 0;
        if (!this.isVisible) {
          return hiddenVisibility;
        }
        const styles2 = {
          visibility: ""
        };
        const transformTemplate2 = this.getTransformTemplate();
        if (this.needsReset) {
          this.needsReset = false;
          styles2.opacity = "";
          styles2.pointerEvents = resolveMotionValue(styleProp === null || styleProp === void 0 ? void 0 : styleProp.pointerEvents) || "";
          styles2.transform = transformTemplate2 ? transformTemplate2(this.latestValues, "") : "none";
          return styles2;
        }
        const lead = this.getLead();
        if (!this.projectionDelta || !this.layout || !lead.target) {
          const emptyStyles = {};
          if (this.options.layoutId) {
            emptyStyles.opacity = this.latestValues.opacity !== void 0 ? this.latestValues.opacity : 1;
            emptyStyles.pointerEvents = resolveMotionValue(styleProp === null || styleProp === void 0 ? void 0 : styleProp.pointerEvents) || "";
          }
          if (this.hasProjected && !hasTransform(this.latestValues)) {
            emptyStyles.transform = transformTemplate2 ? transformTemplate2({}, "") : "none";
            this.hasProjected = false;
          }
          return emptyStyles;
        }
        const valuesToRender = lead.animationValues || lead.latestValues;
        this.applyTransformsToTarget();
        styles2.transform = buildProjectionTransform(this.projectionDeltaWithTransform, this.treeScale, valuesToRender);
        if (transformTemplate2) {
          styles2.transform = transformTemplate2(valuesToRender, styles2.transform);
        }
        const { x: x2, y: y2 } = this.projectionDelta;
        styles2.transformOrigin = `${x2.origin * 100}% ${y2.origin * 100}% 0`;
        if (lead.animationValues) {
          styles2.opacity = lead === this ? (_b3 = (_a4 = valuesToRender.opacity) !== null && _a4 !== void 0 ? _a4 : this.latestValues.opacity) !== null && _b3 !== void 0 ? _b3 : 1 : this.preserveOpacity ? this.latestValues.opacity : valuesToRender.opacityExit;
        } else {
          styles2.opacity = lead === this ? valuesToRender.opacity !== void 0 ? valuesToRender.opacity : "" : valuesToRender.opacityExit !== void 0 ? valuesToRender.opacityExit : 0;
        }
        for (const key in scaleCorrectors) {
          if (valuesToRender[key] === void 0)
            continue;
          const { correct, applyTo } = scaleCorrectors[key];
          const corrected = styles2.transform === "none" ? valuesToRender[key] : correct(valuesToRender[key], lead);
          if (applyTo) {
            const num = applyTo.length;
            for (let i = 0; i < num; i++) {
              styles2[applyTo[i]] = corrected;
            }
          } else {
            styles2[key] = corrected;
          }
        }
        if (this.options.layoutId) {
          styles2.pointerEvents = lead === this ? resolveMotionValue(styleProp === null || styleProp === void 0 ? void 0 : styleProp.pointerEvents) || "" : "none";
        }
        return styles2;
      }
      clearSnapshot() {
        this.resumeFrom = this.snapshot = void 0;
      }
      // Only run on root
      resetTree() {
        this.root.nodes.forEach((node2) => {
          var _a4;
          return (_a4 = node2.currentAnimation) === null || _a4 === void 0 ? void 0 : _a4.stop();
        });
        this.root.nodes.forEach(clearMeasurements);
        this.root.sharedNodes.clear();
      }
    };
  }
  function updateLayout(node2) {
    node2.updateLayout();
  }
  function notifyLayoutUpdate(node2) {
    var _a4;
    const snapshot = ((_a4 = node2.resumeFrom) === null || _a4 === void 0 ? void 0 : _a4.snapshot) || node2.snapshot;
    if (node2.isLead() && node2.layout && snapshot && node2.hasListeners("didUpdate")) {
      const { layoutBox: layout2, measuredBox: measuredLayout } = node2.layout;
      const { animationType } = node2.options;
      const isShared = snapshot.source !== node2.layout.source;
      if (animationType === "size") {
        eachAxis((axis) => {
          const axisSnapshot = isShared ? snapshot.measuredBox[axis] : snapshot.layoutBox[axis];
          const length2 = calcLength(axisSnapshot);
          axisSnapshot.min = layout2[axis].min;
          axisSnapshot.max = axisSnapshot.min + length2;
        });
      } else if (shouldAnimatePositionOnly(animationType, snapshot.layoutBox, layout2)) {
        eachAxis((axis) => {
          const axisSnapshot = isShared ? snapshot.measuredBox[axis] : snapshot.layoutBox[axis];
          const length2 = calcLength(layout2[axis]);
          axisSnapshot.max = axisSnapshot.min + length2;
          if (node2.relativeTarget && !node2.currentAnimation) {
            node2.isProjectionDirty = true;
            node2.relativeTarget[axis].max = node2.relativeTarget[axis].min + length2;
          }
        });
      }
      const layoutDelta = createDelta();
      calcBoxDelta(layoutDelta, layout2, snapshot.layoutBox);
      const visualDelta = createDelta();
      if (isShared) {
        calcBoxDelta(visualDelta, node2.applyTransform(measuredLayout, true), snapshot.measuredBox);
      } else {
        calcBoxDelta(visualDelta, layout2, snapshot.layoutBox);
      }
      const hasLayoutChanged = !isDeltaZero(layoutDelta);
      let hasRelativeTargetChanged = false;
      if (!node2.resumeFrom) {
        const relativeParent = node2.getClosestProjectingParent();
        if (relativeParent && !relativeParent.resumeFrom) {
          const { snapshot: parentSnapshot, layout: parentLayout } = relativeParent;
          if (parentSnapshot && parentLayout) {
            const relativeSnapshot = createBox();
            calcRelativePosition(relativeSnapshot, snapshot.layoutBox, parentSnapshot.layoutBox);
            const relativeLayout = createBox();
            calcRelativePosition(relativeLayout, layout2, parentLayout.layoutBox);
            if (!boxEqualsRounded(relativeSnapshot, relativeLayout)) {
              hasRelativeTargetChanged = true;
            }
            if (relativeParent.options.layoutRoot) {
              node2.relativeTarget = relativeLayout;
              node2.relativeTargetOrigin = relativeSnapshot;
              node2.relativeParent = relativeParent;
            }
          }
        }
      }
      node2.notifyListeners("didUpdate", {
        layout: layout2,
        snapshot,
        delta: visualDelta,
        layoutDelta,
        hasLayoutChanged,
        hasRelativeTargetChanged
      });
    } else if (node2.isLead()) {
      const { onExitComplete } = node2.options;
      onExitComplete && onExitComplete();
    }
    node2.options.transition = void 0;
  }
  function propagateDirtyNodes(node2) {
    projectionFrameData.totalNodes++;
    if (!node2.parent)
      return;
    if (!node2.isProjecting()) {
      node2.isProjectionDirty = node2.parent.isProjectionDirty;
    }
    node2.isSharedProjectionDirty || (node2.isSharedProjectionDirty = Boolean(node2.isProjectionDirty || node2.parent.isProjectionDirty || node2.parent.isSharedProjectionDirty));
    node2.isTransformDirty || (node2.isTransformDirty = node2.parent.isTransformDirty);
  }
  function cleanDirtyNodes(node2) {
    node2.isProjectionDirty = node2.isSharedProjectionDirty = node2.isTransformDirty = false;
  }
  function clearSnapshot(node2) {
    node2.clearSnapshot();
  }
  function clearMeasurements(node2) {
    node2.clearMeasurements();
  }
  function clearIsLayoutDirty(node2) {
    node2.isLayoutDirty = false;
  }
  function resetTransformStyle(node2) {
    const { visualElement } = node2.options;
    if (visualElement && visualElement.getProps().onBeforeLayoutMeasure) {
      visualElement.notify("BeforeLayoutMeasure");
    }
    node2.resetTransform();
  }
  function finishAnimation(node2) {
    node2.finishAnimation();
    node2.targetDelta = node2.relativeTarget = node2.target = void 0;
    node2.isProjectionDirty = true;
  }
  function resolveTargetDelta(node2) {
    node2.resolveTargetDelta();
  }
  function calcProjection(node2) {
    node2.calcProjection();
  }
  function resetSkewAndRotation(node2) {
    node2.resetSkewAndRotation();
  }
  function removeLeadSnapshots(stack) {
    stack.removeLeadSnapshot();
  }
  function mixAxisDelta(output, delta, p2) {
    output.translate = mixNumber$1(delta.translate, 0, p2);
    output.scale = mixNumber$1(delta.scale, 1, p2);
    output.origin = delta.origin;
    output.originPoint = delta.originPoint;
  }
  function mixAxis(output, from2, to, p2) {
    output.min = mixNumber$1(from2.min, to.min, p2);
    output.max = mixNumber$1(from2.max, to.max, p2);
  }
  function mixBox(output, from2, to, p2) {
    mixAxis(output.x, from2.x, to.x, p2);
    mixAxis(output.y, from2.y, to.y, p2);
  }
  function hasOpacityCrossfade(node2) {
    return node2.animationValues && node2.animationValues.opacityExit !== void 0;
  }
  const defaultLayoutTransition = {
    duration: 0.45,
    ease: [0.4, 0, 0.1, 1]
  };
  const userAgentContains = (string) => typeof navigator !== "undefined" && navigator.userAgent && navigator.userAgent.toLowerCase().includes(string);
  const roundPoint = userAgentContains("applewebkit/") && !userAgentContains("chrome/") ? Math.round : noop;
  function roundAxis(axis) {
    axis.min = roundPoint(axis.min);
    axis.max = roundPoint(axis.max);
  }
  function roundBox(box) {
    roundAxis(box.x);
    roundAxis(box.y);
  }
  function shouldAnimatePositionOnly(animationType, snapshot, layout2) {
    return animationType === "position" || animationType === "preserve-aspect" && !isNear(aspectRatio(snapshot), aspectRatio(layout2), 0.2);
  }
  const DocumentProjectionNode = createProjectionNode({
    attachResizeListener: (ref, notify) => addDomEvent(ref, "resize", notify),
    measureScroll: () => ({
      x: document.documentElement.scrollLeft || document.body.scrollLeft,
      y: document.documentElement.scrollTop || document.body.scrollTop
    }),
    checkIsScrollRoot: () => true
  });
  const rootProjectionNode = {
    current: void 0
  };
  const HTMLProjectionNode = createProjectionNode({
    measureScroll: (instance) => ({
      x: instance.scrollLeft,
      y: instance.scrollTop
    }),
    defaultParent: () => {
      if (!rootProjectionNode.current) {
        const documentNode = new DocumentProjectionNode({});
        documentNode.mount(window);
        documentNode.setOptions({ layoutScroll: true });
        rootProjectionNode.current = documentNode;
      }
      return rootProjectionNode.current;
    },
    resetTransform: (instance, value) => {
      instance.style.transform = value !== void 0 ? value : "none";
    },
    checkIsScrollRoot: (instance) => Boolean(window.getComputedStyle(instance).position === "fixed")
  });
  const drag = {
    pan: {
      Feature: PanGesture
    },
    drag: {
      Feature: DragGesture,
      ProjectionNode: HTMLProjectionNode,
      MeasureLayout
    }
  };
  const prefersReducedMotion = { current: null };
  const hasReducedMotionListener = { current: false };
  function initPrefersReducedMotion() {
    hasReducedMotionListener.current = true;
    if (!isBrowser)
      return;
    if (window.matchMedia) {
      const motionMediaQuery = window.matchMedia("(prefers-reduced-motion)");
      const setReducedMotionPreferences = () => prefersReducedMotion.current = motionMediaQuery.matches;
      motionMediaQuery.addListener(setReducedMotionPreferences);
      setReducedMotionPreferences();
    } else {
      prefersReducedMotion.current = false;
    }
  }
  function updateMotionValuesFromProps(element, next2, prev2) {
    const { willChange } = next2;
    for (const key in next2) {
      const nextValue = next2[key];
      const prevValue = prev2[key];
      if (isMotionValue(nextValue)) {
        element.addValue(key, nextValue);
        if (isWillChangeMotionValue(willChange)) {
          willChange.add(key);
        }
      } else if (isMotionValue(prevValue)) {
        element.addValue(key, motionValue(nextValue, { owner: element }));
        if (isWillChangeMotionValue(willChange)) {
          willChange.remove(key);
        }
      } else if (prevValue !== nextValue) {
        if (element.hasValue(key)) {
          const existingValue = element.getValue(key);
          if (existingValue.liveStyle === true) {
            existingValue.jump(nextValue);
          } else if (!existingValue.hasAnimated) {
            existingValue.set(nextValue);
          }
        } else {
          const latestValue = element.getStaticValue(key);
          element.addValue(key, motionValue(latestValue !== void 0 ? latestValue : nextValue, { owner: element }));
        }
      }
    }
    for (const key in prev2) {
      if (next2[key] === void 0)
        element.removeValue(key);
    }
    return next2;
  }
  const visualElementStore = /* @__PURE__ */ new WeakMap();
  const valueTypes = [...dimensionValueTypes, color, complex];
  const findValueType = (v2) => valueTypes.find(testValueType(v2));
  const featureNames = Object.keys(featureDefinitions);
  const numFeatures = featureNames.length;
  const propEventHandlers = [
    "AnimationStart",
    "AnimationComplete",
    "Update",
    "BeforeLayoutMeasure",
    "LayoutMeasure",
    "LayoutAnimationStart",
    "LayoutAnimationComplete"
  ];
  const numVariantProps = variantProps.length;
  function getClosestProjectingNode(visualElement) {
    if (!visualElement)
      return void 0;
    return visualElement.options.allowProjection !== false ? visualElement.projection : getClosestProjectingNode(visualElement.parent);
  }
  class VisualElement {
    /**
     * This method takes React props and returns found MotionValues. For example, HTML
     * MotionValues will be found within the style prop, whereas for Three.js within attribute arrays.
     *
     * This isn't an abstract method as it needs calling in the constructor, but it is
     * intended to be one.
     */
    scrapeMotionValuesFromProps(_props, _prevProps, _visualElement) {
      return {};
    }
    constructor({ parent, props, presenceContext, reducedMotionConfig, blockInitialAnimation, visualState }, options = {}) {
      this.resolveKeyframes = (keyframes2, onComplete, name, value) => {
        return new this.KeyframeResolver(keyframes2, onComplete, name, value, this);
      };
      this.current = null;
      this.children = /* @__PURE__ */ new Set();
      this.isVariantNode = false;
      this.isControllingVariants = false;
      this.shouldReduceMotion = null;
      this.values = /* @__PURE__ */ new Map();
      this.KeyframeResolver = KeyframeResolver;
      this.features = {};
      this.valueSubscriptions = /* @__PURE__ */ new Map();
      this.prevMotionValues = {};
      this.events = {};
      this.propEventSubscriptions = {};
      this.notifyUpdate = () => this.notify("Update", this.latestValues);
      this.render = () => {
        if (!this.current)
          return;
        this.triggerBuild();
        this.renderInstance(this.current, this.renderState, this.props.style, this.projection);
      };
      this.scheduleRender = () => frame.render(this.render, false, true);
      const { latestValues, renderState } = visualState;
      this.latestValues = latestValues;
      this.baseTarget = { ...latestValues };
      this.initialValues = props.initial ? { ...latestValues } : {};
      this.renderState = renderState;
      this.parent = parent;
      this.props = props;
      this.presenceContext = presenceContext;
      this.depth = parent ? parent.depth + 1 : 0;
      this.reducedMotionConfig = reducedMotionConfig;
      this.options = options;
      this.blockInitialAnimation = Boolean(blockInitialAnimation);
      this.isControllingVariants = isControllingVariants(props);
      this.isVariantNode = isVariantNode(props);
      if (this.isVariantNode) {
        this.variantChildren = /* @__PURE__ */ new Set();
      }
      this.manuallyAnimateOnMount = Boolean(parent && parent.current);
      const { willChange, ...initialMotionValues } = this.scrapeMotionValuesFromProps(props, {}, this);
      for (const key in initialMotionValues) {
        const value = initialMotionValues[key];
        if (latestValues[key] !== void 0 && isMotionValue(value)) {
          value.set(latestValues[key], false);
          if (isWillChangeMotionValue(willChange)) {
            willChange.add(key);
          }
        }
      }
    }
    mount(instance) {
      this.current = instance;
      visualElementStore.set(instance, this);
      if (this.projection && !this.projection.instance) {
        this.projection.mount(instance);
      }
      if (this.parent && this.isVariantNode && !this.isControllingVariants) {
        this.removeFromVariantTree = this.parent.addVariantChild(this);
      }
      this.values.forEach((value, key) => this.bindToMotionValue(key, value));
      if (!hasReducedMotionListener.current) {
        initPrefersReducedMotion();
      }
      this.shouldReduceMotion = this.reducedMotionConfig === "never" ? false : this.reducedMotionConfig === "always" ? true : prefersReducedMotion.current;
      if (this.parent)
        this.parent.children.add(this);
      this.update(this.props, this.presenceContext);
    }
    unmount() {
      var _a4;
      visualElementStore.delete(this.current);
      this.projection && this.projection.unmount();
      cancelFrame(this.notifyUpdate);
      cancelFrame(this.render);
      this.valueSubscriptions.forEach((remove) => remove());
      this.removeFromVariantTree && this.removeFromVariantTree();
      this.parent && this.parent.children.delete(this);
      for (const key in this.events) {
        this.events[key].clear();
      }
      for (const key in this.features) {
        (_a4 = this.features[key]) === null || _a4 === void 0 ? void 0 : _a4.unmount();
      }
      this.current = null;
    }
    bindToMotionValue(key, value) {
      const valueIsTransform = transformProps.has(key);
      const removeOnChange = value.on("change", (latestValue) => {
        this.latestValues[key] = latestValue;
        this.props.onUpdate && frame.preRender(this.notifyUpdate);
        if (valueIsTransform && this.projection) {
          this.projection.isTransformDirty = true;
        }
      });
      const removeOnRenderRequest = value.on("renderRequest", this.scheduleRender);
      this.valueSubscriptions.set(key, () => {
        removeOnChange();
        removeOnRenderRequest();
        if (value.owner)
          value.stop();
      });
    }
    sortNodePosition(other) {
      if (!this.current || !this.sortInstanceNodePosition || this.type !== other.type) {
        return 0;
      }
      return this.sortInstanceNodePosition(this.current, other.current);
    }
    loadFeatures({ children, ...renderedProps }, isStrict, preloadedFeatures2, initialLayoutGroupConfig) {
      let ProjectionNodeConstructor;
      let MeasureLayout2;
      for (let i = 0; i < numFeatures; i++) {
        const name = featureNames[i];
        const { isEnabled, Feature: FeatureConstructor, ProjectionNode, MeasureLayout: MeasureLayoutComponent } = featureDefinitions[name];
        if (ProjectionNode)
          ProjectionNodeConstructor = ProjectionNode;
        if (isEnabled(renderedProps)) {
          if (!this.features[name] && FeatureConstructor) {
            this.features[name] = new FeatureConstructor(this);
          }
          if (MeasureLayoutComponent) {
            MeasureLayout2 = MeasureLayoutComponent;
          }
        }
      }
      if ((this.type === "html" || this.type === "svg") && !this.projection && ProjectionNodeConstructor) {
        this.projection = new ProjectionNodeConstructor(this.latestValues, getClosestProjectingNode(this.parent));
        const { layoutId, layout: layout2, drag: drag2, dragConstraints, layoutScroll, layoutRoot } = renderedProps;
        this.projection.setOptions({
          layoutId,
          layout: layout2,
          alwaysMeasureLayout: Boolean(drag2) || dragConstraints && isRefObject(dragConstraints),
          visualElement: this,
          scheduleRender: () => this.scheduleRender(),
          /**
           * TODO: Update options in an effect. This could be tricky as it'll be too late
           * to update by the time layout animations run.
           * We also need to fix this safeToRemove by linking it up to the one returned by usePresence,
           * ensuring it gets called if there's no potential layout animations.
           *
           */
          animationType: typeof layout2 === "string" ? layout2 : "both",
          initialPromotionConfig: initialLayoutGroupConfig,
          layoutScroll,
          layoutRoot
        });
      }
      return MeasureLayout2;
    }
    updateFeatures() {
      for (const key in this.features) {
        const feature = this.features[key];
        if (feature.isMounted) {
          feature.update();
        } else {
          feature.mount();
          feature.isMounted = true;
        }
      }
    }
    triggerBuild() {
      this.build(this.renderState, this.latestValues, this.options, this.props);
    }
    /**
     * Measure the current viewport box with or without transforms.
     * Only measures axis-aligned boxes, rotate and skew must be manually
     * removed with a re-render to work.
     */
    measureViewportBox() {
      return this.current ? this.measureInstanceViewportBox(this.current, this.props) : createBox();
    }
    getStaticValue(key) {
      return this.latestValues[key];
    }
    setStaticValue(key, value) {
      this.latestValues[key] = value;
    }
    /**
     * Update the provided props. Ensure any newly-added motion values are
     * added to our map, old ones removed, and listeners updated.
     */
    update(props, presenceContext) {
      if (props.transformTemplate || this.props.transformTemplate) {
        this.scheduleRender();
      }
      this.prevProps = this.props;
      this.props = props;
      this.prevPresenceContext = this.presenceContext;
      this.presenceContext = presenceContext;
      for (let i = 0; i < propEventHandlers.length; i++) {
        const key = propEventHandlers[i];
        if (this.propEventSubscriptions[key]) {
          this.propEventSubscriptions[key]();
          delete this.propEventSubscriptions[key];
        }
        const listenerName = "on" + key;
        const listener = props[listenerName];
        if (listener) {
          this.propEventSubscriptions[key] = this.on(key, listener);
        }
      }
      this.prevMotionValues = updateMotionValuesFromProps(this, this.scrapeMotionValuesFromProps(props, this.prevProps, this), this.prevMotionValues);
      if (this.handleChildMotionValue) {
        this.handleChildMotionValue();
      }
    }
    getProps() {
      return this.props;
    }
    /**
     * Returns the variant definition with a given name.
     */
    getVariant(name) {
      return this.props.variants ? this.props.variants[name] : void 0;
    }
    /**
     * Returns the defined default transition on this component.
     */
    getDefaultTransition() {
      return this.props.transition;
    }
    getTransformPagePoint() {
      return this.props.transformPagePoint;
    }
    getClosestVariantNode() {
      return this.isVariantNode ? this : this.parent ? this.parent.getClosestVariantNode() : void 0;
    }
    getVariantContext(startAtParent = false) {
      if (startAtParent) {
        return this.parent ? this.parent.getVariantContext() : void 0;
      }
      if (!this.isControllingVariants) {
        const context2 = this.parent ? this.parent.getVariantContext() || {} : {};
        if (this.props.initial !== void 0) {
          context2.initial = this.props.initial;
        }
        return context2;
      }
      const context = {};
      for (let i = 0; i < numVariantProps; i++) {
        const name = variantProps[i];
        const prop = this.props[name];
        if (isVariantLabel(prop) || prop === false) {
          context[name] = prop;
        }
      }
      return context;
    }
    /**
     * Add a child visual element to our set of children.
     */
    addVariantChild(child) {
      const closestVariantNode = this.getClosestVariantNode();
      if (closestVariantNode) {
        closestVariantNode.variantChildren && closestVariantNode.variantChildren.add(child);
        return () => closestVariantNode.variantChildren.delete(child);
      }
    }
    /**
     * Add a motion value and bind it to this visual element.
     */
    addValue(key, value) {
      const existingValue = this.values.get(key);
      if (value !== existingValue) {
        if (existingValue)
          this.removeValue(key);
        this.bindToMotionValue(key, value);
        this.values.set(key, value);
        this.latestValues[key] = value.get();
      }
    }
    /**
     * Remove a motion value and unbind any active subscriptions.
     */
    removeValue(key) {
      this.values.delete(key);
      const unsubscribe = this.valueSubscriptions.get(key);
      if (unsubscribe) {
        unsubscribe();
        this.valueSubscriptions.delete(key);
      }
      delete this.latestValues[key];
      this.removeValueFromRenderState(key, this.renderState);
    }
    /**
     * Check whether we have a motion value for this key
     */
    hasValue(key) {
      return this.values.has(key);
    }
    getValue(key, defaultValue) {
      if (this.props.values && this.props.values[key]) {
        return this.props.values[key];
      }
      let value = this.values.get(key);
      if (value === void 0 && defaultValue !== void 0) {
        value = motionValue(defaultValue === null ? void 0 : defaultValue, { owner: this });
        this.addValue(key, value);
      }
      return value;
    }
    /**
     * If we're trying to animate to a previously unencountered value,
     * we need to check for it in our state and as a last resort read it
     * directly from the instance (which might have performance implications).
     */
    readValue(key, target) {
      var _a4;
      let value = this.latestValues[key] !== void 0 || !this.current ? this.latestValues[key] : (_a4 = this.getBaseTargetFromProps(this.props, key)) !== null && _a4 !== void 0 ? _a4 : this.readValueFromInstance(this.current, key, this.options);
      if (value !== void 0 && value !== null) {
        if (typeof value === "string" && (isNumericalString(value) || isZeroValueString(value))) {
          value = parseFloat(value);
        } else if (!findValueType(value) && complex.test(target)) {
          value = getAnimatableNone(key, target);
        }
        this.setBaseTarget(key, isMotionValue(value) ? value.get() : value);
      }
      return isMotionValue(value) ? value.get() : value;
    }
    /**
     * Set the base target to later animate back to. This is currently
     * only hydrated on creation and when we first read a value.
     */
    setBaseTarget(key, value) {
      this.baseTarget[key] = value;
    }
    /**
     * Find the base target for a value thats been removed from all animation
     * props.
     */
    getBaseTarget(key) {
      var _a4;
      const { initial } = this.props;
      let valueFromInitial;
      if (typeof initial === "string" || typeof initial === "object") {
        const variant = resolveVariantFromProps(this.props, initial, (_a4 = this.presenceContext) === null || _a4 === void 0 ? void 0 : _a4.custom);
        if (variant) {
          valueFromInitial = variant[key];
        }
      }
      if (initial && valueFromInitial !== void 0) {
        return valueFromInitial;
      }
      const target = this.getBaseTargetFromProps(this.props, key);
      if (target !== void 0 && !isMotionValue(target))
        return target;
      return this.initialValues[key] !== void 0 && valueFromInitial === void 0 ? void 0 : this.baseTarget[key];
    }
    on(eventName, callback) {
      if (!this.events[eventName]) {
        this.events[eventName] = new SubscriptionManager();
      }
      return this.events[eventName].add(callback);
    }
    notify(eventName, ...args) {
      if (this.events[eventName]) {
        this.events[eventName].notify(...args);
      }
    }
  }
  class DOMVisualElement extends VisualElement {
    constructor() {
      super(...arguments);
      this.KeyframeResolver = DOMKeyframesResolver;
    }
    sortInstanceNodePosition(a, b2) {
      return a.compareDocumentPosition(b2) & 2 ? 1 : -1;
    }
    getBaseTargetFromProps(props, key) {
      return props.style ? props.style[key] : void 0;
    }
    removeValueFromRenderState(key, { vars: vars2, style }) {
      delete vars2[key];
      delete style[key];
    }
  }
  function getComputedStyle(element) {
    return window.getComputedStyle(element);
  }
  class HTMLVisualElement extends DOMVisualElement {
    constructor() {
      super(...arguments);
      this.type = "html";
    }
    readValueFromInstance(instance, key) {
      if (transformProps.has(key)) {
        const defaultType = getDefaultValueType(key);
        return defaultType ? defaultType.default || 0 : 0;
      } else {
        const computedStyle = getComputedStyle(instance);
        const value = (isCSSVariableName(key) ? computedStyle.getPropertyValue(key) : computedStyle[key]) || 0;
        return typeof value === "string" ? value.trim() : value;
      }
    }
    measureInstanceViewportBox(instance, { transformPagePoint }) {
      return measureViewportBox(instance, transformPagePoint);
    }
    build(renderState, latestValues, options, props) {
      buildHTMLStyles(renderState, latestValues, options, props.transformTemplate);
    }
    scrapeMotionValuesFromProps(props, prevProps, visualElement) {
      return scrapeMotionValuesFromProps$1(props, prevProps, visualElement);
    }
    handleChildMotionValue() {
      if (this.childSubscription) {
        this.childSubscription();
        delete this.childSubscription;
      }
      const { children } = this.props;
      if (isMotionValue(children)) {
        this.childSubscription = children.on("change", (latest) => {
          if (this.current)
            this.current.textContent = `${latest}`;
        });
      }
    }
    renderInstance(instance, renderState, styleProp, projection) {
      renderHTML(instance, renderState, styleProp, projection);
    }
  }
  class SVGVisualElement extends DOMVisualElement {
    constructor() {
      super(...arguments);
      this.type = "svg";
      this.isSVGTag = false;
    }
    getBaseTargetFromProps(props, key) {
      return props[key];
    }
    readValueFromInstance(instance, key) {
      if (transformProps.has(key)) {
        const defaultType = getDefaultValueType(key);
        return defaultType ? defaultType.default || 0 : 0;
      }
      key = !camelCaseAttributes.has(key) ? camelToDash(key) : key;
      return instance.getAttribute(key);
    }
    measureInstanceViewportBox() {
      return createBox();
    }
    scrapeMotionValuesFromProps(props, prevProps, visualElement) {
      return scrapeMotionValuesFromProps(props, prevProps, visualElement);
    }
    build(renderState, latestValues, options, props) {
      buildSVGAttrs(renderState, latestValues, options, this.isSVGTag, props.transformTemplate);
    }
    renderInstance(instance, renderState, styleProp, projection) {
      renderSVG(instance, renderState, styleProp, projection);
    }
    mount(instance) {
      this.isSVGTag = isSVGTag(instance.tagName);
      super.mount(instance);
    }
  }
  const createDomVisualElement = (Component, options) => {
    return isSVGComponent(Component) ? new SVGVisualElement(options, { enableHardwareAcceleration: false }) : new HTMLVisualElement(options, {
      allowProjection: Component !== reactExports.Fragment,
      enableHardwareAcceleration: true
    });
  };
  const layout = {
    layout: {
      ProjectionNode: HTMLProjectionNode,
      MeasureLayout
    }
  };
  const preloadedFeatures = {
    ...animations,
    ...gestureAnimations,
    ...drag,
    ...layout
  };
  const motion = /* @__PURE__ */ createMotionProxy((Component, config2) => createDomMotionConfig(Component, config2, preloadedFeatures, createDomVisualElement));
  function useIsMounted() {
    const isMounted = reactExports.useRef(false);
    useIsomorphicLayoutEffect(() => {
      isMounted.current = true;
      return () => {
        isMounted.current = false;
      };
    }, []);
    return isMounted;
  }
  function useForceUpdate() {
    const isMounted = useIsMounted();
    const [forcedRenderCount, setForcedRenderCount] = reactExports.useState(0);
    const forceRender = reactExports.useCallback(() => {
      isMounted.current && setForcedRenderCount(forcedRenderCount + 1);
    }, [forcedRenderCount]);
    const deferredForceRender = reactExports.useCallback(() => frame.postRender(forceRender), [forceRender]);
    return [deferredForceRender, forcedRenderCount];
  }
  class PopChildMeasure extends reactExports.Component {
    getSnapshotBeforeUpdate(prevProps) {
      const element = this.props.childRef.current;
      if (element && prevProps.isPresent && !this.props.isPresent) {
        const size2 = this.props.sizeRef.current;
        size2.height = element.offsetHeight || 0;
        size2.width = element.offsetWidth || 0;
        size2.top = element.offsetTop;
        size2.left = element.offsetLeft;
      }
      return null;
    }
    /**
     * Required with getSnapshotBeforeUpdate to stop React complaining.
     */
    componentDidUpdate() {
    }
    render() {
      return this.props.children;
    }
  }
  function PopChild({ children, isPresent: isPresent2 }) {
    const id2 = reactExports.useId();
    const ref = reactExports.useRef(null);
    const size2 = reactExports.useRef({
      width: 0,
      height: 0,
      top: 0,
      left: 0
    });
    const { nonce } = reactExports.useContext(MotionConfigContext);
    reactExports.useInsertionEffect(() => {
      const { width, height, top, left } = size2.current;
      if (isPresent2 || !ref.current || !width || !height)
        return;
      ref.current.dataset.motionPopId = id2;
      const style = document.createElement("style");
      if (nonce)
        style.nonce = nonce;
      document.head.appendChild(style);
      if (style.sheet) {
        style.sheet.insertRule(`
          [data-motion-pop-id="${id2}"] {
            position: absolute !important;
            width: ${width}px !important;
            height: ${height}px !important;
            top: ${top}px !important;
            left: ${left}px !important;
          }
        `);
      }
      return () => {
        document.head.removeChild(style);
      };
    }, [isPresent2]);
    return jsxRuntimeExports.jsx(PopChildMeasure, { isPresent: isPresent2, childRef: ref, sizeRef: size2, children: reactExports.cloneElement(children, { ref }) });
  }
  const PresenceChild = ({ children, initial, isPresent: isPresent2, onExitComplete, custom, presenceAffectsLayout, mode: mode2 }) => {
    const presenceChildren = useConstant(newChildrenMap);
    const id2 = reactExports.useId();
    const context = reactExports.useMemo(
      () => ({
        id: id2,
        initial,
        isPresent: isPresent2,
        custom,
        onExitComplete: (childId) => {
          presenceChildren.set(childId, true);
          for (const isComplete of presenceChildren.values()) {
            if (!isComplete)
              return;
          }
          onExitComplete && onExitComplete();
        },
        register: (childId) => {
          presenceChildren.set(childId, false);
          return () => presenceChildren.delete(childId);
        }
      }),
      /**
       * If the presence of a child affects the layout of the components around it,
       * we want to make a new context value to ensure they get re-rendered
       * so they can detect that layout change.
       */
      presenceAffectsLayout ? [Math.random()] : [isPresent2]
    );
    reactExports.useMemo(() => {
      presenceChildren.forEach((_2, key) => presenceChildren.set(key, false));
    }, [isPresent2]);
    reactExports.useEffect(() => {
      !isPresent2 && !presenceChildren.size && onExitComplete && onExitComplete();
    }, [isPresent2]);
    if (mode2 === "popLayout") {
      children = jsxRuntimeExports.jsx(PopChild, { isPresent: isPresent2, children });
    }
    return jsxRuntimeExports.jsx(PresenceContext.Provider, { value: context, children });
  };
  function newChildrenMap() {
    return /* @__PURE__ */ new Map();
  }
  function useUnmountEffect(callback) {
    return reactExports.useEffect(() => () => callback(), []);
  }
  const getChildKey = (child) => child.key || "";
  function updateChildLookup(children, allChildren) {
    children.forEach((child) => {
      const key = getChildKey(child);
      allChildren.set(key, child);
    });
  }
  function onlyElements(children) {
    const filtered = [];
    reactExports.Children.forEach(children, (child) => {
      if (reactExports.isValidElement(child))
        filtered.push(child);
    });
    return filtered;
  }
  const AnimatePresence = ({ children, custom, initial = true, onExitComplete, exitBeforeEnter, presenceAffectsLayout = true, mode: mode2 = "sync" }) => {
    const forceRender = reactExports.useContext(LayoutGroupContext).forceRender || useForceUpdate()[0];
    const isMounted = useIsMounted();
    const filteredChildren = onlyElements(children);
    let childrenToRender = filteredChildren;
    const exitingChildren = reactExports.useRef(/* @__PURE__ */ new Map()).current;
    const presentChildren = reactExports.useRef(childrenToRender);
    const allChildren = reactExports.useRef(/* @__PURE__ */ new Map()).current;
    const isInitialRender = reactExports.useRef(true);
    useIsomorphicLayoutEffect(() => {
      isInitialRender.current = false;
      updateChildLookup(filteredChildren, allChildren);
      presentChildren.current = childrenToRender;
    });
    useUnmountEffect(() => {
      isInitialRender.current = true;
      allChildren.clear();
      exitingChildren.clear();
    });
    if (isInitialRender.current) {
      return jsxRuntimeExports.jsx(jsxRuntimeExports.Fragment, { children: childrenToRender.map((child) => jsxRuntimeExports.jsx(PresenceChild, { isPresent: true, initial: initial ? void 0 : false, presenceAffectsLayout, mode: mode2, children: child }, getChildKey(child))) });
    }
    childrenToRender = [...childrenToRender];
    const presentKeys = presentChildren.current.map(getChildKey);
    const targetKeys = filteredChildren.map(getChildKey);
    const numPresent = presentKeys.length;
    for (let i = 0; i < numPresent; i++) {
      const key = presentKeys[i];
      if (targetKeys.indexOf(key) === -1 && !exitingChildren.has(key)) {
        exitingChildren.set(key, void 0);
      }
    }
    if (mode2 === "wait" && exitingChildren.size) {
      childrenToRender = [];
    }
    exitingChildren.forEach((component, key) => {
      if (targetKeys.indexOf(key) !== -1)
        return;
      const child = allChildren.get(key);
      if (!child)
        return;
      const insertionIndex = presentKeys.indexOf(key);
      let exitingComponent = component;
      if (!exitingComponent) {
        const onExit = () => {
          exitingChildren.delete(key);
          const leftOverKeys = Array.from(allChildren.keys()).filter((childKey) => !targetKeys.includes(childKey));
          leftOverKeys.forEach((leftOverKey) => allChildren.delete(leftOverKey));
          presentChildren.current = filteredChildren.filter((presentChild) => {
            const presentChildKey = getChildKey(presentChild);
            return (
              // filter out the node exiting
              presentChildKey === key || // filter out the leftover children
              leftOverKeys.includes(presentChildKey)
            );
          });
          if (!exitingChildren.size) {
            if (isMounted.current === false)
              return;
            forceRender();
            onExitComplete && onExitComplete();
          }
        };
        exitingComponent = jsxRuntimeExports.jsx(PresenceChild, { isPresent: false, onExitComplete: onExit, custom, presenceAffectsLayout, mode: mode2, children: child }, getChildKey(child));
        exitingChildren.set(key, exitingComponent);
      }
      childrenToRender.splice(insertionIndex, 0, exitingComponent);
    });
    childrenToRender = childrenToRender.map((child) => {
      const key = child.key;
      return exitingChildren.has(key) ? child : jsxRuntimeExports.jsx(PresenceChild, { isPresent: true, presenceAffectsLayout, mode: mode2, children: child }, getChildKey(child));
    });
    return jsxRuntimeExports.jsx(jsxRuntimeExports.Fragment, { children: exitingChildren.size ? childrenToRender : childrenToRender.map((child) => reactExports.cloneElement(child)) });
  };
  var toastMotionVariants = {
    initial: (props) => {
      const { position: position2 } = props;
      const dir = ["top", "bottom"].includes(position2) ? "y" : "x";
      let factor = ["top-right", "bottom-right"].includes(position2) ? 1 : -1;
      if (position2 === "bottom")
        factor = 1;
      return {
        opacity: 0,
        [dir]: factor * 24
      };
    },
    animate: {
      opacity: 1,
      y: 0,
      x: 0,
      scale: 1,
      transition: {
        duration: 0.4,
        ease: [0.4, 0, 0.2, 1]
      }
    },
    exit: {
      opacity: 0,
      scale: 0.85,
      transition: {
        duration: 0.2,
        ease: [0.4, 0, 1, 1]
      }
    }
  };
  var ToastComponent = reactExports.memo((props) => {
    const {
      id: id2,
      message,
      onCloseComplete,
      onRequestRemove,
      requestClose = false,
      position: position2 = "bottom",
      duration = 5e3,
      containerStyle,
      motionVariants = toastMotionVariants,
      toastSpacing = "0.5rem"
    } = props;
    const [delay2, setDelay] = reactExports.useState(duration);
    const isPresent2 = useIsPresent();
    useUpdateEffect(() => {
      if (!isPresent2) {
        onCloseComplete == null ? void 0 : onCloseComplete();
      }
    }, [isPresent2]);
    useUpdateEffect(() => {
      setDelay(duration);
    }, [duration]);
    const onMouseEnter = () => setDelay(null);
    const onMouseLeave = () => setDelay(duration);
    const close = () => {
      if (isPresent2)
        onRequestRemove();
    };
    reactExports.useEffect(() => {
      if (isPresent2 && requestClose) {
        onRequestRemove();
      }
    }, [isPresent2, requestClose, onRequestRemove]);
    useTimeout(close, delay2);
    const containerStyles = reactExports.useMemo(
      () => ({
        pointerEvents: "auto",
        maxWidth: 560,
        minWidth: 300,
        margin: toastSpacing,
        ...containerStyle
      }),
      [containerStyle, toastSpacing]
    );
    const toastStyle = reactExports.useMemo(() => getToastStyle(position2), [position2]);
    return /* @__PURE__ */ jsxRuntimeExports.jsx(
      motion.div,
      {
        layout: true,
        className: "chakra-toast",
        variants: motionVariants,
        initial: "initial",
        animate: "animate",
        exit: "exit",
        onHoverStart: onMouseEnter,
        onHoverEnd: onMouseLeave,
        custom: { position: position2 },
        style: toastStyle,
        children: /* @__PURE__ */ jsxRuntimeExports.jsx(
          chakra.div,
          {
            role: "status",
            "aria-atomic": "true",
            className: "chakra-toast__inner",
            __css: containerStyles,
            children: runIfFn$2(message, { id: id2, onClose: close })
          }
        )
      }
    );
  });
  ToastComponent.displayName = "ToastComponent";
  var fallbackIcon = {
    path: /* @__PURE__ */ jsxRuntimeExports.jsxs("g", { stroke: "currentColor", strokeWidth: "1.5", children: [
      /* @__PURE__ */ jsxRuntimeExports.jsx(
        "path",
        {
          strokeLinecap: "round",
          fill: "none",
          d: "M9,9a3,3,0,1,1,4,2.829,1.5,1.5,0,0,0-1,1.415V14.25"
        }
      ),
      /* @__PURE__ */ jsxRuntimeExports.jsx(
        "path",
        {
          fill: "currentColor",
          strokeLinecap: "round",
          d: "M12,17.25a.375.375,0,1,0,.375.375A.375.375,0,0,0,12,17.25h0"
        }
      ),
      /* @__PURE__ */ jsxRuntimeExports.jsx("circle", { fill: "none", strokeMiterlimit: "10", cx: "12", cy: "12", r: "11.25" })
    ] }),
    viewBox: "0 0 24 24"
  };
  var Icon = forwardRef((props, ref) => {
    const {
      as: element,
      viewBox,
      color: color2 = "currentColor",
      focusable = false,
      children,
      className,
      __css,
      ...rest
    } = props;
    const _className = cx("chakra-icon", className);
    const customStyles = useStyleConfig("Icon", props);
    const styles2 = {
      w: "1em",
      h: "1em",
      display: "inline-block",
      lineHeight: "1em",
      flexShrink: 0,
      color: color2,
      ...__css,
      ...customStyles
    };
    const shared = {
      ref,
      focusable,
      className: _className,
      __css: styles2
    };
    const _viewBox = viewBox != null ? viewBox : fallbackIcon.viewBox;
    if (element && typeof element !== "string") {
      return /* @__PURE__ */ jsxRuntimeExports.jsx(chakra.svg, { as: element, ...shared, ...rest });
    }
    const _path = children != null ? children : fallbackIcon.path;
    return /* @__PURE__ */ jsxRuntimeExports.jsx(chakra.svg, { verticalAlign: "middle", viewBox: _viewBox, ...shared, ...rest, children: _path });
  });
  Icon.displayName = "Icon";
  function CheckIcon(props) {
    return /* @__PURE__ */ jsxRuntimeExports.jsx(Icon, { viewBox: "0 0 24 24", ...props, children: /* @__PURE__ */ jsxRuntimeExports.jsx(
      "path",
      {
        fill: "currentColor",
        d: "M12,0A12,12,0,1,0,24,12,12.014,12.014,0,0,0,12,0Zm6.927,8.2-6.845,9.289a1.011,1.011,0,0,1-1.43.188L5.764,13.769a1,1,0,1,1,1.25-1.562l4.076,3.261,6.227-8.451A1,1,0,1,1,18.927,8.2Z"
      }
    ) });
  }
  function InfoIcon(props) {
    return /* @__PURE__ */ jsxRuntimeExports.jsx(Icon, { viewBox: "0 0 24 24", ...props, children: /* @__PURE__ */ jsxRuntimeExports.jsx(
      "path",
      {
        fill: "currentColor",
        d: "M12,0A12,12,0,1,0,24,12,12.013,12.013,0,0,0,12,0Zm.25,5a1.5,1.5,0,1,1-1.5,1.5A1.5,1.5,0,0,1,12.25,5ZM14.5,18.5h-4a1,1,0,0,1,0-2h.75a.25.25,0,0,0,.25-.25v-4.5a.25.25,0,0,0-.25-.25H10.5a1,1,0,0,1,0-2h1a2,2,0,0,1,2,2v4.75a.25.25,0,0,0,.25.25h.75a1,1,0,1,1,0,2Z"
      }
    ) });
  }
  function WarningIcon(props) {
    return /* @__PURE__ */ jsxRuntimeExports.jsx(Icon, { viewBox: "0 0 24 24", ...props, children: /* @__PURE__ */ jsxRuntimeExports.jsx(
      "path",
      {
        fill: "currentColor",
        d: "M11.983,0a12.206,12.206,0,0,0-8.51,3.653A11.8,11.8,0,0,0,0,12.207,11.779,11.779,0,0,0,11.8,24h.214A12.111,12.111,0,0,0,24,11.791h0A11.766,11.766,0,0,0,11.983,0ZM10.5,16.542a1.476,1.476,0,0,1,1.449-1.53h.027a1.527,1.527,0,0,1,1.523,1.47,1.475,1.475,0,0,1-1.449,1.53h-.027A1.529,1.529,0,0,1,10.5,16.542ZM11,12.5v-6a1,1,0,0,1,2,0v6a1,1,0,1,1-2,0Z"
      }
    ) });
  }
  var spin = keyframes$1({
    "0%": {
      transform: "rotate(0deg)"
    },
    "100%": {
      transform: "rotate(360deg)"
    }
  });
  var Spinner = forwardRef((props, ref) => {
    const styles2 = useStyleConfig("Spinner", props);
    const {
      label = "Loading...",
      thickness = "2px",
      speed = "0.45s",
      emptyColor = "transparent",
      className,
      ...rest
    } = omitThemingProps(props);
    const _className = cx("chakra-spinner", className);
    const spinnerStyles = {
      display: "inline-block",
      borderColor: "currentColor",
      borderStyle: "solid",
      borderRadius: "99999px",
      borderWidth: thickness,
      borderBottomColor: emptyColor,
      borderLeftColor: emptyColor,
      animation: `${spin} ${speed} linear infinite`,
      ...styles2
    };
    return /* @__PURE__ */ jsxRuntimeExports.jsx(
      chakra.div,
      {
        ref,
        __css: spinnerStyles,
        className: _className,
        ...rest,
        children: label && /* @__PURE__ */ jsxRuntimeExports.jsx(chakra.span, { srOnly: true, children: label })
      }
    );
  });
  Spinner.displayName = "Spinner";
  var [AlertProvider, useAlertContext] = createContext$1({
    name: "AlertContext",
    hookName: "useAlertContext",
    providerName: "<Alert />"
  });
  var [AlertStylesProvider, useAlertStyles] = createContext$1({
    name: `AlertStylesContext`,
    hookName: `useAlertStyles`,
    providerName: "<Alert />"
  });
  var STATUSES = {
    info: { icon: InfoIcon, colorScheme: "blue" },
    warning: { icon: WarningIcon, colorScheme: "orange" },
    success: { icon: CheckIcon, colorScheme: "green" },
    error: { icon: WarningIcon, colorScheme: "red" },
    loading: { icon: Spinner, colorScheme: "blue" }
  };
  function getStatusColorScheme(status) {
    return STATUSES[status].colorScheme;
  }
  function getStatusIcon(status) {
    return STATUSES[status].icon;
  }
  var AlertDescription = forwardRef(
    function AlertDescription2(props, ref) {
      const styles2 = useAlertStyles();
      const { status } = useAlertContext();
      const descriptionStyles = {
        display: "inline",
        ...styles2.description
      };
      return /* @__PURE__ */ jsxRuntimeExports.jsx(
        chakra.div,
        {
          ref,
          "data-status": status,
          ...props,
          className: cx("chakra-alert__desc", props.className),
          __css: descriptionStyles
        }
      );
    }
  );
  AlertDescription.displayName = "AlertDescription";
  function AlertIcon(props) {
    const { status } = useAlertContext();
    const BaseIcon = getStatusIcon(status);
    const styles2 = useAlertStyles();
    const css2 = status === "loading" ? styles2.spinner : styles2.icon;
    return /* @__PURE__ */ jsxRuntimeExports.jsx(
      chakra.span,
      {
        display: "inherit",
        "data-status": status,
        ...props,
        className: cx("chakra-alert__icon", props.className),
        __css: css2,
        children: props.children || /* @__PURE__ */ jsxRuntimeExports.jsx(BaseIcon, { h: "100%", w: "100%" })
      }
    );
  }
  AlertIcon.displayName = "AlertIcon";
  var AlertTitle = forwardRef(
    function AlertTitle2(props, ref) {
      const styles2 = useAlertStyles();
      const { status } = useAlertContext();
      return /* @__PURE__ */ jsxRuntimeExports.jsx(
        chakra.div,
        {
          ref,
          "data-status": status,
          ...props,
          className: cx("chakra-alert__title", props.className),
          __css: styles2.title
        }
      );
    }
  );
  AlertTitle.displayName = "AlertTitle";
  var Alert = forwardRef(function Alert2(props, ref) {
    var _a4;
    const { status = "info", addRole = true, ...rest } = omitThemingProps(props);
    const colorScheme = (_a4 = props.colorScheme) != null ? _a4 : getStatusColorScheme(status);
    const styles2 = useMultiStyleConfig("Alert", { ...props, colorScheme });
    const alertStyles = {
      width: "100%",
      display: "flex",
      alignItems: "center",
      position: "relative",
      overflow: "hidden",
      ...styles2.container
    };
    return /* @__PURE__ */ jsxRuntimeExports.jsx(AlertProvider, { value: { status }, children: /* @__PURE__ */ jsxRuntimeExports.jsx(AlertStylesProvider, { value: styles2, children: /* @__PURE__ */ jsxRuntimeExports.jsx(
      chakra.div,
      {
        "data-status": status,
        role: addRole ? "alert" : void 0,
        ref,
        ...rest,
        className: cx("chakra-alert", props.className),
        __css: alertStyles
      }
    ) }) });
  });
  Alert.displayName = "Alert";
  function CloseIcon(props) {
    return /* @__PURE__ */ jsxRuntimeExports.jsx(Icon, { focusable: "false", "aria-hidden": true, ...props, children: /* @__PURE__ */ jsxRuntimeExports.jsx(
      "path",
      {
        fill: "currentColor",
        d: "M.439,21.44a1.5,1.5,0,0,0,2.122,2.121L11.823,14.3a.25.25,0,0,1,.354,0l9.262,9.263a1.5,1.5,0,1,0,2.122-2.121L14.3,12.177a.25.25,0,0,1,0-.354l9.263-9.262A1.5,1.5,0,0,0,21.439.44L12.177,9.7a.25.25,0,0,1-.354,0L2.561.44A1.5,1.5,0,0,0,.439,2.561L9.7,11.823a.25.25,0,0,1,0,.354Z"
      }
    ) });
  }
  var CloseButton = forwardRef(
    function CloseButton2(props, ref) {
      const styles2 = useStyleConfig("CloseButton", props);
      const { children, isDisabled, __css, ...rest } = omitThemingProps(props);
      const baseStyle2 = {
        outline: 0,
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        flexShrink: 0
      };
      return /* @__PURE__ */ jsxRuntimeExports.jsx(
        chakra.button,
        {
          type: "button",
          "aria-label": "Close",
          ref,
          disabled: isDisabled,
          __css: {
            ...baseStyle2,
            ...styles2,
            ...__css
          },
          ...rest,
          children: children || /* @__PURE__ */ jsxRuntimeExports.jsx(CloseIcon, { width: "1em", height: "1em" })
        }
      );
    }
  );
  CloseButton.displayName = "CloseButton";
  var initialState = {
    top: [],
    "top-left": [],
    "top-right": [],
    "bottom-left": [],
    bottom: [],
    "bottom-right": []
  };
  var toastStore = createStore(initialState);
  function createStore(initialState2) {
    let state2 = initialState2;
    const listeners = /* @__PURE__ */ new Set();
    const setState = (setStateFn) => {
      state2 = setStateFn(state2);
      listeners.forEach((l2) => l2());
    };
    return {
      getState: () => state2,
      subscribe: (listener) => {
        listeners.add(listener);
        return () => {
          setState(() => initialState2);
          listeners.delete(listener);
        };
      },
      /**
       * Delete a toast record at its position
       */
      removeToast: (id2, position2) => {
        setState((prevState) => ({
          ...prevState,
          // id may be string or number
          // eslint-disable-next-line eqeqeq
          [position2]: prevState[position2].filter((toast) => toast.id != id2)
        }));
      },
      notify: (message, options) => {
        const toast = createToast(message, options);
        const { position: position2, id: id2 } = toast;
        setState((prevToasts) => {
          var _a4, _b3;
          const isTop = position2.includes("top");
          const toasts = isTop ? [toast, ...(_a4 = prevToasts[position2]) != null ? _a4 : []] : [...(_b3 = prevToasts[position2]) != null ? _b3 : [], toast];
          return {
            ...prevToasts,
            [position2]: toasts
          };
        });
        return id2;
      },
      update: (id2, options) => {
        if (!id2)
          return;
        setState((prevState) => {
          const nextState = { ...prevState };
          const { position: position2, index } = findToast(nextState, id2);
          if (position2 && index !== -1) {
            nextState[position2][index] = {
              ...nextState[position2][index],
              ...options,
              message: createRenderToast(options)
            };
          }
          return nextState;
        });
      },
      closeAll: ({ positions } = {}) => {
        setState((prev2) => {
          const allPositions = [
            "bottom",
            "bottom-right",
            "bottom-left",
            "top",
            "top-left",
            "top-right"
          ];
          const positionsToClose = positions != null ? positions : allPositions;
          return positionsToClose.reduce(
            (acc, position2) => {
              acc[position2] = prev2[position2].map((toast) => ({
                ...toast,
                requestClose: true
              }));
              return acc;
            },
            { ...prev2 }
          );
        });
      },
      close: (id2) => {
        setState((prevState) => {
          const position2 = getToastPosition(prevState, id2);
          if (!position2)
            return prevState;
          return {
            ...prevState,
            [position2]: prevState[position2].map((toast) => {
              if (toast.id == id2) {
                return {
                  ...toast,
                  requestClose: true
                };
              }
              return toast;
            })
          };
        });
      },
      isActive: (id2) => Boolean(findToast(toastStore.getState(), id2).position)
    };
  }
  var counter = 0;
  function createToast(message, options = {}) {
    var _a4, _b3;
    counter += 1;
    const id2 = (_a4 = options.id) != null ? _a4 : counter;
    const position2 = (_b3 = options.position) != null ? _b3 : "bottom";
    return {
      id: id2,
      message,
      position: position2,
      duration: options.duration,
      onCloseComplete: options.onCloseComplete,
      onRequestRemove: () => toastStore.removeToast(String(id2), position2),
      status: options.status,
      requestClose: false,
      containerStyle: options.containerStyle
    };
  }
  var Toast = (props) => {
    const {
      status,
      variant = "solid",
      id: id2,
      title,
      isClosable,
      onClose,
      description,
      colorScheme,
      icon
    } = props;
    const ids = id2 ? {
      root: `toast-${id2}`,
      title: `toast-${id2}-title`,
      description: `toast-${id2}-description`
    } : void 0;
    return /* @__PURE__ */ jsxRuntimeExports.jsxs(
      Alert,
      {
        addRole: false,
        status,
        variant,
        id: ids == null ? void 0 : ids.root,
        alignItems: "start",
        borderRadius: "md",
        boxShadow: "lg",
        paddingEnd: 8,
        textAlign: "start",
        width: "auto",
        colorScheme,
        children: [
          /* @__PURE__ */ jsxRuntimeExports.jsx(AlertIcon, { children: icon }),
          /* @__PURE__ */ jsxRuntimeExports.jsxs(chakra.div, { flex: "1", maxWidth: "100%", children: [
            title && /* @__PURE__ */ jsxRuntimeExports.jsx(AlertTitle, { id: ids == null ? void 0 : ids.title, children: title }),
            description && /* @__PURE__ */ jsxRuntimeExports.jsx(AlertDescription, { id: ids == null ? void 0 : ids.description, display: "block", children: description })
          ] }),
          isClosable && /* @__PURE__ */ jsxRuntimeExports.jsx(
            CloseButton,
            {
              size: "sm",
              onClick: onClose,
              position: "absolute",
              insetEnd: 1,
              top: 1
            }
          )
        ]
      }
    );
  };
  function createRenderToast(options = {}) {
    const { render, toastComponent: ToastComponent2 = Toast } = options;
    const renderToast = (props) => {
      if (typeof render === "function") {
        return render({ ...props, ...options });
      }
      return /* @__PURE__ */ jsxRuntimeExports.jsx(ToastComponent2, { ...props, ...options });
    };
    return renderToast;
  }
  var [ToastOptionProvider, useToastOptionContext] = createContext$1({
    name: `ToastOptionsContext`,
    strict: false
  });
  var ToastProvider = (props) => {
    const state2 = reactExports.useSyncExternalStore(
      toastStore.subscribe,
      toastStore.getState,
      toastStore.getState
    );
    const {
      motionVariants,
      component: Component = ToastComponent,
      portalProps
    } = props;
    const stateKeys = Object.keys(state2);
    const toastList = stateKeys.map((position2) => {
      const toasts = state2[position2];
      return /* @__PURE__ */ jsxRuntimeExports.jsx(
        "div",
        {
          role: "region",
          "aria-live": "polite",
          "aria-label": `Notifications-${position2}`,
          id: `chakra-toast-manager-${position2}`,
          style: getToastListStyle(position2),
          children: /* @__PURE__ */ jsxRuntimeExports.jsx(AnimatePresence, { initial: false, children: toasts.map((toast) => /* @__PURE__ */ jsxRuntimeExports.jsx(
            Component,
            {
              motionVariants,
              ...toast
            },
            toast.id
          )) })
        },
        position2
      );
    });
    return /* @__PURE__ */ jsxRuntimeExports.jsx(Portal, { ...portalProps, children: toastList });
  };
  var createChakraProvider = (providerTheme) => {
    return function ChakraProvider2({
      children,
      theme: theme2 = providerTheme,
      toastOptions,
      ...restProps
    }) {
      return /* @__PURE__ */ jsxRuntimeExports.jsxs(ChakraProvider$1, { theme: theme2, ...restProps, children: [
        /* @__PURE__ */ jsxRuntimeExports.jsx(ToastOptionProvider, { value: toastOptions == null ? void 0 : toastOptions.defaultOptions, children }),
        /* @__PURE__ */ jsxRuntimeExports.jsx(ToastProvider, { ...toastOptions })
      ] });
    };
  };
  var ChakraProvider = createChakraProvider(theme);
  function assignRef(ref, value) {
    if (ref == null)
      return;
    if (typeof ref === "function") {
      ref(value);
      return;
    }
    try {
      ref.current = value;
    } catch (error) {
      throw new Error(`Cannot assign value '${value}' to ref '${ref}'`);
    }
  }
  function mergeRefs(...refs) {
    return (node2) => {
      refs.forEach((ref) => {
        assignRef(ref, node2);
      });
    };
  }
  var [FormControlStylesProvider, useFormControlStyles] = createContext$1({
    name: `FormControlStylesContext`,
    errorMessage: `useFormControlStyles returned is 'undefined'. Seems you forgot to wrap the components in "<FormControl />" `
  });
  var [FormControlProvider, useFormControlContext] = createContext$1({
    strict: false,
    name: "FormControlContext"
  });
  function useFormControlProvider(props) {
    const {
      id: idProp,
      isRequired,
      isInvalid,
      isDisabled,
      isReadOnly,
      ...htmlProps
    } = props;
    const uuid = reactExports.useId();
    const id2 = idProp || `field-${uuid}`;
    const labelId = `${id2}-label`;
    const feedbackId = `${id2}-feedback`;
    const helpTextId = `${id2}-helptext`;
    const [hasFeedbackText, setHasFeedbackText] = reactExports.useState(false);
    const [hasHelpText, setHasHelpText] = reactExports.useState(false);
    const [isFocused, setFocus] = reactExports.useState(false);
    const getHelpTextProps = reactExports.useCallback(
      (props2 = {}, forwardedRef = null) => ({
        id: helpTextId,
        ...props2,
        /**
         * Notify the field context when the help text is rendered on screen,
         * so we can apply the correct `aria-describedby` to the field (e.g. input, textarea).
         */
        ref: mergeRefs(forwardedRef, (node2) => {
          if (!node2)
            return;
          setHasHelpText(true);
        })
      }),
      [helpTextId]
    );
    const getLabelProps = reactExports.useCallback(
      (props2 = {}, forwardedRef = null) => ({
        ...props2,
        ref: forwardedRef,
        "data-focus": dataAttr(isFocused),
        "data-disabled": dataAttr(isDisabled),
        "data-invalid": dataAttr(isInvalid),
        "data-readonly": dataAttr(isReadOnly),
        id: props2.id !== void 0 ? props2.id : labelId,
        htmlFor: props2.htmlFor !== void 0 ? props2.htmlFor : id2
      }),
      [id2, isDisabled, isFocused, isInvalid, isReadOnly, labelId]
    );
    const getErrorMessageProps = reactExports.useCallback(
      (props2 = {}, forwardedRef = null) => ({
        id: feedbackId,
        ...props2,
        /**
         * Notify the field context when the error message is rendered on screen,
         * so we can apply the correct `aria-describedby` to the field (e.g. input, textarea).
         */
        ref: mergeRefs(forwardedRef, (node2) => {
          if (!node2)
            return;
          setHasFeedbackText(true);
        }),
        "aria-live": "polite"
      }),
      [feedbackId]
    );
    const getRootProps = reactExports.useCallback(
      (props2 = {}, forwardedRef = null) => ({
        ...props2,
        ...htmlProps,
        ref: forwardedRef,
        role: "group",
        "data-focus": dataAttr(isFocused),
        "data-disabled": dataAttr(isDisabled),
        "data-invalid": dataAttr(isInvalid),
        "data-readonly": dataAttr(isReadOnly)
      }),
      [htmlProps, isDisabled, isFocused, isInvalid, isReadOnly]
    );
    const getRequiredIndicatorProps = reactExports.useCallback(
      (props2 = {}, forwardedRef = null) => ({
        ...props2,
        ref: forwardedRef,
        role: "presentation",
        "aria-hidden": true,
        children: props2.children || "*"
      }),
      []
    );
    return {
      isRequired: !!isRequired,
      isInvalid: !!isInvalid,
      isReadOnly: !!isReadOnly,
      isDisabled: !!isDisabled,
      isFocused: !!isFocused,
      onFocus: () => setFocus(true),
      onBlur: () => setFocus(false),
      hasFeedbackText,
      setHasFeedbackText,
      hasHelpText,
      setHasHelpText,
      id: id2,
      labelId,
      feedbackId,
      helpTextId,
      htmlProps,
      getHelpTextProps,
      getErrorMessageProps,
      getRootProps,
      getLabelProps,
      getRequiredIndicatorProps
    };
  }
  var FormControl = forwardRef(
    function FormControl2(props, ref) {
      const styles2 = useMultiStyleConfig("Form", props);
      const ownProps = omitThemingProps(props);
      const {
        getRootProps,
        htmlProps: _2,
        ...context
      } = useFormControlProvider(ownProps);
      const className = cx("chakra-form-control", props.className);
      return /* @__PURE__ */ jsxRuntimeExports.jsx(FormControlProvider, { value: context, children: /* @__PURE__ */ jsxRuntimeExports.jsx(FormControlStylesProvider, { value: styles2, children: /* @__PURE__ */ jsxRuntimeExports.jsx(
        chakra.div,
        {
          ...getRootProps({}, ref),
          className,
          __css: styles2["container"]
        }
      ) }) });
    }
  );
  FormControl.displayName = "FormControl";
  var FormHelperText = forwardRef(
    function FormHelperText2(props, ref) {
      const field = useFormControlContext();
      const styles2 = useFormControlStyles();
      const className = cx("chakra-form__helper-text", props.className);
      return /* @__PURE__ */ jsxRuntimeExports.jsx(
        chakra.div,
        {
          ...field == null ? void 0 : field.getHelpTextProps(props, ref),
          __css: styles2.helperText,
          className
        }
      );
    }
  );
  FormHelperText.displayName = "FormHelperText";
  function useFormControl(props) {
    const { isDisabled, isInvalid, isReadOnly, isRequired, ...rest } = useFormControlProps(props);
    return {
      ...rest,
      disabled: isDisabled,
      readOnly: isReadOnly,
      required: isRequired,
      "aria-invalid": ariaAttr(isInvalid),
      "aria-required": ariaAttr(isRequired),
      "aria-readonly": ariaAttr(isReadOnly)
    };
  }
  function useFormControlProps(props) {
    var _a4, _b3, _c2;
    const field = useFormControlContext();
    const {
      id: id2,
      disabled,
      readOnly,
      required,
      isRequired,
      isInvalid,
      isReadOnly,
      isDisabled,
      onFocus,
      onBlur,
      ...rest
    } = props;
    const labelIds = props["aria-describedby"] ? [props["aria-describedby"]] : [];
    if ((field == null ? void 0 : field.hasFeedbackText) && (field == null ? void 0 : field.isInvalid)) {
      labelIds.push(field.feedbackId);
    }
    if (field == null ? void 0 : field.hasHelpText) {
      labelIds.push(field.helpTextId);
    }
    return {
      ...rest,
      "aria-describedby": labelIds.join(" ") || void 0,
      id: id2 != null ? id2 : field == null ? void 0 : field.id,
      isDisabled: (_a4 = disabled != null ? disabled : isDisabled) != null ? _a4 : field == null ? void 0 : field.isDisabled,
      isReadOnly: (_b3 = readOnly != null ? readOnly : isReadOnly) != null ? _b3 : field == null ? void 0 : field.isReadOnly,
      isRequired: (_c2 = required != null ? required : isRequired) != null ? _c2 : field == null ? void 0 : field.isRequired,
      isInvalid: isInvalid != null ? isInvalid : field == null ? void 0 : field.isInvalid,
      onFocus: callAllHandlers(field == null ? void 0 : field.onFocus, onFocus),
      onBlur: callAllHandlers(field == null ? void 0 : field.onBlur, onBlur)
    };
  }
  var __assign = function() {
    __assign = Object.assign || function __assign2(t2) {
      for (var s, i = 1, n2 = arguments.length; i < n2; i++) {
        s = arguments[i];
        for (var p2 in s)
          if (Object.prototype.hasOwnProperty.call(s, p2))
            t2[p2] = s[p2];
      }
      return t2;
    };
    return __assign.apply(this, arguments);
  };
  function __spreadArray(to, from2, pack) {
    if (pack || arguments.length === 2)
      for (var i = 0, l2 = from2.length, ar; i < l2; i++) {
        if (ar || !(i in from2)) {
          if (!ar)
            ar = Array.prototype.slice.call(from2, 0, i);
          ar[i] = from2[i];
        }
      }
    return to.concat(ar || Array.prototype.slice.call(from2));
  }
  typeof SuppressedError === "function" ? SuppressedError : function(error, suppressed, message) {
    var e2 = new Error(message);
    return e2.name = "SuppressedError", e2.error = error, e2.suppressed = suppressed, e2;
  };
  var Input = forwardRef(function Input2(props, ref) {
    const { htmlSize, ...rest } = props;
    const styles2 = useMultiStyleConfig("Input", rest);
    const ownProps = omitThemingProps(rest);
    const input = useFormControl(ownProps);
    const _className = cx("chakra-input", props.className);
    return /* @__PURE__ */ jsxRuntimeExports.jsx(
      chakra.input,
      {
        size: htmlSize,
        ...input,
        __css: styles2.field,
        ref,
        className: _className
      }
    );
  });
  Input.displayName = "Input";
  Input.id = "Input";
  var Box = chakra("div");
  Box.displayName = "Box";
  var Square = forwardRef(function Square2(props, ref) {
    const { size: size2, centerContent = true, ...rest } = props;
    const styles2 = centerContent ? { display: "flex", alignItems: "center", justifyContent: "center" } : {};
    return /* @__PURE__ */ jsxRuntimeExports.jsx(
      Box,
      {
        ref,
        boxSize: size2,
        __css: {
          ...styles2,
          flexShrink: 0,
          flexGrow: 0
        },
        ...rest
      }
    );
  });
  Square.displayName = "Square";
  var Circle = forwardRef(function Circle2(props, ref) {
    const { size: size2, ...rest } = props;
    return /* @__PURE__ */ jsxRuntimeExports.jsx(Square, { size: size2, ref, borderRadius: "9999px", ...rest });
  });
  Circle.displayName = "Circle";
  var [TableStylesProvider, useTableStyles] = createContext$1({
    name: `TableStylesContext`,
    errorMessage: `useTableStyles returned is 'undefined'. Seems you forgot to wrap the components in "<Table />" `
  });
  var Table = forwardRef((props, ref) => {
    const styles2 = useMultiStyleConfig("Table", props);
    const { className, layout: layout2, ...tableProps } = omitThemingProps(props);
    return /* @__PURE__ */ jsxRuntimeExports.jsx(TableStylesProvider, { value: styles2, children: /* @__PURE__ */ jsxRuntimeExports.jsx(
      chakra.table,
      {
        ref,
        __css: { tableLayout: layout2, ...styles2.table },
        className: cx("chakra-table", className),
        ...tableProps
      }
    ) });
  });
  Table.displayName = "Table";
  var Thead = forwardRef((props, ref) => {
    const styles2 = useTableStyles();
    return /* @__PURE__ */ jsxRuntimeExports.jsx(chakra.thead, { ...props, ref, __css: styles2.thead });
  });
  var Tr = forwardRef((props, ref) => {
    const styles2 = useTableStyles();
    return /* @__PURE__ */ jsxRuntimeExports.jsx(chakra.tr, { ...props, ref, __css: styles2.tr });
  });
  var Tbody = forwardRef((props, ref) => {
    const styles2 = useTableStyles();
    return /* @__PURE__ */ jsxRuntimeExports.jsx(chakra.tbody, { ...props, ref, __css: styles2.tbody });
  });
  var Td = forwardRef(
    ({ isNumeric, ...rest }, ref) => {
      const styles2 = useTableStyles();
      return /* @__PURE__ */ jsxRuntimeExports.jsx(
        chakra.td,
        {
          ...rest,
          ref,
          __css: styles2.td,
          "data-is-numeric": isNumeric
        }
      );
    }
  );
  var Th = forwardRef(
    ({ isNumeric, ...rest }, ref) => {
      const styles2 = useTableStyles();
      return /* @__PURE__ */ jsxRuntimeExports.jsx(
        chakra.th,
        {
          ...rest,
          ref,
          __css: styles2.th,
          "data-is-numeric": isNumeric
        }
      );
    }
  );
  var reactTable = { exports: {} };
  var reactTable_production_min = { exports: {} };
  (function(module, exports) {
    !function(e2, t2) {
      t2(exports, reactExports);
    }(commonjsGlobal, function(e2, t2) {
      function n2(e3, t3, n3, o2, r3, i2, u3) {
        try {
          var l3 = e3[i2](u3), s2 = l3.value;
        } catch (e4) {
          return void n3(e4);
        }
        l3.done ? t3(s2) : Promise.resolve(s2).then(o2, r3);
      }
      function o(e3) {
        return function() {
          var t3 = this, o2 = arguments;
          return new Promise(function(r3, i2) {
            var u3 = e3.apply(t3, o2);
            function l3(e4) {
              n2(u3, r3, i2, l3, s2, "next", e4);
            }
            function s2(e4) {
              n2(u3, r3, i2, l3, s2, "throw", e4);
            }
            l3(void 0);
          });
        };
      }
      function r2() {
        return (r2 = Object.assign || function(e3) {
          for (var t3 = 1; t3 < arguments.length; t3++) {
            var n3 = arguments[t3];
            for (var o2 in n3)
              Object.prototype.hasOwnProperty.call(n3, o2) && (e3[o2] = n3[o2]);
          }
          return e3;
        }).apply(this, arguments);
      }
      function i(e3, t3) {
        if (null == e3)
          return {};
        var n3, o2, r3 = {}, i2 = Object.keys(e3);
        for (o2 = 0; o2 < i2.length; o2++)
          n3 = i2[o2], t3.indexOf(n3) >= 0 || (r3[n3] = e3[n3]);
        return r3;
      }
      function u2(e3) {
        var t3 = function(e4, t4) {
          if ("object" != typeof e4 || null === e4)
            return e4;
          var n3 = e4[Symbol.toPrimitive];
          if (void 0 !== n3) {
            var o2 = n3.call(e4, t4);
            if ("object" != typeof o2)
              return o2;
            throw new TypeError("@@toPrimitive must return a primitive value.");
          }
          return String(e4);
        }(e3, "string");
        return "symbol" == typeof t3 ? t3 : String(t3);
      }
      t2 = t2 && Object.prototype.hasOwnProperty.call(t2, "default") ? t2.default : t2;
      var l2 = { init: "init" }, s = function(e3) {
        var t3 = e3.value;
        return void 0 === t3 ? "" : t3;
      }, a = function() {
        return t2.createElement(t2.Fragment, null, " ");
      }, c2 = { Cell: s, width: 150, minWidth: 0, maxWidth: Number.MAX_SAFE_INTEGER };
      function d2() {
        for (var e3 = arguments.length, t3 = new Array(e3), n3 = 0; n3 < e3; n3++)
          t3[n3] = arguments[n3];
        return t3.reduce(function(e4, t4) {
          var n4 = t4.style, o2 = t4.className;
          return e4 = r2({}, e4, {}, i(t4, ["style", "className"])), n4 && (e4.style = e4.style ? r2({}, e4.style || {}, {}, n4 || {}) : n4), o2 && (e4.className = e4.className ? e4.className + " " + o2 : o2), "" === e4.className && delete e4.className, e4;
        }, {});
      }
      var f2 = function(e3, t3) {
        return void 0 === t3 && (t3 = {}), function(n3) {
          return void 0 === n3 && (n3 = {}), [].concat(e3, [n3]).reduce(function(e4, o2) {
            return function e5(t4, n4, o3) {
              return "function" == typeof n4 ? e5({}, n4(t4, o3)) : Array.isArray(n4) ? d2.apply(void 0, [t4].concat(n4)) : d2(t4, n4);
            }(e4, o2, r2({}, t3, { userProps: n3 }));
          }, {});
        };
      }, p2 = function(e3, t3, n3, o2) {
        return void 0 === n3 && (n3 = {}), e3.reduce(function(e4, t4) {
          return t4(e4, n3);
        }, t3);
      }, g2 = function(e3, t3, n3) {
        return void 0 === n3 && (n3 = {}), e3.forEach(function(e4) {
          e4(t3, n3);
        });
      };
      function v2(e3, t3, n3, o2) {
        e3.findIndex(function(e4) {
          return e4.pluginName === n3;
        });
        t3.forEach(function(t4) {
          e3.findIndex(function(e4) {
            return e4.pluginName === t4;
          });
        });
      }
      function m2(e3, t3) {
        return "function" == typeof e3 ? e3(t3) : e3;
      }
      function h2(e3) {
        var n3 = t2.useRef();
        return n3.current = e3, t2.useCallback(function() {
          return n3.current;
        }, []);
      }
      var y2 = "undefined" != typeof document ? t2.useLayoutEffect : t2.useEffect;
      function w2(e3, n3) {
        var o2 = t2.useRef(false);
        y2(function() {
          o2.current && e3(), o2.current = true;
        }, n3);
      }
      function R2(e3, t3, n3) {
        return void 0 === n3 && (n3 = {}), function(o2, i2) {
          void 0 === i2 && (i2 = {});
          var u3 = "string" == typeof o2 ? t3[o2] : o2;
          if (void 0 === u3)
            throw console.info(t3), new Error("Renderer Error ☝️");
          return b2(u3, r2({}, e3, { column: t3 }, n3, {}, i2));
        };
      }
      function b2(e3, n3) {
        return function(e4) {
          return "function" == typeof e4 && ((t3 = Object.getPrototypeOf(e4)).prototype && t3.prototype.isReactComponent);
          var t3;
        }(o2 = e3) || "function" == typeof o2 || function(e4) {
          return "object" == typeof e4 && "symbol" == typeof e4.$$typeof && ["react.memo", "react.forward_ref"].includes(e4.$$typeof.description);
        }(o2) ? t2.createElement(e3, n3) : e3;
        var o2;
      }
      function S2(e3, t3, n3) {
        return void 0 === n3 && (n3 = 0), e3.map(function(e4) {
          return x2(e4 = r2({}, e4, { parent: t3, depth: n3 })), e4.columns && (e4.columns = S2(e4.columns, e4, n3 + 1)), e4;
        });
      }
      function C2(e3) {
        return G2(e3, "columns");
      }
      function x2(e3) {
        var t3 = e3.id, n3 = e3.accessor, o2 = e3.Header;
        if ("string" == typeof n3) {
          t3 = t3 || n3;
          var r3 = n3.split(".");
          n3 = function(e4) {
            return function(e5, t4, n4) {
              if (!t4)
                return e5;
              var o3, r4 = "function" == typeof t4 ? t4 : JSON.stringify(t4), i2 = E2.get(r4) || function() {
                var e6 = function(e7) {
                  return function e8(t5, n5) {
                    void 0 === n5 && (n5 = []);
                    if (Array.isArray(t5))
                      for (var o4 = 0; o4 < t5.length; o4 += 1)
                        e8(t5[o4], n5);
                    else
                      n5.push(t5);
                    return n5;
                  }(e7).map(function(e8) {
                    return String(e8).replace(".", "_");
                  }).join(".").replace(T2, ".").replace(O2, "").split(".");
                }(t4);
                return E2.set(r4, e6), e6;
              }();
              try {
                o3 = i2.reduce(function(e6, t5) {
                  return e6[t5];
                }, e5);
              } catch (e6) {
              }
              return void 0 !== o3 ? o3 : n4;
            }(e4, r3);
          };
        }
        if (!t3 && "string" == typeof o2 && o2 && (t3 = o2), !t3 && e3.columns)
          throw console.error(e3), new Error('A column ID (or unique "Header" value) is required!');
        if (!t3)
          throw console.error(e3), new Error("A column ID (or string accessor) is required!");
        return Object.assign(e3, { id: t3, accessor: n3 }), e3;
      }
      function P2(e3, t3) {
        if (!t3)
          throw new Error();
        return Object.assign(e3, r2({ Header: a, Footer: a }, c2, {}, t3, {}, e3)), Object.assign(e3, { originalWidth: e3.width }), e3;
      }
      function B2(e3, t3, n3) {
        void 0 === n3 && (n3 = function() {
          return {};
        });
        for (var o2 = [], i2 = e3, u3 = 0, l3 = function() {
          return u3++;
        }, s2 = function() {
          var e4 = { headers: [] }, u4 = [], s3 = i2.some(function(e5) {
            return e5.parent;
          });
          i2.forEach(function(o3) {
            var i3, a2 = [].concat(u4).reverse()[0];
            if (s3) {
              if (o3.parent)
                i3 = r2({}, o3.parent, { originalId: o3.parent.id, id: o3.parent.id + "_" + l3(), headers: [o3] }, n3(o3));
              else
                i3 = P2(r2({ originalId: o3.id + "_placeholder", id: o3.id + "_placeholder_" + l3(), placeholderOf: o3, headers: [o3] }, n3(o3)), t3);
              a2 && a2.originalId === i3.originalId ? a2.headers.push(o3) : u4.push(i3);
            }
            e4.headers.push(o3);
          }), o2.push(e4), i2 = u4;
        }; i2.length; )
          s2();
        return o2.reverse();
      }
      var E2 = /* @__PURE__ */ new Map();
      function I2() {
        for (var e3 = arguments.length, t3 = new Array(e3), n3 = 0; n3 < e3; n3++)
          t3[n3] = arguments[n3];
        for (var o2 = 0; o2 < t3.length; o2 += 1)
          if (void 0 !== t3[o2])
            return t3[o2];
      }
      function F2(e3) {
        if ("function" == typeof e3)
          return e3;
      }
      function G2(e3, t3) {
        var n3 = [];
        return function e4(o2) {
          o2.forEach(function(o3) {
            o3[t3] ? e4(o3[t3]) : n3.push(o3);
          });
        }(e3), n3;
      }
      function A2(e3, t3) {
        var n3 = t3.manualExpandedKey, o2 = t3.expanded, r3 = t3.expandSubRows, i2 = void 0 === r3 || r3, u3 = [];
        return e3.forEach(function(e4) {
          return function e5(t4, r4) {
            void 0 === r4 && (r4 = true), t4.isExpanded = t4.original && t4.original[n3] || o2[t4.id], t4.canExpand = t4.subRows && !!t4.subRows.length, r4 && u3.push(t4), t4.subRows && t4.subRows.length && t4.isExpanded && t4.subRows.forEach(function(t5) {
              return e5(t5, i2);
            });
          }(e4);
        }), u3;
      }
      function k2(e3, t3, n3) {
        return F2(e3) || t3[e3] || n3[e3] || n3.text;
      }
      function H2(e3, t3, n3) {
        return e3 ? e3(t3, n3) : void 0 === t3;
      }
      function W2() {
        throw new Error("React-Table: You have not called prepareRow(row) one or more rows you are attempting to render.");
      }
      var z2 = null;
      var T2 = /\[/g, O2 = /\]/g;
      var M2 = function(e3) {
        return r2({ role: "table" }, e3);
      }, j2 = function(e3) {
        return r2({ role: "rowgroup" }, e3);
      }, L2 = function(e3, t3) {
        var n3 = t3.column;
        return r2({ key: "header_" + n3.id, colSpan: n3.totalVisibleHeaderCount, role: "columnheader" }, e3);
      }, N2 = function(e3, t3) {
        var n3 = t3.column;
        return r2({ key: "footer_" + n3.id, colSpan: n3.totalVisibleHeaderCount }, e3);
      }, D2 = function(e3, t3) {
        return r2({ key: "headerGroup_" + t3.index, role: "row" }, e3);
      }, V2 = function(e3, t3) {
        return r2({ key: "footerGroup_" + t3.index }, e3);
      }, _2 = function(e3, t3) {
        return r2({ key: "row_" + t3.row.id, role: "row" }, e3);
      }, X2 = function(e3, t3) {
        var n3 = t3.cell;
        return r2({ key: "cell_" + n3.row.id + "_" + n3.column.id, role: "cell" }, e3);
      };
      function q2() {
        return { useOptions: [], stateReducers: [], useControlledState: [], columns: [], columnsDeps: [], allColumns: [], allColumnsDeps: [], accessValue: [], materializedColumns: [], materializedColumnsDeps: [], useInstanceAfterData: [], visibleColumns: [], visibleColumnsDeps: [], headerGroups: [], headerGroupsDeps: [], useInstanceBeforeDimensions: [], useInstance: [], prepareRow: [], getTableProps: [M2], getTableBodyProps: [j2], getHeaderGroupProps: [D2], getFooterGroupProps: [V2], getHeaderProps: [L2], getFooterProps: [N2], getRowProps: [_2], getCellProps: [X2], useFinalInstance: [] };
      }
      l2.resetHiddenColumns = "resetHiddenColumns", l2.toggleHideColumn = "toggleHideColumn", l2.setHiddenColumns = "setHiddenColumns", l2.toggleHideAllColumns = "toggleHideAllColumns";
      var K2 = function(e3) {
        e3.getToggleHiddenProps = [U2], e3.getToggleHideAllColumnsProps = [$2], e3.stateReducers.push(J2), e3.useInstanceBeforeDimensions.push(Y2), e3.headerGroupsDeps.push(function(e4, t3) {
          var n3 = t3.instance;
          return [].concat(e4, [n3.state.hiddenColumns]);
        }), e3.useInstance.push(Q2);
      };
      K2.pluginName = "useColumnVisibility";
      var U2 = function(e3, t3) {
        var n3 = t3.column;
        return [e3, { onChange: function(e4) {
          n3.toggleHidden(!e4.target.checked);
        }, style: { cursor: "pointer" }, checked: n3.isVisible, title: "Toggle Column Visible" }];
      }, $2 = function(e3, t3) {
        var n3 = t3.instance;
        return [e3, { onChange: function(e4) {
          n3.toggleHideAllColumns(!e4.target.checked);
        }, style: { cursor: "pointer" }, checked: !n3.allColumnsHidden && !n3.state.hiddenColumns.length, title: "Toggle All Columns Hidden", indeterminate: !n3.allColumnsHidden && n3.state.hiddenColumns.length }];
      };
      function J2(e3, t3, n3, o2) {
        if (t3.type === l2.init)
          return r2({ hiddenColumns: [] }, e3);
        if (t3.type === l2.resetHiddenColumns)
          return r2({}, e3, { hiddenColumns: o2.initialState.hiddenColumns || [] });
        if (t3.type === l2.toggleHideColumn) {
          var i2 = (void 0 !== t3.value ? t3.value : !e3.hiddenColumns.includes(t3.columnId)) ? [].concat(e3.hiddenColumns, [t3.columnId]) : e3.hiddenColumns.filter(function(e4) {
            return e4 !== t3.columnId;
          });
          return r2({}, e3, { hiddenColumns: i2 });
        }
        return t3.type === l2.setHiddenColumns ? r2({}, e3, { hiddenColumns: m2(t3.value, e3.hiddenColumns) }) : t3.type === l2.toggleHideAllColumns ? r2({}, e3, { hiddenColumns: (void 0 !== t3.value ? t3.value : !e3.hiddenColumns.length) ? o2.allColumns.map(function(e4) {
          return e4.id;
        }) : [] }) : void 0;
      }
      function Y2(e3) {
        var n3 = e3.headers, o2 = e3.state.hiddenColumns;
        t2.useRef(false).current;
        var r3 = 0;
        n3.forEach(function(e4) {
          return r3 += function e5(t3, n4) {
            t3.isVisible = n4 && !o2.includes(t3.id);
            var r4 = 0;
            return t3.headers && t3.headers.length ? t3.headers.forEach(function(n5) {
              return r4 += e5(n5, t3.isVisible);
            }) : r4 = t3.isVisible ? 1 : 0, t3.totalVisibleHeaderCount = r4, r4;
          }(e4, true);
        });
      }
      function Q2(e3) {
        var n3 = e3.columns, o2 = e3.flatHeaders, r3 = e3.dispatch, i2 = e3.allColumns, u3 = e3.getHooks, s2 = e3.state.hiddenColumns, a2 = e3.autoResetHiddenColumns, c3 = void 0 === a2 || a2, d3 = h2(e3), p3 = i2.length === s2.length, g3 = t2.useCallback(function(e4, t3) {
          return r3({ type: l2.toggleHideColumn, columnId: e4, value: t3 });
        }, [r3]), v3 = t2.useCallback(function(e4) {
          return r3({ type: l2.setHiddenColumns, value: e4 });
        }, [r3]), m3 = t2.useCallback(function(e4) {
          return r3({ type: l2.toggleHideAllColumns, value: e4 });
        }, [r3]), y3 = f2(u3().getToggleHideAllColumnsProps, { instance: d3() });
        o2.forEach(function(e4) {
          e4.toggleHidden = function(t3) {
            r3({ type: l2.toggleHideColumn, columnId: e4.id, value: t3 });
          }, e4.getToggleHiddenProps = f2(u3().getToggleHiddenProps, { instance: d3(), column: e4 });
        });
        var R3 = h2(c3);
        w2(function() {
          R3() && r3({ type: l2.resetHiddenColumns });
        }, [r3, n3]), Object.assign(e3, { allColumnsHidden: p3, toggleHideColumn: g3, setHiddenColumns: v3, toggleHideAllColumns: m3, getToggleHideAllColumnsProps: y3 });
      }
      var Z2 = {}, ee2 = {}, te2 = function(e3, t3, n3) {
        return e3;
      }, ne2 = function(e3, t3) {
        return e3.subRows || [];
      }, oe2 = function(e3, t3, n3) {
        return "" + (n3 ? [n3.id, t3].join(".") : t3);
      }, re2 = function(e3) {
        return e3;
      };
      function ie2(e3) {
        var t3 = e3.initialState, n3 = void 0 === t3 ? Z2 : t3, o2 = e3.defaultColumn, u3 = void 0 === o2 ? ee2 : o2, l3 = e3.getSubRows, s2 = void 0 === l3 ? ne2 : l3, a2 = e3.getRowId, c3 = void 0 === a2 ? oe2 : a2, d3 = e3.stateReducer, f3 = void 0 === d3 ? te2 : d3, p3 = e3.useControlledState, g3 = void 0 === p3 ? re2 : p3;
        return r2({}, i(e3, ["initialState", "defaultColumn", "getSubRows", "getRowId", "stateReducer", "useControlledState"]), { initialState: n3, defaultColumn: u3, getSubRows: s2, getRowId: c3, stateReducer: f3, useControlledState: g3 });
      }
      function ue2(e3, t3) {
        void 0 === t3 && (t3 = 0);
        var n3 = 0, o2 = 0, r3 = 0, i2 = 0;
        return e3.forEach(function(e4) {
          var u3 = e4.headers;
          if (e4.totalLeft = t3, u3 && u3.length) {
            var l3 = ue2(u3, t3), s2 = l3[0], a2 = l3[1], c3 = l3[2], d3 = l3[3];
            e4.totalMinWidth = s2, e4.totalWidth = a2, e4.totalMaxWidth = c3, e4.totalFlexWidth = d3;
          } else
            e4.totalMinWidth = e4.minWidth, e4.totalWidth = Math.min(Math.max(e4.minWidth, e4.width), e4.maxWidth), e4.totalMaxWidth = e4.maxWidth, e4.totalFlexWidth = e4.canResize ? e4.totalWidth : 0;
          e4.isVisible && (t3 += e4.totalWidth, n3 += e4.totalMinWidth, o2 += e4.totalWidth, r3 += e4.totalMaxWidth, i2 += e4.totalFlexWidth);
        }), [n3, o2, r3, i2];
      }
      function le2(e3) {
        var t3 = e3.data, n3 = e3.rows, o2 = e3.flatRows, r3 = e3.rowsById, i2 = e3.column, u3 = e3.getRowId, l3 = e3.getSubRows, s2 = e3.accessValueHooks, a2 = e3.getInstance;
        t3.forEach(function(e4, c3) {
          return function e5(n4, c4, d3, f3, g3) {
            void 0 === d3 && (d3 = 0);
            var v3 = n4, m3 = u3(n4, c4, f3), h3 = r3[m3];
            if (h3)
              h3.subRows && h3.originalSubRows.forEach(function(t4, n5) {
                return e5(t4, n5, d3 + 1, h3);
              });
            else if ((h3 = { id: m3, original: v3, index: c4, depth: d3, cells: [{}] }).cells.map = W2, h3.cells.filter = W2, h3.cells.forEach = W2, h3.cells[0].getCellProps = W2, h3.values = {}, g3.push(h3), o2.push(h3), r3[m3] = h3, h3.originalSubRows = l3(n4, c4), h3.originalSubRows) {
              var y3 = [];
              h3.originalSubRows.forEach(function(t4, n5) {
                return e5(t4, n5, d3 + 1, h3, y3);
              }), h3.subRows = y3;
            }
            i2.accessor && (h3.values[i2.id] = i2.accessor(n4, c4, h3, g3, t3)), h3.values[i2.id] = p2(s2, h3.values[i2.id], { row: h3, column: i2, instance: a2() });
          }(e4, c3, 0, void 0, n3);
        });
      }
      l2.resetExpanded = "resetExpanded", l2.toggleRowExpanded = "toggleRowExpanded", l2.toggleAllRowsExpanded = "toggleAllRowsExpanded";
      var se2 = function(e3) {
        e3.getToggleAllRowsExpandedProps = [ae2], e3.getToggleRowExpandedProps = [ce2], e3.stateReducers.push(de2), e3.useInstance.push(fe2), e3.prepareRow.push(pe2);
      };
      se2.pluginName = "useExpanded";
      var ae2 = function(e3, t3) {
        var n3 = t3.instance;
        return [e3, { onClick: function(e4) {
          n3.toggleAllRowsExpanded();
        }, style: { cursor: "pointer" }, title: "Toggle All Rows Expanded" }];
      }, ce2 = function(e3, t3) {
        var n3 = t3.row;
        return [e3, { onClick: function() {
          n3.toggleRowExpanded();
        }, style: { cursor: "pointer" }, title: "Toggle Row Expanded" }];
      };
      function de2(e3, t3, n3, o2) {
        if (t3.type === l2.init)
          return r2({ expanded: {} }, e3);
        if (t3.type === l2.resetExpanded)
          return r2({}, e3, { expanded: o2.initialState.expanded || {} });
        if (t3.type === l2.toggleAllRowsExpanded) {
          var s2 = t3.value, a2 = o2.rowsById, c3 = Object.keys(a2).length === Object.keys(e3.expanded).length;
          if (void 0 !== s2 ? s2 : !c3) {
            var d3 = {};
            return Object.keys(a2).forEach(function(e4) {
              d3[e4] = true;
            }), r2({}, e3, { expanded: d3 });
          }
          return r2({}, e3, { expanded: {} });
        }
        if (t3.type === l2.toggleRowExpanded) {
          var f3, p3 = t3.id, g3 = t3.value, v3 = e3.expanded[p3], m3 = void 0 !== g3 ? g3 : !v3;
          if (!v3 && m3)
            return r2({}, e3, { expanded: r2({}, e3.expanded, (f3 = {}, f3[p3] = true, f3)) });
          if (v3 && !m3) {
            var h3 = e3.expanded;
            h3[p3];
            return r2({}, e3, { expanded: i(h3, [p3].map(u2)) });
          }
          return e3;
        }
      }
      function fe2(e3) {
        var n3 = e3.data, o2 = e3.rows, r3 = e3.rowsById, i2 = e3.manualExpandedKey, u3 = void 0 === i2 ? "expanded" : i2, s2 = e3.paginateExpandedRows, a2 = void 0 === s2 || s2, c3 = e3.expandSubRows, d3 = void 0 === c3 || c3, p3 = e3.autoResetExpanded, g3 = void 0 === p3 || p3, m3 = e3.getHooks, y3 = e3.plugins, R3 = e3.state.expanded, b3 = e3.dispatch;
        v2(y3, ["useSortBy", "useGroupBy", "usePivotColumns", "useGlobalFilter"], "useExpanded");
        var S3 = h2(g3), C3 = Boolean(Object.keys(r3).length && Object.keys(R3).length);
        C3 && Object.keys(r3).some(function(e4) {
          return !R3[e4];
        }) && (C3 = false), w2(function() {
          S3() && b3({ type: l2.resetExpanded });
        }, [b3, n3]);
        var x3 = t2.useCallback(function(e4, t3) {
          b3({ type: l2.toggleRowExpanded, id: e4, value: t3 });
        }, [b3]), P3 = t2.useCallback(function(e4) {
          return b3({ type: l2.toggleAllRowsExpanded, value: e4 });
        }, [b3]), B3 = t2.useMemo(function() {
          return a2 ? A2(o2, { manualExpandedKey: u3, expanded: R3, expandSubRows: d3 }) : o2;
        }, [a2, o2, u3, R3, d3]), E3 = t2.useMemo(function() {
          return function(e4) {
            var t3 = 0;
            return Object.keys(e4).forEach(function(e5) {
              var n4 = e5.split(".");
              t3 = Math.max(t3, n4.length);
            }), t3;
          }(R3);
        }, [R3]), I3 = h2(e3), F3 = f2(m3().getToggleAllRowsExpandedProps, { instance: I3() });
        Object.assign(e3, { preExpandedRows: o2, expandedRows: B3, rows: B3, expandedDepth: E3, isAllRowsExpanded: C3, toggleRowExpanded: x3, toggleAllRowsExpanded: P3, getToggleAllRowsExpandedProps: F3 });
      }
      function pe2(e3, t3) {
        var n3 = t3.instance.getHooks, o2 = t3.instance;
        e3.toggleRowExpanded = function(t4) {
          return o2.toggleRowExpanded(e3.id, t4);
        }, e3.getToggleRowExpandedProps = f2(n3().getToggleRowExpandedProps, { instance: o2, row: e3 });
      }
      var ge2 = function(e3, t3, n3) {
        return e3 = e3.filter(function(e4) {
          return t3.some(function(t4) {
            var o2 = e4.values[t4];
            return String(o2).toLowerCase().includes(String(n3).toLowerCase());
          });
        });
      };
      ge2.autoRemove = function(e3) {
        return !e3;
      };
      var ve2 = function(e3, t3, n3) {
        return e3.filter(function(e4) {
          return t3.some(function(t4) {
            var o2 = e4.values[t4];
            return void 0 === o2 || String(o2).toLowerCase() === String(n3).toLowerCase();
          });
        });
      };
      ve2.autoRemove = function(e3) {
        return !e3;
      };
      var me2 = function(e3, t3, n3) {
        return e3.filter(function(e4) {
          return t3.some(function(t4) {
            var o2 = e4.values[t4];
            return void 0 === o2 || String(o2) === String(n3);
          });
        });
      };
      me2.autoRemove = function(e3) {
        return !e3;
      };
      var he2 = function(e3, t3, n3) {
        return e3.filter(function(e4) {
          return t3.some(function(t4) {
            return e4.values[t4].includes(n3);
          });
        });
      };
      he2.autoRemove = function(e3) {
        return !e3 || !e3.length;
      };
      var ye2 = function(e3, t3, n3) {
        return e3.filter(function(e4) {
          return t3.some(function(t4) {
            var o2 = e4.values[t4];
            return o2 && o2.length && n3.every(function(e5) {
              return o2.includes(e5);
            });
          });
        });
      };
      ye2.autoRemove = function(e3) {
        return !e3 || !e3.length;
      };
      var we2 = function(e3, t3, n3) {
        return e3.filter(function(e4) {
          return t3.some(function(t4) {
            var o2 = e4.values[t4];
            return o2 && o2.length && n3.some(function(e5) {
              return o2.includes(e5);
            });
          });
        });
      };
      we2.autoRemove = function(e3) {
        return !e3 || !e3.length;
      };
      var Re2 = function(e3, t3, n3) {
        return e3.filter(function(e4) {
          return t3.some(function(t4) {
            var o2 = e4.values[t4];
            return n3.includes(o2);
          });
        });
      };
      Re2.autoRemove = function(e3) {
        return !e3 || !e3.length;
      };
      var be2 = function(e3, t3, n3) {
        return e3.filter(function(e4) {
          return t3.some(function(t4) {
            return e4.values[t4] === n3;
          });
        });
      };
      be2.autoRemove = function(e3) {
        return void 0 === e3;
      };
      var Se2 = function(e3, t3, n3) {
        return e3.filter(function(e4) {
          return t3.some(function(t4) {
            return e4.values[t4] == n3;
          });
        });
      };
      Se2.autoRemove = function(e3) {
        return null == e3;
      };
      var Ce2 = function(e3, t3, n3) {
        var o2 = n3 || [], r3 = o2[0], i2 = o2[1];
        if ((r3 = "number" == typeof r3 ? r3 : -1 / 0) > (i2 = "number" == typeof i2 ? i2 : 1 / 0)) {
          var u3 = r3;
          r3 = i2, i2 = u3;
        }
        return e3.filter(function(e4) {
          return t3.some(function(t4) {
            var n4 = e4.values[t4];
            return n4 >= r3 && n4 <= i2;
          });
        });
      };
      Ce2.autoRemove = function(e3) {
        return !e3 || "number" != typeof e3[0] && "number" != typeof e3[1];
      };
      var xe2 = Object.freeze({ __proto__: null, text: ge2, exactText: ve2, exactTextCase: me2, includes: he2, includesAll: ye2, includesSome: we2, includesValue: Re2, exact: be2, equals: Se2, between: Ce2 });
      l2.resetFilters = "resetFilters", l2.setFilter = "setFilter", l2.setAllFilters = "setAllFilters";
      var Pe2 = function(e3) {
        e3.stateReducers.push(Be2), e3.useInstance.push(Ee2);
      };
      function Be2(e3, t3, n3, o2) {
        if (t3.type === l2.init)
          return r2({ filters: [] }, e3);
        if (t3.type === l2.resetFilters)
          return r2({}, e3, { filters: o2.initialState.filters || [] });
        if (t3.type === l2.setFilter) {
          var i2 = t3.columnId, u3 = t3.filterValue, s2 = o2.allColumns, a2 = o2.filterTypes, c3 = s2.find(function(e4) {
            return e4.id === i2;
          });
          if (!c3)
            throw new Error("React-Table: Could not find a column with id: " + i2);
          var d3 = k2(c3.filter, a2 || {}, xe2), f3 = e3.filters.find(function(e4) {
            return e4.id === i2;
          }), p3 = m2(u3, f3 && f3.value);
          return H2(d3.autoRemove, p3, c3) ? r2({}, e3, { filters: e3.filters.filter(function(e4) {
            return e4.id !== i2;
          }) }) : r2({}, e3, f3 ? { filters: e3.filters.map(function(e4) {
            return e4.id === i2 ? { id: i2, value: p3 } : e4;
          }) } : { filters: [].concat(e3.filters, [{ id: i2, value: p3 }]) });
        }
        if (t3.type === l2.setAllFilters) {
          var g3 = t3.filters, v3 = o2.allColumns, h3 = o2.filterTypes;
          return r2({}, e3, { filters: m2(g3, e3.filters).filter(function(e4) {
            var t4 = v3.find(function(t5) {
              return t5.id === e4.id;
            });
            return !H2(k2(t4.filter, h3 || {}, xe2).autoRemove, e4.value, t4);
          }) });
        }
      }
      function Ee2(e3) {
        var n3 = e3.data, o2 = e3.rows, r3 = e3.flatRows, i2 = e3.rowsById, u3 = e3.allColumns, s2 = e3.filterTypes, a2 = e3.manualFilters, c3 = e3.defaultCanFilter, d3 = void 0 !== c3 && c3, f3 = e3.disableFilters, p3 = e3.state.filters, g3 = e3.dispatch, v3 = e3.autoResetFilters, m3 = void 0 === v3 || v3, y3 = t2.useCallback(function(e4, t3) {
          g3({ type: l2.setFilter, columnId: e4, filterValue: t3 });
        }, [g3]), R3 = t2.useCallback(function(e4) {
          g3({ type: l2.setAllFilters, filters: e4 });
        }, [g3]);
        u3.forEach(function(e4) {
          var t3 = e4.id, n4 = e4.accessor, o3 = e4.defaultCanFilter, r4 = e4.disableFilters;
          e4.canFilter = n4 ? I2(true !== r4 && void 0, true !== f3 && void 0, true) : I2(o3, d3, false), e4.setFilter = function(t4) {
            return y3(e4.id, t4);
          };
          var i3 = p3.find(function(e5) {
            return e5.id === t3;
          });
          e4.filterValue = i3 && i3.value;
        });
        var b3 = t2.useMemo(function() {
          if (a2 || !p3.length)
            return [o2, r3, i2];
          var e4 = [], t3 = {};
          return [function n4(o3, r4) {
            void 0 === r4 && (r4 = 0);
            var i3 = o3;
            return (i3 = p3.reduce(function(e5, t4) {
              var n5 = t4.id, o4 = t4.value, i4 = u3.find(function(e6) {
                return e6.id === n5;
              });
              if (!i4)
                return e5;
              0 === r4 && (i4.preFilteredRows = e5);
              var l3 = k2(i4.filter, s2 || {}, xe2);
              return l3 ? (i4.filteredRows = l3(e5, [n5], o4), i4.filteredRows) : (console.warn("Could not find a valid 'column.filter' for column with the ID: " + i4.id + "."), e5);
            }, o3)).forEach(function(o4) {
              e4.push(o4), t3[o4.id] = o4, o4.subRows && (o4.subRows = o4.subRows && o4.subRows.length > 0 ? n4(o4.subRows, r4 + 1) : o4.subRows);
            }), i3;
          }(o2), e4, t3];
        }, [a2, p3, o2, r3, i2, u3, s2]), S3 = b3[0], C3 = b3[1], x3 = b3[2];
        t2.useMemo(function() {
          u3.filter(function(e4) {
            return !p3.find(function(t3) {
              return t3.id === e4.id;
            });
          }).forEach(function(e4) {
            e4.preFilteredRows = S3, e4.filteredRows = S3;
          });
        }, [S3, p3, u3]);
        var P3 = h2(m3);
        w2(function() {
          P3() && g3({ type: l2.resetFilters });
        }, [g3, a2 ? null : n3]), Object.assign(e3, { preFilteredRows: o2, preFilteredFlatRows: r3, preFilteredRowsById: i2, filteredRows: S3, filteredFlatRows: C3, filteredRowsById: x3, rows: S3, flatRows: C3, rowsById: x3, setFilter: y3, setAllFilters: R3 });
      }
      Pe2.pluginName = "useFilters", l2.resetGlobalFilter = "resetGlobalFilter", l2.setGlobalFilter = "setGlobalFilter";
      var Ie2 = function(e3) {
        e3.stateReducers.push(Fe2), e3.useInstance.push(Ge2);
      };
      function Fe2(e3, t3, n3, o2) {
        if (t3.type === l2.resetGlobalFilter)
          return r2({}, e3, { globalFilter: o2.initialState.globalFilter || void 0 });
        if (t3.type === l2.setGlobalFilter) {
          var u3 = t3.filterValue, s2 = o2.userFilterTypes, a2 = k2(o2.globalFilter, s2 || {}, xe2), c3 = m2(u3, e3.globalFilter);
          if (H2(a2.autoRemove, c3)) {
            e3.globalFilter;
            return i(e3, ["globalFilter"]);
          }
          return r2({}, e3, { globalFilter: c3 });
        }
      }
      function Ge2(e3) {
        var n3 = e3.data, o2 = e3.rows, r3 = e3.flatRows, i2 = e3.rowsById, u3 = e3.allColumns, s2 = e3.filterTypes, a2 = e3.globalFilter, c3 = e3.manualGlobalFilter, d3 = e3.state.globalFilter, f3 = e3.dispatch, p3 = e3.autoResetGlobalFilter, g3 = void 0 === p3 || p3, v3 = e3.disableGlobalFilter, m3 = t2.useCallback(function(e4) {
          f3({ type: l2.setGlobalFilter, filterValue: e4 });
        }, [f3]), y3 = t2.useMemo(function() {
          if (c3 || void 0 === d3)
            return [o2, r3, i2];
          var e4 = [], t3 = {}, n4 = k2(a2, s2 || {}, xe2);
          if (!n4)
            return console.warn("Could not find a valid 'globalFilter' option."), o2;
          u3.forEach(function(e5) {
            var t4 = e5.disableGlobalFilter;
            e5.canFilter = I2(true !== t4 && void 0, true !== v3 && void 0, true);
          });
          var l3 = u3.filter(function(e5) {
            return true === e5.canFilter;
          });
          return [function o3(r4) {
            return (r4 = n4(r4, l3.map(function(e5) {
              return e5.id;
            }), d3)).forEach(function(n5) {
              e4.push(n5), t3[n5.id] = n5, n5.subRows = n5.subRows && n5.subRows.length ? o3(n5.subRows) : n5.subRows;
            }), r4;
          }(o2), e4, t3];
        }, [c3, d3, a2, s2, u3, o2, r3, i2, v3]), R3 = y3[0], b3 = y3[1], S3 = y3[2], C3 = h2(g3);
        w2(function() {
          C3() && f3({ type: l2.resetGlobalFilter });
        }, [f3, c3 ? null : n3]), Object.assign(e3, { preGlobalFilteredRows: o2, preGlobalFilteredFlatRows: r3, preGlobalFilteredRowsById: i2, globalFilteredRows: R3, globalFilteredFlatRows: b3, globalFilteredRowsById: S3, rows: R3, flatRows: b3, rowsById: S3, setGlobalFilter: m3, disableGlobalFilter: v3 });
      }
      function Ae2(e3, t3) {
        return t3.reduce(function(e4, t4) {
          return e4 + ("number" == typeof t4 ? t4 : 0);
        }, 0);
      }
      Ie2.pluginName = "useGlobalFilter";
      var ke2 = Object.freeze({ __proto__: null, sum: Ae2, min: function(e3) {
        var t3 = e3[0] || 0;
        return e3.forEach(function(e4) {
          "number" == typeof e4 && (t3 = Math.min(t3, e4));
        }), t3;
      }, max: function(e3) {
        var t3 = e3[0] || 0;
        return e3.forEach(function(e4) {
          "number" == typeof e4 && (t3 = Math.max(t3, e4));
        }), t3;
      }, minMax: function(e3) {
        var t3 = e3[0] || 0, n3 = e3[0] || 0;
        return e3.forEach(function(e4) {
          "number" == typeof e4 && (t3 = Math.min(t3, e4), n3 = Math.max(n3, e4));
        }), t3 + ".." + n3;
      }, average: function(e3) {
        return Ae2(0, e3) / e3.length;
      }, median: function(e3) {
        if (!e3.length)
          return null;
        var t3 = Math.floor(e3.length / 2), n3 = [].concat(e3).sort(function(e4, t4) {
          return e4 - t4;
        });
        return e3.length % 2 != 0 ? n3[t3] : (n3[t3 - 1] + n3[t3]) / 2;
      }, unique: function(e3) {
        return Array.from(new Set(e3).values());
      }, uniqueCount: function(e3) {
        return new Set(e3).size;
      }, count: function(e3) {
        return e3.length;
      } }), He2 = [], We2 = {};
      l2.resetGroupBy = "resetGroupBy", l2.setGroupBy = "setGroupBy", l2.toggleGroupBy = "toggleGroupBy";
      var ze2 = function(e3) {
        e3.getGroupByToggleProps = [Te2], e3.stateReducers.push(Oe2), e3.visibleColumnsDeps.push(function(e4, t3) {
          var n3 = t3.instance;
          return [].concat(e4, [n3.state.groupBy]);
        }), e3.visibleColumns.push(Me2), e3.useInstance.push(Le2), e3.prepareRow.push(Ne2);
      };
      ze2.pluginName = "useGroupBy";
      var Te2 = function(e3, t3) {
        var n3 = t3.header;
        return [e3, { onClick: n3.canGroupBy ? function(e4) {
          e4.persist(), n3.toggleGroupBy();
        } : void 0, style: { cursor: n3.canGroupBy ? "pointer" : void 0 }, title: "Toggle GroupBy" }];
      };
      function Oe2(e3, t3, n3, o2) {
        if (t3.type === l2.init)
          return r2({ groupBy: [] }, e3);
        if (t3.type === l2.resetGroupBy)
          return r2({}, e3, { groupBy: o2.initialState.groupBy || [] });
        if (t3.type === l2.setGroupBy)
          return r2({}, e3, { groupBy: t3.value });
        if (t3.type === l2.toggleGroupBy) {
          var i2 = t3.columnId, u3 = t3.value, s2 = void 0 !== u3 ? u3 : !e3.groupBy.includes(i2);
          return r2({}, e3, s2 ? { groupBy: [].concat(e3.groupBy, [i2]) } : { groupBy: e3.groupBy.filter(function(e4) {
            return e4 !== i2;
          }) });
        }
      }
      function Me2(e3, t3) {
        var n3 = t3.instance.state.groupBy, o2 = n3.map(function(t4) {
          return e3.find(function(e4) {
            return e4.id === t4;
          });
        }).filter(Boolean), r3 = e3.filter(function(e4) {
          return !n3.includes(e4.id);
        });
        return (e3 = [].concat(o2, r3)).forEach(function(e4) {
          e4.isGrouped = n3.includes(e4.id), e4.groupedIndex = n3.indexOf(e4.id);
        }), e3;
      }
      var je2 = {};
      function Le2(e3) {
        var n3 = e3.data, o2 = e3.rows, i2 = e3.flatRows, u3 = e3.rowsById, s2 = e3.allColumns, a2 = e3.flatHeaders, c3 = e3.groupByFn, d3 = void 0 === c3 ? De2 : c3, p3 = e3.manualGroupBy, g3 = e3.aggregations, m3 = void 0 === g3 ? je2 : g3, y3 = e3.plugins, R3 = e3.state.groupBy, b3 = e3.dispatch, S3 = e3.autoResetGroupBy, C3 = void 0 === S3 || S3, x3 = e3.disableGroupBy, P3 = e3.defaultCanGroupBy, B3 = e3.getHooks;
        v2(y3, ["useColumnOrder", "useFilters"], "useGroupBy");
        var E3 = h2(e3);
        s2.forEach(function(t3) {
          var n4 = t3.accessor, o3 = t3.defaultGroupBy, r3 = t3.disableGroupBy;
          t3.canGroupBy = n4 ? I2(t3.canGroupBy, true !== r3 && void 0, true !== x3 && void 0, true) : I2(t3.canGroupBy, o3, P3, false), t3.canGroupBy && (t3.toggleGroupBy = function() {
            return e3.toggleGroupBy(t3.id);
          }), t3.Aggregated = t3.Aggregated || t3.Cell;
        });
        var F3 = t2.useCallback(function(e4, t3) {
          b3({ type: l2.toggleGroupBy, columnId: e4, value: t3 });
        }, [b3]), A3 = t2.useCallback(function(e4) {
          b3({ type: l2.setGroupBy, value: e4 });
        }, [b3]);
        a2.forEach(function(e4) {
          e4.getGroupByToggleProps = f2(B3().getGroupByToggleProps, { instance: E3(), header: e4 });
        });
        var k3 = t2.useMemo(function() {
          if (p3 || !R3.length)
            return [o2, i2, u3, He2, We2, i2, u3];
          var e4 = R3.filter(function(e5) {
            return s2.find(function(t4) {
              return t4.id === e5;
            });
          }), t3 = [], n4 = {}, l3 = [], a3 = {}, c4 = [], f3 = {}, g4 = function o3(i3, u4, p4) {
            if (void 0 === u4 && (u4 = 0), u4 === e4.length)
              return i3.map(function(e5) {
                return r2({}, e5, { depth: u4 });
              });
            var g5 = e4[u4], v3 = d3(i3, g5);
            return Object.entries(v3).map(function(r3, i4) {
              var d4 = r3[0], v4 = r3[1], h3 = g5 + ":" + d4, y4 = o3(v4, u4 + 1, h3 = p4 ? p4 + ">" + h3 : h3), w3 = u4 ? G2(v4, "leafRows") : v4, R4 = function(t4, n5, o4) {
                var r4 = {};
                return s2.forEach(function(i5) {
                  if (e4.includes(i5.id))
                    r4[i5.id] = n5[0] ? n5[0].values[i5.id] : null;
                  else {
                    var u5 = "function" == typeof i5.aggregate ? i5.aggregate : m3[i5.aggregate] || ke2[i5.aggregate];
                    if (u5) {
                      var l4 = n5.map(function(e5) {
                        return e5.values[i5.id];
                      }), s3 = t4.map(function(e5) {
                        var t5 = e5.values[i5.id];
                        if (!o4 && i5.aggregateValue) {
                          var n6 = "function" == typeof i5.aggregateValue ? i5.aggregateValue : m3[i5.aggregateValue] || ke2[i5.aggregateValue];
                          if (!n6)
                            throw console.info({ column: i5 }), new Error("React Table: Invalid column.aggregateValue option for column listed above");
                          t5 = n6(t5, e5, i5);
                        }
                        return t5;
                      });
                      r4[i5.id] = u5(s3, l4);
                    } else {
                      if (i5.aggregate)
                        throw console.info({ column: i5 }), new Error("React Table: Invalid column.aggregate option for column listed above");
                      r4[i5.id] = null;
                    }
                  }
                }), r4;
              }(w3, v4, u4), b4 = { id: h3, isGrouped: true, groupByID: g5, groupByVal: d4, values: R4, subRows: y4, leafRows: w3, depth: u4, index: i4 };
              return y4.forEach(function(e5) {
                t3.push(e5), n4[e5.id] = e5, e5.isGrouped ? (l3.push(e5), a3[e5.id] = e5) : (c4.push(e5), f3[e5.id] = e5);
              }), b4;
            });
          }(o2);
          return g4.forEach(function(e5) {
            t3.push(e5), n4[e5.id] = e5, e5.isGrouped ? (l3.push(e5), a3[e5.id] = e5) : (c4.push(e5), f3[e5.id] = e5);
          }), [g4, t3, n4, l3, a3, c4, f3];
        }, [p3, R3, o2, i2, u3, s2, m3, d3]), H3 = k3[0], W3 = k3[1], z3 = k3[2], T3 = k3[3], O3 = k3[4], M3 = k3[5], j3 = k3[6], L3 = h2(C3);
        w2(function() {
          L3() && b3({ type: l2.resetGroupBy });
        }, [b3, p3 ? null : n3]), Object.assign(e3, { preGroupedRows: o2, preGroupedFlatRow: i2, preGroupedRowsById: u3, groupedRows: H3, groupedFlatRows: W3, groupedRowsById: z3, onlyGroupedFlatRows: T3, onlyGroupedRowsById: O3, nonGroupedFlatRows: M3, nonGroupedRowsById: j3, rows: H3, flatRows: W3, rowsById: z3, toggleGroupBy: F3, setGroupBy: A3 });
      }
      function Ne2(e3) {
        e3.allCells.forEach(function(t3) {
          var n3;
          t3.isGrouped = t3.column.isGrouped && t3.column.id === e3.groupByID, t3.isPlaceholder = !t3.isGrouped && t3.column.isGrouped, t3.isAggregated = !t3.isGrouped && !t3.isPlaceholder && (null == (n3 = e3.subRows) ? void 0 : n3.length);
        });
      }
      function De2(e3, t3) {
        return e3.reduce(function(e4, n3, o2) {
          var r3 = "" + n3.values[t3];
          return e4[r3] = Array.isArray(e4[r3]) ? e4[r3] : [], e4[r3].push(n3), e4;
        }, {});
      }
      var Ve2 = /([0-9]+)/gm;
      function _e2(e3, t3) {
        return e3 === t3 ? 0 : e3 > t3 ? 1 : -1;
      }
      function Xe2(e3, t3, n3) {
        return [e3.values[n3], t3.values[n3]];
      }
      function qe2(e3) {
        return "number" == typeof e3 ? isNaN(e3) || e3 === 1 / 0 || e3 === -1 / 0 ? "" : String(e3) : "string" == typeof e3 ? e3 : "";
      }
      var Ke2 = Object.freeze({ __proto__: null, alphanumeric: function(e3, t3, n3) {
        var o2 = Xe2(e3, t3, n3), r3 = o2[0], i2 = o2[1];
        for (r3 = qe2(r3), i2 = qe2(i2), r3 = r3.split(Ve2).filter(Boolean), i2 = i2.split(Ve2).filter(Boolean); r3.length && i2.length; ) {
          var u3 = r3.shift(), l3 = i2.shift(), s2 = parseInt(u3, 10), a2 = parseInt(l3, 10), c3 = [s2, a2].sort();
          if (isNaN(c3[0])) {
            if (u3 > l3)
              return 1;
            if (l3 > u3)
              return -1;
          } else {
            if (isNaN(c3[1]))
              return isNaN(s2) ? -1 : 1;
            if (s2 > a2)
              return 1;
            if (a2 > s2)
              return -1;
          }
        }
        return r3.length - i2.length;
      }, datetime: function(e3, t3, n3) {
        var o2 = Xe2(e3, t3, n3), r3 = o2[0], i2 = o2[1];
        return _e2(r3 = r3.getTime(), i2 = i2.getTime());
      }, basic: function(e3, t3, n3) {
        var o2 = Xe2(e3, t3, n3);
        return _e2(o2[0], o2[1]);
      }, string: function(e3, t3, n3) {
        var o2 = Xe2(e3, t3, n3), r3 = o2[0], i2 = o2[1];
        for (r3 = r3.split("").filter(Boolean), i2 = i2.split("").filter(Boolean); r3.length && i2.length; ) {
          var u3 = r3.shift(), l3 = i2.shift(), s2 = u3.toLowerCase(), a2 = l3.toLowerCase();
          if (s2 > a2)
            return 1;
          if (a2 > s2)
            return -1;
          if (u3 > l3)
            return 1;
          if (l3 > u3)
            return -1;
        }
        return r3.length - i2.length;
      }, number: function(e3, t3, n3) {
        var o2 = Xe2(e3, t3, n3), r3 = o2[0], i2 = o2[1], u3 = /[^0-9.]/gi;
        return _e2(r3 = Number(String(r3).replace(u3, "")), i2 = Number(String(i2).replace(u3, "")));
      } });
      l2.resetSortBy = "resetSortBy", l2.setSortBy = "setSortBy", l2.toggleSortBy = "toggleSortBy", l2.clearSortBy = "clearSortBy", c2.sortType = "alphanumeric", c2.sortDescFirst = false;
      var Ue2 = function(e3) {
        e3.getSortByToggleProps = [$e2], e3.stateReducers.push(Je2), e3.useInstance.push(Ye2);
      };
      Ue2.pluginName = "useSortBy";
      var $e2 = function(e3, t3) {
        var n3 = t3.instance, o2 = t3.column, r3 = n3.isMultiSortEvent, i2 = void 0 === r3 ? function(e4) {
          return e4.shiftKey;
        } : r3;
        return [e3, { onClick: o2.canSort ? function(e4) {
          e4.persist(), o2.toggleSortBy(void 0, !n3.disableMultiSort && i2(e4));
        } : void 0, style: { cursor: o2.canSort ? "pointer" : void 0 }, title: o2.canSort ? "Toggle SortBy" : void 0 }];
      };
      function Je2(e3, t3, n3, o2) {
        if (t3.type === l2.init)
          return r2({ sortBy: [] }, e3);
        if (t3.type === l2.resetSortBy)
          return r2({}, e3, { sortBy: o2.initialState.sortBy || [] });
        if (t3.type === l2.clearSortBy)
          return r2({}, e3, { sortBy: e3.sortBy.filter(function(e4) {
            return e4.id !== t3.columnId;
          }) });
        if (t3.type === l2.setSortBy)
          return r2({}, e3, { sortBy: t3.sortBy });
        if (t3.type === l2.toggleSortBy) {
          var i2, u3 = t3.columnId, s2 = t3.desc, a2 = t3.multi, c3 = o2.allColumns, d3 = o2.disableMultiSort, f3 = o2.disableSortRemove, p3 = o2.disableMultiRemove, g3 = o2.maxMultiSortColCount, v3 = void 0 === g3 ? Number.MAX_SAFE_INTEGER : g3, m3 = e3.sortBy, h3 = c3.find(function(e4) {
            return e4.id === u3;
          }).sortDescFirst, y3 = m3.find(function(e4) {
            return e4.id === u3;
          }), w3 = m3.findIndex(function(e4) {
            return e4.id === u3;
          }), R3 = null != s2, b3 = [];
          return "toggle" !== (i2 = !d3 && a2 ? y3 ? "toggle" : "add" : w3 !== m3.length - 1 || 1 !== m3.length ? "replace" : y3 ? "toggle" : "replace") || f3 || R3 || a2 && p3 || !(y3 && y3.desc && !h3 || !y3.desc && h3) || (i2 = "remove"), "replace" === i2 ? b3 = [{ id: u3, desc: R3 ? s2 : h3 }] : "add" === i2 ? (b3 = [].concat(m3, [{ id: u3, desc: R3 ? s2 : h3 }])).splice(0, b3.length - v3) : "toggle" === i2 ? b3 = m3.map(function(e4) {
            return e4.id === u3 ? r2({}, e4, { desc: R3 ? s2 : !y3.desc }) : e4;
          }) : "remove" === i2 && (b3 = m3.filter(function(e4) {
            return e4.id !== u3;
          })), r2({}, e3, { sortBy: b3 });
        }
      }
      function Ye2(e3) {
        var n3 = e3.data, o2 = e3.rows, r3 = e3.flatRows, i2 = e3.allColumns, u3 = e3.orderByFn, s2 = void 0 === u3 ? Qe2 : u3, a2 = e3.sortTypes, c3 = e3.manualSortBy, d3 = e3.defaultCanSort, p3 = e3.disableSortBy, g3 = e3.flatHeaders, m3 = e3.state.sortBy, y3 = e3.dispatch, R3 = e3.plugins, b3 = e3.getHooks, S3 = e3.autoResetSortBy, C3 = void 0 === S3 || S3;
        v2(R3, ["useFilters", "useGlobalFilter", "useGroupBy", "usePivotColumns"], "useSortBy");
        var x3 = t2.useCallback(function(e4) {
          y3({ type: l2.setSortBy, sortBy: e4 });
        }, [y3]), P3 = t2.useCallback(function(e4, t3, n4) {
          y3({ type: l2.toggleSortBy, columnId: e4, desc: t3, multi: n4 });
        }, [y3]), B3 = h2(e3);
        g3.forEach(function(e4) {
          var t3 = e4.accessor, n4 = e4.canSort, o3 = e4.disableSortBy, r4 = e4.id, i3 = t3 ? I2(true !== o3 && void 0, true !== p3 && void 0, true) : I2(d3, n4, false);
          e4.canSort = i3, e4.canSort && (e4.toggleSortBy = function(t4, n5) {
            return P3(e4.id, t4, n5);
          }, e4.clearSortBy = function() {
            y3({ type: l2.clearSortBy, columnId: e4.id });
          }), e4.getSortByToggleProps = f2(b3().getSortByToggleProps, { instance: B3(), column: e4 });
          var u4 = m3.find(function(e5) {
            return e5.id === r4;
          });
          e4.isSorted = !!u4, e4.sortedIndex = m3.findIndex(function(e5) {
            return e5.id === r4;
          }), e4.isSortedDesc = e4.isSorted ? u4.desc : void 0;
        });
        var E3 = t2.useMemo(function() {
          if (c3 || !m3.length)
            return [o2, r3];
          var e4 = [], t3 = m3.filter(function(e5) {
            return i2.find(function(t4) {
              return t4.id === e5.id;
            });
          });
          return [function n4(o3) {
            var r4 = s2(o3, t3.map(function(e5) {
              var t4 = i2.find(function(t5) {
                return t5.id === e5.id;
              });
              if (!t4)
                throw new Error("React-Table: Could not find a column with id: " + e5.id + " while sorting");
              var n5 = t4.sortType, o4 = F2(n5) || (a2 || {})[n5] || Ke2[n5];
              if (!o4)
                throw new Error("React-Table: Could not find a valid sortType of '" + n5 + "' for column '" + e5.id + "'.");
              return function(t5, n6) {
                return o4(t5, n6, e5.id, e5.desc);
              };
            }), t3.map(function(e5) {
              var t4 = i2.find(function(t5) {
                return t5.id === e5.id;
              });
              return t4 && t4.sortInverted ? e5.desc : !e5.desc;
            }));
            return r4.forEach(function(t4) {
              e4.push(t4), t4.subRows && 0 !== t4.subRows.length && (t4.subRows = n4(t4.subRows));
            }), r4;
          }(o2), e4];
        }, [c3, m3, o2, r3, i2, s2, a2]), G3 = E3[0], A3 = E3[1], k3 = h2(C3);
        w2(function() {
          k3() && y3({ type: l2.resetSortBy });
        }, [c3 ? null : n3]), Object.assign(e3, { preSortedRows: o2, preSortedFlatRows: r3, sortedRows: G3, sortedFlatRows: A3, rows: G3, flatRows: A3, setSortBy: x3, toggleSortBy: P3 });
      }
      function Qe2(e3, t3, n3) {
        return [].concat(e3).sort(function(e4, o2) {
          for (var r3 = 0; r3 < t3.length; r3 += 1) {
            var i2 = t3[r3], u3 = false === n3[r3] || "desc" === n3[r3], l3 = i2(e4, o2);
            if (0 !== l3)
              return u3 ? -l3 : l3;
          }
          return n3[0] ? e4.index - o2.index : o2.index - e4.index;
        });
      }
      l2.resetPage = "resetPage", l2.gotoPage = "gotoPage", l2.setPageSize = "setPageSize";
      var Ze2 = function(e3) {
        e3.stateReducers.push(et), e3.useInstance.push(tt);
      };
      function et(e3, t3, n3, o2) {
        if (t3.type === l2.init)
          return r2({ pageSize: 10, pageIndex: 0 }, e3);
        if (t3.type === l2.resetPage)
          return r2({}, e3, { pageIndex: o2.initialState.pageIndex || 0 });
        if (t3.type === l2.gotoPage) {
          var i2 = o2.pageCount, u3 = o2.page, s2 = m2(t3.pageIndex, e3.pageIndex), a2 = false;
          return s2 > e3.pageIndex ? a2 = -1 === i2 ? u3.length >= e3.pageSize : s2 < i2 : s2 < e3.pageIndex && (a2 = s2 > -1), a2 ? r2({}, e3, { pageIndex: s2 }) : e3;
        }
        if (t3.type === l2.setPageSize) {
          var c3 = t3.pageSize, d3 = e3.pageSize * e3.pageIndex;
          return r2({}, e3, { pageIndex: Math.floor(d3 / c3), pageSize: c3 });
        }
      }
      function tt(e3) {
        var n3 = e3.rows, o2 = e3.autoResetPage, r3 = void 0 === o2 || o2, i2 = e3.manualExpandedKey, u3 = void 0 === i2 ? "expanded" : i2, s2 = e3.plugins, a2 = e3.pageCount, c3 = e3.paginateExpandedRows, d3 = void 0 === c3 || c3, f3 = e3.expandSubRows, p3 = void 0 === f3 || f3, g3 = e3.state, m3 = g3.pageSize, y3 = g3.pageIndex, R3 = g3.expanded, b3 = g3.globalFilter, S3 = g3.filters, C3 = g3.groupBy, x3 = g3.sortBy, P3 = e3.dispatch, B3 = e3.data, E3 = e3.manualPagination;
        v2(s2, ["useGlobalFilter", "useFilters", "useGroupBy", "useSortBy", "useExpanded"], "usePagination");
        var I3 = h2(r3);
        w2(function() {
          I3() && P3({ type: l2.resetPage });
        }, [P3, E3 ? null : B3, b3, S3, C3, x3]);
        var F3 = E3 ? a2 : Math.ceil(n3.length / m3), G3 = t2.useMemo(function() {
          return F3 > 0 ? [].concat(new Array(F3)).fill(null).map(function(e4, t3) {
            return t3;
          }) : [];
        }, [F3]), k3 = t2.useMemo(function() {
          var e4;
          if (E3)
            e4 = n3;
          else {
            var t3 = m3 * y3, o3 = t3 + m3;
            e4 = n3.slice(t3, o3);
          }
          return d3 ? e4 : A2(e4, { manualExpandedKey: u3, expanded: R3, expandSubRows: p3 });
        }, [p3, R3, u3, E3, y3, m3, d3, n3]), H3 = y3 > 0, W3 = -1 === F3 ? k3.length >= m3 : y3 < F3 - 1, z3 = t2.useCallback(function(e4) {
          P3({ type: l2.gotoPage, pageIndex: e4 });
        }, [P3]), T3 = t2.useCallback(function() {
          return z3(function(e4) {
            return e4 - 1;
          });
        }, [z3]), O3 = t2.useCallback(function() {
          return z3(function(e4) {
            return e4 + 1;
          });
        }, [z3]), M3 = t2.useCallback(function(e4) {
          P3({ type: l2.setPageSize, pageSize: e4 });
        }, [P3]);
        Object.assign(e3, { pageOptions: G3, pageCount: F3, page: k3, canPreviousPage: H3, canNextPage: W3, gotoPage: z3, previousPage: T3, nextPage: O3, setPageSize: M3 });
      }
      Ze2.pluginName = "usePagination", l2.resetPivot = "resetPivot", l2.togglePivot = "togglePivot";
      var nt = function(e3) {
        e3.getPivotToggleProps = [rt], e3.stateReducers.push(it2), e3.useInstanceAfterData.push(ut2), e3.allColumns.push(lt2), e3.accessValue.push(st2), e3.materializedColumns.push(at2), e3.materializedColumnsDeps.push(ct2), e3.visibleColumns.push(dt), e3.visibleColumnsDeps.push(ft), e3.useInstance.push(pt2), e3.prepareRow.push(gt);
      };
      nt.pluginName = "usePivotColumns";
      var ot2 = [], rt = function(e3, t3) {
        var n3 = t3.header;
        return [e3, { onClick: n3.canPivot ? function(e4) {
          e4.persist(), n3.togglePivot();
        } : void 0, style: { cursor: n3.canPivot ? "pointer" : void 0 }, title: "Toggle Pivot" }];
      };
      function it2(e3, t3, n3, o2) {
        if (t3.type === l2.init)
          return r2({ pivotColumns: ot2 }, e3);
        if (t3.type === l2.resetPivot)
          return r2({}, e3, { pivotColumns: o2.initialState.pivotColumns || ot2 });
        if (t3.type === l2.togglePivot) {
          var i2 = t3.columnId, u3 = t3.value, s2 = void 0 !== u3 ? u3 : !e3.pivotColumns.includes(i2);
          return r2({}, e3, s2 ? { pivotColumns: [].concat(e3.pivotColumns, [i2]) } : { pivotColumns: e3.pivotColumns.filter(function(e4) {
            return e4 !== i2;
          }) });
        }
      }
      function ut2(e3) {
        e3.allColumns.forEach(function(t3) {
          t3.isPivotSource = e3.state.pivotColumns.includes(t3.id);
        });
      }
      function lt2(e3, t3) {
        var n3 = t3.instance;
        return e3.forEach(function(e4) {
          e4.isPivotSource = n3.state.pivotColumns.includes(e4.id), e4.uniqueValues = /* @__PURE__ */ new Set();
        }), e3;
      }
      function st2(e3, t3) {
        var n3 = t3.column;
        return n3.uniqueValues && void 0 !== e3 && n3.uniqueValues.add(e3), e3;
      }
      function at2(e3, t3) {
        var n3 = t3.instance, o2 = n3.allColumns, i2 = n3.state;
        if (!i2.pivotColumns.length || !i2.groupBy || !i2.groupBy.length)
          return e3;
        var u3 = i2.pivotColumns.map(function(e4) {
          return o2.find(function(t4) {
            return t4.id === e4;
          });
        }).filter(Boolean), l3 = o2.filter(function(e4) {
          return !e4.isPivotSource && !i2.groupBy.includes(e4.id) && !i2.pivotColumns.includes(e4.id);
        }), s2 = C2(function e4(t4, n4, o3) {
          void 0 === t4 && (t4 = 0), void 0 === o3 && (o3 = []);
          var i3 = u3[t4];
          return i3 ? Array.from(i3.uniqueValues).sort().map(function(u4) {
            var l4 = r2({}, i3, { Header: i3.PivotHeader || "string" == typeof i3.header ? i3.Header + ": " + u4 : u4, isPivotGroup: true, parent: n4, depth: t4, id: n4 ? n4.id + "." + i3.id + "." + u4 : i3.id + "." + u4, pivotValue: u4 });
            return l4.columns = e4(t4 + 1, l4, [].concat(o3, [function(e5) {
              return e5.values[i3.id] === u4;
            }])), l4;
          }) : l3.map(function(e5) {
            return r2({}, e5, { canPivot: false, isPivoted: true, parent: n4, depth: t4, id: "" + (n4 ? n4.id + "." + e5.id : e5.id), accessor: function(t5, n5, r3) {
              if (o3.every(function(e6) {
                return e6(r3);
              }))
                return r3.values[e5.id];
            } });
          });
        }());
        return [].concat(e3, s2);
      }
      function ct2(e3, t3) {
        var n3 = t3.instance.state, o2 = n3.pivotColumns, r3 = n3.groupBy;
        return [].concat(e3, [o2, r3]);
      }
      function dt(e3, t3) {
        var n3 = t3.instance.state;
        return e3 = e3.filter(function(e4) {
          return !e4.isPivotSource;
        }), n3.pivotColumns.length && n3.groupBy && n3.groupBy.length && (e3 = e3.filter(function(e4) {
          return e4.isGrouped || e4.isPivoted;
        })), e3;
      }
      function ft(e3, t3) {
        var n3 = t3.instance;
        return [].concat(e3, [n3.state.pivotColumns, n3.state.groupBy]);
      }
      function pt2(e3) {
        var t3 = e3.columns, n3 = e3.allColumns, o2 = e3.flatHeaders, r3 = e3.getHooks, i2 = e3.plugins, u3 = e3.dispatch, s2 = e3.autoResetPivot, a2 = void 0 === s2 || s2, c3 = e3.manaulPivot, d3 = e3.disablePivot, p3 = e3.defaultCanPivot;
        v2(i2, ["useGroupBy"], "usePivotColumns");
        var g3 = h2(e3);
        n3.forEach(function(t4) {
          var n4 = t4.accessor, o3 = t4.defaultPivot, r4 = t4.disablePivot;
          t4.canPivot = n4 ? I2(t4.canPivot, true !== r4 && void 0, true !== d3 && void 0, true) : I2(t4.canPivot, o3, p3, false), t4.canPivot && (t4.togglePivot = function() {
            return e3.togglePivot(t4.id);
          }), t4.Aggregated = t4.Aggregated || t4.Cell;
        });
        o2.forEach(function(e4) {
          e4.getPivotToggleProps = f2(r3().getPivotToggleProps, { instance: g3(), header: e4 });
        });
        var m3 = h2(a2);
        w2(function() {
          m3() && u3({ type: l2.resetPivot });
        }, [u3, c3 ? null : t3]), Object.assign(e3, { togglePivot: function(e4, t4) {
          u3({ type: l2.togglePivot, columnId: e4, value: t4 });
        } });
      }
      function gt(e3) {
        e3.allCells.forEach(function(e4) {
          e4.isPivoted = e4.column.isPivoted;
        });
      }
      l2.resetSelectedRows = "resetSelectedRows", l2.toggleAllRowsSelected = "toggleAllRowsSelected", l2.toggleRowSelected = "toggleRowSelected", l2.toggleAllPageRowsSelected = "toggleAllPageRowsSelected";
      var vt = function(e3) {
        e3.getToggleRowSelectedProps = [mt], e3.getToggleAllRowsSelectedProps = [ht], e3.getToggleAllPageRowsSelectedProps = [yt], e3.stateReducers.push(wt), e3.useInstance.push(Rt), e3.prepareRow.push(bt);
      };
      vt.pluginName = "useRowSelect";
      var mt = function(e3, t3) {
        var n3 = t3.instance, o2 = t3.row, r3 = n3.manualRowSelectedKey, i2 = void 0 === r3 ? "isSelected" : r3;
        return [e3, { onChange: function(e4) {
          o2.toggleRowSelected(e4.target.checked);
        }, style: { cursor: "pointer" }, checked: !(!o2.original || !o2.original[i2]) || o2.isSelected, title: "Toggle Row Selected", indeterminate: o2.isSomeSelected }];
      }, ht = function(e3, t3) {
        var n3 = t3.instance;
        return [e3, { onChange: function(e4) {
          n3.toggleAllRowsSelected(e4.target.checked);
        }, style: { cursor: "pointer" }, checked: n3.isAllRowsSelected, title: "Toggle All Rows Selected", indeterminate: Boolean(!n3.isAllRowsSelected && Object.keys(n3.state.selectedRowIds).length) }];
      }, yt = function(e3, t3) {
        var n3 = t3.instance;
        return [e3, { onChange: function(e4) {
          n3.toggleAllPageRowsSelected(e4.target.checked);
        }, style: { cursor: "pointer" }, checked: n3.isAllPageRowsSelected, title: "Toggle All Current Page Rows Selected", indeterminate: Boolean(!n3.isAllPageRowsSelected && n3.page.some(function(e4) {
          var t4 = e4.id;
          return n3.state.selectedRowIds[t4];
        })) }];
      };
      function wt(e3, t3, n3, o2) {
        if (t3.type === l2.init)
          return r2({ selectedRowIds: {} }, e3);
        if (t3.type === l2.resetSelectedRows)
          return r2({}, e3, { selectedRowIds: o2.initialState.selectedRowIds || {} });
        if (t3.type === l2.toggleAllRowsSelected) {
          var i2 = t3.value, u3 = o2.isAllRowsSelected, s2 = o2.rowsById, a2 = o2.nonGroupedRowsById, c3 = void 0 === a2 ? s2 : a2, d3 = void 0 !== i2 ? i2 : !u3, f3 = Object.assign({}, e3.selectedRowIds);
          return d3 ? Object.keys(c3).forEach(function(e4) {
            f3[e4] = true;
          }) : Object.keys(c3).forEach(function(e4) {
            delete f3[e4];
          }), r2({}, e3, { selectedRowIds: f3 });
        }
        if (t3.type === l2.toggleRowSelected) {
          var p3 = t3.id, g3 = t3.value, v3 = o2.rowsById, m3 = o2.selectSubRows, h3 = void 0 === m3 || m3, y3 = o2.getSubRows, w3 = e3.selectedRowIds[p3], R3 = void 0 !== g3 ? g3 : !w3;
          if (w3 === R3)
            return e3;
          var b3 = r2({}, e3.selectedRowIds);
          return function e4(t4) {
            var n4 = v3[t4];
            if (n4 && (n4.isGrouped || (R3 ? b3[t4] = true : delete b3[t4]), h3 && y3(n4)))
              return y3(n4).forEach(function(t5) {
                return e4(t5.id);
              });
          }(p3), r2({}, e3, { selectedRowIds: b3 });
        }
        if (t3.type === l2.toggleAllPageRowsSelected) {
          var S3 = t3.value, C3 = o2.page, x3 = o2.rowsById, P3 = o2.selectSubRows, B3 = void 0 === P3 || P3, E3 = o2.isAllPageRowsSelected, I3 = o2.getSubRows, F3 = void 0 !== S3 ? S3 : !E3, G3 = r2({}, e3.selectedRowIds);
          return C3.forEach(function(e4) {
            return function e5(t4) {
              var n4 = x3[t4];
              if (n4.isGrouped || (F3 ? G3[t4] = true : delete G3[t4]), B3 && I3(n4))
                return I3(n4).forEach(function(t5) {
                  return e5(t5.id);
                });
            }(e4.id);
          }), r2({}, e3, { selectedRowIds: G3 });
        }
        return e3;
      }
      function Rt(e3) {
        var n3 = e3.data, o2 = e3.rows, r3 = e3.getHooks, i2 = e3.plugins, u3 = e3.rowsById, s2 = e3.nonGroupedRowsById, a2 = void 0 === s2 ? u3 : s2, c3 = e3.autoResetSelectedRows, d3 = void 0 === c3 || c3, p3 = e3.state.selectedRowIds, g3 = e3.selectSubRows, m3 = void 0 === g3 || g3, y3 = e3.dispatch, R3 = e3.page, b3 = e3.getSubRows;
        v2(i2, ["useFilters", "useGroupBy", "useSortBy", "useExpanded", "usePagination"], "useRowSelect");
        var S3 = t2.useMemo(function() {
          var e4 = [];
          return o2.forEach(function(t3) {
            var n4 = m3 ? function e5(t4, n5, o3) {
              if (n5[t4.id])
                return true;
              var r4 = o3(t4);
              if (r4 && r4.length) {
                var i3 = true, u4 = false;
                return r4.forEach(function(t5) {
                  u4 && !i3 || (e5(t5, n5, o3) ? u4 = true : i3 = false);
                }), !!i3 || !!u4 && null;
              }
              return false;
            }(t3, p3, b3) : !!p3[t3.id];
            t3.isSelected = !!n4, t3.isSomeSelected = null === n4, n4 && e4.push(t3);
          }), e4;
        }, [o2, m3, p3, b3]), C3 = Boolean(Object.keys(a2).length && Object.keys(p3).length), x3 = C3;
        C3 && Object.keys(a2).some(function(e4) {
          return !p3[e4];
        }) && (C3 = false), C3 || R3 && R3.length && R3.some(function(e4) {
          var t3 = e4.id;
          return !p3[t3];
        }) && (x3 = false);
        var P3 = h2(d3);
        w2(function() {
          P3() && y3({ type: l2.resetSelectedRows });
        }, [y3, n3]);
        var B3 = t2.useCallback(function(e4) {
          return y3({ type: l2.toggleAllRowsSelected, value: e4 });
        }, [y3]), E3 = t2.useCallback(function(e4) {
          return y3({ type: l2.toggleAllPageRowsSelected, value: e4 });
        }, [y3]), I3 = t2.useCallback(function(e4, t3) {
          return y3({ type: l2.toggleRowSelected, id: e4, value: t3 });
        }, [y3]), F3 = h2(e3), G3 = f2(r3().getToggleAllRowsSelectedProps, { instance: F3() }), A3 = f2(r3().getToggleAllPageRowsSelectedProps, { instance: F3() });
        Object.assign(e3, { selectedFlatRows: S3, isAllRowsSelected: C3, isAllPageRowsSelected: x3, toggleRowSelected: I3, toggleAllRowsSelected: B3, getToggleAllRowsSelectedProps: G3, getToggleAllPageRowsSelectedProps: A3, toggleAllPageRowsSelected: E3 });
      }
      function bt(e3, t3) {
        var n3 = t3.instance;
        e3.toggleRowSelected = function(t4) {
          return n3.toggleRowSelected(e3.id, t4);
        }, e3.getToggleRowSelectedProps = f2(n3.getHooks().getToggleRowSelectedProps, { instance: n3, row: e3 });
      }
      var St = function(e3) {
        return {};
      }, Ct = function(e3) {
        return {};
      };
      l2.setRowState = "setRowState", l2.setCellState = "setCellState", l2.resetRowState = "resetRowState";
      var xt = function(e3) {
        e3.stateReducers.push(Pt), e3.useInstance.push(Bt), e3.prepareRow.push(Et);
      };
      function Pt(e3, t3, n3, o2) {
        var i2 = o2.initialRowStateAccessor, u3 = void 0 === i2 ? St : i2, s2 = o2.initialCellStateAccessor, a2 = void 0 === s2 ? Ct : s2, c3 = o2.rowsById;
        if (t3.type === l2.init)
          return r2({ rowState: {} }, e3);
        if (t3.type === l2.resetRowState)
          return r2({}, e3, { rowState: o2.initialState.rowState || {} });
        if (t3.type === l2.setRowState) {
          var d3, f3 = t3.rowId, p3 = t3.value, g3 = void 0 !== e3.rowState[f3] ? e3.rowState[f3] : u3(c3[f3]);
          return r2({}, e3, { rowState: r2({}, e3.rowState, (d3 = {}, d3[f3] = m2(p3, g3), d3)) });
        }
        if (t3.type === l2.setCellState) {
          var v3, h3, y3, w3, R3, b3 = t3.rowId, S3 = t3.columnId, C3 = t3.value, x3 = void 0 !== e3.rowState[b3] ? e3.rowState[b3] : u3(c3[b3]), P3 = void 0 !== (null == x3 ? void 0 : null == (v3 = x3.cellState) ? void 0 : v3[S3]) ? x3.cellState[S3] : a2(null == (h3 = c3[b3]) ? void 0 : null == (y3 = h3.cells) ? void 0 : y3.find(function(e4) {
            return e4.column.id === S3;
          }));
          return r2({}, e3, { rowState: r2({}, e3.rowState, (R3 = {}, R3[b3] = r2({}, x3, { cellState: r2({}, x3.cellState || {}, (w3 = {}, w3[S3] = m2(C3, P3), w3)) }), R3)) });
        }
      }
      function Bt(e3) {
        var n3 = e3.autoResetRowState, o2 = void 0 === n3 || n3, r3 = e3.data, i2 = e3.dispatch, u3 = t2.useCallback(function(e4, t3) {
          return i2({ type: l2.setRowState, rowId: e4, value: t3 });
        }, [i2]), s2 = t2.useCallback(function(e4, t3, n4) {
          return i2({ type: l2.setCellState, rowId: e4, columnId: t3, value: n4 });
        }, [i2]), a2 = h2(o2);
        w2(function() {
          a2() && i2({ type: l2.resetRowState });
        }, [r3]), Object.assign(e3, { setRowState: u3, setCellState: s2 });
      }
      function Et(e3, t3) {
        var n3 = t3.instance, o2 = n3.initialRowStateAccessor, r3 = void 0 === o2 ? St : o2, i2 = n3.initialCellStateAccessor, u3 = void 0 === i2 ? Ct : i2, l3 = n3.state.rowState;
        e3 && (e3.state = void 0 !== l3[e3.id] ? l3[e3.id] : r3(e3), e3.setState = function(t4) {
          return n3.setRowState(e3.id, t4);
        }, e3.cells.forEach(function(t4) {
          e3.state.cellState || (e3.state.cellState = {}), t4.state = void 0 !== e3.state.cellState[t4.column.id] ? e3.state.cellState[t4.column.id] : u3(t4), t4.setState = function(o3) {
            return n3.setCellState(e3.id, t4.column.id, o3);
          };
        }));
      }
      xt.pluginName = "useRowState", l2.resetColumnOrder = "resetColumnOrder", l2.setColumnOrder = "setColumnOrder";
      var It = function(e3) {
        e3.stateReducers.push(Ft), e3.visibleColumnsDeps.push(function(e4, t3) {
          var n3 = t3.instance;
          return [].concat(e4, [n3.state.columnOrder]);
        }), e3.visibleColumns.push(Gt), e3.useInstance.push(At);
      };
      function Ft(e3, t3, n3, o2) {
        return t3.type === l2.init ? r2({ columnOrder: [] }, e3) : t3.type === l2.resetColumnOrder ? r2({}, e3, { columnOrder: o2.initialState.columnOrder || [] }) : t3.type === l2.setColumnOrder ? r2({}, e3, { columnOrder: m2(t3.columnOrder, e3.columnOrder) }) : void 0;
      }
      function Gt(e3, t3) {
        var n3 = t3.instance.state.columnOrder;
        if (!n3 || !n3.length)
          return e3;
        for (var o2 = [].concat(n3), r3 = [].concat(e3), i2 = [], u3 = function() {
          var e4 = o2.shift(), t4 = r3.findIndex(function(t5) {
            return t5.id === e4;
          });
          t4 > -1 && i2.push(r3.splice(t4, 1)[0]);
        }; r3.length && o2.length; )
          u3();
        return [].concat(i2, r3);
      }
      function At(e3) {
        var n3 = e3.dispatch;
        e3.setColumnOrder = t2.useCallback(function(e4) {
          return n3({ type: l2.setColumnOrder, columnOrder: e4 });
        }, [n3]);
      }
      It.pluginName = "useColumnOrder", c2.canResize = true, l2.columnStartResizing = "columnStartResizing", l2.columnResizing = "columnResizing", l2.columnDoneResizing = "columnDoneResizing", l2.resetResize = "resetResize";
      var kt = function(e3) {
        e3.getResizerProps = [Ht], e3.getHeaderProps.push({ style: { position: "relative" } }), e3.stateReducers.push(Wt), e3.useInstance.push(Tt), e3.useInstanceBeforeDimensions.push(zt);
      }, Ht = function(e3, t3) {
        var n3 = t3.instance, o2 = t3.header, r3 = n3.dispatch, i2 = function(e4, t4) {
          var n4 = false;
          if ("touchstart" === e4.type) {
            if (e4.touches && e4.touches.length > 1)
              return;
            n4 = true;
          }
          var o3, i3, u3 = function(e5) {
            var t5 = [];
            return function e6(n5) {
              n5.columns && n5.columns.length && n5.columns.map(e6);
              t5.push(n5);
            }(e5), t5;
          }(t4).map(function(e5) {
            return [e5.id, e5.totalWidth];
          }), s2 = n4 ? Math.round(e4.touches[0].clientX) : e4.clientX, a2 = function() {
            window.cancelAnimationFrame(o3), o3 = null, r3({ type: l2.columnDoneResizing });
          }, c3 = function() {
            window.cancelAnimationFrame(o3), o3 = null, r3({ type: l2.columnResizing, clientX: i3 });
          }, d3 = function(e5) {
            i3 = e5, o3 || (o3 = window.requestAnimationFrame(c3));
          }, f3 = { mouse: { moveEvent: "mousemove", moveHandler: function(e5) {
            return d3(e5.clientX);
          }, upEvent: "mouseup", upHandler: function(e5) {
            document.removeEventListener("mousemove", f3.mouse.moveHandler), document.removeEventListener("mouseup", f3.mouse.upHandler), a2();
          } }, touch: { moveEvent: "touchmove", moveHandler: function(e5) {
            return e5.cancelable && (e5.preventDefault(), e5.stopPropagation()), d3(e5.touches[0].clientX), false;
          }, upEvent: "touchend", upHandler: function(e5) {
            document.removeEventListener(f3.touch.moveEvent, f3.touch.moveHandler), document.removeEventListener(f3.touch.upEvent, f3.touch.moveHandler), a2();
          } } }, p3 = n4 ? f3.touch : f3.mouse, g3 = !!function() {
            if ("boolean" == typeof z2)
              return z2;
            var e5 = false;
            try {
              var t5 = { get passive() {
                return e5 = true, false;
              } };
              window.addEventListener("test", null, t5), window.removeEventListener("test", null, t5);
            } catch (t6) {
              e5 = false;
            }
            return z2 = e5;
          }() && { passive: false };
          document.addEventListener(p3.moveEvent, p3.moveHandler, g3), document.addEventListener(p3.upEvent, p3.upHandler, g3), r3({ type: l2.columnStartResizing, columnId: t4.id, columnWidth: t4.totalWidth, headerIdWidths: u3, clientX: s2 });
        };
        return [e3, { onMouseDown: function(e4) {
          return e4.persist() || i2(e4, o2);
        }, onTouchStart: function(e4) {
          return e4.persist() || i2(e4, o2);
        }, style: { cursor: "col-resize" }, draggable: false, role: "separator" }];
      };
      function Wt(e3, t3) {
        if (t3.type === l2.init)
          return r2({ columnResizing: { columnWidths: {} } }, e3);
        if (t3.type === l2.resetResize)
          return r2({}, e3, { columnResizing: { columnWidths: {} } });
        if (t3.type === l2.columnStartResizing) {
          var n3 = t3.clientX, o2 = t3.columnId, i2 = t3.columnWidth, u3 = t3.headerIdWidths;
          return r2({}, e3, { columnResizing: r2({}, e3.columnResizing, { startX: n3, headerIdWidths: u3, columnWidth: i2, isResizingColumn: o2 }) });
        }
        if (t3.type === l2.columnResizing) {
          var s2 = t3.clientX, a2 = e3.columnResizing, c3 = a2.startX, d3 = a2.columnWidth, f3 = a2.headerIdWidths, p3 = (s2 - c3) / d3, g3 = {};
          return (void 0 === f3 ? [] : f3).forEach(function(e4) {
            var t4 = e4[0], n4 = e4[1];
            g3[t4] = Math.max(n4 + n4 * p3, 0);
          }), r2({}, e3, { columnResizing: r2({}, e3.columnResizing, { columnWidths: r2({}, e3.columnResizing.columnWidths, {}, g3) }) });
        }
        return t3.type === l2.columnDoneResizing ? r2({}, e3, { columnResizing: r2({}, e3.columnResizing, { startX: null, isResizingColumn: null }) }) : void 0;
      }
      kt.pluginName = "useResizeColumns";
      var zt = function(e3) {
        var t3 = e3.flatHeaders, n3 = e3.disableResizing, o2 = e3.getHooks, r3 = e3.state.columnResizing, i2 = h2(e3);
        t3.forEach(function(e4) {
          var t4 = I2(true !== e4.disableResizing && void 0, true !== n3 && void 0, true);
          e4.canResize = t4, e4.width = r3.columnWidths[e4.id] || e4.originalWidth || e4.width, e4.isResizing = r3.isResizingColumn === e4.id, t4 && (e4.getResizerProps = f2(o2().getResizerProps, { instance: i2(), header: e4 }));
        });
      };
      function Tt(e3) {
        var n3 = e3.plugins, o2 = e3.dispatch, r3 = e3.autoResetResize, i2 = void 0 === r3 || r3, u3 = e3.columns;
        v2(n3, ["useAbsoluteLayout"], "useResizeColumns");
        var s2 = h2(i2);
        w2(function() {
          s2() && o2({ type: l2.resetResize });
        }, [u3]);
        var a2 = t2.useCallback(function() {
          return o2({ type: l2.resetResize });
        }, [o2]);
        Object.assign(e3, { resetResizing: a2 });
      }
      var Ot = { position: "absolute", top: 0 }, Mt = function(e3) {
        e3.getTableBodyProps.push(jt), e3.getRowProps.push(jt), e3.getHeaderGroupProps.push(jt), e3.getFooterGroupProps.push(jt), e3.getHeaderProps.push(function(e4, t3) {
          var n3 = t3.column;
          return [e4, { style: r2({}, Ot, { left: n3.totalLeft + "px", width: n3.totalWidth + "px" }) }];
        }), e3.getCellProps.push(function(e4, t3) {
          var n3 = t3.cell;
          return [e4, { style: r2({}, Ot, { left: n3.column.totalLeft + "px", width: n3.column.totalWidth + "px" }) }];
        }), e3.getFooterProps.push(function(e4, t3) {
          var n3 = t3.column;
          return [e4, { style: r2({}, Ot, { left: n3.totalLeft + "px", width: n3.totalWidth + "px" }) }];
        });
      };
      Mt.pluginName = "useAbsoluteLayout";
      var jt = function(e3, t3) {
        return [e3, { style: { position: "relative", width: t3.instance.totalColumnsWidth + "px" } }];
      }, Lt = { display: "inline-block", boxSizing: "border-box" }, Nt = function(e3, t3) {
        return [e3, { style: { display: "flex", width: t3.instance.totalColumnsWidth + "px" } }];
      }, Dt = function(e3) {
        e3.getRowProps.push(Nt), e3.getHeaderGroupProps.push(Nt), e3.getFooterGroupProps.push(Nt), e3.getHeaderProps.push(function(e4, t3) {
          var n3 = t3.column;
          return [e4, { style: r2({}, Lt, { width: n3.totalWidth + "px" }) }];
        }), e3.getCellProps.push(function(e4, t3) {
          var n3 = t3.cell;
          return [e4, { style: r2({}, Lt, { width: n3.column.totalWidth + "px" }) }];
        }), e3.getFooterProps.push(function(e4, t3) {
          var n3 = t3.column;
          return [e4, { style: r2({}, Lt, { width: n3.totalWidth + "px" }) }];
        });
      };
      function Vt(e3) {
        e3.getTableProps.push(_t), e3.getRowProps.push(Xt), e3.getHeaderGroupProps.push(Xt), e3.getFooterGroupProps.push(Xt), e3.getHeaderProps.push(qt), e3.getCellProps.push(Kt), e3.getFooterProps.push(Ut);
      }
      Dt.pluginName = "useBlockLayout", Vt.pluginName = "useFlexLayout";
      var _t = function(e3, t3) {
        return [e3, { style: { minWidth: t3.instance.totalColumnsMinWidth + "px" } }];
      }, Xt = function(e3, t3) {
        return [e3, { style: { display: "flex", flex: "1 0 auto", minWidth: t3.instance.totalColumnsMinWidth + "px" } }];
      }, qt = function(e3, t3) {
        var n3 = t3.column;
        return [e3, { style: { boxSizing: "border-box", flex: n3.totalFlexWidth ? n3.totalFlexWidth + " 0 auto" : void 0, minWidth: n3.totalMinWidth + "px", width: n3.totalWidth + "px" } }];
      }, Kt = function(e3, t3) {
        var n3 = t3.cell;
        return [e3, { style: { boxSizing: "border-box", flex: n3.column.totalFlexWidth + " 0 auto", minWidth: n3.column.totalMinWidth + "px", width: n3.column.totalWidth + "px" } }];
      }, Ut = function(e3, t3) {
        var n3 = t3.column;
        return [e3, { style: { boxSizing: "border-box", flex: n3.totalFlexWidth ? n3.totalFlexWidth + " 0 auto" : void 0, minWidth: n3.totalMinWidth + "px", width: n3.totalWidth + "px" } }];
      };
      function $t(e3) {
        e3.stateReducers.push(Zt), e3.getTableProps.push(Jt), e3.getHeaderProps.push(Yt), e3.getRowProps.push(Qt);
      }
      l2.columnStartResizing = "columnStartResizing", l2.columnResizing = "columnResizing", l2.columnDoneResizing = "columnDoneResizing", l2.resetResize = "resetResize", $t.pluginName = "useGridLayout";
      var Jt = function(e3, t3) {
        var n3 = t3.instance;
        return [e3, { style: { display: "grid", gridTemplateColumns: n3.visibleColumns.map(function(e4) {
          var t4;
          return n3.state.gridLayout.columnWidths[e4.id] ? n3.state.gridLayout.columnWidths[e4.id] + "px" : (null == (t4 = n3.state.columnResizing) ? void 0 : t4.isResizingColumn) ? n3.state.gridLayout.startWidths[e4.id] + "px" : "number" == typeof e4.width ? e4.width + "px" : e4.width;
        }).join(" ") } }];
      }, Yt = function(e3, t3) {
        var n3 = t3.column;
        return [e3, { id: "header-cell-" + n3.id, style: { position: "sticky", gridColumn: "span " + n3.totalVisibleHeaderCount } }];
      }, Qt = function(e3, t3) {
        var n3 = t3.row;
        return n3.isExpanded ? [e3, { style: { gridColumn: "1 / " + (n3.cells.length + 1) } }] : [e3, {}];
      };
      function Zt(e3, t3, n3, o2) {
        if (t3.type === l2.init)
          return r2({ gridLayout: { columnWidths: {} } }, e3);
        if (t3.type === l2.resetResize)
          return r2({}, e3, { gridLayout: { columnWidths: {} } });
        if (t3.type === l2.columnStartResizing) {
          var i2 = t3.columnId, u3 = t3.headerIdWidths, s2 = en(i2);
          if (void 0 !== s2) {
            var a2 = o2.visibleColumns.reduce(function(e4, t4) {
              var n4;
              return r2({}, e4, ((n4 = {})[t4.id] = en(t4.id), n4));
            }, {}), c3 = o2.visibleColumns.reduce(function(e4, t4) {
              var n4;
              return r2({}, e4, ((n4 = {})[t4.id] = t4.minWidth, n4));
            }, {}), d3 = o2.visibleColumns.reduce(function(e4, t4) {
              var n4;
              return r2({}, e4, ((n4 = {})[t4.id] = t4.maxWidth, n4));
            }, {}), f3 = u3.map(function(e4) {
              var t4 = e4[0];
              return [t4, en(t4)];
            });
            return r2({}, e3, { gridLayout: r2({}, e3.gridLayout, { startWidths: a2, minWidths: c3, maxWidths: d3, headerIdGridWidths: f3, columnWidth: s2 }) });
          }
          return e3;
        }
        if (t3.type === l2.columnResizing) {
          var p3 = t3.clientX, g3 = e3.columnResizing.startX, v3 = e3.gridLayout, m3 = v3.columnWidth, h3 = v3.minWidths, y3 = v3.maxWidths, w3 = v3.headerIdGridWidths, R3 = (p3 - g3) / m3, b3 = {};
          return (void 0 === w3 ? [] : w3).forEach(function(e4) {
            var t4 = e4[0], n4 = e4[1];
            b3[t4] = Math.min(Math.max(h3[t4], n4 + n4 * R3), y3[t4]);
          }), r2({}, e3, { gridLayout: r2({}, e3.gridLayout, { columnWidths: r2({}, e3.gridLayout.columnWidths, {}, b3) }) });
        }
        return t3.type === l2.columnDoneResizing ? r2({}, e3, { gridLayout: r2({}, e3.gridLayout, { startWidths: {}, minWidths: {}, maxWidths: {} }) }) : void 0;
      }
      function en(e3) {
        var t3, n3 = null == (t3 = document.getElementById("header-cell-" + e3)) ? void 0 : t3.offsetWidth;
        if (void 0 !== n3)
          return n3;
      }
      e2._UNSTABLE_usePivotColumns = nt, e2.actions = l2, e2.defaultColumn = c2, e2.defaultGroupByFn = De2, e2.defaultOrderByFn = Qe2, e2.defaultRenderer = s, e2.emptyRenderer = a, e2.ensurePluginOrder = v2, e2.flexRender = b2, e2.functionalUpdate = m2, e2.loopHooks = g2, e2.makePropGetter = f2, e2.makeRenderer = R2, e2.reduceHooks = p2, e2.safeUseLayoutEffect = y2, e2.useAbsoluteLayout = Mt, e2.useAsyncDebounce = function(e3, n3) {
        void 0 === n3 && (n3 = 0);
        var r3 = t2.useRef({}), i2 = h2(e3), u3 = h2(n3);
        return t2.useCallback(function() {
          var e4 = o(regeneratorRuntime.mark(function e5() {
            var t3, n4, l3, s2 = arguments;
            return regeneratorRuntime.wrap(function(e6) {
              for (; ; )
                switch (e6.prev = e6.next) {
                  case 0:
                    for (t3 = s2.length, n4 = new Array(t3), l3 = 0; l3 < t3; l3++)
                      n4[l3] = s2[l3];
                    return r3.current.promise || (r3.current.promise = new Promise(function(e7, t4) {
                      r3.current.resolve = e7, r3.current.reject = t4;
                    })), r3.current.timeout && clearTimeout(r3.current.timeout), r3.current.timeout = setTimeout(o(regeneratorRuntime.mark(function e7() {
                      return regeneratorRuntime.wrap(function(e8) {
                        for (; ; )
                          switch (e8.prev = e8.next) {
                            case 0:
                              return delete r3.current.timeout, e8.prev = 1, e8.t0 = r3.current, e8.next = 5, i2().apply(void 0, n4);
                            case 5:
                              e8.t1 = e8.sent, e8.t0.resolve.call(e8.t0, e8.t1), e8.next = 12;
                              break;
                            case 9:
                              e8.prev = 9, e8.t2 = e8.catch(1), r3.current.reject(e8.t2);
                            case 12:
                              return e8.prev = 12, delete r3.current.promise, e8.finish(12);
                            case 15:
                            case "end":
                              return e8.stop();
                          }
                      }, e7, null, [[1, 9, 12, 15]]);
                    })), u3()), e6.abrupt("return", r3.current.promise);
                  case 5:
                  case "end":
                    return e6.stop();
                }
            }, e5);
          }));
          return function() {
            return e4.apply(this, arguments);
          };
        }(), [i2, u3]);
      }, e2.useBlockLayout = Dt, e2.useColumnOrder = It, e2.useExpanded = se2, e2.useFilters = Pe2, e2.useFlexLayout = Vt, e2.useGetLatest = h2, e2.useGlobalFilter = Ie2, e2.useGridLayout = $t, e2.useGroupBy = ze2, e2.useMountedLayoutEffect = w2, e2.usePagination = Ze2, e2.useResizeColumns = kt, e2.useRowSelect = vt, e2.useRowState = xt, e2.useSortBy = Ue2, e2.useTable = function(e3) {
        for (var n3 = arguments.length, o2 = new Array(n3 > 1 ? n3 - 1 : 0), i2 = 1; i2 < n3; i2++)
          o2[i2 - 1] = arguments[i2];
        e3 = ie2(e3), o2 = [K2].concat(o2);
        var u3 = t2.useRef({}), s2 = h2(u3.current);
        Object.assign(s2(), r2({}, e3, { plugins: o2, hooks: q2() })), o2.filter(Boolean).forEach(function(e4) {
          e4(s2().hooks);
        });
        var a2 = h2(s2().hooks);
        s2().getHooks = a2, delete s2().hooks, Object.assign(s2(), p2(a2().useOptions, ie2(e3)));
        var c3 = s2(), d3 = c3.data, v3 = c3.columns, m3 = c3.initialState, y3 = c3.defaultColumn, w3 = c3.getSubRows, b3 = c3.getRowId, E3 = c3.stateReducer, I3 = c3.useControlledState, F3 = h2(E3), G3 = t2.useCallback(function(e4, t3) {
          if (!t3.type)
            throw console.info({ action: t3 }), new Error("Unknown Action 👆");
          return [].concat(a2().stateReducers, Array.isArray(F3()) ? F3() : [F3()]).reduce(function(n4, o3) {
            return o3(n4, t3, e4, s2()) || n4;
          }, e4);
        }, [a2, F3, s2]), A3 = t2.useReducer(G3, void 0, function() {
          return G3(m3, { type: l2.init });
        }), k3 = A3[0], H3 = A3[1], W3 = p2([].concat(a2().useControlledState, [I3]), k3, { instance: s2() });
        Object.assign(s2(), { state: W3, dispatch: H3 });
        var z3 = t2.useMemo(function() {
          return S2(p2(a2().columns, v3, { instance: s2() }));
        }, [a2, s2, v3].concat(p2(a2().columnsDeps, [], { instance: s2() })));
        s2().columns = z3;
        var T3 = t2.useMemo(function() {
          return p2(a2().allColumns, C2(z3), { instance: s2() }).map(x2);
        }, [z3, a2, s2].concat(p2(a2().allColumnsDeps, [], { instance: s2() })));
        s2().allColumns = T3;
        var O3 = t2.useMemo(function() {
          for (var e4 = [], t3 = [], n4 = {}, o3 = [].concat(T3); o3.length; ) {
            var r3 = o3.shift();
            le2({ data: d3, rows: e4, flatRows: t3, rowsById: n4, column: r3, getRowId: b3, getSubRows: w3, accessValueHooks: a2().accessValue, getInstance: s2 });
          }
          return [e4, t3, n4];
        }, [T3, d3, b3, w3, a2, s2]), M3 = O3[0], j3 = O3[1], L3 = O3[2];
        Object.assign(s2(), { rows: M3, initialRows: [].concat(M3), flatRows: j3, rowsById: L3 }), g2(a2().useInstanceAfterData, s2());
        var N3 = t2.useMemo(function() {
          return p2(a2().visibleColumns, T3, { instance: s2() }).map(function(e4) {
            return P2(e4, y3);
          });
        }, [a2, T3, s2, y3].concat(p2(a2().visibleColumnsDeps, [], { instance: s2() })));
        T3 = t2.useMemo(function() {
          var e4 = [].concat(N3);
          return T3.forEach(function(t3) {
            e4.find(function(e5) {
              return e5.id === t3.id;
            }) || e4.push(t3);
          }), e4;
        }, [T3, N3]), s2().allColumns = T3;
        var D3 = t2.useMemo(function() {
          return p2(a2().headerGroups, B2(N3, y3), s2());
        }, [a2, N3, y3, s2].concat(p2(a2().headerGroupsDeps, [], { instance: s2() })));
        s2().headerGroups = D3;
        var V3 = t2.useMemo(function() {
          return D3.length ? D3[0].headers : [];
        }, [D3]);
        s2().headers = V3, s2().flatHeaders = D3.reduce(function(e4, t3) {
          return [].concat(e4, t3.headers);
        }, []), g2(a2().useInstanceBeforeDimensions, s2());
        var _3 = N3.filter(function(e4) {
          return e4.isVisible;
        }).map(function(e4) {
          return e4.id;
        }).sort().join("_");
        N3 = t2.useMemo(function() {
          return N3.filter(function(e4) {
            return e4.isVisible;
          });
        }, [N3, _3]), s2().visibleColumns = N3;
        var X3 = ue2(V3), U3 = X3[0], $3 = X3[1], J3 = X3[2];
        return s2().totalColumnsMinWidth = U3, s2().totalColumnsWidth = $3, s2().totalColumnsMaxWidth = J3, g2(a2().useInstance, s2()), [].concat(s2().flatHeaders, s2().allColumns).forEach(function(e4) {
          e4.render = R2(s2(), e4), e4.getHeaderProps = f2(a2().getHeaderProps, { instance: s2(), column: e4 }), e4.getFooterProps = f2(a2().getFooterProps, { instance: s2(), column: e4 });
        }), s2().headerGroups = t2.useMemo(function() {
          return D3.filter(function(e4, t3) {
            return e4.headers = e4.headers.filter(function(e5) {
              return e5.headers ? function e6(t4) {
                return t4.filter(function(t5) {
                  return t5.headers ? e6(t5.headers) : t5.isVisible;
                }).length;
              }(e5.headers) : e5.isVisible;
            }), !!e4.headers.length && (e4.getHeaderGroupProps = f2(a2().getHeaderGroupProps, { instance: s2(), headerGroup: e4, index: t3 }), e4.getFooterGroupProps = f2(a2().getFooterGroupProps, { instance: s2(), headerGroup: e4, index: t3 }), true);
          });
        }, [D3, s2, a2]), s2().footerGroups = [].concat(s2().headerGroups).reverse(), s2().prepareRow = t2.useCallback(function(e4) {
          e4.getRowProps = f2(a2().getRowProps, { instance: s2(), row: e4 }), e4.allCells = T3.map(function(t3) {
            var n4 = e4.values[t3.id], o3 = { column: t3, row: e4, value: n4 };
            return o3.getCellProps = f2(a2().getCellProps, { instance: s2(), cell: o3 }), o3.render = R2(s2(), t3, { row: e4, cell: o3, value: n4 }), o3;
          }), e4.cells = N3.map(function(t3) {
            return e4.allCells.find(function(e5) {
              return e5.column.id === t3.id;
            });
          }), g2(a2().prepareRow, e4, { instance: s2() });
        }, [a2, s2, T3, N3]), s2().getTableProps = f2(a2().getTableProps, { instance: s2() }), s2().getTableBodyProps = f2(a2().getTableBodyProps, { instance: s2() }), g2(a2().useFinalInstance, s2()), s2();
      }, Object.defineProperty(e2, "__esModule", { value: true });
    });
  })(reactTable_production_min, reactTable_production_min.exports);
  var reactTable_production_minExports = reactTable_production_min.exports;
  {
    reactTable.exports = reactTable_production_minExports;
  }
  var reactTableExports = reactTable.exports;
  const customTheme = extendTheme({
    colors: {
      primary: {
        100: "#E5FCF1",
        200: "#27EF96",
        300: "#10DE82",
        400: "#0EBE6F",
        500: "#0CA25F",
        600: "#0A864F",
        700: "#086F42",
        800: "#075C37",
        900: "#064C2E"
      }
    },
    fonts: {
      heading: "Arial, sans-serif",
      body: "Arial, sans-serif"
    }
  });
  var MS = "-ms-";
  var MOZ = "-moz-";
  var WEBKIT = "-webkit-";
  var COMMENT = "comm";
  var RULESET = "rule";
  var DECLARATION = "decl";
  var IMPORT = "@import";
  var KEYFRAMES = "@keyframes";
  var LAYER = "@layer";
  var abs = Math.abs;
  var from = String.fromCharCode;
  var assign = Object.assign;
  function hash(value, length2) {
    return charat(value, 0) ^ 45 ? (((length2 << 2 ^ charat(value, 0)) << 2 ^ charat(value, 1)) << 2 ^ charat(value, 2)) << 2 ^ charat(value, 3) : 0;
  }
  function trim(value) {
    return value.trim();
  }
  function match(value, pattern) {
    return (value = pattern.exec(value)) ? value[0] : value;
  }
  function replace(value, pattern, replacement) {
    return value.replace(pattern, replacement);
  }
  function indexof(value, search, position2) {
    return value.indexOf(search, position2);
  }
  function charat(value, index) {
    return value.charCodeAt(index) | 0;
  }
  function substr(value, begin, end) {
    return value.slice(begin, end);
  }
  function strlen(value) {
    return value.length;
  }
  function sizeof(value) {
    return value.length;
  }
  function append(value, array) {
    return array.push(value), value;
  }
  function combine(array, callback) {
    return array.map(callback).join("");
  }
  function filter(array, pattern) {
    return array.filter(function(value) {
      return !match(value, pattern);
    });
  }
  var line = 1;
  var column = 1;
  var length = 0;
  var position = 0;
  var character = 0;
  var characters = "";
  function node(value, root, parent, type, props, children, length2, siblings) {
    return { value, root, parent, type, props, children, line, column, length: length2, return: "", siblings };
  }
  function copy(root, props) {
    return assign(node("", null, null, "", null, null, 0, root.siblings), root, { length: -root.length }, props);
  }
  function lift(root) {
    while (root.root)
      root = copy(root.root, { children: [root] });
    append(root, root.siblings);
  }
  function char() {
    return character;
  }
  function prev() {
    character = position > 0 ? charat(characters, --position) : 0;
    if (column--, character === 10)
      column = 1, line--;
    return character;
  }
  function next() {
    character = position < length ? charat(characters, position++) : 0;
    if (column++, character === 10)
      column = 1, line++;
    return character;
  }
  function peek() {
    return charat(characters, position);
  }
  function caret() {
    return position;
  }
  function slice(begin, end) {
    return substr(characters, begin, end);
  }
  function token(type) {
    switch (type) {
      case 0:
      case 9:
      case 10:
      case 13:
      case 32:
        return 5;
      case 33:
      case 43:
      case 44:
      case 47:
      case 62:
      case 64:
      case 126:
      case 59:
      case 123:
      case 125:
        return 4;
      case 58:
        return 3;
      case 34:
      case 39:
      case 40:
      case 91:
        return 2;
      case 41:
      case 93:
        return 1;
    }
    return 0;
  }
  function alloc(value) {
    return line = column = 1, length = strlen(characters = value), position = 0, [];
  }
  function dealloc(value) {
    return characters = "", value;
  }
  function delimit(type) {
    return trim(slice(position - 1, delimiter(type === 91 ? type + 2 : type === 40 ? type + 1 : type)));
  }
  function whitespace(type) {
    while (character = peek())
      if (character < 33)
        next();
      else
        break;
    return token(type) > 2 || token(character) > 3 ? "" : " ";
  }
  function escaping(index, count) {
    while (--count && next())
      if (character < 48 || character > 102 || character > 57 && character < 65 || character > 70 && character < 97)
        break;
    return slice(index, caret() + (count < 6 && peek() == 32 && next() == 32));
  }
  function delimiter(type) {
    while (next())
      switch (character) {
        case type:
          return position;
        case 34:
        case 39:
          if (type !== 34 && type !== 39)
            delimiter(character);
          break;
        case 40:
          if (type === 41)
            delimiter(type);
          break;
        case 92:
          next();
          break;
      }
    return position;
  }
  function commenter(type, index) {
    while (next())
      if (type + character === 47 + 10)
        break;
      else if (type + character === 42 + 42 && peek() === 47)
        break;
    return "/*" + slice(index, position - 1) + "*" + from(type === 47 ? type : next());
  }
  function identifier(index) {
    while (!token(peek()))
      next();
    return slice(index, position);
  }
  function compile(value) {
    return dealloc(parse("", null, null, null, [""], value = alloc(value), 0, [0], value));
  }
  function parse(value, root, parent, rule, rules, rulesets, pseudo, points, declarations) {
    var index = 0;
    var offset = 0;
    var length2 = pseudo;
    var atrule = 0;
    var property = 0;
    var previous = 0;
    var variable = 1;
    var scanning = 1;
    var ampersand = 1;
    var character2 = 0;
    var type = "";
    var props = rules;
    var children = rulesets;
    var reference = rule;
    var characters2 = type;
    while (scanning)
      switch (previous = character2, character2 = next()) {
        case 40:
          if (previous != 108 && charat(characters2, length2 - 1) == 58) {
            if (indexof(characters2 += replace(delimit(character2), "&", "&\f"), "&\f", abs(index ? points[index - 1] : 0)) != -1)
              ampersand = -1;
            break;
          }
        case 34:
        case 39:
        case 91:
          characters2 += delimit(character2);
          break;
        case 9:
        case 10:
        case 13:
        case 32:
          characters2 += whitespace(previous);
          break;
        case 92:
          characters2 += escaping(caret() - 1, 7);
          continue;
        case 47:
          switch (peek()) {
            case 42:
            case 47:
              append(comment(commenter(next(), caret()), root, parent, declarations), declarations);
              break;
            default:
              characters2 += "/";
          }
          break;
        case 123 * variable:
          points[index++] = strlen(characters2) * ampersand;
        case 125 * variable:
        case 59:
        case 0:
          switch (character2) {
            case 0:
            case 125:
              scanning = 0;
            case 59 + offset:
              if (ampersand == -1)
                characters2 = replace(characters2, /\f/g, "");
              if (property > 0 && strlen(characters2) - length2)
                append(property > 32 ? declaration(characters2 + ";", rule, parent, length2 - 1, declarations) : declaration(replace(characters2, " ", "") + ";", rule, parent, length2 - 2, declarations), declarations);
              break;
            case 59:
              characters2 += ";";
            default:
              append(reference = ruleset(characters2, root, parent, index, offset, rules, points, type, props = [], children = [], length2, rulesets), rulesets);
              if (character2 === 123)
                if (offset === 0)
                  parse(characters2, root, reference, reference, props, rulesets, length2, points, children);
                else
                  switch (atrule === 99 && charat(characters2, 3) === 110 ? 100 : atrule) {
                    case 100:
                    case 108:
                    case 109:
                    case 115:
                      parse(value, reference, reference, rule && append(ruleset(value, reference, reference, 0, 0, rules, points, type, rules, props = [], length2, children), children), rules, children, length2, points, rule ? props : children);
                      break;
                    default:
                      parse(characters2, reference, reference, reference, [""], children, 0, points, children);
                  }
          }
          index = offset = property = 0, variable = ampersand = 1, type = characters2 = "", length2 = pseudo;
          break;
        case 58:
          length2 = 1 + strlen(characters2), property = previous;
        default:
          if (variable < 1) {
            if (character2 == 123)
              --variable;
            else if (character2 == 125 && variable++ == 0 && prev() == 125)
              continue;
          }
          switch (characters2 += from(character2), character2 * variable) {
            case 38:
              ampersand = offset > 0 ? 1 : (characters2 += "\f", -1);
              break;
            case 44:
              points[index++] = (strlen(characters2) - 1) * ampersand, ampersand = 1;
              break;
            case 64:
              if (peek() === 45)
                characters2 += delimit(next());
              atrule = peek(), offset = length2 = strlen(type = characters2 += identifier(caret())), character2++;
              break;
            case 45:
              if (previous === 45 && strlen(characters2) == 2)
                variable = 0;
          }
      }
    return rulesets;
  }
  function ruleset(value, root, parent, index, offset, rules, points, type, props, children, length2, siblings) {
    var post = offset - 1;
    var rule = offset === 0 ? rules : [""];
    var size2 = sizeof(rule);
    for (var i = 0, j2 = 0, k2 = 0; i < index; ++i)
      for (var x2 = 0, y2 = substr(value, post + 1, post = abs(j2 = points[i])), z2 = value; x2 < size2; ++x2)
        if (z2 = trim(j2 > 0 ? rule[x2] + " " + y2 : replace(y2, /&\f/g, rule[x2])))
          props[k2++] = z2;
    return node(value, root, parent, offset === 0 ? RULESET : type, props, children, length2, siblings);
  }
  function comment(value, root, parent, siblings) {
    return node(value, root, parent, COMMENT, from(char()), substr(value, 2, -2), 0, siblings);
  }
  function declaration(value, root, parent, length2, siblings) {
    return node(value, root, parent, DECLARATION, substr(value, 0, length2), substr(value, length2 + 1, -1), length2, siblings);
  }
  function prefix(value, length2, children) {
    switch (hash(value, length2)) {
      case 5103:
        return WEBKIT + "print-" + value + value;
      case 5737:
      case 4201:
      case 3177:
      case 3433:
      case 1641:
      case 4457:
      case 2921:
      case 5572:
      case 6356:
      case 5844:
      case 3191:
      case 6645:
      case 3005:
      case 6391:
      case 5879:
      case 5623:
      case 6135:
      case 4599:
      case 4855:
      case 4215:
      case 6389:
      case 5109:
      case 5365:
      case 5621:
      case 3829:
        return WEBKIT + value + value;
      case 4789:
        return MOZ + value + value;
      case 5349:
      case 4246:
      case 4810:
      case 6968:
      case 2756:
        return WEBKIT + value + MOZ + value + MS + value + value;
      case 5936:
        switch (charat(value, length2 + 11)) {
          case 114:
            return WEBKIT + value + MS + replace(value, /[svh]\w+-[tblr]{2}/, "tb") + value;
          case 108:
            return WEBKIT + value + MS + replace(value, /[svh]\w+-[tblr]{2}/, "tb-rl") + value;
          case 45:
            return WEBKIT + value + MS + replace(value, /[svh]\w+-[tblr]{2}/, "lr") + value;
        }
      case 6828:
      case 4268:
      case 2903:
        return WEBKIT + value + MS + value + value;
      case 6165:
        return WEBKIT + value + MS + "flex-" + value + value;
      case 5187:
        return WEBKIT + value + replace(value, /(\w+).+(:[^]+)/, WEBKIT + "box-$1$2" + MS + "flex-$1$2") + value;
      case 5443:
        return WEBKIT + value + MS + "flex-item-" + replace(value, /flex-|-self/g, "") + (!match(value, /flex-|baseline/) ? MS + "grid-row-" + replace(value, /flex-|-self/g, "") : "") + value;
      case 4675:
        return WEBKIT + value + MS + "flex-line-pack" + replace(value, /align-content|flex-|-self/g, "") + value;
      case 5548:
        return WEBKIT + value + MS + replace(value, "shrink", "negative") + value;
      case 5292:
        return WEBKIT + value + MS + replace(value, "basis", "preferred-size") + value;
      case 6060:
        return WEBKIT + "box-" + replace(value, "-grow", "") + WEBKIT + value + MS + replace(value, "grow", "positive") + value;
      case 4554:
        return WEBKIT + replace(value, /([^-])(transform)/g, "$1" + WEBKIT + "$2") + value;
      case 6187:
        return replace(replace(replace(value, /(zoom-|grab)/, WEBKIT + "$1"), /(image-set)/, WEBKIT + "$1"), value, "") + value;
      case 5495:
      case 3959:
        return replace(value, /(image-set\([^]*)/, WEBKIT + "$1$`$1");
      case 4968:
        return replace(replace(value, /(.+:)(flex-)?(.*)/, WEBKIT + "box-pack:$3" + MS + "flex-pack:$3"), /s.+-b[^;]+/, "justify") + WEBKIT + value + value;
      case 4200:
        if (!match(value, /flex-|baseline/))
          return MS + "grid-column-align" + substr(value, length2) + value;
        break;
      case 2592:
      case 3360:
        return MS + replace(value, "template-", "") + value;
      case 4384:
      case 3616:
        if (children && children.some(function(element, index) {
          return length2 = index, match(element.props, /grid-\w+-end/);
        })) {
          return ~indexof(value + (children = children[length2].value), "span", 0) ? value : MS + replace(value, "-start", "") + value + MS + "grid-row-span:" + (~indexof(children, "span", 0) ? match(children, /\d+/) : +match(children, /\d+/) - +match(value, /\d+/)) + ";";
        }
        return MS + replace(value, "-start", "") + value;
      case 4896:
      case 4128:
        return children && children.some(function(element) {
          return match(element.props, /grid-\w+-start/);
        }) ? value : MS + replace(replace(value, "-end", "-span"), "span ", "") + value;
      case 4095:
      case 3583:
      case 4068:
      case 2532:
        return replace(value, /(.+)-inline(.+)/, WEBKIT + "$1$2") + value;
      case 8116:
      case 7059:
      case 5753:
      case 5535:
      case 5445:
      case 5701:
      case 4933:
      case 4677:
      case 5533:
      case 5789:
      case 5021:
      case 4765:
        if (strlen(value) - 1 - length2 > 6)
          switch (charat(value, length2 + 1)) {
            case 109:
              if (charat(value, length2 + 4) !== 45)
                break;
            case 102:
              return replace(value, /(.+:)(.+)-([^]+)/, "$1" + WEBKIT + "$2-$3$1" + MOZ + (charat(value, length2 + 3) == 108 ? "$3" : "$2-$3")) + value;
            case 115:
              return ~indexof(value, "stretch", 0) ? prefix(replace(value, "stretch", "fill-available"), length2, children) + value : value;
          }
        break;
      case 5152:
      case 5920:
        return replace(value, /(.+?):(\d+)(\s*\/\s*(span)?\s*(\d+))?(.*)/, function(_2, a, b2, c2, d2, e2, f2) {
          return MS + a + ":" + b2 + f2 + (c2 ? MS + a + "-span:" + (d2 ? e2 : +e2 - +b2) + f2 : "") + value;
        });
      case 4949:
        if (charat(value, length2 + 6) === 121)
          return replace(value, ":", ":" + WEBKIT) + value;
        break;
      case 6444:
        switch (charat(value, charat(value, 14) === 45 ? 18 : 11)) {
          case 120:
            return replace(value, /(.+:)([^;\s!]+)(;|(\s+)?!.+)?/, "$1" + WEBKIT + (charat(value, 14) === 45 ? "inline-" : "") + "box$3$1" + WEBKIT + "$2$3$1" + MS + "$2box$3") + value;
          case 100:
            return replace(value, ":", ":" + MS) + value;
        }
        break;
      case 5719:
      case 2647:
      case 2135:
      case 3927:
      case 2391:
        return replace(value, "scroll-", "scroll-snap-") + value;
    }
    return value;
  }
  function serialize(children, callback) {
    var output = "";
    for (var i = 0; i < children.length; i++)
      output += callback(children[i], i, children, callback) || "";
    return output;
  }
  function stringify(element, index, children, callback) {
    switch (element.type) {
      case LAYER:
        if (element.children.length)
          break;
      case IMPORT:
      case DECLARATION:
        return element.return = element.return || element.value;
      case COMMENT:
        return "";
      case KEYFRAMES:
        return element.return = element.value + "{" + serialize(element.children, callback) + "}";
      case RULESET:
        if (!strlen(element.value = element.props.join(",")))
          return "";
    }
    return strlen(children = serialize(element.children, callback)) ? element.return = element.value + "{" + children + "}" : "";
  }
  function middleware(collection) {
    var length2 = sizeof(collection);
    return function(element, index, children, callback) {
      var output = "";
      for (var i = 0; i < length2; i++)
        output += collection[i](element, index, children, callback) || "";
      return output;
    };
  }
  function rulesheet(callback) {
    return function(element) {
      if (!element.root) {
        if (element = element.return)
          callback(element);
      }
    };
  }
  function prefixer(element, index, children, callback) {
    if (element.length > -1) {
      if (!element.return)
        switch (element.type) {
          case DECLARATION:
            element.return = prefix(element.value, element.length, children);
            return;
          case KEYFRAMES:
            return serialize([copy(element, { value: replace(element.value, "@", "@" + WEBKIT) })], callback);
          case RULESET:
            if (element.length)
              return combine(children = element.props, function(value) {
                switch (match(value, callback = /(::plac\w+|:read-\w+)/)) {
                  case ":read-only":
                  case ":read-write":
                    lift(copy(element, { props: [replace(value, /:(read-\w+)/, ":" + MOZ + "$1")] }));
                    lift(copy(element, { props: [value] }));
                    assign(element, { props: filter(children, callback) });
                    break;
                  case "::placeholder":
                    lift(copy(element, { props: [replace(value, /:(plac\w+)/, ":" + WEBKIT + "input-$1")] }));
                    lift(copy(element, { props: [replace(value, /:(plac\w+)/, ":" + MOZ + "$1")] }));
                    lift(copy(element, { props: [replace(value, /:(plac\w+)/, MS + "input-$1")] }));
                    lift(copy(element, { props: [value] }));
                    assign(element, { props: filter(children, callback) });
                    break;
                }
                return "";
              });
        }
    }
  }
  var define_process_env_default = {};
  var f = "undefined" != typeof process && void 0 !== define_process_env_default && (define_process_env_default.REACT_APP_SC_ATTR || define_process_env_default.SC_ATTR) || "data-styled", m = "active", y = "data-styled-version", v = "6.1.11", g = "/*!sc*/\n", S = "undefined" != typeof window && "HTMLElement" in window, w = Boolean("boolean" == typeof SC_DISABLE_SPEEDY ? SC_DISABLE_SPEEDY : "undefined" != typeof process && void 0 !== define_process_env_default && void 0 !== define_process_env_default.REACT_APP_SC_DISABLE_SPEEDY && "" !== define_process_env_default.REACT_APP_SC_DISABLE_SPEEDY ? "false" !== define_process_env_default.REACT_APP_SC_DISABLE_SPEEDY && define_process_env_default.REACT_APP_SC_DISABLE_SPEEDY : "undefined" != typeof process && void 0 !== define_process_env_default && void 0 !== define_process_env_default.SC_DISABLE_SPEEDY && "" !== define_process_env_default.SC_DISABLE_SPEEDY ? "false" !== define_process_env_default.SC_DISABLE_SPEEDY && define_process_env_default.SC_DISABLE_SPEEDY : false), _ = Object.freeze([]), C = Object.freeze({});
  function I(e2, t2, n2) {
    return void 0 === n2 && (n2 = C), e2.theme !== n2.theme && e2.theme || t2 || n2.theme;
  }
  var A = /* @__PURE__ */ new Set(["a", "abbr", "address", "area", "article", "aside", "audio", "b", "base", "bdi", "bdo", "big", "blockquote", "body", "br", "button", "canvas", "caption", "cite", "code", "col", "colgroup", "data", "datalist", "dd", "del", "details", "dfn", "dialog", "div", "dl", "dt", "em", "embed", "fieldset", "figcaption", "figure", "footer", "form", "h1", "h2", "h3", "h4", "h5", "h6", "header", "hgroup", "hr", "html", "i", "iframe", "img", "input", "ins", "kbd", "keygen", "label", "legend", "li", "link", "main", "map", "mark", "menu", "menuitem", "meta", "meter", "nav", "noscript", "object", "ol", "optgroup", "option", "output", "p", "param", "picture", "pre", "progress", "q", "rp", "rt", "ruby", "s", "samp", "script", "section", "select", "small", "source", "span", "strong", "style", "sub", "summary", "sup", "table", "tbody", "td", "textarea", "tfoot", "th", "thead", "time", "tr", "track", "u", "ul", "use", "var", "video", "wbr", "circle", "clipPath", "defs", "ellipse", "foreignObject", "g", "image", "line", "linearGradient", "marker", "mask", "path", "pattern", "polygon", "polyline", "radialGradient", "rect", "stop", "svg", "text", "tspan"]), O = /[!"#$%&'()*+,./:;<=>?@[\\\]^`{|}~-]+/g, D = /(^-|-$)/g;
  function R(e2) {
    return e2.replace(O, "-").replace(D, "");
  }
  var T = /(a)(d)/gi, k = 52, j = function(e2) {
    return String.fromCharCode(e2 + (e2 > 25 ? 39 : 97));
  };
  function x(e2) {
    var t2, n2 = "";
    for (t2 = Math.abs(e2); t2 > k; t2 = t2 / k | 0)
      n2 = j(t2 % k) + n2;
    return (j(t2 % k) + n2).replace(T, "$1-$2");
  }
  var V, F = 5381, M = function(e2, t2) {
    for (var n2 = t2.length; n2; )
      e2 = 33 * e2 ^ t2.charCodeAt(--n2);
    return e2;
  }, $ = function(e2) {
    return M(F, e2);
  };
  function z(e2) {
    return x($(e2) >>> 0);
  }
  function B(e2) {
    return e2.displayName || e2.name || "Component";
  }
  function L(e2) {
    return "string" == typeof e2 && true;
  }
  var G = "function" == typeof Symbol && Symbol.for, Y = G ? Symbol.for("react.memo") : 60115, W = G ? Symbol.for("react.forward_ref") : 60112, q = { childContextTypes: true, contextType: true, contextTypes: true, defaultProps: true, displayName: true, getDefaultProps: true, getDerivedStateFromError: true, getDerivedStateFromProps: true, mixins: true, propTypes: true, type: true }, H = { name: true, length: true, prototype: true, caller: true, callee: true, arguments: true, arity: true }, U = { $$typeof: true, compare: true, defaultProps: true, displayName: true, propTypes: true, type: true }, J = ((V = {})[W] = { $$typeof: true, render: true, defaultProps: true, displayName: true, propTypes: true }, V[Y] = U, V);
  function X(e2) {
    return ("type" in (t2 = e2) && t2.type.$$typeof) === Y ? U : "$$typeof" in e2 ? J[e2.$$typeof] : q;
    var t2;
  }
  var Z = Object.defineProperty, K = Object.getOwnPropertyNames, Q = Object.getOwnPropertySymbols, ee = Object.getOwnPropertyDescriptor, te = Object.getPrototypeOf, ne = Object.prototype;
  function oe(e2, t2, n2) {
    if ("string" != typeof t2) {
      if (ne) {
        var o2 = te(t2);
        o2 && o2 !== ne && oe(e2, o2, n2);
      }
      var r2 = K(t2);
      Q && (r2 = r2.concat(Q(t2)));
      for (var s2 = X(e2), i2 = X(t2), a2 = 0; a2 < r2.length; ++a2) {
        var c2 = r2[a2];
        if (!(c2 in H || n2 && n2[c2] || i2 && c2 in i2 || s2 && c2 in s2)) {
          var l2 = ee(t2, c2);
          try {
            Z(e2, c2, l2);
          } catch (e3) {
          }
        }
      }
    }
    return e2;
  }
  function re(e2) {
    return "function" == typeof e2;
  }
  function se(e2) {
    return "object" == typeof e2 && "styledComponentId" in e2;
  }
  function ie(e2, t2) {
    return e2 && t2 ? "".concat(e2, " ").concat(t2) : e2 || t2 || "";
  }
  function ae(e2, t2) {
    if (0 === e2.length)
      return "";
    for (var n2 = e2[0], o2 = 1; o2 < e2.length; o2++)
      n2 += e2[o2];
    return n2;
  }
  function ce(e2) {
    return null !== e2 && "object" == typeof e2 && e2.constructor.name === Object.name && !("props" in e2 && e2.$$typeof);
  }
  function le(e2, t2, n2) {
    if (void 0 === n2 && (n2 = false), !n2 && !ce(e2) && !Array.isArray(e2))
      return t2;
    if (Array.isArray(t2))
      for (var o2 = 0; o2 < t2.length; o2++)
        e2[o2] = le(e2[o2], t2[o2]);
    else if (ce(t2))
      for (var o2 in t2)
        e2[o2] = le(e2[o2], t2[o2]);
    return e2;
  }
  function ue(e2, t2) {
    Object.defineProperty(e2, "toString", { value: t2 });
  }
  function he(t2) {
    for (var n2 = [], o2 = 1; o2 < arguments.length; o2++)
      n2[o2 - 1] = arguments[o2];
    return new Error("An error occurred. See https://github.com/styled-components/styled-components/blob/main/packages/styled-components/src/utils/errors.md#".concat(t2, " for more information.").concat(n2.length > 0 ? " Args: ".concat(n2.join(", ")) : ""));
  }
  var fe = function() {
    function e2(e3) {
      this.groupSizes = new Uint32Array(512), this.length = 512, this.tag = e3;
    }
    return e2.prototype.indexOfGroup = function(e3) {
      for (var t2 = 0, n2 = 0; n2 < e3; n2++)
        t2 += this.groupSizes[n2];
      return t2;
    }, e2.prototype.insertRules = function(e3, t2) {
      if (e3 >= this.groupSizes.length) {
        for (var n2 = this.groupSizes, o2 = n2.length, r2 = o2; e3 >= r2; )
          if ((r2 <<= 1) < 0)
            throw he(16, "".concat(e3));
        this.groupSizes = new Uint32Array(r2), this.groupSizes.set(n2), this.length = r2;
        for (var s2 = o2; s2 < r2; s2++)
          this.groupSizes[s2] = 0;
      }
      for (var i2 = this.indexOfGroup(e3 + 1), a2 = (s2 = 0, t2.length); s2 < a2; s2++)
        this.tag.insertRule(i2, t2[s2]) && (this.groupSizes[e3]++, i2++);
    }, e2.prototype.clearGroup = function(e3) {
      if (e3 < this.length) {
        var t2 = this.groupSizes[e3], n2 = this.indexOfGroup(e3), o2 = n2 + t2;
        this.groupSizes[e3] = 0;
        for (var r2 = n2; r2 < o2; r2++)
          this.tag.deleteRule(n2);
      }
    }, e2.prototype.getGroup = function(e3) {
      var t2 = "";
      if (e3 >= this.length || 0 === this.groupSizes[e3])
        return t2;
      for (var n2 = this.groupSizes[e3], o2 = this.indexOfGroup(e3), r2 = o2 + n2, s2 = o2; s2 < r2; s2++)
        t2 += "".concat(this.tag.getRule(s2)).concat(g);
      return t2;
    }, e2;
  }(), ye = /* @__PURE__ */ new Map(), ve = /* @__PURE__ */ new Map(), ge = 1, Se = function(e2) {
    if (ye.has(e2))
      return ye.get(e2);
    for (; ve.has(ge); )
      ge++;
    var t2 = ge++;
    return ye.set(e2, t2), ve.set(t2, e2), t2;
  }, we = function(e2, t2) {
    ge = t2 + 1, ye.set(e2, t2), ve.set(t2, e2);
  }, be = "style[".concat(f, "][").concat(y, '="').concat(v, '"]'), Ee = new RegExp("^".concat(f, '\\.g(\\d+)\\[id="([\\w\\d-]+)"\\].*?"([^"]*)')), Ne = function(e2, t2, n2) {
    for (var o2, r2 = n2.split(","), s2 = 0, i2 = r2.length; s2 < i2; s2++)
      (o2 = r2[s2]) && e2.registerName(t2, o2);
  }, Pe = function(e2, t2) {
    for (var n2, o2 = (null !== (n2 = t2.textContent) && void 0 !== n2 ? n2 : "").split(g), r2 = [], s2 = 0, i2 = o2.length; s2 < i2; s2++) {
      var a2 = o2[s2].trim();
      if (a2) {
        var c2 = a2.match(Ee);
        if (c2) {
          var l2 = 0 | parseInt(c2[1], 10), u2 = c2[2];
          0 !== l2 && (we(u2, l2), Ne(e2, u2, c2[3]), e2.getTag().insertRules(l2, r2)), r2.length = 0;
        } else
          r2.push(a2);
      }
    }
  };
  function _e() {
    return "undefined" != typeof __webpack_nonce__ ? __webpack_nonce__ : null;
  }
  var Ce = function(e2) {
    var t2 = document.head, n2 = e2 || t2, o2 = document.createElement("style"), r2 = function(e3) {
      var t3 = Array.from(e3.querySelectorAll("style[".concat(f, "]")));
      return t3[t3.length - 1];
    }(n2), s2 = void 0 !== r2 ? r2.nextSibling : null;
    o2.setAttribute(f, m), o2.setAttribute(y, v);
    var i2 = _e();
    return i2 && o2.setAttribute("nonce", i2), n2.insertBefore(o2, s2), o2;
  }, Ie = function() {
    function e2(e3) {
      this.element = Ce(e3), this.element.appendChild(document.createTextNode("")), this.sheet = function(e4) {
        if (e4.sheet)
          return e4.sheet;
        for (var t2 = document.styleSheets, n2 = 0, o2 = t2.length; n2 < o2; n2++) {
          var r2 = t2[n2];
          if (r2.ownerNode === e4)
            return r2;
        }
        throw he(17);
      }(this.element), this.length = 0;
    }
    return e2.prototype.insertRule = function(e3, t2) {
      try {
        return this.sheet.insertRule(t2, e3), this.length++, true;
      } catch (e4) {
        return false;
      }
    }, e2.prototype.deleteRule = function(e3) {
      this.sheet.deleteRule(e3), this.length--;
    }, e2.prototype.getRule = function(e3) {
      var t2 = this.sheet.cssRules[e3];
      return t2 && t2.cssText ? t2.cssText : "";
    }, e2;
  }(), Ae = function() {
    function e2(e3) {
      this.element = Ce(e3), this.nodes = this.element.childNodes, this.length = 0;
    }
    return e2.prototype.insertRule = function(e3, t2) {
      if (e3 <= this.length && e3 >= 0) {
        var n2 = document.createTextNode(t2);
        return this.element.insertBefore(n2, this.nodes[e3] || null), this.length++, true;
      }
      return false;
    }, e2.prototype.deleteRule = function(e3) {
      this.element.removeChild(this.nodes[e3]), this.length--;
    }, e2.prototype.getRule = function(e3) {
      return e3 < this.length ? this.nodes[e3].textContent : "";
    }, e2;
  }(), Oe = function() {
    function e2(e3) {
      this.rules = [], this.length = 0;
    }
    return e2.prototype.insertRule = function(e3, t2) {
      return e3 <= this.length && (this.rules.splice(e3, 0, t2), this.length++, true);
    }, e2.prototype.deleteRule = function(e3) {
      this.rules.splice(e3, 1), this.length--;
    }, e2.prototype.getRule = function(e3) {
      return e3 < this.length ? this.rules[e3] : "";
    }, e2;
  }(), De = S, Re = { isServer: !S, useCSSOMInjection: !w }, Te = function() {
    function e2(e3, n2, o2) {
      void 0 === e3 && (e3 = C), void 0 === n2 && (n2 = {});
      var r2 = this;
      this.options = __assign(__assign({}, Re), e3), this.gs = n2, this.names = new Map(o2), this.server = !!e3.isServer, !this.server && S && De && (De = false, function(e4) {
        for (var t2 = document.querySelectorAll(be), n3 = 0, o3 = t2.length; n3 < o3; n3++) {
          var r3 = t2[n3];
          r3 && r3.getAttribute(f) !== m && (Pe(e4, r3), r3.parentNode && r3.parentNode.removeChild(r3));
        }
      }(this)), ue(this, function() {
        return function(e4) {
          for (var t2 = e4.getTag(), n3 = t2.length, o3 = "", r3 = function(n4) {
            var r4 = function(e5) {
              return ve.get(e5);
            }(n4);
            if (void 0 === r4)
              return "continue";
            var s3 = e4.names.get(r4), i2 = t2.getGroup(n4);
            if (void 0 === s3 || 0 === i2.length)
              return "continue";
            var a2 = "".concat(f, ".g").concat(n4, '[id="').concat(r4, '"]'), c2 = "";
            void 0 !== s3 && s3.forEach(function(e5) {
              e5.length > 0 && (c2 += "".concat(e5, ","));
            }), o3 += "".concat(i2).concat(a2, '{content:"').concat(c2, '"}').concat(g);
          }, s2 = 0; s2 < n3; s2++)
            r3(s2);
          return o3;
        }(r2);
      });
    }
    return e2.registerId = function(e3) {
      return Se(e3);
    }, e2.prototype.reconstructWithOptions = function(n2, o2) {
      return void 0 === o2 && (o2 = true), new e2(__assign(__assign({}, this.options), n2), this.gs, o2 && this.names || void 0);
    }, e2.prototype.allocateGSInstance = function(e3) {
      return this.gs[e3] = (this.gs[e3] || 0) + 1;
    }, e2.prototype.getTag = function() {
      return this.tag || (this.tag = (e3 = function(e4) {
        var t2 = e4.useCSSOMInjection, n2 = e4.target;
        return e4.isServer ? new Oe(n2) : t2 ? new Ie(n2) : new Ae(n2);
      }(this.options), new fe(e3)));
      var e3;
    }, e2.prototype.hasNameForId = function(e3, t2) {
      return this.names.has(e3) && this.names.get(e3).has(t2);
    }, e2.prototype.registerName = function(e3, t2) {
      if (Se(e3), this.names.has(e3))
        this.names.get(e3).add(t2);
      else {
        var n2 = /* @__PURE__ */ new Set();
        n2.add(t2), this.names.set(e3, n2);
      }
    }, e2.prototype.insertRules = function(e3, t2, n2) {
      this.registerName(e3, t2), this.getTag().insertRules(Se(e3), n2);
    }, e2.prototype.clearNames = function(e3) {
      this.names.has(e3) && this.names.get(e3).clear();
    }, e2.prototype.clearRules = function(e3) {
      this.getTag().clearGroup(Se(e3)), this.clearNames(e3);
    }, e2.prototype.clearTag = function() {
      this.tag = void 0;
    }, e2;
  }(), ke = /&/g, je = /^\s*\/\/.*$/gm;
  function xe(e2, t2) {
    return e2.map(function(e3) {
      return "rule" === e3.type && (e3.value = "".concat(t2, " ").concat(e3.value), e3.value = e3.value.replaceAll(",", ",".concat(t2, " ")), e3.props = e3.props.map(function(e4) {
        return "".concat(t2, " ").concat(e4);
      })), Array.isArray(e3.children) && "@keyframes" !== e3.type && (e3.children = xe(e3.children, t2)), e3;
    });
  }
  function Ve(e2) {
    var t2, n2, o2, r2 = C, s2 = r2.options, i2 = void 0 === s2 ? C : s2, a2 = r2.plugins, c2 = void 0 === a2 ? _ : a2, l2 = function(e3, o3, r3) {
      return r3.startsWith(n2) && r3.endsWith(n2) && r3.replaceAll(n2, "").length > 0 ? ".".concat(t2) : e3;
    }, u2 = c2.slice();
    u2.push(function(e3) {
      e3.type === RULESET && e3.value.includes("&") && (e3.props[0] = e3.props[0].replace(ke, n2).replace(o2, l2));
    }), i2.prefix && u2.push(prefixer), u2.push(stringify);
    var p2 = function(e3, r3, s3, a3) {
      void 0 === r3 && (r3 = ""), void 0 === s3 && (s3 = ""), void 0 === a3 && (a3 = "&"), t2 = a3, n2 = r3, o2 = new RegExp("\\".concat(n2, "\\b"), "g");
      var c3 = e3.replace(je, ""), l3 = compile(s3 || r3 ? "".concat(s3, " ").concat(r3, " { ").concat(c3, " }") : c3);
      i2.namespace && (l3 = xe(l3, i2.namespace));
      var p3 = [];
      return serialize(l3, middleware(u2.concat(rulesheet(function(e4) {
        return p3.push(e4);
      })))), p3;
    };
    return p2.hash = c2.length ? c2.reduce(function(e3, t3) {
      return t3.name || he(15), M(e3, t3.name);
    }, F).toString() : "", p2;
  }
  var Fe = new Te(), Me = Ve(), $e = React.createContext({ shouldForwardProp: void 0, styleSheet: Fe, stylis: Me });
  $e.Consumer;
  React.createContext(void 0);
  function Le() {
    return reactExports.useContext($e);
  }
  var Ye = function() {
    function e2(e3, t2) {
      var n2 = this;
      this.inject = function(e4, t3) {
        void 0 === t3 && (t3 = Me);
        var o2 = n2.name + t3.hash;
        e4.hasNameForId(n2.id, o2) || e4.insertRules(n2.id, o2, t3(n2.rules, o2, "@keyframes"));
      }, this.name = e3, this.id = "sc-keyframes-".concat(e3), this.rules = t2, ue(this, function() {
        throw he(12, String(n2.name));
      });
    }
    return e2.prototype.getName = function(e3) {
      return void 0 === e3 && (e3 = Me), this.name + e3.hash;
    }, e2;
  }(), We = function(e2) {
    return e2 >= "A" && e2 <= "Z";
  };
  function qe(e2) {
    for (var t2 = "", n2 = 0; n2 < e2.length; n2++) {
      var o2 = e2[n2];
      if (1 === n2 && "-" === o2 && "-" === e2[0])
        return e2;
      We(o2) ? t2 += "-" + o2.toLowerCase() : t2 += o2;
    }
    return t2.startsWith("ms-") ? "-" + t2 : t2;
  }
  var He = function(e2) {
    return null == e2 || false === e2 || "" === e2;
  }, Ue = function(t2) {
    var n2, o2, r2 = [];
    for (var s2 in t2) {
      var i2 = t2[s2];
      t2.hasOwnProperty(s2) && !He(i2) && (Array.isArray(i2) && i2.isCss || re(i2) ? r2.push("".concat(qe(s2), ":"), i2, ";") : ce(i2) ? r2.push.apply(r2, __spreadArray(__spreadArray(["".concat(s2, " {")], Ue(i2), false), ["}"], false)) : r2.push("".concat(qe(s2), ": ").concat((n2 = s2, null == (o2 = i2) || "boolean" == typeof o2 || "" === o2 ? "" : "number" != typeof o2 || 0 === o2 || n2 in unitlessKeys || n2.startsWith("--") ? String(o2).trim() : "".concat(o2, "px")), ";")));
    }
    return r2;
  };
  function Je(e2, t2, n2, o2) {
    if (He(e2))
      return [];
    if (se(e2))
      return [".".concat(e2.styledComponentId)];
    if (re(e2)) {
      if (!re(s2 = e2) || s2.prototype && s2.prototype.isReactComponent || !t2)
        return [e2];
      var r2 = e2(t2);
      return Je(r2, t2, n2, o2);
    }
    var s2;
    return e2 instanceof Ye ? n2 ? (e2.inject(n2, o2), [e2.getName(o2)]) : [e2] : ce(e2) ? Ue(e2) : Array.isArray(e2) ? Array.prototype.concat.apply(_, e2.map(function(e3) {
      return Je(e3, t2, n2, o2);
    })) : [e2.toString()];
  }
  function Xe(e2) {
    for (var t2 = 0; t2 < e2.length; t2 += 1) {
      var n2 = e2[t2];
      if (re(n2) && !se(n2))
        return false;
    }
    return true;
  }
  var Ze = $(v), Ke = function() {
    function e2(e3, t2, n2) {
      this.rules = e3, this.staticRulesId = "", this.isStatic = (void 0 === n2 || n2.isStatic) && Xe(e3), this.componentId = t2, this.baseHash = M(Ze, t2), this.baseStyle = n2, Te.registerId(t2);
    }
    return e2.prototype.generateAndInjectStyles = function(e3, t2, n2) {
      var o2 = this.baseStyle ? this.baseStyle.generateAndInjectStyles(e3, t2, n2) : "";
      if (this.isStatic && !n2.hash)
        if (this.staticRulesId && t2.hasNameForId(this.componentId, this.staticRulesId))
          o2 = ie(o2, this.staticRulesId);
        else {
          var r2 = ae(Je(this.rules, e3, t2, n2)), s2 = x(M(this.baseHash, r2) >>> 0);
          if (!t2.hasNameForId(this.componentId, s2)) {
            var i2 = n2(r2, ".".concat(s2), void 0, this.componentId);
            t2.insertRules(this.componentId, s2, i2);
          }
          o2 = ie(o2, s2), this.staticRulesId = s2;
        }
      else {
        for (var a2 = M(this.baseHash, n2.hash), c2 = "", l2 = 0; l2 < this.rules.length; l2++) {
          var u2 = this.rules[l2];
          if ("string" == typeof u2)
            c2 += u2;
          else if (u2) {
            var p2 = ae(Je(u2, e3, t2, n2));
            a2 = M(a2, p2 + l2), c2 += p2;
          }
        }
        if (c2) {
          var d2 = x(a2 >>> 0);
          t2.hasNameForId(this.componentId, d2) || t2.insertRules(this.componentId, d2, n2(c2, ".".concat(d2), void 0, this.componentId)), o2 = ie(o2, d2);
        }
      }
      return o2;
    }, e2;
  }(), Qe = React.createContext(void 0);
  Qe.Consumer;
  var ot = {};
  function st(e2, r2, s2) {
    var i2 = se(e2), a2 = e2, c2 = !L(e2), p2 = r2.attrs, d2 = void 0 === p2 ? _ : p2, h2 = r2.componentId, f2 = void 0 === h2 ? function(e3, t2) {
      var n2 = "string" != typeof e3 ? "sc" : R(e3);
      ot[n2] = (ot[n2] || 0) + 1;
      var o2 = "".concat(n2, "-").concat(z(v + n2 + ot[n2]));
      return t2 ? "".concat(t2, "-").concat(o2) : o2;
    }(r2.displayName, r2.parentComponentId) : h2, m2 = r2.displayName, y2 = void 0 === m2 ? function(e3) {
      return L(e3) ? "styled.".concat(e3) : "Styled(".concat(B(e3), ")");
    }(e2) : m2, g2 = r2.displayName && r2.componentId ? "".concat(R(r2.displayName), "-").concat(r2.componentId) : r2.componentId || f2, S2 = i2 && a2.attrs ? a2.attrs.concat(d2).filter(Boolean) : d2, w2 = r2.shouldForwardProp;
    if (i2 && a2.shouldForwardProp) {
      var b2 = a2.shouldForwardProp;
      if (r2.shouldForwardProp) {
        var E2 = r2.shouldForwardProp;
        w2 = function(e3, t2) {
          return b2(e3, t2) && E2(e3, t2);
        };
      } else
        w2 = b2;
    }
    var N2 = new Ke(s2, g2, i2 ? a2.componentStyle : void 0);
    function O2(e3, r3) {
      return function(e4, r4, s3) {
        var i3 = e4.attrs, a3 = e4.componentStyle, c3 = e4.defaultProps, p3 = e4.foldedComponentIds, d3 = e4.styledComponentId, h3 = e4.target, f3 = React.useContext(Qe), m3 = Le(), y3 = e4.shouldForwardProp || m3.shouldForwardProp;
        var v2 = I(r4, f3, c3) || C, g3 = function(e5, n2, o2) {
          for (var r5, s4 = __assign(__assign({}, n2), { className: void 0, theme: o2 }), i4 = 0; i4 < e5.length; i4 += 1) {
            var a4 = re(r5 = e5[i4]) ? r5(s4) : r5;
            for (var c4 in a4)
              s4[c4] = "className" === c4 ? ie(s4[c4], a4[c4]) : "style" === c4 ? __assign(__assign({}, s4[c4]), a4[c4]) : a4[c4];
          }
          return n2.className && (s4.className = ie(s4.className, n2.className)), s4;
        }(i3, r4, v2), S3 = g3.as || h3, w3 = {};
        for (var b3 in g3)
          void 0 === g3[b3] || "$" === b3[0] || "as" === b3 || "theme" === b3 && g3.theme === v2 || ("forwardedAs" === b3 ? w3.as = g3.forwardedAs : y3 && !y3(b3, S3) || (w3[b3] = g3[b3], y3 || true));
        var E3 = function(e5, t2) {
          var n2 = Le(), o2 = e5.generateAndInjectStyles(t2, n2.styleSheet, n2.stylis);
          return o2;
        }(a3, g3);
        var N3 = ie(p3, d3);
        return E3 && (N3 += " " + E3), g3.className && (N3 += " " + g3.className), w3[L(S3) && !A.has(S3) ? "class" : "className"] = N3, w3.ref = s3, reactExports.createElement(S3, w3);
      }(D2, e3, r3);
    }
    O2.displayName = y2;
    var D2 = React.forwardRef(O2);
    return D2.attrs = S2, D2.componentStyle = N2, D2.displayName = y2, D2.shouldForwardProp = w2, D2.foldedComponentIds = i2 ? ie(a2.foldedComponentIds, a2.styledComponentId) : "", D2.styledComponentId = g2, D2.target = i2 ? a2.target : e2, Object.defineProperty(D2, "defaultProps", { get: function() {
      return this._foldedDefaultProps;
    }, set: function(e3) {
      this._foldedDefaultProps = i2 ? function(e4) {
        for (var t2 = [], n2 = 1; n2 < arguments.length; n2++)
          t2[n2 - 1] = arguments[n2];
        for (var o2 = 0, r3 = t2; o2 < r3.length; o2++)
          le(e4, r3[o2], true);
        return e4;
      }({}, a2.defaultProps, e3) : e3;
    } }), ue(D2, function() {
      return ".".concat(D2.styledComponentId);
    }), c2 && oe(D2, e2, { attrs: true, componentStyle: true, displayName: true, foldedComponentIds: true, shouldForwardProp: true, styledComponentId: true, target: true }), D2;
  }
  function it(e2, t2) {
    for (var n2 = [e2[0]], o2 = 0, r2 = t2.length; o2 < r2; o2 += 1)
      n2.push(t2[o2], e2[o2 + 1]);
    return n2;
  }
  var at = function(e2) {
    return Object.assign(e2, { isCss: true });
  };
  function ct(t2) {
    for (var n2 = [], o2 = 1; o2 < arguments.length; o2++)
      n2[o2 - 1] = arguments[o2];
    if (re(t2) || ce(t2))
      return at(Je(it(_, __spreadArray([t2], n2, true))));
    var r2 = t2;
    return 0 === n2.length && 1 === r2.length && "string" == typeof r2[0] ? Je(r2) : at(Je(it(r2, n2)));
  }
  function lt(n2, o2, r2) {
    if (void 0 === r2 && (r2 = C), !o2)
      throw he(1, o2);
    var s2 = function(t2) {
      for (var s3 = [], i2 = 1; i2 < arguments.length; i2++)
        s3[i2 - 1] = arguments[i2];
      return n2(o2, r2, ct.apply(void 0, __spreadArray([t2], s3, false)));
    };
    return s2.attrs = function(e2) {
      return lt(n2, o2, __assign(__assign({}, r2), { attrs: Array.prototype.concat(r2.attrs, e2).filter(Boolean) }));
    }, s2.withConfig = function(e2) {
      return lt(n2, o2, __assign(__assign({}, r2), e2));
    }, s2;
  }
  var ut = function(e2) {
    return lt(st, e2);
  }, pt = ut;
  A.forEach(function(e2) {
    pt[e2] = ut(e2);
  });
  const DefaultColumnFilter = ({ column: { filterValue, preFilteredRows, setFilter } }) => {
    const count = preFilteredRows.length;
    return /* @__PURE__ */ jsxRuntimeExports.jsx(
      Input,
      {
        value: filterValue || "",
        onChange: (e2) => {
          setFilter(e2.target.value || void 0);
        },
        placeholder: `Search ${count} records...`
      }
    );
  };
  const EditableCell = ({ value: initialValue, row: { index }, column: { id: id2 }, updateMyData }) => {
    const [value, setValue] = reactExports.useState(initialValue);
    const onChange = (e2) => {
      setValue(e2.target.value);
    };
    const onBlur = () => {
      updateMyData(index, id2, value);
    };
    reactExports.useEffect(() => {
      setValue(initialValue);
    }, [initialValue]);
    return /* @__PURE__ */ jsxRuntimeExports.jsx(Input, { value, onChange, onBlur });
  };
  const DataTableWrapper = pt.div`
    .table {
        width: 100%;
    }
`;
  const DataTable = ({ data: initialData, comm_id }) => {
    const [data, setData] = reactExports.useState(initialData);
    const updateMyData = (rowIndex, columnId, value) => {
      setData(
        (old) => old.map((row, index) => {
          if (index === rowIndex) {
            return {
              ...row,
              [columnId]: value
            };
          }
          return row;
        })
      );
      const comm = window.Jupyter.notebook.kernel.comm_manager.get_comm(comm_id);
      if (comm) {
        comm.send({ method: "update", content: { rowIndex, columnId, value } });
      }
    };
    const columns = reactExports.useMemo(() => {
      if (data.length === 0)
        return [];
      return Object.keys(data[0]).map((key) => ({
        Header: key,
        accessor: key,
        Filter: DefaultColumnFilter,
        Cell: EditableCell
      }));
    }, [data]);
    const defaultColumn = reactExports.useMemo(
      () => ({
        Filter: DefaultColumnFilter,
        Cell: EditableCell
      }),
      []
    );
    const {
      getTableProps,
      getTableBodyProps,
      headerGroups,
      rows,
      prepareRow,
      setFilter,
      state: { filters }
    } = reactTableExports.useTable(
      {
        columns,
        data,
        defaultColumn,
        updateMyData
      },
      reactTableExports.useFilters,
      reactTableExports.useSortBy
    );
    return /* @__PURE__ */ jsxRuntimeExports.jsx(ChakraProvider, { theme: customTheme, children: /* @__PURE__ */ jsxRuntimeExports.jsx(DataTableWrapper, { children: /* @__PURE__ */ jsxRuntimeExports.jsx(Box, { p: 4, borderWidth: "1px", borderRadius: "lg", overflow: "hidden", children: /* @__PURE__ */ jsxRuntimeExports.jsxs(Table, { ...getTableProps(), className: "table", children: [
      /* @__PURE__ */ jsxRuntimeExports.jsx(Thead, { children: headerGroups.map((headerGroup) => /* @__PURE__ */ jsxRuntimeExports.jsx(Tr, { ...headerGroup.getHeaderGroupProps(), children: headerGroup.headers.map((column2) => /* @__PURE__ */ jsxRuntimeExports.jsxs(Th, { ...column2.getHeaderProps(), children: [
        column2.render("Header"),
        /* @__PURE__ */ jsxRuntimeExports.jsx("div", { children: column2.canFilter ? column2.render("Filter") : null })
      ] })) })) }),
      /* @__PURE__ */ jsxRuntimeExports.jsx(Tbody, { ...getTableBodyProps(), children: rows.map((row) => {
        prepareRow(row);
        return /* @__PURE__ */ jsxRuntimeExports.jsx(Tr, { ...row.getRowProps(), children: row.cells.map((cell) => /* @__PURE__ */ jsxRuntimeExports.jsx(Td, { ...cell.getCellProps(), children: cell.render("Cell") })) });
      }) })
    ] }) }) }) });
  };
  window.VMComponents = {
    DataTable
  };
  window.React = React;
  window.ReactDOM = ReactDOM;
})();
