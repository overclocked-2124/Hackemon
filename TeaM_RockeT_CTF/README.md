# 🚀 Team Rocket Crypto Facility - CTF Challenge

A multi-layered cybersecurity challenge combining reverse engineering, cryptography, and exploitation techniques in a Pokémon-themed environment.

![Team Rocket CTF](https://img.shields.io/badge/CTF-Hard-red) ![Category](https://img.shields.io/badge/Category-Reverse%20Engineering-blue) ![Points](https://img.shields.io/badge/Points-500--750-green)

## 🎯 Challenge Overview

**Category:** Reverse Engineering + Cryptography + Exploitation  
**Difficulty:** Hard  
**Estimated Solve Time:** 1–3 hours  
**Flag Format:** `CTF{TEAM_ROCKET_CRYPTO_MASTER_2025}`  
**Points:** 500–750 (depending on CTF scoring system)

## 📖 Story & Mission

> _"Agent, you've successfully infiltrated Team Rocket's secret cryptographic facility. Intelligence suggests they're using a multi-layered security system based on Pokémon type effectiveness to protect their master plan. Multiple security layers stand between you and their secrets."_

Your mission is to chain multiple exploits together to recover Team Rocket's encrypted master flag.

## 🎮 Skills Required

- **Binary Protocol Analysis** – Understanding custom communication formats
- **SQL Injection** – Exploiting database vulnerabilities to escalate privileges
- **Cryptographic Analysis** – Multi-layer encryption with custom algorithms
- **Reverse Engineering** – Understanding Pokémon-themed cipher implementations
- **Exploit Chaining** – Combining multiple attack vectors
- **Frequency Analysis** – Analyzing encrypted data patterns

## 🏗️ Challenge Components

### 1. 🔧 Binary Protocol Reverse Engineering

- Custom "Team Rocket" protocol with magic bytes `ROCK`
- Structured format: Magic + Version + Pokémon ID + Command + Payload + Checksum
- Multiple intercepted messages to analyze
- Hex data decoding and protocol structure identification

### 2. 🗃️ Vulnerable Database System

- Pokédex database with intentional SQL injection vulnerabilities
- Access level restrictions (1–5)
- Hidden high-value entries requiring privilege escalation
- Real-world SQL injection scenarios

### 3. 🔐 Multi-Layer Encryption System

- **Layer 1:** Custom Pokémon type effectiveness cipher
- **Layer 2:** AES-256-CBC encryption with hardcoded key
- **Layer 3:** Base64 encoding
- **Key Derivation:** Based on Pokémon National Dex numbers and type values

### 4. 🛡️ Anti-Cheat Measures

- Developer tools detection and blocking
- Rate limiting (100ms between requests)
- Session fingerprinting and management
- Server-side validation only
- Content obfuscation when cheating detected

## 🚀 Quick Start

### Local Development

1. **Clone the repository:**

```bash
git clone git@github.com:RaghottamNadgoudar/Team-Rocket-Cypher.git
cd Team-Rocket-Cypher
```
