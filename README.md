# claude-mark2 — Suite Marketing IA en Français pour Claude Code

Une suite complète de skills, agents et scripts marketing entièrement en français, conçue pour Claude Code.

## Installation rapide

```bash
git clone https://github.com/mounra/ai-marketing.git
cd ai-marketing
bash install.sh
```

Ou en une commande depuis n'importe où :

```bash
curl -fsSL https://raw.githubusercontent.com/mounra/ai-marketing/main/install.sh | bash
```

## Ce qui est installé

| Composant | Quantité | Description |
|-----------|----------|-------------|
| Skills | 15 | Commandes slash pour chaque tâche marketing |
| Agents | 5 | Sous-agents spécialisés pour l'audit complet |
| Scripts | 4 | Scripts Python d'analyse et de génération |
| Modèles | 4 | Templates prêts à l'emploi |

## Commandes disponibles

```
/market audit <url>        Audit marketing complet (5 agents parallèles)
/market quick <url>        Aperçu marketing en 60 secondes
/market copy <url>         Générer du texte optimisé
/market emails <sujet>     Générer des séquences d'emails
/market social <sujet>     Calendrier de contenu réseaux sociaux
/market ads <url>          Créatifs et textes publicitaires
/market funnel <url>       Analyse du tunnel de vente
/market competitors <url>  Intelligence concurrentielle
/market landing <url>      CRO de page d'atterrissage
/market launch <produit>   Plan de lancement produit
/market proposal <client>  Générateur de proposition commerciale
/market report <url>       Rapport marketing complet (Markdown)
/market report-pdf <url>   Rapport marketing complet (PDF)
/market seo <url>          Audit SEO de contenu
/market brand <url>        Analyse la marque

```
## Détail des commandes 

Voici l'explication des 15 commandes de la suite marketing, complétement réécrite avec des cas d'usage concrets pour une boutique e-commerce qui vend des produits physiques (comme des vêtements, des cosmétiques, de l'électronique, des accessoires, etc.).

1. La Commande Maîtresse (L'Audit Global)
/market audit <url>

À quoi ça sert : C'est un scanner complet de votre boutique en ligne. Il analyse tout : le parcours d'achat, le SEO, le design, et la confiance.
Cas d'usage E-commerce : Avant de dépenser des milliers d'euros en publicités Facebook pour le Black Friday, vous lancez cette commande sur l'URL de votre boutique. Elle vous dira : "Attention, il manque des avis clients visibles sur vos fiches produits" ou "Le bouton 'Ajouter au panier' n'est pas assez visible sur la version mobile".
/market quick <url>

À quoi ça sert : La version flash de l'audit (analyse de la page d'accueil d'un coup d'œil).
Cas d'usage E-commerce : Vous venez de changer la bannière de votre page d'accueil avec une nouvelle promotion. Vous lancez la commande pour vérifier si l'offre (ex: "-20% sur la collection d'été") est bien compréhensible en moins de 3 secondes par un visiteur.

2. Le Tunnel de Vente et la Conversion
/market funnel <url>

À quoi ça sert : Analyser le parcours du client, du clic sur la pub jusqu'à la page de paiement.
Cas d'usage E-commerce : Vous avez 10 000 visiteurs par mois, mais seulement 50 ventes. Vous lancez cette commande pour trouver d'où vient le problème. Elle vous révèlera par exemple que le "goulot d'étranglement" se trouve à l'étape des frais de port (panier abandonné à cause de frais trop élevés ou découverts trop tard).
/market landing <url>

À quoi ça sert : Optimiser une page spécifique pour qu'elle vende mieux.
Cas d'usage E-commerce : Vous avez créé une page de vente dédiée pour votre produit "Best-Seller" (ex: un sérum anti-âge). La commande va analyser la page produit spécifique et vous dire d'ajouter des photos "Avant/Après", de remonter les bénéfices au-dessus du prix, et de créer de l'urgence.

3. Fiches Produits et Rédaction
/market copy <url>

À quoi ça sert : Réécrire des textes ennuyeux pour en faire des textes qui font vendre.
Cas d'usage E-commerce : Au lieu d'écrire "T-shirt 100% coton, col rond, noir", la commande va transformer la description de votre fiche produit en se basant sur les bénéfices clients : "Le T-shirt noir parfait qui ne rétrécit pas au lavage et met votre carrure en valeur".
/market brand <url>

À quoi ça sert : Définir le ton de votre marque pour avoir une image cohérente.
Cas d'usage E-commerce : Si vous vendez des montres de luxe, vous ne parlez pas aux clients de la même manière que si vous vendez des produits de beauté éco-responsables ciblés pour la génération Z. Cette commande crée votre "bible de marque" (le vocabulaire exact à utiliser sur le site et les réseaux sociaux).
/market seo <url>

À quoi ça sert : Optimiser les fiches produits et les collections pour ressortir sur Google.
Cas d'usage E-commerce : Vous lancez une nouvelle gamme de "sacs à dos imperméables". La commande va analyser votre page de collection et vérifier si vous utilisez les bons mots-clés dans les titres (H1, H2), les balises alt des images, et la description, pour attirer du trafic gratuit.

4. Acquisition (Publicité et Réseaux)
/market ads <url>

À quoi ça sert : Générer les textes (copywriting) et les idées d'images ou vidéos pour vos publicités payantes.
Cas d'usage E-commerce : Vous avez un budget pour des publicités TikTok ou Instagram (Meta Ads). Vous fournissez le lien de votre produit star à la commande, et elle vous écrit 3 scripts de vidéos courtes (ex: format "Unboxing", format "Problème/Solution", format "Témoignage UGC") prêts à être tournés.
/market social <sujet/url>

À quoi ça sert : Créer le planning complet de vos posts sur Instagram, TikTok, Pinterest, etc.
Cas d'usage E-commerce : Vous n'avez pas d'idées de publications pour Décembre. La commande vous planifie 1 mois de contenu : "Lundi : Montrer comment utiliser le produit en hiver", "Mercredi : Preuve sociale avec l'avis de Sophie", "Vendredi : Focus sur notre packaging écologique idéal pour offrir".
/market competitors <url>

À quoi ça sert : Scanner les boutiques concurrentes.
Cas d'usage E-commerce : Vous vendez des gourdes isothermes. Vous lancez la commande sur le site du leader de votre marché. L'outil vous montrera leurs meilleures offres (ils offrent les frais de port dès 50€), et vous proposera des stratégies pour vous différencier (par exemple, offrir un ebook gratuit sur la randonnée avec chaque gourde).

5. Fidélisation et Séquences E-mails
/market emails <sujet/url>

À quoi ça sert : Rédiger entièrement les e-mails automatiques que reçoit le client.
Cas d'usage E-commerce : C'est indispensable ! Vous demandez : "Crée une séquence de 3 e-mails de 'Récupération de Panier Abandonné' pour ma marque de bijoux". La commande va générer :
L'e-mail envoyé 4h après ("Oups, vous avez oublié quelque chose ?")
L'e-mail envoyé le lendemain (Preuve sociale + garantie)
L'e-mail envoyé 48h après (Code promo -10% de dernière chance)
/market launch <produit>

À quoi ça sert : Créer le plan d'action pour sortir un nouveau produit.
Cas d'usage E-commerce : Vous lancez une nouvelle saveur exclusive de compléments alimentaires sportifs en édition limitée. La commande vous fait le calendrier : comment teaser la "liste VIP" d'abord, quel e-mail envoyer le jour J de l'ouverture des ventes, et l'e-mail "Dernières heures" avant la rupture de stock.

6. Agence et B2B (Optionnel pour l'UGC)
Note : Ces deux commandes sont plus utiles si vous proposez des services, mais elles peuvent s'adapter.

/market proposal <client> (Rare en e-commerce B2C)

À quoi ça sert : Faire une proposition commerciale.
Cas d'usage E-commerce B2B : Vous essayez de vendre vos produits physiques en gros (Wholesale) à un revendeur physique ou un grand distributeur. La commande génère l'argumentaire complet et le devis structuré pour le convaincre de vous référencer.
/market report <url> et /market report-pdf <url>

À quoi ça sert : Éditer un rapport global.
Cas d'usage E-commerce : Réunir toutes les données pour faire un point avec vos associés, ou si vous engagez une agence de pub, pour leur donner un briefing complet sur l'état de votre site (les taux de conversion actuels, l'audit SEO, la stratégie, etc.).

## Prérequis

- **Claude Code** installé et configuré
- **Python 3.8+** pour les scripts d'analyse
- **reportlab** (optionnel, pour les rapports PDF) : `pip install reportlab`

## Structure du projet

```
claude-mark2/
├── market/
│   └── SKILL.md              # Orchestrateur principal
├── skills/
│   ├── market-audit/         # Audit marketing complet
│   ├── market-brand/         # Voix de marque
│   ├── market-copy/          # Copywriting optimisé
│   ├── market-emails/        # Séquences d'emails
│   ├── market-competitors/   # Analyse concurrentielle
│   ├── market-social/        # Calendrier réseaux sociaux
│   ├── market-funnel/        # Analyse du tunnel
│   ├── market-ads/           # Campagnes publicitaires
│   ├── market-proposal/      # Proposition commerciale
│   ├── market-landing/       # CRO page d'atterrissage
│   ├── market-launch/        # Plan de lancement
│   ├── market-report/        # Rapport marketing (MD)
│   ├── market-report-pdf/    # Rapport marketing (PDF)
│   └── market-seo/           # Audit SEO
├── agents/
│   ├── market-content.md     # Agent contenu & message
│   ├── market-conversion.md  # Agent optimisation conversion
│   ├── market-competitive.md # Agent analyse concurrentielle
│   ├── market-technical.md   # Agent technique & SEO
│   └── market-strategy.md    # Agent stratégie & croissance
├── scripts/
│   ├── analyze_page.py       # Analyse de page web
│   ├── competitor_scanner.py # Scanner de concurrents
│   ├── social_calendar.py    # Générateur de calendrier social
│   └── generate_pdf_report.py# Générateur de rapport PDF
├── templates/
│   ├── email-welcome.md      # Séquence email de bienvenue
│   ├── proposal-template.md  # Modèle de proposition client
│   ├── content-calendar.md   # Calendrier de contenu 30 jours
│   └── launch-checklist.md   # Checklist de lancement produit
├── install.sh                # Installateur
├── uninstall.sh              # Désinstallateur
└── requirements.txt          # Dépendances Python
```

## Fichiers générés

Chaque commande crée un fichier de rapport dans votre répertoire de travail :

| Commande | Fichier généré |
|----------|----------------|
| `/market audit` | `AUDIT-MARKETING.md` |
| `/market brand` | `VOIX-DE-MARQUE.md` |
| `/market copy` | `SUGGESTIONS-COPY.md` |
| `/market emails` | `SEQUENCES-EMAILS.md` |
| `/market competitors` | `RAPPORT-CONCURRENTS.md` |
| `/market social` | `CALENDRIER-SOCIAL.md` |
| `/market funnel` | `ANALYSE-FUNNEL.md` |
| `/market ads` | `CAMPAGNES-PUB.md` |
| `/market proposal` | `PROPOSITION-CLIENT.md` |
| `/market landing` | `ANALYSE-LANDING.md` |
| `/market launch` | `PLAN-LANCEMENT.md` |
| `/market report` | `RAPPORT-MARKETING.md` |
| `/market report-pdf` | `RAPPORT-MARKETING-<domaine>.pdf` |
| `/market seo` | `AUDIT-SEO.md` |

## Désinstallation

```bash
bash uninstall.sh
```

## Licence

MIT License — voir [LICENSE](LICENSE)
