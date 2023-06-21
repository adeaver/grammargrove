/** @type {import('tailwindcss').Config} */

import colors from 'tailwindcss/colors.js';

export default {
  content: ["./src/**/*.{ts,tsx}"],
  theme: {
    extend: {
        fontFamily: {
            body: ['Noto Sans', 'Noto Sans SC', 'sans-serif'],
        },
        colors: {
            'primary': colors.red,
            'text': colors.slate,
            'confirmation': colors.green,
            'warning': colors.orange,
        },
    },
  },
  plugins: [],
}

