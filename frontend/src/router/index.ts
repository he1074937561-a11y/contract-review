import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      component: () => import('../components/AppLayout.vue'),
      children: [
        { path: '', name: 'Upload', component: () => import('../views/Upload.vue'), meta: { requiresAuth: true } },
        { path: 'contracts', name: 'History', component: () => import('../views/History.vue'), meta: { requiresAuth: true } },
        { path: 'review', name: 'Review', component: () => import('../views/Review.vue'), meta: { requiresAuth: true } },
        { path: 'contracts/:id', name: 'Workbench', component: () => import('../views/Workbench.vue'), meta: { requiresAuth: true } },
        { path: 'contracts/:id/report', name: 'Report', component: () => import('../views/Report.vue'), meta: { requiresAuth: true } },
        { path: 'admin', name: 'Admin', component: () => import('../views/Admin.vue'), meta: { requiresAuth: true, role: 'admin' } },
      ],
    },
    { path: '/login', name: 'Login', component: () => import('../views/Login.vue') },
  ],
})

router.beforeEach((to, _from, next) => {
  const token = localStorage.getItem('token')
  if (to.meta.requiresAuth && !token) {
    next('/login')
  } else if (to.path === '/login' && token) {
    next('/')
  } else {
    next()
  }
})

export default router
