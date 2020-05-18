import Vue from "vue";
import VueRouter from "vue-router";

import Answer from "./views/games/Answer";
import Question from "./views/games/Question";
import Result from "./views/games/Result";
import Setting from "./views/games/Setting";

import Entrance from "./views/users/Entrance";
import Home from "./views/users/Home";
import New from "./views/users/New";

import AdminIndex from "./views/admin/AdminIndex";
import CreateSong from "./views/admin/CreateSong";

import Test from "./views/games/Test";

Vue.use(VueRouter)

const router = new VueRouter({
  //todo:サーバーでmode historyのredirect設定をする
  mode: "history",
  routes: [
    {path: '/game/answer', component: Answer},
    {path: '/game/question', component: Question},
    {path: '/game/result', component: Result},
    {path: '/game/setting', component: Setting},

    {path: '/user/entrance', component: Entrance},
    {path: '/', component: Home},
    {path: '/user/new', component: New},

    {path: '/admin/', component: AdminIndex},
    {path: '/admin/song/new/', component: CreateSong},

    {path: '/game/test', component: Test},

  ]
});

export default router
