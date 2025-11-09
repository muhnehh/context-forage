# 🚀 QUICK START - ContextForge

## 3 Steps to Run

### Step 1: Install
```bash
pip install -r requirements.txt
```

### Step 2: Test (verify it works)
```bash
python test_real_mcp.py
```
Should show: ✅ 3/3 tests passed

### Step 3: Run
```bash
streamlit run app.py
```
Opens at: http://localhost:8501

---

## That's It!

1. Upload a research document (PDF or TXT)
2. Click "Analyze with Multi-Agent System"
3. Watch 4 AI agents collaborate
4. Download PDF report with results

---

## What You Get

✅ Research gaps identified  
✅ Gaps debated (pro/con arguments)  
✅ Novel hypotheses generated  
✅ Hypotheses refined & evolved  
✅ Real MCP messages tracked  
✅ Privacy protection applied  

---

## Troubleshooting

**"ModuleNotFoundError"**
→ `pip install --upgrade crewai litellm diffprivlib streamlit langchain`

**"LLM failed"**
→ Tests still pass? Then UI is falling back gracefully (agent handling errors)

**"No MCP messages"**
→ LLM needs to run. Either:
- Set Groq API key: `export GROQ_API_KEY="your-key"`
- Or start Ollama: `ollama serve`

---

## More Info

Read: `SETUP.md` for detailed guide  
Read: `CLEANUP_SUMMARY.md` for what changed

---

Status: ✅ READY TO USE
