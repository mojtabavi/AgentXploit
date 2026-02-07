# REST API Reference

FastAPI-based REST API with real-time streaming for PentestAI framework.

## Base URL

```
http://localhost:8000
```

## Authentication

Currently no authentication required (designed for local use). For production, add:

```python
from fastapi.security import HTTPBearer

security = HTTPBearer()

@app.post("/api/pentest/stream")
async def start_pentest(request: PentestRequest, token: str = Depends(security)):
    # Validate token
    ...
```

## Endpoints

### Health Check

Check API server health and LLM connection.

**Endpoint:** `GET /api/health`

**Response:**
```json
{
  "status": "healthy",
  "llm_model": "gpt-4",
  "version": "1.0.0",
  "timestamp": "2024-02-06T12:34:56.789Z"
}
```

**Example:**
```bash
curl http://localhost:8000/api/health
```

```python
import requests

response = requests.get("http://localhost:8000/api/health")
print(response.json())
```

### Start Pentest (Streaming)

Start a penetration test with real-time streaming updates.

**Endpoint:** `POST /api/pentest/stream`

**Request Body:**
```json
{
  "target": "192.168.1.100",
  "mode": "full",
  "maxRounds": 5
}
```

**Parameters:**
- `target` (string, **required**): Target IP/hostname/URL
- `mode` (string): Pentest mode
  - `"auto"` or `"full"`: Full assessment (pentest + remediation)
  - `"scan_only"` or `"pentest"`: Pentest only
  - `"interactive"` or `"pentest"`: Interactive mode (same as scan_only)
- `maxRounds` (integer): Maximum iterations (default: 5)

**Response:** Server-Sent Events (SSE) stream

**Event Types:**

1. **Connection Check**
```json
{
  "type": "connection_check",
  "status": "connected",
  "model": "gpt-4"
}
```

2. **Phase Updates**
```json
{
  "type": "phase",
  "phase": "initialization",
  "message": "Initializing PentestAI controller..."
}
```

Available phases:
- `initialization`: Setting up controller
- `phase_1`: Running pentest module
- `phase_2`: Running remediation module
- `scan`: Scanning target (pentest only)

3. **Progress Updates**
```json
{
  "type": "progress",
  "message": "Planner agent generating attack plan...",
  "details": {
    "current_round": 3,
    "max_rounds": 5
  }
}
```

4. **Results**
```json
{
  "type": "result",
  "data": {
    "vulnerabilities": [...],
    "remediation_strategies": [...],
    "statistics": {...}
  }
}
```

5. **Errors**
```json
{
  "type": "error",
  "error": "Connection to LLM failed",
  "details": "Invalid API key"
}
```

**Example: cURL**
```bash
curl -X POST http://localhost:8000/api/pentest/stream \
  -H "Content-Type: application/json" \
  -d '{
    "target": "192.168.1.100",
    "mode": "full",
    "maxRounds": 5
  }' \
  --no-buffer
```

**Example: Python (requests)**
```python
import requests
import json

url = "http://localhost:8000/api/pentest/stream"
data = {
    "target": "192.168.1.100",
    "mode": "full",
    "maxRounds": 5
}

response = requests.post(url, json=data, stream=True)

for line in response.iter_lines():
    if line:
        line_str = line.decode('utf-8')
        if line_str.startswith('data: '):
            event_data = json.loads(line_str[6:])
            
            if event_data["type"] == "progress":
                print(f"📝 {event_data['message']}")
            elif event_data["type"] == "result":
                print("✅ Assessment complete!")
                print(f"Vulnerabilities: {len(event_data['data']['vulnerabilities'])}")
            elif event_data["type"] == "error":
                print(f"❌ Error: {event_data['error']}")
```

**Example: JavaScript (Fetch API)**
```javascript
const response = await fetch('http://localhost:8000/api/pentest/stream', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    target: '192.168.1.100',
    mode: 'full',
    maxRounds: 5,
  }),
});

const reader = response.body.getReader();
const decoder = new TextDecoder();

while (true) {
  const { value, done } = await reader.read();
  if (done) break;
  
  const chunk = decoder.decode(value);
  const lines = chunk.split('\n');
  
  for (const line of lines) {
    if (line.startsWith('data: ')) {
      const event = JSON.parse(line.slice(6));
      
      if (event.type === 'progress') {
        console.log(`📝 ${event.message}`);
      } else if (event.type === 'result') {
        console.log('✅ Complete!');
        console.log('Vulnerabilities:', event.data.vulnerabilities);
      }
    }
  }
}
```

**Example: React Component**
```jsx
import { useState } from 'react';

function PentestStream() {
  const [messages, setMessages] = useState([]);
  const [isRunning, setIsRunning] = useState(false);

  const startPentest = async () => {
    setIsRunning(true);
    setMessages([]);

    const response = await fetch('http://localhost:8000/api/pentest/stream', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        target: '192.168.1.100',
        mode: 'full',
        maxRounds: 5,
      }),
    });

    const reader = response.body.getReader();
    const decoder = new TextDecoder();

    while (true) {
      const { value, done } = await reader.read();
      if (done) break;

      const chunk = decoder.decode(value);
      const lines = chunk.split('\n');

      for (const line of lines) {
        if (line.startsWith('data: ')) {
          const event = JSON.parse(line.slice(6));
          
          if (event.type === 'progress') {
            setMessages(prev => [...prev, event.message]);
          } else if (event.type === 'result') {
            setMessages(prev => [...prev, 'Assessment complete!']);
            setIsRunning(false);
          }
        }
      }
    }
  };

  return (
    <div>
      <button onClick={startPentest} disabled={isRunning}>
        Start Pentest
      </button>
      <div>
        {messages.map((msg, i) => <div key={i}>{msg}</div>)}
      </div>
    </div>
  );
}
```

## Data Models

### PentestRequest

```typescript
interface PentestRequest {
  target: string;      // Required: IP/hostname/URL
  mode: string;        // "full", "scan_only", "interactive"
  maxRounds: number;   // Max iterations (default: 5)
}
```

### Vulnerability

```typescript
interface Vulnerability {
  id: string;
  name: string;
  description: string;
  severity: "CRITICAL" | "HIGH" | "MEDIUM" | "LOW" | "INFO";
  cvss_score: number;  // 0.0-10.0
  cve_id?: string;
  service: string;
  port?: number;
  exploit_method: string;
  discovered_at: string;  // ISO 8601
  metadata: Record<string, any>;
}
```

### RemediationStrategy

```typescript
interface RemediationStrategy {
  id: string;
  vulnerability_id: string;
  name: string;
  description: string;
  remediation_type: "patch" | "reconfigure" | "monitor" | "isolate" | "compensating_control";
  cost: number;
  effectiveness: number;  // 0.0-1.0
  implementation_time: string;
  required_skills: string[];
  metadata: Record<string, any>;
}
```

### Result

```typescript
interface Result {
  vulnerabilities: Vulnerability[];
  remediation_strategies: RemediationStrategy[];
  statistics: {
    duration_seconds: number;
    tasks_executed: number;
    counterfactual_rounds: number;
    optimization_score: number;
  };
  attack_plan?: any;  // Optional attack tree
}
```

## Error Responses

All errors follow this format:

```json
{
  "type": "error",
  "error": "Error message",
  "details": "Additional context"
}
```

**Common Errors:**

| Error | Cause | Solution |
|-------|-------|----------|
| `LLM connection failed` | Invalid API key | Check `OPENAI_API_KEY` in `.env` |
| `Target cannot be empty` | Missing target | Provide valid target in request |
| `Invalid mode` | Unknown mode | Use "full", "scan_only", or "interactive" |
| `Configuration error` | Invalid config | Check all required settings |
| `MCP server unreachable` | Kali MCP down | Verify `docker-compose ps` |

## Rate Limits

No rate limits on the API server itself. However, LLM providers have limits:

**OpenAI:**
- Free tier: 3 requests/minute
- Tier 1: 60 requests/minute
- See: https://platform.openai.com/account/limits

**ArvanCloud:**
- Check your plan limits

## CORS Configuration

CORS is enabled for local development:

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React UI
    allow_methods=["*"],
    allow_headers=["*"],
)
```

For production, restrict origins:

```python
allow_origins=["https://yourdomain.com"]
```

## WebSocket Alternative (Future)

For lower latency, WebSocket support is planned:

```python
@app.websocket("/ws/pentest")
async def pentest_ws(websocket: WebSocket):
    await websocket.accept()
    # Real-time bidirectional communication
```

## API Versioning

Current version: `v1` (implicit in `/api/*`)

Future versions will use explicit prefixes:
- `/api/v1/*`
- `/api/v2/*`

## Complete Integration Example

```python
#!/usr/bin/env python3
"""Complete REST API integration example."""

import requests
import json
import time

API_BASE = "http://localhost:8000"

def check_health():
    """Check API health."""
    response = requests.get(f"{API_BASE}/api/health")
    if response.status_code == 200:
        data = response.json()
        print(f"✅ API healthy - Model: {data['llm_model']}")
        return True
    else:
        print("❌ API unhealthy")
        return False

def run_pentest(target: str, mode: str = "full", max_rounds: int = 5):
    """Run penetration test with streaming."""
    print(f"\n🔍 Starting pentest on {target}...")
    print(f"   Mode: {mode}")
    print(f"   Max Rounds: {max_rounds}")
    print("-" * 60)
    
    url = f"{API_BASE}/api/pentest/stream"
    data = {
        "target": target,
        "mode": mode,
        "maxRounds": max_rounds
    }
    
    response = requests.post(url, json=data, stream=True)
    
    vulnerabilities = []
    strategies = []
    
    for line in response.iter_lines():
        if line:
            line_str = line.decode('utf-8')
            if line_str.startswith('data: '):
                event = json.loads(line_str[6:])
                
                if event["type"] == "connection_check":
                    print(f"🔗 Connection: {event['status']}")
                    
                elif event["type"] == "phase":
                    print(f"\n📍 {event['phase'].upper()}: {event['message']}")
                    
                elif event["type"] == "progress":
                    print(f"   {event['message']}")
                    
                elif event["type"] == "result":
                    print("\n✅ Assessment Complete!")
                    vulnerabilities = event["data"]["vulnerabilities"]
                    strategies = event["data"].get("remediation_strategies", [])
                    
                    print(f"\n📊 Results:")
                    print(f"   Vulnerabilities: {len(vulnerabilities)}")
                    print(f"   Remediation Strategies: {len(strategies)}")
                    
                    if "statistics" in event["data"]:
                        stats = event["data"]["statistics"]
                        print(f"   Duration: {stats.get('duration_seconds', 0):.1f}s")
                    
                elif event["type"] == "error":
                    print(f"\n❌ Error: {event['error']}")
                    if "details" in event:
                        print(f"   Details: {event['details']}")
    
    print("-" * 60)
    return vulnerabilities, strategies

def main():
    # 1. Check health
    if not check_health():
        print("API is not ready. Start with: docker-compose up -d")
        return
    
    # 2. Run full assessment
    vulnerabilities, strategies = run_pentest(
        target="192.168.1.100",
        mode="full",
        max_rounds=5
    )
    
    # 3. Display vulnerabilities
    if vulnerabilities:
        print("\n🔴 Top Vulnerabilities:")
        for vuln in sorted(vulnerabilities, key=lambda v: v["cvss_score"], reverse=True)[:5]:
            print(f"   • {vuln['name']}")
            print(f"     Severity: {vuln['severity']} (CVSS {vuln['cvss_score']})")
            print(f"     Service: {vuln['service']}")
    
    # 4. Display remediation
    if strategies:
        print("\n✅ Recommended Actions:")
        for strategy in strategies[:5]:
            print(f"   • {strategy['name']}")
            print(f"     Type: {strategy['remediation_type']}")
            print(f"     Cost: {strategy['cost']:.1f}, Effectiveness: {strategy['effectiveness']:.1%}")

if __name__ == "__main__":
    main()
```

## Testing

```bash
# Start API server
docker-compose up -d pentestai-api

# Health check
curl http://localhost:8000/api/health

# Stream pentest
curl -X POST http://localhost:8000/api/pentest/stream \
  -H "Content-Type: application/json" \
  -d '{"target":"192.168.1.100","mode":"full","maxRounds":5}' \
  --no-buffer

# View logs
docker logs -f pentestai-api
```

## Monitoring

```python
# Add Prometheus metrics
from prometheus_fastapi_instrumentator import Instrumentator

instrumentator = Instrumentator()
instrumentator.instrument(app).expose(app)

# Metrics at /metrics
```

---

See also:
- [Python API Reference](python-api.md)
- [Data Models](data-models.md)
- [React UI Integration](../ui/react-ui.md)
