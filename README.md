# Voice Assistant - Jarvis AI

A Python-based voice assistant designed to provide an interactive voice-driven experience using modern AI technologies.

## Overview

This project explores the development of a personal AI voice assistant capable of receiving voice input, processing user requests, and providing responses through an interactive assistant interface.

The project was built as a hands-on exploration of voice AI, API integration, and conversational AI systems.

## Key Features

* Voice-based interaction
* AI-powered conversational responses
* Python-based implementation
* Integration with Google Gemini API
* Real-time voice assistant capabilities
* Environment variable support for API credentials
* Model availability checking

## Technologies Used

* Python
* Google Gemini API
* LiveKit
* Speech Recognition
* Text-to-Speech
* Python-dotenv

## Project Structure

```text
VOICE-ASSISTANT/
│
├── free_jarvis.py       # Main voice assistant implementation
├── check_models.py      # Utility for checking available AI models
├── README.md            # Project documentation
├── .gitignore           # Prevents sensitive files from being committed
└── .env                 # Local environment variables (not committed)
```

## How It Works

```text
Voice Input
     |
     v
Speech Recognition
     |
     v
AI Processing
     |
     v
Google Gemini
     |
     v
Generated Response
     |
     v
Voice Output
```

The assistant receives user input through voice interaction, processes the request using an AI model, and generates a conversational response.

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/Hari150806/VOICE-ASSISTANT.git
cd VOICE-ASSISTANT
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

### 3. Install dependencies

If the project contains a `requirements.txt` file:

```bash
pip install -r requirements.txt
```

If it does not, install the dependencies required by the current implementation.

### 4. Configure environment variables

Create a `.env` file in the project root and add your API credentials.

```env
GEMINI_API_KEY=your_api_key_here
```

Do not commit your `.env` file or expose API keys publicly.

### 5. Run the assistant

```bash
python free_jarvis.py
```

## Security

API credentials are stored through environment variables rather than directly inside the source code.

The `.gitignore` file is used to prevent sensitive configuration files from being committed to the repository.

## Future Improvements

Potential improvements include:

* Better natural language understanding
* More reliable voice interaction
* Additional AI tools and capabilities
* Improved error handling
* More integrations with external applications
* Improved conversational memory
* A more polished user interface


