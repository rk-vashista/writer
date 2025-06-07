# 🎯 AI Content Generator

<div align="center">

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115.12-009688.svg)](https://fastapi.tiangolo.com)
[![CrewAI](https://img.shields.io/badge/CrewAI-0.121.1-orange.svg)](https://github.com/joaomdmoura/crewAI)
[![OpenAI](https://img.shields.io/badge/OpenAI-1.75.0-412991.svg)](https://openai.com)
[![LangChain](https://img.shields.io/badge/LangChain-0.3.25-1C3C3C.svg)](https://langchain.com)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

</div>

> A powerful AI-driven content generation platform that creates engaging, platform-optimized content using intelligent multi-agent crews powered by CrewAI and OpenAI GPT-4.

## ✨ Features

### 🤖 Multi-Agent Content Creation
- **Content Strategist**: Analyzes market trends and develops comprehensive content strategies
- **Content Creator**: Generates engaging, platform-specific content with optimal formatting
- **Content Optimizer**: Refines content based on performance metrics and feedback
- **Platform Specialist**: Ensures platform-specific optimization for algorithms and best practices
- **Audience Researcher**: Conducts behavioral analysis and audience insights
- **SEO Specialist**: Optimizes content for search engine visibility and discovery
- **Viral Content Analyst**: Analyzes viral patterns and engagement factors
- **Brand Voice Guardian**: Maintains consistent brand voice and tone across content
- **GitHub Specialist**: Analyzes repositories and generates technical content
- **Quality Assurance**: Ensures content accuracy, style consistency, and error-free output

### 🎨 Modern Web Interface
- **Responsive Design**: Beautiful UI built with Tailwind CSS that works on all devices
- **Real-time Updates**: Live progress tracking via WebSocket connections
- **Interactive Forms**: Dynamic form fields that adapt to selected platforms
- **Toast Notifications**: Instant feedback for user actions and status updates
- **Markdown Rendering**: Rich text display with syntax highlighting for code
- **Copy-to-Clipboard**: One-click content copying for immediate use

### 📝 Advanced Content Generation
- **Multi-Platform Support**: Twitter, LinkedIn, Instagram, GitHub, Medium, and more
- **Content Types**: Posts, threads, articles, captions, repository descriptions, README files
- **GitHub Integration**: Repository analysis, README generation, and documentation
- **Tone Customization**: Professional, casual, humorous, authoritative, inspiring tones
- **Audience Targeting**: Developers, marketers, entrepreneurs, general audience
- **Goal-Oriented**: Engagement, education, promotion, brand awareness
- **Quick Mode**: Streamlined content generation for rapid results

### 🔄 Intelligent Feedback System
- **Iterative Improvement**: Content refinement based on user feedback
- **Performance Analysis**: Built-in metrics and optimization suggestions
- **A/B Testing**: Multiple content variations for testing
- **Continuous Learning**: Agents improve based on feedback patterns

## 🚀 Quick Start

### Prerequisites
- **Python**: >=3.10,<3.13 (Python 3.11 recommended)
- **OpenAI API Key**: Required for GPT-4/GPT-3.5 content generation
- **GitHub Token**: Optional, for analyzing private repositories  
- **Serper API Key**: Optional, for enhanced web research capabilities

### System Requirements
- **RAM**: Minimum 4GB (8GB recommended for optimal performance)
- **Storage**: ~500MB for dependencies
- **Network**: Stable internet connection for API calls
- **OS**: Linux, macOS, or Windows (Linux/WSL recommended)

### Core Dependencies
This project uses the following key dependencies:
- **CrewAI**: `0.121.1` - Multi-agent orchestration framework
- **FastAPI**: `0.115.12` - Modern web framework for APIs
- **OpenAI**: `1.75.0` - OpenAI API client
- **LangChain**: `0.3.25` - LLM application framework
- **Uvicorn**: `>=0.27.0` - ASGI server for FastAPI
- **WebSockets**: `>=12.0` - Real-time communication

### Installation

1. **Clone and setup the repository**:
```bash
git clone https://github.com/rk-vashista/writer
cd writer
python -m venv .venv
source .venv/bin/activate 
# On Windows: .venv\Scripts\activate
```

2. **Install dependencies**:
```bash
# Using pip (standard method)
pip install -e .

# Or using uv (faster, recommended)
uv sync
```

3. **Configure environment variables**:
```bash
# Create .env file with your API keys
cat << EOF > .env
# Required
OPENAI_API_KEY=your_openai_api_key_here
MODEL=gpt-4-turbo-preview

# Optional: For GitHub repository analysis
GITHUB_TOKEN=your_github_token_here

# Optional: For enhanced web research
SERPER_API_KEY=your_serper_api_key_here

# Optional: For debugging and tracing
LANGCHAIN_TRACING_V2=true
LANGCHAIN_ENDPOINT=https://api.smith.langchain.com
LANGCHAIN_API_KEY=your_langchain_api_key
EOF
```

### Running the Application

#### Web Interface (Recommended)
```bash
# Start the web server
content-generator serve

# Alternative using uvicorn directly
uvicorn pitch.api:app --reload --host 0.0.0.0 --port 8000
```
Visit `http://localhost:8000` in your browser to access the interactive web interface.

#### Command Line Interface
```bash
# Generate content via CLI (basic mode)
content-generator

# Train the crew with custom data
content-generator train <iterations> <training_file.json>
# Example: content-generator train 5 training_data.json

# Test the crew performance
content-generator test <iterations> <model>
# Example: content-generator test 3 gpt-4

# Replay a specific task for debugging
content-generator replay <task_id>
# Example: content-generator replay task_abc123
```

## 🎬 Quick Demo

### 5-Minute Setup
```bash
# Clone and setup
git clone https://github.com/rk-vashista/writer && cd writer
python -m venv .venv && source .venv/bin/activate
pip install -e .

# Add your OpenAI API key
echo "OPENAI_API_KEY=your_key_here" > .env
echo "MODEL=gpt-4-turbo-preview" >> .env

# Start the server
content-generator serve
```

Then visit `http://localhost:8000` and try generating content for Twitter about "AI developments" with a professional tone!

### Sample Output
Here's what you might get for a Twitter post about "AI developments":

```
🚀 The AI landscape is evolving at breakneck speed! 

Key developments this week:
✅ GPT-4 Turbo's enhanced reasoning
✅ New multimodal capabilities 
✅ Reduced API costs by 3x

The future of human-AI collaboration is here. What's your take on these advancements?

#AI #MachineLearning #GPT4 #Innovation #TechTrends
```

## 🏗️ Project Architecture

```
content-generator/
├── 📁 src/pitch/               # Main application package
│   ├── 🐍 __init__.py         # Package initialization
│   ├── 🌐 api.py              # FastAPI web server & REST endpoints
│   ├── 🤖 crew.py             # CrewAI agent definitions & orchestration
│   ├── 🎯 main.py             # CLI entry points & server launcher
│   ├── 📡 status_manager.py   # Real-time WebSocket status updates
│   │
│   ├── 📁 config/             # Configuration files
│   │   ├── 🤖 agents.yaml     # Agent roles, goals & behaviors
│   │   └── 📋 tasks.yaml      # Task definitions & workflows
│   │
│   ├── 📁 static/             # Web UI assets
│   │   ├── 🌐 index.html      # Main web interface
│   │   ├── ⚡ script.js       # Client-side logic & WebSocket handling
│   │   └── 🎨 styles.css      # Custom styling & animations
│   │
│   └── 📁 tools/             # AI agent tools & utilities
│       ├── 🛠️ custom_tool.py    # Specialized analysis tools
│       ├── 📄 document_tools.py # PDF/document parsing
│       ├── 🐙 github_tool.py    # GitHub repository analysis
│       └── 🔍 serper_tool.py    # Web research capabilities
│
├── 📋 pyproject.toml          # Project configuration & dependencies
├── 🔒 uv.lock               # Dependency lock file
├── 📖 README.md              # This documentation
├── 📊 monitor.py             # WebSocket monitoring utility
└── 🔧 .env                   # Environment variables (create this)
```

### Key Components

- **API Layer** (`api.py`): FastAPI server handling HTTP requests and WebSocket connections
- **Agent Orchestration** (`crew.py`): CrewAI-based multi-agent content generation system
- **Configuration** (`config/`): YAML-based agent and task definitions for easy customization
- **Tools** (`tools/`): Specialized utilities for document parsing, GitHub analysis, and web research
- **Web Interface** (`static/`): Modern, responsive UI with real-time progress tracking

## 🔧 Configuration & Customization

### Agent Configuration
Edit `src/pitch/config/agents.yaml` to customize agent behaviors and capabilities:

```yaml
content_strategist:
  role: Senior Content Strategy Architect
  goal: Design comprehensive content strategies that maximize engagement
  backstory: You're a veteran content strategist with 15+ years of experience...
  verbose: true
  allow_delegation: true

content_creator:
  role: Master Content Craftsperson & Writer
  goal: Create compelling, publication-ready content that stops scrolling
  backstory: You're a creative polymath and prolific writer...
  verbose: true
  allow_delegation: false
```

### Task Workflows
Modify `src/pitch/config/tasks.yaml` to define custom task sequences:

```yaml
quick_content_creation_task:
  description: CREATE IMMEDIATE, PUBLICATION-READY CONTENT
  expected_output: The actual content as it should appear when published
  agent: content_creator

audience_research_task:
  description: Research target audience behavior and preferences
  expected_output: Actionable audience insights for content optimization
  agent: audience_researcher
```

### Environment Variables
Configure your `.env` file with the following options:

```bash
# Required
OPENAI_API_KEY=your_openai_api_key

# Model Configuration
MODEL=gpt-4-turbo-preview              # Recommended: gpt-4-turbo-preview, gpt-4, gpt-3.5-turbo
TEMPERATURE=0.7                        # Creativity level (0.0-1.0)

# Optional Integrations
GITHUB_TOKEN=your_github_token         # For private repo analysis
SERPER_API_KEY=your_serper_key        # For enhanced web research
LANGCHAIN_TRACING_V2=true             # For debugging (optional)
LANGCHAIN_ENDPOINT=https://api.smith.langchain.com
LANGCHAIN_API_KEY=your_langchain_api_key
```

## 📝 Usage Examples

### Web Interface Usage

1. **Access the Interface**
   - Open `http://localhost:8000` in your browser
   - Choose your target platform from the dropdown

2. **Basic Content Generation**
   ```
   Platform: Twitter
   Content Type: Social Media Post
   Topic: "Latest developments in AI"
   Tone: Professional
   Target Audience: Tech enthusiasts
   Goals: Drive engagement and educate
   ```

3. **GitHub Repository Analysis**
   ```
   Platform: GitHub
   Content Type: Repository Description
   Repository URL: https://github.com/user/repo
   GitHub Token: [Optional for private repos]
   Target Audience: Developers
   ```

4. **Content with Feedback Loop**
   - Generate initial content
   - Review the output
   - Provide specific feedback in the feedback box
   - Regenerate for improved results

### Command Line Usage

```bash
# Basic content generation
content-generator

# Training the crew with custom data
content-generator train 10 my_training_data.json

# Testing crew performance
content-generator test 5 gpt-4

# Replaying a specific task for debugging
content-generator replay task_abc123
```

### API Integration

```python
import requests

# Generate content via API
response = requests.post("http://localhost:8000/generate", data={
    "platform": "twitter",
    "content_type": "social media post",
    "topic": "Machine Learning trends",
    "tone": "professional",
    "target_audience": "developers",
    "content_goals": "education and engagement"
})

job_id = response.json()["job_id"]
```

### Platform-Specific Features

#### Twitter/X
- Character limit optimization
- Hashtag research and recommendations
- Thread structure for long-form content
- Engagement-focused hooks

#### LinkedIn
- Professional tone calibration
- Industry-specific content
- Article formatting
- Network-appropriate messaging

#### GitHub
- Repository analysis and description generation
- README file creation
- Technical documentation
- Developer community insights

#### Instagram
- Visual content recommendations
- Caption optimization
- Hashtag strategies
- Story-friendly formatting

## 🛠️ Available Tools & Integrations

### Content Analysis Tools
- **Market Research Tool**: Analyzes market trends and audience behavior
- **Competitor Analysis Tool**: Studies competitor strategies and performance
- **Trend Analysis Tool**: Identifies trending topics and themes
- **Viral Content Analyzer**: Analyzes viral patterns and engagement factors

### Optimization Tools
- **Content Optimization Tool**: Enhances readability and engagement
- **Hashtag Research Tool**: Finds optimal hashtags for reach
- **SEO Analyzer**: Optimizes content for search discovery
- **Performance Predictor**: Forecasts content performance metrics

### Platform-Specific Tools
- **Platform Analyzer**: Ensures platform-specific optimization
- **Algorithm Insights Tool**: Adapts to platform algorithms
- **Format Optimizer**: Optimizes content structure per platform

### Research & Intelligence
- **Audience Analysis Tool**: Deep audience behavior analysis
- **Psychographic Profiler**: Psychological audience insights
- **Web Research Tool**: Real-time web content research
- **Document Parser**: Extracts insights from uploaded documents

### Quality Assurance
- **Quality Checker**: Ensures content accuracy and consistency
- **Fact Verifier**: Validates factual claims and statements
- **Style Guide Enforcer**: Maintains brand voice consistency
- **Brand Voice Analyzer**: Calibrates tone and messaging

## 🚀 Advanced Features

### Real-Time Progress Tracking
- Live WebSocket updates during content generation
- Step-by-step progress visualization
- Detailed logging of agent activities
- Error handling and recovery notifications

### Multi-Agent Collaboration
- Agents work together in coordinated workflows
- Automatic task delegation and management
- Quality checks at each stage
- Iterative improvement through feedback loops

### Platform Algorithm Optimization
- Twitter/X: Engagement-focused content with optimal timing
- LinkedIn: Professional networking and thought leadership
- Instagram: Visual storytelling and community building
- GitHub: Technical documentation and developer engagement

### Content Performance Analytics
- Built-in performance prediction
- A/B testing recommendations
- Engagement optimization suggestions
- Platform-specific best practices

## 🔧 Troubleshooting

### Common Issues

#### Installation Problems
```bash
# If you encounter dependency conflicts
pip install --upgrade pip
pip install -e . --force-reinstall

# For uv users
uv sync --refresh
```

#### API Key Issues
- Ensure your OpenAI API key is valid and has sufficient credits
- Check that your `.env` file is in the project root directory
- Verify environment variables are loaded: `echo $OPENAI_API_KEY`

#### WebSocket Connection Issues
```bash
# Check if port 8000 is available
netstat -tulpn | grep :8000

# Start with different port if needed
uvicorn pitch.api:app --host 0.0.0.0 --port 8001
```

#### Permission Errors
```bash
# Make sure you have proper permissions
chmod +x src/pitch/main.py

# Check virtual environment activation
which python  # Should point to your .venv/bin/python
```

### Performance Optimization
- Use `gpt-4-turbo-preview` for better performance vs `gpt-4`
- Enable request caching by setting `LANGCHAIN_CACHE=true`
- For production, consider using Redis for session management

### Debugging
```bash
# Enable verbose logging
export LANGCHAIN_VERBOSE=true

# Enable CrewAI debugging
export CREWAI_DEBUG=true

# Monitor WebSocket connections
python monitor.py
```

### Using the WebSocket Monitor
The project includes a monitoring utility for debugging WebSocket connections:

```bash
# Monitor real-time WebSocket activity
python monitor.py

# This will show:
# - Connection status
# - Message flow between client and server
# - Agent progress updates
# - Error messages and debugging info
```

## 🧪 Development & Testing

### Running Tests
```bash
# Test crew performance
content-generator test 3 gpt-4-turbo-preview

# Test with different models
content-generator test 5 gpt-3.5-turbo
```

### Development Setup
```bash
# Install development dependencies
pip install -e ".[dev]"

# Run in development mode with hot reload
uvicorn pitch.api:app --reload --log-level debug
```

### Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

#### Development Guidelines
1. Follow PEP 8 style guidelines
2. Add tests for new features
3. Update documentation for API changes
4. Test with multiple OpenAI models

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with [crewAI](https://github.com/joaomdmoura/crewAI)
- UI powered by [Tailwind CSS](https://tailwindcss.com)
- Developed with [FastAPI](https://fastapi.tiangolo.com)

---

<div align="center">
Made with ❤️ by content creators, for content creators
</div>
