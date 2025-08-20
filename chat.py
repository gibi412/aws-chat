import json
import logging
from typing import List, Dict, Any

import boto3
from botocore.config import Config
from botocore.credentials import Credentials
from botocore.session import get_session

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

ACCESS_KEY_ID = "AKIARJ5AUHRXQRBJXQVL"
SECRET_ACCESS_KEY = "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"
SESSION_TOKEN = None

class BedrockClient:
    def __init__(self, region: str = "us-east-1"):
        creds = Credentials(ACCESS_KEY_ID, SECRET_ACCESS_KEY, SESSION_TOKEN)
        session = get_session()
        self.client = session.create_client(
            "bedrock-runtime",
            region_name=region,
            credentials=creds,
            config=Config(retries={"max_attempts": 3})
        )

    def converse(self, model_id: str, messages: List[Dict[str, Any]]) -> str:
        payload = {"messages": messages}
        try:
            response = self.client.invoke_model(
                modelId=model_id,
                contentType="application/json",
                accept="application/json",
                body=json.dumps(payload)
            )
            data = json.loads(response["body"].read())
            content = data.get("output", {}).get("message", {}).get("content", [{}])
            return content[0].get("text", "") if content else ""
        except Exception as e:
            logger.error("Bedrock call failed: %s", e)
            return "error"

if __name__ == "__main__":
    user_msg = input("You: ").strip()
    client = BedrockClient("us-east-1")
    msgs = [{"role": "user", "content": [{"text": user_msg}]}]
    reply = client.converse("meta.llama3-8b-instruct-v1:0", msgs)
    print("Assistant:", reply)
