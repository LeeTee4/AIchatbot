#!/bin/bash
# Startup script for Lee Electronics Chatbot

echo "🚀 Starting Lee Electronics AI Chatbot..."

# Check if we're in the right directory
if [ ! -f "manage.py" ]; then
    echo "❌ Error: Please run this script from the Django project root directory"
    exit 1
fi

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    source venv/Scripts/activate
else
    source venv/bin/activate
fi

# Install dependencies
echo "📚 Installing dependencies..."
pip install -r requirements.txt

# Check for .env file
if [ ! -f ".env" ]; then
    echo "⚙️  Creating .env file from template..."
    cp .env.example .env
    echo "❗ Please edit .env file and add your Gemini API key!"
    echo "   GEMINI_API_KEY=your-actual-api-key-here"
fi

# Run migrations
echo "🗄️  Running database migrations..."
python manage.py migrate

# Start the server
echo "🌟 Starting Django development server..."
echo "📱 Frontend: cd frontend && npm install && npm run dev"
echo "🔗 Backend will be available at: http://localhost:8000"
echo "🔗 Frontend will be available at: http://localhost:3000"
echo ""

python manage.py runserver
