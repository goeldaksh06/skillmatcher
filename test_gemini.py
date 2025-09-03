import google.generativeai as genai

# 🔑 Replace with your actual Gemini API key from Google AI Studio
genai.configure(api_key="AIzaSyBXOpwC7XwUrQgCOCrnjTH5EApfTAmEfVE")

# Use Gemini Pro for text tasks
model = genai.GenerativeModel("gemini-1.5-flash")

# Ask it to generate a question
response = model.generate_content("Generate 1 interview question for Python.")

print("AI Interviewer:", response.text)
