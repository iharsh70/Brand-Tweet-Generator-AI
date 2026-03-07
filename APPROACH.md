# Approach Document: AI-Powered Brand Tweet Generator

## 1. Problem Understanding

Brands need consistent, on-voice social media content but manual tweet creation is time-consuming and often inconsistent across team members. This tool uses AI to analyze brand identity and generate varied, on-brand tweets that feel authentic.

## 2. How I Analysed Brand Voice

The system uses a **multi-signal inference approach**:

- **Direct signals**: User-provided tone attributes (witty, bold, professional, etc.), industry context, and campaign objectives are fed directly to the AI
- **Descriptive inference**: The brand description and product details are analyzed by GPT-4o to infer deeper voice characteristics like emotional undercurrent, communication cadence, and vocabulary patterns
- **Voice matching (optional)**: When users paste sample tweets or brand content, the AI analyzes linguistic patterns, sentence structures, vocabulary choices, and emotional tone to replicate the exact voice
- **Audience-driven calibration**: Target audience information shapes the vocabulary level, cultural references, and engagement style of generated tweets

The AI produces a **Brand Voice Summary** with:
- One-line tone description
- Inferred target audience with psychographic detail
- 3-4 content themes
- 3-4 actionable voice guidelines

## 3. Prompt Engineering Strategy

### Two-Layer Prompting
- **System prompt**: Establishes the AI persona ("elite social media strategist with 15 years experience") and defines strict output rules (280 char limit, no placeholders, varied structures)
- **User prompt**: Structured with clear `##` sections for Brand Profile, Description, Tone, Campaign Objectives, Audience, and Sample Content

### Variety Enforcement
The prompt explicitly requires:
- At least 5 different style categories across 10 tweets
- A specific mix: 2-3 with hashtags, 1-2 questions, 1-2 CTAs, 1 viral-potential tweet
- No repeated opening words or structures

### Structured Output
- Uses OpenAI's `response_format={"type": "json_object"}` to guarantee valid JSON
- Response includes metadata (style tag, character count) for each tweet
- Temperature set to 0.8 for creative variety while maintaining coherence

## 4. Tools Used

| Tool | Purpose |
|------|---------|
| **Python 3.13** | Core programming language |
| **Streamlit** | Web interface framework with built-in form handling |
| **OpenAI GPT-4o** | AI model for brand voice analysis and tweet generation |
| **python-dotenv** | Secure API key management |

## 5. Architecture

```
User Input (Streamlit Form)
    |
    v
Input Validation (required fields, min/max lengths)
    |
    v
Prompt Construction (system + user prompt with structured sections)
    |
    v
OpenAI GPT-4o API Call (temperature 0.8, JSON mode)
    |
    v
Response Parsing (JSON to Python dict)
    |
    v
UI Rendering (voice summary card + tweet grid with style tags)
```

## 6. Key Design Decisions

- **Streamlit over React/Next.js**: Faster to build, easier to deploy, sufficient for the use case
- **GPT-4o over GPT-4o-mini**: Better quality for creative writing tasks, worth the cost difference
- **JSON mode over function calling**: Simpler implementation, reliable structured output
- **No database**: Stateless design keeps the tool simple and deployment-free
- **No web scraping**: User-provided inputs ensure legal safety and give users control over brand context

## 7. Limitations & Future Improvements

- No persistent history (each generation is independent)
- Could add Twitter API integration for direct posting
- Could add A/B testing suggestions for tweet variations
- Could support multiple platforms (LinkedIn, Instagram captions)
- Could add brand preset templates for faster setup
