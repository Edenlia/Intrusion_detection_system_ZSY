
const routes = [
  {
    path: '/',
    component: () => import('layouts/MainLayout.vue'),
    children: [
      { path: '', component: () => import('pages/Login.vue') },
      { path: 'register', component: () => import('pages/Register.vue') },
      { path: 'home', component: () => import('pages/Home.vue') },
      { path: 'profile', component: () => import('pages/Profile.vue') },
      { path: 'camera', component: () => import('pages/Camera.vue') },
      { path: 'camera_detail', component: () => import('pages/CameraDetail.vue') },
      { path: 'case', component: () => import('pages/Case.vue') },
      { path: 'case_detail', component: () => import('pages/CaseDetail.vue') },
      { path: 'analytics', component: () => import('pages/Analytics.vue') },
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
