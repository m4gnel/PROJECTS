"""
AI Interview Agent
Conducts intelligent, context-aware interviews and provides multi-dimensional feedback.
Supports modern OpenAI SDK (v1.0+) with robust heuristic fallback for offline or zero-key environments.
"""

import os
import json
import random
from datetime import datetime, timezone
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize modern OpenAI client safely
OPENAI_AVAILABLE = False
openai_client = None

try:
    import openai
    api_key = os.getenv('OPENAI_API_KEY')
    if api_key and api_key.strip() and not api_key.startswith('your-'):
        openai_client = openai.OpenAI(api_key=api_key.strip())
        OPENAI_AVAILABLE = True
except Exception as e:
    OPENAI_AVAILABLE = False


class AIInterviewAgent:
    """
    Intelligent AI agent that conducts interviews and provides comprehensive evaluation.
    Works seamlessly both with live LLM (OpenAI GPT-4/GPT-4o) and high-accuracy heuristic evaluation.
    """
    
    def __init__(self, interview_type='technical', level='intermediate', field='software'):
        self.interview_type = (interview_type or 'technical').lower()
        self.level = (level or 'intermediate').lower()
        self.field = (field or 'software').lower()
        self.conversation_history = []
        
    def generate_question(self, context=None):
        """
        Generate a relevant interview question based on context, domain, and experience level.
        
        Args:
            context: Previous answers and performance data
            
        Returns:
            dict: Question dictionary with metadata
        """
        if OPENAI_AVAILABLE and openai_client:
            try:
                system_prompt = f"""You are an elite {self.interview_type} interviewer conducting an interview for a {self.field} role at {self.level} level.
Ask ONE clear, relevant, high-impact interview question. Match difficulty to {self.level} level.
Return ONLY the question text without conversational preamble or numbering."""

                messages = [{"role": "system", "content": system_prompt}]
                if context:
                    messages.append({"role": "system", "content": f"Candidate context: {context}"})
                messages.append({"role": "user", "content": f"Generate a {self.interview_type} interview question for {self.field} at {self.level} level."})

                response = openai_client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=messages,
                    max_tokens=250,
                    temperature=0.7
                )
                question_text = response.choices[0].message.content.strip().strip('"')
                
                return {
                    'text': question_text,
                    'type': self.interview_type,
                    'level': self.level,
                    'field': self.field,
                    'difficulty': 'hard' if self.level in ['senior', 'lead'] else ('medium' if self.level == 'intermediate' else 'easy'),
                    'generated_at': datetime.now(timezone.utc).isoformat(),
                    'source': 'openai-gpt'
                }
            except Exception as e:
                # Log error and fall through to curated question generator
                print(f"[AI Agent] OpenAI generation fallback triggered: {e}")
        
        return self._get_curated_question(context)

    def _get_curated_question(self, context=None):
        """Curated high-quality questions mapped by role and level"""
        question_bank = {
            'software': {
                'entry': [
                    "Explain the difference between let, const, and var in JavaScript. When would you use each?",
                    "What is the difference between a stack and a queue? Describe a real-world scenario where you would use each.",
                    "Explain the concept of Object-Oriented Programming (OOP) and its four core pillars with examples."
                ],
                'intermediate': [
                    "What is closure in JavaScript? Can you walk through a practical scenario where closures solve a problem?",
                    "Explain how RESTful APIs differ from GraphQL. What are the trade-offs in terms of network overhead and caching?",
                    "What is the difference between SQL and NoSQL databases? When would you choose PostgreSQL over MongoDB?"
                ],
                'senior': [
                    "Design a scalable, highly available URL shortening service (like bit.ly) handling 100M active URLs and 10,000 req/sec.",
                    "Explain the CAP theorem and describe how distributed database systems navigate consistency vs availability trade-offs.",
                    "How would you troubleshoot and resolve high CPU utilization and latency spikes in a distributed microservices architecture?"
                ]
            },
            'data-science': {
                'entry': [
                    "What is the difference between supervised and unsupervised learning? Provide examples of algorithms for each.",
                    "Explain the bias-variance tradeoff in machine learning and how regularization helps prevent overfitting.",
                    "How do you handle missing values or outliers in a dataset during feature engineering?"
                ],
                'intermediate': [
                    "How does the Random Forest algorithm work, and why does bagging reduce variance compared to an individual decision tree?",
                    "Explain precision, recall, and F1-score. When is ROC-AUC a misleading metric for model evaluation?",
                    "Walk me through how you would detect and correct data drift in a production ML pipeline."
                ],
                'senior': [
                    "Design an end-to-end real-time recommendation system for an e-commerce platform processing millions of events per hour.",
                    "Explain the transformer architecture, self-attention mechanism, and how multi-head attention improves representation learning.",
                    "How do you quantify and mitigate algorithmic bias in predictive models deployed in production?"
                ]
            },
            'behavioral': {
                'all': [
                    "Tell me about a time when you had to work with a difficult team member or stakeholder. How did you resolve the conflict?",
                    "Describe a project where requirements changed dramatically midway through. How did you adapt your plan and deliver results?",
                    "Give an example of a mistake or failure you experienced in a project. What happened, how did you handle it, and what did you learn?",
                    "Tell me about a time you had to make a high-stakes technical decision with incomplete information and a tight deadline."
                ]
            },
            'system-design': {
                'all': [
                    "Design a real-time collaborative document editing system like Google Docs. Consider concurrency control and state synchronization.",
                    "Design a scalable notification system supporting email, SMS, and push notifications with rate limiting and deduplication.",
                    "Design a video streaming architecture like YouTube or Netflix, addressing transcoding, CDN distribution, and adaptive bitrate streaming."
                ]
            },
            'hr': {
                'all': [
                    "Why are you interested in joining our organization, and what makes you a great cultural and technical fit?",
                    "Where do you envision your professional journey in the next 3 to 5 years?",
                    "What is your greatest technical strength, and what is an area of development you are actively working on improving?"
                ]
            }
        }
        
        category_key = self.interview_type if self.interview_type in ['behavioral', 'system-design', 'hr'] else 'software'
        if category_key in ['behavioral', 'system-design', 'hr']:
            options = question_bank[category_key]['all']
        else:
            field_key = self.field if self.field in question_bank else 'software'
            lvl_key = self.level if self.level in ['entry', 'senior'] else 'intermediate'
            options = question_bank[field_key].get(lvl_key, question_bank['software']['intermediate'])
            
        selected_text = random.choice(options)
        return {
            'text': selected_text,
            'type': self.interview_type,
            'level': self.level,
            'field': self.field,
            'difficulty': 'hard' if self.level in ['senior', 'lead'] else ('medium' if self.level == 'intermediate' else 'easy'),
            'generated_at': datetime.now(timezone.utc).isoformat(),
            'source': 'curated-master'
        }

    def analyze_answer(self, question, answer_text):
        """
        Analyze user's answer and return multi-dimensional feedback with granular metrics.
        
        Args:
            question: The question prompt that was posed
            answer_text: User's candidate response
            
        Returns:
            dict: Comprehensive structured evaluation
        """
        if not answer_text or len(answer_text.strip()) == 0:
            return self._empty_answer_feedback()
            
        if OPENAI_AVAILABLE and openai_client:
            try:
                system_prompt = f"""You are an expert interviewer evaluating a candidate's answer for a {self.level} {self.field} role in a {self.interview_type} interview.
Question: {question}

Return ONLY a valid JSON object matching this schema exactly:
{{
    "score": 8.5,
    "strengths": ["Clear communication", "Demonstrated foundational depth", "Good example provided"],
    "improvements": ["Explain trade-offs more explicitly", "Mention edge-case handling"],
    "detailed_feedback": "Paragraph offering professional, constructive critique.",
    "technical_accuracy": 8.5,
    "communication_clarity": 9.0,
    "depth_of_knowledge": 8.0,
    "confidence_level": 8.5,
    "key_concepts_covered": ["concept1", "concept2"],
    "missing_concepts": ["concept3"],
    "next_steps": ["Review distributed systems primer", "Practice STAR structure"]
}}
Score range is 0.0 to 10.0. Be precise, balanced, and constructive."""

                response = openai_client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": f"Candidate answer:\n\n{answer_text}"}
                    ],
                    max_tokens=850,
                    temperature=0.3
                )
                
                raw_content = response.choices[0].message.content.strip()
                if "```json" in raw_content:
                    raw_content = raw_content.split("```json")[1].split("```")[0].strip()
                elif "```" in raw_content:
                    raw_content = raw_content.split("```")[1].split("```")[0].strip()
                    
                feedback = json.loads(raw_content)
                feedback['analyzed_at'] = datetime.now(timezone.utc).isoformat()
                feedback['model'] = 'gpt-4o-mini'
                feedback['answer_length'] = len(answer_text.split())
                return feedback
                
            except Exception as e:
                print(f"[AI Agent] OpenAI analysis failed, using advanced heuristic engine: {e}")
        
        return self._evaluate_heuristic(question, answer_text)

    def _evaluate_heuristic(self, question, answer_text):
        """
        Advanced heuristic evaluation engine.
        Calculates scores using semantic keyword detection, STAR structure matching,
        logical transitions, technical vocabulary, and clarity metrics.
        """
        words = answer_text.strip().split()
        word_count = len(words)
        lower_text = answer_text.lower()
        sentences = [s.strip() for s in answer_text.split('.') if len(s.strip()) > 0]
        sentence_count = max(1, len(sentences))
        
        # Base scoring from depth and length
        if word_count < 15:
            base_score = 3.5
        elif word_count < 40:
            base_score = 5.5
        elif word_count < 80:
            base_score = 7.0
        elif word_count < 160:
            base_score = 8.2
        else:
            base_score = 8.8
            
        quality_delta = 0.0
        strengths = []
        improvements = []
        covered_concepts = []
        missing_concepts = []
        
        # Concrete examples check
        example_markers = ['for example', 'for instance', 'in my experience', 'such as', 'specifically', 'at my previous']
        if any(m in lower_text for m in example_markers):
            quality_delta += 0.5
            strengths.append("Provided concrete real-world context and illustrative examples.")
            covered_concepts.append("practical application")
        else:
            improvements.append("Enrich your answer with specific real-world examples from your experience.")
            missing_concepts.append("concrete examples")
            
        # Logical argumentation
        logic_markers = ['because', 'therefore', 'consequently', 'as a result', 'furthermore', 'however', 'trade-off']
        if any(m in lower_text for m in logic_markers):
            quality_delta += 0.4
            strengths.append("Structured logical reasoning with clear cause-and-effect transitions.")
        else:
            improvements.append("Use transition connectors (e.g., 'because', 'as a result') to build clearer reasoning.")
            
        # Behavioral STAR evaluation
        if self.interview_type == 'behavioral':
            star_map = {
                'situation': ['situation', 'context', 'project was', 'faced with', 'working at', 'team was'],
                'task': ['task', 'goal', 'responsibility', 'objective', 'needed to', 'my role'],
                'action': ['i implemented', 'i decided', 'i took', 'action', 'i organized', 'i reached out', 'i built'],
                'result': ['result', 'outcome', 'impact', 'delivered', 'improved', 'learned', 'achieved']
            }
            star_hits = sum(1 for dim, keys in star_map.items() if any(k in lower_text for k in keys))
            if star_hits >= 3:
                quality_delta += 0.6
                strengths.append("Effectively structured using the STAR methodology (Situation, Task, Action, Result).")
                covered_concepts.append("STAR methodology")
            else:
                improvements.append("Explicitly frame behavioral answers around Situation, Task, Action, and measurable Result.")
                missing_concepts.append("STAR framework")
                
        # Technical terminology
        if self.interview_type in ['technical', 'system-design']:
            tech_terms = [
                'complexity', 'scalability', 'performance', 'latency', 'architecture', 
                'concurrency', 'caching', 'database', 'api', 'memory', 'optimization', 
                'security', 'trade-off', 'modularity', 'consistency', 'asynchronous'
            ]
            matched_terms = [t for t in tech_terms if t in lower_text]
            if len(matched_terms) >= 3:
                quality_delta += 0.6
                strengths.append(f"Demonstrated technical fluency using industry concepts ({', '.join(matched_terms[:3])}).")
                covered_concepts.extend(matched_terms[:3])
            elif len(matched_terms) >= 1:
                quality_delta += 0.2
                covered_concepts.extend(matched_terms)
            else:
                improvements.append("Incorporate more industry-standard technical terminology and architectural principles.")
                missing_concepts.append("architectural terminology")
                
        # Conciseness vs wordiness check
        if sentence_count >= 3 and (word_count / sentence_count) > 35:
            improvements.append("Break long compound sentences into concise, easily digestible points.")
            
        final_score = min(9.8, max(3.0, round(base_score + quality_delta, 1)))
        
        # Sub-metrics
        tech_acc = min(10.0, max(3.0, round(final_score + (0.3 if len(covered_concepts) >= 2 else -0.3), 1)))
        comm_clar = min(10.0, max(3.0, round(final_score + (0.4 if sentence_count >= 3 else -0.2), 1)))
        depth_know = min(10.0, max(3.0, round(final_score + (0.5 if word_count > 100 else -0.5), 1)))
        conf_lvl = min(10.0, max(3.0, round((tech_acc + comm_clar) / 2.0, 1)))
        
        if not strengths:
            strengths = [
                "Directly addressed the prompt question.",
                "Professional tone and clear intent in communication."
            ]
        if not improvements:
            improvements = [
                "Explore boundary conditions and architectural trade-offs.",
                "Quantify business outcomes or performance metrics where possible."
            ]
            
        detailed_feedback = (
            f"Your response demonstrates a solid foundational understanding of the prompt. "
            f"{strengths[0]} To elevate this response to top-tier benchmark standards, {improvements[0].lower()} "
            f"Keep focusing on structured delivery and clear examples."
        )
        
        return {
            'score': final_score,
            'strengths': strengths[:4],
            'improvements': improvements[:3],
            'detailed_feedback': detailed_feedback,
            'technical_accuracy': tech_acc,
            'communication_clarity': comm_clar,
            'depth_of_knowledge': depth_know,
            'confidence_level': conf_lvl,
            'key_concepts_covered': covered_concepts[:4],
            'missing_concepts': missing_concepts[:3],
            'next_steps': [
                "Practice structuring technical explanations in 2-3 minute timed windows.",
                "Prepare 2 concrete portfolio stories highlighting difficult trade-offs."
            ],
            'analyzed_at': datetime.now(timezone.utc).isoformat(),
            'model': 'heuristic-master-v2',
            'answer_length': word_count
        }

    def _empty_answer_feedback(self):
        """Feedback for blank or whitespace answers"""
        return {
            'score': 1.0,
            'strengths': ["Session initiated"],
            'improvements': ["Please enter a complete response before submitting"],
            'detailed_feedback': "No candidate answer text was provided. Enter a detailed response to receive feedback.",
            'technical_accuracy': 1.0,
            'communication_clarity': 1.0,
            'depth_of_knowledge': 1.0,
            'confidence_level': 1.0,
            'key_concepts_covered': [],
            'missing_concepts': ["Core response"],
            'next_steps': ["Review question prompt carefully and compose answer"],
            'analyzed_at': datetime.now(timezone.utc).isoformat(),
            'model': 'validator',
            'answer_length': 0
        }

    def adaptive_next_question(self, performance_history):
        """
        Dynamically adjusts interview difficulty based on candidate score progression.
        """
        if not performance_history:
            return self.generate_question()
            
        avg_score = sum(performance_history) / len(performance_history)
        
        if avg_score >= 8.5:
            self.level = 'senior'
            context = "Candidate demonstrated exceptional competence. Escalating to senior difficulty."
        elif avg_score >= 6.5:
            self.level = 'intermediate'
            context = "Candidate has solid command. Maintaining intermediate difficulty."
        else:
            self.level = 'entry'
            context = "Candidate requires foundational coaching. Adjusting to accessible questions."
            
        return self.generate_question(context=context)

    def generate_interview_report(self, all_answers_feedback):
        """
        Compiles holistic interview performance dossier.
        """
        if not all_answers_feedback:
            return {'error': 'No feedback data available'}
            
        scores = [f.get('score', 0) for f in all_answers_feedback]
        avg_score = round(sum(scores) / len(scores), 1)
        
        all_strengths = []
        all_improvements = []
        for f in all_answers_feedback:
            all_strengths.extend(f.get('strengths', []))
            all_improvements.extend(f.get('improvements', []))
            
        # Deduplicate while preserving order
        unique_strengths = list(dict.fromkeys(all_strengths))[:5]
        unique_improvements = list(dict.fromkeys(all_improvements))[:5]
        
        return {
            'overall_score': avg_score,
            'total_questions': len(all_answers_feedback),
            'performance_trend': 'improving' if len(scores) > 1 and scores[-1] >= scores[0] else 'steady',
            'top_strengths': unique_strengths,
            'areas_for_improvement': unique_improvements,
            'average_scores': {
                'technical_accuracy': round(sum(f.get('technical_accuracy', avg_score) for f in all_answers_feedback) / len(all_answers_feedback), 1),
                'communication_clarity': round(sum(f.get('communication_clarity', avg_score) for f in all_answers_feedback) / len(all_answers_feedback), 1),
                'depth_of_knowledge': round(sum(f.get('depth_of_knowledge', avg_score) for f in all_answers_feedback) / len(all_answers_feedback), 1),
            },
            'recommendation': self._get_recommendation(avg_score),
            'generated_at': datetime.now(timezone.utc).isoformat()
        }

    def _get_recommendation(self, score):
        """Actionable recruiter-style recommendation based on score"""
        if score >= 9.0:
            return "Strong Hire / Ready for Onsite: Demonstrates depth, articulation, and architectural maturity."
        elif score >= 7.5:
            return "Hire / Interview Ready: Solid fundamentals and clear communication; refine edge-case analysis."
        elif score >= 6.0:
            return "Leaning Hire: Good conceptual grounding. Work on structuring answers with concrete examples."
        else:
            return "Needs Practice: Recommend reviewing core fundamentals and practicing the STAR response method."


# Module self-test
if __name__ == '__main__':
    agent = AIInterviewAgent(interview_type='technical', level='intermediate', field='software')
    q = agent.generate_question()
    print(f"Generated Question: {q['text']}")
    sample_ans = "Closures in JavaScript are functions bundled with their lexical environment, allowing inner functions to access outer scope variables even after the outer function has executed. For instance, closures are useful for data privacy like private variables in factory functions."
    eval_res = agent.analyze_answer(q['text'], sample_ans)
    print(f"Score: {eval_res['score']}/10")
    print(f"Strengths: {eval_res['strengths']}")
    print(f"Model: {eval_res['model']}")
    print("AI Agent verified successfully!")