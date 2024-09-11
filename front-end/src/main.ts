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
app["config"]["globalProperties"].callCentreUrl = 'https://testapp.tfg.ltd/api/v1/'
// app["config"]["globalProperties"].callCentreUrl = 'http://192.168.8.152:8082/api/v1/'

app["config"]["globalProperties"].orderSysUrl = 'https://testapp.tfg.ltd/api/v3/'
// app["config"]["globalProperties"].orderSysUrl = 'http://192.168.8.152:8000/api/v3/'

app["config"]["globalProperties"].atomSysUrl = 'https://testapp.tfg.ltd/api/v4/'
// app["config"]["globalProperties"].atomSysUrl = 'http://192.168.8.152:8088/api/v4/'

app["config"]["globalProperties"].chatbotUrl = 'https://testapp.tfg.ltd/api/atom/'
// app["config"]["globalProperties"].chatbotUrl = 'http://192.168.8.11:8083/api/v1/'

// app["config"]["globalProperties"].aiSysUrl = 'http://192.168.8.152:8000/api/v1/'
app["config"]["globalProperties"].aiSysUrl = 'https://testapp.tfg.ltd/api/atom/'
// app["config"]["globalProperties"].realTimeSTT = 'ws://localhost:8765'
app["config"]["globalProperties"].realTimeSTT = 'ws://lab.tfg.ai:12013'
// app["config"]["globalProperties"].realTimeSTT = 'ws://192.168.8.11:9001'


app.mount('#app')
