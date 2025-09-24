#!/bin/bash
# Quick setup script for A2A Python SDK development

set -e

echo "🚀 Setting up A2A Python SDK development environment..."

# Check if we're in the right directory
if [ ! -f "pyproject.toml" ] || [ ! -d "src/a2a" ]; then
    echo "❌ Please run this script from the a2a-python repository root"
    exit 1
fi

# Check Python version
python_version=$(python3 --version 2>&1 | cut -d' ' -f2 | cut -d'.' -f1,2)
required_version="3.10"

if [[ $(echo "$python_version $required_version" | awk '{print ($1 < $2)}') == 1 ]]; then
    echo "❌ Python $required_version+ required, but found $python_version"
    exit 1
fi

echo "✅ Python $python_version detected"

# Install the package in development mode
echo "📦 Installing A2A SDK in development mode..."
pip install -e ".[http-server]"

# Install development dependencies (optional)
if command -v uv &> /dev/null; then
    echo "📦 Installing development dependencies with uv..."
    uv sync --dev
else
    echo "📦 Installing additional development tools..."
    pip install pytest pytest-asyncio uvicorn
fi

echo ""
echo "🎉 Setup complete!"
echo ""
echo "🏃 Quick start:"
echo "  cd examples/simple-echo-agent"
echo "  python agent.py"
echo ""
echo "🧪 Run tests:"
echo "  cd examples/simple-echo-agent" 
echo "  python test_client.py"
echo ""
echo "🔧 Validate agents:"
echo "  python examples/utils/validate_agent.py http://localhost:8000"
echo ""
echo "📖 Read the guide:"
echo "  cat GETTING_STARTED.md"
echo ""
echo "Happy A2A development! 🚀"