---
name: Pulse Insight Engine
colors:
  surface: '#0b1326'
  surface-dim: '#0b1326'
  surface-bright: '#31394d'
  surface-container-lowest: '#060e20'
  surface-container-low: '#131b2e'
  surface-container: '#171f33'
  surface-container-high: '#222a3d'
  surface-container-highest: '#2d3449'
  on-surface: '#dae2fd'
  on-surface-variant: '#b9cacb'
  inverse-surface: '#dae2fd'
  inverse-on-surface: '#283044'
  outline: '#849495'
  outline-variant: '#3b494b'
  surface-tint: '#00dbe9'
  primary: '#dbfcff'
  on-primary: '#00363a'
  primary-container: '#00f0ff'
  on-primary-container: '#006970'
  inverse-primary: '#006970'
  secondary: '#d0bcff'
  on-secondary: '#3c0091'
  secondary-container: '#571bc1'
  on-secondary-container: '#c4abff'
  tertiary: '#d8ffe7'
  on-tertiary: '#003824'
  tertiary-container: '#65f2b5'
  on-tertiary-container: '#006d4a'
  error: '#ffb4ab'
  on-error: '#690005'
  error-container: '#93000a'
  on-error-container: '#ffdad6'
  primary-fixed: '#7df4ff'
  primary-fixed-dim: '#00dbe9'
  on-primary-fixed: '#002022'
  on-primary-fixed-variant: '#004f54'
  secondary-fixed: '#e9ddff'
  secondary-fixed-dim: '#d0bcff'
  on-secondary-fixed: '#23005c'
  on-secondary-fixed-variant: '#5516be'
  tertiary-fixed: '#6ffbbe'
  tertiary-fixed-dim: '#4edea3'
  on-tertiary-fixed: '#002113'
  on-tertiary-fixed-variant: '#005236'
  background: '#0b1326'
  on-background: '#dae2fd'
  surface-variant: '#2d3449'
typography:
  display-lg:
    fontFamily: Sora
    fontSize: 48px
    fontWeight: '700'
    lineHeight: 56px
    letterSpacing: -0.02em
  headline-lg:
    fontFamily: Sora
    fontSize: 32px
    fontWeight: '600'
    lineHeight: 40px
    letterSpacing: -0.01em
  headline-lg-mobile:
    fontFamily: Sora
    fontSize: 24px
    fontWeight: '600'
    lineHeight: 32px
  body-md:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 24px
  label-sm:
    fontFamily: JetBrains Mono
    fontSize: 12px
    fontWeight: '500'
    lineHeight: 16px
    letterSpacing: 0.05em
rounded:
  sm: 0.125rem
  DEFAULT: 0.25rem
  md: 0.375rem
  lg: 0.5rem
  xl: 0.75rem
  full: 9999px
spacing:
  base: 4px
  xs: 8px
  sm: 16px
  md: 24px
  lg: 40px
  xl: 64px
  gutter: 20px
  margin-mobile: 16px
  margin-desktop: 32px
---

## Brand & Style

The design system is engineered for high-velocity data analysis and automated decision-making. It embodies a **Futuristic Glassmorphic** aesthetic, blending the precision of aerospace instrumentation with the accessibility of modern SaaS. The personality is analytical, authoritative, and fast-moving.

The interface prioritizes a sense of "living data" through light-emitting elements and semi-transparent layers. It avoids heavy, solid blocks in favor of depth, refraction, and subtle luminosity. The emotional response should be one of being at the helm of a sophisticated, high-tech command center.

## Colors

The palette is built on a "Midnight Base" to maximize the impact of neon accents. 

- **Primary (Electric Cyan):** Used for critical actions, active states, and primary data threads. It should carry a subtle CSS `drop-shadow` or `box-shadow` glow effect (blur: 10px, opacity: 0.3) to simulate light emission.
- **Secondary (Electric Violet):** Used for automated insights, AI-driven features, and secondary interactive elements.
- **Surface (Deep Charcoal/Midnight):** The foundation of the UI. Backgrounds use a gradient from `#0F172A` to `#020617` to create environmental depth.
- **Status Colors:** Success is rendered in vivid Emerald, Warning in Safety Orange, and Error in Neon Crimson. All status colors must maintain high saturation to contrast against the dark base.

## Typography

This design system utilizes a three-font hierarchy to balance character and readability:
1. **Sora (Headlines):** A geometric sans-serif with a futuristic edge. Used for large displays and section headers to establish the brand's high-tech voice.
2. **Inter (Body):** The workhorse for data density. Its neutral, systematic nature ensures that complex analytical text remains legible.
3. **JetBrains Mono (Data/Labels):** Used for timestamps, coordinates, numerical data, and small labels. The monospaced nature emphasizes the "Engine" aspect of the brand, suggesting precision and code-like accuracy.

## Layout & Spacing

The layout follows a **Fluid Grid** model with a heavy emphasis on information density. 

- **Desktop:** A 12-column grid with 20px gutters. Content is housed in "Modules" (cards) that snap to the grid.
- **Mobile:** A 4-column grid with 16px side margins. Large data tables reflow into "Insight Cards."
- **Rhythm:** An 8px linear scale handles the majority of spacing, but a 4px "micro-step" is permitted for tight data clusters and utility bars. 

The layout should feel like a dashboard at all times, with sticky sidebars for navigation and a persistent "Global Pulse" bar at the top for real-time system alerts.

## Elevation & Depth

Depth is achieved through **Glassmorphism** and layering rather than traditional shadows.

1. **Surface Tiers:**
   - **Level 0 (Background):** Deepest navy, matte.
   - **Level 1 (Modules):** Semi-transparent (10-15% white overlay) with a 20px `backdrop-filter: blur()`.
   - **Level 2 (Popovers/Modals):** Higher transparency (25%) with a more intense blur (40px) and a thin 1px border (20% white).

2. **Borders:** Instead of shadows, use 1px "inner glows" or borders. Active elements feature a primary-colored stroke with a `0 0 8px` outer glow.
3. **Interaction:** Hovering over a module should increase the backdrop blur and slightly brighten the border-opacity, creating a "lifting" effect from the background.

## Shapes

The shape language is **Soft (Radius: 4px - 12px)**. 

- Small components (buttons, inputs) use a 4px radius to maintain a professional, sharp-edged look.
- Container modules use a 12px radius (`rounded-xl`) to soften the overall technical feel and create a more approachable interface.
- Avoid fully circular "pill" shapes unless used for status indicators or notification badges.

## Components

- **Buttons:** Primary buttons are solid Electric Cyan with black text for maximum contrast. Secondary buttons are "Ghost" style with an Electric Violet border and no fill, becoming semi-transparent violet on hover.
- **Glass Cards:** All containers must feature a `backdrop-filter: blur(12px)` and a subtle linear gradient border (top-left to bottom-right: white at 10% to white at 2%).
- **Inputs:** Darker than the background surface with a 1px bottom-border only in the inactive state. Upon focus, the border expands to a full Cyan frame with a subtle outer glow.
- **Data Visualization:** Charts should use "Neon Glow" lines. Area charts use a vertical gradient from the accent color (Cyan/Violet) to 0% opacity.
- **Chips/Tags:** Monospaced text (JetBrains Mono) inside small, low-opacity colored boxes. Tags for "AI Automated" or "Predictive" should use the Electric Violet accent.
- **System Indicators:** Use small pulsating dot animations for "Live" data streams to reinforce the "Pulse" brand narrative.