# language: fr

Fonctionnalité: Page d'accueil
  Scénario: Je découvre le site
    Quand je me rends sur la page d'accueil
    Alors je peux lire "Construisons ensemble l'avenir de la France" dans la page
    Et la page est titrée "Conseil National de la Refondation"

  Scénario: Je m'inscris avec le formulaire de la page d'accueil
    Quand je me rends sur la page d'accueil
    Et je remplis le champ "Adresse électronique" avec "jeanne@france.org"
    Et je coche la case "accepte les CGU"
    Et je soumets le formulaire
    Alors je peux lire "jeanne@france.org" dans la page
