# Component-Specific Checklists

This file is referenced by Plan-Review (for planning requirements) and Critic (for edge case attacks). It is a shared resource — not an agent file.

When planning or reviewing a component, load ONLY the relevant section. Do not read the entire file for a single component.

**Maintenance:** Plan-Review owns keeping this file current. When a plan reveals new edge cases or component interactions not captured here, include updates in the plan's `## Canonical Doc Updates` section.

---

<!-- ADD YOUR PROJECT'S CRITICAL COMPONENTS BELOW.

For each component, include:

## [Component Name]

### Planning requirements
- [What must the plan address for this component]

### Edge cases to attack
- [Specific scenarios that could break this component]
- [Boundary conditions and failure modes]

### Research prompts
- [What to search for when planning this component]

Example:

## PDF Export Pipeline

### Planning requirements
- Cover all supported input formats
- Handle large files gracefully
- Error recovery for partial failures

### Edge cases to attack
- Input with zero pages or empty content
- Concurrent export requests for the same resource
- Timeout during external service call

### Research prompts
- How do production systems handle PDF generation at scale?
- What are known pitfalls in async document processing?
-->

---

## Generic (any component not listed above)

This section covers all components that don't have a dedicated section above.

For these components, spend extra time on external research — you have no pre-built checklist to fall back on. Build an edge case list from first principles.

### Edge cases to always consider

- What happens when the input data is valid but empty?
- What happens when the input data is malformed but not invalid by schema?
- What happens at the boundary between two components?
- What happens under concurrent access?
- What happens when a dependency returns an unexpected result?
