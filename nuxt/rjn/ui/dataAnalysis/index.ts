import { defineNuxtModule } from '@nuxt/kit';
import { resolve } from 'path';

export default defineNuxtModule({
    meta: {
        name: 'dataAnalysis',
        configKey: 'dataAnalysis',
    },

    setup(moduleOptions, nuxt) {
        const themeDir = resolve(__dirname, '..');

        nuxt.hook('pages:extend', (pages) => {
            pages.push({
                name: 'DataAnalysis',
                path: '/data/analysis',
                file: resolve(themeDir, 'dataAnalysis/pages/analysis/Analysis.vue'),
            });
        });

        nuxt.hook('imports:dirs', (dirs) => {
            dirs.push(resolve(__dirname, 'store'));
        });
    },
});

