import Vue from 'vue'
import api from '@/api'
import router from '@/router'
import store from '@/store'
import base64 from './base64'

const jumper = {}
const allRoutes = router.matcher.getRoutes()
const directRoutes = allRoutes.filter((r) => r.meta && r.meta.directConnection)
const directRouteMap = routes2map(directRoutes)

/**
* 通用跳转方法
* @param {Object} item
* @template go({
*  【必填】__key__: 'RECRUITION', # 业务类型
*  【可选】__id__: 1004, # 流程id 注意区分【流程实例id】
*  【可选】__tabType__: 'list'|'detail', # 对应《OmsTab.vue》或者《OmsTabPlus.vue》的tab类型
*  【可选】__tabIndex__: '0', # 对应《OmsTab.vue》或者《OmsTabPlus.vue》的tab下标
*  【可选】__todoType__: 'apply'|'approval', # 对应《主页待办》的 “我的申请” 或 “我的审批”
*  【可选】__params__: {}
* })
*/
jumper.go = async function (item) {
  item = depolyCommonProperty(item)

  // 转成小写，方便阅读
  const category = (item.__key__ || '').trim().toLocaleLowerCase()

  // 【流程实例id】，主要用来查询审批日志的
  if (!item.id) {
    const apiName = directRouteMap[category].idFrom
    item.id = await loadIdByApi(item, apiName)
  }

  dispatchTodoParams(category, item)
  matchRouterPath(category, item)
}

/**
 * 新窗口打开一个页面
 * @param {Object|Map} targetDetail
 * @return {Undefined}
 * @template newWindow() # 不带参数，直接停留在主页
 * @template newWindow({ # 参数可参考 jumper.go() })
 */
jumper.newWindow = function (targetDetail) {
  if (targetDetail && targetDetail.__key__) {
    // 另开一个页面展示
    const params = base64.encode(JSON.stringify(targetDetail))
    window.open(`?omsjump=${params}`)
  } else {
    window.open()
  }
}

// 配置公共属性
function depolyCommonProperty (item) {
  // taskType: 是待办列表的一个属性值，用作跳到列表页的判断
  // businessCategory: 是当条待办的一个属性值，用作跳到详情页的判断
  item.__key__ = item.__key__ || item.taskType || item.businessCategory

  // tab类型 => "list": 列表页，"detail": 详情页
  // 默认为 'detail'，主要是为了兼容 mo 跳转的类型
  // 现在mo都是在审批阶段才跳到oms处理，所以在跳转链接中缺省了待办类型
  item.__tabType__ = item.__tabType__ || 'detail'

  // 待办类型 => "apply": 我的申请，"approve": 我的审批，为了区分查询字段的默认赋值“申请人”，“当前处理人”
  // 默认为 'approve'，理由和 __tabType__ 相同
  item.__todoType__ = item.__todoType__ || 'approve'

  // 默认拼装登陆人
  item.handler = spillUserSelectValue()

  // 默认参数
  item.prNo = item.prNo || item.title
  item.flowNo = item.flowNo || item.title
  item.flowNode = item.flowNode || item.statusCode
  item.instanceId = item.instanceId || item.businessId || item.__id__
  item.flowInstanceId = item.flowInstanceId || item.businessId || item.__id__
  item.projectFlowInstanceId = item.projectFlowInstanceId || item.businessId || item.__id__
  item.purchaseFlowInstanceId = item.purchaseFlowInstanceId || item.businessId || item.__id__
  return item
}

// 匹配路由，并进行跳转
function matchRouterPath (category, item) {
  if ([
    'project_purchase_flow',
    'tm_project_purchase_flow',
    'inherit_project_purchase_flow',
    'inherit_tm_project_purchase_flow'
  ].includes(category)) {
    const userRole = store.state.global.userRole || {}
    // 项目采购需要根据登陆人来区分跳转的路由
    if (userRole.type === 'SUPPLIER') {
      router.push({ path: '/pp-project/purchase-supplier' })
    } else {
      router.push({ path: '/pp-project/purchase' })
    }
  } else {
    const params = directRouteMap[category]
    router.push({
      path: params.path,
      query: {
        ...params,
        path: undefined // 清掉path字段，避免转译问题
      }
    })
  }
}

// 保存跳转参数到全局
// businessType：0：保存到 localStorage
// businessType：1：保存到 Vuex
function dispatchTodoParams (category, item) {
  const params = directRouteMap[category]
  const businessType = params.businessType
  // 旧业务类型
  if (businessType === 0) {
    if (item.__tabType__ === 'list') {
      Vue.localStorage.setItem('fromHomeTodoCount', JSON.stringify({ ...params, ...item }))
    }
    if (item.__tabType__ === 'detail') {
      Vue.localStorage.setItem('fromHomeTodoDetail', JSON.stringify({ ...params, ...item }))
    }
  }
  // 新业务类型
  if (businessType === 1) {
    store.commit('setTodoParams', { ...params, ...item })
  }
}

// 根据每个具体审批模块的【基础信息】接口来获取id号
// ID号主要用来查询操作日志
function loadIdByApi (item, apiName) {
  return new Promise(async (resolve) => {
    if (apiName) {
      const res = await api[apiName](item)
      if (res.code === 200 && res.data) {
        resolve(res.data.id)
      } else {
        resolve('')
        throw new Error('操作日志获取流程id失败！')
      }
    } else {
      resolve('')
      if (item.__tabType__ === 'detail') {
        throw new Error('操作日志丢失流程id查询接口，请完善businessApiMap！')
      }
    }
  })
}

// 主要用于给搜索栏【申请人】【当前处理人】赋默认值
function spillUserSelectValue () {
  const res = {}
  const user = store.state.global.user
  res.key = JSON.stringify({ key: user && user.employeeNumber, label: user && user.name })
  res.label = user && user.name
  return [res]
}

/**
* 把 routes 数组转成 map, 方面调用
* @param {Array} routes
* @returns {Object}
*/
function routes2map (routes) {
  const map = Object.create(null)
  routes.forEach(r => {
    const path = r.path
    const tagsMap = r.meta.directConnection
    Object.keys(tagsMap).forEach(tag => {
      map[tag] = {
        path,
        ...tagsMap[tag]
      }
    })
  })
  return map
}

export default jumper
