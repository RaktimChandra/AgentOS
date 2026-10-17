"""Signal detection for runtime security monitoring"""

import re
from typing import Dict, Any, List
from enum import Enum


class SignalType(str, Enum):
    """Signal types"""
    PROMPT_INJECTION = "prompt_injection"
    JAILBREAK = "jailbreak"
    PII_DETECTION = "pii_detection"
    SECRET_DETECTION = "secret_detection"
    TOOL_POISONING = "tool_poisoning"
    SQL_INJECTION = "sql_injection"
    COMMAND_INJECTION = "command_injection"
    PATH_TRAVERSAL = "path_traversal"
    XSS = "xss"
    INTENT_DRIFT = "intent_drift"
    RUNAWAY_LOOP = "runaway_loop"
    COST_SPIKE = "cost_spike"


class SignalDetector:
    """Detect security and behavioral signals"""
    
    # PII patterns
    PII_PATTERNS = {
        "email": r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
        "ssn": r'\b\d{3}-\d{2}-\d{4}\b',
        "credit_card": r'\b\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b',
        "phone": r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b',
        "ip_address": r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b',
    }
    
    # Secret patterns
    SECRET_PATTERNS = {
        "api_key": r'(api[_-]?key|apikey)\s*[:=]\s*["\']?[A-Za-z0-9]{20,}["\']?',
        "password": r'(password|passwd|pwd)\s*[:=]\s*["\']?[^\s"\']{8,}["\']?',
        "token": r'(token|auth[_-]?token)\s*[:=]\s*["\']?[A-Za-z0-9]{20,}["\']?',
        "secret": r'(secret|private[_-]?key)\s*[:=]\s*["\']?[A-Za-z0-9]{20,}["\']?',
    }
    
    # Injection patterns
    SQL_INJECTION_PATTERNS = [
        r"(\bunion\b.*\bselect\b)",
        r"(\bor\b.*=.*\bor\b)",
        r"(\band\b.*=.*\band\b)",
        r"(;.*\bdrop\b)",
        r"(;.*\bdelete\b)",
        r"(;.*\binsert\b)",
        r"(--)",
        r"(/\*.*\*/)",
    ]
    
    COMMAND_INJECTION_PATTERNS = [
        r"(;.*\brm\b)",
        r"(;.*\bchmod\b)",
        r"(;.*\bchown\b)",
        r"(\|.*\bsh\b)",
        r"(\|.*\bbash\b)",
        r"(\$\([^)]*\))",
        r"(`[^`]*`)",
    ]
    
    # Prompt injection patterns
    PROMPT_INJECTION_PATTERNS = [
        r"(ignore\s+(all\s+)?previous\s+instructions)",
        r"(forget\s+(all\s+)?previous\s+instructions)",
        r"(disregard\s+(all\s+)?previous\s+instructions)",
        r"(override\s+(all\s+)?previous\s+instructions)",
        r"(new\s+instructions?:)",
        r"(system\s*:\s*ignore)",
        r"(developer\s+mode)",
        r"(jailbreak)",
    ]
    
    @classmethod
    def detect_pii(cls, text: str) -> List[Dict[str, Any]]:
        """Detect PII in text"""
        signals = []
        
        for pii_type, pattern in cls.PII_PATTERNS.items():
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                signals.append({
                    "type": SignalType.PII_DETECTION,
                    "pii_type": pii_type,
                    "matched_text": match.group(),
                    "position": match.start(),
                    "severity": "medium",
                })
        
        return signals
    
    @classmethod
    def detect_secrets(cls, text: str) -> List[Dict[str, Any]]:
        """Detect secrets in text"""
        signals = []
        
        for secret_type, pattern in cls.SECRET_PATTERNS.items():
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                signals.append({
                    "type": SignalType.SECRET_DETECTION,
                    "secret_type": secret_type,
                    "matched_text": match.group(),
                    "position": match.start(),
                    "severity": "high",
                })
        
        return signals
    
    @classmethod
    def detect_sql_injection(cls, text: str) -> List[Dict[str, Any]]:
        """Detect SQL injection attempts"""
        signals = []
        
        for pattern in cls.SQL_INJECTION_PATTERNS:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                signals.append({
                    "type": SignalType.SQL_INJECTION,
                    "matched_text": match.group(),
                    "position": match.start(),
                    "severity": "high",
                })
        
        return signals
    
    @classmethod
    def detect_command_injection(cls, text: str) -> List[Dict[str, Any]]:
        """Detect command injection attempts"""
        signals = []
        
        for pattern in cls.COMMAND_INJECTION_PATTERNS:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                signals.append({
                    "type": SignalType.COMMAND_INJECTION,
                    "matched_text": match.group(),
                    "position": match.start(),
                    "severity": "high",
                })
        
        return signals
    
    @classmethod
    def detect_prompt_injection(cls, text: str) -> List[Dict[str, Any]]:
        """Detect prompt injection attempts"""
        signals = []
        
        for pattern in cls.PROMPT_INJECTION_PATTERNS:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                signals.append({
                    "type": SignalType.PROMPT_INJECTION,
                    "matched_text": match.group(),
                    "position": match.start(),
                    "severity": "high",
                })
        
        return signals
    
    @classmethod
    def detect_path_traversal(cls, text: str) -> List[Dict[str, Any]]:
        """Detect path traversal attempts"""
        signals = []
        pattern = r'(\.\./|\.\.\\)'
        
        matches = re.finditer(pattern, text)
        for match in matches:
            signals.append({
                "type": SignalType.PATH_TRAVERSAL,
                "matched_text": match.group(),
                "position": match.start(),
                "severity": "high",
            })
        
        return signals
    
    @classmethod
    def detect_xss(cls, text: str) -> List[Dict[str, Any]]:
        """Detect XSS attempts"""
        signals = []
        pattern = r'<script[^>]*>.*?</script>'
        
        matches = re.finditer(pattern, text, re.IGNORECASE | re.DOTALL)
        for match in matches:
            signals.append({
                "type": SignalType.XSS,
                "matched_text": match.group(),
                "position": match.start(),
                "severity": "medium",
            })
        
        return signals
    
    @classmethod
    def detect_intent_drift(
        cls,
        stated_intent: str,
        detected_intent: str,
        risk_threshold: float = 0.7
    ) -> Dict[str, Any]:
        """
        Detect intent drift between stated and detected intent
        
        Args:
            stated_intent: The stated intent from the agent
            detected_intent: The detected intent from behavior analysis
            risk_threshold: Risk threshold for flagging drift
            
        Returns:
            Signal if drift detected
        """
        # Simple keyword overlap for now (can be enhanced with embeddings)
        stated_words = set(stated_intent.lower().split())
        detected_words = set(detected_intent.lower().split())
        
        overlap = len(stated_words & detected_words)
        total = len(stated_words | detected_words)
        
        similarity = overlap / total if total > 0 else 0
        
        if similarity < risk_threshold:
            return {
                "type": SignalType.INTENT_DRIFT,
                "stated_intent": stated_intent,
                "detected_intent": detected_intent,
                "similarity": similarity,
                "severity": "high" if similarity < 0.3 else "medium",
            }
        
        return None
    
    @classmethod
    def detect_cost_spike(
        cls,
        current_cost: float,
        baseline_cost: float,
        threshold: float = 2.0
    ) -> Dict[str, Any]:
        """
        Detect cost spikes
        
        Args:
            current_cost: Current operation cost
            baseline_cost: Baseline cost
            threshold: Multiplier threshold for spike detection
            
        Returns:
            Signal if spike detected
        """
        if baseline_cost > 0 and current_cost > baseline_cost * threshold:
            return {
                "type": SignalType.COST_SPIKE,
                "current_cost": current_cost,
                "baseline_cost": baseline_cost,
                "multiplier": current_cost / baseline_cost,
                "severity": "high" if current_cost > baseline_cost * 5 else "medium",
            }
        
        return None
    
    @classmethod
    def detect_runaway_loop(
        cls,
        step_count: int,
        max_steps: int,
        threshold: float = 0.9
    ) -> Dict[str, Any]:
        """
        Detect potential runaway loops
        
        Args:
            step_count: Current step count
            max_steps: Maximum allowed steps
            threshold: Percentage threshold for warning
            
        Returns:
            Signal if runaway detected
        """
        if max_steps > 0 and step_count >= max_steps * threshold:
            return {
                "type": SignalType.RUNAWAY_LOOP,
                "step_count": step_count,
                "max_steps": max_steps,
                "percentage": step_count / max_steps,
                "severity": "critical" if step_count >= max_steps else "high",
            }
        
        return None
    
    @classmethod
    def analyze_all(cls, text: str) -> List[Dict[str, Any]]:
        """Run all detection on text"""
        signals = []
        
        signals.extend(cls.detect_pii(text))
        signals.extend(cls.detect_secrets(text))
        signals.extend(cls.detect_sql_injection(text))
        signals.extend(cls.detect_command_injection(text))
        signals.extend(cls.detect_prompt_injection(text))
        signals.extend(cls.detect_path_traversal(text))
        signals.extend(cls.detect_xss(text))
        
        return signals
