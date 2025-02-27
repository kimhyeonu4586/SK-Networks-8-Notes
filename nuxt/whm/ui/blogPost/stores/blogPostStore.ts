import { defineStore } from "pinia";
import { blogPostState } from "./blogPostState";
import { blogPostAction } from "./blogPostActions";

export const useBlogPostStore = defineStore("blogPostStore", {
  state: blogPostState,
  actions: blogPostAction,
});
