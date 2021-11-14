``` vue
<template>
  <SApprovallor
    :panes="panes"
    :apimap="apimap"
    :list-config="listConfig"
    :before-submit="beforeSubmit"
    :before-render="beforeRender"
    :apply-modules-map="applyModulesMap"
    :approval-modules-map="approvalModulesMap"
  />
</template>
<script>
import SApprovallor from '@/components/SApprovallor'
import FormItemViewRender from '@/components/FormItemViewRender'
import ApprovalOperation from '@/components/ApprovalOperation'
const FormItemRenderFormItems = [
  {
    layout: {
      span: 12,
      label: 6,
      wrapper: 18
    },
    label: '交付形式',
    show: true, // 字段是否标志
    required: true, // 字段是否必填
    mode: 'edit', // 编辑状态，如果是readonly并且是编辑组件，默认为禁用
    key: 'deliveryTypeCode', // 和后端交互的字段名
    paramKeys: ['deliveryTypeCode', 'deliveryTypeName'],
    props: {
      'value-field': 'itemCode',
      'group-code': 'dg_delivery'
    },
    labelCustomRender (h, formItem, vm) {
      return vnode
    },
    wrapperCustomRender (h, formItem, vm) {
      return vnode
    },
    change (val, formItem, vm) {},
    component: 'DictSelect' // 组件
  }
]
const FormItemViewRenderFormItems = [
  {
    layout: {
      span: 12,
      label: 6,
      wrapper: 18
    },
    label: '附件上传',
    key: 'files',
    labelCustomRender (h, formItem, vm) {
      return vnode
    },
    wrapperCustomRender (h, formItem, vm) {
      return vnode
    }
  }
]
const ApprovalOperationItems = {
  // 提交的选项
  radios: [
    { label: '通过', value: '1', key: 'approvalResult', title: '', component: 'ARadio', event (val, options, vm) {} },
    { label: '不通过', value: '3', key: 'approvalResult', title: '', component: 'ARadio', event (val, options, vm) {} },
    { label: '驳回', value: '2', key: 'approvalResult', title: '', component: 'ARadio', event (val, options, vm) {} },
    { label: '转审', value: '8', key: 'approvalResult', title: '', component: 'ARadio', event (val, options, vm) {} }
  ],
  // 必填项
  inputs: [
    {
      label: '转审人',
      dedfault: '',
      key: 'transfer',
      component: 'UserSelect',
      paramKeys: ['transferAccount', 'transferName'],
      permissions: ['8'],
      change (val, options, vm) {},
      required: true
    },
    {
      label: '审批意见',
      dedfault: '',
      key: 'approvalContent',
      component: 'ATextarea',
      permissions: ['1', '2', '3'],
      change (val, options, vm) {},
      required: true
    }
  ],
  footerCustomRender (h, operationItem, vm) {
    return vnode
  }
}
const apimodel = {
  apply: 'postkeyeventsstart', // 申请 接口
  approval: 'postkeyeventsapprove', // 审批 接口
  list: 'postkeyeventspage', // 列表查询 接口
  detail: 'getkeyeventsdetail', // 审批详情 接口
  export: 'postkeyeventsexport', // 导出列表 接口
  pass: '', // 批量审批 【通过】接口
  unpass: '', // 批量审批 【不通过】接口
  close: 'postkeyeventsbatchClose', // 批量审批 【关闭】接口
  revoke: 'postkeyeventsbatchRevoke', // 批量审批 【撤回】接口
  reject: '', // 批量审批 【驳回】接口
  appliable: 'basicdata.key-events-apply', // 是否有权限申请
  approvalable: 'basicdata.key-events-apply', // 是否有权限审批
  viewable: 'basicdata.key-events', // 是否有权限查看
  passable: '', // 是否有权限批量通过
  unpassable: '', // 是否有权限批量不通过
  closable: 'basicdata.key-events-close', // 是否有权限批量关闭
  revokable: 'basicdata.key-events-revoke', // 是否有权限批量撤回
  rejectable: '', // 是否有权限批量驳回
  logType: 'key_events_flow' // 日志的type
}
const listmodel = {
  columns: [
    {
      title: '流程编号',
      dataIndex: 'flowNo',
      scopedSlots: { customRender: 'flowNo' },
      scopedSlotsRender (h, record, $vm) {
        return <a onClick={() => $vm.projectApproval(record)}>{ record['flowNo'] }</a>
      }
    }
  ],
  searchor: [
    {
      title: '事件类型',
      key: 'eventsType',
      props: {
        'group-code': 'dg_event',
        'value-field': 'itemCode'
      },
      component: 'DictSelect'
    }
  ]
}
const BaseInfoEdit = { component: 'FormItemRender', title: '基本信息', mode: 'edit', show: true, formItems: FormItemRenderFormItems }
const BaseInfoView = { component: FormItemViewRender, title: '基本信息', mode: 'readonly', show: true, columns: FormItemViewRenderFormItems }
const ApprovalOperationEdit = { component: ApprovalOperation, title: '审批操作', mode: 'edit', show: true, operationItem: ApprovalOperationItems }
const applymodel = {
  components: [BaseInfoEdit]
}
const approvalmodel = {
  start: {
    components: {
      dispermission: [BaseInfoView],
      permission: [BaseInfoEdit, ApprovalOperationEdit]
    }
  }
}
export default {
  components: {
    SApprovallor
  },
  data () {
    return {
      panes: [],
      apimap: {
        0: apimodel
      },
      listConfig: {
        0: listmodel
      },
      applyModulesMap: {
        0: applymodel
      },
      approvalModulesMap: {
        0: approvalmodel
      }
    }
  },
  methods: {
    // 补充遗漏字段，比如申请人，申请部门等
    beforeSubmit (params, $vm) {
      return params
    },
    beforeRender (dataSource, formItems, $vm) {

    }
  }
}

</script>
```
