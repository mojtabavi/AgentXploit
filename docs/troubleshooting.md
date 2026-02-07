# Troubleshooting Guide

Common issues and solutions for PentestAI framework.

## Quick Diagnostics

```bash
# Check all services
docker-compose ps

# Test API
curl http://localhost:8000/api/health

# Test Kali MCP
curl http://localhost:5000/health

# View logs
docker-compose logs -f
```

## Docker Issues

### Container Won't Start

**Symptoms:**
```
Error: Container exits immediately
```

**Solutions:**
```bash
# Check logs
docker logs pentestai-api

# Rebuild from scratch
docker-compose down -v
docker-compose up -d --build

# Check for port conflicts
netstat -ano | findstr :8000  # Windows
lsof -i :8000                 # Linux/Mac
```

### Port Already in Use

**Error:**
```
Error: bind: address already in use
```

**Solution:**
```bash
# Find process
netstat -ano | findstr :8000
taskkill /PID <pid> /F  # Windows
kill -9 <pid>           # Linux/Mac

# Or change port in docker-compose.yml
ports:
  - "8001:8000"
```

### Network Issues

**Error:**
```
Error: network pentestai-network declared as external, but could not be found
```

**Solution:**
```bash
# Remove network reference
docker-compose down -v

# Recreate
docker-compose up -d
```

## LLM Connection Issues

### OpenAI API Key Invalid

**Error:**
```json
{"error": "LLM not connected"}
```

**Solutions:**
```bash
# Verify .env file exists
cat .env

# Check API key format (should start with sk-)
echo $OPENAI_API_KEY

# Test API key manually
curl https://api.openai.com/v1/models \
  -H "Authorization: Bearer $OPENAI_API_KEY"

# Restart with new key
docker-compose restart pentestai-api
```

### ArvanCloud Authentication Failed

**Error:**
```
401 Unauthorized
```

**Solution:**
```bash
# ArvanCloud needs "apikey" prefix
# In .env:
ARVANCLOUD_API_KEY=your-token
OPENAI_BASE_URL=https://api.arvancloud.ir/llm/v1

# Controller will automatically add "apikey " prefix
# Set use_apikey_auth=True in config
```

### Rate Limit Exceeded

**Error:**
```
429 Too Many Requests
```

**Solutions:**
- Wait 60 seconds and retry
- Reduce `max_iterations` in config
- Upgrade OpenAI tier: https://platform.openai.com/account/limits
- Use slower temperature (doesn't help with rate limits)

## MCP Server Issues

### Kali MCP Not Accessible

**Error:**
```
Connection refused: http://host.docker.internal:5000
```

**Solutions:**
```bash
# Verify Kali is running
docker-compose ps kali-mcp-server

# Check Kali logs
docker logs kali-mcp-server

# Test from host
curl http://localhost:5000/health

# Test from API container
docker exec pentestai-api curl http://host.docker.internal:5000/health

# Restart Kali
docker-compose restart kali-mcp-server
```

### MCP Tools Not Found

**Error:**
```
Tool 'nmap' not available
```

**Solution:**
```bash
# List available tools
curl http://localhost:5000/tools/list

# Rebuild Kali container
docker-compose build kali-mcp-server
docker-compose up -d kali-mcp-server
```

## UI Issues

### React UI Blank Screen

**Symptoms:**
Browser shows blank page at http://localhost:3000

**Solutions:**
```bash
# Check container logs
docker logs pentestai-react-ui

# Look for errors
docker logs pentestai-react-ui 2>&1 | grep -i error

# Rebuild UI
docker-compose build pentestai-react-ui
docker-compose up -d pentestai-react-ui

# Check browser console (F12)
```

### API Connection Failed in UI

**Error:**
"Failed to connect to API"

**Solutions:**
```bash
# Verify API is running
curl http://localhost:8000/api/health

# Check CORS settings
# Should allow localhost:3000

# Check network
docker network inspect pentestai-network

# Restart both services
docker-compose restart pentestai-api pentestai-react-ui
```

### Streaming Not Working

**Symptoms:**
UI shows "Starting..." but no updates

**Solutions:**
```bash
# Check API logs
docker logs -f pentestai-api

# Test SSE manually
curl -N -X POST http://localhost:8000/api/pentest/stream \
  -H "Content-Type: application/json" \
  -d '{"target":"test","mode":"full","maxRounds":1}'

# Check browser network tab for SSE connection
```

## Python Issues

### Import Errors

**Error:**
```python
ModuleNotFoundError: No module named 'pentestai'
```

**Solution:**
```bash
# Install in development mode
pip install -e .

# Or install directly
pip install -r requirements.txt
```

### Configuration Errors

**Error:**
```
ValueError: Target cannot be empty
```

**Solution:**
```python
# Ensure all required fields are set
config = PentestAIConfig(
    target="192.168.1.100",  # Required!
    openai_api_key="sk-...",  # Required!
)

# Validate before using
errors = config.validate()
if errors:
    print(errors)
```

## Performance Issues

### Slow Execution

**Symptoms:**
Assessment takes > 30 minutes

**Solutions:**
```python
# Reduce iterations
config.max_iterations = 20  # From 50

# Reduce counterfactual rounds
config.counterfactual_rounds = 1  # From 3

# Use faster models
config.utility_model = "gpt-3.5-turbo"  # From gpt-4

# Disable features
config.use_instructor = False  # Skip RAG
config.enable_optimization = False  # Skip Group Knapsack
```

### High Memory Usage

**Symptoms:**
Container using > 4GB RAM

**Solutions:**
```yaml
# docker-compose.yml
services:
  pentestai-api:
    deploy:
      resources:
        limits:
          memory: 2G
```

## Documentation Issues

### Docsify Not Starting

**Error:**
```
docsify-cli: command not found
```

**Solution:**
```bash
# Install docsify-cli globally
npm install -g docsify-cli

# Or use npx (no install needed)
npx docsify-cli serve docs --port 3001
```

### Documentation Not Loading

**Symptoms:**
http://localhost:3001 shows 404

**Solutions:**
```bash
# Check you're in correct directory
ls docs/  # Should show README.md

# Start from project root
cd /path/to/PentestAI
npx docsify-cli serve docs --port 3001

# Use helper script
.\start_docs.ps1  # Windows
./start_docs.sh   # Linux/Mac
```

## Common Configuration Mistakes

### Sandbox Mode Off by Mistake

**Risk:** Real commands executed!

**Prevention:**
```python
# ALWAYS explicitly set
config = PentestAIConfig(
    sandbox_mode=True,  # Default is True, but be explicit
)

# Check before running
assert config.sandbox_mode == True, "Sandbox must be enabled!"
```

### Wrong MCP URL

**Error:**
```
Connection refused: http://localhost:5000
```

**Fix:**
```python
# From inside Docker container, use:
config.kali_mcp_url = "http://host.docker.internal:5000"

# From host machine, use:
config.kali_mcp_url = "http://localhost:5000"
```

### Missing API Key Prefix

**Error:**
```
ArvanCloud: 401 Unauthorized
```

**Fix:**
```python
config = PentestAIConfig(
    openai_api_key="your-token",
    openai_base_url="https://api.arvancloud.ir/llm/v1",
    use_apikey_auth=True,  # This adds "apikey " prefix
)
```

## Getting More Help

If you're still stuck:

1. **Check Logs:**
   ```bash
   docker-compose logs -f
   ```

2. **GitHub Issues:**
   - Search existing: https://github.com/pentestai/pentestai/issues
   - Create new issue with logs and config

3. **Documentation:**
   - Re-read relevant sections at http://localhost:3001
   - Check examples: [docs/examples/](examples/)

4. **Community:**
   - Discord: https://discord.gg/pentestai
   - Discussion: https://github.com/pentestai/pentestai/discussions

5. **Enable Debug Mode:**
   ```python
   import logging
   logging.basicConfig(level=logging.DEBUG)
   ```

## Diagnostic Checklist

Before asking for help, try this checklist:

```bash
# ✅ Services running?
docker-compose ps

# ✅ Logs clean?
docker-compose logs | grep -i error

# ✅ API healthy?
curl http://localhost:8000/api/health

# ✅ Kali healthy?
curl http://localhost:5000/health

# ✅ API key set?
echo $OPENAI_API_KEY | wc -c  # Should be > 40

# ✅ Network working?
docker network inspect pentestai-network

# ✅ Disk space free?
docker system df

# ✅ Latest version?
git pull origin main

# ✅ Config valid?
python -c "from pentestai import PentestAIConfig; config = PentestAIConfig(target='test'); print(config.validate())"
```

Include this checklist output when asking for help!

---

Still having issues? [Create an issue](https://github.com/pentestai/pentestai/issues/new) with:
- Operating system
- Docker version
- Error messages
- Logs
- Configuration (sanitize API keys!)
