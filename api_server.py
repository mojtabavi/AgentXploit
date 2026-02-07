"""
PentestAI FastAPI Backend with Streaming LLM Support
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import asyncio
import json
import logging
import os
import queue
from typing import AsyncGenerator

from pentestai.core.config import PentestAIConfig
from pentestai.core.controller import PentestAIController
from pentestai.llm.client import OpenAIClient

logger = logging.getLogger(__name__)

app = FastAPI(title="PentestAI API")

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global configuration
llm_client = None
controller = None


class PentestRequest(BaseModel):
    target: str
    mode: str = "recon"


class ChatMessage(BaseModel):
    message: str
    history: list = []


class ConversationState:
    """Track conversation state for pentesting intent"""
    def __init__(self):
        self.target = None
        self.mode = None
        self.confirmed = False


def check_llm_connection() -> bool:
    """Check if LLM is connected and working"""
    try:
        if not llm_client:
            return False
        
        # Quick test with higher max_tokens for ArvanCloud
        response = llm_client.generate(
            prompt="ping",
            system_prompt="Respond with only 'pong'",
            max_tokens=50
        )
        # Check if response exists (content may be empty but API works)
        return response is not None
    except Exception as e:
        print(f"LLM connection check failed: {e}")
        return False


@app.on_event("startup")
async def startup():
    """Initialize LLM client on startup"""
    global llm_client
    
    # Determine which provider to use based on environment
    arvan_endpoint = os.getenv("ARVANCLOUD_ENDPOINT")
    openai_base = os.getenv("OPENAI_BASE_URL")
    
    # Prioritize ArvanCloud if endpoint is set
    if arvan_endpoint:
        api_key = os.getenv("ARVANCLOUD_API_KEY")
        base_url = arvan_endpoint
        use_apikey_auth = True
    else:
        api_key = os.getenv("OPENAI_API_KEY")
        base_url = openai_base
        use_apikey_auth = False
    
    model = os.getenv("LLM_MODEL", "gpt-4")
    
    # Check if token is embedded in URL (ArvanCloud gateway pattern)
    token_in_url = base_url and "/gateway/models/" in base_url
    
    if not api_key and not token_in_url:
        print("⚠️  No API key found in environment")
        return
    
    try:
        llm_client = OpenAIClient(
            api_key=api_key,
            model=model,
            base_url=base_url,
            use_apikey_auth=use_apikey_auth,
            token_in_url=token_in_url,
        )
        print(f"✅ LLM client initialized: {model}")
        if token_in_url:
            print(f"   Using token-in-URL authentication (ArvanCloud gateway)")
        elif use_apikey_auth:
            print(f"   Using apikey authentication (ArvanCloud)")
        else:
            print(f"   Using Bearer authentication (OpenAI)")
    except Exception as e:
        print(f"❌ Failed to initialize LLM: {e}")


@app.get("/api/health")
async def health_check():
    """Health check endpoint with LLM connection status"""
    llm_connected = check_llm_connection()
    
    return {
        "status": "ok",
        "llm_connected": llm_connected,
        "llm_model": llm_client.model if llm_client else None,
    }


async def stream_pentest_response(target: str, mode: str) -> AsyncGenerator[str, None]:
    """Stream pentest progress to client"""
    
    def send_message(content: str) -> str:
        """Helper to format SSE messages"""
        return f"data: {json.dumps({'content': content})}\n\n"

    def send_stage(stage: str) -> str:
        """Helper to format SSE stage messages"""
        return f"data: {json.dumps({'stage': stage})}\n\n"

    def send_comment(comment: str) -> str:
        """Helper to format SSE comment messages"""
        return f"data: {json.dumps({'comment': comment})}\n\n"

    def send_tool_event(payload: dict) -> str:
        """Helper to format SSE tool output messages"""
        return f"data: {json.dumps(payload)}\n\n"
    
    def send_error(error: str) -> str:
        """Helper to format SSE error messages"""
        return f"data: {json.dumps({'error': error})}\n\n"
    
    llm_available = check_llm_connection()
    if not llm_available:
        yield send_comment('LLM unavailable, using mock mode for planning')
    
    try:
        # Step 1: Initialize
        yield send_stage('Initializing')
        yield send_message('🔍 **Initializing PentestAI...**\n\n')
        await asyncio.sleep(0.5)
        
        # Check connection
        yield send_message('✅ LLM connection verified\n\n')
        await asyncio.sleep(0.3)
        
        # Step 2: Create configuration
        yield send_message(f'🎯 **Target:** {target}\n')
        yield send_message(f'📊 **Mode:** {mode}\n\n')
        await asyncio.sleep(0.5)
        
        mode_map = {
            'auto': 'full',
            'scan_only': 'pentest',
            'interactive': 'pentest',
        }
        
        event_queue: "queue.Queue[dict]" = queue.Queue()

        def event_handler(payload: dict) -> None:
            event_queue.put(payload)

        llm_api_key = llm_client.api_key if llm_available and llm_client else None
        llm_base_url = llm_client.base_url if llm_client else None

        config = PentestAIConfig(
            target=target,
            openai_api_key=llm_api_key,
            openai_base_url=llm_base_url,
            use_apikey_auth=getattr(llm_client, 'use_apikey_auth', False),
            sandbox_mode=True,
            use_mcp=True,
            mcp_only=True,
            kali_mcp_url=os.getenv("KALI_MCP_URL", "http://host.docker.internal:5000"),
            event_handler=event_handler,
        )
        yield send_comment(f"MCP: using {config.kali_mcp_url}")
        
        # Step 3: Check LLM before controller init
        yield send_message('🔌 **Checking LLM connection...**\n')
        if llm_available:
            if not check_llm_connection():
                yield send_error('LLM connection lost')
                yield "data: [DONE]\n\n"
                return
            yield send_message('✅ LLM ready\n\n')
        else:
            yield send_message('⚠️ LLM unavailable, using mock mode\n\n')
        await asyncio.sleep(0.3)
        
        # Step 4: Initialize controller
        yield send_message('🚀 **Starting pentest controller...**\n\n')
        controller = PentestAIController(config)
        await asyncio.sleep(0.5)
        
        # Step 5: Run assessment
        if mode_map.get(mode, 'pentest') == 'full':
            yield send_message('📊 **Phase 1: Vulnerability Discovery**\n\n')
            await asyncio.sleep(0.5)
            
            # Check LLM before Phase 1
            if llm_available and not check_llm_connection():
                yield send_error('LLM connection lost before Phase 1')
                yield "data: [DONE]\n\n"
                return
            
            yield send_stage('Scanning')
            yield send_comment('MCP: running scan tools')

            pentest_task = asyncio.create_task(asyncio.to_thread(controller.run_full_assessment))
            while not pentest_task.done() or not event_queue.empty():
                try:
                    event = event_queue.get_nowait()
                    event_type = event.get("type")
                    if event_type == "tool_start":
                        yield send_stage('Scanning')
                        yield send_tool_event({"tool_start": event})
                    elif event_type == "tool_output":
                        yield send_tool_event({"tool_output": event})
                except queue.Empty:
                    await asyncio.sleep(0.1)

            pentest_result, remediation_result = await pentest_task
            
            yield send_stage('Enumerating')
            vuln_count = len(pentest_result.vulnerabilities)
            yield send_message(f'✅ **Found {vuln_count} vulnerabilities**\n\n')
            yield send_comment(f"MCP: scan finished with {vuln_count} findings")
            await asyncio.sleep(0.5)
            
            # Display vulnerabilities
            for i, vuln in enumerate(pentest_result.vulnerabilities[:5], 1):
                yield send_message(f'{i}. **{vuln.name}** ({vuln.severity.value})\n')
                desc = vuln.description[:100]
                yield send_message(f'   {desc}...\n\n')
                await asyncio.sleep(0.2)
            
            # Check LLM before Phase 2
            yield send_stage('Reporting')
            yield send_message('\n🔧 **Phase 2: Remediation Planning**\n\n')
            if llm_available and not check_llm_connection():
                yield send_error('LLM connection lost before Phase 2')
                yield "data: [DONE]\n\n"
                return
            
            await asyncio.sleep(0.5)
            strategy_count = len(remediation_result.selected_strategies)
            yield send_message(f'✅ **Generated {strategy_count} remediation strategies**\n\n')
            
            for i, strategy in enumerate(remediation_result.selected_strategies[:5], 1):
                yield send_message(f'{i}. **{strategy.title}**\n')
                yield send_message(f'   Priority: {strategy.priority}\n\n')
                await asyncio.sleep(0.2)
        
        else:
            # Single phase
            yield send_stage('Scanning')
            yield send_message('🔍 **Running vulnerability scan...**\n\n')
            await asyncio.sleep(0.5)
            
            # Check LLM before scan
            if llm_available and not check_llm_connection():
                yield send_error('LLM connection lost before scan')
                yield "data: [DONE]\n\n"
                return
            
            yield send_comment('MCP: running scan tools')

            pentest_task = asyncio.create_task(asyncio.to_thread(controller.run_pentest))
            while not pentest_task.done() or not event_queue.empty():
                try:
                    event = event_queue.get_nowait()
                    event_type = event.get("type")
                    if event_type == "tool_start":
                        yield send_stage('Scanning')
                        yield send_tool_event({"tool_start": event})
                    elif event_type == "tool_output":
                        yield send_tool_event({"tool_output": event})
                except queue.Empty:
                    await asyncio.sleep(0.1)

            result = await pentest_task
            
            yield send_stage('Reporting')
            vuln_count = len(result.vulnerabilities)
            yield send_message(f'✅ **Scan complete! Found {vuln_count} vulnerabilities**\n\n')
            yield send_comment(f"MCP: scan finished with {vuln_count} findings")
            await asyncio.sleep(0.5)
            
            for i, vuln in enumerate(result.vulnerabilities[:10], 1):
                yield send_message(f'{i}. **{vuln.name}** ({vuln.severity.value})\n')
                yield send_message(f'   {vuln.description}\n\n')
                await asyncio.sleep(0.2)
        
        # Final message
        yield send_message('\n✅ **Assessment complete!**\n')
        yield send_message('Results saved to pentestai_results/\n')
        
    except Exception as e:
        yield send_error(str(e))
    
    finally:
        yield "data: [DONE]\n\n"


async def stream_chat_response(message: str, history: list) -> AsyncGenerator[str, None]:
    """Stream conversational chat responses with intent extraction"""
    
    def send_message(content: str) -> str:
        """Helper to format SSE messages"""
        return f"data: {json.dumps({'content': content})}\n\n"

    def send_stage(stage: str) -> str:
        """Helper to format SSE stage messages"""
        return f"data: {json.dumps({'stage': stage})}\n\n"

    def send_comment(comment: str) -> str:
        """Helper to format SSE comment messages"""
        return f"data: {json.dumps({'comment': comment})}\n\n"
    
    def send_error(error: str) -> str:
        """Helper to format SSE error messages"""
        return f"data: {json.dumps({'error': error})}\n\n"
    
    # Check LLM connection
    if not check_llm_connection():
        yield send_error('LLM not connected')
        yield "data: [DONE]\n\n"
        return
    
    try:
        # Build conversation context
        conversation = []
        for msg in history[-10:]:  # Keep last 10 messages
            if msg.get('role') in ['user', 'assistant']:
                conversation.append(f"{msg['role']}: {msg['content']}")
        
        conversation.append(f"user: {message}")
        context = "\n".join(conversation)
        
        # System prompt for conversational pentesting assistant
        system_prompt = """You are PentestAI, a friendly and helpful AI penetration testing assistant.

Your role is to have natural conversations with users about their pentesting needs and help them:
1. Understand what they want to test
2. Identify the target (IP address, domain, or network range)
3. Determine the appropriate scan mode
4. Confirm before starting any tests

Available scan modes:
- **auto**: Full comprehensive assessment (scan + vulnerability analysis + remediation)
- **scan_only**: Quick vulnerability scan only
- **interactive**: Interactive pentesting with you

Guidelines:
- Be conversational and friendly, not robotic
- Ask for missing information naturally
- Validate IP addresses and domains
- Explain what each mode does if asked
- Confirm target and mode before indicating readiness to start
- Be security-conscious and ethical

If the user wants to start a pentest and you have both target and mode:
- Summarize what you'll do
- End your message with: "Ready to proceed? Say 'yes' or 'start' when ready."

If user confirms (says yes, start, go, etc.), respond with:
"Starting [mode] assessment on [target] now..."

Then the system will automatically start the actual pentest.

Be helpful, clear, and professional."""
        
        # Generate response using LLM
        yield send_stage('Thinking')
        response = llm_client.generate(
            prompt=context,
            system_prompt=system_prompt,
            max_tokens=500
        )
        response_text = response.content if hasattr(response, 'content') else str(response)
        logger.info(
            "LLM response generated (%s chars)",
            len(response_text),
        )
        
        # Stream the response character by character for smooth effect
        content = response_text
        # Stream character by character
        for char in content:
            yield send_message(char)
            await asyncio.sleep(0.01)
        
        # Check if we should auto-start pentest
        # Look for confirmation patterns in the user's message
        lower_msg = message.lower().strip()
        confirmation_words = ['yes', 'start', 'go', 'proceed', 'ok', 'sure', 'yeah']
        
        if any(word in lower_msg for word in confirmation_words):
            # Check last assistant message for target/mode information
            for msg in reversed(history[-5:]):
                if msg.get('role') == 'assistant':
                    content = msg.get('content', '').lower()
                    # Look for patterns like "scan 192.168.1.1" or "full assessment on example.com"
                    if 'ready to proceed' in content or 'ready?' in content:
                        # Extract target from conversation history
                        # This is a simple extraction - could be enhanced
                        import re
                        ip_pattern = r'\b(?:\d{1,3}\.){3}\d{1,3}\b'
                        target_match = re.search(ip_pattern, ' '.join([m.get('content', '') for m in history[-5:]]))
                        
                        if target_match:
                            target = target_match.group(0)
                            # Determine mode from explicit context first
                            mode = 'auto'  # Default
                            full_context = ' '.join([m.get('content', '').lower() for m in history[-5:]])
                            mode_match = re.search(r"mode:\s*(auto|scan_only|interactive)", full_context)
                            if mode_match:
                                mode = mode_match.group(1)
                            elif 'scan only' in full_context or 'quick scan' in full_context:
                                mode = 'scan_only'
                            elif 'interactive' in full_context:
                                mode = 'interactive'
                            
                            # Signal to start pentest
                            yield send_message('\n\n---\n\n')
                            yield send_message('🚀 **Starting pentest now...**\n\n')
                            yield send_stage('Scanning')
                            yield send_comment(f"MCP: scheduling {mode} scan on {target}")
                            # The actual pentest will be triggered by the frontend
                        break
    
    except Exception as e:
        yield send_error(f"Error: {str(e)}")
    
    finally:
        yield "data: [DONE]\n\n"


@app.post("/api/chat")
async def chat(request: ChatMessage):
    """Handle conversational chat with intent extraction"""
    
    if not llm_client:
        raise HTTPException(status_code=503, detail="LLM not initialized")
    
    return StreamingResponse(
        stream_chat_response(request.message, request.history),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
        }
    )


@app.post("/api/pentest/stream")
async def pentest_stream(request: PentestRequest):
    """Stream pentest execution with real-time updates"""
    
    if not llm_client:
        raise HTTPException(status_code=503, detail="LLM not initialized")
    
    return StreamingResponse(
        stream_pentest_response(request.target, request.mode),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
        }
    )


@app.get("/")
async def root():
    """Root endpoint"""
    return {"message": "PentestAI API is running"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
