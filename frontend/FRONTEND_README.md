# Lee Electronics AI Chatbot - Frontend

Modern React application built with React Router v7 and Tailwind CSS for the Lee Electronics AI Chatbot.

## 🚀 Quick Start

### Prerequisites
- Node.js 18+ 
- npm or yarn

### Installation

1. **Install dependencies**
   ```bash
   npm install
   ```

2. **Start development server**
   ```bash
   npm run dev
   ```

3. **Build for production**
   ```bash
   npm run build
   ```

The application will be available at `http://localhost:3000`

## 🏗️ Project Structure

```
frontend/
├── app/
│   ├── components/
│   │   └── Layout.tsx          # Main layout component
│   ├── routes/
│   │   ├── home.tsx           # Landing page
│   │   ├── chat.tsx           # Chat interface
│   │   └── about.tsx          # About page
│   ├── services/
│   │   └── api.ts             # Backend API service
│   ├── app.css                # Global styles
│   ├── root.tsx               # Root application component
│   └── routes.ts              # Route configuration
├── public/
└── package.json
```

## 🎨 Features

### 🏠 **Home Page**
- Modern hero section with call-to-action
- Feature highlights
- Responsive design with beautiful gradients

### 💬 **Chat Interface**
- Real-time chat with AI assistant
- Message history with timestamps
- Connection status indicator
- Quick suggestion buttons
- Loading states and error handling

### ℹ️ **About Page**
- Technology overview
- How it works section
- Benefits and features
- Technical specifications

## 🔧 Configuration

### Backend Connection
The frontend connects to the Django backend API at `http://localhost:8000`. To change this:

1. Update `API_BASE_URL` in `app/services/api.ts`
2. Ensure CORS is properly configured in Django settings

### Styling
- Uses Tailwind CSS for styling
- Custom gradients and modern design
- Fully responsive layout
- Dark mode ready (can be extended)

## 🌐 API Integration

The frontend communicates with the Django backend through:

- **POST /api/chat/** - Send messages to AI assistant
- Real-time connection status checking
- Error handling and retry logic

## 📱 Responsive Design

- **Mobile First**: Optimized for mobile devices
- **Tablet Support**: Perfect layout for tablets
- **Desktop**: Full-featured desktop experience
- **Touch Friendly**: Large buttons and easy navigation

## 🚀 Deployment

### Development
```bash
npm run dev
```

### Production Build
```bash
npm run build
npm run start
```

### Environment Variables
No environment variables required for frontend. Backend URL is configured in the API service.

## 🎯 Browser Support

- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

## 📝 Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run start` - Start production server
- `npm run typecheck` - Run TypeScript type checking

## 🛠️ Technology Stack

- **React 19** - Latest React with concurrent features
- **React Router v7** - Modern routing with TypeScript
- **TypeScript** - Type safety and better DX
- **Tailwind CSS** - Utility-first CSS framework
- **Vite** - Fast build tool and dev server

## 🔮 Future Enhancements

- [ ] Dark mode toggle
- [ ] Message export functionality
- [ ] Voice input/output
- [ ] Multi-language support
- [ ] Offline mode
- [ ] Push notifications

---

**Built with ❤️ for Lee Electronics**
