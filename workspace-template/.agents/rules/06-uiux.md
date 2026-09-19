# UI/UX Rules

Recommended activation: **Glob** for `**/*.{tsx,jsx,css}` and UI-related work.

## Design system

- Use shadcn/ui primitives where they match the interaction rather than rebuilding accessible primitives from scratch.
- Treat shadcn components as project-owned open code that may be customized deliberately.
- Centralize design tokens through Tailwind/CSS variables rather than scattering raw visual values.
- Avoid arbitrary one-off visual decisions when a reusable token or component is appropriate.

## Responsive behavior

Design mobile-first and test the meaningful states between named breakpoints. Do not assume that desktop layouts merely shrink successfully.

Check:

- narrow mobile;
- large mobile/small tablet;
- tablet/laptop;
- wide desktop;
- long content;
- empty/loading/error states.

## Accessibility

Target WCAG 2.2 AA-level engineering practices unless a project explicitly requires another standard.

Required habits:

- semantic HTML before ARIA;
- keyboard operability;
- visible focus indicators;
- sensible focus movement for dialogs/menus;
- accessible names for controls;
- sufficient contrast;
- error messages associated with inputs;
- reduced-motion support for non-essential animation;
- touch targets that are practical on small screens;
- no information conveyed by color alone.

## UX states

Interactive features should consider:

- loading;
- success;
- validation failure;
- server failure;
- empty state;
- disabled state;
- optimistic state where used;
- permission-denied state;
- stale data state where relevant.

## Form UX

- Validate inline as the user moves between fields when practical.
- Show validation errors near the relevant field, not only at the form top.
- Preserve form state when navigation is accidental (unsaved changes warning).
- Disable submit while a submission is in flight; re-enable on failure.
- Show clear success feedback after submission.

## Theming and dark mode

When the project supports theming:

- use CSS custom properties or Tailwind's dark mode utilities;
- ensure all colors, borders, and shadows adapt correctly;
- test both modes at every breakpoint;
- do not rely solely on inverting colors; verify contrast in both modes.

## Internationalization awareness

Even for English-only projects:

- avoid hardcoded strings in components; use a structured approach (constants, i18n keys);
- do not assume text direction (LTR); use logical properties (`start`/`end`) where supported;
- account for text expansion (translations can be 30-100% longer than English);
- use date/number formatting that respects locale when relevant.

## Performance

Avoid unnecessary client-side JavaScript. Prefer Server Components for non-interactive UI in Next.js, lazy-load genuinely expensive client functionality, avoid oversized images, and prevent layout shifts.

Use field data where available. For Core Web Vitals, treat LCP <= 2.5s, INP <= 200ms, and CLS <= 0.1 at the 75th percentile as useful targets rather than universal guarantees.

## Content

UI copy should be clear, specific, and actionable. Error messages should tell the user what happened and what they can do next without exposing internal diagnostics.

## Testing

UI changes should be verified with:

- visual inspection at responsive breakpoints;
- keyboard-only navigation;
- automated accessibility scan (axe-core or equivalent);
- component unit tests for interactive behavior;
- E2E tests for critical user journeys when configured.
