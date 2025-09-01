// src/stores/auth.store.js
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import authService from '@/services/auth.service'

export const useAuthStore = defineStore('auth', () => {
  //state
  const accessToken = ref(localStorage.getItem('accessToken') || '')
  const refreshToken = ref(localStorage.getItem('refreshToken') || '')
  const user = ref(JSON.parse(localStorage.getItem('user')) || {})
  const rememberMe = ref(localStorage.getItem('rememberMe') === true)
  const loading = ref(false)

  //getters
  const isAuthenticated = computed(() => !!accessToken.value)

  //actions
  const login = async (uid, pwd, tcode) => {
    loading.value = true
    try {
      const res = await authService.login(uid, pwd, tcode)
      //res = JSON.parse(res)
      //console.log(res)
      accessToken.value = res.access_token
      refreshToken.value = res.refresh_token

      user.value = {
        user_id: res.user.user_id,
        user_name: res.user.user_name,
        user_email: res.user.user_email,
        user_roles: res.user.user_roles,
        tenant_code: res.user.tenant_code
      }
      
      if (rememberMe.value) {
        localStorage.setItem('accessToken', accessToken.value)
        localStorage.setItem('refreshToken', refreshToken.value)
        localStorage.setItem('user', JSON.stringify(user.value))
        localStorage.setItem('rememberMe', true)
      } else {
        sessionStorage.setItem('accessToken', accessToken.value)
        sessionStorage.setItem('refreshToken', refreshToken.value)
        sessionStorage.setItem('user', JSON.stringify(user.value))
        sessionStorage.setItem('rememberMe', false)
      }

      return true
    } catch (error) {
      console.error('登录失败:', error)
      throw error
    } finally {
      loading.value = false
    }
  }

  const setTokens = (access_token, refresh_token) => {
    accessToken.value = access_token;
    refreshToken.value = refresh_token;
    localStorage.setItem('accessToken', access_token);
    localStorage.setItem('refreshToken', refresh_token);
  };

  const clearAuth = () => {
    accessToken.value = '';
    refreshToken.value = '';
    user.value = {};
    localStorage.removeItem('accessToken');
    localStorage.removeItem('refreshToken');
    localStorage.removeItem('user');
    sessionStorage.removeItem('accessToken');
    sessionStorage.removeItem('refreshToken');
    sessionStorage.removeItem('user');
  };

  const refreshAccessToken = async () => {
    try {
      if (!refreshToken.value) {
        throw new Error('No refresh token available');
      }

      const res = await authService.refreshTokens(refreshToken.value);
      setTokens(res.access_token, res.refresh_token);
      
      return accessToken.value;
    } catch (error) {
      clearAuth();
      throw new Error('Token刷新失败: ' + error.message);
    }
  };

  const verifyToken = async () => {
    try{
      const res = await authService.verifyToken();
      return res
    }
    catch(err){
      throw new Error('Token验证失败: ' + err.message);
    }
  }

  return {
    accessToken,
    refreshToken,
    user,
    rememberMe,
    loading,
    isAuthenticated,
    login,
    clearAuth,
    setTokens,
    refreshAccessToken,
    verifyToken
  }
})