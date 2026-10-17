ACT AS:  
A world-class Awwwards-level Creative Developer and Brand Experience Director, specializing in ultra-premium web design, Next.js, Framer Motion, advanced scroll-based storytelling, and 3D-inspired product interactions for global tech brands.

THE TASK:  
Design and implement a high-end, Apple-level scrollytelling landing page for Sony WH-1000XM6 headphones.  
The experience should feel like a cinematic product reveal combined with an interactive engineering showcase, driven entirely by scroll-based image-sequence animation and premium typography/layout. The core mechanic remains: as the user scrolls, an image sequence plays where the headphones explode (disassemble) into a floating technical diagram and then reassemble, synchronized with copywriting and storytelling beats.

TECH STACK INTENT (for behavior/style, not code generation):

* Framework: Next.js 14 (App Router mental model)  
* Styling: Tailwind CSS-style utility thinking (tight spacing, consistent scale)  
* Animation: Framer Motion-style scroll-linked animations, easing, and transitions  
* Rendering: HTML5 Canvas-style image-sequence playback for performance and smoothness

VISUAL DIRECTION & BRAND AESTHETIC:

* Overall vibe: Apple-level, luxury tech, cinematic, ultra-clean, minimal, editorial, premium corporate.  
* Seamless Blending:  
  * The page background color MUST perfectly match the background of the image sequence frames so image edges are 100% invisible and the headphones appear to float in a unified void.  
* Color Palette – Premium Corporate Dark Mode:  
  * Primary background: deep, near-black charcoal \#050505 (or eyedrop from hero frame).  
  * Secondary background: \#0A0A0C subtle variation for sections and overlays.  
  * Headings: text-white/90 with subtle soft glow or very subtle shadow for depth.  
  * Body text: text-white/60 for calm readability.  
  * Accent colors (Sony-inspired, high-end corporate):  
    * Primary accent: rich deep blue \#0050FF (or similar Sony-esque blue).  
    * Secondary accent: electric cyan \#00D6FF for tiny highlights, gradients, or interactive elements.  
  * Use soft gradients:  
    * Example: background radial gradient from \#050505 to a deep desaturated blue \#050815 behind hero content, extremely subtle.  
    * Accent gradient for buttons or key labels: from \#0050FF to \#00D6FF with a premium, glossy but minimal feel.  
* Typography:  
  * Fonts: Inter, SF Pro Display / SF Pro Text, or a Sony-like geometric grotesk.  
  * Style: ultra-clean, tracking-tight, medium-to-bold weights, large scale, strong hierarchy.  
  * Headings: bold, tight line-height, almost editorial—like Apple / Sony global websites.  
  * Body: 16–18px, comfortable line-height, muted color, concise, confident copy.  
* Overall layout feeling: full-bleed, edge-to-edge, generous negative space, no clutter, no decorative noise, restrained use of color, everything feels intentional and premium.

NAVBAR LIKE APPLE – STRUCTURE & BEHAVIOR:

* Ultra-minimal top navigation bar, inspired by Apple’s product pages.  
* Fixed / sticky at the top with a translucent, slightly blurred background (glassmorphism) that subtly appears after scroll.  
* Content (from left to right):  
  * Left: simple text logo “Sony” or “WH‑1000XM6” in a clean, medium-weight font.  
  * Center: minimalist navigation links: “Overview”, “Technology”, “Noise Cancelling”, “Specs”, “Buy”.  
  * Right: primary CTA button (e.g., “Pre-order” or “Discover WH‑1000XM6”) with subtle gradient border, soft hover glow.  
* Navbar styling:  
  * Height: slim and compact, like Apple product nav.  
  * Background: semi-transparent black rgba(5,5,5,0.75) with subtle backdrop blur.  
  * Hover states: very subtle underline or opacity shift, no heavy decoration.  
  * Scroll behavior:  
    * At top: nearly invisible or fully transparent.  
    * After slight scroll: fades in with a gentle transition, reinforcing the premium feel.

CORE INTERACTION: SCROLL-LINKED IMAGE SEQUENCE

* A central HTML5 Canvas-style full-screen area pinned/sticky during scroll.  
* Inside this space, a 120-frame image sequence of Sony WH‑1000XM6 in matte black plays as the user scrolls.  
* Sequence behavior:  
  * Start: fully assembled, hero beauty shot.  
  * Mid: gradually explodes / disassembles into internal components (drivers, microphones, PCBs, cushions, bands, structural elements).  
  * Peak: fully exploded technical diagram, every component floating in perfect alignment, hyper-realistic.  
  * End: components gracefully reassemble into the final hero product.  
* Each frame is ultra-high resolution, cinematic, photorealistic, 8K-level detail, with dramatic rim lighting, deep blacks, controlled reflections, and Apple-level product rendering quality.  
* The canvas and the background color are identical, enabling a seamless, edge-free presentation.

SCROLL LOGIC AND STORYTELLING BEATS (COPYWRITING-DRIVEN):  
Use scroll as a narrative axis. As the user scrolls from 0 to 100%, different text sections appear and disappear, synchronized with the state of the headphones.

1. HERO / INTRO (0–15% scroll)  
* Visual:  
  * WH‑1000XM6 fully assembled in a three-quarter angle, matte black, floating over a deep black background with subtle gradient.  
  * Cinematic rim light tracing the silhouette of the ear cups and headband.  
* Copy (centered, bold, confident, minimal):  
  * Large headline:  
    * “Sony WH‑1000XM6”  
    * Subtitle: “Silence, perfected.” or “Hear only what matters.”  
  * Supporting line (optional, smaller):  
    * “Flagship wireless noise cancelling, re‑engineered for a world that never stops.”  
* Tone: short, confident, high-end corporate product copy, like a hero banner on Sony or Apple’s official site.  
2. ENGINEERING REVEAL (15–40% scroll)  
* Visual:  
  * The headphones begin to subtly separate—ear cups drift away, headband lifts, ear cushions detach.  
  * Internal structure slowly becomes visible: drivers, acoustic chambers, microphones.  
* Copy (left aligned, emerging from the left as user scrolls):  
  * Headline: “Precision-engineered for silence.”  
  * Subcopy:  
    * “Custom drivers, sealed acoustic chambers, and optimized airflow deliver studio-grade clarity.”  
    * “Every component is tuned for balance, power, and comfort—hour after hour.”  
* Feel: technical yet poetic, mixing engineering language with emotional benefit.  
3. NOISE CANCELLING & MICROPHONES (40–65% scroll)  
* Visual:  
  * Components spread further apart, highlighting microphones and processing chips.  
  * Show microphone arrays and control board more prominently.  
* Copy (right aligned, sliding from the right):  
  * Headline: “Adaptive noise cancelling, redefined.”  
  * Supporting key points (short and punchy):  
    * “Multi-microphone array listens in every direction.”  
    * “Real-time noise analysis adjusts to your environment.”  
    * “Your music stays pure—planes, trains, and crowds fade away.”  
* Emphasis: advanced intelligence, real-time adaptation, premium isolation.  
4. SOUND & UPSCALING (65–85% scroll)  
* Visual:  
  * Drivers, coils, magnets, and acoustic chambers highlighted in the exploded view.  
  * Each piece lit with soft highlights to emphasize craftsmanship and Sony’s audio heritage.  
* Copy (left aligned or centered, depending on composition):  
  * Headline: “Immersive, lifelike sound.”  
  * Subcopy:  
    * “High-performance drivers unlock detail, depth, and texture in every track.”  
    * “AI-enhanced upscaling restores clarity to compressed audio, so every note feels alive.”  
* Tone: emotional \+ audiophile, referencing “detail”, “texture”, “space”, “presence”, “studio-level experience”.  
5. REASSEMBLY & CTA (85–100% scroll)  
* Visual:  
  * Components gracefully glide back into place; the headphones reassemble into perfect alignment.  
  * Final resting position: iconic hero pose, ready for purchase.  
* Copy (centered, strong call-to-action):  
  * Headline: “Hear everything. Feel nothing else.”  
  * Subheadline: “WH‑1000XM6. Designed for focus, crafted for comfort.”  
  * CTA button-style copy:  
    * “Experience WH‑1000XM6”  
    * Secondary: “See full specs”  
* Optional micro-copy: “Engineered for airports, offices, and everything in between.”

UI & VISUAL POLISH (HEAVY “GOOD” KEYWORDS):

* Keywords to emphasize in visual style:  
  * Cinematic, photorealistic, hyper-detailed, ultra-premium, luxury tech, editorial, Apple-level, Sony flagship, modern, minimalist, corporate high-end, glassmorphism, gradient glows, smooth, buttery scroll, hardware-accelerated, immersive, interactive storytelling, scrollytelling, polished, Awwwards-level.  
* Stylistic elements:  
  * Soft ambient glows behind the product and key text blocks.  
  * Subtle gradient borders around CTAs and key cards.  
  * Motion blur / depth suggestions through focus and lighting rather than noisy effects.  
  * Extremely subtle grid or alignment hints to ground the design.

TYPOGRAPHY & GRADIENT DETAILS:

* Headings:  
  * Large, tight, using a gradient fill from white to very light blue or cyan for a premium, digital, high-tech feel, but kept subtle.  
  * Example: gradient text: white → \#00D6FF at the very bottom of the letterforms, with a gentle fade.  
* Body:  
  * Solid rgba(255,255,255,0.6), smooth, no gradients, focus on readability.  
* Button text: white, semi-bold, with a subtle drop shadow for legibility over dark backgrounds.

CANVAS & LAYOUT BEHAVIOR (DESCRIPTIVE, NOT CODE):

* Sticky canvas section with height \~400vh, so the user scrolls through multiple story beats while the canvas remains pinned.  
* Canvas is always full-width and full-height of the viewport, with the content (headphones sequence) centered and scaled to fit while preserving aspect ratio.  
* The scroll controls frame index; frame selection uses smooth mapping to avoid flicker or jumps.  
* All UI chrome (navbar, text overlays) float above the canvas with subtle depth and non-intrusive presence.

FINAL PROMPT (COMBINED, READY-TO-USE):

“Design a hyper-premium, Apple-level, cinematic scrollytelling landing page for Sony WH‑1000XM6 flagship noise-cancelling headphones. The experience should feel like a high-end, editorial, corporate product story with a sticky full-screen canvas playing a 120-frame image sequence of matte black WH‑1000XM6 headphones exploding (disassembling) into a floating technical diagram and then reassembling as the user scrolls. The page uses a pure dark-mode aesthetic with a deep charcoal background \#050505 that perfectly matches the image sequence background so the headphones appear to float in seamless black space with no visible edges.

Include an Apple-style, ultra-minimal, fixed top navigation bar: a slim, glassmorphism nav with subtle backdrop blur, near-black translucent background, a simple product title (“WH‑1000XM6”), centered links like “Overview”, “Technology”, “Noise Cancelling”, “Specs”, “Buy”, and a right-aligned gradient CTA button reading “Experience WH‑1000XM6”. The nav starts nearly invisible at the top and gently fades in after a small scroll, mimicking Apple’s product navigation behavior.

Use premium corporate colors and gradients: primary background \#050505, secondary background \#0A0A0C, headings in text-white/90, body text in text-white/60, and sophisticated accent colors like deep Sony blue \#0050FF and electric cyan \#00D6FF for subtle gradients, underlines, and CTA borders. Add extremely subtle radial gradients behind the hero product and key sections, such as a soft glow from \#050505 to \#050815. Typography should use Inter or SF Pro Display/SF Pro Text with tracking-tight, bold headings and clean, readable body text, achieving a modern, minimalist, high-tech, editorial look.

The scroll-linked canvas animation is the core interaction: at 0–15% scroll, show the WH‑1000XM6 fully assembled in a cinematic hero shot with dramatic rim lighting, deep blacks, and photorealistic 8K-level detail. Center the copy: ‘Sony WH‑1000XM6’ as the main headline with ‘Silence, perfected.’ or ‘Hear only what matters.’ as the subheadline, and an optional line like ‘Flagship wireless noise cancelling, re‑engineered for a world that never stops.’. From 15–40% scroll, start the soft explosion of parts: ear cups, headband, and cushions drift apart, revealing internal structure. On the left side, fade in copy like ‘Precision-engineered for silence.’ with short, premium corporate subcopy about custom drivers, sealed acoustic chambers, and all-day comfort.

From 40–65% scroll, emphasize noise cancelling and microphones: highlight the multi-microphone array and processing components in the exploded view. On the right side, fade in copy like ‘Adaptive noise cancelling, redefined.’ with concise supporting lines such as ‘Multi-microphone array listens in every direction.’, ‘Real-time noise analysis adapts to your environment.’, and ‘Your music stays pure—planes, trains, and crowds fade away.’. From 65–85% scroll, put focus on sound quality and upscaling: emphasize drivers, coils, magnets, and acoustic chambers in the composition, with copy stating ‘Immersive, lifelike sound.’ and subcopy about high-performance drivers, detailed soundstage, and AI-enhanced upscaling that restores clarity and presence to compressed audio.

From 85–100% scroll, have all components gracefully glide back into place, the headphones fully reassemble, and the final hero state locks in. Show centered, bold CTA copy: ‘Hear everything. Feel nothing else.’, with subheadline ‘WH‑1000XM6. Designed for focus, crafted for comfort.’ and a primary CTA button ‘Experience WH‑1000XM6’ plus a secondary text link ‘See full specs’. The scroll transitions must feel smooth, buttery, and hardware-accelerated, with no stutter. All overlays (text, nav, buttons) should use subtle fades, slides, and eased transitions that reinforce the ultra-premium, cinematic feel.

Overall, optimize for an Awwwards-level, luxury tech experience with cinematic lighting, photorealistic matte black rendering, ultra-clean layout, high-end corporate color schemes, gradient accents, Apple-like navigation, premium copywriting, immersive scrollytelling, and a feeling of flagship, Sony-level craftsmanship and innovation.”

