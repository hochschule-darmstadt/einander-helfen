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
            path: '/offers/:category',
            name: 'offers',
            component: () => import('@/views/Offers.vue')
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
            path: '/about',
            name: 'about',
            component: () => import('@/views/About.vue')
        },
        {
            path: '*',
            name: 'not-found',
            component: () => import('@/views/PageNotFound.vue')
        },
    ],
});
