# demo-ui-lib

React UI component library with Tesla-inspired design and configurable theming. All components are styled to match Tesla's clean, minimal aesthetic and can be rebranded via `initTheme()`.

**Design tokens:** `#E31937` primary red · `#171A20` near-black · `#D0D1D2` borders · `4px` border-radius · Helvetica Neue / system sans-serif

## Installation

```bash
npm install demo-ui-lib
```

React ≥ 18 is required as a peer dependency.

## Setup

### 1. Import CSS

Once at your application entry point (`main.tsx` / `index.tsx`):

```ts
import "demo-ui-lib/dist/index.css";
```

### 2. Configure theme

```ts
import { initTheme } from "demo-ui-lib";

initTheme({
  primary: "#e31937",   // default: Tesla Red
  secondary: "#171a20", // default: Tesla near-black
});
```

Both parameters are optional — defaults apply without calling `initTheme()`. Call it at any time to switch themes at runtime.

### 3. Toast Provider (only if using Toast)

`ToastProvider` must wrap your app once:

```tsx
import { ToastProvider } from "demo-ui-lib";

ReactDOM.createRoot(document.getElementById("root")!).render(
  <ToastProvider>
    <App />
  </ToastProvider>
);
```

---

## Components

### Button

```tsx
<Button variant="primary" size="md" fullWidth={false} onClick={...}>
  Order Now
</Button>
```

| Prop | Type | Default |
|---|---|---|
| `variant` | `"primary" \| "secondary" \| "ghost"` | `"primary"` |
| `size` | `"sm" \| "md" \| "lg"` | `"md"` |
| `fullWidth` | `boolean` | `false` |

All native `<button>` attributes are forwarded.

---

### Link

```tsx
<Link href="/privacy" variant="muted">Privacy Policy</Link>
```

| Prop | Type | Default |
|---|---|---|
| `variant` | `"default" \| "muted"` | `"default"` |

All native `<a>` attributes are forwarded.

---

### TextInput

```tsx
<TextInput
  label="First Name"
  placeholder="Jane"
  hint="As it appears on your ID."
  error="This field is required."
/>
```

| Prop | Type |
|---|---|
| `label` | `string` |
| `hint` | `string` |
| `error` | `string` |

All native `<input>` attributes are forwarded.

---

### Textarea

```tsx
<Textarea
  label="Delivery Instructions"
  placeholder="Any special notes?"
  rows={4}
  error="This field is required."
/>
```

| Prop | Type | Default |
|---|---|---|
| `label` | `string` | — |
| `hint` | `string` | — |
| `error` | `string` | — |
| `rows` | `number` | `4` |

---

### Select

```tsx
<Select
  label="Model"
  placeholder="Select a model"
  options={[
    { value: "model-s", label: "Model S" },
    { value: "model-3", label: "Model 3" },
  ]}
  error="Please make a selection."
/>
```

| Prop | Type |
|---|---|
| `options` | `{ value: string; label: string }[]` |
| `label` | `string` |
| `placeholder` | `string` |
| `hint` | `string` |
| `error` | `string` |

---

### Checkbox

```tsx
<Checkbox
  label="I agree to the Terms of Service"
  checked={checked}
  onChange={(e) => setChecked(e.target.checked)}
/>
```

| Prop | Type |
|---|---|
| `label` | `string` (required) |

All native `<input type="checkbox">` attributes are forwarded.

---

### RadioButton

Renders as a selectable card with border. Use the same `name` for grouped options.

```tsx
<RadioButton
  name="model"
  value="model-s"
  label="Model S — Long Range"
  checked={selected === "model-s"}
  onChange={() => setSelected("model-s")}
/>
```

| Prop | Type |
|---|---|
| `label` | `string` (required) |

All native `<input type="radio">` attributes are forwarded.

---

### Toggle

```tsx
<Toggle
  label="Autopilot Enabled"
  checked={enabled}
  onChange={(e) => setEnabled(e.target.checked)}
/>
```

| Prop | Type |
|---|---|
| `label` | `string` (required) |

All native `<input type="checkbox">` attributes are forwarded.

---

### Slider

```tsx
<Slider
  min={40000}
  max={150000}
  step={5000}
  value={value}
  onChange={setValue}
  label="Your Budget"
  unit="$"
  formatLabel={(v) => `$${v.toLocaleString("en-US")}`}
/>
```

| Prop | Type | Default |
|---|---|---|
| `min` | `number` | — |
| `max` | `number` | — |
| `step` | `number` | `1` |
| `value` | `number` | — |
| `onChange` | `(value: number) => void` | — |
| `label` | `string` | — |
| `unit` | `string` | — |
| `formatLabel` | `(value: number) => string` | `toLocaleString` |

---

### DateInput

Three separate fields for day, month, and year with underline style.

```tsx
const [date, setDate] = useState({ day: "", month: "", year: "" });

<DateInput
  label="Date of Birth"
  value={date}
  onChange={setDate}
  hint="Must be 18 or older to place an order."
  error="Please enter a valid date."
/>
```

| Prop | Type |
|---|---|
| `value` | `{ day: string; month: string; year: string }` |
| `onChange` | `(value: DateValue) => void` |
| `label` | `string` |
| `hint` | `string` |
| `error` | `string` |

---

### Stepper

```tsx
<Stepper
  steps={[
    { label: "Model" },
    { label: "Configuration" },
    { label: "Details" },
    { label: "Review" },
  ]}
  currentStep={2}
/>
```

| Prop | Type |
|---|---|
| `steps` | `{ label: string }[]` |
| `currentStep` | `number` (1-based) |

---

### Tooltip

```tsx
<Tooltip content="Full Self-Driving enables automatic city and highway driving." position="top">
  <button>FSD Info</button>
</Tooltip>
```

| Prop | Type | Default |
|---|---|---|
| `content` | `string` | — |
| `position` | `"top" \| "bottom" \| "left" \| "right"` | `"top"` |

---

### Modal

```tsx
<Modal
  open={open}
  onClose={() => setOpen(false)}
  title="Terms & Conditions"
  footer={
    <>
      <Button variant="ghost" onClick={() => setOpen(false)}>Decline</Button>
      <Button onClick={() => setOpen(false)}>Accept & Continue</Button>
    </>
  }
>
  <p>Modal content...</p>
</Modal>
```

| Prop | Type |
|---|---|
| `open` | `boolean` |
| `onClose` | `() => void` |
| `title` | `string` |
| `footer` | `React.ReactNode` |

Closes on ESC key and backdrop click. Prevents background scrolling while open.

---

### Toast

```tsx
import { useToast } from "demo-ui-lib";

function MyComponent() {
  const { show } = useToast();

  return (
    <button onClick={() => show("Order confirmed!", "success")}>
      Place Order
    </button>
  );
}
```

`show(message, variant?)` — variants: `"success"` `"error"` `"warning"` `"info"` (default: `"info"`)

Toasts auto-dismiss after 4 seconds and can be manually closed.

---

## Development

```bash
npm run build       # Build library (dist/)
npm run demo        # Start demo app (http://localhost:5173)
npm run screenshots # Capture component screenshots
npm run test        # Run tests
npm run lint        # Lint
```
