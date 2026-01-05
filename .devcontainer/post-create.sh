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
    echo "⚠️  IMPORTANT: Edit .env and add your GITHUB_TOKEN!"
    echo "   Get one FREE at: https://github.com/settings/tokens"
    echo "   Select 'models:read' permission for GitHub Models access"
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
echo "║  REQUIRED STEP - Add your GitHub Token:                        ║"
echo "║  1. Go to: https://github.com/settings/tokens                  ║"
echo "║  2. Create token with 'models:read' permission                 ║"
echo "║  3. Edit .env file and paste: GITHUB_TOKEN=ghp_your_token      ║"
echo "║                                                                ║"
echo "╠════════════════════════════════════════════════════════════════╣"
echo "║  COMMANDS:                                                     ║"
echo "║  • uv run data-agent teach           - Learn DB concepts       ║"
echo "║  • uv run data-agent query \"...\" -c university - Query data   ║"
echo "║  • uv run data-agent chat -c university - Interactive mode     ║"
echo "║                                                                ║"
echo "║  Example queries:                                              ║"
echo "║  • \"What courses does Srinivasan teach?\"                       ║"
echo "║  • \"List all students in Computer Science\"                     ║"
echo "║                                                                ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""
