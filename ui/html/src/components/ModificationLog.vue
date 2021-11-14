<template>
  <div>
    <div style="width: 100%; overflow: hidden;">
      <div v-if="logList && logList.length">
        <div style="overflow: auto">
          <table class="modify-log">
            <thead>
              <tr>
                <template v-for="colItem in columns">
                  <th :key="colItem.dataIndex">{{ colItem.title }}</th>
                </template>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(row,index) in logList" :key="index">
                <template v-for="(colItem,colIndex) in row">
                  <td
                    v-if="colItem && colItem.show"
                    :key="index + '_' + colIndex"
                    :rowspan="colItem.rowspan"
                  >
                    <span v-if="colItem.key === 'createdDate'">{{ colItem.value }}</span>
                    <span v-else-if="colItem.key === 'attachmentUrl'"><s-download :value="colItem.value" /></span>
                    <span v-else>{{ colItem.value }}</span>
                  </td>
                </template>
              </tr>
            </tbody>
          </table>
        </div>
        <a-pagination
          v-model="current"
          style="width:120%; padding-top: 1rem;"
          :page-size-options="pageSizeOptions"
          :total="total"
          show-size-changer
          :page-size="pageSize"
          @showSizeChange="onShowSizeChange"
          @change="logPageChange"
        >
          <template slot="buildOptionText" slot-scope="props">
            <span v-if="props.value !== '100'">{{ props.value }}条/页</span>
            <span v-if="props.value === '100'">全部</span>
          </template>
        </a-pagination>
      </div>
      <div v-else style="text-align:center;line-height:120px">暂无调整记录</div>
    </div>
  </div>
</template>
<script>
import api from '@/api'
export default {
  props: {
    id: {
      type: Number,
      default: null
    },
    logType: {
      type: String,
      default: 'budget'
    },
    columns: {
      type: Array,
      default: () => []
    },
    mergeFields: {
      type: Array,
      default: () => ['createdByName', 'createdDate', 'remark', 'attachmentUrl']
    }
  },
  data () {
    return {
      pageSizeOptions: ['5', '10', '20', '50', '100'],
      current: 1,
      pageSize: 5,
      total: 0,
      logList: []
    }
  },
  watch: {
    id: {
      handler (val) {
        if (val) {
          this.fetchData()
        }
      },
      immediate: true
    }
  },
  created () {
    this.fetchData()
  },
  methods: {
    async fetchData () {
      const res = await api.getppmodifylog({
        pageNum: this.current,
        pageSize: this.pageSize,
        businessId: this.id,
        businessType: this.logType
      })
      if (res.code === 200) {
        if (res.data) {
          this.logList = this.buildMergeTableData(res.data.records, this.columns)
          this.total = res.data.total
        }
      } else {
        this.$message.warn(res.message)
      }
    },
    onShowSizeChange (current, pageSize) {
      this.pageSize = pageSize
      this.current = current
      this.fetchData()
    },
    logPageChange (current, pageSize) {
      this.pageSize = pageSize
      this.current = current
      this.fetchData()
    },
    buildMergeTableData (dataList, columns) {
      const columnKeys = columns.map((col) => col.dataIndex)
      // 把需要合并的字段，注入到每条数据自身的detailLogList里面
      // 然后把所有 detailLogList 合并成一个一维数组进行渲染
      let oneDimensional = []
      dataList.forEach((row) => {
        row.detailLogList.forEach((detailItem, index) => {
          this.mergeFields.forEach((field) => {
            detailItem[field] = row[field]
          })
          // 确认合并行数
          detailItem.rowspan = row.detailLogList.length
          // 给每行合并的单元格进行排位标记，后面会用到
          detailItem.seq = index
        })
        oneDimensional = oneDimensional.concat(row.detailLogList)
      })
      const twoDimensional = []
      // 通过双循环构建二维矩阵，最后交给tr和td循环渲染
      oneDimensional.forEach((row, x) => {
        Object.keys(row).forEach((colKey) => {
          if (!twoDimensional[x]) twoDimensional[x] = [] // 初始化
          const model = {
            value: row[colKey],
            key: colKey,
            show: true,
            rowspan: 1,
            colspan: 1
          }
          // 如果是需要合并的那一列，判断显示隐藏
          // 判断逻辑：如果seq = 0，就显示，其他都隐藏
          if (this.mergeFields.includes(colKey)) {
            model.rowspan = row['rowspan']
            if (row.seq !== 0) {
              model.show = false
            }
          }
          const y = columnKeys.indexOf(colKey)
          if (y > -1) {
            twoDimensional[x][y] = model
          }
        })
      })
      return twoDimensional
    }
  }
}
</script>
<style lang="less" scoped>
table.modify-log {
  width: 100%;
  border-top: 1px solid #e8e8e8;
  border-left: 1px solid #e8e8e8;
   thead {
    th {
      border-bottom: 1px solid #e8e8e8;
      border-right: 1px solid #e8e8e8;
      padding: 8px 10px;
      background-color: #F6F7F9;
      color: #868C97;
      font-weight: bolder;
      -webkit-transition: background 0.3s ease;
      transition: background 0.3s ease;
      background: #fafafa;
      box-sizing: border-box;
      white-space: nowrap;
    }
   }
   tbody {
    td {
      border-right: 1px solid #e8e8e8;
      padding: 8px 10px;
      border-bottom: 1px solid #e8e8e8;
      -webkit-transition: all 0.3s, border 0s;
      transition: all 0.3s, border 0s;
      box-sizing: border-box;
      white-space: nowrap;
      text-align: left;
      border-collapse: collapse;
      color: #333333;
      font-size: 14px;
      font-variant: tabular-nums;
      line-height: 1.5;
      list-style: none;
      -webkit-font-feature-settings: 'tnum';
      font-feature-settings: 'tnum';
    }
  }
}
</style>
