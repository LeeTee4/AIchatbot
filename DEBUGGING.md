# 🔧 Debugging Guide for Lee Electronics Chatbot

## Quick Troubleshooting Steps

### 1. **Check if Backend is Running**
```bash
# Test if Django server is accessible
curl http://localhost:8000/api/test/
```

Expected response:
```json
{
    "message": "Backend is working!",
    "timestamp": 1234567890,
    "gemini_configured": true/false
}
```

### 2. **Test Chat Endpoint**
```bash
# Test the chat endpoint
curl -X POST http://localhost:8000/api/chat/ \
  -H "Content-Type: application/json" \
  -d '{"question": "test"}'
```

Expected response:
```json
{
    "answer": "Connection successful! Lee Electronics AI Assistant is ready to help you."
}
```

### 3. **Frontend Connection Test**
In the chat interface, click the "Test Backend" button to verify connectivity.

## Common Issues and Solutions

### ❌ **"Connection failed" error**

**Symptoms:** Red connection indicator, "Failed to send message" errors

**Solutions:**
1. **Check if Django server is running:**
   ```bash
   python manage.py runserver
   ```

2. **Verify the correct port:** Make sure Django is running on port 8000

3. **Check CORS settings:** Ensure frontend origin is allowed in Django settings

4. **Test with curl:** Use the curl commands above to verify backend

### ❌ **"Internal server error" in backend**

**Symptoms:** 500 errors in Django logs

**Solutions:**
1. **Check Django logs** for the specific error
2. **Missing dependencies:** Install all requirements
   ```bash
   pip install -r requirements.txt
   ```
3. **Missing API key:** Set up your Gemini API key in `.env`
4. **Database issues:** Run migrations
   ```bash
   python manage.py migrate
   ```

### ❌ **"Gemini AI not configured" messages**

**Symptoms:** Mock responses instead of AI responses

**Solutions:**
1. **Get Gemini API key** from [Google AI Studio](https://makersuite.google.com/app/apikey)
2. **Set environment variable:**
   ```bash
   # In .env file
   GEMINI_API_KEY=your-actual-api-key-here
   ```
3. **Restart Django server** after setting the API key

### ❌ **FAISS-related errors**

**Symptoms:** Errors about FAISS not being available

**Solutions:**
1. **Install FAISS:**
   ```bash
   pip install faiss-cpu
   ```
2. **If FAISS installation fails:** The app will fallback to simple search
3. **For M1 Macs:** Use conda to install FAISS
   ```bash
   conda install -c conda-forge faiss-cpu
   ```

### ❌ **Frontend build/development issues**

**Symptoms:** React Router errors, TypeScript errors

**Solutions:**
1. **Install Node.js dependencies:**
   ```bash
   cd frontend
   npm install
   ```
2. **Clear cache and reinstall:**
   ```bash
   rm -rf node_modules package-lock.json
   npm install
   ```
3. **Check Node.js version:** Ensure Node.js 18+ is installed

## Step-by-Step Setup Verification

### Backend Setup ✅
1. **Navigate to project directory**
2. **Create virtual environment:** `python -m venv venv`
3. **Activate virtual environment:** `venv\Scripts\activate` (Windows) or `source venv/bin/activate` (Mac/Linux)
4. **Install dependencies:** `pip install -r requirements.txt`
5. **Set up environment variables:** Copy `.env.example` to `.env` and add your API key
6. **Run migrations:** `python manage.py migrate`
7. **Start server:** `python manage.py runserver`
8. **Test:** Visit http://localhost:8000/api/test/

### Frontend Setup ✅
1. **Navigate to frontend directory:** `cd frontend`
2. **Install dependencies:** `npm install`
3. **Start development server:** `npm run dev`
4. **Test:** Visit http://localhost:3000

## Testing Checklist

- [ ] Backend responds at `http://localhost:8000/api/test/`
- [ ] Chat endpoint responds at `http://localhost:8000/api/chat/`
- [ ] Frontend loads at `http://localhost:3000`
- [ ] Chat interface shows "Connected" status
- [ ] "Test Backend" button works
- [ ] Can send messages and receive responses
- [ ] Gemini AI is configured (not showing mock responses)

## Logs and Debugging

### Backend Logs
```bash
# View Django logs
python manage.py runserver --verbosity=2
```

### Frontend Logs
- Open browser developer tools (F12)
- Check Console tab for JavaScript errors
- Check Network tab for failed API requests

### API Response Debugging
```bash
# Test with detailed output
curl -v http://localhost:8000/api/chat/ \
  -H "Content-Type: application/json" \
  -d '{"question": "hello"}'
```

## Environment Variables

Create a `.env` file in the project root:
```env
# Required for AI functionality
GEMINI_API_KEY=your-actual-gemini-api-key-here

# Optional - Django settings
DEBUG=True
SECRET_KEY=your-secret-key
```

## Performance Tips

1. **First load might be slow:** FAISS index initialization takes time
2. **Subsequent requests are faster:** Index is cached in memory
3. **For production:** Use Redis for caching and proper database

## Getting Help

If you're still having issues:

1. **Check the GitHub Issues** for similar problems
2. **Provide specific error messages** when asking for help
3. **Include your setup details** (OS, Python version, Node.js version)
4. **Share relevant logs** (without sensitive information)

---

**Happy debugging! 🚀**
