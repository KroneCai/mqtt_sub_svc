import { defineAsyncComponent } from 'vue'

// 定义不同布局模板
export default {
  TenantLayout: defineAsyncComponent(() => import('./TenantLayout.vue')),
  PlatformLayout: defineAsyncComponent(() => import('./PlatformLayout.vue'))
}