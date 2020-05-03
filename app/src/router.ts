import Vue from 'vue';
import Router from 'vue-router';

Vue.use(Router);

export default new Router({
    mode: 'history',
    base: process.env.BASE_URL,
    routes: [
        {
            path: '/',
            name: 'home',
            component: () => import('@/views/Home.vue')
        },
        {
            path: '/imprint',
            name: 'imprint',
            component: () => import('@/views/Imprint.vue')
        },
        {
            path: '/privacy',
            name: 'privacy',
            component: () => import('@/views/Privacy.vue')
        },
        {
            path: '*',
            name: 'not-found',
            component: () => import('@/views/PageNotFound.vue')
        },
    ],
});
