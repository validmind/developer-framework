import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import { basename, resolve } from 'path';
import { glob } from 'glob';

// Automatically find all Svelte components in the `gui_src/components` folder
const componentEntries = glob.sync('gui_src/components/*.jsx').reduce((entries, file) => ({
  ...entries,
  [basename(file, '.jsx')]: resolve(__dirname, file)
}), {});

for (const [name, path] of Object.entries(componentEntries)) {
  console.log(`Found component: ${name} at ${path}`);
}

console.log('Building components...');

export default defineConfig({
  plugins: [react()],
  build: {
    minify: false,
    rollupOptions: {
      input: resolve(__dirname, 'gui_src/index.jsx'),
      output: {
        dir: 'validmind/gui/js/',
        entryFileNames: 'bundle.js',
        format: 'iife',
        name: 'VMComponents',
      },
    }
  }
});
