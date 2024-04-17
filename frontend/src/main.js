import { createApp } from "vue";
import App from "./App";
import axios from 'axios';
import VueAxios from 'vue-axios'

import "@/assets/global.css"
import 'bootstrap/dist/css/bootstrap.css';
import 'bootstrap-vue/dist/bootstrap-vue.css';

const axiosInstance = axios.create({
    // baseURL: '/api',
    baseURL: 'http://192.168.0.19:8000/api',
    headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
    },
    timeout: 5000,
});

const app = createApp(App);
app.use(VueAxios, axiosInstance);
app.mount('#app');



