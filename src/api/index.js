import axios from 'axios'

/**
 * API 请求模块 — 星梦智能助手
 *
 * 所有后端接口的封装层，统一处理：
 * - 字段名转换（前端 camelCase → 后端 snake_case）
 * - 响应格式解析 {code, msg, data}
 * - 业务错误与网络错误的统一抛出
 */

// 创建 axios 实例
const request = axios.create({
  baseURL: 'http://localhost:8002',  // FastAPI 后端地址
  timeout: 60000,                     // 大模型调用较慢，60s 超时
  headers: {
    'Content-Type': 'application/json',
  },
})

// ---- 请求拦截器 ----
request.interceptors.request.use(
  (config) => {
    // TODO: token 注入点
    return config
  },
  (error) => Promise.reject(error)
)

// ---- 响应拦截器 —— 统一解析 {code, msg, data} ----
request.interceptors.response.use(
  (response) => {
    const { code, msg, data } = response.data || {}
    if (code && code !== 200) {
      // 业务层错误（400 参数缺失 / 500 服务器错误）
      const err = new Error(msg || `请求异常 (code=${code})`)
      err.code = code
      return Promise.reject(err)
    }
    // 成功：直接返回 data 字段
    return data ?? response.data
  },
  (error) => {
    // 网络层错误（超时、断网、CORS等）
    console.error('[API] 网络请求失败:', error.message)
    return Promise.reject(error)
  }
)

// ============================================================
// 接口方法
// ============================================================

/**
 * 星座星盘分析测算
 * POST /api/star_analysis
 *
 * @param {Object} params - 表单参数（camelCase）
 * @param {string} params.birthDate     - 出生年月日
 * @param {string} params.birthTime     - 出生时间
 * @param {string} params.birthPlace    - 出生地点
 * @param {string} params.gender        - 性别
 * @param {string} params.emotionState  - 情感状态
 * @param {string} params.occupation    - 职业身份
 * @param {string} params.focus         - 测算关注点
 * @returns {Promise<string>} AI 分析文本
 */
export function submitStarAnalysis(params) {
  console.log('[API] 星座星盘分析 — 请求发送')
  return request.post('/api/star_analysis', {
    birth_date:    params.birthDate,
    birth_time:    params.birthTime,
    birth_place:   params.birthPlace,
    gender:        params.gender,
    emotion_status: params.emotionState,
    job:           params.occupation,
    focus:         params.focus,
  })
}

/**
 * 周公解梦
 * POST /api/dream_analysis
 *
 * @param {Object} params - 表单参数（camelCase）
 * @param {string} params.dreamContent  - 梦境内容
 * @param {string} params.dreamTime     - 做梦时间
 * @param {string} params.gender        - 性别
 * @param {number} params.age           - 年龄
 * @param {string} params.occupation    - 职业
 * @param {string} params.recentState   - 近期状态
 * @param {string} params.focus         - 解梦关注点
 * @returns {Promise<string>} AI 解梦文本
 */
export function submitDreamInterpretation(params) {
  console.log('[API] 周公解梦 — 请求发送')
  return request.post('/api/dream_analysis', {
    dream_content: params.dreamContent,
    dream_time:    params.dreamTime,
    gender:        params.gender,
    age:           params.age,
    job:           params.occupation,
    recent_status: params.recentState,
    focus:         params.focus,
  })
}

export default request
