## Énoncé

Pour recruter un stagiaire, une entreprise fait passer des entretiens individuels à quelques étudiants d'une université, un par un. Lors de chaque entretien, l’étudiant présente son bulletin de notes, indiquant sa moyenne annuelle, un score dans $[0,1]$. À l’issue de l’entretien, l’entreprise doit immédiatement prendre une décision : accepter l’étudiant en stage (et donc terminer le processus de recrutement sans voir les autres) ou le refuser définitivement pour passer au suivant.  
En réalité, l’entreprise, peu scrupuleuse, ne se fatigue pas et regarde uniquement le score pour faire son choix. La liste des entretiens comprend $n\geq 2$ passages (on suppose que l'entreprise connaît la valeur de $n$). Pour chaque passage, l’étudiant a été choisi au hasard (avec remise) parmi tous les étudiants de l'université (ce qui signifie qu’un même étudiant peut passer plusieurs entretiens).

**Questions :**

1. 🌶️💻 Peut-on concevoir une stratégie qui garantisse à l’entreprise de recruter, avec une probabilité d’au moins $1/e$, l’étudiant avec le meilleur score parmi les $n$ ?

2. L’entreprise a consulté les archives des années précédentes et connaît désormais la distribution des scores des étudiants dans l’université. Par ailleurs, elle apprend que l'université a suivi un protocole particulier pour constituer la liste de passage, visant à éviter qu'un excellent candidat ne soit recruté trop tôt au détriment de profils intermédiaires : l’étudiant du passage $i$ a été tiré au hasard parmi ceux dont le score appartient à l’intervalle $[a_i, b_i]$, où la suite $(a_i)$ est décroissante et la suite $(b_i)$ est croissante. Ces suites sont connues de l’entreprise. Montrer que l’entreprise peut adopter une stratégie telle que le score moyen de l’étudiant recruté soit au moins égal à la moitié du score moyen du meilleur des $n$ étudiants. Peut-on faire mieux ?

3. 🌶️ Supposons que l’entreprise ait désormais la possibilité de réorganiser librement l’ordre des entretiens dans la liste de passage avant qu’ils ne commencent. En appliquant ensuite la stratégie optimale, quel ordre doit-elle choisir pour maximiser le score moyen de l’étudiant recruté ?

&nbsp;

---
