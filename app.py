import streamlit as st
import json
import os
import time
import google.generativeai as genai
import anthropic
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# ─── Page Config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Brand Tweet Generator | AI-Powered",
    page_icon="🐦",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    /* Global */
    .main .block-container {
        max-width: 1100px;
        padding-top: 2rem;
    }

    /* Hero Section */
    .hero {
        text-align: center;
        padding: 3rem 1rem 2rem;
        background: linear-gradient(135deg, #667eea22 0%, #764ba222 100%);
        border-radius: 16px;
        margin-bottom: 2rem;
    }
    .hero h1 {
        font-size: 2.8rem;
        font-weight: 800;
        margin-bottom: 0.5rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .hero p {
        font-size: 1.1rem;
        color: #666;
        max-width: 600px;
        margin: 0 auto;
    }

    /* Feature badges */
    .badges {
        display: flex;
        justify-content: center;
        gap: 12px;
        margin-top: 1.5rem;
        flex-wrap: wrap;
    }
    .badge-item {
        background: white;
        border: 1px solid #e2e8f0;
        border-radius: 999px;
        padding: 6px 16px;
        font-size: 0.85rem;
        font-weight: 500;
        color: #4a5568;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }

    /* Section Headers */
    .section-header {
        font-size: 1.3rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        color: #1a202c;
    }
    .section-sub {
        font-size: 0.9rem;
        color: #718096;
        margin-bottom: 1.5rem;
    }

    /* Tweet Card */
    .tweet-card {
        background: white;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 16px;
        transition: all 0.2s;
        box-shadow: 0 1px 3px rgba(0,0,0,0.04);
    }
    .tweet-card:hover {
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        transform: translateY(-1px);
    }
    .tweet-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 12px;
    }
    .tweet-number {
        background: #edf2f7;
        color: #2d3748;
        border-radius: 50%;
        width: 28px;
        height: 28px;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        font-weight: 700;
        font-size: 0.8rem;
    }
    .tweet-content {
        font-size: 0.95rem;
        line-height: 1.6;
        color: #2d3748;
        margin-bottom: 12px;
    }
    .tweet-footer {
        display: flex;
        justify-content: space-between;
        align-items: center;
        border-top: 1px solid #f0f0f0;
        padding-top: 10px;
        font-size: 0.75rem;
        color: #a0aec0;
    }

    /* Style Tags */
    .style-tag {
        font-size: 0.7rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        padding: 3px 10px;
        border-radius: 999px;
    }
    .style-engaging { background: #ebf8ff; color: #2b6cb0; }
    .style-promotional { background: #faf5ff; color: #6b46c1; }
    .style-witty { background: #fffbeb; color: #c05621; }
    .style-informative { background: #f0fff4; color: #276749; }
    .style-inspirational { background: #fff5f5; color: #c53030; }
    .style-conversational { background: #e6fffa; color: #285e61; }
    .style-bold { background: #fee2e2; color: #991b1b; }
    .style-storytelling { background: #eef2ff; color: #4338ca; }
    .style-question { background: #ccfbf1; color: #115e59; }
    .style-announcement { background: #fff7ed; color: #c2410c; }

    /* Voice Summary Card */
    .voice-card {
        background: linear-gradient(135deg, #f8faff 0%, #f0f4ff 100%);
        border: 1px solid #d4deff;
        border-left: 4px solid #667eea;
        border-radius: 12px;
        padding: 24px;
        margin-bottom: 2rem;
    }
    .voice-card h3 {
        color: #2d3748;
        margin-bottom: 16px;
    }
    .voice-label {
        font-size: 0.7rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.8px;
        color: #a0aec0;
        margin-bottom: 4px;
    }
    .voice-value {
        font-size: 0.95rem;
        color: #2d3748;
        margin-bottom: 16px;
    }
    .theme-tag {
        background: white;
        border: 1px solid #d4deff;
        border-radius: 999px;
        padding: 4px 12px;
        font-size: 0.8rem;
        color: #4a5568;
        display: inline-block;
        margin: 3px 4px 3px 0;
    }
    .voice-bullet {
        display: flex;
        align-items: flex-start;
        gap: 8px;
        margin-bottom: 8px;
        font-size: 0.9rem;
        color: #4a5568;
        line-height: 1.5;
    }
    .check-icon {
        color: #48bb78;
        font-weight: bold;
        margin-top: 2px;
    }

    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Custom form styling */
    div[data-testid="stForm"] {
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 2rem;
        background: white;
    }
</style>
""", unsafe_allow_html=True)


# ─── Constants ─────────────────────────────────────────────────────────────────
INDUSTRIES = [
    "Technology", "Fashion & Apparel", "Food & Beverage",
    "Health & Fitness", "Finance & Banking", "Education",
    "Travel & Hospitality", "E-commerce & Retail", "Entertainment & Media",
    "Automotive", "Beauty & Cosmetics", "Real Estate",
    "SaaS & Software", "Sports", "Non-Profit & Social Impact",
    "Gaming", "Luxury & Premium", "Sustainability & Green", "Other",
]

TONE_OPTIONS = [
    "Professional", "Casual", "Witty", "Humorous", "Bold",
    "Inspirational", "Minimal", "Premium / Luxury", "Edgy",
    "Informative", "Playful", "Empathetic", "Authoritative",
    "Youthful", "Sophisticated",
]

CAMPAIGN_OBJECTIVES = [
    "Brand Awareness", "Product Launch", "Engagement & Community",
    "Promotion / Sale", "Thought Leadership", "Event Promotion",
    "Customer Education", "Seasonal / Trending",
]


# ─── Prompt Engineering ────────────────────────────────────────────────────────
SYSTEM_PROMPT = """You are an elite social media strategist and brand voice specialist with 15 years of experience crafting viral tweets for Fortune 500 companies and disruptive startups alike.

Your expertise includes:
- Deep understanding of brand voice architecture and tone calibration
- Twitter/X platform best practices and engagement psychology
- Audience segmentation and message targeting
- Creating content that balances brand consistency with creative variety

RESPONSE RULES:
1. Every tweet MUST be under 280 characters. Count carefully.
2. Tweets must feel authentic to the brand — not generic or AI-generated.
3. Each tweet must serve a distinct purpose and use a different style.
4. Include natural use of hashtags (1-2 per tweet maximum, not on every tweet).
5. Include emojis sparingly and only when appropriate for the brand tone.
6. Never use placeholder text like [Brand Name] or [Product]. Use the actual brand name or reference products naturally.
7. Vary sentence structure: mix questions, statements, calls-to-action, and storytelling.
8. Make tweets that real humans would engage with — retweet, like, or reply to.
9. Do NOT start multiple tweets with the same word or structure.
10. Capture the brand's emotional essence, not just surface-level tone.

BRAND VOICE ANALYSIS RULES:
- Analyze the provided brand information holistically.
- Infer what is NOT explicitly stated (audience psychographics, competitive positioning).
- Identify the emotional undercurrent of the brand.
- Produce 3-4 bullet points that a social media manager could use as a daily voice guide.
- Each bullet should be actionable and specific, not vague.

You MUST respond with valid JSON only. No markdown, no code blocks, no extra text. Just pure JSON."""


def build_user_prompt(brand_name, industry, campaign_objectives, brand_description,
                      brand_tone, target_audience, sample_content):
    sections = []

    sections.append("## BRAND PROFILE")
    if brand_name:
        sections.append(f"Brand Name: {brand_name}")
    sections.append(f"Industry: {industry}")

    sections.append("\n## BRAND DESCRIPTION & PRODUCTS")
    sections.append(brand_description)

    sections.append("\n## DESIRED BRAND TONE")
    sections.append(f"Tone attributes: {', '.join(brand_tone)}")

    sections.append("\n## CAMPAIGN OBJECTIVES")
    sections.append(", ".join(campaign_objectives))

    if target_audience:
        sections.append("\n## TARGET AUDIENCE")
        sections.append(target_audience)

    if sample_content:
        sections.append("\n## EXISTING BRAND CONTENT (for voice matching)")
        sections.append(sample_content)
        sections.append("\nAnalyze the above samples to understand the brand's natural voice patterns, vocabulary preferences, and communication style. Match this voice in your generated tweets.")

    sections.append("""\n## GENERATION TASK

Based on the above brand profile, perform two tasks:

TASK 1 — BRAND VOICE ANALYSIS:
Produce a brand voice summary with:
- "tone_summary": A one-line description of the brand's overall tone
- "target_audience_inferred": Who this brand speaks to, with psychographic detail
- "content_themes": array of 3-4 key content themes
- "voice_bullets": array of 3-4 actionable bullet points defining the brand voice

TASK 2 — TWEET GENERATION:
Generate exactly 10 tweets. Each tweet object must have:
- "id": sequential number (1-10)
- "content": the tweet text (max 280 chars)
- "style": one of [engaging, promotional, witty, informative, inspirational, conversational, bold, storytelling, question, announcement]
- "char_count": exact character count

Requirements:
- Use at least 5 DIFFERENT style categories across the 10 tweets
- 2-3 tweets with hashtags (1-2 hashtags each)
- 1-2 tweets with emojis (only if tone supports it)
- 1-2 tweets that are questions or conversation starters
- 1-2 tweets with a call to action
- At least 1 tweet with viral potential

Return JSON with this exact structure:
{
  "brand_voice_summary": {
    "tone_summary": "...",
    "target_audience_inferred": "...",
    "content_themes": ["...", "..."],
    "voice_bullets": ["...", "..."]
  },
  "tweets": [
    {"id": 1, "content": "...", "style": "...", "char_count": 0},
    ...
  ]
}""")

    return "\n".join(sections)


# ─── AI Generation ─────────────────────────────────────────────────────────────
def _generate_gemini(api_key, system_prompt, user_prompt):
    genai.configure(api_key=api_key)
    # Try models in order of preference; fall back if one isn't available
    models_to_try = ["gemini-2.5-flash", "gemini-2.0-flash", "gemini-1.5-flash"]
    last_error = None
    for model_name in models_to_try:
        try:
            model = genai.GenerativeModel(
                model_name=model_name,
                system_instruction=system_prompt,
                generation_config=genai.GenerationConfig(
                    temperature=0.8,
                    max_output_tokens=4000,
                    response_mime_type="application/json",
                ),
            )
            response = model.generate_content(user_prompt)
            return json.loads(response.text)
        except Exception as e:
            last_error = e
            # If it's an auth/key error, don't retry with another model
            err = str(e).lower()
            if "api key" in err or "permission" in err or "forbidden" in err:
                raise
            continue
    raise last_error


def _generate_openai(api_key, system_prompt, user_prompt):
    client = OpenAI(api_key=api_key)
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0.8,
        max_tokens=4000,
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
    )
    return json.loads(response.choices[0].message.content)


def _generate_claude(api_key, system_prompt, user_prompt):
    client = anthropic.Anthropic(api_key=api_key)
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=4000,
        temperature=0.8,
        system=system_prompt,
        messages=[{"role": "user", "content": user_prompt}],
    )
    raw = response.content[0].text
    # Strip markdown code fences if present
    if raw.strip().startswith("```"):
        raw = raw.strip().split("\n", 1)[1].rsplit("```", 1)[0]
    return json.loads(raw)


PROVIDERS = {
    "Gemini (Google)": _generate_gemini,
    "ChatGPT (OpenAI)": _generate_openai,
    "Claude (Anthropic)": _generate_claude,
}


def generate_tweets(provider, api_key, brand_name, industry, campaign_objectives,
                    brand_description, brand_tone, target_audience, sample_content):
    user_prompt = build_user_prompt(
        brand_name, industry, campaign_objectives, brand_description,
        brand_tone, target_audience, sample_content
    )

    gen_fn = PROVIDERS[provider]

    max_retries = 3
    for attempt in range(max_retries):
        try:
            return gen_fn(api_key, SYSTEM_PROMPT, user_prompt)
        except Exception as e:
            if "429" in str(e) and attempt < max_retries - 1:
                wait_time = (attempt + 1) * 30
                st.warning(f"Rate limit hit. Retrying in {wait_time} seconds... (attempt {attempt + 1}/{max_retries})")
                time.sleep(wait_time)
            else:
                raise


# ─── Render Functions ──────────────────────────────────────────────────────────
def render_voice_summary(summary):
    st.markdown('<div class="voice-card">', unsafe_allow_html=True)
    st.markdown("### 🎯 Brand Voice Analysis")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f'<div class="voice-label">TONE</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="voice-value"><strong>{summary["tone_summary"]}</strong></div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div class="voice-label">TARGET AUDIENCE</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="voice-value">{summary["target_audience_inferred"]}</div>', unsafe_allow_html=True)

    st.markdown(f'<div class="voice-label">CONTENT THEMES</div>', unsafe_allow_html=True)
    themes_html = "".join([f'<span class="theme-tag">{t}</span>' for t in summary["content_themes"]])
    st.markdown(themes_html, unsafe_allow_html=True)

    st.markdown('<br>', unsafe_allow_html=True)
    st.markdown(f'<div class="voice-label">VOICE GUIDELINES</div>', unsafe_allow_html=True)
    for bullet in summary["voice_bullets"]:
        st.markdown(f'<div class="voice-bullet"><span class="check-icon">✓</span> {bullet}</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)


def render_tweet_card(tweet):
    style = tweet.get("style", "engaging").lower()
    style_class = f"style-{style}"
    char_count = len(tweet["content"])
    over_limit = char_count > 280
    limit_warning = " ⚠️ Over limit!" if over_limit else ""
    char_color = "#e53e3e" if over_limit else "inherit"

    st.markdown(f"""
    <div class="tweet-card">
        <div class="tweet-header">
            <span class="tweet-number">{tweet["id"]}</span>
            <span class="style-tag {style_class}">{style}</span>
        </div>
        <div class="tweet-content">{tweet["content"]}</div>
        <div class="tweet-footer">
            <span style="color:{char_color}">{char_count} / 280 chars{limit_warning}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)


# ─── Hero Section ──────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <h1>Brand Tweet Generator</h1>
    <p>AI-powered tweet generation that captures your brand's unique voice, tone, and personality. Get 10 ready-to-post tweets with a single click.</p>
    <div class="badges">
        <span class="badge-item">⚡ Multi-AI Powered</span>
        <span class="badge-item">🐦 10 Unique Tweets</span>
        <span class="badge-item">📊 Brand Voice Analysis</span>
    </div>
</div>
""", unsafe_allow_html=True)


# ─── Sidebar: Provider & API Key ──────────────────────────────────────────────
with st.sidebar:
    st.markdown("### ⚙️ AI Provider Configuration")

    provider = st.selectbox(
        "Choose AI Provider",
        options=list(PROVIDERS.keys()),
        help="Select which AI model to use for tweet generation",
    )

    st.markdown("---")

    # Provider-specific API key inputs
    ENV_KEYS = {
        "Gemini (Google)": ("GEMINI_API_KEY", "GOOGLE_API_KEY"),
        "ChatGPT (OpenAI)": ("OPENAI_API_KEY",),
        "Claude (Anthropic)": ("ANTHROPIC_API_KEY",),
    }

    PLACEHOLDERS = {
        "Gemini (Google)": ("AIza...", "Get your key from [aistudio.google.com](https://aistudio.google.com/apikey)"),
        "ChatGPT (OpenAI)": ("sk-...", "Get your key from [platform.openai.com](https://platform.openai.com/api-keys)"),
        "Claude (Anthropic)": ("sk-ant-...", "Get your key from [console.anthropic.com](https://console.anthropic.com/settings/keys)"),
    }

    # Try to load from env first
    api_key = ""
    for env_var in ENV_KEYS[provider]:
        api_key = os.getenv(env_var, "")
        if api_key:
            break

    placeholder, help_text = PLACEHOLDERS[provider]

    if api_key:
        st.success(f"API key loaded from environment")
        if st.checkbox("Use a different key", key=f"override_key_{provider}"):
            override_key = st.text_input(
                "Override API Key",
                type="password",
                placeholder=placeholder,
                help=help_text,
                label_visibility="collapsed",
                key=f"api_key_override_{provider}",
            )
            if override_key:
                api_key = override_key
    else:
        st.markdown(f"**{provider} API Key**")
        api_key = st.text_input(
            "API Key",
            type="password",
            placeholder=placeholder,
            help=help_text,
            label_visibility="collapsed",
            key=f"api_key_{provider}",
        )
        st.caption(help_text)

    # Test API key button
    if api_key:
        if st.button("🔑 Test API Key", key=f"test_key_{provider}"):
            with st.spinner("Testing..."):
                try:
                    if provider == "Gemini (Google)":
                        genai.configure(api_key=api_key)
                        model = genai.GenerativeModel("gemini-2.5-flash")
                        model.generate_content("Say hello in one word.")
                    elif provider == "ChatGPT (OpenAI)":
                        client = OpenAI(api_key=api_key)
                        client.chat.completions.create(
                            model="gpt-4o-mini", max_tokens=5,
                            messages=[{"role": "user", "content": "Hi"}],
                        )
                    elif provider == "Claude (Anthropic)":
                        client = anthropic.Anthropic(api_key=api_key)
                        client.messages.create(
                            model="claude-sonnet-4-20250514", max_tokens=5,
                            messages=[{"role": "user", "content": "Hi"}],
                        )
                    st.success("API key is valid!")
                except Exception as e:
                    st.error(f"Key test failed: {e}")


# ─── Form Section ─────────────────────────────────────────────────────────────
st.markdown('<div class="section-header">Configure Your Brand</div>', unsafe_allow_html=True)
st.markdown('<div class="section-sub">Fill in the details below to generate tailored, on-brand tweets</div>', unsafe_allow_html=True)

with st.form("brand_form"):
    col1, col2 = st.columns(2)

    with col1:
        brand_name = st.text_input(
            "Brand Name",
            placeholder="e.g., Nike, Zomato, Apple",
            help="Optional but recommended",
        )

        industry = st.selectbox(
            "Industry / Category *",
            options=[""] + INDUSTRIES,
            format_func=lambda x: "Select an industry..." if x == "" else x,
        )

        custom_industry = ""
        if industry == "Other":
            custom_industry = st.text_input("Specify your industry")

        campaign_objectives = st.multiselect(
            "Campaign Objectives * (select 1-3)",
            options=CAMPAIGN_OBJECTIVES,
            max_selections=3,
            help="What do you want these tweets to achieve?",
        )

    with col2:
        brand_description = st.text_area(
            "Tell us about your brand and products *",
            placeholder="Describe your brand, key products/services, what makes you unique, and any current campaigns or initiatives...",
            height=120,
            max_chars=1000,
            help="The more detail you provide, the better the results",
        )

        brand_tone = st.multiselect(
            "Brand Tone & Personality * (select 1-4)",
            options=TONE_OPTIONS,
            max_selections=4,
            help="Select the tone attributes that best describe your brand",
        )

        target_audience = st.text_input(
            "Target Audience",
            placeholder="e.g., Gen Z fitness enthusiasts, working professionals aged 25-40",
            help="Optional - helps AI tailor the messaging",
        )

    with st.expander("🔧 Advanced: Voice Matching (Optional)"):
        sample_content = st.text_area(
            "Sample Tweets or Brand Content",
            placeholder="Paste 2-3 sample tweets or brand messages to help match your voice...",
            height=100,
            max_chars=1500,
            help="Providing examples helps the AI match your exact tone",
        )

    submitted = st.form_submit_button(
        "✨ Generate 10 On-Brand Tweets",
        use_container_width=True,
        type="primary",
    )


# ─── Validation & Generation ──────────────────────────────────────────────────
if submitted:
    # Validate required fields
    errors = []
    if not industry:
        errors.append("Please select an industry.")
    if not campaign_objectives:
        errors.append("Please select at least one campaign objective.")
    if not brand_description or len(brand_description.strip()) < 20:
        errors.append("Please provide at least 20 characters in the brand description.")
    if not brand_tone:
        errors.append("Please select at least one brand tone.")
    if not api_key:
        errors.append("Please provide your API key in the sidebar.")

    if errors:
        for error in errors:
            st.error(error)
    else:
        # Use custom industry if "Other" selected
        final_industry = custom_industry if industry == "Other" and custom_industry else industry

        with st.spinner("🧠 Analyzing brand voice and generating tweets... This takes about 10-15 seconds."):
            try:
                result = generate_tweets(
                    provider=provider,
                    api_key=api_key,
                    brand_name=brand_name,
                    industry=final_industry,
                    campaign_objectives=campaign_objectives,
                    brand_description=brand_description,
                    brand_tone=brand_tone,
                    target_audience=target_audience,
                    sample_content=sample_content,
                )

                st.success("Tweets generated successfully!")

                # Store result in session state for persistence
                st.session_state["result"] = result
                st.session_state["brand_name"] = brand_name

            except json.JSONDecodeError:
                st.error("Failed to parse AI response. Please try again.")
            except Exception as e:
                error_msg = str(e).lower()
                raw_msg = str(e)
                if "429" in raw_msg or "quota" in error_msg or "rate limit" in error_msg:
                    st.error(f"**Rate limit / quota exceeded** for {provider}. Switch to a different provider in the sidebar or wait a few minutes.")
                elif "api key" in error_msg or "api_key" in error_msg or "permission" in error_msg or "forbidden" in error_msg or "authentication" in error_msg or "unauthorized" in error_msg:
                    st.error(f"**Invalid or unauthorized API key** for {provider}. Please check your key in the sidebar.\n\nError: `{raw_msg}`")
                elif "billing" in error_msg or "payment" in error_msg or "insufficient" in error_msg or "exceeded" in error_msg:
                    st.error(f"**Billing issue** with {provider}. Your account may need a payment method or plan upgrade.\n\nError: `{raw_msg}`")
                elif "not found" in error_msg or "model" in error_msg:
                    st.error(f"**Model not available** for your {provider} account. This may require a paid plan.\n\nError: `{raw_msg}`")
                else:
                    st.error(f"**Generation failed** ({provider}): {raw_msg}")


# ─── Display Results ───────────────────────────────────────────────────────────
if "result" in st.session_state:
    result = st.session_state["result"]
    brand = st.session_state.get("brand_name", "Brand")

    st.markdown("---")
    st.markdown(f'<div class="section-header">Results{" for " + brand if brand else ""}</div>', unsafe_allow_html=True)

    # Brand Voice Summary
    if "brand_voice_summary" in result:
        render_voice_summary(result["brand_voice_summary"])

    # Tweet Cards
    if "tweets" in result:
        st.markdown(f'<div class="section-header">Generated Tweets ({len(result["tweets"])})</div>', unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        for i, tweet in enumerate(result["tweets"]):
            with (col1 if i % 2 == 0 else col2):
                render_tweet_card(tweet)

        # Copy all tweets button
        st.markdown("---")
        all_tweets_text = "\n\n".join(
            [f"{t['id']}. [{t.get('style', 'tweet')}] {t['content']}" for t in result["tweets"]]
        )
        st.download_button(
            label="📋 Download All Tweets as Text",
            data=all_tweets_text,
            file_name=f"{'_'.join(brand.lower().split()) if brand else 'brand'}_tweets.txt",
            mime="text/plain",
            use_container_width=True,
        )


# ─── Footer ───────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown(
    '<div style="text-align: center; color: #a0aec0; font-size: 0.85rem; padding: 1rem 0;">'
    'Built with Streamlit & Python — Powered by Gemini, ChatGPT & Claude'
    '</div>',
    unsafe_allow_html=True,
)
