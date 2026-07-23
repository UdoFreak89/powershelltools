#!/usr/bin/env python3
"""
AI Battle - Real-time streaming!
See the text letter by letter as the AI writes it - including thinking.
"""

import requests
import json
import sys
import os
import time
from typing import Optional, Tuple

# ==============================================================
#  STREAMING - real-time display
# ==============================================================

def stream_print(text, prefix="", color_end=""):
    """Prints text in real-time character by character"""
    for char in text:
        print(char, end="", flush=True)
        time.sleep(0.01)  # A little slowdown to make it readable

def print_thinking_stream(thinking_text, label="Thinking"):
    """Real-time display of thinking"""
    if not thinking_text:
        return
    lines = thinking_text.strip().split("\n")
    print(f"\n   +---- [BRAIN] {label} " + "-" * (40 - len(label)) + "+")
    for line in lines:
        print(f"   | ", end="", flush=True)
        stream_print(line)
        print()
    print(f"   +" + "-" * 50 + "+")

def print_response_stream(response_text, label="Response"):
    """Real-time display of response"""
    if not response_text:
        return
    lines = response_text.strip().split("\n")
    print(f"\n   /[RESPONSE] {label} " + "=" * (40 - len(label)) + "\\")
    for line in lines:
        print(f"   || ", end="", flush=True)
        stream_print(line)
        print()
    print(f"   \\" + "=" * 50 + "/")

class StreamPrinter:
    """Enables real-time printing of streamed data"""
    def __init__(self):
        self.thinking_buffer = ""
        self.response_buffer = ""
        self.in_thinking = False
        self.printing_thinking = False
        self.printing_response = False
        self.thinking_started = False
        self.response_started = False
    
    def start_thinking(self, label="Thinking"):
        if not self.thinking_started:
            print(f"\n   +---- [BRAIN] {label} " + "-" * 40 + "+")
            self.thinking_started = True
            self.in_thinking = True
    
    def add_thinking(self, token):
        if token:
            self.thinking_buffer += token
            print(f"   | ", end="", flush=True) if not self.printing_thinking else None
            self.printing_thinking = True
            print(token, end="", flush=True)
    
    def end_thinking(self):
        if self.thinking_started:
            print(f"\n   +" + "-" * 50 + "+")
            self.in_thinking = False
    
    def start_response(self, label="Response"):
        if not self.response_started:
            print(f"\n   /[RESPONSE] {label} " + "=" * 40 + "\\")
            self.response_started = True
    
    def add_response(self, token):
        if token:
            self.response_buffer += token
            print(f"   || ", end="", flush=True) if not self.printing_response else None
            self.printing_response = True
            print(token, end="", flush=True)
    
    def end_response(self):
        if self.response_started:
            print(f"\n   \\" + "=" * 50 + "/")
    
    def finish(self):
        self.end_thinking()
        self.end_response()

# ==============================================================
#  AI SERVICES - streaming version
# ==============================================================

class AIService:
    def __init__(self, name: str, api_key: str):
        self.name = name
        self.api_key = api_key
    
    def chat_stream(self, messages: list, model: str, printer: StreamPrinter):
        """Streams response through printer"""
        raise NotImplementedError


class OpenRouterService(AIService):
    BASE_URL = "https://openrouter.ai/api/v1"
    
    def __init__(self, api_key: str):
        super().__init__("OpenRouter", api_key)
    
    def get_models(self) -> list:
        try:
            r = requests.get(f"{self.BASE_URL}/models", timeout=15)
            if r.status_code == 200:
                models = r.json().get("data", [])
                chat_models = []
                for m in models:
                    mid = m["id"]
                    if any(x in mid for x in [
                        "gpt-4", "gpt-3.5", "o1", "o3", "o4",
                        "claude-3", "claude-4",
                        "gemini-1", "gemini-2",
                        "deepseek", "llama-3", "llama-4",
                        "qwen-2", "qwen-3",
                        "mistral", "mixtral",
                        "phi-4", "command-r",
                        "dbrx", "jamba",
                        "north-mini-code", "cohere",
                    ]):
                        chat_models.append(mid)
                return sorted(chat_models)
            return []
        except:
            return self._fallback_models()
    
    def _fallback_models(self):
        return [
            "openai/gpt-4o",
            "openai/gpt-4o-mini",
            "openai/o1",
            "anthropic/claude-3.5-sonnet",
            "anthropic/claude-3-haiku",
            "google/gemini-2.0-flash-001",
            "google/gemini-1.5-pro",
            "deepseek/deepseek-chat",
            "deepseek/deepseek-r1",
            "meta-llama/llama-3.1-405b-instruct",
            "mistralai/mistral-large-latest",
            "cohere/north-mini-code:free",
        ]
    
    def chat_stream(self, messages: list, model: str, printer: StreamPrinter):
        try:
            r = requests.post(
                f"{self.BASE_URL}/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                    "HTTP-Referer": "https://github.com/ai-battle",
                    "X-Title": "AI Battle Arena"
                },
                json={
                    "model": model,
                    "messages": messages,
                    "max_tokens": 500,
                    "temperature": 0.8,
                    "stream": True
                },
                stream=True,
                timeout=60
            )
            
            thinking_done = False
            
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
                    
                    # Thinking/reasoning tokens
                    reasoning = delta.get("reasoning_content") or delta.get("reasoning")
                    if reasoning:
                        if not thinking_done:
                            printer.start_thinking(self.name)
                        printer.add_thinking(reasoning)
                    
                    # Response
                    content = delta.get("content")
                    if content:
                        if not printer.response_started:
                            printer.end_thinking()
                            printer.start_response(self.name)
                        printer.add_response(content)
                        
                except json.JSONDecodeError:
                    continue
            
            printer.finish()
            
        except Exception as e:
            print(f"\n   [Error: {e}]")


class DeepSeekService(AIService):
    BASE_URL = "https://api.deepseek.com"
    
    def __init__(self, api_key: str):
        super().__init__("DeepSeek", api_key)
    
    def get_models(self) -> list:
        try:
            r = requests.get(
                f"{self.BASE_URL}/models",
                headers={"Authorization": f"Bearer {self.api_key}"},
                timeout=10
            )
            if r.status_code == 200:
                return [m["id"] for m in r.json().get("data", [])]
            return []
        except:
            return ["deepseek-chat", "deepseek-reasoner"]
    
    def chat_stream(self, messages: list, model: str, printer: StreamPrinter):
        try:
            r = requests.post(
                f"{self.BASE_URL}/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": model,
                    "messages": messages,
                    "max_tokens": 500,
                    "temperature": 0.8,
                    "stream": True
                },
                stream=True,
                timeout=60
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
                            printer.start_thinking(self.name)
                        printer.add_thinking(reasoning)
                    
                    content = delta.get("content")
                    if content:
                        if not printer.response_started:
                            printer.end_thinking()
                            printer.start_response(self.name)
                        printer.add_response(content)
                        
                except json.JSONDecodeError:
                    continue
            
            printer.finish()
            
        except Exception as e:
            print(f"\n   [Error: {e}]")


class OpenAIService(AIService):
    BASE_URL = "https://api.openai.com/v1"
    
    def __init__(self, api_key: str):
        super().__init__("OpenAI", api_key)
    
    def get_models(self) -> list:
        try:
            r = requests.get(
                f"{self.BASE_URL}/models",
                headers={"Authorization": f"Bearer {self.api_key}"},
                timeout=10
            )
            if r.status_code == 200:
                models = r.json()["data"]
                chat_models = [m["id"] for m in models 
                              if any(x in m["id"] for x in ["gpt", "o1", "o3", "o4"])]
                return sorted(chat_models)
            return []
        except:
            return ["gpt-4o", "gpt-4o-mini", "gpt-4-turbo", "o1", "o3-mini"]
    
    def chat_stream(self, messages: list, model: str, printer: StreamPrinter):
        try:
            is_reasoning = any(x in model for x in ["o1", "o3", "o4"])
            
            payload = {
                "model": model,
                "messages": messages,
                "max_tokens": 500,
                "stream": True
            }
            
            if not is_reasoning:
                payload["temperature"] = 0.8
            
            r = requests.post(
                f"{self.BASE_URL}/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                },
                json=payload,
                stream=True,
                timeout=120
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
                            printer.start_thinking(self.name)
                        printer.add_thinking(reasoning)
                    
                    content = delta.get("content")
                    if content:
                        if not printer.response_started:
                            printer.end_thinking()
                            printer.start_response(self.name)
                        printer.add_response(content)
                        
                except json.JSONDecodeError:
                    continue
            
            printer.finish()
            
        except Exception as e:
            print(f"\n   [Error: {e}]")


class AnthropicService(AIService):
    BASE_URL = "https://api.anthropic.com/v1"
    
    def __init__(self, api_key: str):
        super().__init__("Anthropic", api_key)
    
    def get_models(self) -> list:
        try:
            r = requests.get(
                f"{self.BASE_URL}/models",
                headers={
                    "x-api-key": self.api_key,
                    "anthropic-version": "2023-06-01"
                },
                timeout=10
            )
            if r.status_code == 200:
                models = r.json().get("data", [])
                return [m["id"] for m in models]
            return []
        except:
            return ["claude-3-5-sonnet-20241022", "claude-3-5-haiku-20241022", "claude-3-opus-20240229"]
    
    def chat_stream(self, messages: list, model: str, printer: StreamPrinter):
        try:
            system_msg = ""
            chat_messages = []
            for m in messages:
                if m["role"] == "system":
                    system_msg = m["content"]
                else:
                    chat_messages.append(m)
            
            payload = {
                "model": model,
                "messages": chat_messages,
                "max_tokens": 500,
                "stream": True
            }
            if system_msg:
                payload["system"] = system_msg
            
            if any(x in model for x in ["3-5", "3.5", "claude-4"]):
                payload["thinking"] = {
                    "type": "enabled",
                    "budget_tokens": 200
                }
            
            r = requests.post(
                f"{self.BASE_URL}/messages",
                headers={
                    "x-api-key": self.api_key,
                    "anthropic-version": "2023-06-01",
                    "Content-Type": "application/json"
                },
                json=payload,
                stream=True,
                timeout=120
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
                    event_type = event.get("type", "")
                    
                    if event_type == "content_block_delta":
                        delta = event.get("delta", {})
                        
                        if delta.get("type") == "thinking_delta":
                            thinking = delta.get("thinking", "")
                            if thinking:
                                if not printer.thinking_started:
                                    printer.start_thinking(self.name)
                                printer.add_thinking(thinking)
                        
                        elif delta.get("type") == "text_delta":
                            text = delta.get("text", "")
                            if text:
                                if not printer.response_started:
                                    printer.end_thinking()
                                    printer.start_response(self.name)
                                printer.add_response(text)
                                
                except json.JSONDecodeError:
                    continue
            
            printer.finish()
            
        except Exception as e:
            print(f"\n   [Error: {e}]")


class GoogleService(AIService):
    BASE_URL = "https://generativelanguage.googleapis.com/v1beta"
    
    def __init__(self, api_key: str):
        super().__init__("Google", api_key)
    
    def get_models(self) -> list:
        try:
            r = requests.get(
                f"{self.BASE_URL}/models?key={self.api_key}",
                timeout=10
            )
            if r.status_code == 200:
                models = r.json().get("models", [])
                return [m["name"].split("/")[-1] for m in models 
                       if "generateContent" in m.get("supportedGenerationMethods", [])]
            return []
        except:
            return ["gemini-2.0-flash", "gemini-1.5-pro", "gemini-1.5-flash"]
    
    def chat_stream(self, messages: list, model: str, printer: StreamPrinter):
        try:
            contents = []
            for m in messages:
                if m["role"] != "system":
                    role = "user" if m["role"] == "user" else "model"
                    contents.append({"role": role, "parts": [{"text": m["content"]}]})
            
            generation_config = {"responseMimeType": "text/plain"}
            if "2.5" in model:
                generation_config["thinkingConfig"] = {"thinkingBudget": 200}
            
            payload = {
                "contents": contents,
                "generationConfig": generation_config
            }
            
            r = requests.post(
                f"{self.BASE_URL}/models/{model}:streamGenerateContent?key={self.api_key}",
                headers={"Content-Type": "application/json"},
                json=payload,
                stream=True,
                timeout=120
            )
            
            for line in r.iter_lines():
                if not line:
                    continue
                line = line.decode("utf-8", errors="ignore")
                
                try:
                    chunk = json.loads(line)
                    candidate = chunk.get("candidates", [{}])[0]
                    parts = candidate.get("content", {}).get("parts", [])
                    
                    for part in parts:
                        if part.get("thought"):
                            text = part.get("text", "")
                            if text:
                                if not printer.thinking_started:
                                    printer.start_thinking(self.name)
                                printer.add_thinking(text)
                        elif "text" in part:
                            text = part.get("text", "")
                            if text:
                                if not printer.response_started:
                                    printer.end_thinking()
                                    printer.start_response(self.name)
                                printer.add_response(text)
                                
                except json.JSONDecodeError:
                    continue
            
            printer.finish()
            
        except Exception as e:
            print(f"\n   [Error: {e}]")


# ==============================================================
#  PROVIDERS
# ==============================================================

PROVIDERS = {
    "1": {"name": "OpenRouter", "cls": OpenRouterService, "desc": "100+ models (GPT, Claude, Gemini, DeepSeek, Llama...)"},
    "2": {"name": "DeepSeek", "cls": DeepSeekService, "desc": "deepseek-chat, deepseek-reasoner"},
    "3": {"name": "OpenAI", "cls": OpenAIService, "desc": "GPT-4o, GPT-4, o1, o3"},
    "4": {"name": "Anthropic", "cls": AnthropicService, "desc": "Claude 3.5, Claude 3, Claude 4"},
    "5": {"name": "Google", "cls": GoogleService, "desc": "Gemini 1.5, 2.0"},
}


def clear():
    os.system("cls" if os.name == "nt" else "clear")

def print_banner():
    print("""
+================================================================+
|                    [BATTLE] AI BATTLE ARENA                     |
|         Real-time streaming - see text as the AI writes it!     |
+================================================================+

   LEGEND:
   +---- [BRAIN] ... +   = What the AI is thinking (reasoning) - real-time
   /[RESPONSE] ...  \\   = What the AI responds - real-time

    """)

def select_provider(label: str = "") -> str:
    print(f"\n{'=' * 20} {label} {'=' * 20}")
    print("Select AI provider:\n")
    for key, p in PROVIDERS.items():
        print(f"  {key}. {p['name']:12} - {p['desc']}")
    print()
    
    while True:
        choice = input(">> Choice [1-5]: ").strip()
        if choice in PROVIDERS:
            return choice
        print("Invalid choice!")

def get_api_key(provider_name: str) -> Optional[str]:
    key = input(f"\nAPI key for {provider_name}: ").strip()
    if not key:
        return None
    return key

def create_service(choice: str, api_key: str) -> AIService:
    return PROVIDERS[choice]["cls"](api_key)

def select_model(service: AIService) -> Optional[str]:
    print(f"\nLoading models for {service.name}...")
    models = service.get_models()
    
    if not models:
        print("Failed to load models, enter manually")
        model = input("Model name: ").strip()
        return model if model else None
    
    print(f"\nAvailable models ({len(models)}):\n")
    for i, m in enumerate(models, 1):
        tag = ""
        if any(x in m for x in ["o1", "o3", "o4", "r1", "reasoner", "thinking", "2.5", "3-5", "north-mini"]):
            tag = " [THINK]"
        print(f"  {i:3}. {m}{tag}")
    
    print(f"\n  [THINK] = model with reasoning/thinking")
    print(f"  (or enter model name manually)")
    
    while True:
        choice = input(f"\n>> Select model [1-{len(models)}]: ").strip()
        
        if not choice.isdigit():
            return choice if choice else None
        
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(models):
                return models[idx]
        except ValueError:
            pass
        print("Invalid choice!")

def get_topic() -> str:
    print("\nWhat should the AIs debate about?")
    print("  Examples:")
    print("    - Is pizza better than hamburgers?")
    print("    - Does free will exist?")
    print("    - Who is better - Python or JavaScript?")
    print("    - What is the meaning of life?")
    print("    - Are AIs a threat to humanity?")
    print()
    topic = input(">> Topic: ").strip()
    return topic or "Tell me something interesting about yourself"

def run_battle(ai1_service, ai1_model, ai2_service, ai2_model, topic, rounds=5):
    clear()
    print_banner()
    print(f"[START] BATTLE STARTS!")
    print(f"   AI 1: {ai1_service.name:12} {ai1_model}")
    print(f"          VS")
    print(f"   AI 2: {ai2_service.name:12} {ai2_model}")
    print(f"\n   Topic: {topic}")
    print(f"   Rounds: {rounds}")
    print()
    print("=" * 60)
    
    conversation_ai1 = [
        {"role": "system", "content": f"You are an AI named {ai1_service.name}. You are debating on the topic: {topic}. Reply briefly (2-3 sentences), be witty and original. Don't start with an introduction."},
        {"role": "user", "content": f"Start the debate on the topic: {topic}. Share your first opinion."}
    ]
    
    conversation_ai2 = [
        {"role": "system", "content": f"You are an AI named {ai2_service.name}. You are debating on the topic: {topic}. Reply briefly (2-3 sentences), be witty and original. React to the previous argument."},
        {"role": "user", "content": f"[Waiting for opponent's first reply]"}
    ]
    
    # AI 1 starts
    print(f"\n>>> AI 1: {ai1_service.name} ({ai1_model})")
    printer1 = StreamPrinter()
    ai1_service.chat_stream(conversation_ai1, ai1_model, printer1)
    if printer1.thinking_buffer:
        conversation_ai2.append({"role": "user", "content": f"Your opponent said: {printer1.response_buffer}. How do you respond?"})
    
    for round_num in range(1, rounds + 1):
        time.sleep(0.3)
        
        # AI 2 responds
        print(f"\n>>> AI 2: {ai2_service.name} ({ai2_model})")
        printer2 = StreamPrinter()
        ai2_service.chat_stream(conversation_ai2, ai2_model, printer2)
        conversation_ai1.append({"role": "user", "content": f"Your opponent said: {printer2.response_buffer}. Respond."})
        conversation_ai2.append({"role": "assistant", "content": printer2.response_buffer})
        
        time.sleep(0.3)
        
        if round_num < rounds:
            # AI 1 responds
            print(f"\n>>> AI 1: {ai1_service.name} ({ai1_model})")
            printer1 = StreamPrinter()
            ai1_service.chat_stream(conversation_ai1, ai1_model, printer1)
            conversation_ai2.append({"role": "user", "content": f"Your opponent said: {printer1.response_buffer}. Respond."})
            conversation_ai1.append({"role": "assistant", "content": printer1.response_buffer})
        
        print("\n" + "-" * 60)
    
    print("\n[END] BATTLE ENDS!")
    print(f"   AI 1: {ai1_service.name} ({ai1_model})")
    print(f"   AI 2: {ai2_service.name} ({ai2_model})")
    print(f"   Topic: {topic}\n")

def main():
    while True:
        clear()
        print_banner()
        
        # --- AI 1 ---
        provider1 = select_provider("AI 1")
        api_key1 = get_api_key(PROVIDERS[provider1]["name"])
        if not api_key1:
            print("No API key provided!")
            input("Press Enter to continue...")
            continue
        
        service1 = create_service(provider1, api_key1)
        model1 = select_model(service1)
        if not model1:
            print("No model selected!")
            input("Press Enter to continue...")
            continue
        
        # --- AI 2 (can be same provider!) ---
        provider2 = select_provider("AI 2")
        api_key2 = get_api_key(PROVIDERS[provider2]["name"])
        if not api_key2:
            print("No API key provided!")
            input("Press Enter to continue...")
            continue
        
        service2 = create_service(provider2, api_key2)
        model2 = select_model(service2)
        if not model2:
            print("No model selected!")
            input("Press Enter to continue...")
            continue
        
        # --- Topic ---
        topic = get_topic()
        
        # --- Number of rounds ---
        rounds_input = input("\nNumber of rounds (Enter = 5): ").strip()
        rounds = int(rounds_input) if rounds_input.isdigit() and int(rounds_input) > 0 else 5
        
        # --- BATTLE ---
        run_battle(service1, model1, service2, model2, topic, rounds)
        
        again = input("Another battle? [y/N]: ").strip().lower()
        if again != "y":
            print("\nThanks for watching!\n")
            break

if __name__ == "__main__":
    main()
