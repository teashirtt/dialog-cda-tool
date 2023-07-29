import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import Unocss from 'unocss/vite'
import { presetUno, presetAttributify } from 'unocss'
import { visualizer } from 'rollup-plugin-visualizer'

export default defineConfig({
  server: {
    port: 5100,
    proxy: {
      '/req/': {
        target: 'http://127.0.0.1:5200/',
        pathRewrite: { '^/req/': '' },
        ws: true,
        changeOrigin: true
      }
    }
  },
  plugins: [
    vue(),
    Unocss({
      presets: [
        presetUno(),
        presetAttributify()
      ]
    }),
    visualizer({
      emitFile: false,
      filename: 'analysis-chart.html',
      open: true
    })
  ]
})
