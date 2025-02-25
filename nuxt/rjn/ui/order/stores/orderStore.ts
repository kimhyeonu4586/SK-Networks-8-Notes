import { defineStore } from "pinia";
import { orderState } from "./orderState";
import { orderAction } from "./orderActions";


export const useOrderStore = defineStore('orderStore', {
    state: orderState,
    actions: orderAction,
})