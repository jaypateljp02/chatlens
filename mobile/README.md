# 📱 ChatLens AI - Mobile Android APK (100% On-Device Gemma 2B)

This is the standalone **Android APK codebase** for ChatLens AI.
It runs **Google Gemma 2B INT4** locally on the phone's NPU/GPU using Google MediaPipe LLM Inference API and `sqlite-vec` for 100% offline mobile privacy.

---

## 🛠️ Step-by-Step Android APK Compilation Guide

### 1. Requirements
- Node.js 18+ & npm
- Android Studio Hedgehog / Iguana or higher
- Android SDK 34 (Android 14) with NDK 26
- Java Development Kit (JDK 17)

### 2. Download the Quantized Gemma 2B Model File
1. Download `gemma-2b-it-gpu-int4.bin` (~1.3 GB) from Kaggle / Hugging Face.
2. Place the file inside `mobile/android/app/src/main/assets/gemma-2b-it-gpu-int4.bin`.

### 3. Install Dependencies & Build APK
```bash
cd mobile
npm install
cd android
./gradlew assembleRelease
```

### 4. Locate Compiled APK File
The compiled APK file will be located at:
`mobile/android/app/build/outputs/apk/release/app-release.apk`

Transfer `app-release.apk` to any Android phone and install!
