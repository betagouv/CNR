# language: fr

Fonctionnalité: Page d'accueil
  Scénario: Je découvre le site
    Quand je me rends sur la page d'accueil
    Et je refuse les cookies
#    Alors je peux lire "Construisons ensemble l'avenir de la France" dans la page
#    Et la page est titrée "Conseil National de la Refondation"


  Scénario: J'accepte les cookies
    Quand je me rends sur la page d'accueil
    Et j'accepte les cookies
    Alors j'ai une entrée "cnrAuthorisedCookies" dans le local storage qui contient "googleAds,facebookAudience"


  Scénario: Je personnalise mes cookies
    Quand je me rends sur la page d'accueil
    Et je souhaite personnaliser les cookies
    Et je choisis le cookie "facebookAudience"
    Alors j'ai une entrée "cnrAuthorisedCookies" dans le local storage qui contient "facebookAudience"
