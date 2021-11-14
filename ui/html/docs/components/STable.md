### 样例
``` vue
<template>
  <STable
    :columns="columns" /** 表单列配置 */
    :searchor="searchor" /** 查询头配置 */
    :row-key="'id'" /** 行标记 */
    :data-dict="'xxx'" /** 由于接口不一定都统一，需要在必要时，加一个dataDict路径，帮助获取接口数据 */
    :data-api="'apiNameOrFunction'" /** 绑定表格数据接口 */
    :expand-api="'apiNameOrFunction'" /** 绑定表格数据接口 */
    :import-api="'apiNameOrFunction'" /** 绑定【导入】接口，并开启对应功能按钮，如果为空值就不显示按钮 */
    :export-api="'apiNameOrFunction'" /** 绑定【导出】接口，并开启对应功能按钮，如果为空值就不显示按钮 */
    :abandon-api="'apiNameOrFunction'" /** 绑定批量【放弃】接口，并开启对应功能按钮，如果为空值就不显示按钮 */
    :reject-api="'apiNameOrFunction'" /** 绑定批量【驳回】接口，并开启对应功能按钮，如果为空值就不显示按钮 */
    :pass-api="'apiNameOrFunction'" /** 绑定批量【通过】接口，并开启对应功能按钮，如果为空值就不显示按钮 */
    :revoke-api="'apiNameOrFunction'" /** 绑定批量【撤回】接口，并开启对应功能按钮，如果为空值就不显示按钮 */
    :delete-api="'apiNameOrFunction'" /** 绑定批量【删除】接口，并开启对应功能按钮，如果为空值就不显示按钮 */
    :close-api="'apiNameOrFunction'" /** 绑定批量【关闭】接口，并开启对应功能按钮，如果为空值就不显示按钮 */
    :is-pagination="true" /** 是否翻页 */
    :data-params="null" /** 额外插入查询参数，这个参数会触发fetch */
    :record-status-field="'flowNode'" /** 用来指定每一行数据的状态字段名, 一般【批量处理】时，需要判断是否能操作（比如：end状态的不能撤回） */
    :fetch-immediate="true" /** 是否在渲染table后，立即查询数据 */
    :is-selection="true" /** 是否显示勾选框 */
    :select-mode="'checkbox'" /** 单选还是多选 */
    :show-rank="false" /** 是否显示序号 */
    @update="updateDataSet" /** 刷新回调 */
    @selectChange="selectChange" /** 勾选回调 */

  >
    <!-- 表格头部的摘要插槽 -->
    <template slot="summary">
      <a-button>新建</a-button>
    </template>
  </STable>
</template>
<script>
import STable from '@/components/STable'
export default {
  components: {
    STable
  },
  data () {
    return {
      columns: [
        {
          dataIndex: 'prNo',
          slots: { title: 'prNoTitle' },
          slotsRender (h, vm) {  // 表头插槽实现
            return <h>{ '项目PR' }</h>
          },
          scopedSlots: { customRender: 'prNo' }, // scopedSlots 这个属性定义之后，必须要实现，否则视图只显示空白
          scopedSlotsRender (h, record, vm) {
            return <div>{ record['prNo'] }</div>
          }
        }
      ],
      searchor: [
        {
          title: '项目PR',
          dependKey: 'cityName', // 当前组件（下拉框）的数据，需要依赖其他组件才能自动获取
          key: 'prNo',
          keys: ['projectManagerAccount', 'projectManagerName'], // 查询需要的字段，和 optionKeys 一一对应
          optionKeys: ['key', 'label'], // 选项的取值字段
          /**
           * 这个回调主要的功能就是对需要提交的数据的结构进行修改
           * @param {*} params 需要提交的数据体
           * @param {Object} vm STable模块的代理父级的上下文，STable模块的vm，可以访问vm.$$target
           * @return {Object}
          **/
          beforeSubmit (params, vm) {
            if (params.prNo) {
              params.prNo = 'test'
            }
          },
          /**
           * 这个回调主要的功能就是，在当前组件被渲染之前，可以对 default 属性进行赋值
           * @param {*} params 可以当作需要提交的数据体
           * @param {Object} searchItem 当前项
           * @param {Object} vm STable模块的代理父级的上下文，STable模块的vm，可以访问vm.$$target
           * @return {Object}
          **/
          beforeRender (params, searchItem, vm) {
            searchItem.default = '默认值'
          },
          props: { // vue属性
            'group-code': 'project_type',
            'value-field': 'itemCode',
          },
          domProps: { // dom属性
            innerHTML: ''
          },
          attrs: { // html标签属性
            id: ''
          },
          component: 'xxx'
        }
      ]
    }
  },
  updateDataSet (data) {},
  selectChange (selectRows) {}
}
</script>
```