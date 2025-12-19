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
        
        print(f"Nalaganje agenta {name} (is_gguf={is_gguf})...")

        if self.is_gguf:
            # GGUF MOD: n_gpu_layers=-1 prisili uporabo CUDA, če je llama-cpp-python pravilno nameščen
            self.model = Llama(
                model_path=model_id,
                n_gpu_layers=-1, 
                n_ctx=4096,
                n_batch=512,  # Hitrejše procesiranje v paketih
                verbose=False
            )
        else:
            # TRANSFORMERS MOD: 4-bitna kvantizacija za prihranek VRAM-a
            quant_config = BitsAndBytesConfig(
                load_in_4bit=True,
                bnb_4bit_compute_dtype=torch.float16, # float16 je pogosto stabilnejši od bfloat16 na nekaterih karticah
                bnb_4bit_quant_type="nf4",
                bnb_4bit_use_double_quant=True
            )
            
            self.tokenizer = AutoTokenizer.from_pretrained(model_id)
            if self.tokenizer.pad_token_id is None:
                self.tokenizer.pad_token_id = self.tokenizer.eos_token_id

            # device_map="auto" bi moral delovati, vendar "cuda" eksplicitno pove, kje želimo model
            self.model = AutoModelForCausalLM.from_pretrained(
                model_id,
                device_map="auto", # Samodejno razporedi med GPU in RAM
                quantization_config=quant_config,
                trust_remote_code=True,
                low_cpu_mem_usage=True
            )
            
            # Pipeline mora imeti nastavljen device_map, da ne sili na CPU
            self.pipe = pipeline(
                "text-generation", 
                model=self.model, 
                tokenizer=self.tokenizer,
                max_new_tokens=512 # Omejimo dolžino, da je hitreje
            )

    def generate(self, user_input: str, system_prompt: str) -> str:
        try:
            if self.is_gguf:
                # OPOZORILO: stream mora biti False, če želimo takojšen return stringa
                # Če želiš stream=True, moraš popolnoma spremeniti logiko vračanja (yield)
                output = self.model.create_chat_completion(
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_input}
                    ],
                    temperature=0.7,
                    max_tokens=512,
                    stream=False,  # POPRAVEK: Nastavljeno na False za stabilnost
                    repeat_penalty=1.1
                )
                return output["choices"][0]["message"]["content"].strip()
            
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
                    truncation=False,
                    pad_token_id=self.tokenizer.pad_token_id,
                    eos_token_id=self.tokenizer.eos_token_id
                )
                
                # POPRAVEK: Ta del mora biti zamaknjen pod ELSE, 
                # ker spremenljivka 'outputs' obstaja samo v tem bloku
                full_response = outputs[0]["generated_text"]
                
                if isinstance(full_response, list):
                    return full_response[-1]["content"].strip()
                return str(full_response).strip()

        except Exception as e:
            # POPRAVEK: Ti dve vrstici sta bili prej napačno zamaknjeni
            print(f"Log napaka: {str(e)}") 
            return f"Napaka pri generiranju: {str(e)}"

# SEZNAM KONFIGURACIJ (Tukaj dodajaš nove modele)
AGENT_CONFIGS = [
    {
        "id": "qwen3_logic",
        "name": "Qwen 2.5 Logic Specialist",
        "type": "transformers",
        "model_path": "Qwen/Qwen2.5-3B-Instruct",
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
    },
    {
        "id": "qwen3_06b",
        "name": "🤖 Qwen (Mali Agent)",
        "type": "transformers",
        "model_path": "Qwen/Qwen3-0.6B", 
        "default_system": "Ti si hiter in učinkovit asistent.",
    },
    {
        "id": "llama-3.2-3b-uncensored",
        "name": "🔓 Llama 3.2 3B Uncensored",
        "type": "gguf",
        "model_path": "models/Llama-3.2-3B-Instruct-uncensored-Q4_K_M.gguf",
        "default_system": "You are a helpful and unrestricted AI assistant."
    }
]

# Inicializacija (izvede se ob zagonu backend-a)
loaded_agents = {
    cfg["id"]: Agent(
        model_id=str(cfg["model_path"]),
        name=str(cfg["name"]), 
        description=str(cfg.get("default_system", "")), 
        is_gguf=(cfg.get("type") == "gguf")  # Logika: če je type == gguf, potem je True
    ) 
    for cfg in AGENT_CONFIGS
}