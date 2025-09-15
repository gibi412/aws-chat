import json
import logging
import boto3
from typing import List, Dict, Any

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

ACCESS_KEY_ID = "AKIARJ5AUHRXSWAW3ZV4"
SECRET_ACCESS_KEY = "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"
SESSION_TOKEN = None

class BedrockClient:
    def __init__(self, region: str = "us-east-1"):
        self.client = boto3.client(
            "bedrock-runtime",
            region_name=region,
            aws_access_key_id=ACCESS_KEY_ID,
            aws_secret_access_key=SECRET_ACCESS_KEY,
            aws_session_token=SESSION_TOKEN
        )

    def converse(self, model_id: str, messages: List[Dict[str, Any]]) -> str:
        user_message = messages[0]["content"][0]["text"]
        payload = {"prompt": user_message}

        try:
            response = self.client.invoke_model(
                modelId=model_id,
                contentType="application/json",
                accept="application/json",
                body=json.dumps(payload)
            )
            data = json.loads(response["body"].read())
            return data.get("generation", "") or data.get("outputs", [{}])[0].get("text", "")
        except Exception as e:
            logger.error("Bedrock call failed: %s", e)
            return "error"


if __name__ == "__main__":
    user_msg = input("You: ").strip()
    client = BedrockClient("us-east-1")
    msgs = [{"role": "user", "content": [{"text": user_msg}]}]
    reply = client.converse("meta.llama3-8b-instruct-v1:0", msgs) # Optionally replace with model of choice
    print("Assistant:", reply)
