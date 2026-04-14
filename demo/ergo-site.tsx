import ReactDOM from "react-dom/client";
import { initTheme } from "../src/theme";
import { ErgoHeader } from "../src/components/ergo/ErgoHeader";
import type { ErgoMegaMenuCategory } from "../src/components/ergo/ErgoMegaMenu";
import { ErgoPromoBanner } from "../src/components/ergo/ErgoPromoBanner";
import { ErgoHeroBanner } from "../src/components/ergo/ErgoHeroBanner";
import { ErgoSectionHeader } from "../src/components/ergo/ErgoSectionHeader";
import { ErgoPromoCard } from "../src/components/ergo/ErgoPromoCard";
import { ErgoTileCard } from "../src/components/ergo/ErgoTileCard";
import { ErgoCarousel } from "../src/components/ergo/ErgoCarousel";
import { ErgoAccordion } from "../src/components/ergo/ErgoAccordion";
import { ErgoReviewSection } from "../src/components/ergo/ErgoReviewSection";
import { ErgoArticleTeaser } from "../src/components/ergo/ErgoArticleTeaser";
import { ErgoFooter } from "../src/components/ergo/ErgoFooter";

initTheme({ primary: "#8e0038", secondary: "#bf1528" });

const ERGO_ICONS =
  "https://www.ergo.de/etc.clientlibs/ergoone/clientlibs/publish/assets/resources/icons";
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

function ErgoSitePage() {
  return (
    <div style={{ fontFamily: "var(--font-family)", color: "var(--color-text)" }}>
      <ErgoHeader categories={categories} />

      <main style={{ marginTop: 97 }}>
        {/* Promo Banner */}
        <ErgoPromoBanner
          text="100%-Flatrate für professionelle Zahnreinigungen. Jetzt berechnen"
          href="#"
        />

        {/* Hero */}
        <ErgoHeroBanner
          image={`${ERGO_ASSETS}/produkte/leben/sterbegeldversicherung.dam.jpg`}
          title="ERGO Sterbevorsorge"
          headline="Entlasten Sie Ihre Lieben"
          description="Der Abschied ist schon schwer genug. Machen Sie Ihrer Familie zumindest das Finanzielle leicht."
          price={{ prefix: "Z. B.", value: "27,02", suffix: "monatlich" }}
          ctas={[
            { href: "#", label: "Jetzt informieren", variant: "pill" },
            { href: "#", label: "Beitrag berechnen", variant: "filled" },
          ]}
        />

        {/* Bestseller Section */}
        <section style={{ padding: "64px 24px", maxWidth: 1440, margin: "0 auto" }}>
          <ErgoSectionHeader
            label="BESTSELLER"
            heading="Die beliebtesten Produkte"
            subtitle="Zuverlässige Vorsorge für Sie: ganz einfach mit ERGO."
          />
          <div style={{ marginTop: 40 }}>
            <ErgoCarousel columns={{ mobile: 1, tablet: 2, desktop: 3 }}>
              <ErgoPromoCard
                image={`${ERGO_ASSETS}/produkte/kranken/zahnzusatzversicherungen/zahnzusatzversicherung-im-vergleich.dam.jpg`}
                headline="Zahnzusatzversicherungen im Vergleich"
                description="Ausgezeichnete Leistungen für Ihr Lächeln: bis zu 100 % Premium-Schutz."
                price={{ prefix: "Z. B.", value: "24,70", suffix: "monatlich" }}
                ctas={[{ href: "#", label: "Jetzt informieren", variant: "pill" }]}
              />
              <ErgoPromoCard
                image={`${ERGO_ASSETS}/produkte/sach/rechtsschutz/rechtsschutzversicherung.dam.jpg`}
                headline="Rechtsschutz"
                description="Stellen Sie sich Ihr Rechtsschutzpaket so zusammen, wie es zu Ihnen passt."
                price={{ prefix: "Ab", value: "12,17", suffix: "monatlich" }}
                ctas={[{ href: "#", label: "Jetzt informieren", variant: "pill" }]}
              />
              <ErgoPromoCard
                image={`${ERGO_ASSETS}/produkte/kranken/augenversicherung.dam.jpg`}
                headline="Augen- und Brillenversicherung"
                description="Versicherungsschutz für Ihren Durchblick: bis zu 300 € Zuschuss."
                price={{ prefix: "Z. B.", value: "7,10", suffix: "monatlich" }}
                ctas={[{ href: "#", label: "Jetzt informieren", variant: "pill" }]}
              />
            </ErgoCarousel>
          </div>
        </section>

        {/* Aktuelles Section */}
        <section style={{ padding: "64px 24px", backgroundColor: "var(--color-bg-blue)" }}>
          <div style={{ maxWidth: 1440, margin: "0 auto" }}>
            <ErgoSectionHeader
              label="AKTUELLES"
              heading="Aktionen und Produktangebote"
              subtitle="Wissenswertes für Sie"
            />
            <div style={{ marginTop: 40 }}>
              <ErgoCarousel columns={{ mobile: 1, tablet: 2, desktop: 3 }}>
                <ErgoTileCard
                  icon={`${ERGO_ICONS}/RiskIcon.svg`}
                  title="Risikolebensversicherung"
                  text="Für alle, die Ihnen am Herzen liegen."
                  ctaLabel="Mehr erfahren"
                  ctaHref="#"
                  bgColor="var(--color-bg-blue)"
                />
                <ErgoTileCard
                  icon={`${ERGO_ICONS}/DentalOrthodonticsIcon.svg`}
                  title="Kieferorthopädie Sofort für Kinder"
                  text="Rundum sicher vor hohen Zuzahlungen."
                  ctaLabel="Mehr erfahren"
                  ctaHref="#"
                  bgColor="var(--color-bg-blue)"
                />
                <ErgoTileCard
                  icon={`${ERGO_ICONS}/HobbyIcon.svg`}
                  title="Berufsunfähigkeitsversicherung"
                  text="Flexibler Schutz, der Ihre Karriere begleitet."
                  ctaLabel="Mehr erfahren"
                  ctaHref="#"
                  bgColor="var(--color-bg-blue)"
                />
              </ErgoCarousel>
            </div>
          </div>
        </section>

        {/* Kundenbewertungen */}
        <section style={{ padding: "64px 24px", backgroundColor: "var(--color-bg-green)" }}>
          <div style={{ maxWidth: 1440, margin: "0 auto" }}>
            <ErgoSectionHeader
              label="KUNDENBEWERTUNGEN"
              heading="Das sagen ERGO Kunden"
              subtitle="Nützliches Feedback und Erfahrungen für Sie"
            />
            <ErgoReviewSection
              quote="Ich habe meine Zahnarztrechnungen an Ergo geschickt und sie haben mir direkt das Geld überwiesen. Top. Bin sehr zufrieden."
              rating={4.6}
              reviewCount="387.143"
              companyName="ERGO Krankenversicherung AG"
            />
          </div>
        </section>

        {/* Kontakt Section */}
        <section style={{ padding: "64px 24px", maxWidth: 1440, margin: "0 auto" }}>
          <ErgoSectionHeader
            label="KONTAKT"
            heading="Sie haben Fragen?"
            subtitle="Ob Fragen, Kritik oder persönliche Beratung: ERGO ist für Sie da"
          />
          <div style={{ marginTop: 40 }}>
            <ErgoCarousel columns={{ mobile: 1, tablet: 2, desktop: 4 }}>
              <ErgoTileCard
                icon={`${ERGO_ICONS}/MailIcon.svg`}
                title="E-Mail"
                text="Schreiben Sie eine Nachricht."
                ctaLabel="Zum Kontaktformular"
                ctaHref="#"
                variant="contact"
              />
              <ErgoTileCard
                icon={`${ERGO_ICONS}/ChatIcon.svg`}
                title="Chat"
                text="Ein Klick führt zum Chat."
                ctaLabel="Chat öffnen"
                ctaHref="#"
                variant="contact"
              />
              <ErgoTileCard
                icon={`${ERGO_ICONS}/LocationIcon.svg`}
                title="ERGO Berater"
                text="Finden Sie Ihren ERGO Berater."
                ctaLabel="Zum Berater"
                ctaHref="#"
                variant="contact"
              />
              <ErgoTileCard
                icon={`${ERGO_ICONS}/PhoneIcon.svg`}
                title="Telefon"
                text="Rufen Sie an – gebührenfrei."
                ctaLabel="0800 / 3746 095"
                ctaHref="tel:08003746095"
                variant="contact"
              />
            </ErgoCarousel>
          </div>
        </section>

        {/* Ratgeber Section */}
        <section style={{ padding: "64px 24px", backgroundColor: "var(--color-bg-magenta)" }}>
          <div style={{ maxWidth: 1440, margin: "0 auto" }}>
            <ErgoSectionHeader
              label="RATGEBER"
              heading="Tipps der Redaktion"
              subtitle="Lesen lohnt sich!"
            />
            <div style={{ marginTop: 40 }}>
              <ErgoCarousel columns={{ mobile: 1, tablet: 2, desktop: 3 }}>
                <ErgoArticleTeaser
                  headline="Zahnwurzelentzündung"
                  subhead="Erreger im Zahn"
                  text="Wenn Karies oder Parodontitis unbehandelt bleibt, kann sich das Innere eines Zahnes entzünden."
                  ctaLabel="Mehr lesen"
                  ctaHref="#"
                />
                <ErgoArticleTeaser
                  headline="Der Organspendeausweis"
                  subhead="Leben retten mit Organspende"
                  text="Die Unsicherheit beim Thema Organspende ist oft groß."
                  ctaLabel="Mehr lesen"
                  ctaHref="#"
                />
                <ErgoArticleTeaser
                  headline="Professionelle Zahnreinigung"
                  subhead="Was ist PZR?"
                  text="Drei Buchstaben umfassend erklärt."
                  ctaLabel="Mehr lesen"
                  ctaHref="#"
                />
              </ErgoCarousel>
            </div>
          </div>
        </section>

        {/* Warum ERGO */}
        <section style={{ padding: "64px 24px", maxWidth: 1440, margin: "0 auto" }}>
          <ErgoSectionHeader
            label="WARUM ERGO?"
            heading="Einfach, weil's wichtig ist."
            subtitle="Ihr verlässlicher Partner für Versicherungen."
          />
          <div style={{ marginTop: 40 }}>
            <ErgoCarousel columns={{ mobile: 1, tablet: 3, desktop: 3 }}>
              <ErgoTileCard
                icon={`${ERGO_ICONS}/GlobeIcon.svg`}
                title="Weltweit"
                stat="in über 20 Ländern"
                variant="stat"
              />
              <ErgoTileCard
                icon={`${ERGO_ICONS}/GroupIcon.svg`}
                title="31 Mio."
                stat="zufriedene Kunden"
                variant="stat"
              />
              <ErgoTileCard
                icon={`${ERGO_ICONS}/HandshakeIcon.svg`}
                title="100+ Jahre"
                stat="Erfahrung"
                variant="stat"
              />
            </ErgoCarousel>
          </div>
        </section>

        {/* FAQ Accordion */}
        <section style={{ padding: "64px 24px", maxWidth: 800, margin: "0 auto" }}>
          <ErgoSectionHeader heading="Häufig gestellte Fragen" />
          <div style={{ marginTop: 32 }}>
            <ErgoAccordion
              items={[
                {
                  title: "Was ist eine Zahnzusatzversicherung?",
                  content: (
                    <p>
                      Eine Zahnzusatzversicherung ergänzt die Leistungen Ihrer
                      gesetzlichen Krankenversicherung für Zahnbehandlungen,
                      Zahnersatz und Kieferorthopädie.
                    </p>
                  ),
                },
                {
                  title: "Wann zahlt die Zahnzusatzversicherung?",
                  content: (
                    <p>
                      Die Zahnzusatzversicherung zahlt für zahnärztliche
                      Behandlungen, die über den Leistungskatalog der
                      gesetzlichen Krankenversicherung hinausgehen.
                    </p>
                  ),
                },
                {
                  title: "Gibt es eine Wartezeit?",
                  content: (
                    <p>
                      Bei einigen Tarifen gibt es eine Wartezeit von 8 Monaten.
                      ERGO bietet auch Tarife mit Sofortschutz ohne Wartezeit an.
                    </p>
                  ),
                },
              ]}
              allowMultiple
            />
          </div>
        </section>
      </main>

      <ErgoFooter linkGroups={footerLinks} />
    </div>
  );
}

ReactDOM.createRoot(document.getElementById("root")!).render(<ErgoSitePage />);
