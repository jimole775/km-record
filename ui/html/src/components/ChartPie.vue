<template>
  <div :id="id" :style="{height: height}" />
</template>

<script>
import echarts from 'echarts'
import utils from '@/utils'

let idIndex = 0

export default {
  name: 'ChartPie',
  props: {
    data: {
      type: Array,
      required: true
    },
    height: {
      type: String,
      default: '300px'
    }
  },
  data () {
    return {
      id: '',
      chartObj: null,
      pieData: this.data
    }
  },
  watch: {
    data: function (newVal) {
      this.pieData = newVal
      this.initChart()
    }
  },
  created () {
    this.genID()
  },
  mounted () {
    this.initChart()
    window.addEventListener('resize', utils.debounce(this.resize, 50))
  },
  methods: {
    genID () {
      idIndex++
      this.id = 'pie' + idIndex
    },
    getLegendByData () {
      if (utils.isEmpty(this.pieData)) {
        return []
      }
      return this.pieData.map(item => {
        return item.name
      })
    },
    createRandomColor (pieData) {
      // ['#F1D9A4', '#B6DF8D', '#9FE7DE', '#A4C8E7', '#B39FEF', '#EFB0D9']
      const res = []
      const cArray = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F']
      function pickOneStyle () {
        // 选择一个色系，一般保持第一位在 8 以上，13以下，可以让整个色块保持是亮色系，但是又不至于太白
        const firstNum = Math.floor(Math.random() * 10) + 8
        const secondNum = Math.floor(Math.random() * 15)
        return `${cArray[firstNum > 13 ? 13 : firstNum]}${cArray[secondNum]}`
      }
      while (res.length < pieData.length) {
        let r = pickOneStyle()
        let g = pickOneStyle()
        let b = pickOneStyle()
        if (!res.includes(`#${r}${g}${b}`)) {
          res.push(`#${r}${g}${b}`)
        }
      }
      return res
    },
    initChart () {
      if (utils.isEmpty(this.pieData)) {
        return
      }
      let option = {
        title: { show: false },
        color: this.createRandomColor(this.pieData),
        tooltip: {
          trigger: 'item',
          formatter: '{b}：{c} ({d}%)'
        },
        series: [
          {
            name: '供应商人员分布',
            type: 'pie',
            radius: '50%',
            center: ['50%', '50%'],
            selectedMode: 'single',
            data: this.pieData,
            itemStyle: {
              emphasis: {
                shadowBlur: 10,
                shadowOffsetX: 0,
                shadowColor: 'rgba(0, 0, 0, 0.5)'
              }
            }
          }
        ]
      }
      this.chartObj = echarts.init(document.getElementById(this.id))
      // 绘制图表
      this.chartObj.setOption(option)
      this.resize()
    },
    resize () {
      if (this.chartObj) {
        this.chartObj.resize()
      }
    }
  },
  beforeDestroy () {
    window.removeEventListener('resize', utils.debounce(this.resize, 50))
  }
}
</script>
