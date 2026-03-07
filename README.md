# Brand Tweet Generator - AI-Powered Social Media Content

An AI-powered tool that analyzes brand voice and generates 10 on-brand tweets with variety in style, tone, and purpose. Supports multiple AI providers.

---

## Features

- **Multi-AI Provider Support** — Choose between **Gemini (Google)**, **ChatGPT (OpenAI)**, or **Claude (Anthropic)**
- **Brand Voice Analysis** — AI infers tone, target audience, and content themes from your brand description
- **10 Unique Tweets** — Each tweet uses a different style (witty, promotional, engaging, informative, etc.)
- **Test API Key** — Verify your API key works before generating
- **Copy & Download** — Download all 10 tweets as a text file
- **Voice Matching** — Optional sample content input for precise tone replication
- **Smart Model Fallback** — Gemini automatically tries `2.5-flash` → `2.0-flash` → `1.5-flash`

---

## Tech Stack

| Component | Technology |
|-----------|-----------|
| Frontend | **Streamlit** (Python web framework) |
| AI Providers | **Google Gemini 2.5 Flash**, **OpenAI GPT-4o-mini**, **Anthropic Claude Sonnet** |
| Language | **Python 3.10+** |
| Config | **python-dotenv** for environment variables |

---

## Requirements

### System Requirements
- **Python** 3.10 or higher
- **pip** (Python package manager)
- An API key from at least one provider:
  - [Google AI Studio](https://aistudio.google.com/apikey) (Gemini) — **Free tier available**
  - [OpenAI Platform](https://platform.openai.com/api-keys) (ChatGPT) — Requires billing
  - [Anthropic Console](https://console.anthropic.com/settings/keys) (Claude) — Requires billing

### Python Dependencies
| Package | Version | Purpose |
|---------|---------|---------|
| `streamlit` | 1.55.0 | Web UI framework |
| `google-generativeai` | 0.8.5 | Google Gemini API |
| `openai` | >=1.0.0 | OpenAI ChatGPT API |
| `anthropic` | >=0.40.0 | Anthropic Claude API |
| `python-dotenv` | 1.1.1 | Load `.env` file |

---

## Quick Start

### 1. Clone the repository
```bash
git clone <repo-url>
cd intership
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Set up API keys (optional)
Copy the example env file and add your keys:
```bash
cp .env.example .env
```

Edit `.env`:
```env
# At least one key is required. Get free Gemini key from https://aistudio.google.com/apikey
GEMINI_API_KEY=your-gemini-api-key-here

# Optional — requires OpenAI billing
OPENAI_API_KEY=your-openai-api-key-here

# Optional — requires Anthropic billing
ANTHROPIC_API_KEY=your-anthropic-api-key-here
```

> **Tip:** You can skip this step and enter API keys directly in the app sidebar.

### 4. Run the app
```bash
python -m streamlit run app.py
```

The app will open at **http://localhost:8501**

### Alternative: Using the batch file (Windows)
```bash
run.bat
```

---

## How to Use

1. **Select AI Provider** — Choose Gemini, ChatGPT, or Claude in the sidebar
2. **Enter API Key** — Paste your key in the sidebar (or load from `.env`)
3. **Test API Key** — Click "Test API Key" to verify it works
4. **Fill Brand Details:**
   - Brand Name (e.g., `Zomato`)
   - Industry (e.g., `Food & Beverage`)
   - Brand Description (min 20 characters)
   - Brand Tone (e.g., `Witty`, `Bold`, `Playful`)
   - Campaign Objectives (e.g., `Product Launch`)
   - Target Audience (optional)
5. **Generate** — Click "Generate 10 On-Brand Tweets"
6. **Download** — Save results as a text file

### Example Input (Zomato)
| Field | Value |
|-------|-------|
| Brand Name | `Zomato` |
| Industry | `Food & Beverage` |
| Description | `India's leading food delivery platform. Known for witty social media, quirky push notifications, and bold marketing.` |
| Tone | `Witty`, `Bold`, `Conversational`, `Playful` |
| Objectives | `Product Launch`, `Engagement & Community` |
| Audience | `Urban millennials and Gen Z aged 18-35, food lovers` |

---

## Project Structure

```
intership/
├── app.py                    # Main Streamlit application (all logic)
├── requirements.txt          # Python dependencies
├── .env                      # API keys (not committed to git)
├── .env.example              # API key template
├── run.bat                   # Windows batch file to run the app
├── .gitignore                # Git ignore rules
├── .streamlit/
│   └── config.toml           # Streamlit theme configuration
├── examples/
│   ├── nike-output.md        # Example output for Nike
│   └── zomato-output.md      # Example output for Zomato
├── APPROACH.md               # Detailed approach & design decisions
└── README.md                 # This file
```

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| `streamlit: command not found` | Use `python -m streamlit run app.py` instead |
| `API key loaded from environment` but errors | Check "Use a different key" checkbox in sidebar to override |
| `TypeError: Failed to fetch dynamically imported module` | Hard refresh browser (`Ctrl+Shift+R`) or try a different port: `python -m streamlit run app.py --server.port 8502` |
| `Rate limit / quota exceeded` | Wait a few minutes or switch to a different AI provider |
| `Billing issue` | Your API account needs a payment method. Gemini free tier is recommended |
| Blank page after generation | Scroll down — results appear below the form |

---

## Example Brands Tested

- **Nike** — Bold, inspirational, athletic brand voice
- **Zomato** — Witty, humorous, casual Indian food delivery brand

See the `examples/` folder for sample outputs.

---

## License

This project was built as an internship assignment.
