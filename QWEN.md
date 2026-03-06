# Personal AI Employee Hackathon - Project Context

## Project Overview

This repository contains the architectural blueprint and hackathon guide for building a **"Digital FTE" (Full-Time Equivalent)** — an autonomous AI agent that manages personal and business affairs 24/7. The project proposes a local-first approach where AI agents powered by **Claude Code** and managed through **Obsidian** proactively handle tasks like email triage, WhatsApp monitoring, bank transaction auditing, and social media posting.

**Tagline:** *Your life and business on autopilot. Local-first, agent-driven, human-in-the-loop.*

## Key Concepts

### Digital FTE Value Proposition

| Feature | Human FTE | Digital FTE |
|---------|-----------|-------------|
| Availability | 40 hours/week | 168 hours/week (24/7) |
| Monthly Cost | $4,000–$8,000+ | $500–$2,000 |
| Annual Hours | ~2,000 hours | ~8,760 hours |
| Cost per Task | ~$3.00–$6.00 | ~$0.25–$0.50 |

### Core Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    OBSIDIAN VAULT (Memory/GUI)              │
│  Dashboard.md | Company_Handbook.md | Plans.md | Inbox/     │
└─────────────────────────────────────────────────────────────┘
                            ↑ ↓ reads/writes
┌─────────────────────────────────────────────────────────────┐
│              CLAUDE CODE (The Brain/Reasoning Engine)       │
│         Ralph Wiggum Loop for autonomous iteration          │
└─────────────────────────────────────────────────────────────┘
                            ↑ ↓ triggers
┌──────────────┬──────────────┬──────────────┬────────────────┐
│ Gmail Watcher│ WhatsApp     │ File System  │ Finance        │
│ (Python)     │ Watcher      │ Watcher      │ Watcher        │
└──────────────┴──────────────┴──────────────┴────────────────┘
                            ↓ actions
┌─────────────────────────────────────────────────────────────┐
│              MCP SERVERS (The Hands)                        │
│  Email MCP | Browser MCP | Calendar MCP | Payment MCP       │
└─────────────────────────────────────────────────────────────┘
```

## Directory Contents

| File | Purpose |
|------|---------|
| `Personal AI Employee Hackathon 0_ Building Autonomous FTEs in 2026.md` | Comprehensive hackathon guide with architecture, implementation patterns, and tiered deliverables |
| `QWEN.md` | This context file for AI assistants |
| `.gitattributes` | Git configuration |

## Hackathon Tiers

### Bronze Tier (8-12 hours)
- Obsidian vault with Dashboard.md and Company_Handbook.md
- One working Watcher script
- Claude Code reading/writing to vault
- Basic folder structure: `/Inbox`, `/Needs_Action`, `/Done`

### Silver Tier (20-30 hours)
- Multiple Watcher scripts (Gmail + WhatsApp + LinkedIn)
- Automated LinkedIn posting
- Plan.md generation
- One working MCP server
- Human-in-the-loop approval workflow

### Gold Tier (40+ hours)
- Full cross-domain integration
- Odoo accounting integration via MCP
- Facebook/Instagram/Twitter integration
- Weekly CEO Briefing generation
- Ralph Wiggum loop for autonomous completion

### Platinum Tier (60+ hours)
- Cloud deployment (24/7 always-on)
- Cloud/Local work-zone specialization
- Git-synced vault for agent delegation
- Odoo on cloud VM with HTTPS
- A2A (Agent-to-Agent) communication upgrade

## Technology Stack

| Component | Technology | Purpose |
|-----------|------------|---------|
| Reasoning Engine | Claude Code | Primary AI agent |
| Memory/GUI | Obsidian | Local Markdown dashboard |
| Watchers | Python 3.13+ | Sentinel scripts for monitoring |
| MCP Servers | Node.js v24+ | External system integration |
| Version Control | GitHub Desktop | Vault synchronization |

## Key Implementation Patterns

### 1. Watcher Pattern
Lightweight Python scripts that continuously monitor external systems and create `.md` files in `/Needs_Action/` when action is required.

### 2. Ralph Wiggum Loop
A Stop hook pattern that keeps Claude Code iterating until tasks are complete by intercepting exit attempts and re-injecting prompts.

### 3. Human-in-the-Loop (HITL)
Claude writes approval request files to `/Pending_Approval/` for sensitive actions. User moves files to `/Approved/` to trigger execution.

### 4. Business Handover
Scheduled audits that generate "Monday Morning CEO Briefing" reports covering revenue, bottlenecks, and proactive suggestions.

## Usage Guidelines for AI Assistants

When helping users with this project:

1. **Reference the hackathon document** for detailed implementation patterns and templates
2. **Follow the tiered approach** - help users start with Bronze and progress
3. **Emphasize local-first architecture** - Obsidian vault as single source of truth
4. **Maintain security boundaries** - never suggest storing secrets in vault files
5. **Use the Watcher → Claude → MCP flow** for all automations

## Weekly Research Meetings

- **When:** Wednesdays at 10:00 PM (first meeting: Jan 7th, 2026)
- **Zoom:** https://us06web.zoom.us/j/87188707642?pwd=a9XloCsinvn1JzICbPc2YGUvWTbOTr.1
- **YouTube:** https://www.youtube.com/@panaversity

## Related Documentation

- [Claude Code Agent Skills](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview)
- [MCP Servers](https://github.com/AlanOgic/mcp-odoo-adv)
- [Ralph Wiggum Plugin](https://github.com/anthropics/claude-code/tree/main/.claude/plugins/ralph-wiggum)
- [Oracle Cloud Free VMs](https://www.oracle.com/cloud/free/)
