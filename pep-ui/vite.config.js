import { resolve } from 'path'
import createExternal from 'vite-plugin-external'

export default {
  root: resolve(__dirname, 'src'),
  build: {
    outDir: '../dist'
  },
  plugins: [
    createExternal({
      externals: {
        $: 'window.jQuery'
      }
    })
  ],
  server: {
    port: 8080
  }
}
