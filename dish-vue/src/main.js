import { createApp } from 'vue';
import App from './App.vue';
import router from './router'; // 引入路由器
// 导入 ElementPlus 
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'

const app = createApp(App)
// 挂载 ElementPlus
app.use(ElementPlus)
app.use(router)
app.mount('#app');