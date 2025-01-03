/** @type {import('tailwindcss').Config} */
module.exports = {
  darkMode: 'class',
  // important: true,
  content: [
    "./form_campaign_app/templates/**/*.{html,js}",
    "./form_campaign_app/static/js/*.js",
    "./node_modules/flowbite/**/*.js",
  ],
  theme: {
    extend: {},
  },
  plugins: [
    require('flowbite/plugin')({
    }),
  ]
}

