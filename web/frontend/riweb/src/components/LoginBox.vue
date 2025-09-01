<template>
  <div class="login-container">
    <el-card class="login-card">
      <div class="login-header">
        <h2>欢迎登录能多洁Pest Connect平台</h2>
      </div>
      
      <el-form 
        ref="loginForm" 
        :model="form" 
        :rules="rules" 
        class="login-form"
        @keyup.enter="handleLogin"
      >
        <!-- 用户名 -->
        <el-form-item prop="userid">
          <el-input
            v-model="form.userid"
            placeholder="请输入用户帐号"
            :prefix-icon="User"
            size="small"
          />
        </el-form-item>
        
        <!-- 密码 -->
        <el-form-item prop="password">
          <el-input
            v-model="form.password"
            type="password"
            size="small"
            placeholder="请输入密码"
            :prefix-icon="Lock"
            show-password
          />
        </el-form-item>

        <!-- 租户代码 -->
        <el-form-item prop="tenantCode">
          <el-input
            v-model="form.tenantCode"
            placeholder="请输入租户代码"
            :prefix-icon="OfficeBuilding"
            size="small"
          />
        </el-form-item>
        
        
        <!-- 记住我和忘记密码 -->
        <el-form-item class="login-options">
            <el-row :gutter="20" style="width:100%;">
                <el-col :span="12">
                    <el-checkbox v-model="rememberMe" size="small" checked >记住我</el-checkbox>
                </el-col>
                <el-col :span="12">
                    <el-button type="text" @click="handleForgetPassword" size="small">忘记密码?</el-button>
                </el-col>
            </el-row>
        </el-form-item>
        
        <!-- 登录按钮 -->
        <el-form-item>
          <el-button
            type="primary"
            class="login-btn"
            :loading="loading"
            @click="handleLogin"
          >
            登录
          </el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth.store'
import { OfficeBuilding, User, Lock } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'

const router = useRouter()
const authStore = useAuthStore()

const form = ref({
  tenantCode: '',
  userid: '',
  password: ''
})

const rememberMe = ref(authStore.rememberMe)
const loading = computed(() => authStore.loading)

const rules = {
  tenantCode: [
    { required: true, message: '请输入租户代码', trigger: 'blur' }
  ],
  userid: [
    { required: true, message: '请输入用户帐号', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 8, max: 20, message: '长度在 8 到 20 个字符', trigger: 'blur' },
    //必须包含至少1个大写字母、1个小写字母、1个数字和1个特殊字符
    // { pattern: /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*()_+\-=\[\]{}|;:'",.<>/?]).{8,20}$/,  message: '密码复杂度不匹配', trigger: 'blur' },
    //不能包含空格
    // { pattern: /^\S+$/, message: '不能包含空格', trigger: 'blur' }
  ]
}

const handleLogin = async () => {
  try {
    //console.log('登录请求数据:', form.value)
    authStore.rememberMe = rememberMe.value
    await authStore.login(form.value.userid, form.value.password, form.value.tenantCode)
    ElMessage.success('登录成功')
    router.push('/')
  } catch (error) {
    console.error('登录失败:', error)
    ElMessage.error(error.message || '登录失败')
  }
}

const handleForgetPassword = () => {
  ElMessage.info('请联系管理员重置密码')
  // router.push('/forget-password')
}
</script>

<style lang="scss" scoped>
@use '@/assets/styles/main.scss' as main;

.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
}

.login-card {
  width: 100%;
  border-radius: 8px;
  box-shadow: 0px 5px 16px 0 rgba(0, 0, 0, 0.2);
  margin:0px 10px;
  padding:0px 0px;
}

.login-header {
  text-align: center;
  margin-bottom: 10px;
}

.login-header h2 {
  color: main.$secondary-color;
  font-size: 14px;
}

.login-form {
  padding: 0 10px;
}

.login-options {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.login-btn {
  width: 100%;
  margin-top: 5px;
  background-color: main.$secondary-color;
}
</style>