import { useEffect, useRef, useState } from 'react'
import ReactMarkdown from 'react-markdown'
import remarkGfm from 'remark-gfm'
import parseHtml from 'html-react-parser'
import { useLLMOutput } from '@llm-ui/react'
import { markdownLookBack } from '@llm-ui/markdown'
import {
  allLangs,
  allLangsAlias,
  codeBlockLookBack,
  findCompleteCodeBlock,
  findPartialCodeBlock,
  loadHighlighter,
  useCodeBlockToHtml,
} from '@llm-ui/code'
import { bundledThemes } from 'shiki/themes'
import { getHighlighterCore } from 'shiki/core'
import { bundledLanguagesInfo } from 'shiki/langs'
import getWasm from 'shiki/wasm'
import './App.css'

const highlighter = loadHighlighter(
  getHighlighterCore({
    langs: allLangs(bundledLanguagesInfo),
    langAlias: allLangsAlias(bundledLanguagesInfo),
    themes: Object.values(bundledThemes),
    loadWasm: getWasm,
  }),
)

const MarkdownBlock = ({ blockMatch }) => {
  const markdown = blockMatch.output || ''
  return <ReactMarkdown remarkPlugins={[remarkGfm]}>{markdown}</ReactMarkdown>
}

const CodeBlock = ({ blockMatch }) => {
  const { html, code } = useCodeBlockToHtml({
    markdownCodeBlock: blockMatch.output,
    highlighter,
    codeToHtmlOptions: { theme: 'github-dark' },
  })

  if (!html) {
    return (
      <pre className="code-fallback">
        <code>{code}</code>
      </pre>
    )
  }

  return <div className="code-block">{parseHtml(html)}</div>
}

const AssistantMessage = ({ content, isStreaming }) => {
  const { blockMatches } = useLLMOutput({
    llmOutput: content || '',
    fallbackBlock: {
      component: MarkdownBlock,
      lookBack: markdownLookBack(),
    },
    blocks: [
      {
        component: CodeBlock,
        findCompleteMatch: findCompleteCodeBlock(),
        findPartialMatch: findPartialCodeBlock(),
        lookBack: codeBlockLookBack(),
      },
    ],
    isStreamFinished: !isStreaming,
  })

  return (
    <div className="assistant-message">
      {blockMatches.map((blockMatch, index) => {
        const Component = blockMatch.block.component
        return <Component key={index} blockMatch={blockMatch} />
      })}
      {isStreaming && <span className="cursor">▊</span>}
    </div>
  )
}

function App() {
  const [connected, setConnected] = useState(false)
  const [connectionStatus, setConnectionStatus] = useState('checking')
  const [messages, setMessages] = useState([])
  const [userInput, setUserInput] = useState('')
  const [isStreaming, setIsStreaming] = useState(false)
  const [streamingMessage, setStreamingMessage] = useState('')
  const [stage, setStage] = useState('Idle')
  const [pendingComments, setPendingComments] = useState([])
  const [pendingToolOutputs, setPendingToolOutputs] = useState([])
  const messagesEndRef = useRef(null)
  const apiBaseUrl = import.meta.env.VITE_API_URL || '/api'

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages, streamingMessage])

  useEffect(() => {
    checkConnection()
    const interval = setInterval(() => {
      if (!connected) {
        checkConnection()
      }
    }, 5000)
    return () => clearInterval(interval)
  }, [connected])

  const checkConnection = async () => {
    try {
      setConnectionStatus('checking')
      const response = await fetch(`${apiBaseUrl}/health`, {
        method: 'GET',
        headers: { Accept: 'application/json' },
      })

      if (!response.ok) {
        throw new Error(`HTTP ${response.status}`)
      }

      const data = await response.json()
      if (data.llm_connected) {
        setConnected(true)
        setConnectionStatus('connected')
      } else {
        setConnected(false)
        setConnectionStatus('llm_disconnected')
      }
    } catch (error) {
      console.error('Connection check failed:', error)
      setConnected(false)
      setConnectionStatus('api_disconnected')
    }
  }

  const streamSse = async ({ url, body, initialStage }) => {
    setIsStreaming(true)
    setStreamingMessage('')
    setStage(initialStage)
    setPendingComments([])
    setPendingToolOutputs([])

    let localComments = []
    let localToolOutputs = []

    try {
      const response = await fetch(url, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body),
      })

      if (!response.ok) {
        throw new Error(`HTTP ${response.status}`)
      }

      if (!response.body) {
        throw new Error('No response body received')
      }

      const reader = response.body.getReader()
      const decoder = new TextDecoder()
      let buffer = ''
      let fullMessage = ''

      while (true) {
        const { done, value } = await reader.read()
        if (done) break

        buffer += decoder.decode(value, { stream: true })
        const lines = buffer.split('\n')
        buffer = lines.pop()

        for (const line of lines) {
          if (!line.startsWith('data: ')) continue

          const data = line.slice(6)
          if (data === '[DONE]') {
            if (fullMessage) {
              setMessages((prev) => [
                ...prev,
                {
                  role: 'assistant',
                  content: fullMessage,
                  timestamp: Date.now(),
                  comments: localComments,
                  toolOutputs: localToolOutputs,
                },
              ])
            }
            setStreamingMessage('')
            setIsStreaming(false)
            setStage('Idle')
            setPendingComments([])
            setPendingToolOutputs([])
          } else {
            try {
              const json = JSON.parse(data)
              if (json.stage) {
                setStage(json.stage)
              }
              if (json.comment) {
                localComments = [...localComments, json.comment]
                setPendingComments(localComments)
              }
              if (json.tool_output) {
                localToolOutputs = [...localToolOutputs, json.tool_output]
                setPendingToolOutputs(localToolOutputs)
              }
              if (json.tool_start) {
                localToolOutputs = [...localToolOutputs, { ...json.tool_start, output: '' }]
                setPendingToolOutputs(localToolOutputs)
              }
              if (json.content) {
                fullMessage += json.content
                setStreamingMessage(fullMessage)
                setStage((current) => (current === 'Idle' ? 'Responding' : current))
              }
            } catch (e) {
              console.error('Parse error:', e)
            }
          }
        }
      }
    } catch (error) {
      setMessages((prev) => [
        ...prev,
        {
          role: 'system',
          content: `Error: ${error.message}`,
          timestamp: Date.now(),
        },
      ])
      setIsStreaming(false)
      setStage('Idle')
      setPendingComments([])
      setPendingToolOutputs([])
    }
  }

  const sendMessage = async () => {
    const message = userInput.trim()
    if (!message || isStreaming || !connected) return

    const nextHistory = [
      ...messages.map((entry) => ({ role: entry.role, content: entry.content })),
      { role: 'user', content: message },
    ]

    setMessages((prev) => [
      ...prev,
      {
        role: 'user',
        content: message,
        timestamp: Date.now(),
      },
    ])
    setUserInput('')

    await streamSse({
      url: `${apiBaseUrl}/chat`,
      body: { message, history: nextHistory },
      initialStage: 'Analyzing request',
    })
  }

  const parseConfirmation = (text) => {
    const lower = text.toLowerCase()
    if (!lower.includes('ready to proceed')) return null

    const modeMatch = lower.match(/mode:\s*(auto|scan_only|interactive)/)
    const mode = modeMatch ? modeMatch[1] : 'scan_only'
    const ipMatch = text.match(/\b(?:\d{1,3}\.){3}\d{1,3}\b/)
    const target = ipMatch ? ipMatch[0] : null

    return target ? { target, mode } : null
  }

  const startPentest = async (target, mode) => {
    if (!target || !mode || isStreaming || !connected) return

    setMessages((prev) => [
      ...prev,
      {
        role: 'user',
        content: 'start',
        timestamp: Date.now(),
      },
    ])

    await streamSse({
      url: `${apiBaseUrl}/pentest/stream`,
      body: { target, mode },
      initialStage: 'Scanning',
    })
  }

  const handleKeyDown = (event) => {
    if (event.key === 'Enter' && !event.shiftKey) {
      event.preventDefault()
      sendMessage()
    }
  }

  const getStatusMessage = () => {
    switch (connectionStatus) {
      case 'checking':
        return { text: 'Connecting', color: 'rgba(255, 193, 7, 0.9)' }
      case 'connected':
        return { text: 'Ready', color: 'rgba(76, 175, 80, 0.9)' }
      case 'llm_disconnected':
        return { text: 'LLM Offline', color: 'rgba(244, 67, 54, 0.9)' }
      case 'api_disconnected':
        return { text: 'API Offline', color: 'rgba(244, 67, 54, 0.9)' }
      default:
        return { text: 'Unknown', color: 'rgba(158, 158, 158, 0.9)' }
    }
  }

  const status = getStatusMessage()

  return (
    <div className="app">
      <header className="header">
        <div className="header-inner">
          <span className="brand-mark">PentestAI</span>
          <div className="status-pill" style={{ color: status.color }}>
            <span className="status-dot" style={{ backgroundColor: status.color }} />
            <span>{status.text}</span>
          </div>
        </div>
      </header>

      <main className="chat-shell">
        <div className="chat-body">
          {messages.length === 0 && !streamingMessage && (
            <div className="chat-empty">
              <div className="chat-empty-title">Start a session</div>
              <div className="chat-empty-text">
                Example: "Scan 10.0.0.12 for open ports and summarize risks."
              </div>
            </div>
          )}

          {messages.map((message, index) => (
            <div key={index} className={`message ${message.role}`}>
              <div className="message-meta">{message.role === 'user' ? 'You' : 'PentestAI'}</div>
              {message.role === 'user' ? (
                <div className="message-bubble user-bubble">{message.content}</div>
              ) : (
                <div className="message-bubble assistant-bubble">
                  <AssistantMessage content={message.content} isStreaming={false} />
                  {(() => {
                    const confirmation = parseConfirmation(message.content)
                    if (!confirmation) return null
                    return (
                      <div className="confirm-actions">
                        <button
                          className="confirm-button"
                          onClick={() => startPentest(confirmation.target, confirmation.mode)}
                          disabled={isStreaming || !connected}
                        >
                          Start {confirmation.mode}
                        </button>
                        <button
                          className="confirm-button ghost"
                          onClick={() => setUserInput('')}
                          disabled={isStreaming}
                        >
                          Cancel
                        </button>
                      </div>
                    )
                  })()}
                  {message.comments?.length > 0 && (
                    <div className="comment-list">
                      {message.comments.map((comment, commentIndex) => (
                        <div key={commentIndex} className="comment-line">
                          # {comment}
                        </div>
                      ))}
                    </div>
                  )}
                  {message.toolOutputs?.length > 0 && (
                    <div className="tool-output-list">
                      {message.toolOutputs.map((toolOutput, toolIndex) => (
                        <details key={toolIndex} className="tool-output">
                          <summary>
                            Tool output: {toolOutput.tool || 'unknown'} {toolOutput.task_id ? `(${toolOutput.task_id})` : ''}
                          </summary>
                          <pre>{toolOutput.output || 'Output not available yet.'}</pre>
                        </details>
                      ))}
                    </div>
                  )}
                </div>
              )}
            </div>
          ))}

          {streamingMessage && (
            <div className="message assistant">
              <div className="message-meta">PentestAI</div>
              <div className="stage-indicator">Stage: {stage}</div>
              <div className="message-bubble assistant-bubble">
                <AssistantMessage content={streamingMessage} isStreaming={true} />
                {pendingComments.length > 0 && (
                  <div className="comment-list">
                    {pendingComments.map((comment, commentIndex) => (
                      <div key={commentIndex} className="comment-line">
                        # {comment}
                      </div>
                    ))}
                  </div>
                )}
                {pendingToolOutputs.length > 0 && (
                  <div className="tool-output-list">
                    {pendingToolOutputs.map((toolOutput, toolIndex) => (
                      <details key={toolIndex} className="tool-output">
                        <summary>
                          Tool output: {toolOutput.tool || 'unknown'} {toolOutput.task_id ? `(${toolOutput.task_id})` : ''}
                        </summary>
                        <pre>{toolOutput.output || 'Running...'}</pre>
                      </details>
                    ))}
                  </div>
                )}
              </div>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>

        <div className="chat-input">
          <textarea
            className="input"
            value={userInput}
            onChange={(event) => setUserInput(event.target.value)}
            onKeyDown={handleKeyDown}
            placeholder={connected ? 'Send a message...' : status.text}
            disabled={!connected || isStreaming}
            rows={2}
          />
          <button
            className="send"
            onClick={sendMessage}
            disabled={!connected || !userInput.trim() || isStreaming}
          >
            {isStreaming ? 'Working...' : 'Send'}
          </button>
        </div>

        {!connected && (
          <div className="chat-warning">
            {connectionStatus === 'api_disconnected'
              ? 'API server is not running or unreachable from Docker.'
              : 'LLM connection failed. Check the API configuration.'}
          </div>
        )}
      </main>
    </div>
  )
}

export default App
