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
import { ErgoReviewSection } from "../src/components/ergo/ErgoReviewSection";
import { ErgoCtaButton } from "../src/components/ergo/ErgoCtaButton";
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
                badge={`${ERGO_ASSETS}/testurteile/dentaltarif-ds75-ds90-ds100-dvb-dve-25nt40.dam.png`}
                ctas={[{ href: "#", label: "Jetzt informieren", variant: "filled" }]}
              />
              <ErgoPromoCard
                image={`${ERGO_ASSETS}/produkte/sach/rechtsschutz/rechtsschutzversicherung.dam.jpg`}
                headline="Rechtsschutz"
                description="Stellen Sie sich Ihr Rechtsschutzpaket so zusammen, wie es zu Ihnen passt."
                price={{ prefix: "Ab", value: "12,17", suffix: "monatlich" }}
                badge={`${ERGO_ASSETS}/grafiken/nebenkostenabrechnung-stoerer.dam.svg`}
                ctas={[{ href: "#", label: "Jetzt informieren", variant: "filled" }]}
              />
              <ErgoPromoCard
                image={`${ERGO_ASSETS}/produkte/kranken/augenversicherung.dam.jpg`}
                headline="Augen- und Brillenversicherung"
                description="Versicherungsschutz für Ihren Durchblick: bis zu 300 € Zuschuss."
                price={{ prefix: "Z. B.", value: "7,10", suffix: "monatlich" }}
                badge={`${ERGO_ASSETS}/testurteile/ekomi_stoerer.dam.png`}
                ctas={[{ href: "#", label: "Jetzt informieren", variant: "filled" }]}
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
                <ErgoTileCard
                  icon={`${ERGO_ICONS}/BrokenArmIcon.svg`}
                  title="Unfallversicherung"
                  text="Finanzielle Absicherung bei Unfällen."
                  ctaLabel="Mehr erfahren"
                  ctaHref="#"
                  bgColor="var(--color-bg-blue)"
                />
                <ErgoTileCard
                  icon={`${ERGO_ICONS}/HospitalIcon.svg`}
                  title="Krankenhauszusatzversicherung"
                  text="Privatpatient im Krankenhaus."
                  ctaLabel="Mehr erfahren"
                  ctaHref="#"
                  bgColor="var(--color-bg-blue)"
                />
                <ErgoTileCard
                  icon={`${ERGO_ICONS}/HandsMoneyIcon.svg`}
                  title="Basis-Rente"
                  text="Steuerlich geförderte Altersvorsorge."
                  ctaLabel="Mehr erfahren"
                  ctaHref="#"
                  bgColor="var(--color-bg-blue)"
                />
              </ErgoCarousel>
            </div>
          </div>
        </section>

        {/* Services Section */}
        <section style={{ padding: "64px 24px", maxWidth: 1440, margin: "0 auto" }}>
          <ErgoSectionHeader
            label="SERVICES"
            heading="Sparen Sie Zeit durch einfache Online-Services"
            subtitle="Informationen und Wissenswertes für ERGO Kunden und Interessierte"
          />
          <div style={{ marginTop: 40 }}>
            <ErgoCarousel columns={{ mobile: 1, tablet: 2, desktop: 2 }}>
              <ErgoPromoCard
                layout="vertical"
                image={`${ERGO_ASSETS}/landingpages/frau-vor-laptop.dam.jpg`}
                headline="Schaden oder Leistungsfall melden"
                description="Rechnungen einreichen, Schäden oder Leistungsfälle melden? Hier sind Sie richtig. Oder rufen Sie an."
                ctas={[{ href: "#", label: "Rechnung einreichen", variant: "arrow" }]}
              />
              <ErgoPromoCard
                layout="vertical"
                image={`${ERGO_ASSETS}/service/kundenbereich-vertraege-mann-tablet.dam.jpg`}
                headline="Ihr ERGO Kundenportal"
                description="Behalten Sie Ihre Versicherungen im Blick! Hier finden Sie viele Services, Ihr digitales Postfach und können bei Gewinnspielen mitmachen."
                badge={`https://assets.ergo.com/content/dam/ergo/grafiken/3-mio-kunden.dam.svg`}
                ctas={[{ href: "#", label: "Zum Kundenportal", variant: "pill" }]}
              />
            </ErgoCarousel>
          </div>
          <div style={{ marginTop: 32, textAlign: "center" }}>
            <ErgoCtaButton
              href="#"
              label="Alle Services ansehen"
              variant="arrow"
            />
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
          <div style={{ marginTop: 32, textAlign: "center" }}>
            <ErgoCtaButton
              href="#"
              label="Alle Kontaktmöglichkeiten ansehen"
              variant="arrow"
            />
          </div>
        </section>

        {/* Wissenswertes Section */}
        <section style={{ padding: "64px 24px", backgroundColor: "#fef6d2" }}>
          <div style={{ maxWidth: 1440, margin: "0 auto" }}>
            <ErgoSectionHeader
              label="WISSENSWERTES"
              heading="Rundum gut informiert mit ERGO"
              subtitle="Ihr Plus an Serviceleistungen"
            />
            <div style={{ marginTop: 40 }}>
              <ErgoCarousel columns={{ mobile: 1, tablet: 3, desktop: 3 }}>
                <ErgoTileCard
                  icon={`${ERGO_ICONS}/MegaphoneIcon.svg`}
                  title="Kunden werben Kunden"
                  text="Für jeden neu geworbenen Kunden erhalten Sie eine Geldprämie von bis zu 150 € und sichern sich die Gewinnchance auf einen von 3 kleinen Goldbarren."
                  ctaLabel="Gleich mitmachen"
                  ctaHref="#"
                  bgColor="#fef6d2"
                />
                <ErgoTileCard
                  icon={`${ERGO_ICONS}/BusinessCardIcon.svg`}
                  title="Der ERGO Newsletter"
                  text="Nichts mehr verpassen und immer top informiert."
                  ctaLabel="Jetzt anmelden"
                  ctaHref="#"
                  bgColor="#fef6d2"
                />
                <ErgoTileCard
                  icon={`${ERGO_ICONS}/StoreIcon.svg`}
                  title="Extra für Geschäftskunden"
                  text="Eine passgenaue, breite Produktpalette für Gewerbe."
                  ctaLabel="Zum Geschäftskundenbereich"
                  ctaHref="#"
                  bgColor="#fef6d2"
                />
              </ErgoCarousel>
            </div>
          </div>
        </section>

        {/* Seasonal Promo */}
        <section style={{ padding: "64px 24px", maxWidth: 1440, margin: "0 auto" }}>
          <ErgoPromoCard
            layout="horizontal"
            image={`${ERGO_ASSETS}/ratgeber/impuls/jungefrautanztimkirschgarten.dam.jpg`}
            headline="Frühlings-Check"
            description="Prüfen Sie jetzt Ihren Versicherungsschutz und starten Sie gut abgesichert in die neue Saison."
            ctas={[{ href: "#", label: "Jetzt prüfen", variant: "filled" }]}
          />
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

      </main>

      <ErgoFooter linkGroups={footerLinks} />
    </div>
  );
}

ReactDOM.createRoot(document.getElementById("root")!).render(<ErgoSitePage />);
