@echo off
echo 🚀 Starting Lee Electronics AI Chatbot...

REM Check if we're in the right directory
if not exist "manage.py" (
    echo ❌ Error: Please run this script from the Django project root directory
    pause
    exit /b 1
)

REM Check if virtual environment exists
if not exist "venv" (
    echo 📦 Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo 🔧 Activating virtual environment...
call venv\Scripts\activate

REM Install dependencies
echo 📚 Installing dependencies...
pip install -r requirements.txt

REM Check for .env file
if not exist ".env" (
    echo ⚙️  Creating .env file from template...
    copy .env.example .env
    echo ❗ Please edit .env file and add your Gemini API key!
    echo    GEMINI_API_KEY=your-actual-api-key-here
)

REM Run migrations
echo 🗄️  Running database migrations...
python manage.py migrate

REM Start the server
echo 🌟 Starting Django development server...
echo 📱 Frontend: cd frontend && npm install && npm run dev
echo 🔗 Backend will be available at: http://localhost:8000
echo 🔗 Frontend will be available at: http://localhost:3000
echo.

python manage.py runserver
