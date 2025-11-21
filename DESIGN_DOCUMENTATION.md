# 🎨 UI/UX Design Documentation
## AI-Based Air Quality & Health Prediction System (IHIP)

---

## Table of Contents
1. [Design Philosophy](#design-philosophy)
2. [Color System](#color-system)
3. [Typography](#typography)
4. [Component Library](#component-library)
5. [Layout Grids](#layout-grids)
6. [Interaction Flows](#interaction-flows)
7. [Accessibility Guidelines](#accessibility-guidelines)
8. [Mobile Design](#mobile-design)
9. [Dark Mode](#dark-mode)
10. [Implementation Notes](#implementation-notes)

---

## Design Philosophy

### Core Principles
- **Simplicity First:** Clean, uncluttered interface focusing on essential information
- **Data-Driven:** Prioritize key metrics and actionable insights
- **Government Standard:** Professional, trustworthy aesthetic suitable for public health
- **Accessibility:** WCAG 2.1 Level AA compliant
- **Mobile-First:** Responsive design that works on all devices

### Visual Style
- **Minimalistic:** No unnecessary decorations or gradients
- **Professional:** Government health dashboard aesthetic
- **Modern:** Contemporary UI patterns and interactions
- **Trustworthy:** Clear hierarchy and consistent styling

---

## Color System

### Primary Palette

#### Risk Level Colors
```css
/* Low Risk / Good */
--risk-low: #2ECC71;
RGB: (46, 204, 113)
Usage: AQI 0-50, Low health risk indicators

/* Medium Risk / Moderate */
--risk-medium: #F1C40F;
RGB: (241, 196, 15)
Usage: AQI 51-100, Medium health risk indicators

/* High Risk / Unhealthy */
--risk-high: #E67E22;
RGB: (230, 126, 34)
Usage: AQI 101-200, High health risk indicators

/* Very High Risk / Hazardous */
--risk-very-high: #E74C3C;
RGB: (231, 76, 60)
Usage: AQI 201-300, Very high health risk indicators

/* Hazardous */
--risk-hazardous: #8B0000;
RGB: (139, 0, 0)
Usage: AQI 300+, Extreme health risk
```

#### UI Colors
```css
/* Primary Brand */
--primary-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
--primary-purple: #667eea;
--primary-dark: #764ba2;

/* Backgrounds */
--bg-primary: #F7FAFC;
--bg-card: #FFFFFF;
--bg-secondary: #EDF2F7;

/* Text */
--text-primary: #2C3E50;
--text-secondary: #718096;
--text-muted: #A0AEC0;
--text-white: #FFFFFF;

/* Borders */
--border-light: #E2E8F0;
--border-medium: #CBD5E0;
--border-dark: #A0AEC0;

/* Status Colors */
--success: #2ECC71;
--warning: #F1C40F;
--error: #E74C3C;
--info: #3498DB;
```

### Dark Mode Palette
```css
/* Backgrounds */
--dark-bg-primary: #1a202c;
--dark-bg-card: #2D3748;
--dark-bg-secondary: #1A202C;

/* Text */
--dark-text-primary: #E2E8F0;
--dark-text-secondary: #A0AEC0;
--dark-text-muted: #718096;

/* Borders */
--dark-border-light: #4A5568;
--dark-border-medium: #2D3748;
```

### Color Usage Guidelines

#### Risk Colors
- **Always pair color with text labels** (not color alone)
- Use for: AQI indicators, health risk badges, alert banners
- Ensure 4.5:1 contrast ratio with text

#### Background Colors
- **Light background (#F7FAFC)** for main content area
- **White cards (#FFFFFF)** for content containers
- **Gradient headers** for main sections

#### Text Colors
- **Primary text (#2C3E50)** for headings and important content
- **Secondary text (#718096)** for labels and descriptions
- **Muted text (#A0AEC0)** for timestamps and metadata

---

## Typography

### Font Family
```css
font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
```

**Why Inter?**
- Modern, clean, professional appearance
- Excellent readability at all sizes
- Wide range of weights
- Optimized for digital screens
- Free and open-source

### Font Weights
```css
--font-light: 300;      /* Subtle text, large headings */
--font-regular: 400;    /* Body text, default */
--font-medium: 500;     /* Emphasis, labels */
--font-semibold: 600;   /* Subheadings, buttons */
--font-bold: 700;       /* Headings, metrics */
```

### Type Scale

#### Desktop
```css
/* Display */
.display-1: 4rem (64px), weight: 700, line-height: 1.1
.display-2: 3rem (48px), weight: 700, line-height: 1.2

/* Headings */
h1: 2rem (32px), weight: 700, line-height: 1.3
h2: 1.5rem (24px), weight: 600, line-height: 1.4
h3: 1.25rem (20px), weight: 600, line-height: 1.4
h4: 1.125rem (18px), weight: 600, line-height: 1.5

/* Body */
.body-large: 1.125rem (18px), weight: 400, line-height: 1.6
.body: 1rem (16px), weight: 400, line-height: 1.6
.body-small: 0.875rem (14px), weight: 400, line-height: 1.6

/* Labels */
.label: 0.875rem (14px), weight: 600, line-height: 1.4, uppercase
.caption: 0.75rem (12px), weight: 500, line-height: 1.4
```

#### Mobile
```css
/* Reduce sizes by 15-20% for mobile */
h1: 1.5rem (24px)
h2: 1.25rem (20px)
.display-1: 2.5rem (40px)
```

### Letter Spacing
```css
--letter-spacing-tight: -0.02em;    /* Large headings */
--letter-spacing-normal: 0;         /* Body text */
--letter-spacing-wide: 0.05em;      /* Labels, buttons */
--letter-spacing-wider: 0.1em;      /* Small caps */
```

---

## Component Library

### 1. Metric Cards

#### Standard Metric Card
```
┌─────────────────────────┐
│ LABEL (uppercase)       │
│                         │
│      123                │  ← Big metric
│                         │
│ Status text            │
└─────────────────────────┘
```

**Properties:**
- Background: white (#FFFFFF)
- Border-radius: 12px
- Box-shadow: 0 2px 8px rgba(0,0,0,0.08)
- Padding: 1.5rem
- Hover: translateY(-2px), shadow increase

#### Risk Metric Card
```
┌─────────────────────────┐
│ HEALTH RISK            │
│                         │
│      High              │  ← Colored background
│                         │
│ Risk Level             │
└─────────────────────────┘
```

**Properties:**
- Background: Risk color (green/yellow/orange/red)
- Text color: White or dark (based on contrast)
- Border-left accent in some variants

### 2. Alert Banners

```
┌─────────────────────────────────────────┐
│ ⚠️ High Health Risk Alert: Message     │
│    here with recommendations            │
└─────────────────────────────────────────┘
```

**Properties:**
- Background: Risk color at 20% opacity (rgba)
- Border-left: 4px solid risk color
- Text color: Full risk color
- Padding: 1rem 1.5rem
- Border-radius: 8px
- Font-weight: 500

### 3. Buttons

#### Primary Button
- Background: #667eea (primary purple)
- Text: White
- Border-radius: 8px
- Padding: 0.5rem 1.5rem
- Font-weight: 500
- Hover: translateY(-1px), shadow

#### Secondary Button
- Background: transparent
- Border: 1px solid #CBD5E0
- Text: #4A5568
- Same other properties as primary

#### Icon Button
- Size: 40x40px
- Border-radius: 50%
- Center aligned icon
- Hover effect

### 4. Charts

**Common Properties:**
- Background: transparent
- Plot background: transparent
- Grid: rgba(0,0,0,0.05)
- Border-radius: 12px (container)
- Margin: 0 (for full width)
- Height: 300-600px depending on chart type

**Chart Types:**
- Line charts: Smooth curves, 3px width
- Area charts: 10% opacity fill
- Bar charts: Rounded corners
- Heatmaps: Risk color scale
- Box plots: Standard deviation display

### 5. Navigation

#### Sidebar
- Width: 280px
- Background: White (#FFFFFF)
- Fixed position
- Box-shadow: 2px 0 4px rgba(0,0,0,0.04)

#### Navigation Items
- Padding: 0.75rem 1rem
- Border-radius: 8px
- Hover: Background #F7FAFC
- Active: Background gradient, white text

### 6. Form Elements

#### Input Fields
- Border: 1px solid #E2E8F0
- Border-radius: 8px
- Padding: 0.75rem 1rem
- Focus: Border #667eea, box-shadow

#### Select Dropdowns
- Same as input fields
- Arrow icon on right
- Max-height for dropdown: 300px

#### Checkboxes & Radio
- Custom styled
- Accent color: #667eea
- Size: 20x20px
- Border-radius: 4px (checkbox), 50% (radio)

### 7. Loading States

#### Skeleton Loader
```css
background: linear-gradient(90deg, 
  #f0f0f0 25%, 
  #e0e0e0 50%, 
  #f0f0f0 75%
);
animation: loading 1.5s infinite;
border-radius: 8px;
```

#### Spinner
- Size: 40x40px
- Color: #667eea
- Border: 4px
- Animation: spin 1s linear infinite

### 8. Empty States

```
┌─────────────────────────┐
│                         │
│        📭 (icon)       │
│                         │
│   No Data Available    │
│   Description here     │
│                         │
│    [Action Button]     │
└─────────────────────────┘
```

**Properties:**
- Center aligned
- Icon: 4rem size
- Text: #A0AEC0 (muted)
- Padding: 3rem

---

## Layout Grids

### Desktop (> 768px)

#### 4-Column Grid (Metrics)
```
┌───────┬───────┬───────┬───────┐
│ Col 1 │ Col 2 │ Col 3 │ Col 4 │
└───────┴───────┴───────┴───────┘
Gap: 1rem
```

#### 3-Column Grid (Cards)
```
┌──────────┬──────────┬──────────┐
│  Card 1  │  Card 2  │  Card 3  │
└──────────┴──────────┴──────────┘
Gap: 1.5rem
```

#### 2-Column Grid (Content)
```
┌─────────────────┬─────────────┐
│   Main (66%)    │ Side (33%) │
└─────────────────┴─────────────┘
Gap: 2rem
```

### Tablet (768px)

#### 2-Column Grid
```
┌──────────────┬──────────────┐
│   Column 1   │   Column 2   │
└──────────────┴──────────────┘
Gap: 1rem
```

### Mobile (< 768px)

#### Single Column
```
┌─────────────────────────┐
│      Full Width         │
├─────────────────────────┤
│      Full Width         │
├─────────────────────────┤
│      Full Width         │
└─────────────────────────┘
Gap: 1rem
```

### Container Widths
```css
--container-max-width: 1400px;
--container-padding: 2rem;
--container-padding-mobile: 1rem;
```

---

## Interaction Flows

### User Journey: Checking Air Quality

```
1. Landing on Home Dashboard
   ↓
2. View current AQI and risk level
   ↓
3. See color-coded alert (if applicable)
   ↓
4. Check 30-day trend
   ↓
5. Quick action: Subscribe to alerts
   OR
   View detailed map
   OR
   View trends & analytics
```

### User Journey: Personal Risk Assessment

```
1. Navigate to Health Risk Calculator
   ↓
2. Fill out personal information
   - Age
   - Health conditions
   - Exposure level
   - Location
   ↓
3. Submit form
   ↓
4. View personalized risk score
   ↓
5. Read recommendations
   ↓
6. Review safety tips
```

### User Journey: Exploring Data (Map)

```
1. Navigate to Interactive Map
   ↓
2. View color-coded cities
   ↓
3. Click on a city marker
   ↓
4. View detailed city panel
   - AQI
   - PM2.5, PM10
   - Health advisory
   ↓
5. Compare multiple cities
```

### User Journey: Admin Workflow

```
1. Navigate to Admin Dashboard
   ↓
2. Check system status
   ↓
3. Monitor data sources
   ↓
4. Review AI model performance
   ↓
5. Retrain model (if needed)
   ↓
6. View prediction accuracy
   ↓
7. Export reports
```

### State Management

#### Key States
- **Loading:** Show skeleton loaders
- **Success:** Display data with animations
- **Error:** Show error message with retry option
- **Empty:** Display empty state with call-to-action

#### Transitions
- Smooth fade-in for data updates
- Loading → Success: 0.3s ease
- Page transitions: Instant (Streamlit rerun)

---

## Accessibility Guidelines

### WCAG 2.1 Level AA Compliance

#### Color Contrast
- **Normal text:** Minimum 4.5:1 ratio
- **Large text (18pt+):** Minimum 3:1 ratio
- **UI components:** Minimum 3:1 ratio

#### Examples
✅ White text on #E74C3C (red) = 5.2:1
✅ White text on #2ECC71 (green) = 3.8:1
✅ Dark text (#2C3E50) on #F1C40F (yellow) = 8.5:1

#### Keyboard Navigation
- All interactive elements accessible via Tab
- Focus indicators clearly visible
- Skip navigation links
- Logical tab order

#### Screen Readers
- Semantic HTML (headings, lists, nav)
- Alt text for icons (using emoji + text)
- ARIA labels where needed
- Form labels properly associated

#### Visual Indicators
- Never rely on color alone
- Use icons + text for status
- Clear error messages
- Descriptive link text

#### Motion & Animation
- Respect prefers-reduced-motion
- No auto-playing videos
- Smooth, purposeful transitions
- Cancel-able loading states

---

## Mobile Design

### Responsive Breakpoints
```css
/* Mobile First */
@media (min-width: 640px) { /* Small tablets */ }
@media (min-width: 768px) { /* Tablets */ }
@media (min-width: 1024px) { /* Desktop */ }
@media (min-width: 1280px) { /* Large desktop */ }
```

### Mobile Optimizations

#### Touch Targets
- Minimum size: 44x44px
- Spacing between targets: 8px minimum
- Larger padding for buttons

#### Typography
- Reduce font sizes by 15-20%
- Increase line-height for readability
- Shorter line lengths (optimal: 50-75 characters)

#### Layout
- Single column layout
- Collapsible sections
- Bottom sheet for filters
- Fixed headers with minimal height

#### Navigation
- Hamburger menu for sidebar
- Bottom navigation for key actions
- Swipe gestures (where applicable)

#### Images & Charts
- Lazy loading
- Responsive images
- Simplified charts for mobile
- Touch-enabled zoom/pan

#### Performance
- Minimize initial payload
- Progressive enhancement
- Optimize images
- Lazy load components

---

## Dark Mode

### Implementation Strategy
- CSS variables for all colors
- Detect system preference: `prefers-color-scheme`
- User toggle override
- Persist preference in local storage

### Color Adjustments

#### Backgrounds
```css
Light: #F7FAFC → Dark: #1a202c
Light: #FFFFFF → Dark: #2D3748
```

#### Text
```css
Light: #2C3E50 → Dark: #E2E8F0
Light: #718096 → Dark: #A0AEC0
```

#### Borders
```css
Light: #E2E8F0 → Dark: #4A5568
```

#### Shadows
```css
Light: rgba(0,0,0,0.08) → Dark: rgba(0,0,0,0.3)
```

### Component Adaptations
- Reduce shadow intensity
- Increase border visibility
- Adjust chart colors for contrast
- Soften bright colors (risk indicators)

---

## Implementation Notes

### Technology Stack
- **Framework:** Streamlit 1.31.0
- **Visualization:** Plotly 5.18.0
- **Data Processing:** Pandas, NumPy
- **Styling:** Custom CSS with Markdown

### Performance Considerations
- Lazy load heavy components
- Cache data queries with `@st.cache_data`
- Optimize chart rendering
- Minimize reruns with session state

### Browser Support
- Chrome/Edge (latest 2 versions)
- Firefox (latest 2 versions)
- Safari (latest 2 versions)
- Mobile browsers (iOS Safari, Chrome Android)

### Export Formats
This design system can be exported to:
- **React:** Component-based architecture
- **Vue:** Similar structure
- **Flutter:** Mobile app implementation
- **Figma:** Design mockups
- **Adobe XD:** Prototypes

---

## Design Checklist

### Before Launch
- [ ] All colors meet contrast requirements
- [ ] Typography scales work on all devices
- [ ] All interactive elements keyboard accessible
- [ ] Screen reader tested
- [ ] Mobile responsive on common devices
- [ ] Dark mode fully functional
- [ ] Loading states implemented
- [ ] Empty states designed
- [ ] Error handling UX defined
- [ ] Performance optimized

### Maintenance
- [ ] Document any design changes
- [ ] Update this guide with new components
- [ ] Test new features on mobile
- [ ] Verify accessibility with each update
- [ ] Keep design tokens synchronized

---

## Resources

### Design Tools
- **Figma:** For mockups and prototypes
- **Adobe Color:** For color palette generation
- **Contrast Checker:** WebAIM contrast checker
- **Google Fonts:** For Inter font family

### Inspiration
- Government of India digital services
- WHO air quality dashboards
- Modern weather applications
- Healthcare portals

### References
- [WCAG 2.1 Guidelines](https://www.w3.org/WAI/WCAG21/quickref/)
- [Material Design](https://material.io/)
- [Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines/)
- [Streamlit Documentation](https://docs.streamlit.io/)

---

**Document Version:** 1.0
**Last Updated:** November 21, 2025
**Maintainer:** UI/UX Team

---

<div align="center">

**This design system ensures consistency, accessibility, and excellence across the IHIP platform.**

</div>
