# AI Business Report Generator

An end-to-end analytics project that transforms raw sales data into business KPIs, structured insights, and AI-generated executive reports using Python, Streamlit, and a local Ollama model.

## Project Overview

This project was built to simulate a realistic business analytics workflow that combines traditional data analysis with modern AI-assisted reporting.

The application takes sales data as input, processes and analyzes it in Python, identifies business-relevant patterns such as category performance and revenue trends, and then converts those findings into an executive-style report using a locally hosted language model.

The result is a complete analytics pipeline that demonstrates:

- data loading and cleaning
- KPI generation
- category and regional analysis
- weekly and monthly trend analysis
- automated insight generation
- local LLM-based business reporting
- interactive dashboard development with Streamlit

## Why this project matters

Many business teams do not need raw tables or technical notebooks. They need:

- clear KPIs
- trend monitoring
- understandable summaries
- fast executive reporting

This project addresses exactly that gap by combining analytics and AI in a practical business use case.

## Tech Stack
Python
Pandas
NumPy
Streamlit
Requests
Ollama
Local LLM model (llama3.2:1b)

## Why Ollama was used instead of a cloud API

This project uses **Ollama** for local LLM inference instead of a hosted API such as OpenAI.

That decision was made intentionally for several reasons:

### No API key required

A local setup makes the project easier to run and reproduce without requiring external credentials or paid API access.

### Better portfolio accessibility

Recruiters, hiring managers, and other developers can understand the architecture without needing access to a private API account.

### Lower operational dependency

Using a local model reduces dependency on external cloud services during development.

### Stronger engineering story

Running a local LLM shows practical understanding of modern AI tooling beyond simple API calls. It demonstrates how analytics applications can integrate with local inference workflows.

### Privacy-friendly architecture

A local model is also a useful design choice for scenarios where sensitive internal business data should not be sent to external services.

## Core Features

- Load and clean raw sales data from CSV files
- Calculate core business KPIs
- Analyze revenue by product category
- Analyze revenue by region
- Generate weekly revenue trends
- Generate monthly revenue trends
- Translate analytical output into structured business insights
- Generate executive-style AI business reports with a local LLM
- Visualize metrics and trends in a Streamlit dashboard
- Upload custom CSV files directly in the app
- Filter analysis by date range, region, and category
- Download filtered datasets and generated reports

## Example Use Case

A business stakeholder uploads a sales dataset and wants a quick performance summary.

The application can answer questions such as:

- Which category generated the highest revenue?
- Which region performed best?
- Did revenue increase or decline this month?
- What are the most important business trends?
- Can these findings be summarized into a short executive report?

## Project Architecture


Raw Sales Data
    ↓
Data Loading
    ↓
Data Cleaning
    ↓
KPI Calculation
    ↓
Category and Region Analysis
    ↓
Weekly and Monthly Trend Analysis
    ↓
Structured Business Insights
    ↓
Local LLM Report Generation via Ollama
    ↓
Interactive Streamlit Dashboard


## Repo structure 

ai-business-report-generator/

│

├── app/

│   └── streamlit_app.py

│

├── data/

│   └── superstore_sales.csv

│

├── outputs/

│   └── .gitkeep

│

├── src/

│   ├── analysis.py

│   ├── data_cleaning.py

│   ├── data_loader.py

│   ├── insight_engine.py

│   └── llm_report.py

│

├── .gitignore

├── main.py

├── README.md

└── requirements.txt


## How the pipeline works

### Data loading

The project begins by loading a sales dataset from CSV format.

### Data cleaning

Column names are standardized, date fields are converted into datetime format, and invalid or incomplete records are removed where necessary.

### KPI generation

The analytics layer calculates core business metrics such as:

total revenue
total profit
total number of orders
average order value

### Revenue analysis

Revenue is aggregated across business dimensions such as:

category
region


### Trend analysis

The application resamples sales data over time to calculate:

weekly revenue
weekly growth rates
monthly revenue
monthly growth rates

### Insight generation

The structured insight layer converts numerical results into readable business statements, for example:

weekly revenue increased by 5.2%
technology is the top performing category
the west region generated the highest revenue


### AI report generation

These structured insights are passed to a local language model through Ollama.
The model then creates a short executive report designed for business stakeholders.

### Dashboard

All outputs are displayed in a Streamlit dashboard that supports filtering, CSV upload, data preview, and report download.
