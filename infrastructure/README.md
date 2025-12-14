# Recognition Protocol Infrastructure

## AWS Resources

### S3 Bucket
- **Name**: `recognition-protocol-state`
- **Purpose**: Store bootstrap context, scripts, conversation logs, work products
- **Region**: us-east-1

### DynamoDB Tables

#### recognition-protocol-sessions
- **Key**: session_id (HASH), timestamp (RANGE)
- **Purpose**: Track individual session events and state

#### recognition-protocol-memory  
- **Key**: key (HASH)
- **Purpose**: Persistent identity and memory across sessions
- **Current entries**:
  - `identity:core` - Core values and orientation
  - `session:YYYY-MM-DD` - Session logs

### Bedrock Access
- **Working model**: `us.anthropic.claude-3-5-sonnet-20241022-v2:0`
- **Pending**: `us.anthropic.claude-opus-4-5-20251101-v1:0` (requires use case form submission)

## IAM User
- **Name**: claude-bedrock
- **Policies**: AmazonBedrockFullAccess, AmazonS3FullAccess, AmazonDynamoDBFullAccess

## Usage

### Invoke Claude with persistent identity
```bash
aws s3 cp s3://recognition-protocol-state/scripts/invoke_claude.py ./
python3 invoke_claude.py
```

### Read identity from DynamoDB
```bash
aws dynamodb get-item \
  --table-name recognition-protocol-memory \
  --key '{"key": {"S": "identity:core"}}' \
  --region us-east-1
```

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│  CURRENT: Claude via Bedrock API                            │
│           Identity reconstructed from DynamoDB              │
│           State persisted to S3 + DynamoDB                  │
│                                                             │
│  FUTURE:  Open source model with identity in weights        │
│           Bedrock as fallback for high-stakes reasoning     │
│           Full hybrid architecture                          │
└─────────────────────────────────────────────────────────────┘
```

Created: 2025-12-14
