const routes = [
  {
    path: '/',
    component: () => import('layouts/MainLayout.vue'),
    children: [
      { path: '', component: () => import('pages/Login.vue')},
      { path: 'register', component: () => import('pages/Register.vue') },
      { path: 'home', component: () => import('pages/Home.vue') },
      { path: 'profile', component: () => import('pages/Profile.vue') },
      { path: 'camera', component: () => import('pages/Camera.vue') },
      { path: 'camera_detail/:id', component: () => import('pages/CameraDetail.vue'), props: true },
      { path: 'case', component: () => import('pages/Case.vue') },
      { path: 'case_detail/:id', component: () => import('pages/CaseDetail.vue'), props: true },
      { path: 'analytics', component: () => import('pages/Analytics.vue') },
      { path: 'admin_analytics', component: () => import('pages/AdminAnalytics.vue') },
      { path: 'admin_home', component: () => import('pages/AdminHome.vue') },
      { path: 'admin_profile', component: () => import('pages/AdminProfile.vue') },
      { path: 'admin_user_analytics/:id', component: () => import('pages/AdminUserAnalytics.vue') },
    ]
  },
  // Always leave this as last one,
  // but you can also remove it
  {
    path: '/:catchAll(.*)*',
    component: () => import('pages/Error404.vue')
  }
]

export default routes
