"""Pronunciation engine executing rule pipelines using BFS."""

from typing import List, Set, Dict, Optional
from korean_pronunciation.state import PronunciationState
from korean_pronunciation.tokenizer import tokenize
from korean_pronunciation.analyzers import get_analyzer, BaseMorphAnalyzer
from korean_pronunciation.rules.base import BaseRule


class PronunciationEngine:
    """BFS-based pronunciation engine.

    Explores all possible pronunciation branches of an input string
    by applying a pipeline of rules sequentially and deduplicating states.
    """

    def __init__(self, pipeline: List[BaseRule], analyzer: Optional[BaseMorphAnalyzer] = None):
        """Initialize the engine with a rule pipeline and an analyzer.

        If no analyzer is provided, the default one (Kiwi or Simple fallback) is used.
        """
        self.pipeline = pipeline
        self.analyzer = analyzer if analyzer is not None else get_analyzer()

    def get_pronunciations(self, text: str) -> List[dict]:
        """Convert input Korean text into all valid standard pronunciations.

        Returns a sorted list of dictionaries containing the pronunciation and applied rules.
        """
        if not text:
            return []

        # 1. Tokenize and decompose into initial state
        initial_state = tokenize(text, self.analyzer)
        
        # 2. Explore pronunciation states using BFS
        current_states: List[PronunciationState] = [initial_state]
        
        for rule in self.pipeline:
            next_states: List[PronunciationState] = []
            seen_keys: Set[str] = set()
            
            for state in current_states:
                # Apply the rule (might produce 1 or more states)
                outputs = rule.apply(state)
                
                # Deduplicate immediately to keep space complexity small
                for out_state in outputs:
                    key = out_state.canonical_key()
                    if key not in seen_keys:
                        seen_keys.add(key)
                        next_states.append(out_state)
            
            current_states = next_states

        # 3. Format final composed results
        results = []
        seen_keys = set()
        for state in current_states:
            key = state.canonical_key()
            if key not in seen_keys:
                seen_keys.add(key)
                results.append({
                    "pronunciation": key,
                    "applied_rules": list(state.applied_rules)
                })
        
        results.sort(key=lambda x: x["pronunciation"])
        return results
