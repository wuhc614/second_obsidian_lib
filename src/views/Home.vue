<template>
  <!--
    首页 — 星梦智能助手入口
    展示主标题 + 两个功能入口按钮，全CSS科幻深蓝HUD风格
  -->
  <div class="home-page">
    <!-- 星空粒子背景（纯CSS实现） -->
    <div class="starfield" aria-hidden="true">
      <span
        v-for="i in 60"
        :key="i"
        class="star"
        :style="starStyle(i)"
      ></span>
    </div>

    <!-- 主内容区 -->
    <div class="home-content">
      <!-- 顶部装饰线 -->
      <div class="top-ornament" aria-hidden="true">
        <span class="ornament-line"></span>
        <span class="ornament-diamond">◆</span>
        <span class="ornament-line"></span>
      </div>

      <!-- 主标题 -->
      <h1 class="main-title">
        <span class="title-glow">星</span>
        <span class="title-glow delay-1">梦</span>
        <span class="title-glow delay-2">智</span>
        <span class="title-glow delay-3">能</span>
        <span class="title-glow delay-4">助</span>
        <span class="title-glow delay-5">手</span>
      </h1>

      <!-- 副标题 -->
      <p class="sub-title hud-title-line">
        探索星辰奥秘 · 解读梦境玄机
      </p>

      <!-- 功能入口卡片组 -->
      <div class="entry-cards">
        <!-- 星座星盘分析入口 -->
        <button class="entry-card hud-panel hud-panel-glow" @click="goStar">
          <!-- 卡片边角装饰 -->
          <span class="card-corner tl"></span>
          <span class="card-corner tr"></span>
          <span class="card-corner bl"></span>
          <span class="card-corner br"></span>

          <div class="card-icon star-icon">
            <!-- 纯CSS八角星 -->
            <span class="octagram"></span>
          </div>
          <h2 class="card-title">星座星盘分析</h2>
          <p class="card-desc">
            输入你的出生信息，获取专属星盘解读，洞察人生运势走向
          </p>
          <span class="card-action">
            进入测算
            <span class="arrow">→</span>
          </span>
        </button>

        <!-- 周公解梦入口 -->
        <button class="entry-card hud-panel hud-panel-glow" @click="goDream">
          <span class="card-corner tl"></span>
          <span class="card-corner tr"></span>
          <span class="card-corner bl"></span>
          <span class="card-corner br"></span>

          <div class="card-icon dream-icon">
            <!-- 纯CSS月亮 -->
            <span class="moon"></span>
          </div>
          <h2 class="card-title">周公解梦</h2>
          <p class="card-desc">
            描述你的梦境细节，AI智能解读潜意识深处的暗示与预兆
          </p>
          <span class="card-action">
            开始解梦
            <span class="arrow">→</span>
          </span>
        </button>
      </div>

      <!-- 底部状态条 -->
      <div class="status-bar" aria-hidden="true">
        <span class="status-dot"></span>
        <span class="status-text">SYSTEM ONLINE</span>
        <span class="status-code">v1.0.0</span>
      </div>
    </div>
  </div>
</template>

<script setup>
/**
 * Home.vue — 首页
 * 提供星座星盘分析和周公解梦两个功能入口
 */
import { useRouter } from 'vue-router'

const router = useRouter()

/** 跳转到星座星盘分析页 */
function goStar() {
  router.push('/star')
}

/** 跳转到周公解梦页 */
function goDream() {
  router.push('/dream')
}

/** 生成每颗星星的随机CSS样式 */
function starStyle(i) {
  const size = Math.random() * 3 + 1 // 1~4px
  const left = Math.random() * 100
  const top = Math.random() * 100
  const delay = Math.random() * 6
  const duration = 2 + Math.random() * 4
  // 三种闪烁动画随机选取
  const animNames = ['twinkle1', 'twinkle2', 'twinkle3']
  const animName = animNames[i % 3]
  // 随机颜色：蓝白/紫白
  const hue = Math.random() > 0.6 ? 200 : 260
  const color = `hsla(${hue}, 80%, ${70 + Math.random() * 20}%, ${0.3 + Math.random() * 0.5})`

  return {
    width: `${size}px`,
    height: `${size}px`,
    left: `${left}%`,
    top: `${top}%`,
    animationDelay: `${delay}s`,
    animationDuration: `${duration}s`,
    animationName: animName,
    backgroundColor: color,
    boxShadow: `0 0 ${size * 2}px ${color}`,
  }
}
</script>

<style scoped>
/* ============================================================
   首页样式
   ============================================================ */

.home-page {
  position: relative;
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
  background:
    /* 径向渐变模拟深空 */
    radial-gradient(ellipse at 30% 20%, rgba(0, 212, 255, 0.04) 0%, transparent 60%),
    radial-gradient(ellipse at 70% 80%, rgba(123, 97, 255, 0.03) 0%, transparent 60%),
    #0a0e1a;
}

/* ---- 星空粒子 ---- */
.starfield {
  position: absolute;
  inset: 0;
  pointer-events: none;
  z-index: 0;
}
.starfield .star {
  position: absolute;
  border-radius: 50%;
  animation-timing-function: ease-in-out;
  animation-iteration-count: infinite;
}

/* ---- 主内容 ---- */
.home-content {
  position: relative;
  z-index: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 40px 20px;
  animation: fadeIn 0.8s ease-out forwards;
}

/* ---- 顶部装饰 ---- */
.top-ornament {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 28px;
}
.ornament-line {
  display: block;
  width: 60px;
  height: 1px;
  background: linear-gradient(90deg, transparent, rgba(0, 212, 255, 0.5), transparent);
}
.ornament-diamond {
  color: rgba(0, 212, 255, 0.5);
  font-size: 0.6rem;
  text-shadow: 0 0 8px rgba(0, 212, 255, 0.5);
  animation: float 3s ease-in-out infinite;
}

/* ---- 主标题（逐字辉光） ---- */
.main-title {
  font-size: clamp(2.4rem, 6vw, 4rem);
  font-weight: 700;
  letter-spacing: 0.25em;
  margin-bottom: 12px;
  display: flex;
  gap: 4px;
}
.title-glow {
  display: inline-block;
  background: linear-gradient(180deg, #e0f0ff 0%, #00d4ff 50%, #7b61ff 100%);
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;
  filter: drop-shadow(0 0 12px rgba(0, 212, 255, 0.5))
          drop-shadow(0 0 24px rgba(0, 212, 255, 0.2));
  animation: float 4s ease-in-out infinite;
}
/* 每个字不同的动画延迟 */
.title-glow.delay-1 { animation-delay: 0.1s; }
.title-glow.delay-2 { animation-delay: 0.2s; }
.title-glow.delay-3 { animation-delay: 0.3s; }
.title-glow.delay-4 { animation-delay: 0.4s; }
.title-glow.delay-5 { animation-delay: 0.5s; }

/* ---- 副标题 ---- */
.sub-title {
  font-size: 1rem;
  color: #5a7a9a;
  letter-spacing: 0.3em;
  margin-bottom: 50px;
}

/* ---- 功能入口卡片组 ---- */
.entry-cards {
  display: flex;
  gap: 32px;
  flex-wrap: wrap;
  justify-content: center;
}

/* ---- 单个入口卡片 ---- */
.entry-card {
  position: relative;
  width: 300px;
  padding: 36px 28px 28px;
  cursor: pointer;
  text-align: center;
  display: flex;
  flex-direction: column;
  align-items: center;
  animation: fadeIn 0.6s ease-out forwards;
}
.entry-card:nth-child(2) {
  animation-delay: 0.15s;
}

/* 卡片hover时整体上浮 + 辉光增强 */
.entry-card:hover {
  transform: translateY(-6px);
  transition: transform 0.35s ease, border-color 0.35s ease, box-shadow 0.35s ease;
}

/* 卡片四角装饰 */
.card-corner {
  position: absolute;
  width: 16px;
  height: 16px;
  border-color: rgba(0, 212, 255, 0.5);
  border-style: solid;
  border-width: 0;
  transition: all 0.4s ease;
}
.card-corner.tl { top: 4px; left: 4px;   border-top-width: 1px; border-left-width: 1px; }
.card-corner.tr { top: 4px; right: 4px;  border-top-width: 1px; border-right-width: 1px; }
.card-corner.bl { bottom: 4px; left: 4px;  border-bottom-width: 1px; border-left-width: 1px; }
.card-corner.br { bottom: 4px; right: 4px; border-bottom-width: 1px; border-right-width: 1px; }

.entry-card:hover .card-corner {
  border-color: rgba(0, 212, 255, 0.9);
  width: 22px;
  height: 22px;
}

/* ---- 卡片图标 ---- */
.card-icon {
  width: 64px;
  height: 64px;
  margin-bottom: 18px;
  display: flex;
  align-items: center;
  justify-content: center;
}

/* 纯CSS八角星 */
.octagram {
  display: block;
  width: 40px;
  height: 40px;
  background: rgba(0, 212, 255, 0.6);
  clip-path: polygon(
    50% 0%,    62% 38%,   100% 50%,
    62% 62%,   50% 100%,  38% 62%,
    0% 50%,    38% 38%
  );
  box-shadow: 0 0 20px rgba(0, 212, 255, 0.5),
              0 0 40px rgba(0, 212, 255, 0.2);
  animation: float 3s ease-in-out infinite;
}

/* 纯CSS月亮 */
.moon {
  display: block;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: rgba(200, 180, 220, 0.9);
  box-shadow:
    inset -8px 2px 0 rgba(120, 100, 160, 0.6),
    0 0 20px rgba(180, 160, 220, 0.5),
    0 0 40px rgba(180, 160, 220, 0.2);
  animation: float 4s ease-in-out infinite;
}

/* ---- 卡片标题 ---- */
.card-title {
  font-size: 1.3rem;
  font-weight: 600;
  color: #b8d0e7;
  letter-spacing: 0.12em;
  margin-bottom: 10px;
  transition: color 0.3s ease, text-shadow 0.3s ease;
}
.entry-card:hover .card-title {
  color: #00d4ff;
  text-shadow: 0 0 15px rgba(0, 212, 255, 0.6);
}

/* ---- 卡片描述 ---- */
.card-desc {
  font-size: 0.85rem;
  color: #5a7a9a;
  line-height: 1.6;
  margin-bottom: 20px;
}

/* ---- 卡片操作文字 ---- */
.card-action {
  font-size: 0.9rem;
  font-weight: 500;
  color: rgba(0, 212, 255, 0.6);
  letter-spacing: 0.1em;
  display: flex;
  align-items: center;
  gap: 6px;
  transition: all 0.3s ease;
}
.card-action .arrow {
  transition: transform 0.3s ease;
}
.entry-card:hover .card-action {
  color: #00d4ff;
  text-shadow: 0 0 10px rgba(0, 212, 255, 0.5);
}
.entry-card:hover .card-action .arrow {
  transform: translateX(4px);
}

/* ---- 底部状态条 ---- */
.status-bar {
  margin-top: 48px;
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 8px 18px;
  border: 1px solid rgba(0, 212, 255, 0.12);
  clip-path: polygon(
    4px 0%,     calc(100% - 4px) 0%,
    100% 4px,   100% calc(100% - 4px),
    calc(100% - 4px) 100%, 4px 100%,
    0% calc(100% - 4px), 0% 4px
  );
}
.status-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: #00ff88;
  box-shadow: 0 0 6px rgba(0, 255, 136, 0.6);
  animation: glowPulse 2s ease-in-out infinite alternate;
}
.status-text {
  font-size: 0.7rem;
  letter-spacing: 0.2em;
  color: #5a7a9a;
}
.status-code {
  font-size: 0.7rem;
  color: rgba(0, 212, 255, 0.3);
  margin-left: auto;
}

/* ---- 响应式 ---- */
@media (max-width: 680px) {
  .entry-cards {
    flex-direction: column;
    align-items: center;
  }
  .entry-card {
    width: 100%;
    max-width: 320px;
  }
}
</style>
