# Tailwind CSS Setup Guide

This guide will help you set up and use Tailwind CSS in your project using the Tailwind CLI.

## Prerequisites

- Node.js and npm should be installed on your machine.
- Tailwind CSS is already set up in your project.

## Installation

1. **Ensure Tailwind CSS is installed:**

   If Tailwind CSS is not installed, run the following command in your project directory:

   ```bash
   npm install tailwindcss
   ```

2. **Verify Tailwind Configuration:**

   Ensure you have a `tailwind.config.js` file. If not, create one using:

   ```bash
   npx tailwindcss init
   ```

3. **CSS File Setup:**

   Ensure your `input.css` file includes the Tailwind directives:

   ```css
   @tailwind base;
   @tailwind components;
   @tailwind utilities;
   ```

4. **Build your CSS:**

   Use the Tailwind CLI to compile your CSS. The command is already set up in your `package.json`:

   ```json
   "scripts": {
     "watch": "npx tailwindcss -i ./form_campaign_app/static/tailwind/input.css -o ./form_campaign_app/static/tailwind/output.css --watch"
   }
   ```

   Run the build script to generate your CSS:

   ```bash
   npm run watch
   ```

5. **Include the compiled CSS in your HTML:**

   Link the compiled CSS file in your HTML file:

   ```html
   <link href="/form_campaign_app/static/tailwind/output.css" rel="stylesheet">
   ```

## Development

- To watch for changes and automatically rebuild your CSS, use the `watch` script as shown above.

## Additional Resources

- [Tailwind CSS Documentation](https://tailwindcss.com/docs)
- [Tailwind CSS GitHub Repository](https://github.com/tailwindlabs/tailwindcss)
