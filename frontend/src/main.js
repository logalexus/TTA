import { createApp } from "vue";
import App from "./App";
import axios from 'axios';
import VueAxios from 'vue-axios'
import ToastPlugin from 'vue-toast-notification';
import { createRouter, createWebHistory } from 'vue-router'
import Content from '@/views/Content.vue';

import "@/assets/global.css"
import 'bootstrap/dist/css/bootstrap.css';
import 'vue-toast-notification/dist/theme-bootstrap.css';

const router = createRouter({
  routes: [{
    path: '/',
    name: 'home',
    component: App
  },
  {
    path: '/:stream_id?',
    name: 'stream',
    props: true,
    components: {
      content: Content,
    },
  },
  ],
  linkActiveClass: 'active',
  history: createWebHistory()
})


const axiosInstance = axios.create({
  // baseURL: '/api',
  baseURL: `http://${window.location.hostname}:8000/api`,
  headers: {
    'Accept': 'application/json',
    'Content-Type': 'application/json',
  },
  timeout: 5000,
  withCredentials: true,
});

const app = createApp(App);
app.use(VueAxios, axiosInstance);
app.use(ToastPlugin);
app.use(router)
app.mount('#app');



