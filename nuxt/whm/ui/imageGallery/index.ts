import { defineNuxtModule } from "@nuxt/kit";
import { resolve } from "path";

export default defineNuxtModule({
  meta: {
    name: "imageGallery",
    configKey: "imageGallery",
  },

  setup(moduleOptions, nuxt) {
    const themeDir = resolve(__dirname, "..");

    nuxt.hook("pages:extend", (pages) => {
      pages.push({
        name: "ImageGalleryList",
        path: "/image-gallery/list",
        file: resolve(themeDir, "imageGallery/pages/list/List.vue"),
      });
    });

    nuxt.hook("pages:extend", (pages) => {
      pages.push({
        name: "ImageGalleryRegister",
        path: "/image-gallery/register",
        file: resolve(themeDir, "imageGallery/pages/register/Register.vue"),
      });
    });

    nuxt.hook("imports:dirs", (dirs) => {
      dirs.push(resolve(__dirname, "store"));
    });
  },
});
