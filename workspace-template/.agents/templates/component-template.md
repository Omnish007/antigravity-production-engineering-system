# UI Component Specification

## Name

## Purpose

What problem does this component solve? Why does it exist?

## Ownership / feature

Which feature or module owns this component?

## Composition

### Required children/parts

### Primitives used

List any UI library primitives (shadcn/ui, Radix, etc.) used as building blocks.

## Props / public API

| Prop | Type | Required | Default | Description |
|---|---|---|---|---|
| | | | | |

## State model

| State | Condition | Visual behavior | User interaction |
|---|---|---|---|
| idle | default | | |
| loading | async operation pending | skeleton or spinner | inputs disabled |
| success | operation completed | success feedback | normal interaction |
| error | operation failed | error message | retry available |
| empty | no data | empty state guidance | action prompt |
| disabled | interaction not allowed | muted appearance | no interaction |

## Responsive behavior

| Breakpoint | Layout changes |
|---|---|
| mobile (< 640px) | |
| tablet (640-1024px) | |
| desktop (> 1024px) | |

## Accessibility

- semantic element:
- ARIA role (if not implicit):
- accessible name:
- keyboard behavior:
- focus behavior:
- focus trap (if modal/dialog):
- error association (aria-describedby):
- live region (aria-live, if dynamic content):
- reduced-motion behavior:
- color contrast: meets WCAG AA (4.5:1 text, 3:1 large text)
- touch target: minimum 48x48 CSS pixels

## Interaction states

| State | Trigger | Visual feedback |
|---|---|---|
| hover | mouse enter | |
| active/pressed | mouse down / touch | |
| focus-visible | keyboard navigation | |
| selected | user selection | |
| dragging | drag start | |

## Data dependencies

- What data does this component need?
- Where does the data come from (props, server, client state)?
- What happens when data is unavailable?

## Performance considerations

- Does this component render lists? If so, is virtualization needed?
- Does it import heavy libraries? Can they be lazy-loaded?
- Are there unnecessary re-render risks?
- Should it use React.memo? (Only if profiling justifies it.)

## Error handling

- What errors can occur within this component?
- How are errors displayed to the user?
- Is an error boundary needed above or within this component?

## Tests

- Unit tests for logic and state transitions.
- Integration tests for data flow and composition.
- Accessibility tests (axe-core or equivalent).
- Visual regression tests (if configured).

## Screens / consumers

List the pages or parent components that use this component.

## Related conventions / ADRs

Link to relevant design decisions or conventions.
