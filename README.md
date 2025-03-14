# Mental Health AI Voice Assistant

![license](https://img.shields.io/badge/license-MIT-blue.svg)
![version](https://img.shields.io/badge/version-1.0.0-brightgreen.svg)
![python](https://img.shields.io/badge/python-3.10+-blue.svg)
![flask](https://img.shields.io/badge/flask-2.0+-lightgrey.svg)
![react](https://img.shields.io/badge/react-18.0+-61DAFB.svg)
![openai](https://img.shields.io/badge/openai-API-green.svg)
![livekit](https://img.shields.io/badge/livekit-latest-red.svg)
![sqlite](https://img.shields.io/badge/sqlite-3-blue.svg)

A conversational AI assistant leveraging advanced language models to provide mental health support through voice interaction.

## Table of Contents

1. [Overview](#overview)
2. [Features](#features)
3. [Tech Stack](#tech-stack)
4. [File Structure](#file-structure)
5. [License](#license)
6. [Contact](#contact)
7. [Future Enhancements](#future-enhancements)

## Overview

This project creates an intelligent voice assistant specifically designed to support mental health conversations. The system utilizes multimodal AI capabilities, allowing users to engage in natural voice conversations about mental health topics, receive supportive responses, and access mental health resources.

## Features

- Voice-based interaction with natural language processing
- Context-aware conversations that maintain session history
- Mental health resource recommendations
- Emotion recognition and appropriate response generation
- User profile management for personalized experiences
- Multi-platform accessibility (web interface)
- Privacy-focused design with local data storage

## Tech Stack

### Backend
- **Python**: Core programming language
- **LiveKit**: Framework for real-time communication (livekit-agents, livekit-plugins-openai, livekit-plugins-silero)
- **OpenAI**: Large language model integration for understanding and generating human-like responses
- **SQLite3**: Local database for storing conversation records and user information
- **Flask/Flask-CORS/Flask-Async**: Web framework for RESTful API endpoints
- **Uvicorn**: ASGI server implementation
- **Python-dotenv**: Environment variable management
- **Typing/Dataclasses**: Type annotations and data structures

### Frontend
- **React**: UI framework for the web interface
- **CSS**: Custom styling with responsive design
- **JSX**: JavaScript XML for component rendering

### Voice Processing
- **Silero**: Voice-to-text processing
- **Text-to-Speech**: Voice synthesis for assistant responses

## File Structure

```
.
├── backend/
│   ├── agent.py          # Core assistant logic
│   ├── api.py            # API interface definitions
│   ├── db_driver.py      # Database operations
│   ├── prompts.py        # LLM prompt templates
│   ├── requirements.txt  # Python dependencies
│   ├── sample.env        # Environment variables template  
│   └── server.py         # Flask server implementation
│
├── frontend/
│   ├── src/
│   │   ├── components/   # React components
│   │   ├── App.css       # Main styling
│   │   ├── App.jsx       # Main application component
│   │   ├── index.css     # Global styles
│   │   └── main.jsx      # Application entry point
│   ├── .gitignore
│   ├── README.md
│   ├── eslint.config.js
│   ├── index.html
│   ├── package-lock.json
│   ├── package.json
│   └── vite.config.js
│
└── README.md             # Project documentation
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contact

- **Email**: akflixs@gmail.com
- **LinkedIn**: [linkedin.com/in/akflixs](https://www.linkedin.com/in/akflixs/)
- **GitHub**: [github.com/akflixs](https://github.com/akflixs)

## Future Enhancements

- Specialized mental health resources integration
- Improved emotion detection through voice analysis
- Crisis intervention protocols
- User preference customization
- Mobile application support
- Integration with healthcare provider systems
- Anonymous data analytics for system improvement
