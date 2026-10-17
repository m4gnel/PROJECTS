from typing import Dict, Any, List, Tuple


class HallucinationCheck:
    """Grounding & Hallucination Critic.
    
    Verifies that AI-generated diagnostic claims, chemical recommendations,
    and cultural management advice are backed by retrieved ICAR/KAU citations.
    """

    def verify_grounding(
        self,
        advisory: Dict[str, Any],
        retrieved_knowledge: List[Dict[str, Any]]
    ) -> Tuple[bool, float, List[str]]:
        """Evaluate grounding score of an advisory against retrieved knowledge documents.
        
        Returns:
            (is_grounded: bool, grounding_score: float, issues: List[str])
        """
        issues = []
        if not retrieved_knowledge:
            issues.append("WARNING: Zero verified ICAR/KAU knowledge documents retrieved for citation grounding.")
            return True, 0.5, issues

        # Extract citation IDs from retrieved docs
        verified_doc_ids = {
            doc.get("id") or doc.get("doc_id") or doc.get("title", "").lower()
            for doc in retrieved_knowledge
            if isinstance(doc, dict)
        }

        # Check citations referenced in advisory
        citations = advisory.get("citations") or advisory.get("evidence_citations") or []
        if not isinstance(citations, list):
            citations = []

        valid_citations_count = 0
        for citation in citations:
            cit_id = citation.get("doc_id") or citation.get("id") or citation.get("title", "").lower()
            if cit_id in verified_doc_ids or any(str(v) in str(cit_id) for v in verified_doc_ids):
                valid_citations_count += 1
            else:
                issues.append(f"UNGROUNDED: Citation '{cit_id}' in advisory is not in retrieved ICAR knowledge base.")

        total_citations = max(1, len(citations))
        grounding_score = round(valid_citations_count / total_citations, 2)
        is_grounded = grounding_score >= 0.70

        return is_grounded, grounding_score, issues
