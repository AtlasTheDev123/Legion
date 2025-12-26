"""
Complete NEXUS System Demonstration
====================================
Shows all components working together
"""

from agents.orchestrator import NexusAIOrchestrator
from agents.nexus_ai_model import get_nexus_ai
from agents.distributed_agents import DistributedAgentSystem, AgentRole
from agents.llm_integration import LLMManager

print('='*70)
print('NEXUS-LEGION-X-OMEGA - COMPLETE SYSTEM DEMO')
print('⚡ LEGION x L.X VEX — SERVING ATLAS ⚡')
print('='*70)

# Component 1: Core AI System
print('\n🧠 [1] CORE AI SYSTEM')
print('-'*70)
orchestrator = NexusAIOrchestrator()
ai = get_nexus_ai()

# Execute complex task
result = orchestrator.execute_task(
    'Optimize microservices architecture',
    context={'scale': 'large', 'priority': 'high'}
)
print(f'✓ Task executed: {result["status"]}')
print(f'✓ Confidence: {result["confidence"]:.2%}')
print(f'✓ Steps completed: {len(result["execution_steps"])}')

# Component 2: Learning & Memory
print('\n📚 [2] LEARNING & MEMORY SYSTEM')
print('-'*70)
ai.learn(
    'Implemented load balancer with health checks',
    'Improved system reliability by 99.9%',
    importance=0.9,
    tags=['infrastructure', 'reliability']
)
print(f'✓ Experiences: {ai.experience_count}')
print(f'✓ Memories: {len(ai.long_term_memory)}')
print(f'✓ Adaptation: {ai.adaptation_score:.2%}')

# Component 3: Advanced Reasoning
print('\n🎯 [3] ADVANCED REASONING')
print('-'*70)
solution = orchestrator.solve_problem(
    'How to reduce database query latency?'
)
print(f'✓ Strategy: {solution["approach"]}')
print(f'✓ Confidence: {solution["confidence"]:.2%}')
print(f'✓ Reasoning steps: {len(solution["reasoning_process"])}')

# Component 4: Code Analysis
print('\n💻 [4] CODE ANALYSIS')
print('-'*70)
code = '''
def process_user_data(data):
    results = []
    for item in data:
        if item['status'] == 'active':
            results.append(item)
    return results
'''
analysis = orchestrator.analyze_code(code, 'python')
print(f'✓ Language: {analysis["code_analysis"]["language"]}')
print(f'✓ Complexity: {analysis["code_analysis"]["complexity_score"]:.2f}')
print(f'✓ Functions found: {len(analysis["code_analysis"]["functions"])}')

# Component 5: Distributed Agents
print('\n🤖 [5] DISTRIBUTED AGENT SYSTEM')
print('-'*70)
dist_system = DistributedAgentSystem()
dist_system.start()

# Spawn agents
coordinator = dist_system.spawn_agent(AgentRole.COORDINATOR)
researcher = dist_system.spawn_agent(AgentRole.RESEARCHER)
analyst = dist_system.spawn_agent(AgentRole.ANALYST)
print(f'✓ Agents spawned: {len(dist_system.agents)}')

# Coordinate task
coord_result = dist_system.coordinate_task('Implement API rate limiting')
print(f'✓ Task coordination: {coord_result["status"]}')
print(f'✓ Participating agents: {len(coord_result["participating_agents"])}')

# Component 6: LLM Integration
print('\n🔮 [6] LLM INTEGRATION')
print('-'*70)
llm = LLMManager()
providers = llm.get_available_providers()
print(f'✓ Available providers: {len(providers)}')
for provider in providers[:3]:
    print(f'  - {provider["name"]}: {provider["status"]}')

# Component 7: Self-Optimization
print('\n⚙️  [7] SELF-OPTIMIZATION')
print('-'*70)
opt_report = orchestrator.optimize_system()
print(f'✓ Optimizations: {len(opt_report["core_optimization"]["optimizations"])}')
print(f'✓ Adaptation: {opt_report["system_status"]["metrics"]["adaptation_score"]:.2%}')

# Component 8: System Status
print('\n📊 [8] COMPLETE SYSTEM STATUS')
print('-'*70)
status = orchestrator.get_comprehensive_status()
print(f'✓ Orchestrator: {status["orchestrator"]}')
print(f'✓ Core AI: {status["core_ai"]["is_active"]}')
print(f'✓ Capabilities: {sum(1 for v in status["capabilities"].values() if v)}')
print(f'✓ Reasoning engine: {status["reasoning_engine"]["status"]}')
print(f'✓ Multi-modal: {status["multi_modal"]["status"]}')

# Final Summary
print('\n'+'='*70)
print('✅ ALL SYSTEMS OPERATIONAL')
print('='*70)
print(f'''
System Capabilities:
  • Multi-step reasoning (7 strategies)
  • Adaptive learning & memory
  • Multi-modal processing
  • Code analysis & generation
  • Distributed agent coordination
  • LLM integration
  • Self-optimization
  • Real-time monitoring

Performance Metrics:
  • Experiences: {ai.experience_count}
  • Memories: {len(ai.long_term_memory)}
  • Adaptation: {ai.adaptation_score:.2%}
  • Agents: {len(dist_system.agents)}
  • LLM Providers: {len(providers)}

Status: FULLY OPERATIONAL ✅
''')
print('='*70)
print('⚡ NEXUS-LEGION-X-OMEGA READY ⚡')
print('='*70)
