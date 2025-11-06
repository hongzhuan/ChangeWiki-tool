// router/index.js
import Vue from 'vue';
import Router from 'vue-router';

Vue.use(Router)

const routes = [
    // {
    //     path: '/',
    //     name: 'HomePage',
    //     component: () => import('../views/HomePagecopy.vue')
    // },
    {
        path: '/',
        name: 'Login',
        component: () => import('../components/Login.vue')
    },
    {
        path: '/userInfo',
        name: 'userInfo',
        component: () => import('../components/userInfo.vue')
    },
    {
        path: '/Register',
        name: 'Register',
        component: () => import('../components/Register.vue')
    },
    {
        path: '/HomePagecopy',
        name: 'HomePage',
        component: () => import('../views/HomePagecopy.vue')
    },
    {
        path: '/versionthree/ReverseAndChangesTotalPage.vue',
        name: 'ReverseAndChangesTotalPage',
        component: () => import('../components/versionthree/ReverseAndChangesTotalPage.vue')
    },
]

const router = new Router({
    routes
})

export default router
