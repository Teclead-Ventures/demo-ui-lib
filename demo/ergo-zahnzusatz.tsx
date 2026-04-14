import ReactDOM from "react-dom/client";
import { initTheme } from "../src/theme";
import { ErgoHeader } from "../src/components/ergo/ErgoHeader";
import type { ErgoMegaMenuCategory } from "../src/components/ergo/ErgoMegaMenu";
import { ErgoHeroBanner } from "../src/components/ergo/ErgoHeroBanner";
import { ErgoPromoCard } from "../src/components/ergo/ErgoPromoCard";
import { ErgoTileCard } from "../src/components/ergo/ErgoTileCard";
import { ErgoCarousel } from "../src/components/ergo/ErgoCarousel";
import { ErgoReviewSection } from "../src/components/ergo/ErgoReviewSection";
import { ErgoAccordion } from "../src/components/ergo/ErgoAccordion";
import { ErgoDownloadLink } from "../src/components/ergo/ErgoDownloadLink";
import { ErgoStickyFooter } from "../src/components/ergo/ErgoStickyFooter";
import { ErgoFooter } from "../src/components/ergo/ErgoFooter";

initTheme({ primary: "#8e0038", secondary: "#bf1528" });

const ERGO_ASSETS = "https://assets.ergo.com/content/dam/ergo";
const ERGO_ICONS =
  "https://www.ergo.de/etc.clientlibs/ergoone/clientlibs/publish/assets/resources/icons";

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

const h2Style: React.CSSProperties = {
  fontFamily: "'Source Serif 4', serif",
  fontSize: 28,
  fontWeight: 700,
  color: "#333",
  lineHeight: 1.3,
  margin: 0,
  textAlign: "center",
};

const h3Style: React.CSSProperties = {
  fontFamily: "'Source Serif 4', serif",
  fontSize: 24,
  fontWeight: 700,
  color: "#333",
  lineHeight: 1.3,
  margin: 0,
};

const bodyStyle: React.CSSProperties = {
  fontSize: 16,
  color: "#333",
  lineHeight: 1.5,
  marginTop: 16,
  maxWidth: 800,
  textAlign: "center",
  margin: "16px auto 0",
};

const sectionStyle: React.CSSProperties = {
  padding: "48px 24px",
  maxWidth: 1440,
  margin: "0 auto",
};

const faqItems = [
  {
    title: "Wie funktioniert eine Zahnzusatzversicherung?",
    content: (
      <p>
        Steht bei Ihnen eine Zahnersatz-Behandlung an, dann erstellt der
        Zahnarzt eine Patienteninformation zum Zahnersatz für Sie. Die
        Krankenkasse prüft und genehmigt den Heil- und Kostenplan. Melden Sie
        sich bereits mit der ausgehändigten Patienteninformation bei der ERGO,
        um die Kostenübernahme des Restbetrages zu besprechen.
      </p>
    ),
  },
  {
    title: "Wie viel kostet eine gute Zahnzusatzversicherung?",
    content: (
      <p>
        Der Versicherungsbeitrag richtet sich vor allem nach dem
        Leistungsumfang und nicht allein nach dem Alter. Achten Sie darauf,
        welche Leistungen in welchem Umfang versichert sind. Bei ERGO können
        Sie sich die Leistungen Ihrer Zahnzusatzversicherung selbst
        zusammenstellen und so den monatlichen Beitrag mitbestimmen.
      </p>
    ),
  },
  {
    title:
      "Was bezahlt die gesetzliche Krankenkasse bei Zahnbehandlungen?",
    content: (
      <p>
        Die gesetzliche Krankenkasse übernimmt bei Zahnbehandlungen oft nicht
        die gesamten Kosten, sondern nur einen Teil. Mit lückenlos geführtem
        Bonusheft können Sie den Festzuschuss für Zahnersatz erhöhen: nach 5
        Jahren auf 70 %, nach 10 Jahren auf 75 %.
      </p>
    ),
  },
  {
    title: "Was und wie viel übernimmt eine Zahnzusatzversicherung?",
    content: (
      <p>
        Die Leistungen orientieren sich daran, was die gesetzlichen
        Krankenkassen in der Regel nicht bezahlen. ERGO bietet Ihnen
        Zahnzusatzversicherungen für Zahnersatz und Zahnerhalt.
        Leistungsinhalte und Leistungsumfang können Sie selbst wählen.
      </p>
    ),
  },
  {
    title: "Wann zahlt die Zahnzusatzversicherung nicht?",
    content: (
      <p>
        Ausgeschlossen sind in der Regel Kosten für Behandlungen, die bei
        Abschluss der Versicherung schon begonnen haben oder angeraten sind.
        Bei ERGO gibt es aber Ausnahmen: die Zahnzusatzversicherung mit
        Sofortschutz übernimmt Kosten auch für bereits 6 Monate vor
        Versicherungsbeginn begonnene Behandlungen.
      </p>
    ),
  },
  {
    title:
      "Wird Bleaching von der Zahnzusatzversicherung übernommen?",
    content: (
      <p>
        Bleaching wird nicht von jeder Zahnzusatzversicherung übernommen. Bei
        ERGO gibt es aber Tarife, die auch die Kosten für Bleaching unter
        bestimmten Voraussetzungen übernehmen. Der Dental-Vorsorge Premium
        übernimmt die Kosten für Bleaching zu 100 %.
      </p>
    ),
  },
  {
    title: "Welche Zahnzusatzversicherung zahlt sofort?",
    content: (
      <p>
        Bei den Zahnzusatzversicherungen von ERGO genießen Sie
        Versicherungsschutz vom ersten Moment an – ohne Wartezeit. Bei den
        Tarifen Zahnzusatzversicherung Sofort und Kieferorthopädie Sofort
        besteht auch keine Leistungsbegrenzung in den ersten
        Versicherungsjahren.
      </p>
    ),
  },
  {
    title: "Wann lohnt sich eine Zahnzusatzversicherung?",
    content: (
      <p>
        Der Abschluss einer Zahnzusatzversicherung lohnt sich für alle, die
        gesetzlich krankenversichert sind und sich vor hohen Eigenleistungen
        für Zahnbehandlungen schützen möchten. Es ist unmöglich
        vorherzusagen, wann Zahnersatz nötig wird.
      </p>
    ),
  },
  {
    title: "Kostet eine Zahnzusatzversicherung je nach Alter mehr?",
    content: (
      <p>
        Da sich der Beitrag bei ERGO neben dem gewählten Leistungsumfang auch
        nach dem Alter richtet, ist der Beitrag auch altersabhängig. Sollte
        eine altersbedingte Beitragsanpassung anstehen, werden Sie rechtzeitig
        informiert.
      </p>
    ),
  },
  {
    title: "Gibt es eine Zahnzusatzversicherung für Familien?",
    content: (
      <p>
        Eine Zahnzusatzversicherung für die ganze Familie in einem Tarif gibt
        es nicht. ERGO bietet Ihnen aber eine Zahnversicherung für Kinder mit
        Sofortleistung für kieferorthopädische Maßnahmen sowie passende Tarife
        für Erwachsene.
      </p>
    ),
  },
  {
    title:
      "Kann eine Zahnzusatzversicherung von der Steuer abgesetzt werden?",
    content: (
      <p>
        Ja, Beiträge für die Zahnzusatzversicherung sind Sonderausgaben der
        Kategorie „sonstige Vorsorgeaufwendungen" und können somit steuerlich
        geltend gemacht werden.
      </p>
    ),
  },
  {
    title: "Was sind die Vorteile einer Zahnzusatzversicherung?",
    content: (
      <p>
        Der große Vorteil besteht darin, dass Sie sich über Eigenanteile oder
        hohe Privatrechnungen Ihrer Zahnarztpraxis keine Gedanken mehr machen
        müssen. Bei ERGO finden Sie Zahnzusatzversicherungen, die Ihre
        Privatkosten deutlich verringern oder sogar komplett übernehmen.
      </p>
    ),
  },
  {
    title:
      "Übernimmt eine Zahnzusatzversicherung auch die Zahnreinigung?",
    content: (
      <p>
        Nicht jede private Zahnversicherung übernimmt die Kosten für die
        Professionelle Zahnreinigung (PZR). Mit Dental-Vorsorge Premium von
        ERGO sichern Sie sich 100 % der Kosten für jede PZR.
      </p>
    ),
  },
  {
    title: "Was zahlt eine Zahnzusatzversicherung bei Implantaten?",
    content: (
      <p>
        Beim ERGO-Tarif Dental-Schutz können Sie wählen, ob im Leistungsfall
        für ein Implantat 75 %, 90 % oder 100 % des Restbetrages übernommen
        wird.
      </p>
    ),
  },
  {
    title:
      "Müssen Gesundheitsfragen beantwortet werden beim Abschluss einer Zahnzusatzversicherung?",
    content: (
      <p>
        Für den Abschluss einer Zahnzusatzversicherung bei ERGO müssen keine
        Gesundheitsfragen beantwortet werden.
      </p>
    ),
  },
  {
    title: "Wie kann eine Zahnzusatzversicherung gekündigt werden?",
    content: (
      <p>
        In der Regel muss eine Zahnversicherung in schriftlicher Form
        gekündigt werden. Bei den ERGO-Tarifen Dental-Vorsorge, Dental-Schutz
        gilt ein monatliches Kündigungsrecht. Für die Tarife mit Sofortschutz
        gilt nach 24 Monaten ein monatliches Kündigungsrecht.
      </p>
    ),
  },
  {
    title: "Welche Zahnzusatzversicherung passt zu mir?",
    content: (
      <div>
        <p>
          <strong>Zahnersatz benötigt:</strong> Dann empfiehlt sich die
          Zahnersatzversicherung mit Sofortleistung. Damit verdoppeln Sie vom
          ersten Tag an den Festzuschuss der gesetzlichen Krankenversicherung.
        </p>
        <p style={{ marginTop: 8 }}>
          <strong>Zähne möglichst lange erhalten:</strong> Entscheiden Sie
          sich für einen der Zahnerhalttarife mit Basis- oder Premiumschutz.
        </p>
        <p style={{ marginTop: 8 }}>
          <strong>Vorsorge für Zahnersatz:</strong> Mit dem ERGO Dental-Schutz
          können Sie bis zu 100 % bei Zahnersatz sparen.
        </p>
      </div>
    ),
  },
  {
    title:
      "Gibt es Ausschlusskriterien, durch die man keine Zahnzusatzversicherung abschließen kann?",
    content: (
      <p>
        Personen, die keine Mitgliedschaft oder Mitversicherung in einer
        deutschen gesetzlichen Krankenversicherung vorweisen können, können bei
        ERGO leider keine Zahnzusatzversicherung abschließen.
      </p>
    ),
  },
];

const quickLinks = [
  { icon: "DocumentIcon", title: "Zahnrechnung einreichen", bgColor: "#f5e1eb" },
  { icon: "DentalRepairIcon", title: "Schon in Behandlung?", bgColor: "#fef6d2" },
  { icon: "DentalToothCleaningIcon", title: "Prof. Zahnreinigung", bgColor: "#ffe0cb" },
  { icon: "DentalImplantIcon", title: "Ratgeber Zahnersatz", bgColor: "#f5e1eb" },
  { icon: "ChecklistIcon", title: "Welcher Versicherungstyp?", bgColor: "#fef6d2" },
  { icon: "ShieldIcon", title: "Angst vorm Zahnarzt?", bgColor: "#ffe0cb" },
  { icon: "ToothIcon", title: "Schöne Zähne", bgColor: "#f5e1eb" },
  { icon: "MoneyIcon", title: "Zahnkosten zu hoch?", bgColor: "#fef6d2" },
  { icon: "HeartIcon", title: "Zahnspange nötig?", bgColor: "#ffe0cb" },
];

function ErgoZahnzusatzPage() {
  return (
    <div style={{ fontFamily: "var(--font-family)", color: "var(--color-text)" }}>
      <ErgoHeader categories={categories} />

      <main style={{ marginTop: 97 }}>
        {/* Hero */}
        <ErgoHeroBanner
          variant="short"
          textPosition="left"
          bgColor="#ffe0cb"
          image={`${ERGO_ASSETS}/produkte/kranken/zahnzusatzversicherungen/zahnzusatzversicherung.dam.jpg`}
          title="Zahnversicherungen"
          headline="Jeder Zahn ein guter Grund"
          description="Die ERGO Zahnzusatzversicherung schließt die Kostenlücke der gesetzlichen Krankenkasse und erstattet je nach Tarif bis zu 100 % für Zahnersatz, Kieferorthopädie und Prophylaxe."
        />

        {/* Why section */}
        <section style={sectionStyle}>
          <h2 style={h2Style}>
            Warum ist eine Zahnzusatzversicherung sinnvoll?
          </h2>
          <p style={bodyStyle}>
            Mit guter Pflege und regelmäßiger Vorsorge bleiben Ihre Zähne
            gesund und schön. Mit einer privaten Zahnzusatzversicherung
            strahlen Sie auch noch, wenn die Zahnarztrechnung kommt. Denn ohne
            private Absicherung kann Ihr Eigenanteil schnell auf ein paar
            Tausend Euro steigen.
          </p>
        </section>

        {/* Product overview */}
        <section style={sectionStyle}>
          <h2 style={h2Style}>
            Die Zahnzusatzversicherungen der ERGO im Überblick
          </h2>
          <div style={{ display: "flex", flexDirection: "column", gap: 24, marginTop: 24 }}>
            <ErgoPromoCard
              layout="horizontal"
              bgColor="#fef6d2"
              flag="Vorsorgeprodukt des Jahres 2023"
              image={`${ERGO_ASSETS}/produkte/kranken/zahnzusatzversicherungen/zahnzusatzversicherung-im-vergleich.dam.jpg`}
              headline="Individueller Zahnschutz"
              description="Wählen Sie Ihre individuelle Zahnversicherung. Und zahlen Sie nur für Leistungen, die Sie auch wirklich brauchen."
              price={{ prefix: "z. B.", value: "24,70", suffix: "monatlich" }}
              ctas={[{ href: "#", label: "Mehr erfahren", variant: "arrow" }]}
            />
            <ErgoPromoCard
              layout="horizontal"
              bgColor="#f5e1eb"
              image={`${ERGO_ASSETS}/produkte/kranken/zahnzusatzversicherungen/zek-produkt-gespiegelt.dam.jpg`}
              headline="Zahnzusatzversicherung mit Sofortschutz"
              description="Abschließen, auch wenn es eigentlich schon zu spät ist."
              price={{ prefix: "", value: "37,60", suffix: "monatlich" }}
              ctas={[{ href: "#", label: "Mehr erfahren", variant: "arrow" }]}
            />
            <ErgoPromoCard
              layout="horizontal"
              image={`${ERGO_ASSETS}/produkte/kranken/zahnzusatzversicherungen/kieferorthopaedie.dam.jpg`}
              headline="ERGO Kieferorthopädie Sofortschutz für Kinder"
              description="Ist Ihr Kind schon in Behandlung beim Kieferorthopäden? Diese Zahnzusatzversicherung zahlt auch, wenn es eigentlich schon zu spät ist."
              price={{ prefix: "ab", value: "12,70", suffix: "monatlich" }}
              ctas={[{ href: "#", label: "Mehr erfahren", variant: "arrow" }]}
            />
          </div>
        </section>

        {/* TestSiegel section */}
        <section style={{ padding: "48px 24px", backgroundColor: "#ccecef" }}>
          <div style={{ maxWidth: 1440, margin: "0 auto" }}>
            <h2 style={h2Style}>
              Die ERGO Zahnzusatzversicherungen – immer wieder ausgezeichnet
            </h2>
            <p style={bodyStyle}>Bei ERGO sind Sie in guten Händen.</p>
            <div
              style={{
                display: "flex",
                gap: 24,
                justifyContent: "center",
                flexWrap: "wrap",
                marginTop: 24,
              }}
            >
              <img
                src={`${ERGO_ASSETS}/testurteile/dentaltarif-ds75-ds90-ds100-dvb-dve-25nt40.dam.png`}
                alt="Testsiegel Dental-Tarif"
                style={{ height: 120 }}
              />
              <img
                src={`${ERGO_ASSETS}/testurteile/dentalschutz-ds75-ds90-ds100-25zx67.dam.png`}
                alt="Testsiegel Dental-Schutz"
                style={{ height: 120 }}
              />
              <img
                src={`${ERGO_ASSETS}/testurteile/dentalschutz-ds75-24ty61.dam.png`}
                alt="Testsiegel Dental-Schutz DS75"
                style={{ height: 120 }}
              />
            </div>
            <div style={{ marginTop: 24 }}>
              <ErgoReviewSection
                quote=""
                rating={4.6}
                reviewCount="387.143"
                companyName="ERGO Krankenversicherung AG"
              />
            </div>
          </div>
        </section>

        {/* Sub-product: Zahnerhalt */}
        <section style={sectionStyle}>
          <h3 style={h3Style}>Zahnversicherungen für Zahnerhalt</h3>
          <div style={{ marginTop: 16 }}>
            <ErgoCarousel columns={{ mobile: 1, tablet: 2, desktop: 2 }}>
              <ErgoTileCard
                variant="link"
                title="Dental-Vorsorge (DVB DVE)"
                text="Wer früher vorsorgt, lächelt länger: zuverlässiger Schutz für Ihren Zahnerhalt."
                ctaLabel="zum Produkt"
                ctaHref="#"
              />
            </ErgoCarousel>
          </div>
        </section>

        {/* Sub-product: Zahnersatz */}
        <section style={sectionStyle}>
          <h3 style={h3Style}>Zahnversicherungen für Zahnersatz</h3>
          <div style={{ marginTop: 16 }}>
            <ErgoCarousel columns={{ mobile: 1, tablet: 2, desktop: 2 }}>
              <ErgoTileCard
                variant="link"
                title="Verdoppelter Festzuschuss bei Zahnersatz (ZEF)"
                text="Reduzieren Sie den Eigenanteil bei Zahnersatz."
                ctaLabel="zum Produkt"
                ctaHref="#"
              />
              <ErgoTileCard
                variant="link"
                title="Dental-Schutz (DS75 DS90 DS100)"
                text="Mit den ERGO Dental-Schutz Tarifen bei Zahnersatz bis zu 100 % sparen – ohne Gesundheitsprüfung."
                ctaLabel="zum Produkt"
                ctaHref="#"
              />
              <ErgoTileCard
                variant="link"
                title="Zahnersatz mit Implantaten (ZZP)"
                text="Verdoppelung bei Zahnersatz wie Brücken, Kronen oder Prothesen und je Implantat bis zu 500 €."
                ctaLabel="zum Produkt"
                ctaHref="#"
              />
            </ErgoCarousel>
          </div>
        </section>

        {/* Sub-product: Sofortleistung */}
        <section style={sectionStyle}>
          <h3 style={h3Style}>
            Zahnzusatzversicherungen mit Sofortleistung
          </h3>
          <div style={{ marginTop: 16 }}>
            <ErgoCarousel columns={{ mobile: 1, tablet: 2, desktop: 2 }}>
              <ErgoTileCard
                variant="link"
                title="Zahnzusatzversicherung mit Sofortschutz (ZEK)"
                text="Abschließen, auch wenn es eigentlich schon zu spät ist."
                ctaLabel="zum Produkt"
                ctaHref="#"
              />
              <ErgoTileCard
                variant="link"
                title="Kieferorthopädie Sofort (KFO)"
                text="Einzigartiger Schutz mit Sofortleistung für Kinder."
                ctaLabel="zum Produkt"
                ctaHref="#"
              />
            </ErgoCarousel>
          </div>
        </section>

        {/* DKV cross-sell */}
        <section style={sectionStyle}>
          <h2 style={h2Style}>Die Zahnzusatzversicherungen der DKV</h2>
          <div style={{ marginTop: 24 }}>
            <ErgoPromoCard
              layout="horizontal"
              bgColor="#d3ebe5"
              image={`${ERGO_ASSETS}/produkte/kranken/zahnzusatzversicherungen/zahnzusatzversicherung-kombimed.dam.jpg`}
              headline="Sorgenfreier Rundumschutz Zahn der DKV"
              description="Für Ihr gesundes Lachen. Von Zahnbehandlung bis Zahnersatz. Für alle, die es einfach mögen."
              ctas={[{ href: "#", label: "Mehr erfahren", variant: "arrow" }]}
            />
          </div>
        </section>

        {/* QuickLinks */}
        <section style={sectionStyle}>
          <h2 style={h2Style}>Ihr Lächeln ist uns wichtig!</h2>
          <div style={{ marginTop: 24 }}>
            <ErgoCarousel columns={{ mobile: 1, tablet: 2, desktop: 3 }}>
              {quickLinks.map((link, i) => (
                <ErgoTileCard
                  key={i}
                  icon={`${ERGO_ICONS}/${link.icon}.svg`}
                  title={link.title}
                  ctaLabel="weiter"
                  ctaHref="#"
                  bgColor={link.bgColor}
                />
              ))}
            </ErgoCarousel>
          </div>
        </section>

        {/* Contact */}
        <section style={sectionStyle}>
          <h2 style={h2Style}>Nicht sicher, was Sie benötigen?</h2>
          <p style={bodyStyle}>
            Dann lassen Sie sich helfen. Die Experten von ERGO sind gern für
            Sie da.
          </p>
          <div style={{ marginTop: 24 }}>
            <ErgoCarousel columns={{ mobile: 1, tablet: 2, desktop: 3 }}>
              <ErgoTileCard
                icon={`${ERGO_ICONS}/PhoneIcon.svg`}
                title="7-24 Uhr (gebührenfrei)"
                text="Rufen Sie an!"
                ctaLabel="0800 / 999 4580"
                ctaHref="tel:08009994580"
                variant="contact"
              />
              <ErgoTileCard
                icon={`${ERGO_ICONS}/ManIcon.svg`}
                title="Ihr ERGO Berater"
                text="Gleich Termin vereinbaren!"
                ctaLabel="Berater kontaktieren"
                ctaHref="#"
                variant="contact"
              />
              <ErgoTileCard
                icon={`${ERGO_ICONS}/ChatIcon.svg`}
                title="Per Chat"
                text="Ein Klick und los gehts!"
                ctaLabel="Chat starten"
                ctaHref="#"
                variant="contact"
              />
            </ErgoCarousel>
          </div>
        </section>

        {/* Download */}
        <section style={sectionStyle}>
          <h2 style={h2Style}>Wissenswertes für Sie zum Download</h2>
          <div style={{ marginTop: 24 }}>
            <ErgoDownloadLink
              title="ERGO Zahntarife im Überblick"
              href="#"
              fileType="pdf"
              fileSize="712 KB"
            />
          </div>
        </section>

        {/* FAQ */}
        <section style={sectionStyle}>
          <h2 style={h2Style}>
            FAQs - Häufig gestellte Fragen zu Zahnzusatzversicherungen
          </h2>
          <div style={{ marginTop: 24 }}>
            <ErgoAccordion items={faqItems} />
          </div>
        </section>

        {/* Disclaimer */}
        <section style={{ padding: "24px", maxWidth: 1440, margin: "0 auto" }}>
          <p style={{ fontSize: 14, color: "#333", lineHeight: 1.5 }}>
            * Für die Zahnersatztarife "Dental-Schutz" zahlen Sie in den
            ersten 6 Vertragsmonaten nur 50 % des Tarifbeitrags. Es handelt
            sich um eine vereinfachte Darstellung. Altersbedingte
            Beitragserhöhungen können darin nicht berücksichtigt werden.
          </p>
          <button
            type="button"
            style={{
              fontSize: 14,
              color: "#8e0038",
              background: "transparent",
              border: "none",
              borderRadius: 100,
              padding: "4px 0",
              cursor: "pointer",
              fontWeight: 700,
              marginTop: 8,
            }}
          >
            Zur Beitragstabelle
          </button>
        </section>
      </main>

      <ErgoStickyFooter
        productName="Zahnzusatzversicherung"
        ctaLabel="Beitrag berechnen"
        ctaHref="#"
      />

      <ErgoFooter linkGroups={footerLinks} />
    </div>
  );
}

ReactDOM.createRoot(document.getElementById("root")!).render(
  <ErgoZahnzusatzPage />
);
