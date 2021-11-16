// const marked = require("marked");
// const renderer = new marked.Renderer();
// const { BundleAnalyzerPlugin } = require('webpack-bundle-analyzer')
// const HtmlWebpackPlugin = require('html-webpack-plugin')
const path = require('path')
module.exports = {
  publicPath: path.join(__dirname, 'dist').replace(/\\/g, '/'),
  configureWebpack: {
    devtool: 'source-map',
    plugins: [
      // new BundleAnalyzerPlugin({
      //   analyzerHost: 'localhost',
      //   analyzerPort: '8088'
      // }),
      // new HtmlWebpackPlugin({
      //   prefetch: false,
      //   preload: false
      // }),
    ]
  },
  chainWebpack: config => {
    // config
    //   .entry('app')
    //   .clear()
    //   .add('babel-polyfill')
    //   .add('E:\\py_pro\\opr-record-pc\\ui\\html\\src\\main.js')
    // console.log('plugins:', )
    // config.plugins.delete('prefetch')
    // config.plugins.delete('preload')
    config.module
      .rule('md')
      .test(/\.md$/)
      .use('html-loader')
      .loader('html-loader')
      .end()
      .use('markdown-loader')
      // .tap(options => {
      //   // 修改它的选项...
      //   console.log(options)
      //   options.renderer = renderer
      //   return options
      // })
      .loader('markdown-loader')
      .end()
    // config
    //   .plugin('html')
    //   .tap(args => {
    //     // args[0].publicPath = path.join(__dirname, 'dist').replace(/\\/g, '/')
    //     console.log(args)
    //     return args
    //   })
    //   .end()
  },
  css: {
    loaderOptions: {
      less: {
        lessOptions: {
          modifyVars: {
            'primary-color': '#2DC84D',
            'link-color': '#2DC84D',
            'font-family': '"Microsoft YaHei", "Helvetica Neue"',
            'body-background': '#F2F4F8',
            'layout-header-background': '#F2F4F8',
            'layout-header-padding': '0 15px',
            'layout-footer-background': '#F2F4F8',
            'layout-footer-padding': '17px',
            'layout-header-height': '50px',
            'menu-bg': '#FFFFFF',
            'menu-collapsed-width': '50px',
            'border-radius-base': '3px',
            'text-color': '#666666',
            'item-hover-bg': '#F2FAF7',
            'table-row-hover-bg': '#F2FAF7',
            'table-selected-row-bg': '#F2FAF7'
          },
          javascriptEnabled: true
        }
      }
    }
  }
}