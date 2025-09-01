import axios from "axios";

export default () => {
    const api = axios.create({
        baseURL: "http://localhost:8000/api/v1",
        timeout: 10000,
    });
    api.interceptors.request.use(
        (config) => {
            const token = localStorage.getItem('accessToken');
            if (token) {
                config.headers['Authorization'] = `Bearer ${token}`;
            }
            return config;
        },
        (error) => {
            return Promise.reject(error);
        }
    );
    api.interceptors.response.use(
        (response) => {
            return response;
        },
        async (error) => {
            const originalRequest = error.config;
            if (error.response.status === 401 && !originalRequest._retry) {
                // 处理 401 错误，例如刷新 token
                originalRequest._retry = true;
                try {
                    const refreshToken = localStorage.getItem('refreshToken');
                    const res = await authService.refreshToken(refreshToken);
                    // 刷新成功，更新 token 并重新发送请求
                    localStorage.setItem('accessToken', res.access_token);
                    originalRequest.headers['Authorization'] = `Bearer ${res.access_token}`;
                    localStorage.setItem('refreshToken', res.refresh_token);
                    return api(originalRequest);
                } catch (refreshError) {
                    localStorage.removeItem('accessToken');
                    localStorage.removeItem('refreshToken');
                    localStorage.removeItem('user');
                    // 跳转到登录页
                    window.location.href = '/login';
                    return Promise.reject(refreshError);
                }
            }
            return Promise.reject(error);
        }
    );
    return api;
}