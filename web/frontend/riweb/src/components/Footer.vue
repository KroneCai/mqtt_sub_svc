<script setup></script>

<template>
  <div class="footer">
    <h3>Copyright © 2023 <a href="">RiWeb</a></h3>
  </div>
</template>

<style lang="scss" scoped>
@import '@/assets/main.scss';
.footer {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 10px;

  a {
    text-decoration: none;
    color: $secondary-color;

    &:hover {
      color: $primary-color;
    }
  }
}
</style>