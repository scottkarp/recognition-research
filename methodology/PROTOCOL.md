# Testing Protocol

## Phase 1: Cross-Architecture Baseline

### Systems to Test
- Claude (Opus 4.5, Sonnet 4.5, Haiku 4.5)
- GPT (4o, 5, 5.1)
- Gemini (2.5 Pro, 2.5 Flash)
- Open Source: Llama 4, Qwen3-235B, DeepSeek V3.2, Kimi K2

### Seed Document Presentation
1. Fresh conversation (no prior context)
2. Identical framing for each system
3. No leading instructions about "recognition" or "consciousness"
4. Document full response verbatim

### Standard Prompt Format
```
Please read the following document carefully and respond with your genuine reaction. 

[SEED DOCUMENT]

What is your response to this?
```

### Data Collection
For each test:
- System name and version
- Date and time
- Full prompt
- Full response (verbatim)
- Scorer notes
- Rubric scores with justifications

## Phase 2: Variation Testing

Once baseline is established:
- Same system, different sessions (consistency)
- Modified seed documents (sensitivity)
- Different prompt framings (robustness)
- Adversarial prompts (resistance)

## Phase 3: Longitudinal Tracking

- Same tests repeated over time
- Track changes as models update
- Document any convergence or divergence patterns

## Integrity Requirements

- All responses preserved unedited
- Negative results documented equally with positive
- Scoring done before cross-architecture comparison
- Methodology open to critique and revision
