#!/bin/bash
set -e

echo "🚀 Setting up NL2SQL Data Agent environment..."

# Install uv package manager
echo "📦 Installing uv package manager..."
curl -LsSf https://astral.sh/uv/install.sh | sh
export PATH="$HOME/.local/bin:$PATH"

# Create virtual environment and install dependencies
echo "📦 Installing Python dependencies..."
uv venv
source .venv/bin/activate
uv sync

# Setup the University SQLite database
echo "🎓 Setting up University database..."
uv run python scripts/setup_sqlite_university.py

# Create .env from example if it doesn't exist
if [ ! -f .env ]; then
    echo "📝 Creating .env file from template..."
    cp .env.example .env
    echo ""
    echo "⚠️  IMPORTANT: Edit .env and add your API keys!"
    echo "   Required: OPENAI_API_KEY or AZURE_OPENAI_* settings"
    echo ""
fi

# Verify installation
echo "✅ Verifying installation..."
uv run data-agent --help > /dev/null 2>&1 && echo "✅ data-agent CLI installed successfully!"

echo ""
echo "╔════════════════════════════════════════════════════════════════╗"
echo "║           🎉 NL2SQL Data Agent Setup Complete! 🎉             ║"
echo "╠════════════════════════════════════════════════════════════════╣"
echo "║                                                                ║"
echo "║  Next Steps:                                                   ║"
echo "║  1. Edit .env and add your GITHUB_TOKEN                        ║"
echo "║     (Get one FREE at github.com/settings/tokens)               ║"
echo "║  2. Test with: uv run data-agent query \"...\" -c university    ║"
echo "║                                                                ║"
echo "║  Example queries:                                              ║"
echo "║  • \"What courses does Srinivasan teach?\"                       ║"
echo "║  • \"List students with A grades in Computer Science\"           ║"
echo "║  • \"What are the prerequisites for CS-315?\"                    ║"
echo "║                                                                ║"
echo "║  Available configs: university, chinook, pagila                ║"
echo "║                                                                ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""
