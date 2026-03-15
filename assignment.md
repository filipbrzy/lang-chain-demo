# LangGraph Multi-Agent System Assignment: Research Paper Analysis & Publication Pipeline

## Overview
Build a sophisticated multi-agent system using LangGraph that processes research papers through a non-linear workflow with conditional routing, parallel execution, human-in-the-loop decisions, and state persistence.

## Scenario
Create an automated research paper analysis pipeline that:
1. Accepts a research paper (title, abstract, content)
2. Routes it through multiple specialized agents
3. Makes intelligent routing decisions based on content and quality
4. Produces a comprehensive analysis report and publication recommendation

## Required Agents

### 1. **Coordinator Agent**
- **Role**: Entry point, initial classification
- **Tasks**: 
  - Classify paper domain (CS, Biology, Physics, Math, etc.)
  - Assess paper complexity (Basic, Intermediate, Advanced)
  - Route to appropriate specialist agents
  
### 2. **Content Analyzer Agent**
- **Role**: Deep content analysis
- **Tasks**:
  - Extract key findings and methodologies
  - Identify novelty score (1-10)
  - Extract citations and references count
  - Generate summary

### 3. **Quality Assessor Agent**
- **Role**: Quality evaluation
- **Tasks**:
  - Evaluate methodology rigor (1-10)
  - Check for logical consistency
  - Assess reproducibility
  - Generate quality score

### 4. **Plagiarism Checker Agent**
- **Role**: Originality verification
- **Tasks**:
  - Simulate plagiarism check (mock implementation)
  - Check for self-plagiarism indicators
  - Return originality percentage
  - Flag concerns if originality < 85%

### 5. **Statistical Validator Agent**
- **Role**: Validates statistical claims (for papers with data)
- **Tasks**:
  - Identify statistical methods mentioned
  - Validate if appropriate tests are used
  - Check for p-hacking indicators
  - Only activated for empirical papers

### 6. **Ethics Reviewer Agent**
- **Role**: Ethical considerations review
- **Tasks**:
  - Check for ethical concerns
  - Verify consent and privacy mentions
  - Flag high-risk research
  - Only activated for human/animal subject papers

### 7. **Revision Suggester Agent**
- **Role**: Improvement recommendations (activated on conditional failure)
- **Tasks**:
  - Generate specific improvement suggestions
  - Prioritize critical issues
  - Create revision checklist

### 8. **Publication Recommender Agent**
- **Role**: Final decision maker
- **Tasks**:
  - Aggregate all agent outputs
  - Recommend: Accept / Minor Revisions / Major Revisions / Reject
  - Suggest target journals/conferences
  - Generate final report

## System Architecture Requirements

### LangGraph-Specific Features to Implement

#### 1. **StateGraph with Complex State**
```python
class PaperState(TypedDict):
    # Input
    paper_title: str
    paper_abstract: str
    paper_content: str
    
    # Metadata
    domain: str
    complexity: str
    has_statistical_analysis: bool
    has_human_subjects: bool
    
    # Agent Results
    content_analysis: dict
    quality_score: float
    novelty_score: float
    originality_percentage: float
    statistical_validation: Optional[dict]
    ethics_review: Optional[dict]
    
    # Decision Tracking
    requires_revision: bool
    revision_suggestions: Optional[list]
    plagiarism_flags: list
    
    # Final Output
    final_decision: str
    recommended_venues: list
    final_report: str
    
    # Workflow Metadata
    agents_visited: list
    iteration_count: int
```

#### 2. **Conditional Edges** (Multiple Decision Points)
- **After Coordinator**: Route to parallel analysis OR reject immediately if spam
- **After Plagiarism Check**: 
  - If originality < 85% → Route to Revision Suggester → END
  - Else → Continue to Quality Assessor
- **After Quality Assessor**:
  - If quality_score < 4 → Route to Revision Suggester → END
  - Else → Continue based on paper type
- **Domain-Specific Routing**:
  - If has_statistical_analysis → Include Statistical Validator
  - If has_human_subjects → Include Ethics Reviewer
- **After All Reviews**:
  - If any critical flags → Route to Revision Suggester
  - Else → Route to Publication Recommender

#### 3. **Parallel Execution Nodes**
Create a parallel node that runs simultaneously:
- Content Analyzer
- Plagiarism Checker
- Initial Quality Assessment

Use LangGraph's `Send` API or parallel branches pattern.

#### 4. **Human-in-the-Loop Integration**
Add human intervention points:
- **After Plagiarism Concerns**: Human reviews flagged issues
- **Before Final Decision**: Human can override recommendation
- Use `interrupt_before` or `interrupt_after` on specific nodes

#### 5. **Sub-graphs**
Create a sub-graph for the revision workflow:
- Revision Suggester → Human Review → Accept Changes / Request Re-analysis
- This sub-graph can loop back to main graph if re-submission requested

#### 6. **Checkpointing & Persistence**
- Implement MemorySaver or custom checkpointer
- Enable pause/resume of analysis
- Store intermediate states for audit trail

#### 7. **Dynamic Branching**
Implement a routing function that dynamically determines path based on:
- Paper domain
- Quality thresholds
- Flag accumulation

#### 8. **Cycles and Loops**
- Allow up to 2 re-review cycles if paper is revised
- Track `iteration_count` in state
- Prevent infinite loops with max_iterations check

#### 9. **Tool Integration**
Each agent should use tools:
- Web search tool (for reference checking)
- Calculator tool (for statistical validation)
- Mock database tool (for plagiarism checking)

## Workflow Diagram (Non-Linear)

```
START
  ↓
[Coordinator Agent] ← human_input (paper details)
  ↓
  ├→ (if spam/invalid) → END
  │
  ├→ [PARALLEL EXECUTION]
  │   ├→ [Content Analyzer]
  │   ├→ [Plagiarism Checker]
  │   └→ [Quality Assessor (Preliminary)]
  │   
  ↓ (wait for all parallel)
  │
[Plagiarism Gate]
  ↓
  ├→ (if originality < 85%) → [Revision Suggester] → [Human Review] → END
  │
  ↓ (else)
[Quality Gate]
  ↓
  ├→ (if quality < 4) → [Revision Suggester] → [Human Review] → END
  │
  ↓ (else)
[Domain-Specific Routing]
  ↓
  ├→ (if statistical) → [Statistical Validator] ─┐
  ├→ (if ethical)     → [Ethics Reviewer] ──────┤
  └→ (basic paper)    → (skip) ─────────────────┤
                                                  ↓
                                        [Aggregation Node]
                                                  ↓
                                        [Critical Flags Check]
                                                  ↓
                                        ├→ (has critical flags)
                                        │   → [Revision Suggester]
                                        │      → [Human Review]
                                        │         ├→ (accept suggestions) → END
                                        │         └→ (request reanalysis) → LOOP BACK (max 2 times)
                                        │
                                        └→ (no critical flags)
                                            → [Publication Recommender]
                                            → [Human Final Approval] (interrupt)
                                            → END
```

## Detailed Implementation Requirements

### Phase 1: Setup & Basic Graph (30%)
- [ ] Install dependencies: `langgraph`, `langchain`, `langchain-openai`
- [ ] Define `PaperState` TypedDict with all required fields
- [ ] Create empty agent functions (stubs) for all 8 agents
- [ ] Initialize StateGraph with PaperState
- [ ] Add all nodes to graph
- [ ] Implement basic START → Coordinator → END flow
- [ ] Test with simple print statements

### Phase 2: Implement Agents (25%)
- [ ] Implement Coordinator Agent with LLM
  - Domain classification
  - Complexity assessment
  - Output structured data
- [ ] Implement Content Analyzer Agent
  - Use LLM to extract findings
  - Generate novelty score
  - Create summary
- [ ] Implement Quality Assessor Agent
  - Evaluate methodology
  - Generate quality score
- [ ] Implement Plagiarism Checker (mock)
  - Simulate API call
  - Return random but realistic score
- [ ] Implement Statistical Validator
  - Parse for statistical keywords
  - Validate appropriateness
- [ ] Implement Ethics Reviewer
  - Scan for ethical keywords
  - Flag concerns
- [ ] Implement Revision Suggester
  - Aggregate issues
  - Generate actionable suggestions
- [ ] Implement Publication Recommender
  - Make final decision
  - Recommend venues
  - Generate comprehensive report

### Phase 3: Conditional Routing (20%)
- [ ] Implement spam detection conditional from Coordinator
- [ ] Implement plagiarism gate routing function
- [ ] Implement quality gate routing function
- [ ] Implement domain-specific routing logic
  - Determine if paper needs Statistical Validator
  - Determine if paper needs Ethics Reviewer
- [ ] Implement critical flags check routing
- [ ] Test all routing paths with different inputs

### Phase 4: Parallel Execution (10%)
- [ ] Implement parallel node for:
  - Content Analyzer
  - Plagiarism Checker  
  - Quality Assessor
- [ ] Use `Send` API or configure branches correctly
- [ ] Implement aggregation node to collect results
- [ ] Verify parallel execution with timing tests

### Phase 5: Advanced Features (15%)
- [ ] **Human-in-the-Loop**:
  - Add interrupt after plagiarism concerns
  - Add interrupt before final decision
  - Implement resume functionality
- [ ] **Checkpointing**:
  - Configure MemorySaver
  - Test save/resume workflow
  - Store checkpoint to SQLite or in-memory
- [ ] **Cycles/Loops**:
  - Implement loop from human review back to coordinator
  - Track iteration_count
  - Enforce max_iterations = 2
  - Add exit condition
- [ ] **Sub-graph** (Bonus):
  - Create revision sub-graph
  - Integrate with main graph

### Phase 6: Testing & Validation (10%)
- [ ] Create test cases:
  - High-quality paper (should accept)
  - Low-quality paper (should suggest major revisions)
  - Plagiarized paper (should reject)
  - Statistical paper (should activate validator)
  - Ethical concerns paper (should activate ethics reviewer)
  - Borderline paper requiring human input
- [ ] Test checkpoint persistence
- [ ] Test loop/cycle with resubmission
- [ ] Test parallel execution efficiency
- [ ] Validate all conditional paths are reachable
- [ ] Create visualization of graph using `draw_ascii()` or `draw_png()`

## Deliverables

### Code Files
1. **`multiagent_pipeline.py`** - Main implementation
2. **`agents.py`** - Individual agent implementations
3. **`state.py`** - State definition and helpers
4. **`tools.py`** - Tool definitions for agents
5. **`config.py`** - Configuration and constants
6. **`test_pipeline.py`** - Test cases

### Documentation
1. **`ARCHITECTURE.md`** - System design explanation
2. **Graph visualization** - PNG or ASCII diagram of the workflow
3. **Example outputs** - At least 3 different scenarios
4. **`REPORT.md`** - Reflection on langgraph features used

## Evaluation Criteria

### Correctness (30%)
- All agents implemented and functional
- Routing logic works correctly
- State management is bug-free
- Produces expected outputs

### LangGraph Feature Usage (35%)
- ✅ StateGraph properly configured
- ✅ Conditional edges implemented (multiple decision points)
- ✅ Parallel execution working
- ✅ Human-in-the-loop integrated
- ✅ Checkpointing/persistence functional
- ✅ Cycles/loops with termination conditions
- ✅ Dynamic routing based on state
- ✅ (Bonus) Sub-graphs implemented

### Code Quality (20%)
- Clean, readable code
- Proper type hints
- Good separation of concerns
- Error handling
- Comments where needed

### Complexity & Creativity (15%)
- Non-trivial workflow
- Realistic scenario
- Good use of LLM capabilities
- Innovative routing logic
- Bonus features

## Bonus Challenges

### 🌟 Advanced Features (Optional)
1. **Map-Reduce Pattern**: If paper is very long, chunk it and analyze chunks in parallel, then reduce
2. **Streaming**: Stream agent outputs in real-time
3. **Custom Checkpointer**: Implement custom checkpoint storage (e.g., PostgreSQL)
4. **Multiple Sub-graphs**: Create domain-specific sub-graphs (e.g., CS papers have code review sub-graph)
5. **Time-based Routing**: Add timeout handling for slow agents
6. **Confidence Scores**: Track confidence in decisions and route to human when low
7. **Multi-Hop Tool Use**: Agents use tools that call other tools
8. **Dynamic Agent Creation**: Based on domain, dynamically add specialized agents

## Tips for Success

1. **Start Simple**: Get basic linear flow working first
2. **Test Incrementally**: Add one feature at a time
3. **Use Mocks**: Don't need real LLM calls for every test - use mocks
4. **Visualize Often**: Generate graph diagrams frequently to verify structure
5. **Read Docs**: LangGraph docs have excellent examples
6. **Debug State**: Print state at each node during development
7. **Handle Errors**: Add try-catch blocks, especially around LLM calls
8. **Think About Edge Cases**: What if all parallel agents fail? What if human never responds?

## Resources

- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- LangGraph Examples: Multi-agent collaboration, human-in-the-loop, checkpointing
- [LangChain Tools](https://python.langchain.com/docs/modules/agents/tools/)
- State management patterns in LangGraph

## Example Test Input

```python
test_paper = {
    "paper_title": "Novel Approach to Deep Learning Optimization Using Quantum Annealing",
    "paper_abstract": "This paper presents a groundbreaking method for optimizing neural network training using quantum annealing techniques. We demonstrate 40% faster convergence on benchmark datasets...",
    "paper_content": "Introduction: Deep learning has revolutionized... [full content]"
}

# Run pipeline
result = app.invoke(test_paper)
print(result["final_report"])
```

## Expected Output Structure

```json
{
  "final_decision": "Accept with Minor Revisions",
  "recommended_venues": ["NeurIPS", "ICML", "Nature Machine Intelligence"],
  "overall_scores": {
    "novelty": 8.5,
    "quality": 7.8,
    "originality": 92.3,
    "statistical_rigor": 8.0
  },
  "summary": "The paper presents an innovative approach...",
  "required_revisions": [
    "Expand experimental validation section",
    "Add comparison with recent 2025 work on quantum ML"
  ],
  "agents_consulted": [
    "coordinator", "content_analyzer", "plagiarism_checker",
    "quality_assessor", "statistical_validator", "publication_recommender"
  ],
  "workflow_iterations": 1
}
```

---

## Getting Started

1. Create a new branch: `git checkout -b langgraph-assignment`
2. Create directory: `mkdir -p src/multiagent`
3. Start with Phase 1
4. Commit frequently
5. Test each phase before moving to next
6. Have fun! 🚀

**Estimated Time**: 8-12 hours for full implementation with all features

Good luck building your multi-agent system! Remember: the goal is to exercise LangGraph's unique capabilities, so embrace the complexity and non-linearity! 🎯
