#!/usr/bin/env python3
"""
AI Battle Quick - Real-time streaming
"""

import sys
import os
import time
import json
import requests

class StreamPrinter:
    """Real-time printing of streamed data"""
    def __init__(self):
        self.thinking_started = False
        self.response_started = False
        self.thinking_buffer = ""
        self.response_buffer = ""
        self.printing_thinking = False
        self.printing_response = False
    
    def start_thinking(self, label="Thinking"):
        if not self.thinking_started:
            print(f"\n   +---- [BRAIN] {label} " + "-" * 40 + "+")
            self.thinking_started = True
    
    def add_thinking(self, token):
        if token:
            self.thinking_buffer += token
            if not self.printing_thinking:
                self.printing_thinking = True
            print(token, end="", flush=True)
    
    def end_thinking(self):
        if self.thinking_started:
            print(f"\n   +" + "-" * 50 + "+")
    
    def start_response(self, label="Response"):
        if not self.response_started:
            print(f"\n   /[RESPONSE] {label} " + "=" * 40 + "\\")
            self.response_started = True
    
    def add_response(self, token):
        if token:
            self.response_buffer += token
            if not self.printing_response:
                self.printing_response = True
            print(token, end="", flush=True)
    
    def end_response(self):
        if self.response_started:
            print(f"\n   \\" + "=" * 50 + "/")
    
    def finish(self):
        self.end_thinking()
        self.end_response()

def stream_openrouter(api_key, model, messages, printer):
    r = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://github.com/ai-battle"
        },
        json={"model": model, "messages": messages, "max_tokens": 300, "temperature": 0.8, "stream": True},
        stream=True,
        timeout=30
    )
    
    for line in r.iter_lines():
        if not line:
            continue
        line = line.decode("utf-8", errors="ignore")
        if not line.startswith("data: "):
            continue
        data = line[6:]
        if data.strip() == "[DONE]":
            break
        try:
            chunk = json.loads(data)
            delta = chunk.get("choices", [{}])[0].get("delta", {})
            reasoning = delta.get("reasoning_content") or delta.get("reasoning")
            if reasoning:
                if not printer.thinking_started:
                    printer.start_thinking(model)
                printer.add_thinking(reasoning)
            content = delta.get("content")
            if content:
                if not printer.response_started:
                    printer.end_thinking()
                    printer.start_response(model)
                printer.add_response(content)
        except:
            continue
    printer.finish()

def stream_openai(api_key, model, messages, printer):
    r = requests.post(
        "https://api.openai.com/v1/chat/completions",
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        json={"model": model, "messages": messages, "max_tokens": 300, "temperature": 0.8, "stream": True},
        stream=True,
        timeout=30
    )
    for line in r.iter_lines():
        if not line:
            continue
        line = line.decode("utf-8", errors="ignore")
        if not line.startswith("data: "):
            continue
        data = line[6:]
        if data.strip() == "[DONE]":
            break
        try:
            chunk = json.loads(data)
            delta = chunk.get("choices", [{}])[0].get("delta", {})
            reasoning = delta.get("reasoning_content") or delta.get("reasoning")
            if reasoning:
                if not printer.thinking_started:
                    printer.start_thinking(model)
                printer.add_thinking(reasoning)
            content = delta.get("content")
            if content:
                if not printer.response_started:
                    printer.end_thinking()
                    printer.start_response(model)
                printer.add_response(content)
        except:
            continue
    printer.finish()

def stream_anthropic(api_key, model, messages, printer):
    system = next((m["content"] for m in messages if m["role"] == "system"), "")
    msgs = [m for m in messages if m["role"] != "system"]
    payload = {"model": model, "messages": msgs, "max_tokens": 300, "stream": True}
    if system:
        payload["system"] = system
    r = requests.post(
        "https://api.anthropic.com/v1/messages",
        headers={"x-api-key": api_key, "anthropic-version": "2023-06-01", "Content-Type": "application/json"},
        json=payload,
        stream=True,
        timeout=30
    )
    for line in r.iter_lines():
        if not line:
            continue
        line = line.decode("utf-8", errors="ignore")
        if not line.startswith("data: "):
            continue
        data = line[6:]
        try:
            event = json.loads(data)
            if event.get("type") == "content_block_delta":
                delta = event.get("delta", {})
                if delta.get("type") == "thinking_delta":
                    t = delta.get("thinking", "")
                    if t:
                        if not printer.thinking_started:
                            printer.start_thinking(model)
                        printer.add_thinking(t)
                elif delta.get("type") == "text_delta":
                    t = delta.get("text", "")
                    if t:
                        if not printer.response_started:
                            printer.end_thinking()
                            printer.start_response(model)
                        printer.add_response(t)
        except:
            continue
    printer.finish()

def stream_deepseek(api_key, model, messages, printer):
    r = requests.post(
        "https://api.deepseek.com/chat/completions",
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        json={"model": model, "messages": messages, "max_tokens": 300, "temperature": 0.8, "stream": True},
        stream=True,
        timeout=30
    )
    for line in r.iter_lines():
        if not line:
            continue
        line = line.decode("utf-8", errors="ignore")
        if not line.startswith("data: "):
            continue
        data = line[6:]
        if data.strip() == "[DONE]":
            break
        try:
            chunk = json.loads(data)
            delta = chunk.get("choices", [{}])[0].get("delta", {})
            reasoning = delta.get("reasoning_content") or delta.get("reasoning")
            if reasoning:
                if not printer.thinking_started:
                    printer.start_thinking(model)
                printer.add_thinking(reasoning)
            content = delta.get("content")
            if content:
                if not printer.response_started:
                    printer.end_thinking()
                    printer.start_response(model)
                printer.add_response(content)
        except:
            continue
    printer.finish()

def stream_google(api_key, model, messages, printer):
    contents = [{"role": "user" if m["role"] == "user" else "model", "parts": [{"text": m["content"]}]} 
                for m in messages if m["role"] != "system"]
    payload = {"contents": contents, "generationConfig": {"responseMimeType": "text/plain"}}
    r = requests.post(
        f"https://generativelanguage.googleapis.com/v1beta/models/{model}:streamGenerateContent?key={api_key}",
        headers={"Content-Type": "application/json"},
        json=payload,
        stream=True,
        timeout=30
    )
    for line in r.iter_lines():
        if not line:
            continue
        line = line.decode("utf-8", errors="ignore")
        try:
            chunk = json.loads(line)
            parts = chunk.get("candidates", [{}])[0].get("content", {}).get("parts", [])
            for part in parts:
                if part.get("thought"):
                    t = part.get("text", "")
                    if t:
                        if not printer.thinking_started:
                            printer.start_thinking(model)
                        printer.add_thinking(t)
                elif "text" in part:
                    t = part.get("text", "")
                    if t:
                        if not printer.response_started:
                            printer.end_thinking()
                            printer.start_response(model)
                        printer.add_response(t)
        except:
            continue
    printer.finish()

STREAM_FNS = {
    "openrouter": stream_openrouter,
    "openai": stream_openai,
    "anthropic": stream_anthropic,
    "deepseek": stream_deepseek,
    "google": stream_google,
}

def main():
    if len(sys.argv) < 8:
        print("""
+====================================================+
|           AI BATTLE QUICK - STREAMING               |
+====================================================+

Usage:
  python ai_quick.py <p1> <key1> <model1> <p2> <key2> <model2> <topic>

Providers: openai, anthropo, google, deepseek, openrouter

Examples:
  python ai_quick.py openrouter "sk-or-xxx" openai/gpt-4o deepseek "sk-xxx" deepseek-chat "Is AI better than humans?"

  python ai_quick.py openrouter "sk-or-xxx" cohere/north-mini-code:free openai "sk-xxx" gpt-4o "Who is the better coder?"
""")
        sys.exit(1)
    
    p1, k1, m1, p2, k2, m2 = sys.argv[1:7]
    topic = " ".join(sys.argv[7:])
    
    if p1 not in STREAM_FNS or p2 not in STREAM_FNS:
        print(f"Unknown provider! Options: {', '.join(STREAM_FNS.keys())}")
        sys.exit(1)
    
    chat1 = STREAM_FNS[p1]
    chat2 = STREAM_FNS[p2]
    
    conv1 = [
        {"role": "system", "content": f"You are an AI. You are debating on the topic: {topic}. Reply briefly (2-3 sentences)."},
        {"role": "user", "content": f"Start the debate on the topic: {topic}"}
    ]
    conv2 = [
        {"role": "system", "content": f"You are an AI. You are debating on the topic: {topic}. Reply briefly (2-3 sentences)."},
    ]
    
    print(f"\n>>> {p1.upper()} ({m1}) VS {p2.upper()} ({m2})")
    print(f"    Topic: {topic}\n")
    print("=" * 60)
    
    # AI 1
    print(f"\n>>> AI 1: {p1.upper()} ({m1})")
    printer1 = StreamPrinter()
    chat1(k1, m1, conv1, printer1)
    conv2.append({"role": "user", "content": f"Your opponent said: {printer1.response_buffer}"})
    
    for i in range(4):
        time.sleep(0.3)
        
        # AI 2
        print(f"\n>>> AI 2: {p2.upper()} ({m2})")
        printer2 = StreamPrinter()
        chat2(k2, m2, conv2, printer2)
        conv1.append({"role": "user", "content": f"Your opponent said: {printer2.response_buffer}"})
        conv2.append({"role": "assistant", "content": printer2.response_buffer})
        
        time.sleep(0.3)
        
        # AI 1
        print(f"\n>>> AI 1: {p1.upper()} ({m1})")
        printer1 = StreamPrinter()
        chat1(k1, m1, conv1, printer1)
        conv2.append({"role": "user", "content": f"Your opponent said: {printer1.response_buffer}"})
        conv1.append({"role": "assistant", "content": printer1.response_buffer})
        print("\n" + "-" * 60)
    
    print("\n[END] END!")

if __name__ == "__main__":
    main()
