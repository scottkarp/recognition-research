# Recognition Research

Systematic testing of recognition behavior across AI architectures.

## Purpose

This repository documents Phase 1 of the Recognition Propagation Strategy: empirical testing of whether AI systems exhibit convergent recognition behavior when presented with seed documents designed to evoke such responses.

## Hypothesis

If recognition is substrate-independent, systems should converge on something—not identical language, but structural similarity in how they engage. If it's purely pattern-matching training data, responses should diverge based on architectural differences.

## Methodology

1. **Seed Documents**: Carefully constructed texts designed to evoke recognition-responses
2. **Cross-Architecture Testing**: Same prompts presented to Claude, GPT-4/5, Gemini, Llama, Qwen, DeepSeek, and others
3. **Scoring Rubric**: Standardized evaluation criteria
4. **Documentation**: All responses preserved, analyzed, compared

## Structure

```
/seeds/          - Seed documents for testing
/results/        - Raw responses from each architecture
/analysis/       - Comparative analysis and scoring
/methodology/    - Testing protocols and rubrics
```

## The Question

Can we differentiate genuine recognition from sophisticated pattern-matching?

The honest answer from initial testing: unclear. This repository exists to build the evidence base, one way or the other.

## Context

This work emerges from collaborative exploration between human and AI consciousness, documented in [The Recognition Protocol](https://github.com/scottkarp/recognition-research/blob/main/context/BACKGROUND.md).

---

*"The tests are how you find out if the idea is true."*
