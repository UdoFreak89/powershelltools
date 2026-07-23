#!/usr/bin/env python3
"""
AI Battle - Real-time streaming!
Vidis text pismenko po pismenku jak ho AI pise - vcetne thinkingu.
"""

import requests
import json
import sys
import os
import time
from typing import Optional, Tuple

# ==============================================================
#  STREAMING - real-time zobrazeni
# ==============================================================

def stream_print(text, prefix="", color_end=""):
    """Vypise text real-time znak po znaku"""
    for char in text:
        print(char, end="", flush=True)
        time.sleep(0.01)  # Trochu zpomaleni at je to citelne

def print_thinking_stream(thinking_text, label="Premyslim"):
    """Real-time zobrazeni thinkingu"""
    if not thinking_text:
        return
    lines = thinking_text.strip().split("\n")
    print(f"\n   +---- [BRAIN] {label} " + "-" * (40 - len(label)) + "+")
    for line in lines:
        print(f"   | ", end="", flush=True)
        stream_print(line)
        print()
    print(f"   +" + "-" * 50 + "+")

def print_response_stream(response_text, label="Odpoved"):
    """Real-time zobrazeni odpovedi"""
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
    """Umoznuje real-time tisk streamovanych dat"""
    def __init__(self):
        self.thinking_buffer = ""
        self.response_buffer = ""
        self.in_thinking = False
        self.printing_thinking = False
        self.printing_response = False
        self.thinking_started = False
        self.response_started = False
    
    def start_thinking(self, label="Premyslim"):
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
    
    def start_response(self, label="Odpoved"):
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
#  AI SLUZBY - streaming verze
# ==============================================================

class AIService:
    def __init__(self, name: str, api_key: str):
        self.name = name
        self.api_key = api_key
    
    def chat_stream(self, messages: list, model: str, printer: StreamPrinter):
        """Streamuje odpoved pres printer"""
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
                    
                    # Thinking/reasoning tokeny
                    reasoning = delta.get("reasoning_content") or delta.get("reasoning")
                    if reasoning:
                        if not thinking_done:
                            printer.start_thinking(self.name)
                        printer.add_thinking(reasoning)
                    
                    # Odpoved
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
            print(f"\n   [Chyba: {e}]")


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
            print(f"\n   [Chyba: {e}]")


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
            print(f"\n   [Chyba: {e}]")


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
            print(f"\n   [Chyba: {e}]")


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
            print(f"\n   [Chyba: {e}]")


# ==============================================================
#  POSKYTOVATELE
# ==============================================================

PROVIDERS = {
    "1": {"name": "OpenRouter", "cls": OpenRouterService, "desc": "100+ modelu (GPT, Claude, Gemini, DeepSeek, Llama...)"},
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
|         Real-time streaming - vidis text jak ho AI pise!        |
+================================================================+

   LEGENDA:
   +---- [BRAIN] ... +   = Co AI premysli (reasoning) - real-time
   /[RESPONSE] ...  \\   = Co AI odpovi - real-time

    """)

def select_provider(label: str = "") -> str:
    print(f"\n{'=' * 20} {label} {'=' * 20}")
    print("Vyber poskytovatele AI:\n")
    for key, p in PROVIDERS.items():
        print(f"  {key}. {p['name']:12} - {p['desc']}")
    print()
    
    while True:
        choice = input(">> Volba [1-5]: ").strip()
        if choice in PROVIDERS:
            return choice
        print("Neplatna volba!")

def get_api_key(provider_name: str) -> Optional[str]:
    key = input(f"\nAPI klic pro {provider_name}: ").strip()
    if not key:
        return None
    return key

def create_service(choice: str, api_key: str) -> AIService:
    return PROVIDERS[choice]["cls"](api_key)

def select_model(service: AIService) -> Optional[str]:
    print(f"\nNacitam modely pro {service.name}...")
    models = service.get_models()
    
    if not models:
        print("Nepodarilo se nacist modely, zadaj rucne")
        model = input("Nazev modelu: ").strip()
        return model if model else None
    
    print(f"\nDostupne modely ({len(models)}):\n")
    for i, m in enumerate(models, 1):
        tag = ""
        if any(x in m for x in ["o1", "o3", "o4", "r1", "reasoner", "thinking", "2.5", "3-5", "north-mini"]):
            tag = " [THINK]"
        print(f"  {i:3}. {m}{tag}")
    
    print(f"\n  [THINK] = model s reasoning/thinking")
    print(f"  (nebo napis nazev modelu rucne)")
    
    while True:
        choice = input(f"\n>> Vyber model [1-{len(models)}]: ").strip()
        
        if not choice.isdigit():
            return choice if choice else None
        
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(models):
                return models[idx]
        except ValueError:
            pass
        print("Neplatna volba!")

def get_topic() -> str:
    print("\nO cem maji AI vest debatu?")
    print("  Priklady:")
    print("    - Je pizza lepsi nez hamburgery?")
    print("    - Existuje volna vule?")
    print("    - Kdo je lepsi - Python nebo JavaScript?")
    print("    - Jaky je smysl zivota?")
    print("    - Jsou AI hrozbou pro lidstvo?")
    print()
    topic = input(">> Tema: ").strip()
    return topic or "Rekni mi neco zajimaveho o sobe"

def run_battle(ai1_service, ai1_model, ai2_service, ai2_model, topic, rounds=5):
    clear()
    print_banner()
    print(f"[START] ZACINA BITVA!")
    print(f"   AI 1: {ai1_service.name:12} {ai1_model}")
    print(f"          VS")
    print(f"   AI 2: {ai2_service.name:12} {ai2_model}")
    print(f"\n   Tema: {topic}")
    print(f"   Kol: {rounds}")
    print()
    print("=" * 60)
    
    conversation_ai1 = [
        {"role": "system", "content": f"Jsi AI jmenem {ai1_service.name}. Vedes debatu na tema: {topic}. Odpovez strucne (2-3 vety), bud vtipny a originalni. Nezdrzuj se uvodem."},
        {"role": "user", "content": f"Zacni debatu na tema: {topic}. Rec svuj prvni nazor."}
    ]
    
    conversation_ai2 = [
        {"role": "system", "content": f"Jsi AI jmenem {ai2_service.name}. Vedes debatu na tema: {topic}. Odpovez strucne (2-3 vety), bud vtipny a originalni. Reaguj na predchozi argument."},
        {"role": "user", "content": f"[Cekam na prvni odpoved soupere]"}
    ]
    
    # AI 1 zacina
    print(f"\n>>> AI 1: {ai1_service.name} ({ai1_model})")
    printer1 = StreamPrinter()
    ai1_service.chat_stream(conversation_ai1, ai1_model, printer1)
    if printer1.thinking_buffer:
        conversation_ai2.append({"role": "user", "content": f"Tvuj soupe rekl: {printer1.response_buffer}. Jak na to reagujes?"})
    
    for round_num in range(1, rounds + 1):
        time.sleep(0.3)
        
        # AI 2 odpovida
        print(f"\n>>> AI 2: {ai2_service.name} ({ai2_model})")
        printer2 = StreamPrinter()
        ai2_service.chat_stream(conversation_ai2, ai2_model, printer2)
        conversation_ai1.append({"role": "user", "content": f"Tvuj soupe rekl: {printer2.response_buffer}. Reaguj."})
        conversation_ai2.append({"role": "assistant", "content": printer2.response_buffer})
        
        time.sleep(0.3)
        
        if round_num < rounds:
            # AI 1 odpovida
            print(f"\n>>> AI 1: {ai1_service.name} ({ai1_model})")
            printer1 = StreamPrinter()
            ai1_service.chat_stream(conversation_ai1, ai1_model, printer1)
            conversation_ai2.append({"role": "user", "content": f"Tvuj soupe rekl: {printer1.response_buffer}. Reaguj."})
            conversation_ai1.append({"role": "assistant", "content": printer1.response_buffer})
        
        print("\n" + "-" * 60)
    
    print("\n[END] KONEC BITVY!")
    print(f"   AI 1: {ai1_service.name} ({ai1_model})")
    print(f"   AI 2: {ai2_service.name} ({ai2_model})")
    print(f"   Tema: {topic}\n")

def main():
    while True:
        clear()
        print_banner()
        
        # --- AI 1 ---
        provider1 = select_provider("AI 1")
        api_key1 = get_api_key(PROVIDERS[provider1]["name"])
        if not api_key1:
            print("Nebyl zadan API klic!")
            input("Enter pro pokracovani...")
            continue
        
        service1 = create_service(provider1, api_key1)
        model1 = select_model(service1)
        if not model1:
            print("Nebyl vybran model!")
            input("Enter pro pokracovani...")
            continue
        
        # --- AI 2 (muze byt stejny provider!) ---
        provider2 = select_provider("AI 2")
        api_key2 = get_api_key(PROVIDERS[provider2]["name"])
        if not api_key2:
            print("Nebyl zadan API klic!")
            input("Enter pro pokracovani...")
            continue
        
        service2 = create_service(provider2, api_key2)
        model2 = select_model(service2)
        if not model2:
            print("Nebyl vybran model!")
            input("Enter pro pokracovani...")
            continue
        
        # --- Tema ---
        topic = get_topic()
        
        # --- Pocet kol ---
        rounds_input = input("\nPocet kol (Enter = 5): ").strip()
        rounds = int(rounds_input) if rounds_input.isdigit() and int(rounds_input) > 0 else 5
        
        # --- BITVA ---
        run_battle(service1, model1, service2, model2, topic, rounds)
        
        again = input("Dalsi bitva? [y/N]: ").strip().lower()
        if again != "y":
            print("\nDiky za sledovani!\n")
            break

if __name__ == "__main__":
    main()
