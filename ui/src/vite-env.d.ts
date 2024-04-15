/// <reference types="vite/client" />

interface ImportMetaEnv {
  readonly VITE_ZIMFARM_WEBAPI: string;
  readonly VITE_ZIMIT_API_URL: string;
}

interface ImportMeta {
  readonly env: ImportMetaEnv;
}
