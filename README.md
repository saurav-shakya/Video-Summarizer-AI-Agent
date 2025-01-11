# Video Summarizer AI Agent

> **Transform videos into summaries and code snippets using Gemini 2.0**

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)  
![Streamlit](https://img.shields.io/badge/streamlit-latest-red.svg)  
![License](https://img.shields.io/badge/license-MIT-green.svg)

---

## 🌟 Features
- **📹 Video Upload & Analysis**: Supports multiple formats like MP4, MOV, and AVI.
- **🤖 AI-Powered Analysis**: Leverages Google Gemini 2.0 for advanced content understanding.
- **📝 Detailed Summaries**: Extract concise and meaningful summaries from videos.
- **💻 Code Extraction**: Generate code snippets directly from coding tutorials.
- **⚡ Smart Rate Limit Handling**: Ensures smooth and uninterrupted usage.

---

## 🚀 Quick Start

### 1. Clone the Repository and Setup Environment
```bash
# Clone the repository
git clone https://github.com/saurav-shakya/Video-Summarizer-AI-Agent.git

# Navigate to the project directory
cd Video-Summarizer-AI-Agent

# Create a virtual environment
python -m venv venv

# Activate the virtual environment (Windows)
.\venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Add API Key
Create a `.env` file in the root directory and add your Google Gemini API key:
```env
GOOGLE_API_KEY=your_gemini_api_key_here
```

### 3. Run the Application
```bash
streamlit run app.py
```

---

## 📁 Project Structure
```
Video-Summarizer-AI-Agent/
├── app.py              # Main application
├── requirements.txt    # Dependencies
├── .env                # API keys
└── README.md           # Documentation
```

---

## 🛠️ Technologies Used

- **Frontend**: Streamlit - Interactive UI for video uploads and results display.
- **Backend**: Python + PhiData - Handles AI integration and processing logic.
- **AI Engine**: Google Gemini 2.0 - Powers the video summarization and code extraction.
- **Search API**: DuckDuckGo API - Enhances contextual searches and lookups.

---

## 📋 Dependencies
Ensure the following dependencies are installed (listed in `requirements.txt`):

- `streamlit`
- `google-generativeai`
- `phidata`
- `python-dotenv`
- `tenacity`
- `duckduckgo-search`

To install all dependencies:
```bash
pip install -r requirements.txt
```

---

## 🤝 How to Contribute

We welcome contributions to enhance the functionality of this project! Here's how you can contribute:

1. **Fork the Repository**: Click on the "Fork" button at the top of the repository page.
2. **Clone Your Fork**:
   ```bash
   git clone https://github.com/your-username/Video-Summarizer-AI-Agent.git
   ```
3. **Create a New Branch**:
   ```bash
   git checkout -b feature-name
   ```
4. **Make Your Changes**: Add features, fix bugs, or improve documentation.
5. **Commit Changes**:
   ```bash
   git commit -m "Describe your changes"
   ```
6. **Push to Your Fork**:
   ```bash
   git push origin feature-name
   ```
7. **Create a Pull Request**: Submit your changes for review on the original repository.

---

## 👤 Author

**Saurav Shakya**  
GitHub: [@saurav-shakya](https://github.com/saurav-shakya)

---

