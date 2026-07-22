# Design: Add Dark Mode

## Technical Approach

Store the selection client-side and mirror it to the profile service so
it survives sign-out.

## Architecture Decisions

### Decision: DisplayModeStore over per-page state

A single `DisplayModeStore` owns the current selection and notifies
subscribers when it changes.

### Decision: CSS custom properties over per-component styles

The `ThemeToggle` component implements the manual theme preference
toggle from the proposal; palette swaps happen entirely through CSS
custom properties, so components never branch on the selection.

## File Changes

- Create `src/stores/DisplayModeStore.ts`
- Create `src/components/ThemeToggle.tsx`
- Modify `src/styles/palette.css`
