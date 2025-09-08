# 🚀 E2E Job Recommender System

Welcome to the **E2EJobRecommender** repository! This project is a robust, end-to-end job recommendation system designed to match users with the most relevant job opportunities using advanced algorithms and scalable infrastructure.

## 🌟 Features

- **Personalized Job Recommendations:** Tailors job suggestions to each user's profile, preferences, and skillset.
- **End-to-End Pipeline:** From data ingestion and preprocessing to model training and recommendation serving.
- **Modular Architecture:** Organized codebase with clear separation of concerns for easy customization and extension.
- **Dockerized Deployment:** Easily spin up the system using Docker and Docker Compose for consistent environments.
- **Interactive Notebooks:** Jupyter notebooks for exploratory data analysis, model evaluation, and prototyping.
- **Logging & Artifacts:** Comprehensive logging and artifact management for experiment tracking and debugging.

## 🏗️ Project Structure

```
├── app/                # Application logic (APIs, interfaces)
├── artifacts/          # Model artifacts, checkpoints, etc.
├── logs/               # Log files
├── notebooks/          # Jupyter notebooks for prototyping & EDA
├── src/                # Source code for core modules
├── main.py             # Main entry point to launch the server
├── requirements.txt    # Python dependencies
├── docker-compose.yaml # Docker Compose configuration
├── Dockerfile          # Docker image build file
├── setup.py, pyproject.toml # Packaging and build files
```

## 🚦 Getting Started

### 1. Prerequisites

- Python (version as per `.python-version`)
- Docker & Docker Compose

### 2. Installation

Clone the repository:
```bash
git clone https://github.com/Kra09-kp/E2EJobRecommender.git
cd E2EJobRecommender
```

Install dependencies:
```bash
pip install -r requirements.txt
```

### 3. Running the Server

Start the application using MCP:
```bash
mcp dev main.py
```
- This will launch the job recommender server.
- Stop the server with `Ctrl+C`.

> **Tip:** If you encounter a timeout error while fetching jobs, increase the request timeout value in the server UI's configuration section.

Or, use Docker Compose:
```bash
docker-compose up --build
```

## 📝 Notebooks

Check the `notebooks/` directory for sample data analysis, model experiments, and prototyping.

## 📄 License

This project is licensed under the MIT License.

---

Built with ❤️ by [Kra09-kp](https://github.com/Kra09-kp)
