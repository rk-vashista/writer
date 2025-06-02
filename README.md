# 🎯 AI Content Generator

<div align="center">



</div>



> A powerful AI-driven content generation platform that creates engaging, platform-optimized content using intelligent agents.

## ✨ Features

### 🤖 Multi-Agent Content Creation
- **Content Strategist**: Plans and structures content strategy
- **Content Creator**: Generates engaging platform-specific content
- **Content Optimizer**: Refines and optimizes based on feedback

### 🎨 Modern Web Interface
- Beautiful, responsive design with Tailwind CSS
- Real-time progress tracking with WebSocket updates
- Interactive progress visualization
- Toast notifications
- Dark mode support

### 📝 Content Generation
- Support for multiple platforms (Twitter, LinkedIn, Instagram, etc.)
- Various content types (posts, threads, articles, captions)
- Customizable tone and style
- Target audience optimization
- Goal-oriented content creation

### 🔄 Feedback Loop
- Instant content regeneration
- User feedback incorporation
- Continuous content improvement
- Platform-specific best practices

## 🚀 Quick Start

### Prerequisites
- Python >=3.10,<3.13
- OpenAI API key

### Installation

1. Clone the repository and set up your environment:
```bash
git clone https://github.com/rk-vashista/writer
cd writer
python -m venv .venv
source .venv/bin/activate 
# On Windows: .venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -e .
```

3. Set up environment variables:
```bash
# Create .env file
cat << EOF > .env
OPENAI_API_KEY=your_key_here
MODEL=gpt-4-turbo-preview
EOF
```

### Running the Application

Start the server:
```bash
uvicorn pitch.api:app --reload --host 0.0.0.0 --port 8000
```

Visit `http://localhost:8000` in your browser to start generating content!

## 🏗️ Project Structure

```
src/pitch/
├── api.py              # FastAPI application and endpoints
├── crew.py            # AI agents configuration
├── status_manager.py  # WebSocket status updates
├── config/           # Configuration files
│   ├── agents.yaml   # Agent definitions
│   └── tasks.yaml    # Task definitions
├── static/           # Web interface
│   ├── index.html
│   ├── script.js
│   └── styles.css
└── tools/            # Agent tools
    └── serper_tool.py
```

## 🔧 Configuration

### Customizing Agents
Edit `src/pitch/config/agents.yaml` to modify agent behaviors:
```yaml
content_strategist:
  role: Expert Content Strategist
  goal: Plan and structure content
  # ...

content_creator:
  role: Creative Content Writer
  goal: Create engaging content
  # ...
```

### Customizing Tasks
Edit `src/pitch/config/tasks.yaml` to define task workflows:
```yaml
content_strategy_task:
  description: Plan content strategy...
  expected_output: Detailed content strategy
  # ...
```

## 📝 Usage Example

1. Select your target platform (e.g., Twitter, LinkedIn)
2. Choose content type (post, thread, article)
3. Enter your topic and goals
4. Set tone and target audience
5. Generate content
6. Review and provide feedback if needed
7. Copy and use your optimized content!

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

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
