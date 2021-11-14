<template>
  <Panel :code="code" title="通用审批样例">
    <template slot="example">
      <ApprovalOperation
        :operation-item="options"
        @submit="submitHandler"
      />
    </template>
    <template slot="description">
      通用审批样例
    </template>
  </Panel>
</template>
<script>
import code from './code.md'
import ApprovalOperation from '@/components/ApprovalOperation'
export default {
  title: '通用审批',
  name: 'Example1',
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
            permissions: ['1', '2'],
            change (val, options, vm) {},
            required: true
          }
        ]
      }
    }
  },
  methods: {
    submitHandler (data) {
      this.$modal.success({
        title: '操作结果',
        content: JSON.stringify(data)
      })
    }
  }
}
</script>
