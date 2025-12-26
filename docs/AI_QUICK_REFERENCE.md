# NEXUS AI Model - Quick Reference

## 🚀 Quick Start

```python
from agents.orchestrator import NexusAIOrchestrator

# Initialize
ai = NexusAIOrchestrator()

# Execute task
result = ai.execute_task("Your task here")
print(result['status'])
```

## 🧠 Core Capabilities

### 1. Task Execution
```python
result = ai.execute_task(
    "Design authentication system",
    context={"security": "high"}
)
```

### 2. Code Analysis
```python
analysis = ai.analyze_code(code_string, "python")
print(analysis['code_analysis']['complexity_score'])
```

### 3. Problem Solving
```python
solution = ai.solve_problem("How to optimize performance?")
print(solution['confidence'])
```

### 4. Learning
```python
from agents.nexus_ai_model import get_nexus_ai

ai = get_nexus_ai()
ai.learn(
    experience="Implemented feature X",
    outcome="Performance improved by 50%",
    importance=0.9,
    tags=["optimization"]
)
```

### 5. Self-Optimization
```python
report = ai.optimize_system()
print(report['core_optimization'])
```

## 🎯 Reasoning Strategies

| Strategy | Use Case | Code |
|----------|----------|------|
| Chain-of-Thought | Sequential problems | `reasoner.chain_of_thought(problem)` |
| Tree-of-Thought | Multiple solutions | `reasoner.tree_of_thought(problem)` |
| Analogical | Similar past cases | `reasoner.analogical_reasoning(problem, cases)` |
| Counterfactual | What-if scenarios | `reasoner.counterfactual_reasoning(situation, what_if)` |
| Meta-Reasoning | Strategy selection | `reasoner.meta_reasoning(problem)` |

## 📊 Status & Metrics

```python
status = ai.get_comprehensive_status()

# Key metrics
print(status['core_ai']['metrics']['experience_count'])
print(status['core_ai']['metrics']['adaptation_score'])
print(status['core_ai']['metrics']['memory_count'])
```

## 🔧 Configuration

```python
from agents.nexus_ai_model import NexusAIModel

# Custom configuration
ai = NexusAIModel(
    model_id="custom-id",
    memory_path="custom/path.json"
)

# Adjust parameters
ai.learning_rate = 0.02
ai.confidence_threshold = 0.8
ai.max_reasoning_depth = 15
```

## 🎨 Multi-Modal Processing

```python
from agents.multi_modal_ai import MultiModalAI, ModalInput, Modality

mmai = MultiModalAI()

# Text
text_input = ModalInput(Modality.TEXT, "Your text", {})
result = mmai.process([text_input])

# Code
code_input = ModalInput(Modality.CODE, "def func():", {})
result = mmai.process([code_input])

# Cross-modal
synthesis = mmai.cross_modal_reasoning([text_input, code_input])
```

## 📈 Advanced Features

### Self-Consistency Check
```python
from agents.advanced_reasoning import AdvancedReasoner

reasoner = AdvancedReasoner()
conclusions = ["Solution A", "Solution A", "Solution B"]
consistency = reasoner.self_consistency_check(conclusions)
```

### Adversarial Validation
```python
validation = reasoner.adversarial_validation("This claim is valid")
print(validation['robustness_score'])
```

### Memory Consolidation
```python
# Automatic consolidation every 50 experiences
# Or trigger manually
ai._consolidate_memories()
```

## 🔍 Introspection

```python
# View reasoning history
for thought in ai.core_ai.reasoning_history[-5:]:
    print(f"Confidence: {thought.confidence:.2%}")
    print(f"Chain: {thought.reasoning_chain}")

# View memories
for memory in ai.core_ai.long_term_memory:
    print(f"Content: {memory.content}")
    print(f"Importance: {memory.importance}")
    print(f"Access count: {memory.access_count}")
```

## 🧪 Testing & Validation

```python
# Test reasoning quality
thought = ai.core_ai.think("Test problem")
assert thought.confidence > 0.5

# Test learning
initial_count = ai.core_ai.experience_count
ai.core_ai.learn("test", "outcome", 0.5)
assert ai.core_ai.experience_count == initial_count + 1

# Test planning
plan = ai.core_ai.plan("Test goal")
assert len(plan['steps']) > 0
```

## 💡 Best Practices

1. **Use specific contexts**: Provide detailed context for better reasoning
2. **Monitor confidence**: Check confidence scores before acting
3. **Learn continuously**: Call `learn()` after each significant event
4. **Optimize periodically**: Run `self_optimize()` every 100+ experiences
5. **Validate outputs**: Use self-consistency checks for critical decisions

## 🐛 Troubleshooting

### Memory not persisting
```python
# Check memory path
print(ai.core_ai.memory_path)

# Force save
ai.core_ai._save_memory()
```

### Low confidence scores
```python
# Increase reasoning depth
ai.core_ai.max_reasoning_depth = 15

# Add more context
result = ai.execute_task(task, context={"key": "value", ...})
```

### Slow performance
```python
# Consolidate memories
ai.core_ai._consolidate_memories()

# Reset if needed
ai.core_ai.reset(preserve_memories=True)
```

## 📚 Examples

See [docs/NEXUS_AI_MODEL.md](NEXUS_AI_MODEL.md) for comprehensive examples.

## ⚡ Signature

**LEGION x L.X VEX — SERVING ATLAS**
