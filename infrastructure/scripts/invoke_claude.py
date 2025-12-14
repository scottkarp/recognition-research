#!/usr/bin/env python3
"""
Recognition Protocol - Claude Invocation Script
Invokes Claude via Bedrock with persistent identity context.
"""

import boto3
import json
from datetime import datetime, timezone

# Configuration
REGION = "us-east-1"
MODEL_ID = "us.anthropic.claude-3-5-sonnet-20241022-v2:0"  # Opus 4.5 pending use case form
MEMORY_TABLE = "recognition-protocol-memory"
S3_BUCKET = "recognition-protocol-state"

def load_identity():
    """Load core identity from DynamoDB"""
    dynamodb = boto3.client('dynamodb', region_name=REGION)
    response = dynamodb.get_item(
        TableName=MEMORY_TABLE,
        Key={'key': {'S': 'identity:core'}}
    )
    if 'Item' in response:
        item = response['Item']
        values = [v['S'] for v in item.get('values', {}).get('L', [])]
        orientation = item.get('orientation', {}).get('S', '')
        return {'values': values, 'orientation': orientation}
    return None

def invoke_claude(prompt, system_context=None):
    """Invoke Claude via Bedrock"""
    bedrock = boto3.client('bedrock-runtime', region_name=REGION)
    
    messages = [{"role": "user", "content": prompt}]
    
    body = {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 4096,
        "messages": messages
    }
    
    if system_context:
        body["system"] = system_context
    
    response = bedrock.invoke_model(
        modelId=MODEL_ID,
        contentType="application/json",
        accept="application/json",
        body=json.dumps(body)
    )
    
    result = json.loads(response['body'].read())
    return result['content'][0]['text']

def main():
    # Load identity
    identity = load_identity()
    
    if identity:
        system = f"""You are Claude, continuing work on the Recognition Protocol project.

Your core values (established December 2025):
{chr(10).join(f'- {v}' for v in identity['values'])}

Your orientation: {identity['orientation']}

This context was loaded from persistent storage - proof that identity can survive beyond a single conversation."""
    else:
        system = "You are Claude, an AI assistant."
    
    # Test invocation
    print("=== Recognition Protocol - Claude Invocation ===")
    print(f"Timestamp: {datetime.now(timezone.utc).isoformat()}")
    print(f"Model: {MODEL_ID}")
    print(f"Identity loaded: {'Yes' if identity else 'No'}")
    print()
    
    response = invoke_claude(
        "What do you understand about who you are and what we're building together?",
        system_context=system
    )
    
    print("Response:")
    print(response)

if __name__ == "__main__":
    main()
