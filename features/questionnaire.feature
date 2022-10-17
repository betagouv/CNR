# language: fr

Fonctionnalité: Questionnaire
  Contexte:
    Quand je me rends sur la page d'accueil
    Et je refuse les cookies
    Et je clique sur "Participer"
    Quand je remplis le champ "Prénom" avec "Micheline"
    Et je remplis le champ "Adresse électronique" avec "micheline@france.org"
    Et je remplis le champ "Code postal" avec "12345"
    Et je choisis "Particulier" pour "Je suis"
    Et je choisis "Climat" pour "Je veux contribuer aux thématiques nationales"
    Et je coche la case "J'ai lu et j'accepte les"
    Et je soumets le formulaire
    Et je soumets le formulaire

  Scénario: Je peux soumettre mes réponses
    Quand je remplis toutes les questions du formulaire
    Et je soumets le formulaire
    Alors il existe une réponse "foobar"
