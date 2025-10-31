#!/bin/bash
# SPTool Setup Script

echo "╔═══════════════════════════════════════════════════════╗"
echo "║                                                       ║"
echo "║   SPTool - System Performance Troubleshooting Tool   ║"
echo "║                  Setup Script                         ║"
echo "║                                                       ║"
echo "╚═══════════════════════════════════════════════════════╝"
echo ""

# Check Python version
echo "Checking Python version..."
python3 --version

if [ $? -ne 0 ]; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

echo "✅ Python is installed"
echo ""

# Create virtual environment (optional but recommended)
read -p "Do you want to create a virtual environment? (recommended) [y/N]: " create_venv

if [[ $create_venv =~ ^[Yy]$ ]]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    
    if [ $? -eq 0 ]; then
        echo "✅ Virtual environment created"
        echo "Activating virtual environment..."
        source venv/bin/activate
        echo "✅ Virtual environment activated"
    else
        echo "❌ Failed to create virtual environment"
        exit 1
    fi
fi

echo ""

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

if [ $? -eq 0 ]; then
    echo "✅ Dependencies installed successfully"
else
    echo "❌ Failed to install dependencies"
    exit 1
fi

echo ""

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "Creating .env configuration file..."
    cp .env.example .env 2>/dev/null || cat > .env << 'EOF'
# SPTool Configuration
SECRET_KEY=dev-secret-key-change-in-production
DEBUG=True
HOST=127.0.0.1
PORT=5000
OPENAI_API_KEY=
REQUIRE_CONFIRMATION=True
LOG_ACTIONS=True
CPU_THRESHOLD=90
MEMORY_THRESHOLD=85
DISK_THRESHOLD=90
TEMP_THRESHOLD=80
EOF
    echo "✅ Configuration file created (.env)"
else
    echo "ℹ️  Configuration file already exists (.env)"
fi

echo ""
echo "╔═══════════════════════════════════════════════════════╗"
echo "║                                                       ║"
echo "║              🎉 Setup Complete! 🎉                    ║"
echo "║                                                       ║"
echo "╚═══════════════════════════════════════════════════════╝"
echo ""
echo "To start the application:"
echo ""
if [[ $create_venv =~ ^[Yy]$ ]]; then
    echo "  1. Activate virtual environment:"
    echo "     source venv/bin/activate"
    echo ""
fi
echo "  2. Run the application:"
echo "     python app.py"
echo ""
echo "  3. Open in browser:"
echo "     http://127.0.0.1:5000"
echo ""
echo "Note: Some fixes may require sudo privileges."
echo "      To run with sudo: sudo python app.py"
echo ""

