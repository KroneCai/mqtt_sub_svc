<template>
  <el-row class="tac">
    <el-col>
      <el-menu
        :router="true"
        default-active="1-1"
        text-color="#333399"
        active-text-color="#ff0000"
        class="el-menu-vertical-demo"
        @open="handleOpen"
        @close="handleClose"
      >
        <el-sub-menu index="1">
          <template #title>
            <el-icon><Cpu /></el-icon>
            <span>IoT Device Mgmt</span>
          </template>
          <el-menu-item index="1-1" :route="{path:'/devices/deployed'}">Deployed Devices</el-menu-item>
          <el-menu-item index="1-2" :route="{path:'/devices/undeployed'}">Undeployed Devices</el-menu-item>
        </el-sub-menu>
        <el-menu-item index="2">
          <el-icon><CreditCard /></el-icon>
          <span>Tenant Mgmt</span>
        </el-menu-item>
        <el-menu-item index="3">
          <el-icon><OfficeBuilding /></el-icon>
          <span>Platform Mgmt</span>
        </el-menu-item>
        <el-sub-menu index="4">
            <template #title>
                <el-icon><setting /></el-icon>
                <span>Settings</span>
            </template>
          <el-menu-item index="4-1">Organizatio Info</el-menu-item>
          <el-menu-item index="4-2">System Config</el-menu-item>
        </el-sub-menu>
      </el-menu>
    </el-col>
  </el-row>
</template>

<style scoped>
.el-menu-item,.el-sub-menu__title, .el-sub-menu__title span{
    font-size: 12px;
    margin:0 0 0 0;
    padding:0 0 0 0;
    height: 30px;
    line-height:30px;
}
</style>

<script lang="ts" setup>
import {
  Cpu,
  OfficeBuilding,
  CreditCard,
  Setting,
} from '@element-plus/icons-vue'

const handleOpen = (key: string, keyPath: string[]) => {
  console.log(key, keyPath)
}
const handleClose = (key: string, keyPath: string[]) => {
  console.log(key, keyPath)
}
</script>