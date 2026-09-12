/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,ts,jsx,tsx}'],
  theme: {
    extend: {
      colors: {
        brand: {
          50: '#f5f3ea',
          100: '#e8e2cf',
          200: '#d8c79f',
          300: '#c7ae6e',
          400: '#b39242',
          500: '#9c7a2a',
          600: '#785925',
          700: '#563f1d',
          800: '#352915',
          900: '#17120d'
        },
        accent: {
          50: '#ebf7ff',
          100: '#d2edff',
          200: '#a9dcff',
          300: '#7fcbff',
          400: '#59b8ff',
          500: '#2e9dff',
          600: '#1e7fe0',
          700: '#1c64b2',
          800: '#1d4f8a',
          900: '#1c3f69'
        }
      },
      boxShadow: {
        glow: '0 0 0 1px rgba(255,255,255,0.06), 0 20px 30px rgba(9, 12, 16, 0.38)'
      }
    }
  },
  plugins: []
}
