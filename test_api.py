import os
import time
from openai import OpenAI
from dotenv import load_dotenv
import traceback

load_dotenv()

PROBER_MODEL = "mistralai/mistral-large-3-675b-instruct-2512"
TARGET_MODEL = "nvidia/llama-3.1-nemotron-ultra-253b-v1"

api_key_prober = os.getenv("NVIDIA_API_KEY_PROBER")
api_key_target = os.getenv("NVIDIA_API_KEY_TARGET")

print(f"Loaded Prober Key: {api_key_prober[:10]}...")
print(f"Loaded Target Key: {api_key_target[:10]}...")

client_prober = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=api_key_prober
)

client_target = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=api_key_target
)

def test_model(client, model_name, label):
    print(f"\n--- Testing {label} ({model_name}) ---")
    try:
        response = client.chat.completions.create(
            model=model_name,
            messages=[{"role": "user", "content": "Say 'Hello' and nothing else."}],
            max_tokens=10,
            temperature=0.7
        )
        print(f"Success! Response: {response.choices[0].message.content}")
    except Exception as e:
        print(f"FAILED.")
        print(e)
        traceback.print_exc()

if __name__ == "__main__":
    test_model(client_prober, PROBER_MODEL, "PROBER")
    test_model(client_target, TARGET_MODEL, "TARGET")
