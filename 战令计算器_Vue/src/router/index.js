import Vue from 'vue'
import Router from 'vue-router'
import Zhanling from '@/components/Zhanling'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'ZhanLing',
      component: Zhanling
    }
  ]
})
