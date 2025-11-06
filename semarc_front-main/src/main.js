import Vue from 'vue';
import App from './App.vue';
import Router from './router';
// import store from './store';
import ElementUI from 'element-ui';
import 'element-ui/lib/theme-chalk/index.css';
import './assets/css/common.css'
import '@/assets/font/font.css'
import rem from "@/js/rem";
import ClickEffect from './components/ClickEffect.vue';
Vue.use(ElementUI);
Vue.use(rem);
Vue.use(ClickEffect);

Vue.config.productionTip = false

// 创建全局点击效果实例
const clickEffectInstance = new Vue(ClickEffect).$mount();
document.body.appendChild(clickEffectInstance.$el);

// 全局监听点击事件
document.addEventListener('click', (event) => {
  clickEffectInstance.createClickEffect(event);
});

new Vue({
  render: h => h(App),
  router: Router,
}).$mount('#app')
