# 🤖 Loopie™: Your Mindful Companion

**Loopie** is a personal observability tool designed for software engineers. It monitors your development workflow in real-time to identify deep work states, quantify context-switching, and mitigate burnout risks in high-performance environments.

## 🚀 Key Features
- **Silent Capture:** Background window activity monitoring using `pygetwindow` without disrupting user workflow.
- **Context Switching Analysis:** Automatic identification of context shifts and their estimated impact on cognitive focus.
- **Smart Categorization:** Application classification into *Productive*, *Communication*, and *Distraction* tiers through keyword-based title analysis.
- **Session Dashboards:** Real-time CLI dashboard displaying active metrics, top applications, and current mental state.
- **Daily Wrap-up:** Automated generation of end-of-day summaries for long-term mental health trend analysis.

## 🛠️ Technical Architecture
The project is built on a modular architecture to ensure scalability (e.g., future biometric data integration):

- **Collector (Ingestion):** Multi-threaded engine for seamless telemetry data capture.
- **Storage (Persistence):** Lightweight relational database using `SQLite`.
- **Analyzer (Business Logic):** Processing engine that transforms raw timestamps into duration metrics and cognitive state definitions.
- **Interface (Visualization):** Dynamic CLI for immediate feedback and session reporting.

## 🧠 The Mental Health Approach

This project stems from the need to visualize cognitive load in software engineering. By measuring "Context Switching," users can identify burnout patterns before they escalate, allowing for intentional interventions such as planned breaks and task re-prioritization.

## 🛠️ Installation & Usage

1. Clone the repository.

2. Install dependencies: pip install pygetwindow.

3. Run the core system: python main.py.

4. To exit and generate your daily summary, press Ctrl+C.

© 2026 Daniela Ruiz
Loopie™ is an open-source initiative to bridge the gap between systems observability and developer wellbeing.