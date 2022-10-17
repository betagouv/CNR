# language: fr

Fonctionnalité: Page d'accueil
  Scénario: Je découvre le site
    Quand je me rends sur la page d'accueil
    Et je refuse les cookies
    Alors je peux lire "Construisons ensemble l'avenir de la France" dans la page
    Et la page est titrée "Conseil National de la Refondation"

  Scénario: Je m'inscris avec le formulaire de la page d'accueil
    Quand je me rends sur la page d'accueil
    Et je refuse les cookies
    Et je remplis le champ "Inscrivez-vous" avec "jeanne@france.org"
    Et je coche la case "J'ai lu et j'accepte les"
    Et je soumets le formulaire
    Alors un participant existe avec l'email "jeanne@france.org"


  Scénario: J'accepte les cookies
    Quand je me rends sur la page d'accueil
    Et j'accepte les cookies
    Alors j'ai une entrée "cnrAuthorisedCookies" dans le local storage qui contient "googleAds,facebookAudience"


  Scénario: Je personnalise mes cookies
    Quand je me rends sur la page d'accueil
    Et je souhaite personnaliser les cookies
    Et je choisis le cookie "facebookAudience"
    Alors j'ai une entrée "cnrAuthorisedCookies" dans le local storage qui contient "facebookAudience"
