/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./app/templates/**/*.html",
    "./app/static/js/**/*.js",
  ],
  theme: {
    extend: {
      colors: {
        // Cores oficiais do Space Girassol
        'sg-sunflower': '#e8a820',
        'sg-amber':     '#d4981a',
        'sg-seed':      '#5c3a21',
        'sg-leaf':      '#4a5d3a',
        'sg-petal':     '#f5ebd9',
        'sg-deep':      '#3a2f25',
      },
      fontFamily: {
        'serif': ['"Cormorant Garamond"', 'Times New Roman', 'serif'],
        'sans':  ['"Source Sans 3"', 'Segoe UI', 'sans-serif'],
      },
    },
  },
  plugins: [],
}