# ⚡ Real-Time E-Commerce AI Streaming Pipeline

An end-to-end real-time data streaming and AI analytics pipeline that simulates e-commerce clickstream events, streams them through Apache Kafka, stores them in DuckDB, and uses Google Gemini to generate business insights.

## 🏗️ Architecture

1. **Producer:** Generates simulated user events, such as page views, add-to-cart actions, and purchases, using `Faker`, then streams them to Aiven Kafka.
2. **Consumer:** Reads events from Kafka and stores them in a local DuckDB database.
3. **AI Dashboard:** A Streamlit application that visualizes real-time metrics, including revenue and unique users, and uses Google Gemini to analyze recent events for potential anomalies and trends.

## 🛠️ Tech Stack

- **Streaming:** Apache Kafka (Aiven Cloud), `kafka-python`
- **Database:** DuckDB
- **AI / LLM:** Google Gemini (`google-generativeai`)
- **Frontend & Analytics:** Streamlit, Pandas
- **Data Generation:** Faker
- **Configuration:** Environment variables (`.env`)

## 📋 Prerequisites

Before getting started, ensure you have:

- Python installed
- An Aiven Kafka service with valid connection credentials
- A Google Gemini API key
- The Aiven Kafka CA certificate (`ca.pem`)

## 🚀 How to Run Locally

### 1. Clone the Repository

```bash
git clone <your-repository-url>
cd <your-repository-folder>
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables

Create a `.env` file in the project root and add your credentials using the variable names expected by your application.

```env
KAFKA_BOOTSTRAP_SERVERS=your-kafka-bootstrap-server
KAFKA_USERNAME=your-kafka-username
KAFKA_PASSWORD=your-kafka-password
GEMINI_API_KEY=your-gemini-api-key
```

**Note:** Update the variable names to match those used in `producer.py`, `consumer.py`, and `dashboard.py`. Do not commit your `.env` file or expose your credentials.

### 4. Configure the Kafka Certificate

Download the CA certificate (`ca.pem`) from your Aiven Kafka service and place it in the project root, unless your application uses a different certificate path.

### 5. Start the Producer

Open Terminal 1 and run:

```bash
python producer.py
```

The producer generates simulated e-commerce events and publishes them to Kafka.

### 6. Start the Consumer

Open Terminal 2 and run:

```bash
python consumer.py
```

The consumer reads Kafka events and writes them to DuckDB.

### 7. Launch the Dashboard

Open Terminal 3 and run:

```bash
streamlit run dashboard.py
```

Open the local URL displayed in the terminal to view the dashboard.

## 📦 Managing Dependencies

To generate or update `requirements.txt` from your active Python environment, run:

```bash
python -m pip freeze > requirements.txt
```

For reproducible installations, consider generating this file from a dedicated virtual environment containing only the project's dependencies.

## 🐙 Push to GitHub

Initialize Git and commit your project:

```bash
git init
git add .
git commit -m "feat: complete real-time Kafka AI streaming pipeline"
git branch -M main
git remote add origin <your-github-repository-url>
git push -u origin main
```

If the repository already has a Git remote configured, skip the `git remote add origin` command.

## 🔐 Security Best Practices

- Keep API keys and Kafka credentials in environment variables.
- Add `.env`, `ca.pem`, database files, and Python cache directories to `.gitignore` where appropriate.
- Never commit secrets or private certificates to a public repository.
- Store required configuration in a `.env.example` file using placeholder values only.

## 📌 Project Goals

- Simulate real-time e-commerce clickstream data.
- Build a Kafka-based event streaming workflow.
- Persist streaming events in DuckDB for analytical queries.
- Visualize live business metrics through Streamlit.
- Use an LLM to generate insights from recent event data.

