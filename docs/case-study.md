# Case Study

## Problem

A conventional automation script can call APIs and execute fixed steps, but it struggles when incoming requests vary in wording and structure. Giving a language model direct authority over external actions introduces a different risk: probabilistic output can trigger unintended side effects.

## Approach

This project separates four responsibilities:

1. The model interprets the request and proposes function calls.
2. The Python orchestrator owns the execution loop.
3. Deterministic policy code authorizes, blocks or redirects side effects.
4. A local MCP server exposes narrowly scoped tools.

## Public demo

The public version uses synthetic support, invoice and sensitive-request examples. Tasks and notifications are local or simulated. No organization-specific data or external business system is required.

## Engineering outcome

The architecture demonstrates how model reasoning can be combined with deterministic controls, standardized MCP tool contracts, bounded execution and human-review fallbacks.
