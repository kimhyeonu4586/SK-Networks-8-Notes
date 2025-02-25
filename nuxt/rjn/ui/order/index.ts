import { defineNuxtModule } from '@nuxt/kit';
import { resolve } from 'path';

export default defineNuxtModule({
    meta: {
        name: 'order',
        configKey: 'order',
    },

    setup(moduleOptions, nuxt) {
        const themeDir = resolve(__dirname, '..');

        nuxt.hook('pages:extend', (pages) => {
            pages.push({
                name: 'OrderList',
                path: '/order/list',
                file: resolve(themeDir, 'order/pages/list/List.vue'),
            });
        });

        nuxt.hook('imports:dirs', (dirs) => {
            dirs.push(resolve(__dirname, 'store'));
        });
    },
});

