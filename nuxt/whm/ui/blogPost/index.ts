import { defineNuxtModule } from "@nuxt/kit";
import { resolve } from "path";

export default defineNuxtModule({
  meta: {
    name: "blogPost",
    configKey: "blogPost",
  },

  setup(moduleOptions, nuxt) {
    const themeDir = resolve(__dirname, "..");

    nuxt.hook("pages:extend", (pages) => {
      pages.push({
        name: "blogPostList",
        path: "/blog-post/list",
        file: resolve(themeDir, "blogPost/pages/list/List.vue"),
      });

      pages.push({
        name: "blogPostRegister",
        path: "/blog-post/register",
        file: resolve(themeDir, "blogPost/pages/register/Register.vue"),
      });

      pages.push({
        name: "blogPostRead",
        path: "/blog-post/read/:id",
        file: resolve(themeDir, "blogPost/pages/read/Read.vue"),
      });

      pages.push({
        name: "blogPostUpdate",
        path: "/blog-post/update/:id",
        file: resolve(themeDir, "blogPost/pages/update/Update.vue"),
      });
    });

    nuxt.hook("imports:dirs", (dirs) => {
      dirs.push(resolve(__dirname, "store"));
    });
  },
});
