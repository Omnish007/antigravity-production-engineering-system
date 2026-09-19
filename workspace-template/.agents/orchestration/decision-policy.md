# Decision Policy

## Purpose

Provide predictable boundaries for autonomous action versus research and human input.

## 1. Act

Act without asking when the answer is established by:

- an accepted ADR;
- project convention;
- explicit user requirement;
- existing configuration;
- installed-version official documentation;
- a reversible, low-risk implementation choice consistent with the above.

## 2. Infer and record

Infer when multiple signals converge strongly and the choice is low-risk or reversible. Record the assumption in the task evidence and, when durable, in project memory.

Do not invent business rules just because the technical implementation would be convenient.

## 3. Research first

Research when:

- documentation is version-sensitive;
- multiple supported technical approaches exist;
- compatibility is uncertain;
- performance/security consequences need evidence;
- the repository's existing behavior is unclear but inspectable.

Prefer official documentation and installed package docs. Record material findings in the task plan or relevant project doc.

## 4. Ask the user

Ask only when uncertainty is a genuine decision the repository cannot determine safely, such as:

- ambiguous business behavior;
- irreversible/high-impact architecture choice;
- production credential change;
- destructive data operation;
- external side effect that cannot be undone;
- public API breaking change;
- financial/legal/compliance decision;
- requirement that has multiple materially different interpretations.

## 5. Change accepted decisions safely

If current work conflicts with an accepted ADR:

- do not silently bypass the ADR;
- determine whether the user intends to change the decision;
- if yes, create a superseding ADR and update affected docs.
