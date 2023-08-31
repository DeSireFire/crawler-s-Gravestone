<template>
  <div class="sidebar">
    <el-menu
        class="sidebar-el-menu"
        :default-active="onRoutes"
        :collapse="sidebar.collapse"
        background-color="#324157"
        text-color="#bfcbd9"
        active-text-color="#20a0ff"
        unique-opened
        router
    >
      <template v-for="item in items">
        <template v-if="item.subs">
          <el-sub-menu :index="item.index" :key="item.index" v-permiss="item.permiss">
            <template #title>
              <el-icon>
                <component :is="item.icon"></component>
              </el-icon>
              <span>{{ item.title }}</span>
            </template>
            <template v-for="subItem in item.subs">
              <el-sub-menu
                  v-if="subItem.subs"
                  :index="subItem.index"
                  :key="subItem.index"
                  v-permiss="item.permiss"
              >
                <template #title>{{ subItem.title }}</template>
                <el-menu-item v-for="(threeItem, i) in subItem.subs" :key="i" :index="threeItem.index">
                  {{ threeItem.title }}
                </el-menu-item>
              </el-sub-menu>
              <el-menu-item v-else :index="subItem.index" v-permiss="item.permiss">
                {{ subItem.title }}
              </el-menu-item>
            </template>
          </el-sub-menu>
        </template>
        <template v-else>
          <el-menu-item :index="item.index" :key="item.index" v-permiss="item.permiss">
            <el-icon>
              <component :is="item.icon"></component>
            </el-icon>
            <template #title>{{ item.title }}</template>
          </el-menu-item>
        </template>
      </template>
    </el-menu>
  </div>
</template>

<script setup lang="ts">
import {computed} from 'vue';
import {useSidebarStore} from '../store/sidebar';
import {useRoute} from 'vue-router';
import {Delete, Edit, Search, Plus, List} from '@element-plus/icons-vue';

const items = [
  {
    icon: 'Odometer',
    index: '/dashboard',
    title: '系统首页',
    permiss: '1',
  },
  {
    icon: 'User',
    index: '2',
    title: '用户管理',
    permiss: '2',
    subs: [
      {
        index: '/permission',
        title: '权限管理',
        permiss: '21',
      },
      {
        index: '/users',
        title: '账号管理',
        permiss: '22',
      },
    ],
  },
  {
    icon: 'Grid',
    index: '6',
    title: '程序管理',
    permiss: '6',
    subs: [
      {
        index: '/program_register',
        title: '程序登记',
        permiss: '61',
      },
      // {
      //   index: '/program_list',
      //   title: '程序列表',
      //   permiss: '62',
      // },
    ],
  },
  {
    icon: 'List',
    index: '4',
    title: '项目管理',
    permiss: '4',
    subs: [
      {
        index: '/projects_list',
        title: '项目列表',
        permiss: '41',
      },
      {
        index: '/jobObjs',
        title: '任务总表',
        permiss: '42',
      },
      {
        index: '/worker_logs',
        title: '日志管理',
        permiss: '43',
      },
    ],
  },
  {
    icon: 'Bell',
    index: '5',
    title: '告警管理',
    permiss: '5',
    subs: [
      {
        index: '/alarm_setting',
        title: '告警器设置',
        permiss: '51',

      },
      {
        index: '/alarm_jobs',
        title: '任务告警',
        permiss: '52',

      },
    ],
  },
  // {
  //   icon: 'Collection',
  //   index: '9',
  //   title: '帮助',
  //   permiss: '9',
  //   subs: [
  //     {
  //       index: '/readme',
  //       title: '使用文档',
  //       permiss: '91',
  //
  //     },
  //     {
  //       index: '/version',
  //       title: '版本历史',
  //       permiss: '92',
  //
  //     },
  //     {
  //       index: '/about',
  //       title: '关于',
  //       permiss: '93',
  //
  //     },
  //   ],
  // },
  {
    icon: 'Collection',
    index: '/readme',
    title: '使用文档',
    permiss: '9',
  },
  // {
  //   icon: 'User',
  //   index: '/user',
  //   title: '个人中心',
  //   permiss: '9',
  // },

  // {
  //   icon: 'Switch',
  //   index: '/api_docs',
  //   title: 'ResfulAPI响应文档',
  //   permiss: '2',
  // },

  // {
  //     icon: 'Calendar',
  //     index: '1',
  //     title: '表格相关',
  //     permiss: '2',
  //     subs: [
  //         {
  //             index: '/table',
  //             title: '常用表格',
  //             permiss: '2',
  //         },
  //         {
  //             index: '/import',
  //             title: '导入Excel',
  //             permiss: '2',
  //         },
  //         {
  //             index: '/export',
  //             title: '导出Excel',
  //             permiss: '2',
  //         },
  //     ],
  // },
  // {
  //     icon: 'DocumentCopy',
  //     index: '/tabs',
  //     title: 'tab选项卡',
  //     permiss: '3',
  // },
  // {
  //     icon: 'Edit',
  //     index: '3',
  //     title: '表单相关',
  //     permiss: '4',
  //     subs: [
  //         {
  //             index: '/form',
  //             title: '基本表单',
  //             permiss: '5',
  //         },
  //         {
  //             index: '/upload',
  //             title: '文件上传',
  //             permiss: '6',
  //         },
  //         {
  //             index: '4',
  //             title: '三级菜单',
  //             permiss: '7',
  //             subs: [
  //                 {
  //                     index: '/editor',
  //                     title: '富文本编辑器',
  //                     permiss: '8',
  //                 },
  //                 {
  //                     index: '/markdown',
  //                     title: 'markdown编辑器',
  //                     permiss: '9',
  //                 },
  //             ],
  //         },
  //     ],
  // },
  // {
  //     icon: 'Setting',
  //     index: '/icon',
  //     title: '自定义图标',
  //     permiss: '10',
  // },
  // {
  //     icon: 'PieChart',
  //     index: '/charts',
  //     title: 'schart图表',
  //     permiss: '11',
  // },

];

const route = useRoute();
const onRoutes = computed(() => {
  return route.path;
});

const sidebar = useSidebarStore();
</script>

<style scoped>
.sidebar {
  display: block;
  position: absolute;
  left: 0;
  top: 70px;
  bottom: 0;
  overflow-y: scroll;
}

.sidebar::-webkit-scrollbar {
  width: 0;
}

.sidebar-el-menu:not(.el-menu--collapse) {
  width: 250px;
}

.sidebar > ul {
  height: 100%;
}
</style>
