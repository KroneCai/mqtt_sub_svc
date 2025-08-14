import { createRouter, createWebHistory, RouteRecordRaw } from 'vue-router'
import Home from '@/views/Home.vue'
import { useMenuStore } from '@/stores/menuStore'

// 静态路由配置
const routes: RouteRecordRaw[] = [
  {
    path: '/',
    redirect: '/home'
  },
  {
    path: '/home',
    name: 'Home',
    component: Home,
    meta: { title: '首页', requiresAuth: true }
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/Login.vue'),
    meta: { title: '登录' }
  },
  // 404页面需放在最后
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: () => import('@/views/error/404.vue')
  }
]

// 动态加载组件的方法
const lazyLoad = (path: string) => {
  return () => import(`@/views/${path}.vue`)
}

// 添加动态路由
export const addDynamicRoutes = async () => {
  const menuStore = useMenuStore()
  await menuStore.fetchMenus()
  
  menuStore.menuList.forEach(menu => {
    router.addRoute({
      path: menu.path,
      name: menu.name,
      component: lazyLoad(menu.component),
      meta: menu.meta,
      children: menu.children?.map(child => ({
        path: child.path,
        name: child.name,
        component: lazyLoad(child.component),
        meta: child.meta
      }))
    })
  })
}

router.beforeEach(async (to, from, next) => {
  // 验证需要登录的路由
  if (to.meta.requiresAuth && !localStorage.getItem('token')) {
    next({ name: 'Login' })
    return
  }

  // 首次加载时添加动态路由
  if (to.name !== 'Login' && !router.hasRoute('System')) {
    await addDynamicRoutes()
    next({ ...to, replace: true }) // 重定向到目标路由
    return
  }

  next()
})

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router