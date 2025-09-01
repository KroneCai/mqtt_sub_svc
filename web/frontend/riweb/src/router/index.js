import { createRouter, createWebHistory } from 'vue-router'
import {useAuthStore} from "@/stores/auth.store";
import layouts from "@/layouts"

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/login',
      name: 'Login',
      meta: {requiresAuth: false, menuIndex:'Login'},
      component: () => import('../views/Login.vue')
    },
    {
      path: '/',
      alias: ['/home'],
      name: 'Home',
      meta: {requiresAuth: true, requiresRole:'user', menuIndex:'M1', layout:'TenantLayout'},
      component: () => import('../views/Home.vue')
    },
    {
      path: '/dashboard',
      alias: ['/dashboard/home'],
      name: 'Dashboard Overview',
      meta: {requiresAuth: true, requiresRole:'user', menuIndex:'M1', layout:'TenantLayout'},
      component: () => import('../views/Dashboard.vue')
    },
  ]
})

// 路由守卫
router.beforeEach((to, from, next) => {
  // 动态设置页面布局
  const layout = to.meta.layout || 'TenantLayout'
  document.body.setAttribute('data-layout', layout)

  //安全认证
  const authStore = useAuthStore();
  // 检查路由是否需要认证
  if(to.meta.requiresAuth && !authStore.isAuthenticated) {
    next({path: '/login'});
    return;
  }
  // 检查角色权限
  if(to.meta.requiresRole){
    if(!authStore.user.user_roles.includes(to.meta.requiresRole)){
      next({path: '/'});
      return;
    }
  }
  // 如果已登录且访问登录页，重定向到首页
  if (to.path === '/login' && authStore.isAuthenticated) {
    next('/');
    return;
  }
  next();
});

export default router