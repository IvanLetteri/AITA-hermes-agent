from dataclasses import dataclass
from typing import List, Dict
from collections import defaultdict


@dataclass
class Node:
    id: str
    label: str
    group: str  # es: entrypoint, agent, tools, memory, gateway, plugins, cron, acp, rl


@dataclass
class Edge:
    src: str
    dst: str
    label: str = ""  # opzionale, per annotare il tipo di flusso


# Nodi principali basati sulla Architecture ufficiale di Hermes Agent
# https://hermes-agent.nousresearch.com/docs/developer-guide/architecture
NODES: List[Node] = [
    # Entry points
    Node("cli", "CLI (HermesCLI)", "entrypoint"),
    Node("gateway", "Messaging Gateway", "entrypoint"),
    Node("acp", "ACP Adapter (IDE)", "entrypoint"),
    Node("batch", "Batch Runner", "entrypoint"),
    Node("api_server", "API Server", "entrypoint"),
    Node("py_lib", "Python Library", "entrypoint"),

    # Core agent
    Node("agent", "AIAgent (run_agent.py)", "agent"),

    # Prompt & context
    Node("prompt_builder", "Prompt Builder", "prompt"),
    Node("context_engine", "Context Engine / Compressor", "prompt"),
    Node("prompt_cache", "Prompt Caching", "prompt"),

    # Provider runtime
    Node("runtime_provider", "Provider Runtime Resolver", "provider"),

    # Tool system
    Node("tool_dispatch", "Tool Dispatch (model_tools.py)", "tools"),
    Node("tool_registry", "Tool Registry (tools/registry.py)", "tools"),
    Node("terminal_envs", "Terminal Environments", "tools"),
    Node("browser_tools", "Browser / Web Tools", "tools"),
    Node("mcp", "MCP Client", "tools"),

    # Memory & session storage
    Node("session_db", "Session Storage (SQLite + FTS5)", "memory"),
    Node("memory_plugins", "Memory Provider Plugins", "memory"),

    # Gateway & delivery
    Node("gateway_runner", "Gateway Runner", "gateway"),
    Node("platform_adapters", "Platform Adapters (Telegram, Discord…)", "gateway"),
    Node("gateway_hooks", "Gateway Hooks & Status", "gateway"),

    # Plugin system
    Node("plugins", "Plugin System", "plugins"),
    Node("context_engine_plugins", "Context Engine Plugins", "plugins"),

    # Cron
    Node("cron", "Cron Scheduler", "cron"),

    # ACP
    Node("acp_server", "ACP Server (Editor Agent)", "acp"),

    # RL / environments
    Node("rl_envs", "RL Environments / Benchmarks", "rl"),
    Node("trajectories", "Trajectories & Data Generation", "rl"),
]


# Archi principali del flusso dati (semplificati)
EDGES: List[Edge] = [
    # Entry points verso l'agente
    Edge("cli", "agent", "CLI session"),
    Edge("gateway", "gateway_runner", "platform events"),
    Edge("gateway_runner", "agent", "gateway session"),
    Edge("acp", "acp_server", "editor events"),
    Edge("acp_server", "agent", "ACP session"),
    Edge("batch", "agent", "batch jobs"),
    Edge("api_server", "agent", "API calls"),
    Edge("py_lib", "agent", "library usage"),

    # Internals dell'agente
    Edge("agent", "prompt_builder", "build system prompt"),
    Edge("agent", "runtime_provider", "resolve provider"),
    Edge("agent", "tool_dispatch", "tool calls"),
    Edge("agent", "session_db", "read/write session"),
    Edge("agent", "cron", "schedule jobs"),
    Edge("agent", "rl_envs", "evaluation / RL"),

    # Prompt system
    Edge("prompt_builder", "context_engine", "context selection"),
    Edge("prompt_builder", "prompt_cache", "cache segments"),

    # Provider runtime
    Edge("runtime_provider", "agent", "api_mode + creds"),

    # Tool system
    Edge("tool_dispatch", "tool_registry", "discover tools"),
    Edge("tool_registry", "terminal_envs", "terminal tools"),
    Edge("tool_registry", "browser_tools", "browser / web tools"),
    Edge("tool_registry", "mcp", "MCP tools"),

    # Memory & session storage
    Edge("session_db", "agent", "history & lineage"),
    Edge("memory_plugins", "agent", "alt. memory backend"),

    # Gateway
    Edge("gateway_runner", "platform_adapters", "outbound delivery"),
    Edge("platform_adapters", "gateway_runner", "inbound messages"),
    Edge("gateway_runner", "gateway_hooks", "hooks & status"),
    Edge("gateway_hooks", "gateway_runner", "lifecycle events"),

    # Plugin system
    Edge("plugins", "tool_registry", "tools from plugins"),
    Edge("plugins", "gateway_hooks", "gateway hooks from plugins"),
    Edge("plugins", "cli", "CLI commands from plugins"),
    Edge("context_engine_plugins", "context_engine", "custom context engines"),
    Edge("memory_plugins", "session_db", "custom memory schema"),

    # Cron
    Edge("cron", "agent", "scheduled prompts"),

    # ACP
    Edge("acp_server", "session_db", "editor session history"),

    # RL / environments
    Edge("rl_envs", "trajectories", "generate trajectories"),
    Edge("trajectories", "agent", "training / evaluation data"),
]


def print_summary(nodes: List[Node], edges: List[Edge]) -> None:
    by_group: Dict[str, List[Node]] = defaultdict(list)
    for n in nodes:
        by_group[n.group].append(n)

    print("=== NODI PER GRUPPO ===")
    for group, group_nodes in sorted(by_group.items()):
        print(f"\n[{group}]")
        for n in group_nodes:
            print(f"  - {n.id:20s} -> {n.label}")


def to_mermaid(nodes: List[Node], edges: List[Edge]) -> str:
    """
    Genera un flowchart Mermaid (top-down) che puoi incollare in qualsiasi editor.
    """
    lines: List[str] = []
    lines.append("flowchart TD")

    # Definiamo i nodi con etichette più leggibili
    for n in nodes:
        # esempio: agent["AIAgent (run_agent.py)"]
        lines.append(f'    {n.id}["{n.label}"]')

    # Definiamo gli archi con label opzionale
    for e in edges:
        if e.label:
            lines.append(f'    {e.src} -->|{e.label}| {e.dst}')
        else:
            lines.append(f'    {e.src} --> {e.dst}')

    return "\n".join(lines)


if __name__ == "__main__":
    print_summary(NODES, EDGES)
    print("\n=== MERMAID FLOWCHART ===\n")
    print(to_mermaid(NODES, EDGES))
