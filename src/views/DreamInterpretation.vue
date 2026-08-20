<template>
  <!--
    周公解梦页
    用户描述梦境 → 校验 → POST /api/dream_analysis → 渲染AI解梦报告
    HUD科幻风格 + 彩蛋关键词检测 + 结构化文本渲染
  -->
  <div class="dream-page">
    <!-- 背景粒子（蓝紫色调） -->
    <div class="bg-particles" aria-hidden="true">
      <span v-for="i in 50" :key="i" class="particle" :style="particleStyle(i)"></span>
    </div>

    <div class="page-container">
      <!-- 顶部导航栏 -->
      <header class="page-header">
        <button class="hud-back" @click="goBack">
          <span class="back-arrow">◂</span>
          返回首页
        </button>
        <div class="header-info">
          <span class="header-badge">DREAM · ANALYSIS</span>
        </div>
      </header>

      <!-- 页面标题 -->
      <div class="page-title-section">
        <h1 class="page-title hud-title-line">周公解梦</h1>
        <p class="page-desc">
          描述你的梦境，AI 智能解读潜意识中的深意
        </p>
      </div>

      <!-- 表单面板 -->
      <form class="form-panel hud-panel" @submit.prevent="handleSubmit" novalidate>
        <!-- 第一行：梦境内容（独立一行，textarea） -->
        <div class="form-group">
          <label class="hud-label hud-required" for="dreamContent">梦境内容</label>
          <textarea
            id="dreamContent"
            v-model.trim="form.dreamContent"
            class="hud-textarea"
            rows="4"
            placeholder="请详细描述你的梦境，包含场景、人物、情节、情绪感受..."
            :class="{ 'input-error': errors.dreamContent }"
          ></textarea>
          <div class="field-meta">
            <span :class="{ 'text-warn': form.dreamContent.length > 480 }">
              {{ form.dreamContent.length }}/500
            </span>
          </div>
          <p v-if="errors.dreamContent" class="hud-error">{{ errors.dreamContent }}</p>
        </div>

        <!-- 第二行：做梦时间 -->
        <div class="form-group">
          <label class="hud-label hud-required" for="dreamTime">做梦时间</label>
          <input
            id="dreamTime"
            v-model.trim="form.dreamTime"
            type="date"
            class="hud-input"
            :class="{ 'input-error': errors.dreamTime }"
          />
          <p v-if="errors.dreamTime" class="hud-error">{{ errors.dreamTime }}</p>
        </div>

        <!-- 第三行：性别 + 年龄（同行） -->
        <div class="form-row">
          <div class="form-group">
            <label class="hud-label hud-required" for="gender">性别</label>
            <select
              id="gender"
              v-model="form.gender"
              class="hud-select"
              :class="{ 'input-error': errors.gender }"
            >
              <option value="" disabled>请选择性别</option>
              <option value="male">男</option>
              <option value="female">女</option>
              <option value="other">其他</option>
            </select>
            <p v-if="errors.gender" class="hud-error">{{ errors.gender }}</p>
          </div>
          <div class="form-group">
            <label class="hud-label hud-required" for="age">年龄</label>
            <input
              id="age"
              v-model.number="form.age"
              type="number"
              class="hud-input"
              placeholder="请输入年龄"
              min="1"
              max="120"
              :class="{ 'input-error': errors.age }"
            />
            <p v-if="errors.age" class="hud-error">{{ errors.age }}</p>
          </div>
        </div>

        <!-- 第四行：职业 -->
        <div class="form-group">
          <label class="hud-label hud-required" for="occupation">职业</label>
          <input
            id="occupation"
            v-model.trim="form.occupation"
            type="text"
            class="hud-input"
            placeholder="如：设计师、教师、创业者"
            :class="{ 'input-error': errors.occupation }"
          />
          <p v-if="errors.occupation" class="hud-error">{{ errors.occupation }}</p>
        </div>

        <!-- 第五行：近期状态 -->
        <div class="form-group">
          <label class="hud-label hud-required" for="recentState">近期状态</label>
          <select
            id="recentState"
            v-model="form.recentState"
            class="hud-select"
            :class="{ 'input-error': errors.recentState }"
          >
            <option value="" disabled>请选择近期状态</option>
            <option value="stressed">压力较大</option>
            <option value="calm">心态平和</option>
            <option value="anxious">焦虑不安</option>
            <option value="excited">兴奋期待</option>
            <option value="tired">疲惫乏力</option>
            <option value="confused">迷茫困惑</option>
          </select>
          <p v-if="errors.recentState" class="hud-error">{{ errors.recentState }}</p>
        </div>

        <!-- 第六行：解梦关注点 -->
        <div class="form-group">
          <label class="hud-label hud-required" for="focus">解梦关注点</label>
          <textarea
            id="focus"
            v-model.trim="form.focus"
            class="hud-textarea"
            rows="3"
            placeholder="你希望通过解梦了解什么？如：情感暗示、事业预兆、健康提醒..."
            :class="{ 'input-error': errors.focus }"
          ></textarea>
          <p v-if="errors.focus" class="hud-error">{{ errors.focus }}</p>
        </div>

        <!-- 提交按钮 -->
        <div class="form-submit">
          <button
            type="submit"
            class="hud-btn submit-btn"
            :disabled="submitting"
          >
            <span v-if="submitting" class="btn-loading">
              <span class="loading-ring"></span>
              梦境解读中...
            </span>
            <span v-else>
              <span class="btn-icon">☽</span>
              立即解梦
            </span>
          </button>
        </div>
      </form>

      <!-- ============================================================
           结果展示区域
           三种状态：成功（AI文本）、错误（异常信息）、彩蛋触发
           ============================================================ -->
      <transition name="result-slide">
        <div
          v-if="result"
          class="result-section hud-result"
          :class="{
            'is-error': result.type === 'error',
            'is-easter-egg': result.easterEgg,
          }"
        >
          <!-- 结果头部 -->
          <div class="result-header">
            <span class="result-icon" :class="{ 'pulse-fast': result.easterEgg }">☽</span>
            <h3>
              {{ result.type === 'error' ? '请求异常' : result.easterEgg ? '🎭 梦境彩蛋' : '解梦分析报告' }}
            </h3>
            <span class="result-icon" :class="{ 'pulse-fast': result.easterEgg }">☽</span>
          </div>

          <!-- 彩蛋触发标签 -->
          <div v-if="result.easterEgg && result.eggTags.length" class="egg-tags">
            <span
              v-for="tag in result.eggTags"
              :key="tag"
              class="egg-tag"
            >#{{ tag }}</span>
          </div>

          <!-- 错误提示 -->
          <div v-if="result.type === 'error'" class="result-body error-body">
            <div class="error-icon-wrap">
              <span class="error-icon-code">{{ result.code }}</span>
            </div>
            <p class="error-message">{{ result.content }}</p>
            <p class="error-hint">
              {{ result.code === 400 ? '请检查表单填写是否完整' : '请确认后端服务已启动且 API Key 已配置' }}
            </p>
          </div>

          <!-- AI 解梦文本（渲染为结构化HTML） -->
          <div v-else class="result-body ai-body">
            <div class="ai-content" v-html="renderAIText(result.content)"></div>

            <!-- 操作栏 -->
            <div class="result-actions">
              <button class="hud-back action-btn" @click="scrollToForm">
                <span class="back-arrow">◂</span> 再次解梦
              </button>
              <span class="result-timestamp">{{ result.timestamp }}</span>
            </div>
          </div>
        </div>
      </transition>
    </div>
  </div>
</template>

<script setup>
/**
 * DreamInterpretation.vue — 周公解梦页
 *
 * 完整流程：
 * 1. 表单填写 → 前端必填校验 → 不通过则阻止提交
 * 2. 校验通过 → 按钮进入加载态 → POST /api/dream_analysis
 * 3. 成功 → 渲染 AI 文本（解析 Markdown → HTML，段落/标题/加粗）
 * 4. 失败 → 区分 code=400/500，展示不同提示
 * 5. 彩蛋：检测用户输入中的趣味关键词
 */
import { reactive, ref, nextTick } from 'vue'
import { useRouter } from 'vue-router'
import { submitDreamInterpretation } from '@/api/index.js'

const router = useRouter()

/** 返回首页 */
function goBack() {
  router.push('/')
}

// ---- 表单数据 ----
const form = reactive({
  dreamContent: '',
  dreamTime: '',
  gender: '',
  age: '',
  occupation: '',
  recentState: '',
  focus: '',
})

// ---- 验证错误 ----
const errors = reactive({
  dreamContent: '',
  dreamTime: '',
  gender: '',
  age: '',
  occupation: '',
  recentState: '',
  focus: '',
})

// ---- 提交状态 ----
const submitting = ref(false)

// ---- 结果对象：{ type, content, code, easterEgg, eggTags, timestamp } ----
const result = ref(null)

// ---- 彩蛋关键词库 ----
const EGG_KEYWORDS = {
  '鬼':     '鬼怪识别图谱已加载 👻',
  '飞':     '飞行模式已激活',
  '掉牙':   '牙齿保险公司已就位',
  '考试':   '考试 PTSD 互助小组发来慰问',
  '前任':   '前任清除程序已运行',
  '裸奔':   '社死预防系统启动',
  '坠落':   '坠落缓冲气垫已部署',
  '追':     '追逐模拟器已上线',
  '蛇':     '蛇类翻译官已连线',
  '水':     '水下呼吸器已装备',
  '死':     '生命探测仪校准中',
  '迷路':   'GPS 信号已恢复',
  '迟到':   '时间管理局已介入',
  '发财':   '财运之门已开锁',
}

/**
 * 表单校验
 * @returns {boolean}
 */
function validate() {
  let valid = true
  Object.keys(errors).forEach((k) => (errors[k] = ''))

  if (!form.dreamContent)           { errors.dreamContent = '请描述你的梦境内容'; valid = false }
  else if (form.dreamContent.length < 10) { errors.dreamContent = '梦境描述至少10个字，请尽量详细'; valid = false }
  else if (form.dreamContent.length > 500) { errors.dreamContent = '梦境描述不能超过500字'; valid = false }
  if (!form.dreamTime)             { errors.dreamTime = '请选择做梦时间'; valid = false }
  if (!form.gender)                { errors.gender = '请选择性别'; valid = false }
  if (form.age === '' || form.age === null) { errors.age = '请输入年龄'; valid = false }
  else if (!Number.isInteger(form.age) || form.age < 1 || form.age > 120) { errors.age = '请输入有效年龄（1-120）'; valid = false }
  if (!form.occupation)            { errors.occupation = '请输入职业'; valid = false }
  else if (form.occupation.length < 2) { errors.occupation = '请输入有效的职业'; valid = false }
  if (!form.recentState)           { errors.recentState = '请选择近期状态'; valid = false }
  if (!form.focus)                 { errors.focus = '请填写解梦关注点'; valid = false }
  else if (form.focus.length < 4)  { errors.focus = '关注点描述至少4个字'; valid = false }

  return valid
}

/**
 * 检测彩蛋关键词
 * @param {string} text
 * @returns {{ triggered: boolean, tags: string[] }}
 */
function detectEasterEgg(text) {
  const tags = []
  for (const [keyword, tag] of Object.entries(EGG_KEYWORDS)) {
    if (text.includes(keyword)) {
      tags.push(tag)
    }
  }
  return { triggered: tags.length > 0, tags }
}

/**
 * 表单提交处理
 */
async function handleSubmit() {
  // 校验不通过 → 阻止请求
  if (!validate()) return

  submitting.value = true
  result.value = null

  // 构建彩蛋检测文本（梦境内容 + 关注点 + 职业）
  const combinedText = `${form.dreamContent} ${form.focus} ${form.occupation} ${form.recentState}`
  const egg = detectEasterEgg(combinedText)

  try {
    const data = await submitDreamInterpretation({
      dreamContent: form.dreamContent,
      dreamTime: form.dreamTime,
      gender: form.gender,
      age: form.age,
      occupation: form.occupation,
      recentState: form.recentState,
      focus: form.focus,
    })

    result.value = {
      type: 'success',
      content: data,
      code: 200,
      easterEgg: egg.triggered,
      eggTags: egg.tags,
      timestamp: new Date().toLocaleString('zh-CN'),
    }
  } catch (err) {
    console.error('解梦请求失败:', err)
    const code = err.code || err.response?.status || 500
    const msg = err.message || '请求失败，请稍后重试'
    result.value = {
      type: 'error',
      content: code === 400
        ? msg
        : 'AI 服务暂时不可用，请确认：\n1. 后端服务已启动\n2. .env 中已配置 DEEPSEEK_API_KEY',
      code,
      easterEgg: egg.triggered,
      eggTags: egg.tags,
      timestamp: new Date().toLocaleString('zh-CN'),
    }
  } finally {
    submitting.value = false
  }
}

/**
 * 将 AI 返回的 Markdown 格式文本 → 结构化 HTML
 * 支持：## 标题、**加粗**、--- 分割线、换行分段
 */
function renderAIText(text) {
  if (!text) return ''

  let html = text
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')

  html = html.replace(/^#{1,2}\s+(.+)$/gm, '<h3 class="ai-h3">$1</h3>')
  html = html.replace(/\*\*(.+?)\*\*/g, '<strong class="ai-bold">$1</strong>')
  html = html.replace(/^---+\s*$/gm, '<hr class="ai-divider">')
  html = html.replace(/\n\n+/g, '</p><p class="ai-p">')
  html = html.replace(/\n/g, '<br>')
  html = '<p class="ai-p">' + html + '</p>'
  html = html.replace(/<p class="ai-p"><\/p>/g, '')

  return html
}

/** 滚动回表单 */
function scrollToForm() {
  result.value = null
  nextTick(() => {
    const formEl = document.querySelector('.form-panel')
    if (formEl) formEl.scrollIntoView({ behavior: 'smooth', block: 'start' })
  })
}

/** 背景粒子样式 */
function particleStyle(i) {
  const size = Math.random() * 2.5 + 1
  const left = Math.random() * 100
  const top = Math.random() * 100
  const delay = Math.random() * 5
  const hue = i % 2 === 0 ? 200 : 270
  return {
    width: `${size}px`,
    height: `${size}px`,
    left: `${left}%`,
    top: `${top}%`,
    animationDelay: `${delay}s`,
    backgroundColor: `hsla(${hue}, 70%, 60%, 0.35)`,
  }
}
</script>

<style scoped>
/* ============================================================
   周公解梦页 — 样式
   ============================================================ */

.dream-page {
  min-height: 100vh;
  background:
    radial-gradient(ellipse at 80% 10%, rgba(123, 97, 255, 0.04) 0%, transparent 55%),
    radial-gradient(ellipse at 20% 70%, rgba(0, 212, 255, 0.03) 0%, transparent 55%),
    #0a0e1a;
  display: flex;
  justify-content: center;
  padding: 20px;
}

.bg-particles {
  position: fixed;
  inset: 0;
  pointer-events: none;
  z-index: 0;
}
.bg-particles .particle {
  position: absolute;
  border-radius: 50%;
  animation: twinkle2 4s ease-in-out infinite;
}

.page-container {
  position: relative;
  z-index: 1;
  width: 100%;
  max-width: 680px;
  animation: fadeIn 0.5s ease-out forwards;
}

/* ---- 顶部导航 ---- */
.page-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 24px;
  flex-wrap: wrap;
  gap: 12px;
}
.header-badge {
  font-size: 0.7rem;
  letter-spacing: 0.25em;
  color: rgba(123, 97, 255, 0.45);
  padding: 4px 12px;
  border: 1px solid rgba(123, 97, 255, 0.18);
  clip-path: polygon(
    3px 0%,     calc(100% - 3px) 0%,
    100% 3px,   100% calc(100% - 3px),
    calc(100% - 3px) 100%, 3px 100%,
    0% calc(100% - 3px), 0% 3px
  );
}

/* ---- 页面标题 ---- */
.page-title-section { text-align: center; margin-bottom: 32px; }
.page-title {
  font-size: 1.6rem;
  font-weight: 600;
  color: #b8d0e7;
  letter-spacing: 0.15em;
  margin-bottom: 8px;
  text-shadow: 0 0 15px rgba(123, 97, 255, 0.35);
}
.page-desc { font-size: 0.9rem; color: #5a7a9a; letter-spacing: 0.05em; }

/* ---- 表单面板 ---- */
.form-panel { padding: 32px 28px; margin-bottom: 28px; }
.form-group { margin-bottom: 20px; }
.form-group:last-of-type { margin-bottom: 0; }
.field-meta { text-align: right; font-size: 0.7rem; color: rgba(90, 122, 154, 0.5); margin-top: 4px; }
.text-warn { color: rgba(255, 160, 60, 0.7); }

.input-error {
  border-color: rgba(255, 107, 157, 0.6) !important;
  box-shadow: 0 0 12px rgba(255, 107, 157, 0.15) !important;
}

/* ---- 提交按钮 ---- */
.form-submit { display: flex; justify-content: center; margin-top: 28px; }
.submit-btn { min-width: 200px; font-size: 1.05rem; }
.submit-btn:disabled { opacity: 0.6; cursor: not-allowed; }
.submit-btn .btn-icon { display: inline-block; margin-right: 6px; animation: float 2s ease-in-out infinite; }

.btn-loading { display: inline-flex; align-items: center; gap: 8px; }
.loading-ring {
  display: inline-block; width: 16px; height: 16px;
  border: 2px solid rgba(123, 97, 255, 0.25);
  border-top-color: #7b61ff;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}
@keyframes spin { to { transform: rotate(360deg); } }

/* ---- 结果展示区域（通用） ---- */
.result-section {
  padding: 28px;
  margin-bottom: 40px;
  transition: all 0.4s ease;
}

.result-section.is-easter-egg {
  border-color: rgba(123, 97, 255, 0.5);
  box-shadow:
    0 0 20px rgba(123, 97, 255, 0.15),
    0 0 40px rgba(255, 107, 157, 0.1),
    inset 0 0 30px rgba(123, 97, 255, 0.04);
}

.result-section.is-error {
  border-color: rgba(255, 107, 157, 0.3);
}

.result-header {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
  margin-bottom: 12px;
}
.result-header h3 {
  font-size: 1.05rem;
  font-weight: 600;
  color: #7b61ff;
  letter-spacing: 0.12em;
  text-shadow: 0 0 10px rgba(123, 97, 255, 0.4);
}
.result-icon {
  color: rgba(123, 97, 255, 0.45);
  font-size: 0.7rem;
  transition: all 0.3s;
}
.result-icon.pulse-fast { animation: pulseFast 0.6s ease-in-out infinite alternate; }
@keyframes pulseFast {
  0% { opacity: 0.3; transform: scale(1); }
  100% { opacity: 1; transform: scale(1.4); }
}

/* ---- 彩蛋标签 ---- */
.egg-tags {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 8px;
  margin-bottom: 16px;
}
.egg-tag {
  font-size: 0.75rem;
  color: #7b61ff;
  background: rgba(123, 97, 255, 0.1);
  border: 1px solid rgba(123, 97, 255, 0.25);
  padding: 3px 10px;
  clip-path: polygon(3px 0%, calc(100% - 3px) 0%, 100% 3px, 100% calc(100% - 3px), calc(100% - 3px) 100%, 3px 100%, 0% calc(100% - 3px), 0% 3px);
  animation: fadeIn 0.4s ease-out forwards;
}

/* ---- 结果内容容器 ---- */
.result-body {
  background: rgba(10, 14, 26, 0.6);
  border: 1px solid rgba(123, 97, 255, 0.12);
  padding: 20px 22px;
}

/* AI 文本主体 */
.ai-body { max-height: 520px; overflow-y: auto; }
.ai-content { font-size: 0.9rem; color: #c0d8ef; line-height: 1.9; letter-spacing: 0.02em; }
.ai-content :deep(.ai-h3) {
  font-size: 1.05rem;
  font-weight: 600;
  color: #c0b0ff;
  margin: 20px 0 10px;
  padding-bottom: 6px;
  border-bottom: 1px solid rgba(123, 97, 255, 0.2);
  text-shadow: 0 0 8px rgba(123, 97, 255, 0.3);
}
.ai-content :deep(.ai-h3:first-child) { margin-top: 0; }
.ai-content :deep(.ai-bold) {
  color: #e0d8ff;
  font-weight: 700;
  text-shadow: 0 0 3px rgba(123, 97, 255, 0.2);
}
.ai-content :deep(.ai-divider) {
  border: none;
  border-top: 1px dashed rgba(123, 97, 255, 0.15);
  margin: 16px 0;
}
.ai-content :deep(.ai-p) { margin: 0 0 8px; }

/* ---- 错误态 ---- */
.error-body { text-align: center; padding: 28px 20px; }
.error-icon-wrap { margin-bottom: 12px; }
.error-icon-code {
  display: inline-block;
  font-size: 2rem;
  font-weight: 700;
  color: #ff6b9d;
  text-shadow: 0 0 15px rgba(255, 107, 157, 0.4);
}
.error-message {
  font-size: 0.9rem;
  color: #b8d0e7;
  line-height: 1.7;
  white-space: pre-line;
  margin-bottom: 12px;
}
.error-hint { font-size: 0.78rem; color: #5a7a9a; }

/* ---- 结果操作栏 ---- */
.result-actions {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-top: 16px;
  padding-top: 12px;
  border-top: 1px solid rgba(123, 97, 255, 0.1);
}
.action-btn { font-size: 0.82rem; }
.result-timestamp {
  font-size: 0.7rem;
  color: rgba(90, 122, 154, 0.5);
  letter-spacing: 0.05em;
}

/* ---- 入场/离场过渡动画 ---- */
.result-slide-enter-active { animation: resultIn 0.45s cubic-bezier(0.22, 1, 0.36, 1); }
.result-slide-leave-active { animation: resultOut 0.25s ease-in; }
@keyframes resultIn {
  0%   { opacity: 0; transform: translateY(24px); }
  100% { opacity: 1; transform: translateY(0); }
}
@keyframes resultOut {
  0%   { opacity: 1; transform: translateY(0); }
  100% { opacity: 0; transform: translateY(-12px); }
}

/* ---- 响应式 ---- */
@media (max-width: 480px) {
  .form-panel { padding: 22px 16px; }
  .page-title { font-size: 1.3rem; }
}
</style>
