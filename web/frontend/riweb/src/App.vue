<template>
  <component :is="currentLayout">
    <router-view />
  </component>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import layouts from '@/layouts'

const route = useRoute()
const currentLayout = computed(() => {
  return layouts[route.meta.layout || 'TenantLayout']
})
</script>