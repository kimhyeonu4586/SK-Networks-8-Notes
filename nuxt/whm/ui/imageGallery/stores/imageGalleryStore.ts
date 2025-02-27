import { defineStore } from "pinia";
import { imageGalleryState } from "./imageGalleryState";
import { imageGalleryAction } from "./imageGalleryActions";

export const useImageGalleryStore = defineStore("imageGalleryStore", {
  state: imageGalleryState,
  actions: imageGalleryAction,
});
