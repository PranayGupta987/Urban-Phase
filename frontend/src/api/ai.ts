import { apiPost } from "./client";

export const getPrediction = (payload: any) => apiPost("/predict", payload);

export const runSimulation = (payload: any) => apiPost("/simulate", payload);
