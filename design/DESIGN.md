---
name: Kinetic Monochrome
colors:
  surface: '#f9f9ff'
  surface-dim: '#d3daea'
  surface-bright: '#f9f9ff'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#f0f3ff'
  surface-container: '#e7eefe'
  surface-container-high: '#e2e8f8'
  surface-container-highest: '#dce2f3'
  on-surface: '#151c27'
  on-surface-variant: '#4c4546'
  inverse-surface: '#2a313d'
  inverse-on-surface: '#ebf1ff'
  outline: '#7e7576'
  outline-variant: '#cfc4c5'
  surface-tint: '#5e5e5e'
  primary: '#000000'
  on-primary: '#ffffff'
  primary-container: '#1b1b1b'
  on-primary-container: '#848484'
  inverse-primary: '#c6c6c6'
  secondary: '#0054cb'
  on-secondary: '#ffffff'
  secondary-container: '#256df0'
  on-secondary-container: '#fefcff'
  tertiary: '#000000'
  on-tertiary: '#ffffff'
  tertiary-container: '#00210d'
  on-tertiary-container: '#00984f'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#e2e2e2'
  primary-fixed-dim: '#c6c6c6'
  on-primary-fixed: '#1b1b1b'
  on-primary-fixed-variant: '#474747'
  secondary-fixed: '#dae2ff'
  secondary-fixed-dim: '#b1c5ff'
  on-secondary-fixed: '#001947'
  on-secondary-fixed-variant: '#00419f'
  tertiary-fixed: '#66fe9c'
  tertiary-fixed-dim: '#44e183'
  on-tertiary-fixed: '#00210d'
  on-tertiary-fixed-variant: '#005228'
  background: '#f9f9ff'
  on-background: '#151c27'
  surface-variant: '#dce2f3'
typography:
  display:
    fontFamily: Inter
    fontSize: 48px
    fontWeight: '700'
    lineHeight: 56px
    letterSpacing: -0.03em
  headline-lg:
    fontFamily: Inter
    fontSize: 36px
    fontWeight: '700'
    lineHeight: 44px
    letterSpacing: -0.025em
  headline-lg-mobile:
    fontFamily: Inter
    fontSize: 28px
    fontWeight: '700'
    lineHeight: 34px
    letterSpacing: -0.02em
  headline-md:
    fontFamily: Inter
    fontSize: 28px
    fontWeight: '600'
    lineHeight: 36px
    letterSpacing: -0.02em
  headline-sm:
    fontFamily: Inter
    fontSize: 22px
    fontWeight: '600'
    lineHeight: 28px
    letterSpacing: -0.015em
  title-lg:
    fontFamily: Inter
    fontSize: 18px
    fontWeight: '600'
    lineHeight: 24px
    letterSpacing: -0.01em
  title-md:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: '600'
    lineHeight: 22px
    letterSpacing: -0.005em
  body-lg:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 24px
    letterSpacing: 0em
  body-md:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: '400'
    lineHeight: 20px
    letterSpacing: 0em
  body-sm:
    fontFamily: Inter
    fontSize: 12px
    fontWeight: '400'
    lineHeight: 16px
    letterSpacing: 0.01em
  label-lg:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: '600'
    lineHeight: 18px
    letterSpacing: 0.01em
  label-md:
    fontFamily: Inter
    fontSize: 12px
    fontWeight: '600'
    lineHeight: 16px
    letterSpacing: 0.02em
  label-sm:
    fontFamily: Inter
    fontSize: 10px
    fontWeight: '700'
    lineHeight: 12px
    letterSpacing: 0.05em
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  gutter: 1.5rem
  margin: 2rem
  space-xs: 0.25rem
  space-sm: 0.5rem
  space-md: 1rem
  space-lg: 1.5rem
  space-xl: 2rem
---

## Brand & Style

This design system delivers a high-precision, utilitarian aesthetic engineered for real-time dispatch, spatial logistics, and on-demand mobility on the web. It merges high-contrast monochrome minimalism with functional digital product design. 

### Brand Personality & Philosophy
- **Intentional Precision:** Every element exists to facilitate wayfinding, selection, or transaction. No purely ornamental visual clutter.
- **Architectural Clarity:** Layouts treat the screen as an interactive spatial dashboard—balancing real-time vector cartography with razor-sharp telemetry and modular floating interfaces.
- **Direct & Confident:** High-contrast text hierarchies, unyielding black/white foundations, and decisive micro-interactions build absolute user trust.

### Visual Style
- **Monochrome Foundation:** Stark black `#000000` paired with crisp `#FFFFFF` surfaces creates maximum legibility, punctuated only by purpose-driven utility accents.
- **Structural Elevation:** Depth is achieved through crisp 1px borders paired with tight ambient drop shadows, mimicking precision physical hardware interfaces.
- **Utilitarian Polish:** Restrained geometry (8px to 12px structural radii) ensures components feel robust, modern, and screen-efficient across rich desktop panels.

## Colors

The system uses an uncompromising high-contrast monochrome architecture where black and white carry 90% of the UI volume. Vibrant functional accents are strictly reserved for critical actions, live tracking status, and telemetry highlights.

### Core Tokens & Palette Architecture
- **Primary (`#000000`):** The definitive brand anchor. Used for primary interactive CTAs, high-emphasis headers, active map pins, and primary iconography.
- **Secondary / Action Blue (`#276EF1`):** Electric blue dedicated to dynamic pathways, active route polylines, links, driver location pings, and focal selection states.
- **Tertiary / Signal Green (`#06C167`):** Safety and success green used for ride confirmation, live vehicle availability, dynamic pricing drops, and positive statuses.
- **Destructive / Alert Red (`#E11900`):** Reserved for ride cancellations, emergency SOS triggers, and form error states.

### Neutral System (Light & Dark Tiers)
- **Base Canvas (`#FFFFFF`):** Default viewport background, map overlay panels, and card bases.
- **Subtle Surface (`#F6F7F9`):** Input field containers, inactive pill toggles, and table alternating strips.
- **Light Border (`#E5E7EB`):** Crisp 1px division for cards, panels, and modal headers.
- **Muted Text (`#5E6470`):** Secondary meta labels, helper text, timestamps, and distance estimations.
- **Dark Surface (`#0F1115`):** Reserved for dark-mode contexts, night-mode map styling, and high-emphasis floating ride monitor panels.
- **Dark Surface Container (`#1E2229`):** Elevated inner card states when in dark context mode.
- **Dark Border (`#2A2F3A`):** Separation lines on dark mode surfaces.

### Accessibility Rules
- Text-to-background contrast on primary headers and body copy strictly maintains a minimum contrast ratio of 12:1.
- Accents (`#276EF1` and `#06C167`) must never be used for low-weight body text; they are strictly limited to buttons, badges, thick route indicators, and icons.

## Typography

The design system relies entirely on **Inter** to channel an ultra-clean, geometric, architectural voice similar to bespoke transit typography. Tight tracking across display titles mimics high-end modern transport signage.

### Hierarchy & Style Rules
- **Display & Headlines:** Tightly tracked (`-0.03em` to `-0.015em`), strong weights (`600` and `700`). Reserved for product tier names (e.g., "Black", "UberX"), checkout final totals, and dashboard hero telemetry.
- **Numeric Optimization:** Use tabular lining figures (`font-variant-numeric: tabular-nums`) across all prices, arrival times, and coordinates to prevent UI jump during real-time dispatch updates.
- **Labels & Micro-Tags:** High-weight uppercase styling is used sparingly for vehicle class tags ("COMFORT", "XL", "PRIORITY") using `label-sm` with widened letter-spacing (`0.05em`) to balance small font sizes.

## Layout & Spacing

The web app is optimized for desktop interactions, prioritizing a split-view or multi-column canvas architecture: persistent contextual sidebars anchoring the booking flow or trip details on the left, alongside interactive full-bleed maps on the right.

### Layout Model
- **Split-View Canvas (Desktop >= 1024px):** A fixed-width or fluid-constrained side navigation drawer (420px to 480px width) fixed to the left or floating with a margin of `2rem` over an edge-to-edge interactive map view.
- **Dashboard Grid (Desktop):** 12-column layout with 24px gutters (`1.5rem`) and 32px outer margins (`2rem`), max-width constrained to 1440px for account, analytics, and booking history screens.
- **Mobile / Responsive Reflow (< 768px):** The left-side interactive drawer transitions to a bottom sheet overlaying the map with a swipe-up expansion mechanism. Side margins compress to `1rem`.

### Spacing Rationale
- Space is applied in strict multiples of 4px/8px.
- Use `space-xs` (4px) for tight icon-to-text relations and dot markers.
- Use `space-sm` (8px) for internal pill padding and stacked list titles.
- Use `space-md` (16px) for standard card padding and form input gaps.
- Use `space-lg` (24px) for card-to-card separations and modal interior spacing.
- Use `space-xl` (32px) for high-level section transitions and desktop panel headers.

## Elevation & Depth

Visual hierarchy uses a refined hybrid approach: low-contrast borders combined with ultra-subtle, ambient multi-layer drop shadows. Surfaces must appear cleanly lifted without looking heavy or skeuomorphic.

### Elevation Levels

- **Level 0 (Flat / Canvas):** Used for base surfaces and background areas.
  - Shadow: None.
  - Border: 1px solid `#E5E7EB` (or `#2A2F3A` in dark mode).

- **Level 1 (Subtle Lift / Cards & Pickers):** Standard state for ride option selection cards, address suggestion lists, and profile panels.
  - Shadow: `0 1px 3px 0 rgba(0, 0, 0, 0.04), 0 1px 2px 0 rgba(0, 0, 0, 0.02)`.
  - Border: 1px solid `#E5E7EB`.

- **Level 2 (Floating Panels / Navigation & Booking Drawer):** Used for floating booking controls and active vehicle tracking summaries positioned over the vector map.
  - Shadow: `0 10px 25px -5px rgba(0, 0, 0, 0.08), 0 8px 10px -6px rgba(0, 0, 0, 0.04)`.
  - Border: 1px solid rgba(0, 0, 0, 0.06).

- **Level 3 (Modals & Critical Overlays):** Used for driver detail profile takeovers, payment method switches, and cancel confirmations.
  - Shadow: `0 20px 35px -10px rgba(0, 0, 0, 0.16)`.
  - Backdrop: `#000000` with 40% opacity, paired with an 8px backdrop blur filter.

## Shapes

The design system adopts a balanced roundedness model (`level 2`) to balance architectural authority with tactile usability:
- **Base Components (Inputs, Buttons, Cards):** Standard radius of `8px` (`0.5rem`). This prevents UI components from appearing overly childish or toy-like, preserving a crisp, corporate aesthetic.
- **Containers & Side Drawers (`rounded-lg`):** Radius of `16px` (`1rem`) applied to floating side sheets, modal dialogs, and parent map-control panels.
- **Pills & Status Badges (`rounded-full`):** Complete 9999px pill radius strictly applied to categorical chips, live status indicators, vehicle counter tags, and avatar frames.

## Components

### Buttons
- **Primary:** Background `#000000`, text `#FFFFFF`, 0 border, 8px radius. Height 48px or 56px (full-width on booking sheets). Hover transitions background to `#222222`. Active state scales down to `0.985`.
- **Secondary:** Background `#F6F7F9`, text `#000000`, 0 border. Hover background to `#E5E7EB`.
- **Accent Action:** Background `#276EF1`, text `#FFFFFF`. Used strictly for "Request Ride", "Confirm Pickup", or dynamic re-routing actions.
- **Destructive:** Background `#FFF1F0`, text `#E11900`, 1px border `#FCDAD7`.

### Input Fields & Address Autocomplete
- **Structure:** 52px total container height with a light grey interior surface (`#F6F7F9`), 8px border radius, and a 1px border (`#E5E7EB`). 
- **Focus State:** Background transitions to `#FFFFFF`, border shifts to 2px solid `#000000`, zero drop shadow.
- **Wayfinding Elements:** Pickup inputs incorporate a tiny solid black square icon on the left; destination inputs incorporate a solid black circle connected by a 2px vertical dashed line.
- **Floating Labels / Clear Actions:** High-contrast `body-sm` helper labels positioned above the input, with an inline circular "✕" clear button appearing on user entry.

### Cards & Ride Selection Tiles
- **Default State:** White background, 12px border radius, 1px solid `#E5E7EB`, 16px internal padding. Left-aligned vehicle silhouette image, center-aligned title with occupant capacity, right-aligned bold tabular price and ETA.
- **Selected State:** 2px solid `#000000` outline with a subtle `#F6F7F9` background tint.
- **Surge / Savings Badge:** Tiny pill embedded inside the card top-right with background `#06C167` or `#000000` using text `#FFFFFF` at `10px` bold.

### Chips & Filter Pills
- **Style:** Compact 32px height, fully rounded pill format (`9999px`).
- **Unselected:** Background `#FFFFFF`, 1px solid `#E5E7EB`, text `#000000`.
- **Selected:** Background `#000000`, text `#FFFFFF`, border `#000000`.

### Lists & Activity Feed
- **Separators:** Hairline 1px solid `#E5E7EB` dividers inset by 16px.
- **Rows:** Minimum 64px height with interactive hover state transitioning to `#F9FAFB`. Left circular avatar or icon container (40px, `#F3F4F6`), dual-line vertical typography (Primary action / timestamp & vehicle detail), right chevron icon (`#9CA3AF`).

### Checkboxes & Radio Controls
- **Radios (Ride Choice / Payment):** 20px outer circle, 2px border `#000000`. Selected state features an 8px solid black center dot.
- **Checkboxes:** 20px square with 4px border radius. Checked state fills `#000000` with a crisp white check vector.

### Telemetry & Ride Status Banners
- **Live Tracking Island:** Floating panel anchored to top-center or bottom-left of the viewport. Features an animated pulsing indicator (`#06C167`), driver rating badge, vehicle license plate in high-contrast monospaced font on a simulated physical yellow or white badge outline, and vehicle model metadata.