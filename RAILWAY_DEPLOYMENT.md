# 🚂 Railway Deployment Guide for Lee Electronics AI Chatbot

## 📋 Prerequisites

1. **Railway Account**: Sign up at [railway.app](https://railway.app)
2. **GitHub Repository**: Your code should be in a GitHub repository
3. **Gemini API Key**: Get one from [Google AI Studio](https://makersuite.google.com/app/apikey)

## 🚀 Deployment Steps

### 1. **Prepare Your Repository**

Make sure these files are in your repository root:
- ✅ `requirements.txt` (with all dependencies)
- ✅ `Procfile` (Railway process configuration)
- ✅ `railway.toml` (Railway configuration)
- ✅ `.env.example` (Environment variables template)

### 2. **Deploy to Railway**

1. **Connect Repository**:
   - Go to [railway.app](https://railway.app)
   - Click "Start a New Project"
   - Select "Deploy from GitHub repo"
   - Choose your repository

2. **Configure Environment Variables**:
   Go to your project → Variables tab and add:
   ```
   GEMINI_API_KEY=your-actual-gemini-api-key-here
   SECRET_KEY=your-super-secret-django-key
   DEBUG=False
   RAILWAY_ENVIRONMENT=production
   ```

3. **Add Database** (Optional but recommended):
   - Click "New" → "Database" → "PostgreSQL"
   - Railway will automatically set `DATABASE_URL`

### 3. **Environment Variables Required**

| Variable | Description | Required |
|----------|-------------|----------|
| `GEMINI_API_KEY` | Your Google Gemini API key | ✅ Yes |
| `SECRET_KEY` | Django secret key | ✅ Yes |
| `DEBUG` | Set to `False` for production | ✅ Yes |
| `DATABASE_URL` | PostgreSQL connection (auto-provided) | ⚡ Auto |
| `FRONTEND_URL` | Your frontend domain for CORS | ❌ Optional |
| `CUSTOM_DOMAIN` | Custom domain if you have one | ❌ Optional |

### 4. **Generate Django Secret Key**

Run this locally to generate a secure secret key:
```python
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
```

### 5. **Deploy Frontend (Optional)**

If you want to deploy the React frontend:

1. **Separate Repository**: Create a new repo for the frontend
2. **Update API URL**: In `frontend/app/services/api.ts`, change:
   ```typescript
   const API_BASE_URL = "https://your-backend-domain.railway.app";
   ```
3. **Deploy**: Use Vercel, Netlify, or Railway for the frontend

## 🔧 Configuration Details

### **Procfile Explained**
```
web: gunicorn Lee_Chat.wsgi:application --bind 0.0.0.0:$PORT
release: python manage.py migrate
```
- `web`: Starts the Django server with Gunicorn
- `release`: Runs database migrations on each deployment

### **Railway.toml Explained**
```toml
[build]
builder = "NIXPACKS"  # Railway's build system

[deploy]
healthcheckPath = "/api/chat/"  # Health check endpoint
healthcheckTimeout = 300
restartPolicyType = "ON_FAILURE"
restartPolicyMaxRetries = 3
```

### **Production Features Enabled**
- ✅ **PostgreSQL Database**: Automatic Railway PostgreSQL
- ✅ **Static File Serving**: WhiteNoise for static files
- ✅ **Security Headers**: HTTPS, HSTS, and security middleware
- ✅ **CORS Configuration**: Proper CORS for frontend integration
- ✅ **Logging**: Structured logging for debugging
- ✅ **Health Checks**: Railway health monitoring

## 🌐 Access Your Deployed App

After deployment:
1. **Backend API**: `https://your-app-name.railway.app`
2. **Health Check**: `https://your-app-name.railway.app/api/chat/`
3. **Test Endpoint**: `https://your-app-name.railway.app/api/test/`

## 🧪 Testing Your Deployment

### Test with cURL:
```bash
# Health check
curl https://your-app-name.railway.app/api/chat/

# Test chat
curl -X POST https://your-app-name.railway.app/api/chat/ \
  -H "Content-Type: application/json" \
  -d '{"question": "test"}'
```

### Test with Postman:
1. **URL**: `https://your-app-name.railway.app/api/chat/`
2. **Method**: POST
3. **Body**: `{"question": "What products do you offer?"}`

## 🐛 Troubleshooting

### **Common Issues**

1. **500 Internal Server Error**
   - Check Railway logs: Project → Deployments → View Logs
   - Verify all environment variables are set
   - Check if `GEMINI_API_KEY` is valid

2. **Database Connection Issues**
   - Ensure PostgreSQL service is running
   - Check `DATABASE_URL` in environment variables

3. **Static Files Not Loading**
   - Run `python manage.py collectstatic` (handled by Railway)
   - Check WhiteNoise configuration

4. **CORS Errors**
   - Add your frontend domain to `FRONTEND_URL` environment variable
   - Check browser developer tools for specific CORS errors

### **View Logs**
```bash
# Railway CLI
railway logs

# Or via web interface
# Go to your project → Deployments → View Logs
```

## 🔄 Continuous Deployment

Railway automatically redeploys when you push to your main branch:
1. **Push code** to GitHub
2. **Railway detects changes** and starts building
3. **Automatic deployment** with zero downtime
4. **Health checks** ensure successful deployment

## 💡 Pro Tips

### **Performance Optimization**
- Use Railway's PostgreSQL for better performance
- Enable static file compression with WhiteNoise
- Monitor resource usage in Railway dashboard

### **Security**
- Regularly rotate your `SECRET_KEY`
- Keep your `GEMINI_API_KEY` secure
- Use Railway's environment variable encryption

### **Monitoring**
- Check Railway metrics for performance
- Monitor API response times
- Set up alerts for downtime

## 🎯 Next Steps

1. **Custom Domain**: Add your domain in Railway settings
2. **SSL Certificate**: Railway provides automatic SSL
3. **Monitoring**: Set up uptime monitoring
4. **Scaling**: Railway auto-scales based on demand

## 🆘 Support

- **Railway Docs**: [docs.railway.app](https://docs.railway.app)
- **Django Deployment**: [docs.djangoproject.com](https://docs.djangoproject.com/en/stable/howto/deployment/)
- **Project Issues**: Check GitHub repository issues

---

**Your Lee Electronics AI Chatbot is now ready for production! 🚀**
