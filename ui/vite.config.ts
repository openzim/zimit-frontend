import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";

/* Function to split index.js into multiple smaller chunks
function manualChunks(id: String) {
  if (id.includes('@fortawesome')) {
    if (id.includes('@fortawesome/free-regular-svg-icons')) {
      return 'fortawesome-free-regular-svg-icons'
    }
    return 'fortawesome'
  }
  if (id.includes('vuetify')) {
    return 'vuetify'
  }
}
*/

export default defineConfig({
  plugins: [vue()],
  /* Configuration to split index.js into multiple smaller chunks
  build: {
    rollupOptions: {
      output: {
        manualChunks: manualChunks
      }
    }
  }*/
});
