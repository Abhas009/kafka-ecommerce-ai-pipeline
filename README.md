\# ⚡ Real-Time E-Commerce AI Streaming Pipeline



An end-to-end real-time data streaming and AI analytics pipeline. This project simulates live e-commerce clickstream data, streams it through Apache Kafka, stores it in DuckDB, and uses Google Gemini to provide real-time AI business insights.



\## 🏗️ Architecture

1\. \*\*Producer\*\*: Generates simulated live user events (page views, add to cart, purchases) using `Faker` and streams them to \*\*Aiven Kafka\*\*.

2\. \*\*Consumer\*\*: Reads the live stream from Kafka and writes it to a local \*\*DuckDB\*\* database.

3\. \*\*AI Dashboard\*\*: A \*\*Streamlit\*\* app that visualizes live metrics (revenue, unique users) and uses \*\*Google Gemini\*\* to analyze recent streaming events for anomalies and trends.



\## 🛠️ Tech Stack

\- \*\*Streaming\*\*: Apache Kafka (Aiven Cloud), `kafka-python`

\- \*\*Database\*\*: DuckDB

\- \*\*AI / LLM\*\*: Google Gemini (`google-generativeai`)

\- \*\*Frontend\*\*: Streamlit, Pandas

\- \*\*Data Generation\*\*: Faker



\## 🚀 How to Run Locally

1\. Clone the repo and install dependencies:

&#x20;  ```bash

&#x20;  pip install -r requirements.txt

Set up your .env file with your Aiven Kafka credentials and Gemini API key.



Download your Aiven Kafka ca.pem certificate and place it in the root directory.



Run the Producer (Terminal 1):



bash

python producer.py

Run the Consumer (Terminal 2):



bash

python consumer.py

Run the Dashboard (Terminal 3):



bash

streamlit run dashboard.py

text



\*\*3. Create `requirements.txt`\*\*

```powershell

pip freeze > requirements.txt

4\. Push to GitHub



powershell

git init

git add .

git commit -m "feat: complete real-time kafka AI streaming pipeline"

