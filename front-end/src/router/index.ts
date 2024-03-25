import {createRouter, createWebHashHistory, RouteRecordRaw} from 'vue-router';

import SalesHotline from '../views/SalesHotline.vue';
import CallCentre from '../views/CallCentre.vue';

const routes: Array<RouteRecordRaw> = [
    {path: '/', component: SalesHotline},
    {path: '/CallCentre', component: CallCentre},
];

const router = createRouter({
    history: createWebHashHistory(),
    routes,
});

export default router;
