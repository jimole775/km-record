<template>
  <div class="panel-base">
    <div class="example">
      <slot name="example" />
    </div>
    <div class="desc">
      <span class="desc-title">
        <slot name="title">
          <span>{{ title }}</span>
        </slot>
      </span>
      <slot name="description">
        <div v-hljs="description" />
      </slot>
    </div>
    <div :class="['fold', show && 'fold-open']">
      <a @click="show = !show">
        <span class="fold-icon">&lt;{{ show ? '/' : '&nbsp;' }}&gt;</span>
      </a>
    </div>
    <div v-if="show" class="code">
      <slot name="code">
        <div v-hljs="code" />
      </slot>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Panel',
  props: {
    title: {
      type: String,
      default: '样例说明'
    },
    description: {
      type: String,
      default: ''
    },
    code: {
      type: String,
      default: ''
    }
  },
  data () {
    return {
      show: false
    }
  }
}
</script>

<style lang="less" scoped>
.panel-base {
  font-size: 12px;
  border: 1px solid #ebedf0;
  margin-bottom: 1rem;
}
.example {
  padding: 1rem;
}
.desc {
  padding: 1rem;
  position: relative;
  border-top: 1px solid #ebedf0;
  .desc-title {
    position: absolute;
    top: -0.55rem;
    background: #fff;
    left: 1rem;
    color: #777;
    padding: 0 0.8rem;
    font-weight: 800;
  }
}
.fold {
  a {
    text-align: center;
    display: block;
  }
  padding: 5px;
  border-top: 1px dashed #ebedf0;
}
.fold-open {
  border-bottom: 1px dashed #ebedf0;
}
.code {
  /deep/ pre {
    padding: 1rem 1.5rem;
  }
}
.fold-icon {
  font-size: 12px;
}
</style>
