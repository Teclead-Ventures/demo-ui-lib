# demo-ui-lib

React UI-Komponentenbibliothek mit konfigurierbarem Theming. Komponenten orientieren sich am ERGO Corporate Design und sind per `initTheme()` für beliebige Primär- und Sekundärfarben anpassbar.

## Installation

```bash
npm install demo-ui-lib
```

React ≥ 18 ist als Peer Dependency erforderlich.

## Einrichtung

### 1. CSS importieren

Einmalig im Einstiegspunkt der Anwendung (z. B. `main.tsx` / `index.tsx`):

```ts
import "demo-ui-lib/dist/index.css";
```

### 2. Theme konfigurieren

```ts
import { initTheme } from "demo-ui-lib";

initTheme({
  primary: "#8c003c",   // Primärfarbe (Standard: ERGO Weinrot)
  secondary: "#6b6b6b", // Sekundärfarbe (Standard: Warm Grey)
});
```

Beide Parameter sind optional — ohne Aufruf gelten die ERGO-Defaults. `initTheme()` kann jederzeit erneut aufgerufen werden, um das Theme zur Laufzeit zu wechseln.

### 3. Toast-Provider (nur wenn Toast genutzt wird)

`ToastProvider` muss einmalig die App umschließen:

```tsx
import { ToastProvider } from "demo-ui-lib";

ReactDOM.createRoot(document.getElementById("root")!).render(
  <ToastProvider>
    <App />
  </ToastProvider>
);
```

---

## Komponenten

### Button

```tsx
<Button variant="primary" size="md" fullWidth={false} onClick={...}>
  weiter
</Button>
```

| Prop | Typ | Default |
|---|---|---|
| `variant` | `"primary" \| "secondary" \| "ghost"` | `"primary"` |
| `size` | `"sm" \| "md" \| "lg"` | `"md"` |
| `fullWidth` | `boolean` | `false` |

Alle nativen `<button>`-Attribute werden durchgereicht.

---

### Link

```tsx
<Link href="/datenschutz" variant="muted">Datenschutz</Link>
```

| Prop | Typ | Default |
|---|---|---|
| `variant` | `"default" \| "muted"` | `"default"` |

Alle nativen `<a>`-Attribute werden durchgereicht.

---

### TextInput

```tsx
<TextInput
  label="Vorname"
  placeholder="Max"
  hint="Wie auf dem Personalausweis."
  error="Dieses Feld ist erforderlich."
/>
```

| Prop | Typ |
|---|---|
| `label` | `string` |
| `hint` | `string` |
| `error` | `string` |

Alle nativen `<input>`-Attribute werden durchgereicht.

---

### Textarea

```tsx
<Textarea
  label="Anmerkungen"
  placeholder="Haben Sie weitere Hinweise?"
  rows={4}
  error="Dieses Feld ist erforderlich."
/>
```

| Prop | Typ |
|---|---|
| `label` | `string` |
| `hint` | `string` |
| `error` | `string` |
| `rows` | `number` (Default: `4`) |

---

### Select

```tsx
<Select
  label="Versicherungsart"
  placeholder="Bitte wählen"
  options={[
    { value: "kfz", label: "KFZ-Versicherung" },
    { value: "haftpflicht", label: "Haftpflichtversicherung" },
  ]}
  error="Bitte treffen Sie eine Auswahl."
/>
```

| Prop | Typ |
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
  label="Ich stimme den AGB zu"
  checked={checked}
  onChange={(e) => setChecked(e.target.checked)}
/>
```

| Prop | Typ |
|---|---|
| `label` | `string` (erforderlich) |

Alle nativen `<input type="checkbox">`-Attribute werden durchgereicht.

---

### RadioButton

Rendert als klickbare Karte mit Umrandung. Für Gruppen denselben `name` verwenden.

```tsx
<RadioButton
  name="tarif"
  value="basis"
  label="Basis-Tarif"
  checked={selected === "basis"}
  onChange={() => setSelected("basis")}
/>
```

| Prop | Typ |
|---|---|
| `label` | `string` (erforderlich) |

Alle nativen `<input type="radio">`-Attribute werden durchgereicht.

---

### Toggle

```tsx
<Toggle
  label="Benachrichtigungen aktivieren"
  checked={enabled}
  onChange={(e) => setEnabled(e.target.checked)}
/>
```

| Prop | Typ |
|---|---|
| `label` | `string` (erforderlich) |

Alle nativen `<input type="checkbox">`-Attribute werden durchgereicht.

---

### Slider

```tsx
<Slider
  min={1000}
  max={20000}
  step={500}
  value={value}
  onChange={setValue}
  label="Versicherungssumme"
  unit="€"
  formatLabel={(v) => `${v.toLocaleString("de-DE")} €`}
/>
```

| Prop | Typ | Default |
|---|---|---|
| `min` | `number` | — |
| `max` | `number` | — |
| `step` | `number` | `1` |
| `value` | `number` | — |
| `onChange` | `(value: number) => void` | — |
| `label` | `string` | — |
| `unit` | `string` | — |
| `formatLabel` | `(value: number) => string` | `toLocaleString("de-DE")` |

---

### DateInput

Drei separate Felder für Tag, Monat und Jahr mit Underline-Stil.

```tsx
const [date, setDate] = useState({ day: "", month: "", year: "" });

<DateInput
  label="Geburtsdatum"
  value={date}
  onChange={setDate}
  hint="Format: TT MM JJJJ"
  error="Bitte geben Sie ein gültiges Datum ein."
/>
```

| Prop | Typ |
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
    { label: "Tarifdaten" },
    { label: "Beitrag" },
    { label: "Persönliches" },
    { label: "Zusammenfassung" },
  ]}
  currentStep={2}
/>
```

| Prop | Typ |
|---|---|
| `steps` | `{ label: string }[]` |
| `currentStep` | `number` (1-basiert) |

---

### Tooltip

```tsx
<Tooltip content="Hinweistext" position="top">
  <button>ⓘ</button>
</Tooltip>
```

| Prop | Typ | Default |
|---|---|---|
| `content` | `string` | — |
| `position` | `"top" \| "bottom" \| "left" \| "right"` | `"top"` |

---

### Modal

```tsx
<Modal
  open={open}
  onClose={() => setOpen(false)}
  title="Datenschutzhinweis"
  footer={
    <>
      <Button variant="ghost" onClick={() => setOpen(false)}>Ablehnen</Button>
      <Button onClick={() => setOpen(false)}>Akzeptieren</Button>
    </>
  }
>
  <p>Inhalt des Modals...</p>
</Modal>
```

| Prop | Typ |
|---|---|
| `open` | `boolean` |
| `onClose` | `() => void` |
| `title` | `string` |
| `footer` | `React.ReactNode` |

Schließt sich bei ESC-Taste und Klick auf den Backdrop. Scrollt das Hintergrund-Dokument nicht mit.

---

### Toast

```tsx
import { useToast } from "demo-ui-lib";

function MeineKomponente() {
  const { show } = useToast();

  return (
    <button onClick={() => show("Gespeichert!", "success")}>
      Speichern
    </button>
  );
}
```

`show(message, variant?)` — verfügbare Varianten: `"success"` `"error"` `"warning"` `"info"` (Default: `"info"`)

Toasts verschwinden automatisch nach 4 Sekunden und können manuell geschlossen werden.

---

## Lokale Entwicklung

```bash
npm run build   # Library bauen (dist/)
npm run demo    # Demo-App starten (http://localhost:5173)
npm run test    # Tests ausführen
npm run lint    # Linting
```
