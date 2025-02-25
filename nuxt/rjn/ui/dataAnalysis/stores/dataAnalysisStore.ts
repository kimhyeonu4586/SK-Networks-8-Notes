import { defineStore } from "pinia";
import { dataAnalysisState } from "./dataAnalysisState";
import { dataAnalysisAction } from "./dataAnalysisActions";

export const useDataAnalysisStore = defineStore('dataAnalysisStore', {
    state: dataAnalysisState,
    actions: dataAnalysisAction,
})