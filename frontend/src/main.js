import { createApp } from "vue";
import App from "./App";
import axios from 'axios';
import VueAxios from 'vue-axios'
import { createRouter, createWebHistory } from 'vue-router'
import Content from '@/views/Content.vue';

import "@/assets/global.css"
import 'bootstrap/dist/css/bootstrap.css';
import 'bootstrap-vue/dist/bootstrap-vue.css';

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
});

const app = createApp(App);
app.use(VueAxios, axiosInstance);
app.use(router)
app.mount('#app');



