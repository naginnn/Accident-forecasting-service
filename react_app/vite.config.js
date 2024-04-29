import path from "path";
import {defineConfig} from 'vite';
import react from '@vitejs/plugin-react';
import viteTsconfigPaths from 'vite-tsconfig-paths';
import checker from 'vite-plugin-checker';


export default defineConfig(() => {
    const baseUrl = path.resolve(__dirname, "src")

    return {
        esbuild: {jsxInject: `import React from 'react'`},
        build: {outDir: 'build'},
        plugins: [
            react({jsxRuntime: 'classic'}),
            viteTsconfigPaths(),
            checker({typescript: true})
        ],
        resolve: {
            alias: [
                {find: '@src', replacement: baseUrl},
            ]
        },
        server: {
            hmr: {
                overlay: true
            },
        },
        clearScreen: false
    };
});
