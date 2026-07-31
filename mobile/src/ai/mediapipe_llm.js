/**
 * 100% On-Device Gemma 2B INT4 Inference Engine for ChatLens Mobile APK.
 * Uses Google MediaPipe LLM Inference API (@google/mediapipe-tasks-genai).
 * Operates completely offline on phone NPU/GPU without internet.
 */

import { LlmInference } from '@google/mediapipe-tasks-genai';

let llmInferenceInstance = null;

export async function initializeOnDeviceLLM(modelPath = 'gemma-2b-it-gpu-int4.bin') {
  if (llmInferenceInstance) return llmInferenceInstance;

  try {
    llmInferenceInstance = await LlmInference.createFromOptions({
      baseOptions: {
        modelAssetPath: modelPath
      },
      maxTokens: 512,
      topK: 40,
      temperature: 0.7,
      randomSeed: 42
    });
    console.log('[OK] Google Gemma 2B On-Device LLM initialized successfully!');
    return llmInferenceInstance;
  } catch (error) {
    console.error('Failed to load on-device LLM:', error);
    throw error;
  }
}

export async function generateOnDeviceSummary(chatText) {
  const llm = await initializeOnDeviceLLM();
  const prompt = `You are ChatLens AI running locally on device. Summarize this WhatsApp chat:\n\n${chatText.slice(0, 2000)}\n\nProvide 3 bullet points:`;
  const response = await llm.generateResponse(prompt);
  return response;
}

export async function answerOnDeviceQuestion(chatText, question) {
  const llm = await initializeOnDeviceLLM();
  const prompt = `Context:\n${chatText.slice(0, 2500)}\n\nQuestion: ${question}\nAnswer using only the context:`;
  const response = await llm.generateResponse(prompt);
  return response;
}
