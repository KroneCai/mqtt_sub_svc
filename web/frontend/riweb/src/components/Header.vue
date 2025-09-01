<template>
  <el-row class="header">
    <el-col :span="4">
      <el-row justify="start">
        <router-link to="/">
      <img
        style="padding: 0 0 0.5rem 1rem; height:45px"
        src="/images/RI_logo.png"
        alt="Element logo"
      /></router-link>
      </el-row>
    </el-col>
    <el-col :span="20" >
      <el-row class="menu-box" justify="end">
       <el-menu
        :default-active="activeIndex"
        :router="false"
        mode="horizontal"
        :ellipsis="false"
        @select="handleSelect"
      >
        <el-menu-item index="M1" :route="{path:'/dashboard'}">数据仪表盘</el-menu-item>
        <el-menu-item index="M2" :route="{path:'/service'}">专业服务</el-menu-item>
        <el-menu-item index="M3" :route="{path:'/management'}">系统管理</el-menu-item>
        <el-sub-menu index="M4">
          <template #title>账户管理</template>
          <el-menu-item index="M4-1">{{user.user_name}}的个人信息</el-menu-item>
          <el-menu-item index="M4-2">重设密码</el-menu-item>
          <el-divider style="margin:8px 0;"/>
          <el-menu-item index="M4-3" @click="handleLogout">安全退出</el-menu-item>
        </el-sub-menu>
      </el-menu>
      </el-row>
    </el-col>
  </el-row>
   
  <el-drawer v-model="dlgUserInfoVisible" direction="rtl">
    <template #header>
      <h4>{{ user.user_name }}的个人信息</h4>
    </template>
    <template #default>
      <div>
        <el-form label-width="auto" style="max-width:280px">
          <el-form-item label="公司代码：">
            <el-text>{{ user.tenant_code }}</el-text>
          </el-form-item>
          <el-form-item label="用户ID：">
            <el-text>{{ user.user_id }}</el-text>
          </el-form-item>
          <el-form-item label="用户名称：">
            <el-text>{{ user.user_name }}</el-text>
          </el-form-item>
          <el-form-item label="电子邮箱：">
            <el-text>{{ user.user_email }}</el-text>
          </el-form-item>
          <el-form-item label="用户角色：">
            <el-text v-for="(role,index) in user.user_roles">
              {{ role }}<span v-if="index < user.user_roles.length-1">, &nbsp;</span>
            </el-text>
          </el-form-item>
        </el-form>
      </div>
    </template>
    <template #footer>
      <div style="flex: auto">
        <el-button type="primary" @click="handleConfirm">关闭窗口</el-button>
      </div>
    </template>
  </el-drawer>
</template>

<script setup>
import { ref,computed } from 'vue'
import router from '@/router'
import {useRoute} from 'vue-router'
import { useAuthStore } from '@/stores/auth.store.js'
import { usePortalStore } from '@/stores/portal.store'
import { ElMessage, ElMessageBox } from 'element-plus'

// state
const route = useRoute()
const authStore = useAuthStore()
const portalStore = usePortalStore()
const dlgUserInfoVisible = ref(false)
const user = authStore.user

// getter
const activeIndex = computed(()=>{
  portalStore.mainMenuIndex = 'M1'
  return route.meta.menuIndex || 'M1'
})

// action
const handleSelect = (key, keyPath) => {
  if(key != 'M0' && key.length<=2) {
    portalStore.mainMenuIndex = key
  }
  switch(key){
    case "M0":
      portalStore.mainMenuIndex = 'M1'
      window.location.href = '/'
      break
    case "M4-1":
      dlgUserInfoVisible.value = true
      break
    default:
      console.log('key',key)
      console.log('portal store menuIndex:', portalStore.mainMenuIndex)
      
  }
}
const handleConfirm = ()=>{
  dlgUserInfoVisible.value = false
  /*
  ElMessageBox.confirm('Do you confirm to close?')
    .then(() => {
      dlgUserInfoVisible.value = false
    })
    .catch(() => {
      // catch error
    })
  */
}
const handleLogout = () => {
  authStore.clearAuth()
  ElMessage.success('Sign out success')
  window.location.href = '/login'
}
</script>

<style language="scss" scoped>
.header{
  border-bottom:2px solid #eeeeee
}
.el-text{
  color:#999999;
}

.menu-box{
  display: flex;
  justify-content: flex-end; /* 水平靠右 */
  align-items: flex-end;    /* 垂直靠底 */
  height:100%;
}

.el-menu--horizontal{
  height: 35px !important;
  border-bottom: none;
}

.menu-divider {
  height: 1px;
  padding: 0;
  margin:0;
  overflow: hidden;
  cursor: default;
}

.el-menu-item {
  margin: 0px 0;
}

h4{
 padding: 0 0px;
 margin: 0 0;
}
</style>