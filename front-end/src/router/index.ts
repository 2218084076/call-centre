import {createRouter, createWebHashHistory, RouteRecordRaw} from 'vue-router';

import AiSys from '../views/AiSys.vue';
import CallCentre from '../views/CallCentre.vue';
import OrderSys from '../views/OrderSys.vue';
import Main from "../views/Main.vue";
import ChatBot from "../views/ChatBot.vue";
import AtomSys from "../views/AtomSys.vue";
import PromptEditor from "../views/PromptEditor.vue";
import RealtimeSTT from "../views/RealtimeSTT.vue";

const routes: Array<RouteRecordRaw> = [
    {path: '/', component: Main},
    {path: '/chatBot', component: ChatBot},
    {path: '/aiSys', component: AiSys},
    {path: '/callCentre', component: CallCentre},
    {path: '/orderSys', component: OrderSys},
    {path: '/acrosticPoem', component: AtomSys},
    {path: '/promptEditor', component: PromptEditor},
    {path: '/realtimeSTT', component: RealtimeSTT}
];

const router = createRouter({
    history: createWebHashHistory(),
    routes,
});

export default router;
