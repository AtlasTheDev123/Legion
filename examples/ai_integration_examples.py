"""
NEXUS AI Integration Examples
==============================
Practical examples of integrating the NEXUS AI Model
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.orchestrator import NexusAIOrchestrator
from agents.nexus_ai_model import get_nexus_ai
from agents.advanced_reasoning import AdvancedReasoner
from agents.multi_modal_ai import MultiModalAI, ModalInput, Modality


def example_1_basic_task_execution():
    """Example 1: Execute a simple task"""
    print("\n" + "="*70)
    print("EXAMPLE 1: Basic Task Execution")
    print("="*70)
    
    ai = NexusAIOrchestrator()
    
    result = ai.execute_task(
        "Create a REST API for user management",
        context={
            "framework": "FastAPI",
            "database": "PostgreSQL",
            "auth": "JWT"
        }
    )
    
    print(f"Status: {result['status']}")
    print(f"Strategy: {result['strategy_used']}")
    print(f"Steps: {len(result['execution_steps'])}")
    print(f"Confidence: {result['confidence']:.2%}")
    
    return result


def example_2_continuous_learning():
    """Example 2: Teach the AI from experiences"""
    print("\n" + "="*70)
    print("EXAMPLE 2: Continuous Learning")
    print("="*70)
    
    ai = get_nexus_ai()
    
    # Learn from success
    ai.learn(
        experience="Implemented Redis caching for API responses",
        outcome="Response time reduced from 200ms to 20ms",
        importance=0.9,
        tags=["performance", "caching", "redis"]
    )
    
    # Learn from failure
    ai.learn(
        experience="Attempted to scale database vertically",
        outcome="Hit hardware limits, horizontal scaling needed",
        importance=0.8,
        tags=["scaling", "database", "architecture"]
    )
    
    # Learn best practice
    ai.learn(
        experience="Added input validation to all endpoints",
        outcome="Prevented 95% of malformed requests",
        importance=0.85,
        tags=["security", "validation", "api"]
    )
    
    print(f"Total experiences: {ai.experience_count}")
    print(f"Memory size: {len(ai.long_term_memory)}")
    print(f"Adaptation score: {ai.adaptation_score:.2%}")
    
    return ai


def example_3_code_review():
    """Example 3: AI-powered code review"""
    print("\n" + "="*70)
    print("EXAMPLE 3: Automated Code Review")
    print("="*70)
    
    ai = NexusAIOrchestrator()
    
    code_to_review = """
def authenticate(username, password):
    user = db.query("SELECT * FROM users WHERE username='" + username + "'")
    if user and user.password == password:
        return generate_token(user)
    return None
"""
    
    analysis = ai.analyze_code(code_to_review, "python")
    
    print("Code Analysis Results:")
    print(f"  Language: {analysis['code_analysis']['language']}")
    print(f"  Complexity: {analysis['code_analysis']['complexity_score']:.2f}")
    print(f"  Issues found: {len(analysis['issues'])}")
    print(f"  Recommendations: {len(analysis['recommendations'])}")
    
    print("\nQuality Assessment:")
    for step in analysis['quality_assessment'][:3]:
        print(f"  - {step}")
    
    return analysis


def example_4_problem_solving_workflow():
    """Example 4: Multi-step problem solving"""
    print("\n" + "="*70)
    print("EXAMPLE 4: Problem Solving Workflow")
    print("="*70)
    
    ai = NexusAIOrchestrator()
    
    problem = "Our API is slow. Users report 3-5 second response times."
    
    # Solve the problem
    solution = ai.solve_problem(problem)
    
    print(f"Problem: {problem}")
    print(f"\nApproach: {solution['approach']}")
    print(f"Confidence: {solution['confidence']:.2%}")
    print(f"\nReasoning steps ({len(solution['reasoning_process'])}):")
    for i, step in enumerate(solution['reasoning_process'], 1):
        print(f"  {i}. {step}")
    
    print(f"\nValidation: {solution['validation']['verdict']}")
    print(f"Consistency: {solution['validation']['consistency_score']:.2%}")
    
    return solution


def example_5_autonomous_optimization():
    """Example 5: Let AI optimize itself"""
    print("\n" + "="*70)
    print("EXAMPLE 5: Self-Optimization")
    print("="*70)
    
    ai = NexusAIOrchestrator()
    
    # Add some experiences first
    for i in range(20):
        ai.core_ai.learn(
            f"Experience {i}",
            f"Outcome {i}",
            importance=0.5 + (i % 5) * 0.1,
            tags=[f"tag{i % 3}"]
        )
    
    # Trigger optimization
    report = ai.optimize_system()
    
    print("Optimization Report:")
    print(f"  Experiences: {report['system_status']['metrics']['experience_count']}")
    print(f"  Adaptation: {report['system_status']['metrics']['adaptation_score']:.2%}")
    print(f"  Memory: {report['system_status']['metrics']['memory_count']} items")
    print(f"\nOptimizations applied: {len(report['core_optimization']['optimizations'])}")
    for opt in report['core_optimization']['optimizations']:
        print(f"  - {opt}")
    
    return report


def example_6_multi_modal_analysis():
    """Example 6: Analyze text and code together"""
    print("\n" + "="*70)
    print("EXAMPLE 6: Multi-Modal Analysis")
    print("="*70)
    
    mmai = MultiModalAI()
    
    # Text requirement
    text_input = ModalInput(
        modality=Modality.TEXT,
        content="We need a secure authentication system with JWT tokens",
        metadata={}
    )
    
    # Code implementation
    code_input = ModalInput(
        modality=Modality.CODE,
        content="""
def create_token(user_id):
    payload = {'user_id': user_id, 'exp': time.time() + 3600}
    return jwt.encode(payload, SECRET_KEY, algorithm='HS256')
""",
        metadata={"language": "python"}
    )
    
    # Analyze both
    results = mmai.process([text_input, code_input])
    
    print("Text Analysis:")
    print(f"  Sentiment: {results[0].content['sentiment']}")
    print(f"  Complexity: {results[0].content['complexity']}")
    
    print("\nCode Analysis:")
    print(f"  Language: {results[1].content['language']}")
    print(f"  Functions: {results[1].content['functions']}")
    
    # Cross-modal reasoning
    synthesis = mmai.cross_modal_reasoning([text_input, code_input])
    print(f"\nCross-Modal Insights:")
    for insight in synthesis['cross_modal_insights']:
        print(f"  - {insight}")
    
    return results, synthesis


def example_7_reasoning_strategies():
    """Example 7: Compare different reasoning strategies"""
    print("\n" + "="*70)
    print("EXAMPLE 7: Reasoning Strategy Comparison")
    print("="*70)
    
    reasoner = AdvancedReasoner()
    
    problem = "Design a scalable microservices architecture"
    
    # Chain-of-thought
    chain = reasoner.chain_of_thought(problem, steps=5)
    print("Chain-of-Thought:")
    for step in chain:
        print(f"  → {step}")
    
    # Tree-of-thought
    tree = reasoner.tree_of_thought(problem)
    print(f"\nTree-of-Thought (exploring {len(tree['branches'])} paths):")
    for branch in tree['branches']:
        print(f"  {branch['approach']}: score {branch['score']:.2f}")
    print(f"  Recommended: {tree['recommended']}")
    
    # Meta-reasoning
    meta = reasoner.meta_reasoning(problem)
    print(f"\nMeta-Reasoning:")
    print(f"  Best strategy: {meta['best_strategy']}")
    print(f"  Confidence: {meta['confidence']:.2%}")
    
    return chain, tree, meta


def example_8_validation_pipeline():
    """Example 8: Validate AI outputs"""
    print("\n" + "="*70)
    print("EXAMPLE 8: Output Validation Pipeline")
    print("="*70)
    
    reasoner = AdvancedReasoner()
    
    claim = "Using Redis will improve our API performance by 70%"
    
    # Self-consistency check
    attempts = [
        "Redis caching improves performance significantly",
        "Caching with Redis yields 60-80% improvement",
        "Redis provides substantial performance gains"
    ]
    consistency = reasoner.self_consistency_check(attempts)
    
    print("Self-Consistency Check:")
    print(f"  Attempts: {consistency['total_attempts']}")
    print(f"  Consistency: {consistency['consistency_score']:.2%}")
    print(f"  Verdict: {consistency['verdict']}")
    
    # Adversarial validation
    validation = reasoner.adversarial_validation(claim)
    
    print("\nAdversarial Validation:")
    print(f"  Claim: {claim}")
    print(f"  Robustness: {validation['robustness_score']:.2%}")
    print(f"  Verdict: {validation['verdict']}")
    print(f"  Challenges addressed: {len(validation['challenges'])}")
    
    return consistency, validation


def run_all_examples():
    """Run all integration examples"""
    print("\n" + "="*70)
    print("NEXUS AI MODEL - INTEGRATION EXAMPLES")
    print("⚡ LEGION x L.X VEX — SERVING ATLAS ⚡")
    print("="*70)
    
    try:
        example_1_basic_task_execution()
        example_2_continuous_learning()
        example_3_code_review()
        example_4_problem_solving_workflow()
        example_5_autonomous_optimization()
        example_6_multi_modal_analysis()
        example_7_reasoning_strategies()
        example_8_validation_pipeline()
        
        print("\n" + "="*70)
        print("✅ All examples completed successfully!")
        print("="*70)
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    run_all_examples()
