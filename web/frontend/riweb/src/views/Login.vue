<script setup>
import { useAuthStore } from '@/stores/auth.store.js'
import { reactive } from 'vue'
import LoginBox from '@/components/LoginBox.vue'
const AuthStore = useAuthStore()

const user_data = reactive({
  email: 'eve.holt@reqres.in',
  pwd: 'cityslicka'
})
</script>

<template>
  <div class="container v-center box-border">
    <el-row class="row-box box-border">
      <el-col :span="10" class="box-border">
        <LoginBox></LoginBox>
      </el-col>
      <el-col :span="14" class="box-border">
        <img src="/images/ri-vant.png" alt="RENTOKIL INITIAL" class="img-box">
      </el-col>
    </el-row>
  </div>
</template>

<style lang="scss" scoped>

.box-border{
  border: 0px solid #ccc;
  display: flex;
  align-items: flex-end;  /* 垂直居中 */
  justify-content: center;  /* 水平居中（可选） */
}
.container {
  display: flex;
  min-height: 100vh;
  align-items: center;  /* 垂直居中 */
  justify-content: center;  /* 水平居中（可选） */
}
.row-box{
  width: 100%;
  height: 350px;
}
.img-box{
  //border-left: 1px solid #ccc;
  width: 510px;
  height: 300px;      /* 显示区域的高度 */
  object-fit: cover;  /* 填充整个容器，裁剪多余部分 */
  object-position: center; /* 居中裁剪（可选：top, left, right, bottom） */
  filter: 
    opacity(1)      /* 80% 透明度 */
    saturate(1.2)     /* 150% 饱和度 */
    brightness(1);  /* 80% 亮度 */
    transform: scaleX(1);
}

@media (min-width: 1024px) {
  .container {
    min-width: 1024px;
  }
}

</style>
