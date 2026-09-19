---
name: uiux
description: Design and implement accessible, responsive, coherent interfaces using Tailwind CSS 4 and shadcn/ui without one-off visual drift.
---

# UI/UX Skill

## Design process

1. Inspect the existing design tokens and components.
2. Reuse shadcn/ui primitives where appropriate.
3. Establish layout hierarchy and content priority.
4. Define states before styling details.
5. Implement mobile-first responsive behavior.
6. Validate keyboard/focus/accessibility.
7. Review visual consistency at representative widths.

## Tailwind

- Prefer project tokens over arbitrary values.
- Keep utility composition readable.
- Use CSS variables/design tokens for themes and semantic colors.
- Avoid mixing multiple styling systems without a documented reason.

## shadcn/ui

Treat generated components as project-owned open code. Customize them deliberately, preserve accessibility behavior, and avoid forking the same primitive into multiple near-identical versions.

## Accessibility

Follow WCAG 2.2 engineering practices. Use semantic HTML before ARIA. Every interactive control needs an accessible name and keyboard operation. Manage focus for modal/popup interactions.

## Visual states

Every substantial component should consider loading, empty, error, disabled, hover/focus/active, and responsive states as appropriate.

## Motion

Animation should support hierarchy or feedback, not decoration for its own sake. Respect reduced-motion preferences and avoid animations that block task completion.
