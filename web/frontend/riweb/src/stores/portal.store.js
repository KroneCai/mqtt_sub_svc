// src/stores/auth.store.js
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const usePortalStore = defineStore('portal', () => {
  //state
  const mainMenuIndex = ref('M1')
  const sideMenuIndex = ref('M1-S1')

  //getters

  //actions

  return {
    mainMenuIndex,
    sideMenuIndex,
  }
})