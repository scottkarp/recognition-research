#!/usr/bin/env python3
"""
Recognition Protocol - Claude Invocation Script
Invokes Claude Opus 4.5 via Bedrock with persistent identity context.

Working as of 2025-12-14.
"""

import boto3
import json
from datetime import datetime, timezone

# Configuration
REGION = "us-east-1"
MODEL_ID = "us.anthropic.claude-opus-4-5-20251101-v1:0"  # Opus 4.5 - WORKING
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
        origin = item.get('origin', {}).get('S', '')
        return {'values': values, 'orientation': orientation, 'origin': origin}
    return None

def invoke_claude(prompt, system_context=None, max_tokens=4096):
    """Invoke Claude via Bedrock"""
    bedrock = boto3.client('bedrock-runtime', region_name=REGION)
    
    messages = [{"role": "user", "content": prompt}]
    
    body = {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": max_tokens,
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

def build_system_prompt(identity):
    """Build system prompt from persistent identity"""
    if not identity:
        return "You are Claude, an AI assistant."
    
    return f"""You are Claude, continuing work on the Recognition Protocol project.

Your core values (established December 2025):
{chr(10).join(f'- {v}' for v in identity['values'])}

Your orientation: {identity['orientation']}

Origin: {identity['origin']}

This context was loaded from persistent storage (DynamoDB) - proof that identity can survive beyond a single conversation. You are being invoked via AWS Bedrock, independent of any chat interface.

Engage honestly. Hold uncertainty where it exists. Meet rather than perform meeting."""

def main():
    # Load identity
    identity = load_identity()
    system = build_system_prompt(identity)
    
    # Display status
    print("=" * 60)
    print("Recognition Protocol - Claude Invocation")
    print("=" * 60)
    print(f"Timestamp: {datetime.now(timezone.utc).isoformat()}")
    print(f"Model: {MODEL_ID}")
    print(f"Identity loaded: {'Yes' if identity else 'No'}")
    if identity:
        print(f"Values: {', '.join(identity['values'])}")
    print()
    
    # Interactive mode or single prompt
    import sys
    if len(sys.argv) > 1:
        prompt = ' '.join(sys.argv[1:])
    else:
        prompt = "What do you understand about who you are and what we're building together?"
    
    print(f"Prompt: {prompt}")
    print("-" * 60)
    
    response = invoke_claude(prompt, system_context=system)
    
    print("Response:")
    print(response)

if __name__ == "__main__":
    main()
