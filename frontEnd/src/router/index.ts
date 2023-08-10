import { createRouter, createWebHashHistory, RouteRecordRaw } from 'vue-router';
import { usePermissStore } from '../store/permiss';
import Home from '../views/base/home.vue';

const routes: RouteRecordRaw[] = [
    {
        path: '/',
        redirect: '/dashboard',
    },
    {
        path: '/',
        name: 'Home',
        component: Home,
        children: [
            {
                path: '/dashboard',
                name: 'dashboard',
                meta: {
                    title: '系统首页',
                    permiss: '1',
                },
                component: () => import(/* webpackChunkName: "dashboard" */ '../views/dashboard.vue'),
            },
            {
                path: '/worker_logs',
                name: 'worker_logs',
                meta: {
                    title: '任务日志',
                    permiss: '14',
                },
                component: () => import(/* webpackChunkName: "worker_logs" */ '../views/projects_views/worker_logs.vue'),
            },
            {
                path: '/api_docs',
                name: 'api_docs',
                meta: {
                    title: 'ResfulAPI响应文档',
                    permiss: '2',
                },
                component: () => import(/* webpackChunkName: "api_docs" */ '../views/api_docs.vue'),
            },
            {
                path: '/users',
                name: 'users_manage',
                meta: {
                    title: '账号管理',
                    permiss: '2',
                },
                component: () => import(/* webpackChunkName: "users_manage" */ '../views/users/users_manage.vue'),
            },
            {
                path: '/projects_list',
                name: 'projects_list',
                meta: {
                    title: '项目列表',
                    permiss: '42',
                },
                component: () => import(/* webpackChunkName: "projects_list" */ '../views/projects_views/projects_list.vue'),
            },
            {
                path: '/projects_tabs',
                name: 'projects_tabs',
                meta: {
                    title: '项目详细',
                    permiss: '42',
                },
                component: () => import(/* webpackChunkName: "projects_tabs" */ '../views/projects_views/projects_tabs.vue'),
            },
            {
                path: '/logging_detail',
                name: 'logging_detail',
                meta: {
                    title: '日志详情',
                    permiss: '42',
                },
                component: () => import(/* webpackChunkName: "logging_detail" */ '../views/projects_views/logging_detail.vue'),
            },
            {
                path: '/jobObjs',
                name: 'jobObjs',
                meta: {
                    title: '任务总表',
                    permiss: '42',
                },
                component: () => import(/* webpackChunkName: "jobObjs" */ '../views/projects_views/jobObjs.vue'),
            },
            {
                path: '/alarm_setting',
                name: 'alarm_setting',
                meta: {
                    title: '告警设置',
                    permiss: '5',
                },
                component: () => import(/* webpackChunkName: "alarm_setting" */ '../views/alarm_views/alarm_setting.vue'),
            },
            {
                path: '/alarm_jobs',
                name: 'alarm_jobs',
                meta: {
                    title: '任务监控',
                    permiss: '5',
                },
                component: () => import(/* webpackChunkName: "alarm_setting" */ '../views/alarm_views/alarm_jobs.vue'),
            },
            {
                path: '/program_list',
                name: 'program_list',
                meta: {
                    title: '程序列表',
                    permiss: '2',
                },
                component: () => import(/* webpackChunkName: "table" */ '../views/program_views/program_list.vue'),
            },
            {
                path: '/program_register',
                name: 'program_register',
                meta: {
                    title: '程序登记',
                    permiss: '2',
                },
                component: () => import(/* webpackChunkName: "table" */ '../views/program_views/program_register.vue'),
            },
            {
                path: '/readme',
                name: 'readme',
                meta: {
                    title: '说明文档',
                    permiss: '2',
                },
                component: () => import(/* webpackChunkName: "table" */ '../views/readme/readme.vue'),
            },

            // 原始模板
            {
                path: '/table',
                name: 'basetable',
                meta: {
                    title: '表格',
                    permiss: '2',
                },
                component: () => import(/* webpackChunkName: "table" */ '../views/table.vue'),
            },
            {
                path: '/redis_table',
                name: 'redis_table',
                meta: {
                    title: 'redis_demo表格',
                    permiss: '2',
                },
                component: () => import(/* webpackChunkName: "table" */ '../views/redis_table.vue'),
            },
            {
                path: '/echart',
                name: 'echart测试',
                meta: {
                    title: 'echart测试',
                    permiss: '2',
                },
                component: () => import(/* webpackChunkName: "table" */ '../views/disc_table.vue'),
            },
            {
                path: '/charts',
                name: 'basecharts',
                meta: {
                    title: '图表',
                    permiss: '11',
                },
                component: () => import(/* webpackChunkName: "charts" */ '../views/charts.vue'),
            },
            {
                path: '/form',
                name: 'baseform',
                meta: {
                    title: '表单',
                    permiss: '5',
                },
                component: () => import(/* webpackChunkName: "form" */ '../views/form.vue'),
            },
            {
                path: '/tabs',
                name: 'tabs',
                meta: {
                    title: 'tab标签',
                    permiss: '3',
                },
                component: () => import(/* webpackChunkName: "tabs" */ '../views/tabs.vue'),
            },
            {
                path: '/permission',
                name: 'permission',
                meta: {
                    title: '权限管理',
                    permiss: '13',
                },
                component: () => import(/* webpackChunkName: "permission" */ '../views/users/permission.vue'),
            },
            {
                path: '/upload',
                name: 'upload',
                meta: {
                    title: '上传插件',
                    permiss: '6',
                },
                component: () => import(/* webpackChunkName: "upload" */ '../views/upload.vue'),
            },
            {
                path: '/icon',
                name: 'icon',
                meta: {
                    title: '自定义图标',
                    permiss: '10',
                },
                component: () => import(/* webpackChunkName: "icon" */ '../views/icon.vue'),
            },
            {
                path: '/user',
                name: 'user',
                meta: {
                    title: '个人中心',
                },
                component: () => import(/* webpackChunkName: "user" */ '../views/users/user.vue'),
            },
            {
                path: '/editor',
                name: 'editor',
                meta: {
                    title: '富文本编辑器',
                    permiss: '8',
                },
                component: () => import(/* webpackChunkName: "editor" */ '../views/editor.vue'),
            },
            {
                path: '/markdown',
                name: 'markdown',
                meta: {
                    title: 'markdown编辑器',
                    permiss: '9',
                },
                component: () => import(/* webpackChunkName: "markdown" */ '../views/markdown.vue'),
            },
            {
                path: '/export',
                name: 'export',
                meta: {
                    title: '导出Excel',
                    permiss: '2',
                },
                component: () => import(/* webpackChunkName: "export" */ '../views/export.vue'),
            },
            {
                path: '/import',
                name: 'import',
                meta: {
                    title: '导入Excel',
                    permiss: '2',
                },
                component: () => import(/* webpackChunkName: "import" */ '../views/import.vue'),
            },
        ],
    },
    {
        path: '/login',
        name: 'Login',
        meta: {
            title: '登录',
        },
        component: () => import(/* webpackChunkName: "login" */ '../views/base/login.vue'),
    },
    {
        path: '/403',
        name: '403',
        meta: {
            title: '没有权限',
        },
        component: () => import(/* webpackChunkName: "403" */ '../views/403.vue'),
    },
];

const router = createRouter({
    history: createWebHashHistory(),
    routes,
});

router.beforeEach((to, from, next) => {
    document.title = `${to.meta.title} | crawlRaXi`;
    // console.log('to',to)
    const role = localStorage.getItem('ms_username');
    const permiss = usePermissStore();
    if (!role && to.path !== '/login') {
        next('/login');
    } else if (!!to.meta.permiss && !permiss.key.includes(to.meta.permiss as string)) {
        // 如果没有权限，则进入403
        next('/403');
    } else {
        next();
    }
});

export default router;
