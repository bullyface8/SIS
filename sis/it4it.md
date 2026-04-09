# Customer Support Ticket Classifier: IT4IT Reflective Summary

## 1. Project Title
**Customer Support Ticket Classifier**

## 2. Strategy to Portfolio (S2P)

The Strategy to Portfolio value stream focuses on aligning business demand with technical prioritization. Small-to-medium enterprise e-commerce stores face the challenge of overwhelming customer support communication. Analyzing, categorizing, and drafting replies for repetitive customer messages—such as delivery questions, return requests, product inquiries, and spam—drains significant operational resources.

The objective of this project was to construct a lightweight, high-ROI AI application that directly streamlines this workflow. During the S2P phase, the strategic scope was deliberately constrained. To maximize feasibility and strictly restrict costs, the tool was scoped as a stateless frontend interface with local logging only. By intentionally omitting costly and complex features like database persistence, user authentication, CRM integration, and real-time messaging, the project prevented scope creep and yielded a stable proof-of-concept demonstrating immediate value to customer support managers.

**Why is an AI agent the right investment to solve this?**

Customer messages are written in natural language with typos, slang, emojis, and variations in phrasing. A traditional script based on if-else rules or regular expressions would require manually listing every possible wording of every question. This is impossible to maintain.

Furthermore, an AI agent (LLM) can generate context-aware reply templates, not just select from a fixed list. It can adapt tone, add politeness, and handle edge cases like sarcasm or mixed intents. A traditional script cannot do this.

Therefore, investing in an AI agent provides higher accuracy, lower maintenance, and better customer experience than a manual or rule-based approach — with API costs as low as $0.001 per request.

## 3. Requirement to Deploy (R2D)

The Requirement to Deploy stream translates business objectives into functional software. This application adopted an AI-assisted, architect-led development methodology using Google Antigravity.

The AI agent was directed through four sequential prompts.

**Prompt 1 (Base Application):**
"Create a customer support ticket classifier using Python and Streamlit. Categories: delivery, return, product_question, spam. User enters text message, clicks a button. System returns category and a reply template. Use DeepSeek API for classification. Log each request to logs.json. Add API error handling. Create requirements.txt and README.md."

The agent generated app.py, classifier.py, logger.py, requirements.txt, and README.md.

**Prompt 2 (Confidence and Token Counting):**
"Add to the existing code: Confidence score (0 to 1) for each classification. Show warning if confidence is below 0.6. Log confidence to logs.json. Add token counting using tiktoken library."

The agent added confidence scoring, low confidence warnings, and tiktoken integration.

**Prompt 3 (Copy Button):**
"Add a copy button for the reply template. Use st.code with language='text' - it has built-in copy functionality."

The agent implemented the copy button using st.code.

**Prompt 4 (API Key Fix):**
"I have a DeepSeek API key. My app crashes with error 'api_key not found' because the code tries to read from environment variable. Don't suggest I create files by hand. Make sure the key is taken from the sidebar input field in app.py. Pass this key to classify_ticket() as a parameter. In classifier.py, remove os.getenv, take the key as a function argument. After fix, run: streamlit run app.py"

The agent modified the code to accept the API key from the Streamlit sidebar instead of .env file.

All agent interactions are documented in the `antigravity_logs` folder.

## 4. Request to Fulfill (R2F)

The Request to Fulfill stream defines the functional consumption mechanism for the end-user. For this tool, service delivery is orchestrated through a self-service, browser-based Streamlit dashboard.

Customer support staff utilize a clean, highly legible interface designed for rapid ticket triage. A user pastes a raw customer message into the system and clicks the classify button. The system instantaneously returns the detected category, a confidence score, token usage, and a draft reply template. The application provides a built-in copy button, allowing the user to copy the template and paste it directly into their live chat or email client. The application also includes a fail-safe Demo Mode. If the API key is missing or network connectivity fails, the system automatically defaults to a local keyword-matching engine, guaranteeing the application never crashes during demonstration.

## 5. Detect to Correct (D2C)

The Detect to Correct stream focuses on systemic monitoring, risk management, and service resilience. Given the inherent business risks of autonomous LLM generation, the project relies on several structural safeguards.

A critical risk mitigation includes confidence scoring. Every classification includes a confidence score between 0.0 and 1.0. If the score falls below 0.6, a warning banner appears recommending manual review. Furthermore, the application includes a comprehensive logging system. Every request is logged to `logs.json` with timestamp, input text, category, confidence, template, and token counts.

For error handling, if the API key is missing or network connectivity fails, the system gracefully catches the exception and defaults to a local regex-driven heuristic engine. This guarantees the application never crashes during a demonstration, actively alerting the user via an elegant warning banner embedded in the UI.

## 6. Reflection

Transitioning from the role of a manual software developer to an AI product architect presents a distinct cognitive shift in project management. Rather than writing iterative logic loops or debugging low-level syntax errors, the architect-led approach demands exhaustive forethought prior to system execution. Directing the Antigravity agent necessitated writing highly structured prompts to establish a firm system boundary.

The primary difficulty lay in preventing the AI from independently expanding the project's scope. LLM agents naturally favor complex, heavily integrated solutions. Keeping the system actively restrained from adding database persistence, user authentication, or outbound messaging required disciplined negative prompting throughout the development cycle.

Another difficulty was API key management. The agent assumed the API key would live in a `.env` file, which violates the "no manual coding" rule. Multiple iterations were needed to redirect key input to the Streamlit sidebar UI instead.

What proved unexpectedly easy was the UI implementation. The agent demonstrated excellent knowledge of Streamlit widgets and generated a polished interface from the first iteration. Reply template generation was also automatic and required no manual refinement.

Ultimately, this methodology validates that as AI offloads the burden of raw code generation, the human engineer's fundamental value shifts entirely toward business requirement specification, architectural constraint, and systemic risk mitigation.
