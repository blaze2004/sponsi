import 'bootstrap/dist/css/bootstrap.css'
import './assets/css/globals.css'
import './assets/css/ui.css'

import { createApp } from 'vue'
import App from './App.vue'
import router from './router'

const app=createApp(App)

app.use(router)

app.mount('#app')
