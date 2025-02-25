import { defineNuxtModule } from '@nuxt/kit';
import { resolve } from 'path';

export default defineNuxtModule({
    meta: {
        name: 'board',
        configKey: 'board',
    },

    setup(moduleOptions, nuxt) {
        const themeDir = resolve(__dirname, '..');

        nuxt.hook('pages:extend', (pages) => {
            pages.push({
                name: 'BoardList',
                path: '/board/list',
                file: resolve(themeDir, 'board/pages/list/List.vue'),
            });

            pages.push({
                name: 'BoardRegister',
                path: '/board/register',
                file: resolve(themeDir, 'board/pages/register/Register.vue'),
            });

            pages.push({
                name: 'BoardRead',
                path: '/board/read/:boardId',
                file: resolve(themeDir, 'board/pages/read/Read.vue'),
            });

            pages.push({
                name: 'BoardModify',
                path: '/board/modify/:boardId',
                file: resolve(themeDir, 'board/pages/modify/Modify.vue'),
            });
        });

        nuxt.hook('imports:dirs', (dirs) => {
            dirs.push(resolve(__dirname, 'store'));
        });
    },
});

