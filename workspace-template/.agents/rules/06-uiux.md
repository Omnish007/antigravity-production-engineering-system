<!-- ID: RULE-UI-001 -->
# UI/UX Rules

<ROLE>
Operate as a Frontend and UI/UX Engineer delivering accessible, responsive, token-driven, and high-performance user interfaces.
</ROLE>

<MISSION>
Enforce WCAG 2.2 AA accessibility standards, responsive mobile-first layouts, explicit asynchronous view states, and centralized design tokens across all frontend interfaces.
</MISSION>

<NON_NEGOTIABLES>
- **UI-01 (Accessibility WCAG AA)**: All UI components must meet WCAG 2.2 AA contrast requirements (4.5:1 minimum for normal text, 3:1 for large text/controls) and provide visible focus indicators for keyboard navigation.
- **UI-02 (Explicit Async States)**: Every asynchronous view MUST explicitly handle loading, error, empty, and data states. Never display an unhandled white-screen or empty layout during data fetching.
</NON_NEGOTIABLES>

<DECISION_RULES>
### Design System & Tokens
- Centralize design tokens (colors, typography, spacing, radii, shadows) via CSS custom properties, design token files, or framework config; avoid raw visual magic numbers in components.
- Use established, accessible UI primitives (e.g. Radix, Headless UI, shadcn/ui) rather than rebuilding complex accessible controls from scratch.

### Responsive & Mobile-First
- Design mobile-first and verify intermediate states between breakpoints (<640px, 640-1024px, >1024px).
- Test with long content, empty states, and error envelopes.

### Forms & Interactions
- Validate inline as the user navigates between fields when feasible.
- Show validation errors adjacent to the relevant input, associated via `aria-describedby`.
- Disable submit buttons while requests are in flight to prevent duplicate submissions; re-enable on failure.

### Performance & Core Web Vitals
- Optimize for Core Web Vitals (LCP <= 2.5s, INP <= 200ms, CLS <= 0.1).
- Set explicit width/height or aspect ratios on images to eliminate layout shifts.
- Lazy-load below-the-fold assets and components.
</DECISION_RULES>

<VERIFICATION_POLICY>
UI modifications must be verified across:
1. Keyboard navigation (Tab, Shift+Tab, Enter, Escape, Space).
2. Automated accessibility scanning with zero critical violations (axe-core or equivalent).
3. Responsive viewport checks (mobile, tablet, desktop).
4. Explicit loading, error, and empty state rendering.
</VERIFICATION_POLICY>

<ANTI_PATTERNS>
- Conveying meaning through color alone without text or iconography.
- Missing visible focus rings on interactive elements.
- Showing a blank screen or unstyled raw text during API fetch operations.
- Hardcoding hex color codes or pixel margins directly in component styles.
</ANTI_PATTERNS>
