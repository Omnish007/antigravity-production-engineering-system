---
name: uiux
id: SKILL-UIUX-001
description: Design and implement accessible, responsive, coherent interfaces using established design tokens, reusable component primitives, and WCAG 2.2 AA standards without visual drift.
---

# UI/UX Skill

<MISSION>
Design and implement accessible, responsive, coherent interfaces using established design tokens, reusable component primitives, and WCAG 2.2 AA standards without visual drift.
</MISSION>

<WHEN_TO_USE>
Activate this skill when executing tasks requiring uiux capabilities, workflows, or architectural guidance.
</WHEN_TO_USE>

<PRECONDITIONS>
### Prerequisites
- The current governed task record `.agents/state/tasks/TASK-ID.json` must be `IN_PROGRESS`.
    - A `TASK_STARTED` event must be recorded in `.agents/state/events/TASK-ID.jsonl`.
    - Must be loaded as part of the Atomic Frontend Bundle alongside `.agents/skills/frontend/SKILL.md` and `.agents/rules/06-uiux.md`.

### Pre-flight Checklist
- [ ] Contrast ratios verified
    - [ ] Keyboard navigation tested
    - [ ] Responsive layout tested on mobile/desktop
    - [ ] Loading and error states designed
</PRECONDITIONS>

<NON_NEGOTIABLES>
- Meet WCAG 2.1 AA contrast requirements (minimum 4.5:1 for normal text).
    - All interactive elements must be fully keyboard accessible with visible focus rings.
    - Ensure zero layout shifts (CLS < 0.1) and responsive design across all devices.
</NON_NEGOTIABLES>

<PROCEDURE>
## Design process

1. **Inspect tokens & components**: Review the project's existing design tokens, typography, color palette, and reusable component library before introducing new UI elements.
2. **Reuse established primitives**: Utilize existing accessible primitives (shadcn/ui, Radix, Material, Headless UI, etc.) rather than hand-crafting complex interactive components.
3. **Establish hierarchy**: Prioritize content flow, headings (`h1`-`h6`), and call-to-action prominence.
4. **Define states first**: Model `idle`, `loading`, `empty`, `error`, `disabled`, and `optimistic` states before polishing visual details.
5. **Mobile-first responsive design**: Implement layouts starting at narrow mobile viewports (<640px) and scale gracefully through tablet and desktop breakpoints.
6. **Accessibility validation**: Verify keyboard navigation, focus indicators, color contrast, and screen-reader semantics.
7. **Cross-viewport visual review**: Check UI rendering across standard breakpoints to ensure cohesive typography, spacing, and alignment.

## Design tokens and systems

- **Centralized tokens**: Define visual values (colors, spacing, font sizes, line heights, border radii, shadows) in centralized token definitions (e.g., CSS custom properties, Tailwind config, design token files).
- **Semantic colors**: Use semantic role names (e.g., `primary`, `destructive`, `muted`, `background`, `surface`, `border`) rather than hardcoded hex or RGB values.
- **Consistency**: Never introduce one-off, arbitrary pixel values when a standard design system token exists.

## Component primitives and customization

- Treat third-party or generated component primitives as project-owned source code.
- Customize primitives deliberately to match project requirements while preserving underlying accessibility and keyboard behavior.
- Avoid forking near-identical variants of the same component; extend base components with props or variants (e.g., `cva` or variant classes).

## Accessibility (WCAG 2.2 AA)

- **Semantic elements**: Use native HTML elements (`<button>`, `<input>`, `<dialog>`, `<nav>`, `<aside>`) before ARIA attributes.
- **Keyboard navigation**: Ensure all interactive elements are reachable via `Tab` and operable via `Enter` or `Space`.
- **Visible focus indicators**: Maintain prominent, high-contrast focus rings (`outline` or `ring`) on all focusable elements. Never set `outline: none` without a high-contrast replacement.
- **Focus management**: Trap focus within open modal dialogs and drawers; return focus to the trigger element upon closing.
- **Contrast ratios**: Verify contrast meets WCAG AA thresholds: minimum 4.5:1 for normal text, 3:1 for large text (>18pt / 24px) and essential UI controls/borders.
- **Touch targets**: Provide touch targets of at least 48x48 CSS pixels for touch-screen usability.

## Motion and micro-interactions

- Use animation to provide user feedback, orient navigation, or show state changes—never for gratuitous decoration.
- Always respect user accessibility preferences by supporting `@media (prefers-reduced-motion: reduce)` to disable or minimize motion.
- Avoid animations that block user input or task completion.
</PROCEDURE>

<VERIFICATION_POLICY>
## Verification

Verify UI/UX changes with:
- Visual inspection across mobile (375px), tablet (768px), and desktop (1280px+) widths;
- Keyboard-only navigation testing (Tab, Shift+Tab, Enter, Space, Escape, Arrow keys);
- Automated accessibility scans (axe-core, Lighthouse, or Pa11y);
- Color contrast verification in both light and dark modes;
- Screen-reader verification (NVDA, VoiceOver, or automated accessibility tree inspection).

### Exit Criteria
UI components pass accessibility checks and visual inspection.
</VERIFICATION_POLICY>

<DELIVERABLES>
- Polished UI components, design tokens, responsive layouts, accessibility audit results, and state handling.
</DELIVERABLES>
