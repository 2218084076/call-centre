import {createApp} from 'vue'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import * as ElementPlusIconsVue from '@element-plus/icons-vue'


import App from './App.vue'
import router from "@/router";

const app = createApp(App)
for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
    app.component(key, component)
}
app.use(router)
app.use(
    ElementPlus,
    {size: 'small', zIndex: 3000},
)
app["config"]["globalProperties"].baseUrl = 'your api url'
app["config"]["globalProperties"].callCentreUrl = 'http://192.168.8.152:8082/api/v1/'
app.mount('#app')
