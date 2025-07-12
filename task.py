import os
import time
import threading
import warnings
import requests
import re
from flask import Flask, request, jsonify, render_template
from ddgs import DDGS
from llama_cpp import Llama

warnings.simplefilter("ignore", ResourceWarning)

# === LLM Setup ===
llm = Llama(
    model_path="Mistral-7B-Instruct-v0.3.Q4_K_M.gguf",  # Replace with your model path
    n_ctx=4096,
    n_threads=os.cpu_count(),
    verbose=False
)

app = Flask(__name__)

# === Reverse Geocoding ===
def reverse_geocode(lat, lon):
    url = "https://nominatim.openstreetmap.org/reverse"
    params = {"lat": lat, "lon": lon, "format": "json", "zoom": 10, "addressdetails": 1}
    headers = {"User-Agent": "GeoApp/1.0"}
    r = requests.get(url, params=params, headers=headers)
    data = r.json()
    address = data.get("address", {})
    return {
        "city": address.get("city") or address.get("town") or address.get("village"),
        "state": address.get("state"),
        "country": address.get("country")
    }

# === DuckDuckGo Search ===
def search_duckduckgo(query, max_results=5):
    results = []
    try:
        with DDGS() as ddgs:
            for r in ddgs.text(query, max_results=max_results):
                results.append({
                    "title": r["title"],
                    "snippet": r["body"]
                })
    except Exception as e:
        print("DDG Search Error:", e)
    return results

# === Prompt Engineering ===
def format_prompt(user_query, search_results, location):
    identity = """You are Sera, a friendly and intelligent AI assistant developed by Sejal.
Always greet warmly and provide helpful, concise, and polite answers. Do not include URLs or say "at this link". If needed, just mention the platform (e.g., JustDial, Zomato)."""

    location_note = f"The user is located in {location}." if location else "The user's location is unknown."

    context = "\n".join(
        f"{i+1}. {item['title']}\n{item['snippet']}"
        for i, item in enumerate(search_results)
    )

    return f"""{identity}
{location_note}

Answer the following user question using the search results. Avoid hyperlinks and phrases like "click here" or "visit the link".

User Query:
{user_query}

Search Results:
{context}

Sera's Response:"""

# === LLM Response ===
def get_summary_from_llm(prompt):
    output = llm(prompt, max_tokens=512, stop=["###"])
    return output["choices"][0]["text"].strip()

# === Routes ===
@app.route('/')
def index():
    return render_template("task.html")

@app.route('/get_location_info', methods=['POST'])
def get_location_info():
    data = request.json
    lat = data.get("latitude")
    lon = data.get("longitude")
    if not lat or not lon:
        return jsonify({"error": "Missing lat/lon"}), 400
    location = reverse_geocode(lat, lon)
    return jsonify(location)

@app.route('/ask', methods=['POST'])
def ask():
    data = request.json
    query = data.get("query", "").strip().lower()
    location = data.get("location", "")

    if not query:
        return jsonify({"error": "Empty query"}), 400

    # === Handle greetings ===
    greetings = ["hi", "hello", "hey", "namaste", "good morning", "good evening"]
    if query in greetings:
        return jsonify({
            "answer": "Hello! 👋 I'm Sera, your smart assistant created by Sejal. How can I assist you today?"
        })

    # === Replace "near me" with actual location ===
    if "near me" in query and location:
        query = query.replace("near me", f"in {location}")

    # === Get search results ===
    results = search_duckduckgo(query)

    # === Format prompt ===
    prompt = format_prompt(query, results, location)

    # === LLM response ===
    answer = get_summary_from_llm(prompt)

    # === Clean the output ===
    answer = re.sub(r'https?://[^\s]+', '', answer)
    answer = re.sub(r'(?i)(at|on|visit|see)\s+(this|that)?\s*(link|url|website)?[\.:]?', '', answer)

    return jsonify({"answer": answer})

# === Start Server ===
if __name__ == "__main__":
    import webbrowser
    threading.Thread(target=lambda: app.run(debug=False, use_reloader=False)).start()
    time.sleep(1)
    webbrowser.open("http://127.0.0.1:5000")
