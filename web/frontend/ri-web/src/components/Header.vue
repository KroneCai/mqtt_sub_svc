<template>
    <el-menu
    :default-active="activeIndex"
    :router="true"
    class="el-menu-demo"
    mode="horizontal"
    :ellipsis="false"
    @select="handleSelect"
  >
    <el-menu-item index="0">
      <img
        style="width: 100px"
        src="/images/RI_logo.png"
        alt="Element logo"
      />
    </el-menu-item>
    <el-menu-item index="1" :route="{path:'/console'}">Console</el-menu-item>
    <el-sub-menu index="2">
      <template #title>Account</template>
      <el-menu-item index="2-1">My Profile</el-menu-item>
      <el-menu-item index="2-2">Change Password</el-menu-item>
      <el-divider />
      <el-menu-item index="2-3">Sign Out</el-menu-item>
    </el-sub-menu>
  </el-menu>
</template>
<script lang="ts" setup>
import { ref } from 'vue'

const activeIndex = ref('1')
const handleSelect = (key: string, keyPath: string[]) => {
  console.log(key, keyPath)
}
</script>

<style scoped>
.el-menu--horizontal > .el-menu-item:nth-child(1) {
  margin-right: auto;
}
</style>