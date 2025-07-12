# AT-chatbot-1
A Flask backend  Llama-based LLM (Mistral 7B GGUF via llama_cpp)  DuckDuckGo API for real-time retrieval  Reverse geolocation using OpenStreetMap  A clean, interactive chat-style UI  Location auto-detection via browser  Prompt engineering for response formatting




# 🗺️ Sera – Smart Local Discovery Chatbot 🤖

**Sera** is a smart, friendly AI chatbot that helps users discover hyperlocal services, businesses, and events using natural language queries — powered by an open-source LLM, real-time web search, and live location detection.

This project was built for the **LocalConnect AI Evaluation Task**.

---

## 🎯 Objective

To build a working prototype of a **local discovery chatbot** that:
- Understands user queries in natural language
- Retrieves real-time search results using DuckDuckGo
- Uses a local LLM (Mistral 7B) to generate helpful responses
- Detects the user’s location and adds context
- Delivers answers through a clean, chat-style UI

---


---

## ⚙️ Tech Stack

| Component       | Technology                                 |
|----------------|---------------------------------------------|
| Backend         | Python + Flask                             |
| LLM             | `llama.cpp` (Mistral 7B Instruct GGUF)     |
| Search API      | DuckDuckGo Search via `ddgs`               |
| Geolocation     | OpenStreetMap Nominatim Reverse Geocoding  |
| Frontend        | HTML + CSS + Vanilla JavaScript            |
| UI Type         | Chat-style interface                       |

---

## 🧠 Features

- ✅ Natural language understanding
- ✅ Real-time DuckDuckGo web search
- ✅ LLM-based response generation (offline with Mistral 7B)
- ✅ Auto-location detection using browser + reverse geocoding
- ✅ Clean, interactive chat UI
- ✅ Prompt-engineered responses (no hyperlinks or ads)
- ✅ Easy deployment (local + browser access)

---



**How to Run Locally
Install Python dependencies:

bash
Copy
Edit
pip install flask ddgs requests llama-cpp-python
Download the Mistral-7B GGUF model:

You will need a quantized .gguf version of Mistral-7B to run this locally using llama.cpp.
🔗 Download it from TheBloke/Mistral-7B-v0.1-GGUF on Hugging Face
For example, you can use the file:
Mistral-7B-Instruct-v0.1.Q4_K_M.gguf

Place the downloaded .gguf file in the project directory **
```bash

