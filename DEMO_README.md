# 🔍 TruthLens Demo Interfaces

This directory contains multiple demo interfaces for the TruthLens AI fact-checking system. Choose the interface that best suits your needs!

## 🚀 Quick Start

### Option 1: Easy Launcher (Recommended)
```bash
python launch_demo.py
```
This will guide you through starting the API and choosing your preferred interface.

### Option 2: Manual Setup
1. **Start the API:**
   ```bash
   python app_demo.py
   ```

2. **Choose your interface:**
   - **Streamlit:** `streamlit run streamlit_demo.py`
   - **Gradio:** `python gradio_demo.py`
   - **API Only:** Use `test_demo.py`

## 📱 Demo Interfaces

### 1. Streamlit Interface (`streamlit_demo.py`)
**Best for:** Beautiful, interactive web interface

**Features:**
- 🎨 Modern, responsive UI
- 📊 Interactive charts and metrics
- 🔄 Real-time updates
- 📱 Mobile-friendly design
- 🎯 Easy-to-use interface

**Start:**
```bash
streamlit run streamlit_demo.py
```

**Access:** http://localhost:8501

### 2. Gradio Interface (`gradio_demo.py`)
**Best for:** Quick sharing and temporary public URLs

**Features:**
- 🌐 Temporary public URL generation
- 📤 Easy sharing with others
- 🎨 Clean, simple interface
- ⚡ Fast loading
- 🔗 Direct API integration

**Start:**
```bash
python gradio_demo.py
```

**Access:** http://localhost:7860 + temporary public URL

### 3. API Testing (`test_demo.py`)
**Best for:** Command-line testing and development

**Features:**
- 🔧 Direct API testing
- 📋 Batch claim testing
- 📊 Detailed output
- 🐛 Debugging friendly

**Start:**
```bash
python test_demo.py
```

## 🛠️ Installation

### Prerequisites
- Python 3.8+
- TruthLens API running (see `app_demo.py`)

### Install Dependencies
```bash
# Install demo dependencies
pip install streamlit gradio requests

# Or install all requirements
pip install -r requirements_minimal.txt
```

## 🔧 Configuration

### Environment Variables
Create a `.env` file with your API keys:
```env
NEWS_API_KEY=your_news_api_key
GUARDIAN_API_KEY=your_guardian_api_key
GOOGLE_API_KEY=your_google_api_key
API_BASE_URL=http://localhost:8000
```

### API Configuration
- **Default API URL:** http://localhost:8000
- **Health Check:** http://localhost:8000/health
- **API Docs:** http://localhost:8000/docs

## 📊 Features

### All Interfaces Include:
- ✅ **Claim Verification:** Enter any claim to verify
- 📰 **Article Analysis:** Find related news articles
- 🔍 **Stance Detection:** Analyze supporting/contradicting evidence
- 📊 **Metrics Dashboard:** Processing time, confidence, evidence strength
- ✅ **Fact-Check Integration:** Google Fact Check API results
- 🎯 **Example Claims:** Pre-loaded test cases

### Streamlit-Specific Features:
- 🎨 **Beautiful UI:** Modern, responsive design
- 📊 **Interactive Charts:** Real-time stance analysis
- 🔄 **Session State:** Remember previous inputs
- 📱 **Mobile Optimized:** Works on all devices

### Gradio-Specific Features:
- 🌐 **Public Sharing:** Temporary URLs for demos
- ⚡ **Fast Loading:** Optimized for quick demos
- 📤 **Easy Export:** Share results easily

## 🎯 Example Claims

Try these example claims to test the system:

1. **True Claims:**
   - "The Eiffel Tower is in Paris"
   - "Climate change is real"
   - "The Earth orbits the Sun"

2. **False Claims:**
   - "The Earth is flat"
   - "Vaccines cause autism"
   - "The moon landing was fake"
   - "5G causes coronavirus"

3. **Controversial Claims:**
   - "Social media causes depression"
   - "Electric cars are better for the environment"

## 🔍 API Endpoints

### Health Check
```bash
GET http://localhost:8000/health
```

### Claim Verification
```bash
POST http://localhost:8000/verify
Content-Type: application/json

{
  "claim": "The Eiffel Tower is in Paris",
  "context": "Tourist information"
}
```

### Components Status
```bash
GET http://localhost:8000/components-status
```

## 🚀 Deployment Options

### 1. Local Development
```bash
# Terminal 1: Start API
python app_demo.py

# Terminal 2: Start Streamlit
streamlit run streamlit_demo.py
```

### 2. Render Deployment
- Deploy `app_demo.py` to Render
- Use the deployed API URL in your demo interfaces

### 3. Streamlit Cloud
- Push to GitHub
- Deploy `streamlit_demo.py` to Streamlit Cloud
- Configure API URL to point to your deployed API

### 4. Gradio Spaces
- Push to GitHub
- Deploy `gradio_demo.py` to Hugging Face Spaces
- Configure API URL to point to your deployed API

## 🐛 Troubleshooting

### Common Issues

**1. API Connection Error**
```bash
# Check if API is running
curl http://localhost:8000/health

# Start API if not running
python app_demo.py
```

**2. Missing Dependencies**
```bash
pip install streamlit gradio requests
```

**3. Port Conflicts**
```bash
# Check what's using the port
netstat -ano | findstr :8000  # Windows
lsof -i :8000                 # Mac/Linux

# Kill process or use different port
```

**4. API Keys Not Working**
- Check your `.env` file
- Verify API keys are valid
- Test API endpoints directly

### Debug Mode
```bash
# Enable debug logging
export LOG_LEVEL=DEBUG
python app_demo.py
```

## 📈 Performance

### Expected Response Times
- **Simple Claims:** 2-5 seconds
- **Complex Claims:** 5-10 seconds
- **No Articles Found:** 1-2 seconds

### Resource Usage
- **Memory:** ~200MB (demo mode)
- **CPU:** Low usage (keyword-based analysis)
- **Network:** Depends on API calls

## 🤝 Contributing

### Adding New Features
1. Modify `app_demo.py` for API changes
2. Update demo interfaces accordingly
3. Test with `test_demo.py`
4. Update documentation

### Custom Interfaces
- **Streamlit:** Modify `streamlit_demo.py`
- **Gradio:** Modify `gradio_demo.py`
- **New Framework:** Create new file following existing patterns

## 📚 Additional Resources

- **API Documentation:** http://localhost:8000/docs
- **GitHub Repository:** https://github.com/Abhishek86798/TruthLens
- **Full Requirements:** `requirements.txt`
- **Demo Requirements:** `requirements_minimal.txt`

## 🎉 Demo Success Tips

1. **Start with Simple Claims:** Test with well-known facts first
2. **Check API Health:** Ensure the backend is running
3. **Use Example Claims:** Try the pre-loaded examples
4. **Monitor Logs:** Watch for any error messages
5. **Share Results:** Use Gradio's public URL for demos

---

**Happy Fact-Checking! 🔍✨**
