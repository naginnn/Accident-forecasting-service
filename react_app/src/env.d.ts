/// <reference types="vite/client" />

interface ImportMetaEnv {
    VITE_API_URL: string;
    VITE_API_BACK_PORT: string;
    VITE_API_MODEL_PORT: string;
}

interface ImportMeta {
    readonly env: ImportMetaEnv
}