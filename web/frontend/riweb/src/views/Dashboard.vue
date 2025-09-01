<template>
  <div>
    <el-card>
      <template #header>ABCD</template>
      ABCD
    </el-card>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import { ElCard } from 'element-plus'
import 'element-plus/dist/index.css'
import layouts from '@/layouts'

const route = useRoute()
const currentLayout = computed(() => {
  return layouts[route.meta.layout || 'TenantLayout']
})
</script>