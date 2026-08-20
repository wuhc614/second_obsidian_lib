/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      /* 自定义科幻HUD色系 */
      colors: {
        'hud': {
          'bg':     '#0a0e1a',   /* 深空背景 */
          'panel':  '#0d1125',   /* 面板底色 */
          'border': '#1a3a5c',   /* 边框色 */
          'glow':   '#00d4ff',   /* 主辉光蓝 */
          'glow-2': '#7b61ff',   /* 辅助辉光紫 */
          'text':   '#b8d0e7',   /* 主文本 */
          'dim':    '#5a7a9a',   /* 次要文本 */
          'accent': '#ff6b9d',   /* 强调色（粉） */
          'success':'#00ff88',   /* 成功绿 */
        }
      },
      /* 自定义辉光动画 */
      animation: {
        'glow-pulse': 'glowPulse 2s ease-in-out infinite alternate',
        'scan-line':  'scanLine 4s linear infinite',
        'float':      'float 6s ease-in-out infinite',
        'fade-in':    'fadeIn 0.6s ease-out forwards',
        'slide-up':   'slideUp 0.5s ease-out forwards',
      },
      keyframes: {
        glowPulse: {
          '0%':   { boxShadow: '0 0 5px rgba(0, 212, 255, 0.3), 0 0 10px rgba(0, 212, 255, 0.1)' },
          '100%': { boxShadow: '0 0 20px rgba(0, 212, 255, 0.6), 0 0 40px rgba(0, 212, 255, 0.3), 0 0 60px rgba(0, 212, 255, 0.1)' },
        },
        scanLine: {
          '0%':   { transform: 'translateY(-100%)' },
          '100%': { transform: 'translateY(100vh)' },
        },
        float: {
          '0%, 100%': { transform: 'translateY(0px)' },
          '50%':      { transform: 'translateY(-10px)' },
        },
        fadeIn: {
          '0%':   { opacity: '0', transform: 'translateY(10px)' },
          '100%': { opacity: '1', transform: 'translateY(0)' },
        },
        slideUp: {
          '0%':   { opacity: '0', transform: 'translateY(20px)' },
          '100%': { opacity: '1', transform: 'translateY(0)' },
        },
      },
    },
  },
  plugins: [],
}
