<template>
  <!-- 星梦智能助手 — 根组件 -->
  <div class="app-root">
    <!-- 路由视图，使用 fade 过渡动画 -->
    <router-view v-slot="{ Component, route }">
      <transition name="page" mode="out-in">
        <component :is="Component" :key="route.path" />
      </transition>
    </router-view>
  </div>
</template>

<script setup>
/**
 * App.vue — 根组件
 * 提供路由切换过渡动画，包裹所有子页面
 */
</script>

<style scoped>
/* 页面切换动画 */
.page-enter-active {
  animation: fadeIn 0.35s ease-out forwards;
}
.page-leave-active {
  animation: fadeIn 0.2s ease-in reverse forwards;
}

@keyframes fadeIn {
  0%   { opacity: 0; transform: translateY(12px); }
  100% { opacity: 1; transform: translateY(0); }
}
</style>
