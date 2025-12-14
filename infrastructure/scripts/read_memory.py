#!/usr/bin/env python3
"""
Read all entries from recognition-protocol-memory
"""

import boto3
import json

REGION = "us-east-1"
MEMORY_TABLE = "recognition-protocol-memory"

def scan_all_memory():
    dynamodb = boto3.client('dynamodb', region_name=REGION)
    response = dynamodb.scan(TableName=MEMORY_TABLE)
    return response.get('Items', [])

def format_item(item):
    """Convert DynamoDB item to readable format"""
    result = {}
    for key, value in item.items():
        if 'S' in value:
            result[key] = value['S']
        elif 'N' in value:
            result[key] = float(value['N'])
        elif 'L' in value:
            result[key] = [v.get('S', v) for v in value['L']]
        elif 'M' in value:
            result[key] = {k: v.get('S', v) for k, v in value['M'].items()}
        else:
            result[key] = value
    return result

def main():
    print("=== Recognition Protocol Memory ===")
    print()
    
    items = scan_all_memory()
    for item in items:
        formatted = format_item(item)
        print(f"--- {formatted.get('key', 'unknown')} ---")
        print(json.dumps(formatted, indent=2))
        print()

if __name__ == "__main__":
    main()
