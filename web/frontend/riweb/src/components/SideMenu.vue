<template>
  <el-row class="tac">
    <el-col>
      <el-menu
        :router="true"
        :default-openeds="openeds"
        text-color="#333399"
        active-text-color="#ff0000"
        class="el-menu-vertical-demo"
      >
        <div v-if="portalStore.mainMenuIndex === 'M1'">
          <el-menu-item index="M1-S1" :route="{path:'/dashboard/home'}">
            <el-icon><Cpu /></el-icon>
            <span>综合监控</span>
          </el-menu-item>
          <el-sub-menu index="M1-S2">
            <template #title>
              <el-icon><Document /></el-icon>
              <span class="sub-menu-title">鼠情监控</span>
            </template>
            <el-menu-item index="M1-S2-1" :route="{path:'/dashboard/mouse/rt-report'}">实时监控台</el-menu-item>
            <el-menu-item index="M1-S2-2" :route="{path:'/dashboard/mouse/st-report'}">统计分析</el-menu-item>
          </el-sub-menu>
          <el-menu-item index="M1-S3">
            <el-icon><CreditCard /></el-icon>
            <span>设备监控</span>
          </el-menu-item>
        </div>
        <div v-if="portalStore.mainMenuIndex === 'M2'">
          <el-sub-menu index="M2-S1">
            <template #title>
              <el-icon><Cpu /></el-icon>
              <span class="sub-menu-title">服务请求</span>
            </template>
            <el-menu-item index="M2-S1-1" :route="{path:'/service/sr/list'}">查看服务请求</el-menu-item>
            <el-menu-item index="M2-S1-1" :route="{path:'/service/sr/sr-report'}">服务请求报告</el-menu-item>
          </el-sub-menu>
          <el-sub-menu index="M2-S2">
            <template #title>
              <el-icon><Document /></el-icon>
              <span class="sub-menu-title">报修</span>
            </template>
            <el-menu-item index="M2-S2-1" :route="{path:'/service/rr/list'}">实时监控台</el-menu-item>
            <el-menu-item index="M2-S2-2" :route="{path:'/service/rr/rr-report'}">维修服务报告</el-menu-item>
          </el-sub-menu>
        </div>
        <div v-if="portalStore.mainMenuIndex === 'M3'">
          <el-menu-item index="M3-S1">
            <el-icon><OfficeBuilding /></el-icon>
            <span>企业信息管理</span>
          </el-menu-item>
          <el-sub-menu index="M3-S2">
            <template #title>
              <el-icon><User /></el-icon>
              <span class="sub-menu-title">用户及授权管理</span>
            </template>
            <el-menu-item index="M3-S2-1" :route="{path:'/service/sr/list'}">用户管理</el-menu-item>
            <el-menu-item index="M3-S2-1" :route="{path:'/service/sr/sr-report'}">用户权限管理</el-menu-item>
          </el-sub-menu>
          <el-sub-menu index="M3-S3">
            <template #title>
              <el-icon><Document /></el-icon>
              <span class="sub-menu-title">设备管理</span>
            </template>
            <el-menu-item index="M3-S3-1" :route="{path:'/service/rr/list'}">设备管理</el-menu-item>
            <el-menu-item index="M3-S3-2" :route="{path:'/service/rr/rr-report'}">查看设备日志</el-menu-item>
          </el-sub-menu>
          <el-menu-item index="M3-S4">
            <el-icon><OfficeBuilding /></el-icon>
            <span>场地设施管理</span>
          </el-menu-item>
          <el-sub-menu index="M3-S5">
            <template #title>
              <el-icon><Document /></el-icon>
              <span class="sub-menu-title">审计日志</span>
            </template>
            <el-menu-item index="M3-S5-1" :route="{path:'/service/rr/list'}">查看审计日志</el-menu-item>
          </el-sub-menu>
        </div>
      </el-menu>
    </el-col>
  </el-row>
</template>

<style scoped>
.el-menu{
  border:none;
}
.el-menu-item{
  font-size: 13px;
  margin:3px 0;
  height: 32px;
  line-height: 32px;
}
.el-sub-menu, .sub-menu-title{
  font-size: 13px;
  margin:5px 0;
  --el-menu-item-height: 38px;
}
</style>

<script setup>
import {ref} from 'vue'
import { usePortalStore } from '@/stores/portal.store'
import {
  Cpu,
  OfficeBuilding,
  User,
  CreditCard,
  Setting,
  Document,
} from '@element-plus/icons-vue'

// states
const portalStore = usePortalStore()
const openeds = ref(['M1-S2','M2-S1','M2-S2','M3-S2','M3-S3','M3-S5'])

// actions

const handleOpen = (key, keyPath) => {
  console.log(key, keyPath)
}
const handleClose = (key, keyPath) => {
  console.log(key, keyPath)
}
</script>