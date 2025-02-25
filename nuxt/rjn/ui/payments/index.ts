import { defineNuxtModule } from '@nuxt/kit';
import { resolve } from 'path';

export default defineNuxtModule({
    meta: {
        name: 'payments',
        configKey: 'payments',
    },

    setup(moduleOptions, nuxt) {
        const themeDir = resolve(__dirname, '..');

        nuxt.hook('pages:extend', (pages) => {
            pages.push({
                name: 'PaymentsConfirm',
                path: '/payments/confirm',
                file: resolve(themeDir, 'payments/pages/confirm/Confirm.vue'),
            });

            pages.push({
                name: 'PaymentsSuccess',
                path: '/payments/success',
                file: resolve(themeDir, 'payments/pages/success/Success.vue'),
            });
        });

        nuxt.hook('imports:dirs', (dirs) => {
            dirs.push(resolve(__dirname, 'store'));
        });
    },
});

