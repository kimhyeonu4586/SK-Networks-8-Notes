import { defineStore } from "pinia";
import { paymentsAction } from "./paymentsActions";
import { paymentsState } from "./paymentsState";

export const usePaymentStore = defineStore('paymentStore', {
    state: paymentsState,
    actions: paymentsAction,
})
