# 🤖 AI Chatbot

A modern, interactive AI chatbot built with Streamlit and powered by multiple AI models through OpenRouter API. Features a beautiful, responsive UI with real-time chat capabilities and comprehensive configuration options.

## ✨ Features

- **Multiple AI Models**: Support for Mistral, DeepSeek, and Google Gemini models
- **Beautiful UI**: Modern gradient design with smooth animations
- **Real-time Chat**: Interactive conversation with AI assistants
- **Chat Statistics**: Track message counts and response times
- **Export Functionality**: Save your conversations
- **Responsive Design**: Works seamlessly on desktop and mobile
- **Customizable**: Extensive configuration through TOML file
- **Random Starters**: Get conversation ideas with random prompts

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- OpenRouter API key

### Installation

### Clone the repository

```bash
git clone https://github.com/mmostafa74/llm-chatbot
cd llm-chatbot
```

### Install dependencies

```bash
pip install -r requirements.txt
```

### Set up environment variables

```bash
# Create .env file
echo "OPENROUTER_API_KEY=your_api_key_here" > .env
```

### Run the application

```bash
streamlit run app.py
```

## ⚙️ Configuration

The application is highly configurable through `config.toml`:

### App Settings

```toml
[app]
title = "AI Chatbot"
page_icon = "🤖"
description = "Ask me anything about AI, coding, or beyond!"
model = "mistralai/mistral-7b-instruct"
system_prompt = "You are a helpful assistant."
```

### API Configuration

```toml
[api]
available_models = [
    "mistralai/mistral-7b-instruct:free",
    "deepseek/deepseek-chat-v3-0324:free",
    "google/gemini-2.0-flash-exp:free",
]
```

### UI Customization

```toml
[ui]
chat_height = 620
layout = "wide"
initial_sidebar_state = "expanded"
```

## 🎨 Styling

The application features a modern design with:

- **Custom CSS**: Comprehensive styling with gradients and animations
- **Google Fonts**: Inter font family for clean typography
- **Responsive Layout**: Mobile-friendly design
- **Message Bubbles**: Distinct styling for user and AI messages
- **Hover Effects**: Interactive elements with smooth transitions

## 🔧 Usage

### Basic Chat

1. Start the application
2. Type your message in the input field
3. Press Enter or click Send
4. View AI responses in real-time

### Advanced Features

- **Model Selection**: Choose from available AI models in the sidebar
- **Temperature Control**: Adjust response creativity
- **Chat Export**: Save conversations as text files
- **Statistics**: Monitor chat metrics
- **Random Prompts**: Get conversation starters

## 📁 Project Structure

```text
llm-chatbot/
├── app.py                 # Main Streamlit application
├── config.toml           # Configuration file
├── config_manager.py     # Configuration management
├── requirements.txt      # Python dependencies
├── .env                 # Environment variables
├── README.md            # Project documentation
└── assets/              # Static assets (if any)
```

## 🔑 Environment Variables

Create a `.env` file in the project root:

```env:.env
# OpenRouter API Configuration
OPENROUTER_API_KEY=your_openrouter_api_key_here

# Optional: Custom API Base URL
OPENROUTER_BASE_URL=https://openrouter.ai/api/v1
```

## 🛠️ Development

### Local Development

```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Run with hot reload
streamlit run app.py --server.runOnSave=true
```

### Code Structure

- `app.py`: Main application logic
- `config_manager.py`: Configuration handling
- `config.toml`: Application settings
- Custom CSS embedded in config for styling

## 📝 License

This project is licensed under the MIT License.

## Troubleshooting

### Common Issues

### API Key Issues

```bash
# Verify your API key is set
echo $OPENROUTER_API_KEY
```

### Module Import Errors

```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### Streamlit Port Issues

```bash
# Run on different port
streamlit run app.py --server.port=8502
```

## 📊 Features Overview

| Feature | Description | Status |
|---------|-------------|--------|
| Multiple AI Models | Support for various LLMs | ✅ |
| Real-time Chat | Interactive conversations | ✅ |
| Export Chat | Save conversations | ✅ |
| Statistics | Chat metrics tracking | ✅ |
| Responsive UI | Mobile-friendly design | ✅ |
| Custom Styling | Modern gradient design | ✅ |
| Configuration | TOML-based settings | ✅ |

## 🔮 Roadmap

- [ ] Chat history persistence
- [ ] User authentication
- [ ] File upload support
- [ ] Voice input/output
- [ ] Multi-language support
- [ ] Plugin system
- [ ] Advanced analytics

## 🙏 Acknowledgments

- [Streamlit](https://streamlit.io/) for the amazing web framework
- [OpenRouter](https://openrouter.ai/) for AI model access
- [Google Fonts](https://fonts.google.com/) for typography
- The open-source community for inspiration

---

Built with ❤️ using Streamlit and OpenRouter
