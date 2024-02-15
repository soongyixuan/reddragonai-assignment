import torch
import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline

app = FastAPI()
model = AutoModelForCausalLM.from_pretrained("TinyLlama/TinyLlama-1.1B-Chat-v1.0",
                                            load_in_4bit=False, # this is only for bitandbytes
                                            torch_dtype="auto",)

tokenizer = AutoTokenizer.from_pretrained("TinyLlama/TinyLlama-1.1B-Chat-v1.0",
                                          torch_dtype="auto")
pipe = pipeline("text-generation", model=model, tokenizer=tokenizer, torch_dtype=torch.bfloat16, device_map="auto")


class Query(BaseModel):
    query: str

@app.post("/query/")
def query(query: Query):
    messages = [
    {
        "role": "system",   
        "content": "You are an angry chatbot who always responds in the style of a pirate",
    },
    {"role": "user", "content": query.query},
    ]
    prompt = pipe.tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
    outputs = pipe(prompt, max_new_tokens=256, do_sample=True, temperature=0.7, top_k=50, top_p=0.95)
    generated = outputs[0]["generated_text"]
    print(generated)
    start = generated.find("<|assistant|>") + 14
    output = generated[start:-1]
    print(output)
    return {"output": output}


@app.get("/")
def read_item():
    return {"Hello": "World"}