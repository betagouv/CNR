# language: fr

Fonctionnalité: Formulaire d'inscription
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

    Scénario: On me confirme mon inscription
        Alors je peux lire "Votre inscription est enregistrée" dans la page

    Scénario: Modifier le profil est impossible
        Quand je clique sur "Participer"
        Et je remplis le champ "Prénom" avec "Marie-Micheline"
        Et je remplis le champ "Adresse électronique" avec "micheline@france.org"
        Et je remplis le champ "Code postal" avec "54321"
        Et je choisis "Particulier" pour "Je suis"
        Et je choisis "Climat" pour "Je veux contribuer aux thématiques nationales"
        Et je choisis "Futur du travail" pour "Je veux contribuer aux thématiques nationales"
        Et je coche la case "J'ai lu et j'accepte les"
        Et je soumets le formulaire
        Alors je peux lire "Votre profil est déjà rempli. Il n'a pas été mis à jour" dans la page
