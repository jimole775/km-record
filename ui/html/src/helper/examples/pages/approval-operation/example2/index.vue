<template>
  <Panel :code="code" title="自定义审批样例">
    <template slot="example">
      <ApprovalOperation
        ref="ApprovalOperationRef"
        :operation-item="options"
        @submit="submitHandler"
      />
    </template>
    <template slot="description">
      自定义关闭按钮
    </template>
  </Panel>
</template>
<script>
import code from './code.md'
import ApprovalOperation from '@/components/ApprovalOperation'
export default {
  title: '自定义审批',
  name: 'Example2',
  components: {
    ApprovalOperation
  },
  data () {
    return {
      code,
      options: {
        // 提交的选项
        radios: [
          { label: '通过', value: '1', key: 'approvalResult', title: '', component: 'ARadio', event (val, options, vm) {} },
          { label: '驳回', value: '2', key: 'approvalResult', title: '', component: 'ARadio', event (val, options, vm) {} },
          { label: '转审', value: '8', key: 'approvalResult', title: '', component: 'ARadio', event (val, options, vm) {} }
        ],
        // 必填项
        inputs: [
          {
            label: '转审人',
            key: 'transfer',
            component: 'UserSelect',
            paramKeys: ['transferAccount', 'transferName'],
            permissions: ['8'],
            change (val, options, vm) {},
            required: true
          },
          {
            label: '审批意见',
            key: 'approvalContent',
            component: 'ATextarea',
            permissions: ['1', '2'],
            change (val, options, vm) {},
            required: true
          }
        ],
        footerCustomRender (h, item, vm) { // $vm属于approval 实例   $vm.$$target 当前节点实例  vmprops映射对象
          let tar = vm.$$target
          let cur = tar.$parent.$parent
          return (<a-form-item label={' '} label-col={{ span: 2 }} wrapper-col={{ span: 18 }}>
            <a-button type="primary" onClick={() => { tar.emitSubmit() }}>提交</a-button>
            <a-button style="margin-left: 1rem" onClick={() => cur.closeHandler(tar)}>关闭</a-button>
          </a-form-item>)
        }
      }
    }
  },
  methods: {
    submitHandler (data) {
      this.$modal.success({
        title: '操作结果',
        content: JSON.stringify(data)
      })
    },
    closeHandler (tar) {
      const res = tar.form.getFieldsValue()
      this.$modal.success({
        title: '操作结果',
        content: JSON.stringify({ ...res, approvalResult: tar.approvalResult })
      })
    }
  }
}
</script>
