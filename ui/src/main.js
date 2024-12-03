import 'bootstrap/dist/css/bootstrap.css';
import './assets/css/globals.css';
import './assets/css/ui.css';

import { createApp } from 'vue';
import App from './App.vue';
import router from './router';
import { createPinia } from 'pinia';

const pinia = createPinia();
const app = createApp(App);

app.use(router);
app.use(pinia);

app.mount('#app');
