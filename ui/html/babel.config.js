module.exports = {
  presets: [
    ['@vue/app', {
      polyfills: [
        'es6.promise',
        'es6.symbol',
        'es7.object.entries'
      ]
    }, '@babel/preset-env']
  ],
  plugins: [
    [
      'import',
      {
        'libraryName': 'ant-design-vue',
        'libraryDirectory': 'es',
        'style': 'true'
      }
    ]
  ]
}
