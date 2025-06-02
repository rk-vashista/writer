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
- Support for multiple platforms (Twitter, LinkedIn, Instagram, GitHub, etc.)
- Various content types (posts, threads, articles, captions, repository descriptions)
- GitHub repository analysis and content generation
- Intelligent tag and description generation for repositories
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
# Optional: Add GitHub token for private repository access
GITHUB_TOKEN=your_github_token_here
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
.
├── .env               # Environment variables configuration
├── .gitignore        # Git ignore rules
├── monitor.py        # WebSocket monitoring utility
├── pyproject.toml    # Project configuration and dependencies
├── README.md         # Project documentation
├── report.md         # Documentation and reports
├── sample.pdf        # Sample document for testing
├── uv.lock           # Dependency lock file
└── src/
    └── pitch/
        ├── __init__.py         # Package initialization
        ├── api.py              # FastAPI application and endpoints
        ├── crew.py             # Content generation crew setup
        ├── main.py             # CLI and server entry points
        ├── status_manager.py   # Real-time status updates via WebSocket
        ├── config/
        │   ├── agents.yaml     # Agent roles and behaviors
        │   └── tasks.yaml      # Task definitions and workflows
        ├── static/
        │   ├── index.html      # Responsive UI with dynamic forms
        │   ├── script.js       # Client-side logic and WebSocket handling
        │   └── styles.css      # Markdown and UI styling
        └── tools/
            ├── __init__.py        # Tools package initialization
            ├── custom_tool.py     # Base tool template
            ├── document_tools.py  # Document parsing utilities
            ├── github_tool.py     # GitHub repository analysis
            └── serper_tool.py     # Web research capabilities
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

### Regular Content Generation
1. Select your target platform (e.g., Twitter, LinkedIn)
2. Choose content type (post, thread, article)
3. Enter your topic and goals
4. Set tone and target audience
5. Generate content
6. Review and provide feedback if needed
7. Copy and use your optimized content!

### GitHub Repository Content
1. Select GitHub as the platform
2. Choose content type (description or tags)
3. Enter the repository URL
4. (Optional) Provide GitHub token for private repositories
5. Set tone and target audience
6. Generate repository-specific content
7. Review and use the optimized description or tags

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
