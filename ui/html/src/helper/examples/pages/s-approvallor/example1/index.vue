<template>
  <Panel :code="code" title="审批样例">
    <template slot="example">
      <SApprovallor
        :panes="panes"
        :apimap="apimap"
        :list-config="listConfig"
        :apply-config="applyConfig"
        :approval-config="approvalConfig"
        :before-submit="beforeSubmit"
        :before-render="beforeRender"
      />
    </template>
    <template slot="description">
      简易模式，为了缩减样例代码的数量，列表字段和详情字段都省略了，具体的配置可参考《关键事件》
    </template>
  </Panel>
</template>
<script>
import SApprovallor from '@/components/SApprovallor'
import ApprovalOperation from '@/components/ApprovalOperation'
import code from './code.md'
export default {
  title: '审批样例',
  name: 'Example1',
  components: {
    SApprovallor
  },
  data () {
    return {
      code,
      // “tab”配置项，参数参考 [STabs](./STabs.md) 文档
      panes: [
        {
          tabName: '关键事件',
          type: 'list',
          tabId: '0',
          closable: false,
          visible: false,
          show: false,
          permission: {
            roles: [],
            config: null
          }
        }
      ],
      // 把所有对应的接口都写到 apimap 统一管理
      // 可多不可少
      apimap: {
        0: {
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
      },
      // “数据列表”配置项，参数参考 [STable](./STable.md) 文档
      listConfig: {
        0: {
          columns: [
            {
              title: '编号',
              dataIndex: 'flowNo',
              scopedSlots: { customRender: 'flowNo' },
              scopedSlotsRender (h, record, $vm) {
                return <a onClick={() => $vm.projectApproval(record)}>{ record['flowNo'] }</a>
              }
            }
          ],
          searchor: [
            {
              title: '编号',
              key: 'flowNo',
              component: 'AInput'
            }
          ]
        }
      },
      // “申请页面” 配置项
      applyConfig: {
        0: {
          // 配置需要展示的组件，一个组件等同于一个板块
          components: [{
            component: 'FormItemRender',
            title: '基本信息',
            mode: 'edit',
            show: true,
            formItems: [
              {
                label: '形式',
                key: 'deliveryTypeCode',
                component: 'AInput'
              }
            ]
          }]
        }
      },
      // “审批详情” 配置项
      approvalConfig: {
        0: {
          // 节点名“start”
          start: {
            // 配置每个节点需要展示的组件，一个组件等同于一个板块
            components: {
              // 没权限审批的，只能看“只读”内容
              dispermission: [{
                component: 'FormItemRender',
                title: '基本信息',
                mode: 'readonly',
                show: true,
                formItems: [
                  {
                    label: '形式',
                    key: 'deliveryTypeCode'
                  }
                ]
              }],
              // 有权限进行审批的
              permission: [
                {
                  component: 'FormItemRender',
                  title: '基本信息',
                  mode: 'edit',
                  show: true,
                  formItems: [
                    {
                      label: '形式',
                      key: 'deliveryTypeCode',
                      component: 'AInput'
                    }
                  ]
                },
                {
                  component: ApprovalOperation,
                  title: '审批操作',
                  mode: 'edit',
                  show: true,
                  operationItem: {
                    // 提交的选项
                    radios: [
                      { label: '通过', value: '1', key: 'approvalResult', title: '', component: 'ARadio', event (val, options, vm) {} },
                      { label: '驳回', value: '2', key: 'approvalResult', title: '', component: 'ARadio', event (val, options, vm) {} },
                      { label: '不通过', value: '3', key: 'approvalResult', title: '', component: 'ARadio', event (val, options, vm) {} }
                    ],
                    // 必填项
                    inputs: [
                      {
                        label: '审批意见',
                        key: 'approvalContent',
                        component: 'ATextarea',
                        permissions: ['1', '2', '3'],
                        required: true
                      }
                    ]
                  }
                }
              ]
            }
          }
        }
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
