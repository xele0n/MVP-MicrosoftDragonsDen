# 🤖 AI Chat Agent Setup Guide

## Overview

SPTool now includes an intelligent AI chat agent that can help diagnose system issues, answer questions, and provide troubleshooting guidance using OpenAI's GPT-3.5.

---

## 🔑 Setup Instructions

### Step 1: Get Your OpenAI API Key

1. Go to [OpenAI Platform](https://platform.openai.com)
2. Sign up or log in to your account
3. Navigate to **API Keys** section
4. Click **"Create new secret key"**
5. Copy the API key (starts with `sk-...`)

### Step 2: Configure SPTool

#### Option A: Using .env file (Recommended)

1. Create or edit `.env` file in the project root:
```bash
cd /home/xeleon/Documents/MVP-MicrosoftDragonsDen
nano .env
```

2. Add your API key:
```env
OPENAI_API_KEY=sk-your-actual-api-key-here
```

3. Save and exit (Ctrl+X, then Y, then Enter)

#### Option B: Using environment variable

```bash
export OPENAI_API_KEY="sk-your-actual-api-key-here"
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

This will install the `openai` Python package.

### Step 4: Start SPTool

```bash
python app.py
```

### Step 5: Test the Chat

1. Open http://127.0.0.1:5000
2. Look for the blue "Ask AI" button in the bottom-right corner
3. Click it to open the chat widget
4. Try sending a message like "Analyze my system performance"

---

## 💬 Using the Chat Agent

### Chat Interface

The AI assistant appears as a floating widget in the bottom-right corner of the screen.

**Features:**
- **Toggle button**: Blue circular button with "AI" icon
- **Quick actions**: Pre-set questions for common tasks
- **Chat history**: Maintains conversation context
- **System context**: AI knows your current system state
- **Minimize**: Collapse the chat while keeping it open
- **Close**: Hide the chat completely

### Quick Start Questions

Try these questions to get started:

1. **"Analyze my system performance"** - Get an instant overview
2. **"My computer is running slow"** - Troubleshoot performance
3. **"How do I free up disk space?"** - Get specific guidance
4. **"What's using the most CPU?"** - Identify resource hogs
5. **"How can I improve memory usage?"** - Optimization tips

### Example Conversations

**Example 1: Performance Analysis**
```
You: Analyze my system performance

AI: Based on your current system state:
- CPU: 45% usage - Normal range
- Memory: 67% - Moderate usage, could be optimized
- Disk: 82% - Getting full, consider cleanup

Top processes consuming resources:
1. Chrome: 12% CPU, 8% Memory
2. Python: 8% CPU, 5% Memory

Recommendations:
- Consider clearing temporary files (use "Clear temporary files" fix)
- Chrome has multiple tabs - close unused ones
- Your disk is at 82% - free up space soon
```

**Example 2: Specific Issue**
```
You: My computer freezes randomly

AI: Random freezing can have several causes. Let me help diagnose:

Based on your system:
- Memory usage is at 87% - this is high and could cause freezing
- Several heavy processes running simultaneously

Immediate actions you can take:
1. Use SPTool's "Run Full Diagnosis" to identify issues
2. Check "Top Processes" tab to see what's consuming resources
3. Consider using the "Clear cache" fix to free memory

Would you like me to explain any specific aspect?
```

---

## 🎯 What the AI Can Do

### Diagnostic Capabilities

- **Analyze current system state** (CPU, memory, disk usage)
- **Identify performance bottlenecks**
- **Explain system metrics**
- **Compare current vs normal values**
- **Detect unusual behavior**

### Troubleshooting Help

- **Suggest specific fixes** from SPTool's available commands
- **Provide step-by-step guidance**
- **Explain what commands do**
- **Recommend best practices**
- **Help prioritize issues**

### Knowledge & Guidance

- **Answer technical questions**
- **Explain system concepts**
- **Provide Linux/Windows specific advice**
- **Suggest preventive measures**
- **Link to relevant SPTool features**

---

## ⚙️ Configuration Options

### In config.py

```python
# OpenAI API settings
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY', '')
```

### Model Selection

By default, the chat uses **GPT-3.5-turbo** for:
- Fast responses
- Cost-effective
- Accurate for technical support

To use GPT-4 (more expensive but smarter), edit `chat_agent.py`:

```python
response = openai.ChatCompletion.create(
    model="gpt-4",  # Change from gpt-3.5-turbo
    messages=messages,
    max_tokens=500,
    temperature=0.7
)
```

---

## 🔐 Security & Privacy

### What Data is Sent to OpenAI?

When you chat with the AI:
- Your message text
- Current system metrics (CPU, memory, disk, top processes)
- Recent conversation history (last 10 messages)

**NOT sent:**
- Personal files
- Passwords or credentials
- Command history
- Detailed process information beyond top 5

### API Key Security

✅ **Do:**
- Store API key in `.env` file (not tracked by git)
- Use `.gitignore` to exclude `.env`
- Keep your key private
- Rotate keys periodically

❌ **Don't:**
- Commit API keys to git
- Share keys publicly
- Use the same key across many services

---

## 💰 Cost Considerations

### Pricing (as of 2024)

**GPT-3.5-turbo:**
- Input: $0.0015 per 1K tokens
- Output: $0.002 per 1K tokens

**Average costs:**
- Simple question: ~$0.001 - $0.003
- Detailed analysis: ~$0.005 - $0.01
- 100 conversations: ~$0.50 - $1.00

### Token Usage

The chat widget shows token usage after each response:
- Typical message: 100-300 tokens
- With system context: 200-500 tokens
- Long conversation: 500-1000 tokens

---

## 🐛 Troubleshooting

### Chat button appears grayed out

**Problem**: API key not configured

**Solution**:
```bash
# Check if key is set
echo $OPENAI_API_KEY

# If empty, add to .env:
echo "OPENAI_API_KEY=sk-your-key" >> .env

# Restart SPTool
python app.py
```

### Error: "Invalid API key"

**Problem**: API key is incorrect or expired

**Solutions**:
1. Verify key from OpenAI dashboard
2. Check for extra spaces in `.env`
3. Generate a new key
4. Update `.env` with correct key

### Error: "Rate limit exceeded"

**Problem**: Too many requests to OpenAI

**Solutions**:
1. Wait a few minutes
2. Upgrade OpenAI plan for higher limits
3. Reduce conversation frequency

### Chat not responding

**Check these:**

1. **Backend running?**
   ```bash
   curl http://127.0.0.1:5000/api/chat/status
   ```

2. **API key set?**
   ```bash
   grep OPENAI_API_KEY .env
   ```

3. **Dependencies installed?**
   ```bash
   pip list | grep openai
   ```

4. **Check console for errors**
   - Open browser DevTools (F12)
   - Check Console tab
   - Look for error messages

---

## 📊 API Endpoints

### Check Chat Status
```bash
curl http://127.0.0.1:5000/api/chat/status
```

Response:
```json
{
  "configured": true,
  "api_key_set": true
}
```

### Send Chat Message
```bash
curl -X POST http://127.0.0.1:5000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello", "include_context": true}'
```

### Get Quick Analysis
```bash
curl http://127.0.0.1:5000/api/chat/analysis
```

### Reset Conversation
```bash
curl -X POST http://127.0.0.1:5000/api/chat/reset
```

---

## 🎨 Customization

### Modify AI Personality

Edit `chat_agent.py`, change the system prompt:

```python
system_prompt = """You are SPTool Assistant, a [YOUR DESCRIPTION HERE].

Your capabilities:
- [LIST YOUR CAPABILITIES]

When responding:
- [YOUR STYLE GUIDELINES]
"""
```

### Adjust Response Length

In `chat_agent.py`:

```python
response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=messages,
    max_tokens=500,  # Increase for longer responses
    temperature=0.7  # 0=focused, 1=creative
)
```

---

## ✅ Verification Checklist

Before using the chat:

- [ ] OpenAI account created
- [ ] API key generated
- [ ] Key added to `.env` file
- [ ] `openai` package installed
- [ ] SPTool running
- [ ] Chat status shows "AI Assistant ready"
- [ ] Test message sent successfully

---

## 📝 Quick Reference

### File Locations

```
/home/xeleon/Documents/MVP-MicrosoftDragonsDen/
├── .env                    # API key stored here
├── chat_agent.py          # AI chat logic
├── app.py                 # API endpoints (line 142-196)
├── static/js/app.js       # Chat UI (line 493-704)
└── templates/index.html   # Chat widget HTML
```

### Key Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Check if chat works
curl http://127.0.0.1:5000/api/chat/status

# View logs
tail -f sptool_actions.log

# Test chat from command line
curl -X POST http://127.0.0.1:5000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "test"}'
```

---

## 🚀 Next Steps

Once chat is working:

1. **Explore features**: Try different types of questions
2. **Check usage**: Monitor OpenAI dashboard for costs
3. **Customize prompts**: Adjust AI personality as needed
4. **Share feedback**: Note what works well and what doesn't
5. **Add context**: The AI improves with more specific questions

---

## 🆘 Need Help?

If you're still having issues:

1. Check the terminal output where SPTool is running
2. Look for Python errors or tracebacks
3. Verify API key is valid at OpenAI dashboard
4. Test API key directly:
   ```bash
   curl https://api.openai.com/v1/models \
     -H "Authorization: Bearer $OPENAI_API_KEY"
   ```

---

**Happy chatting with your AI assistant!** 🤖✨

