/// <reference types="vite/client" />

interface ImportMetaEnv {
    VITE_API_URL: string
    VITE_API_AUTH_PORT: string
    VITE_API_OBJ_PORT: string
    VITE_API_REPORT_PORT: string
}

interface ImportMeta {
    readonly env: ImportMetaEnv
}