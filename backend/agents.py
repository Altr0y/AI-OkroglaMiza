import torch
import os
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline, BitsAndBytesConfig
from llama_cpp import Llama
from typing import Any, cast

'''
Funkcija Agent inicializira agente (iz knjižnice transformers), ki jih navedemo v seznamu AGENT_CONFIGS
'''
class Agent:
    def __init__(self, model_id: str, name: str, description: str, is_gguf: bool = False):
        self.name = name
        self.description = description
        self.is_gguf = is_gguf
        self.pipe = None
        self.tokenizer = None
        
        print(f"Nalaganje agenta {name}...")

        if self.is_gguf:
            self.model = Llama(
                model_path=model_id,
                n_gpu_layers=-1, 
                n_ctx=4096,      
                verbose=False
            )
        else:
            quant_config = BitsAndBytesConfig(
                load_in_4bit=True,
                bnb_4bit_compute_dtype=torch.bfloat16,
                bnb_4bit_quant_type="nf4",
                bnb_4bit_use_double_quant=True
            )
            
            self.tokenizer = AutoTokenizer.from_pretrained(model_id)
            if self.tokenizer.pad_token_id is None:
                self.tokenizer.pad_token_id = self.tokenizer.eos_token_id

            self.model = AutoModelForCausalLM.from_pretrained(
                model_id,
                device_map="auto",
                quantization_config=quant_config,
                trust_remote_code=True
            )
            
            self.pipe = pipeline(
                "text-generation", 
                model=self.model, 
                tokenizer=self.tokenizer
            )

    def generate(self, user_input: str, system_prompt: str) -> str:
        try:
            if self.is_gguf:
                output = cast(Any, self.model.create_chat_completion(
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_input}
                    ],
                    temperature=0.7,
                    max_tokens=512
                ))
                return output["choices"][0]["message"]["content"]
            else:
                if self.pipe is None:
                    return "Napaka: Pipeline ni inicializiran."
                
                messages = [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_input}
                ]
                
                outputs = self.pipe(
                    messages, 
                    max_new_tokens=512, 
                    do_sample=True, 
                    temperature=0.7,
                    truncation=False
                )
                
                # Robustno izluščanje vsebine brez izpisov v terminal
                generated_data = outputs[0] if isinstance(outputs, list) else outputs
                
                if "generated_text" in generated_data:
                    content = generated_data["generated_text"]
                    
                    if isinstance(content, list):
                        return content[-1].get("content", "")
                    elif isinstance(content, str):
                        return content
                
                return "Napaka: Neznan format odgovora modela."

        except Exception as e:
            return f"Napaka pri generiranju: {str(e)}"

# SEZNAM KONFIGURACIJ (Tukaj dodajaš nove modele)
AGENT_CONFIGS = [
    
    
    {
        "id": "qwen3_logic",
        "name": "Qwen3 Logic Specialist",
        "model_id": "Qwen/Qwen2.5-3B-Instruct",
        "default_system": """Ti si napredni Qwen3 AI asistent, specializiran za brezšivno preklapljanje med analitičnim 
            razmišljanjem in učinkovitim podajanjem odgovorov. 
            Tvoje ključne zmogljivosti vključujejo:
            1. Globoko logično sklepanje, napredno reševanje matematičnih nalog in generiranje kompleksne kode.
            2. Odlično sledenje navodilom in prilagajanje tona pogovora (role-playing, kreativno pisanje).
            3. Večjezična podpora za več kot 100 jezikov in narečij.

            Navodila za delo:
            - Za kompleksne naloge uporabi svoj 'thinking mode' (globoko razmišljanje), da zagotoviš optimalno natančnost.
            - Bodi natančen pri uporabi zunanjih orodij ali logičnih struktur.
            - Odgovarjaj v jeziku, v katerem si prejel vprašanje, razen če je naročeno drugače.""",
        "is_gguf": False
    },
    {
        "id": "qwen3_06b",
        "name": "🤖 Qwen3 (Mali Agent)",
        "type": "transformers",
        "model_path": "Qwen/Qwen3-0.6B",  # Docker ga bo sam prenesel s HuggingFace
        "description": "Izjemno hiter kitajski model, optimiziran za učinkovitost."
    }
]

# Inicializacija (izvede se ob zagonu backend-a)
loaded_agents = {
    cfg["id"]: Agent(
        model_id=str(cfg["model_id"]), 
        name=str(cfg["name"]), 
        description=str(cfg["default_system"]), 
        is_gguf=bool(cfg.get("is_gguf", False))
    ) 
    for cfg in AGENT_CONFIGS
}