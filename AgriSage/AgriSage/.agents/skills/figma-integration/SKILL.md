---
name: figma-integration
description: Comprehensive workflow for integrating Figma designs into code via MCP. Use when extracting Figma layouts, inspecting design tokens, converting Figma frames and components into React/HTML/CSS, and downloading design assets.
---

# Figma Integration Workflow (MCP)

This skill guides the agent in consuming Figma design data via Model Context Protocol (MCP) servers and translating them into pixel-accurate, responsive, and maintainable code.

---

## 1. Available Figma MCP Capabilities

When the Figma MCP server is active, the agent has access to design data directly from Figma:

1. **`get_figma_data`**:
   - Fetches the visual hierarchy, layout rules, typography, colors, fills, and dimensions of any Figma file or specific node.
   - Takes `fileKey` (the unique ID from the Figma URL) and optional `nodeId` (the specific frame or element ID).
   - Returns a structured, token-efficient representation optimized for code generation.

2. **`download_figma_images`**:
   - Downloads vector icons (SVG) and raster graphics (PNG/JPG) directly into the project repository.
   - Preserves asset fidelity without requiring manual export from Figma.

---

## 2. Parsing Figma URLs

Figma URLs follow this standard format:
`https://www.figma.com/design/<FILE_KEY>/<FILE_NAME>?node-id=<NODE_ID>`

- **`fileKey`**: The alphanumeric segment immediately following `/design/` or `/file/`.
- **`nodeId`**: The query parameter `node-id`. If the URL contains hyphens (e.g. `12-345` or `1234:5678`), normalize it to standard Figma format `12:345` (replace `-` with `:` if required).

---

## 3. Design-to-Code Translation Rules

### Layout Translation
- **Figma Auto Layout (Horizontal)** $\rightarrow$ CSS `display: flex; flex-direction: row;`
- **Figma Auto Layout (Vertical)** $\rightarrow$ CSS `display: flex; flex-direction: column;`
- **Item Spacing (Gap)** $\rightarrow$ CSS `gap: <value>px;`
- **Padding (Top, Right, Bottom, Left)** $\rightarrow$ CSS `padding: <T>px <R>px <B>px <L>px;`
- **Hug Contents** $\rightarrow$ `width: fit-content;` or default block flow
- **Fill Container** $\rightarrow$ `width: 100%;` or `flex: 1;`
- **Fixed Width/Height** $\rightarrow$ Specify exact pixel or rem values with appropriate responsive bounds (e.g. `max-width`, `min-width`)

### Color & Token Mapping
- Extract hex and rgba values into project CSS variables / design tokens:
  ```css
  :root {
    --primary: #...;
    --surface: #...;
    --text-primary: #...;
  }
  ```
- Ensure dark/light mode semantic mapping rather than hardcoding static hex codes where applicable.

### Typography Mapping
- Font Family: Match Google Fonts or project design system typography.
- Font Weight: `400` (Regular), `500` (Medium), `600` (SemiBold), `700` (Bold).
- Line Height: Express as relative `rem` or percentage unitless values (e.g., `line-height: 1.4`).
- Letter Spacing: Convert tracking from percent/px to `em`.

### Asset Management
- Download vector icons as SVGs into the project's assets directory.
- For illustrations and photography, download WebP/PNG and use responsive `<img>` or picture elements with explicit `alt` tags.

---

## 4. End-to-End Implementation Checklist

1. [ ] Parse the provided Figma URL for `fileKey` and `nodeId`.
2. [ ] Retrieve the design tree using the Figma MCP tool.
3. [ ] Extract colors, typography, spacing, and shadows into the project's styling tokens.
4. [ ] Identify sub-components and isolate reusable units.
5. [ ] Download required SVG icons and image assets.
6. [ ] Construct HTML/JSX structure mirroring the Figma AutoLayout hierarchy.
7. [ ] Apply styling with responsive media queries for desktop, tablet, and mobile.
8. [ ] Verify visual fidelity, interactions, and hover states.
