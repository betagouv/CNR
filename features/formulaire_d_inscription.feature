# language: fr

Fonctionnalité: Formulaire d'inscription
  Contexte:
    Quand je me rends sur la page d'accueil
    Et je clique sur "Participer"

  Scénario: Je peux accéder au formulaire d'inscription depuis la page d'accueil
    Alors je peux lire "S'inscrire pour participer" dans la page

  Scénario: Je remplis le formulaire d'inscription correctement
    Quand je remplis le champ "Prénom" avec "Micheline"
    Et je remplis le champ "Adresse électronique" avec "micheline@france.org"
    Et je remplis le champ "Code postal" avec "12345"
    Et je choisis "Particulier" pour "Je suis :"
    Et je choisis "Climat" pour "Les thématiques sur lesquelles je veux m'investir"
    Et je coche la case "j'accepte les CGU"
    Et je soumets le formulaire
    Alors je peux lire "Votre inscription est enregistrée" dans la page
    Et un email a été envoyé à "micheline@france.org"
