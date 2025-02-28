import { createApp } from 'vue';
import App from './App.vue';
import axios from 'axios';
import './style.scss';
import router from './router';
//import store from './store';
// Создаем экземпляр приложения
const app = createApp(App);
// Настройка Axios в качестве глобального свойства
app.config.globalProperties.$axios = axios;
//app.use(store); 
app.use(router);
// Монтируем приложение
app.mount('#app');
