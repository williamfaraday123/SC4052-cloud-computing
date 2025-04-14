from fastapi import FastAPI
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
from pathlib import Path
from pydantic import BaseModel

app = FastAPI()

# input model
class CodePrompt(BaseModel):
    prompt: str

# Model paths
model_path = Path(__file__).parent / "model"
tokenizer_path = model_path / "tokenizer"

# Verify tokenizer files
required_tokenizer_files = [
    "tokenizer_config.json",
    "special_tokens_map.json",
    "tokenizer.json",
    "vocab.json",
    "merges.txt",
]

missing_files = [f for f in required_tokenizer_files if not (tokenizer_path / f).exists()]
if missing_files:
    raise FileNotFoundError(
        f"Missing tokenizer files: {missing_files}\n"
        f"Found files: {[f.name for f in tokenizer_path.glob('*')]}"
    )

# Load model and tokenizer
try:
    model = AutoModelForCausalLM.from_pretrained(
        model_path,
        local_files_only=True,
        use_safetensors=True
    )
    
    # Try different loading approaches for tokenizer
    try:
        tokenizer = AutoTokenizer.from_pretrained(
            "codeparrot/codeparrot-small"
        )

        #check same vocab size
        print("same vocab size =", model.config.vocab_size == len(tokenizer))

    except Exception as e:
        print(f"First tokenizer load failed: {str(e)}")
        print("Trying alternative loading method...")
        tokenizer = AutoTokenizer.from_pretrained(
            model_path,  # Try loading from model directory instead
            local_files_only=True
        )
        
except Exception as e:
    raise RuntimeError(f"Failed to load model/tokenizer: {str(e)}")

@app.get("/")
async def health_check():
    return {"status": "healthy"}

@app.post("/generate")
async def generate_code(data: CodePrompt):
    prompt = data.prompt.strip()

    # validate the prompt
    if not prompt:
        raise HTTPException(status_code=400, detail="Prompt cannot be empty")
    try:
        inputs = tokenizer(prompt, return_tensors="pt")
        with torch.no_grad():
            outputs = model.generate(**inputs, max_length=100)
        return {
            "generated_code": tokenizer.decode(outputs[0], skip_special_tokens=True)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {e}")