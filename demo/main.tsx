import React, { useState } from "react";
import ReactDOM from "react-dom/client";
import { initTheme } from "../src/theme";
import { Button } from "../src/components/Button";
import { Link } from "../src/components/Link";
import { TextInput } from "../src/components/TextInput";
import { Textarea } from "../src/components/Textarea";
import { Select } from "../src/components/Select";
import { Checkbox } from "../src/components/Checkbox";
import { RadioButton } from "../src/components/RadioButton";
import { Toggle } from "../src/components/Toggle";
import { Stepper } from "../src/components/Stepper";
import { DateInput } from "../src/components/DateInput";
import type { DateValue } from "../src/components/DateInput";
import { Slider } from "../src/components/Slider";
import { Tooltip } from "../src/components/Tooltip";
import { Modal } from "../src/components/Modal";
import { ToastProvider, useToast } from "../src/components/Toast";

initTheme({ primary: "#8e0038", secondary: "#bf1528" });

const STEPS = [
  { label: "Tarifdaten" },
  { label: "Beitrag" },
  { label: "Persönliches" },
  { label: "Zusammenfassung" },
];

const Section = ({ title, children }: { title: string; children: React.ReactNode }) => (
  <section style={{ marginBottom: 56 }}>
    <h2 style={{ fontSize: 12, fontWeight: 700, textTransform: "uppercase", letterSpacing: "0.08em", color: "#737373", marginBottom: 24, borderBottom: "1px solid #e1e1e1", paddingBottom: 10, fontFamily: '"FS Me", Arial, Helvetica, sans-serif' }}>
      {title}
    </h2>
    {children}
  </section>
);

const Row = ({ children }: { children: React.ReactNode }) => (
  <div style={{ display: "flex", flexWrap: "wrap", gap: 12, alignItems: "flex-start" }}>
    {children}
  </div>
);

function ToastDemo() {
  const { show } = useToast();
  return (
    <Row>
      <Button size="sm" variant="secondary" onClick={() => show("Änderungen gespeichert.", "success")}>Success</Button>
      <Button size="sm" variant="secondary" onClick={() => show("Etwas ist schiefgelaufen.", "error")}>Error</Button>
      <Button size="sm" variant="secondary" onClick={() => show("Bitte überprüfen Sie Ihre Eingaben.", "warning")}>Warning</Button>
      <Button size="sm" variant="secondary" onClick={() => show("Ihre Sitzung läuft in 5 Minuten ab.", "info")}>Info</Button>
    </Row>
  );
}

function App() {
  const [radioDate, setRadioDate] = useState("01.06.2026");
  const [stepperStep, setStepperStep] = useState(1);
  const [dateValue, setDateValue] = useState<DateValue>({ day: "23", month: "06", year: "1982" });
  const [sliderValue, setSliderValue] = useState(300000);
  const [modalOpen, setModalOpen] = useState(false);
  const [primaryColor, setPrimaryColor] = useState("#8e0038");
  const [secondaryColor, setSecondaryColor] = useState("#bf1528");

  return (
    <div style={{ fontFamily: '"FS Me", Arial, Helvetica, sans-serif', maxWidth: 680, margin: "0 auto", padding: "48px 24px", color: "#333333" }}>

      {/* ERGO Header */}
      <div style={{ marginBottom: 48, display: "flex", alignItems: "center", gap: 12 }}>
        <div style={{ background: "#8e0038", color: "#fff", fontWeight: 900, fontSize: 22, padding: "4px 10px", letterSpacing: "-0.5px", borderRadius: 2 }}>ERGO</div>
        <span style={{ color: "#8e0038", fontSize: 13, fontStyle: "italic" }}>Einfach, weil's wichtig ist.</span>
      </div>
      <h1 style={{ fontSize: 28, fontWeight: 700, marginBottom: 4, fontFamily: '"Fedra Serif", Georgia, serif', lineHeight: 1.3 }}>Komponentenübersicht</h1>
      <p style={{ color: "#737373", marginBottom: 48, fontSize: 14 }}>ERGO Design System — Versicherungsantrags-UI</p>

      {/* Theme */}
      <section style={{ marginBottom: 56, background: "#f2f2f2", padding: 20, borderRadius: 8 }}>
        <h2 style={{ fontSize: 12, fontWeight: 700, textTransform: "uppercase", letterSpacing: "0.08em", color: "#737373", marginBottom: 16, fontFamily: '"FS Me", Arial, Helvetica, sans-serif' }}>Theme</h2>
        <div style={{ display: "flex", gap: 16, alignItems: "flex-end", flexWrap: "wrap" }}>
          <div>
            <label style={{ display: "block", fontSize: 12, fontWeight: 700, marginBottom: 6 }}>Primärfarbe</label>
            <div style={{ display: "flex", alignItems: "center", gap: 8 }}>
              <input type="color" value={primaryColor} onChange={(e) => setPrimaryColor(e.target.value)} style={{ width: 40, height: 32, cursor: "pointer", border: "1px solid #d9d9d9", borderRadius: 4, padding: 2 }} />
              <span style={{ fontSize: 12, color: "#737373", fontFamily: "monospace" }}>{primaryColor}</span>
            </div>
          </div>
          <div>
            <label style={{ display: "block", fontSize: 12, fontWeight: 700, marginBottom: 6 }}>Sekundärfarbe</label>
            <div style={{ display: "flex", alignItems: "center", gap: 8 }}>
              <input type="color" value={secondaryColor} onChange={(e) => setSecondaryColor(e.target.value)} style={{ width: 40, height: 32, cursor: "pointer", border: "1px solid #d9d9d9", borderRadius: 4, padding: 2 }} />
              <span style={{ fontSize: 12, color: "#737373", fontFamily: "monospace" }}>{secondaryColor}</span>
            </div>
          </div>
          <Button size="sm" onClick={() => initTheme({ primary: primaryColor, secondary: secondaryColor })}>Anwenden</Button>
          <Button size="sm" variant="ghost" onClick={() => { setPrimaryColor("#8e0038"); setSecondaryColor("#bf1528"); initTheme({ primary: "#8e0038", secondary: "#bf1528" }); }}>Reset</Button>
        </div>
      </section>

      <Section title="Stepper — Antragsfortschritt">
        <div style={{ marginBottom: 16 }}>
          <Stepper steps={STEPS} currentStep={stepperStep} />
        </div>
        <Row>
          {STEPS.map((_, i) => (
            <Button key={i} size="sm" variant="secondary" onClick={() => setStepperStep(i + 1)}>Schritt {i + 1}</Button>
          ))}
        </Row>
      </Section>

      <Section title="Button">
        <Row>
          <Button variant="primary">Beitrag berechnen</Button>
          <Button variant="secondary">Mehr erfahren</Button>
          <Button variant="ghost">Zurück</Button>
          <Button disabled>Nicht verfügbar</Button>
        </Row>
        <div style={{ marginTop: 12 }}>
          <Button fullWidth>Jetzt abschließen</Button>
        </div>
        <div style={{ marginTop: 12 }}>
          <Row>
            <Button size="sm">Klein</Button>
            <Button size="md">Mittel</Button>
            <Button size="lg">Groß</Button>
          </Row>
        </div>
      </Section>

      <Section title="Link">
        <Row>
          <Link href="#">Mehr erfahren</Link>
          <Link href="#" variant="muted">Datenschutzhinweise</Link>
        </Row>
      </Section>

      <Section title="Tooltip">
        <Row>
          <Tooltip content="Die Versicherungssumme bestimmt die Auszahlung im Leistungsfall." position="top">
            <Button variant="secondary" size="sm">ⓘ Versicherungssumme</Button>
          </Tooltip>
          <Tooltip content="Hinweis unten" position="bottom">
            <Button variant="secondary" size="sm">ⓘ Unten</Button>
          </Tooltip>
          <Tooltip content="Laufzeit von 5 bis 40 Jahren wählbar." position="right">
            <Button variant="secondary" size="sm">ⓘ Laufzeit</Button>
          </Tooltip>
        </Row>
      </Section>

      <Section title="TextInput">
        <div style={{ display: "flex", flexDirection: "column", gap: 16, maxWidth: 400 }}>
          <TextInput label="Vorname" placeholder="Max" />
          <TextInput label="E-Mail-Adresse" type="email" placeholder="max@beispiel.de" hint="Wir senden Ihre Unterlagen an diese Adresse." />
          <TextInput label="Fehlerstate" placeholder="..." error="Bitte geben Sie einen gültigen Wert ein." />
          <TextInput label="Deaktiviert" value="Nicht editierbar" disabled />
        </div>
      </Section>

      <Section title="Textarea">
        <div style={{ display: "flex", flexDirection: "column", gap: 16, maxWidth: 400 }}>
          <Textarea label="Anmerkungen" placeholder="Haben Sie weitere Hinweise für uns?" rows={4} />
          <Textarea label="Mit Fehler" error="Dieses Feld ist erforderlich." />
        </div>
      </Section>

      <Section title="Select">
        <div style={{ display: "flex", flexDirection: "column", gap: 16, maxWidth: 400 }}>
          <Select label="Versicherungsart" placeholder="Bitte wählen" options={[
            { value: "risikoleben", label: "Risikolebensversicherung" },
            { value: "hausrat", label: "Hausratversicherung" },
            { value: "haftpflicht", label: "Haftpflichtversicherung" },
            { value: "kfz", label: "KFZ-Versicherung" },
          ]} />
          <Select label="Mit Fehler" options={[{ value: "a", label: "Option A" }]} error="Bitte treffen Sie eine Auswahl." />
        </div>
      </Section>

      <Section title="Slider — Versicherungssumme">
        <div style={{ maxWidth: 480 }}>
          <Slider
            min={50000} max={1000000} step={50000}
            value={sliderValue} onChange={setSliderValue}
            label="Gewünschte Versicherungssumme"
            unit="€"
            formatLabel={(v) => `${v.toLocaleString("de-DE")} €`}
          />
        </div>
      </Section>

      <Section title="DateInput — Geburtsdatum">
        <DateInput
          label="Geburtsdatum"
          value={dateValue}
          onChange={setDateValue}
          hint="Die versicherte Person muss zwischen 18 und 69 Jahren alt sein."
        />
      </Section>

      <Section title="RadioButton — Vertragsbeginn">
        <div style={{ display: "flex", flexDirection: "column", gap: 8, maxWidth: 400 }}>
          {[
            { value: "01.05.2026", label: "01.05.2026", description: "Nächstmöglicher Termin" },
            { value: "01.06.2026", label: "01.06.2026", description: "In ca. 4 Wochen" },
            { value: "01.07.2026", label: "01.07.2026", description: "In ca. 8 Wochen" },
          ].map(({ value, label, description }) => (
            <RadioButton key={value} name="startdatum" value={value} label={label} description={description}
              checked={radioDate === value} onChange={() => setRadioDate(value)} />
          ))}
          <RadioButton name="startdatum" value="disabled" label="Individuelles Datum" description="Derzeit nicht verfügbar" disabled />
        </div>
      </Section>

      <Section title="Checkbox">
        <div style={{ display: "flex", flexDirection: "column", gap: 12 }}>
          <Checkbox label="Ich stimme den Allgemeinen Versicherungsbedingungen zu." />
          <Checkbox label="Ich möchte den ERGO-Newsletter erhalten." defaultChecked />
          <Checkbox label="Deaktivierte Option" disabled />
        </div>
      </Section>

      <Section title="Toggle">
        <div style={{ display: "flex", flexDirection: "column", gap: 12 }}>
          <Toggle label="Dynamikerhöhung aktivieren" defaultChecked />
          <Toggle label="Beitragsrückgewähr einschließen" />
          <Toggle label="Option gesperrt" disabled />
        </div>
      </Section>

      <Section title="Modal">
        <Button variant="secondary" onClick={() => setModalOpen(true)}>Datenschutzhinweis anzeigen</Button>
        <Modal
          open={modalOpen}
          onClose={() => setModalOpen(false)}
          title="Einstellungen zum Datenschutz"
          footer={
            <>
              <Button variant="secondary" onClick={() => setModalOpen(false)}>Tool-Einstellungen</Button>
              <Button onClick={() => setModalOpen(false)}>Alle akzeptieren</Button>
            </>
          }
        >
          <p>Wenn Sie auf „Alle akzeptieren" klicken, stimmen Sie der Speicherung von Cookies und ähnlichen Technologien auf Ihrem Gerät zu. Sie helfen uns damit, die Nutzung der Website zu analysieren.</p>
          <p style={{ marginTop: 12 }}>Näheres finden Sie unter <Link href="#">Datenschutzhinweise</Link> und <Link href="#">Impressum</Link>.</p>
        </Modal>
      </Section>

      <Section title="Toast">
        <ToastDemo />
      </Section>
    </div>
  );
}

ReactDOM.createRoot(document.getElementById("root")!).render(
  <ToastProvider>
    <App />
  </ToastProvider>
);
