import ReactDOM from "react-dom/client";
import { initTheme } from "../src/theme";
import { ErgoHeader } from "../src/components/ergo/ErgoHeader";
import type { ErgoMegaMenuCategory } from "../src/components/ergo/ErgoMegaMenu";
import { ErgoHeroBanner } from "../src/components/ergo/ErgoHeroBanner";
import { ErgoPromoCard } from "../src/components/ergo/ErgoPromoCard";
import { ErgoTileCard } from "../src/components/ergo/ErgoTileCard";
import { ErgoCarousel } from "../src/components/ergo/ErgoCarousel";
import { ErgoSectionHeader } from "../src/components/ergo/ErgoSectionHeader";
import { ErgoFooter } from "../src/components/ergo/ErgoFooter";

initTheme({ primary: "#8e0038", secondary: "#bf1528" });

const ERGO_ASSETS = "https://assets.ergo.com/content/dam/ergo";

const categories: ErgoMegaMenuCategory[] = [
  {
    label: "Zahn",
    items: [
      { label: "Zahnzusatzversicherungen", href: "#" },
      { label: "Zahnzusatzversicherung mit Sofortschutz", href: "#" },
      { label: "Kieferorthopädie Sofortschutz für Kinder", href: "#" },
    ],
  },
  { label: "Risikolebensversicherung", items: [] },
  {
    label: "Gesundheit",
    items: [
      { label: "Krankenhauszusatzversicherung", href: "#" },
      { label: "Augen- und Brillenversicherung", href: "#" },
    ],
  },
  { label: "Hausrat & Gebäude", items: [] },
  { label: "Haftpflicht", items: [] },
  { label: "Kfz", items: [] },
  { label: "Reise", items: [] },
  { label: "Rechtsschutz", items: [] },
  { label: "Vorsorge", items: [] },
  { label: "Finanzen", items: [] },
  { label: "Unfallversicherung", items: [] },
];

const footerLinks = [
  {
    title: "Produkte",
    links: [
      { label: "Zahnzusatzversicherung", href: "#" },
      { label: "Rechtsschutzversicherung", href: "#" },
      { label: "Haftpflichtversicherung", href: "#" },
      { label: "Kfz-Versicherung", href: "#" },
    ],
  },
  {
    title: "Service",
    links: [
      { label: "Kundenportal", href: "#" },
      { label: "Schaden melden", href: "#" },
      { label: "Kontakt", href: "#" },
    ],
  },
  {
    title: "Unternehmen",
    links: [
      { label: "Über ERGO", href: "#" },
      { label: "Karriere", href: "#" },
      { label: "Presse", href: "#" },
    ],
  },
  {
    title: "Rechtliches",
    links: [
      { label: "Impressum", href: "#" },
      { label: "Datenschutz", href: "#" },
      { label: "AGB", href: "#" },
    ],
  },
];

interface ProductCategory {
  heading: string;
  description: string;
  image: string;
  badge?: string;
  productName: string;
  productDesc: string;
  price?: { prefix: string; value: string; suffix: string };
  subProducts: string[];
}

const productCategories: ProductCategory[] = [
  {
    heading: "ZAHNZUSATZVERSICHERUNGEN",
    description:
      "Schutz nach Maß für Ihr Lächeln. Möchten Sie hohe Zahnarztrechnungen für Zahnerhalt, Zahnersatz, Kieferorthopädie oder bereits begonnene Behandlungen vermeiden? Vergleichen Sie die Leistungen der ERGO Zahnversicherungen ohne Gesundheitsfragen für passgenauen Schutz.",
    image: `${ERGO_ASSETS}/produkte/kranken/zahnzusatzversicherungen/zahnzusatzversicherung-im-vergleich.dam.jpg`,
    badge: `${ERGO_ASSETS}/testurteile/dentaltarif-ds75-ds90-ds100-dvb-dve-25nt40.dam.png`,
    productName: "Individueller Zahnschutz",
    productDesc:
      "Ausgezeichnete Leistungen für Ihr schönstes Lachen. Bis zu 100 % Premiumschutz. Wählen Sie Ihre individuelle Zahnversicherung und zahlen Sie nur für Leistungen, die Sie auch wirklich brauchen.",
    price: { prefix: "z. B.", value: "24,70", suffix: "monatlich" },
    subProducts: [
      "Dental-Vorsorge für Zahnerhalt",
      "Dental-Schutz für Zahnersatz",
      "Zahnzusatzversicherung mit Sofortschutz ohne Wartezeit",
      "Kieferorthopädie Sofortschutz für Kinder",
      "Zahnzusatzversicherung (DKV)",
      "Zahnersatzversicherung mit Implantaten",
      "Zahnersatzversicherung mit verdoppeltem Festzuschuss",
    ],
  },
  {
    heading: "LEBENSVERSICHERUNGEN",
    description:
      "Damit Ihre Liebsten finanziell abgesichert sind. Sind Sie und Ihre Lieben für jede Lebenslage finanziell abgesichert? Stellen Sie sich diese Frage rechtzeitig, damit es später kein böses Erwachen gibt – für Jung und Alt.",
    image: `${ERGO_ASSETS}/produkte/leben/risikolebensversicherung-aktion.dam.jpg`,
    badge: `${ERGO_ASSETS}/testurteile/risikolebensversicherung-fm.dam.png`,
    productName: "Risikolebensversicherung",
    productDesc: "Exklusiv bei ERGO: Mit Waisenschutz im Premiumtarif.",
    price: { prefix: "Ab", value: "1,97", suffix: "monatlich" },
    subProducts: ["Sterbegeldversicherung", "Kidspolicen"],
  },
  {
    heading: "RECHTSSCHUTZVERSICHERUNGEN",
    description:
      "Damit Sie Ihr gutes Recht bekommen. Die ERGO Rechtsschutzversicherungen bieten umfassenden Schutz vor finanziellen Risiken durch rechtliche Auseinandersetzungen. Machen Sie kurzen Prozess mit dem Kostenrisiko bei einem Rechtsstreit.",
    image: `${ERGO_ASSETS}/produkte/sach/rechtsschutz/rechtsschutzversicherung.dam.jpg`,
    productName: "Rechtsschutzversicherung",
    productDesc:
      "Ob für Singles, Alleinerziehende, Paare und Familien: Stellen Sie sich Ihr Rechtsschutzpaket so zusammen, wie es zu Ihrer Lebenssituation und Ihren Wünschen passt.",
    price: { prefix: "Ab", value: "12,17", suffix: "monatlich" },
    subProducts: [
      "Verkehrsrechtsschutz",
      "Rechtsschutz für Mieter, Vermieter, Eigentümer",
    ],
  },
  {
    heading: "RENTENVERSICHERUNGEN",
    description:
      "Flexible Vorsorge für eine entspannte Zukunft. Die ausgezeichneten privaten Rentenversicherungen von ERGO ermöglichen Ihnen schon mit kleinen Beiträgen ein finanzielles Polster für Ihre Altersvorsorge. Je früher Sie beginnen, desto besser.",
    image: `${ERGO_ASSETS}/produkte/leben/rente/private-rente.dam.jpg`,
    productName: "Private Rentenversicherung",
    productDesc:
      "Für jeden Vorsorgetyp gibt es das passende Anlagekonzept: von renditestark bis sicherheitsorientiert.",
    price: { prefix: "Ab", value: "25,00", suffix: "monatlich" },
    subProducts: [
      "ERGO Chance Familie",
      "ERGO Balance Familie",
      "ERGO Index Familie",
      "Betriebliche Altersversorgung",
    ],
  },
  {
    heading: "KRANKENVERSICHERUNGEN",
    description:
      "Die optimale Ergänzung für gesetzlich Krankenversicherte. Fangen Sie Mehrkosten ab, die Sie sonst aus eigener Tasche zahlen müssen. Ergänzen Sie die Leistungen Ihrer gesetzlichen Krankenversicherung, z. B. mit einer Krankenhauszusatzversicherung oder Krankentagegeld.",
    image: `${ERGO_ASSETS}/produkte/kranken/krankenhauszusatzversicherung-dkv.dam.jpg`,
    badge: `${ERGO_ASSETS}/grafiken/wartezeitverzicht-stoerer.dam.svg`,
    productName: "DKV Krankenhauszusatzversicherung",
    productDesc:
      "Werden Sie schnell wieder gesund: mit Chefarztbehandlung, Ein- oder Zweibettzimmer oder Krankenhaustagegeld.",
    price: { prefix: "Z. B.", value: "6,40", suffix: "monatlich" },
    subProducts: [
      "Augen- und Brillenversicherung",
      "Krankentagegeldversicherung",
      "Rundumzusatzversicherung",
      "ERGO Krankenhauszusatzversicherung",
      "Krankenvollversicherung",
      "Beihilfeversicherung",
    ],
  },
  {
    heading: "HAFTPFLICHTVERSICHERUNGEN",
    description:
      "Damit aus kleinen Missgeschicken kein großer Ärger wird. Was auch immer passiert: Sichern Sie sich finanziell mit einer Haftpflichtversicherung ab, die zu Ihrer Lebenssituation passt – zum Beispiel für Sie selbst, Ihre Familie oder Ihren Hund.",
    image: `${ERGO_ASSETS}/produkte/sach/phv/private-haftpflichtversicherung.dam.jpg`,
    badge: `${ERGO_ASSETS}/testurteile/privathaftpflichtversicherung-23UZ65.dam.jpg`,
    productName: "Private Haftpflichtversicherung",
    productDesc:
      "Gegen dumm gelaufen hilft nur klug versichert. Denn dann sind Sie vor den finanziellen Folgen kleiner und großer Missgeschicke geschützt.",
    price: { prefix: "Z. B.", value: "5,26", suffix: "monatlich" },
    subProducts: [
      "Haus- und Grundbesitzer-Haftpflichtversicherung",
      "Bauherren-Haftpflichtversicherung",
      "Gewässerschaden-Haftpflichtversicherung",
      "Jagd-Haftpflichtversicherung",
      "Hundehalter-Haftpflichtversicherung",
      "Pferdehalter-Haftpflichtversicherung",
      "Wassersport-Haftpflichtversicherung",
    ],
  },
  {
    heading:
      "UNFALL-, BERUFSUNFÄHIGKEITS- UND GRUNDFÄHIGKEITSVERSICHERUNG",
    description:
      "Absicherung Ihres Körpers und Ihrer Arbeitskraft. Passiert ein Unfall, kann man seinen Beruf nicht mehr ausüben oder fallen Grundfähigkeiten des Körpers aus, fehlen Einkommen und Lebensqualität. Die ERGO Unfallversicherung bietet sinnvolle und wichtige Leistungen für Sie und Ihre Kinder.",
    image: `${ERGO_ASSETS}/produkte/sach/unfall/unfallversicherung.dam.jpg`,
    badge: `${ERGO_ASSETS}/grafiken/ohne-gesundheitsfragen-stoerer.dam.svg`,
    productName: "Unfallversicherung",
    productDesc:
      "Individueller Schutz im Baukastensystem für finanzielle und praktische Hilfe nach einem Unfall, z. B. im Haushalt.",
    price: { prefix: "Z. B.", value: "1,89", suffix: "monatlich" },
    subProducts: [
      "Berufsunfähigkeitsversicherung",
      "Grundfähigkeitsversicherung",
    ],
  },
  {
    heading: "PFLEGEVERSICHERUNGEN",
    description:
      "Damit Sie im Pflegefall Hilfe und Unterstützung bekommen. Denken Sie daran: Pflegebedürftigkeit kann nicht nur ältere Menschen plötzlich und unerwartet treffen. Rechtzeitige Vorsorge in eine private Pflegeversicherung zahlt sich aus.",
    image: `${ERGO_ASSETS}/produkte/kranken/pflegezusatzversicherung-li.c327x0x800x600.dam.jpg`,
    productName: "Pflegezusatzversicherung",
    productDesc:
      "Die Kosten im Pflegefall sind enorm. Hier ist private Vorsorge gefragt. Auch der Staat unterstützt Sie mit einem Zuschuss.",
    subProducts: [
      "Pflege Schutz Paket",
      "Pflegezusatzversicherung mit staatlicher Förderung",
    ],
  },
  {
    heading: "KFZ-VERSICHERUNGEN",
    description:
      "Unterwegs immer gut versichert. Schützen Sie Ihre Fahrzeuge entspannt vor hohen Kosten, die durch Unfälle, Diebstahl oder sonstige Schäden entstehen können.",
    image: `${ERGO_ASSETS}/produkte/sach/autoversicherung.dam.jpg`,
    productName: "Autoversicherung",
    productDesc:
      "Schneller Schadenservice. Hohe Versicherungssummen. Umfangreicher Versicherungsschutz.",
    price: { prefix: "Z. B. ab", value: "27,46", suffix: "monatlich" },
    subProducts: [
      "E-Auto-Versicherung",
      "Motorradversicherung",
      "Versicherung für besondere Fahrzeuge",
      "Schutzbrief",
      "Mopedversicherung",
      "E-Bike Versicherung",
    ],
  },
  {
    heading: "HAUSRAT- UND GEBÄUDEVERSICHERUNGEN",
    description:
      "Schützen Sie, was Ihnen gehört. Dinge, die Ihnen lieb und teuer sind, bedürfen besonderer Aufmerksamkeit. Sichern Sie Ihren Besitz mit einer ERGO Hausrat- und einer Glasversicherung ab.",
    image: `${ERGO_ASSETS}/produkte/sach/hausratversicherung.dam.jpg`,
    badge: `${ERGO_ASSETS}/grafiken/einfacher-online-abschluss-stoerer.dam.svg`,
    productName: "Hausratversicherung",
    productDesc:
      "Damit sichern Sie Ihr Hab und Gut finanziell ab gegen Schäden, z. B. durch Brand, Leitungswasser oder Einbruchdiebstahl. ERGO erstattet den Neuwert Ihres Hausrats.",
    price: { prefix: "Z. B.", value: "3,90", suffix: "monatlich" },
    subProducts: [
      "Wohngebäudeversicherung",
      "Gegenstandsversicherung",
      "Kunstversicherung",
      "Glasversicherung",
      "E-Bike Versicherung",
      "Geräteversicherung",
    ],
  },
  {
    heading: "REISEVERSICHERUNGEN",
    description:
      "Urlaub? Aber sicher! Genießen Sie die schönste Zeit des Jahres in vollen Zügen! Und falls doch mal eine Krankheit dazwischen kommen sollte, haben Sie mit einer Reiseversicherung vorausschauend vorgesorgt.",
    image: `${ERGO_ASSETS}/produkte/sach/reise/reiseversicherung_mann_surfbrett.dam.jpg`,
    productName: "Auslandskrankenversicherung",
    productDesc:
      "Krank im Urlaub? Sichern Sie sich bessere medizinische Versorgung und kompetente Ansprechpartner für optimale Hilfe im Notfall. Für alle Reisen im Jahr.",
    price: { prefix: "Z. B. ab", value: "9,90", suffix: "jährlich" },
    subProducts: [
      "RundumSorglos-Reiseversicherung",
      "Reiserücktrittsversicherung",
      "Schülerreiseversicherung",
      "Incoming-Versicherung",
      "Reiseschutz für Langzeitaufenthalte",
      "Gruppenreiseversicherung",
      "Ticketversicherung",
      "Campingversicherung",
      "Selbstbeteiligungs-Schutz für Wohnmobile",
    ],
  },
  {
    heading: "BAUSPAREN UND FINANZPRODUKTE",
    description:
      "Individuelle und zielgerichtete Finanzlösungen. Finanzielle Sicherheit und Vorsorge für später sehen für jeden Menschen in unterschiedlichen Lebenssituationen anders aus.",
    image: `${ERGO_ASSETS}/produkte/leben/rente/kidspolicen.dam.jpg`,
    productName: "ERGO Kidspolicen",
    productDesc:
      "Schenken Sie Zukunft und schaffen Sie für Ihre Kinder, Enkel oder Patenkinder ein attraktives Startkapital. Z. B. für den Führerschein oder ein Auslandssemester.",
    subProducts: [
      "Bausparvertrag",
      "Immobilienfinanzierung",
      "Vermögenspolicen",
      "Geldanlage in Investmentfonds",
      "Monatsgeld",
    ],
  },
];

function splitTagline(desc: string): [string, string] {
  const i = desc.search(/[.!?]\s[A-Z]/);
  return i >= 0 ? [desc.slice(0, i + 1), desc.slice(i + 2)] : [desc, ""];
}

function ErgoProduktePage() {
  return (
    <div
      style={{ fontFamily: "var(--font-family)", color: "var(--color-text)" }}
    >
      <ErgoHeader categories={categories} />

      <main style={{ marginTop: 97 }}>
        {/* Hero */}
        <ErgoHeroBanner
          image={`${ERGO_ASSETS}/service/alleprodukte_uebersicht.dam.jpg`}
          title="Alle ERGO Produkte"
          headline="Das ganze Angebot auf einen Blick"
          variant="short"
          textPosition="left"
        />

        {/* Product Categories */}
        {productCategories.map((cat, idx) => {
          const isLastCategory = idx === productCategories.length - 1;
          const ctas = isLastCategory
            ? [{ href: "#", label: "Jetzt informieren", variant: "pill" as const }]
            : [
                { href: "#", label: "Jetzt informieren", variant: "pill" as const },
                { href: "#", label: "Beitrag berechnen", variant: "filled" as const },
              ];

          return (
            <section
              key={idx}
              style={{ padding: "48px 24px", maxWidth: 1440, margin: "0 auto" }}
            >
              {(() => {
                const [tagline, longDesc] = splitTagline(cat.description);
                return (
                  <>
                    <ErgoSectionHeader label={cat.heading} heading={tagline} />
                    {longDesc && (
                      <p style={{ fontSize: 16, color: "#333", lineHeight: 1.5, textAlign: "center", maxWidth: 900, margin: "8px auto 0" }}>
                        {longDesc}
                      </p>
                    )}
                  </>
                );
              })()}

              <div style={{ marginTop: 24 }}>
                <ErgoPromoCard
                  layout="horizontal"
                  image={cat.image}
                  headline={cat.productName}
                  description={cat.productDesc}
                  price={cat.price}
                  badge={cat.badge}
                  ctas={ctas}
                />
              </div>

              {cat.subProducts.length > 0 && (
                <div style={{ marginTop: 24 }}>
                  <ErgoCarousel
                    columns={{
                      mobile: 1,
                      tablet: 2,
                      desktop: 2,
                    }}
                  >
                    {cat.subProducts.map((sub, subIdx) => (
                      <ErgoTileCard
                        key={subIdx}
                        title={sub}
                        variant="link"
                        ctaLabel="mehr lesen"
                        ctaHref="#"
                      />
                    ))}
                  </ErgoCarousel>
                </div>
              )}
            </section>
          );
        })}
      </main>

      <ErgoFooter linkGroups={footerLinks} />
    </div>
  );
}

ReactDOM.createRoot(document.getElementById("root")!).render(
  <ErgoProduktePage />
);
