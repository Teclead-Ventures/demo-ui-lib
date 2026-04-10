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

initTheme();

const STEPS = [
  { label: "Tarifdaten" },
  { label: "Beitrag" },
  { label: "Persönliches" },
  { label: "Zusammenfassung" },
];

const Section = ({ title, children }: { title: string; children: React.ReactNode }) => (
  <section style={{ marginBottom: 56 }}>
    <h2 style={{ fontSize: 12, fontWeight: 700, textTransform: "uppercase", letterSpacing: "0.08em", color: "#767676", marginBottom: 24, borderBottom: "1px solid #e5e5e5", paddingBottom: 10 }}>
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
  const [sliderValue, setSliderValue] = useState(8000);
  const [modalOpen, setModalOpen] = useState(false);
  const [primaryColor, setPrimaryColor] = useState("#8c003c");
  const [secondaryColor, setSecondaryColor] = useState("#6b6b6b");

  return (
    <div style={{ fontFamily: "-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif", maxWidth: 680, margin: "0 auto", padding: "48px 24px", color: "#1a1a1a" }}>
      <h1 style={{ fontSize: 26, fontWeight: 700, marginBottom: 4 }}>demo-ui-lib</h1>
      <p style={{ color: "#767676", marginBottom: 48, fontSize: 14 }}>Komponentenübersicht</p>

      {/* Theme */}
      <section style={{ marginBottom: 56, background: "#f7f7f7", padding: 20, borderRadius: 8 }}>
        <h2 style={{ fontSize: 12, fontWeight: 700, textTransform: "uppercase", letterSpacing: "0.08em", color: "#767676", marginBottom: 16 }}>Theme</h2>
        <div style={{ display: "flex", gap: 16, alignItems: "flex-end", flexWrap: "wrap" }}>
          <div>
            <label style={{ display: "block", fontSize: 12, fontWeight: 600, marginBottom: 6 }}>Primary</label>
            <input type="color" value={primaryColor} onChange={(e) => setPrimaryColor(e.target.value)} style={{ width: 48, height: 32, cursor: "pointer", border: "1px solid #ccc", borderRadius: 4 }} />
            <span style={{ marginLeft: 8, fontSize: 12, color: "#767676" }}>{primaryColor}</span>
          </div>
          <div>
            <label style={{ display: "block", fontSize: 12, fontWeight: 600, marginBottom: 6 }}>Secondary</label>
            <input type="color" value={secondaryColor} onChange={(e) => setSecondaryColor(e.target.value)} style={{ width: 48, height: 32, cursor: "pointer", border: "1px solid #ccc", borderRadius: 4 }} />
            <span style={{ marginLeft: 8, fontSize: 12, color: "#767676" }}>{secondaryColor}</span>
          </div>
          <Button size="sm" onClick={() => initTheme({ primary: primaryColor, secondary: secondaryColor })}>Anwenden</Button>
          <Button size="sm" variant="ghost" onClick={() => { setPrimaryColor("#8c003c"); setSecondaryColor("#6b6b6b"); initTheme(); }}>Reset</Button>
        </div>
      </section>

      <Section title="Stepper">
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
          <Button variant="primary">weiter</Button>
          <Button variant="secondary">Berechnen</Button>
          <Button variant="ghost">Zurück</Button>
          <Button disabled>Deaktiviert</Button>
        </Row>
        <div style={{ marginTop: 12 }}>
          <Button fullWidth>weiter (full width)</Button>
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
          <Link href="#" variant="muted">Datenschutz</Link>
        </Row>
      </Section>

      <Section title="Tooltip">
        <Row>
          <Tooltip content="Die Versicherungssumme bestimmt die Auszahlung im Leistungsfall." position="top">
            <Button variant="secondary" size="sm">ⓘ Oben</Button>
          </Tooltip>
          <Tooltip content="Hinweis unten" position="bottom">
            <Button variant="secondary" size="sm">ⓘ Unten</Button>
          </Tooltip>
          <Tooltip content="Hinweis rechts" position="right">
            <Button variant="secondary" size="sm">ⓘ Rechts</Button>
          </Tooltip>
        </Row>
      </Section>

      <Section title="TextInput">
        <div style={{ display: "flex", flexDirection: "column", gap: 16, maxWidth: 400 }}>
          <TextInput label="Vorname" placeholder="Max" />
          <TextInput label="E-Mail" type="email" placeholder="max@beispiel.de" hint="Wir geben Ihre Daten nicht weiter." />
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
            { value: "kfz", label: "KFZ-Versicherung" },
            { value: "haftpflicht", label: "Haftpflichtversicherung" },
            { value: "hausrat", label: "Hausratversicherung" },
          ]} />
          <Select label="Mit Fehler" options={[{ value: "a", label: "Option A" }]} error="Bitte treffen Sie eine Auswahl." />
        </div>
      </Section>

      <Section title="Slider">
        <div style={{ maxWidth: 480 }}>
          <Slider
            min={1000} max={20000} step={500}
            value={sliderValue} onChange={setSliderValue}
            label="Wie viel Geld soll verfügbar sein?"
            unit="€"
            formatLabel={(v) => `${v.toLocaleString("de-DE")} €`}
          />
        </div>
      </Section>

      <Section title="DateInput">
        <DateInput
          label="Geburtsdatum"
          value={dateValue}
          onChange={setDateValue}
          hint="Die versicherte Person muss zwischen 40 und 85 Jahre alt sein."
        />
      </Section>

      <Section title="RadioButton — Karten-Style">
        <div style={{ display: "flex", flexDirection: "column", gap: 8, maxWidth: 400 }}>
          {["01.05.2026", "01.06.2026", "01.07.2026"].map((date) => (
            <RadioButton key={date} name="startdatum" value={date} label={date}
              checked={radioDate === date} onChange={() => setRadioDate(date)} />
          ))}
          <RadioButton name="startdatum" value="disabled" label="Nicht verfügbar" disabled />
        </div>
      </Section>

      <Section title="Checkbox">
        <div style={{ display: "flex", flexDirection: "column", gap: 12 }}>
          <Checkbox label="Ich stimme den AGB zu" />
          <Checkbox label="Newsletter abonnieren" defaultChecked />
          <Checkbox label="Deaktiviert" disabled />
        </div>
      </Section>

      <Section title="Toggle">
        <div style={{ display: "flex", flexDirection: "column", gap: 12 }}>
          <Toggle label="Benachrichtigungen aktivieren" defaultChecked />
          <Toggle label="Dunkelmodus" />
          <Toggle label="Deaktiviert" disabled />
        </div>
      </Section>

      <Section title="Modal">
        <Button variant="secondary" onClick={() => setModalOpen(true)}>Modal öffnen</Button>
        <Modal
          open={modalOpen}
          onClose={() => setModalOpen(false)}
          title="Datenschutzhinweis"
          footer={
            <>
              <Button variant="ghost" onClick={() => setModalOpen(false)}>Ablehnen</Button>
              <Button onClick={() => setModalOpen(false)}>Akzeptieren</Button>
            </>
          }
        >
          <p>Ihre personenbezogenen Daten werden gemäß unserer Datenschutzerklärung verarbeitet. Mit dem Abschluss des Vertrages stimmen Sie der Verarbeitung Ihrer Daten zu den genannten Zwecken zu.</p>
          <p style={{ marginTop: 12 }}>Sie können Ihre Einwilligung jederzeit mit Wirkung für die Zukunft widerrufen.</p>
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
