# WhatsApp Chat Analyzer

An interactive WhatsApp chat analytics dashboard built with **Python and Streamlit** that transforms exported WhatsApp conversations into meaningful communication insights through statistics, timelines, activity analysis, word frequency, WordClouds, and emoji analytics.

## 🚀 Live Demo

👉 **Live Application:**  
https://whatsapp-chat-analyzer-dev.streamlit.app/

👉 **GitHub Repository:**  
https://github.com/DevSavaliya/Whatsapp-Chat-Analyzer

---

## 📌 Project Overview

WhatsApp conversations contain valuable information about communication patterns, participation, activity levels, commonly used words, shared links, media, and emojis.

However, raw WhatsApp chat exports are difficult to analyze manually.

The **WhatsApp Chat Analyzer** solves this problem by converting an exported WhatsApp `.txt` chat file into an interactive analytics dashboard.

Users can upload their WhatsApp chat export, select either the complete conversation or an individual participant, and explore different aspects of the conversation through visualizations and statistics.

The application is designed to make conversational data analysis simple, interactive, and accessible without requiring users to write code.

---

## 🎯 Project Objectives

The main objectives of this project are to:

- Convert unstructured WhatsApp chat exports into structured data.
- Provide an easy-to-use analytics dashboard.
- Analyze communication patterns over time.
- Compare participant activity.
- Identify frequently used words and emojis.
- Visualize message activity through charts.
- Provide user-specific analysis.
- Demonstrate practical application of Python data analysis and visualization.
- Deploy the application as an accessible web application using Streamlit Community Cloud.

---

## ✨ Features

### 📊 Overall Statistics

The dashboard provides key conversation statistics such as:

- Total number of messages
- Total number of words
- Total media files shared
- Total links shared

These metrics provide a quick overview of the selected conversation.

---

### 👤 User-Specific Analysis

Users can select:

- **Overall** — analyze the complete conversation.
- **Individual participant** — analyze messages from a specific participant.

This allows users to explore individual communication behavior within a group or personal conversation.

---

### 📈 Monthly Timeline

Visualizes the number of messages exchanged during each month.

This helps identify:

- Highly active months
- Low-activity periods
- Long-term communication trends

---

### 📅 Daily Timeline

Displays message activity by date.

This makes it easier to identify:

- Highly active days
- Communication patterns
- Changes in activity over time

---

### 🗓️ Activity Map

The application analyzes activity by:

- Day of the week
- Month

This helps identify when conversations are most active.

For example, users can determine whether a conversation is more active during weekdays or weekends.

---

### 👥 Most Busy Users

For group conversations, the application identifies participants who sent the highest number of messages.

This provides an overview of participant engagement within the conversation.

---

### ☁️ WordCloud

The application generates a visual WordCloud based on frequently used words.

The WordCloud provides a quick visual representation of the main topics and vocabulary appearing in the conversation.

---

### 🔤 Most Common Words

The application calculates the most frequently used words while filtering common stopwords.

This provides a more meaningful representation of frequently occurring conversational terms.

---

### 😀 Emoji Analysis

The application analyzes emoji usage and displays:

- Most frequently used emojis
- Emoji frequency
- Top 10 emojis

This provides an additional perspective on communication style and emotional expression.

---

### 🔗 Link Analysis

The application identifies links shared within the conversation and provides the total number of links detected.

---

### 📱 Media Analysis

The application detects WhatsApp messages containing media placeholders and calculates the amount of media shared.

---

## 🔄 Application Workflow

The application follows the following general workflow:

```text
WhatsApp Chat Export
        │
        ▼
Upload .txt File
        │
        ▼
Message Preprocessing
        │
        ▼
Date & User Extraction
        │
        ▼
Structured Pandas DataFrame
        │
        ▼
Data Analysis
        │
        ├── Message Statistics
        ├── User Activity
        ├── Monthly Timeline
        ├── Daily Timeline
        ├── Activity Analysis
        ├── Common Words
        ├── WordCloud
        └── Emoji Analysis
        │
        ▼
Interactive Streamlit Dashboard