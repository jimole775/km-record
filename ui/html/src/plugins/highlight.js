import Vue from 'vue'
import hljs from 'highlight.js'
import 'highlight.js/styles/googlecode.css'
import javascript from 'highlight.js/lib/languages/javascript'
hljs.registerLanguage('javascript', javascript)
Vue.directive('hljs', function (el, data) {
  el.innerHTML = data.value
  let blocks = el.querySelectorAll('pre code')
  blocks.forEach((block) => {
    hljs.highlightBlock(block)
  })
})
