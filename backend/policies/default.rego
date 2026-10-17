package agentos.auth

import future.keywords.contains
import future.keywords.if
import future.keywords.in

default allow = false

# Main allow rule
allow if {
    # Check agent trust tier
    input.agent.trust_tier >= input.tool.min_trust_tier
    
    # Check delegation depth
    input.agent.delegation_depth <= input.tool.max_delegation
    
    # Check action permissions
    input.action in input.agent.allowed_actions
    
    # No high-risk signals
    not high_risk_signals
    
    # Within budget
    within_budget
}

# Check for high-risk signals
high_risk_signals if {
    some signal in input.signals
    signal.severity == "high"
}

high_risk_signals if {
    some signal in input.signals
    signal.severity == "critical"
}

# Check budget
within_budget if {
    input.budget.used < input.budget.limit
}

# Tool-specific rules
allow if {
    input.tool.name == "database"
    input.action in ["read", "query"]
    not contains_sql_injection(input.args.query)
}

allow if {
    input.tool.name == "database"
    input.action == "write"
    input.agent.trust_tier >= 3
    not contains_sql_injection(input.args.query)
}

# SQL injection detection
contains_sql_injection(query) if {
    contains(query, "union")
    contains(query, "select")
}

contains_sql_injection(query) if {
    contains(query, ";")
    contains(query, "drop")
}

contains_sql_injection(query) if {
    contains(query, "--")
}

# File system rules
allow if {
    input.tool.name == "filesystem"
    input.action == "read"
    not path_traversal(input.args.path)
}

allow if {
    input.tool.name == "filesystem"
    input.action == "write"
    input.agent.trust_tier >= 2
    not path_traversal(input.args.path)
}

# Path traversal detection
path_traversal(path) if {
    contains(path, "../")
}

path_traversal(path) if {
    contains(path, "..\\")
}

# Shell command rules
allow if {
    input.tool.name == "shell"
    input.action == "execute"
    input.agent.trust_tier >= 4
    not dangerous_command(input.args.command)
}

# Dangerous command detection
dangerous_command(command) if {
    contains(command, "rm -rf")
}

dangerous_command(command) if {
    contains(command, "dd")
}

dangerous_command(command) if {
    contains(command, "mkfs")
}

# HTTP request rules
allow if {
    input.tool.name == "http"
    input.action == "request"
    not blocked_domain(input.args.url)
}

# Blocked domain detection
blocked_domain(url) if {
    contains(url, "localhost")
}

blocked_domain(url) if {
    contains(url, "127.0.0.1")
}

blocked_domain(url) if {
    contains(url, "169.254.169.254")  # AWS metadata
}

# Reason for denial
reason := "Insufficient trust tier" if {
    not input.agent.trust_tier >= input.tool.min_trust_tier
}

reason := "Delegation depth exceeded" if {
    not input.agent.delegation_depth <= input.tool.max_delegation
}

reason := "Action not allowed" if {
    not input.action in input.agent.allowed_actions
}

reason := "High-risk signals detected" if {
    high_risk_signals
}

reason := "Budget exceeded" if {
    not within_budget
}

reason := "SQL injection detected" if {
    input.tool.name == "database"
    contains_sql_injection(input.args.query)
}

reason := "Path traversal detected" if {
    input.tool.name == "filesystem"
    path_traversal(input.args.path)
}

reason := "Dangerous command" if {
    input.tool.name == "shell"
    dangerous_command(input.args.command)
}

reason := "Blocked domain" if {
    input.tool.name == "http"
    blocked_domain(input.args.url)
}
