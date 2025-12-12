## Énoncé

Considérons un jeu auquel participent $K$ joueurs. Chaque joueur reçoit trois dés à six faces. Chacun lance simultanément ses trois dés et obtient un score, défini comme la somme des trois résultats. Après ce premier lancer, chaque joueur doit décider : 
   - soit de conserver ce score et d'arrêter son tour,

   - soit de relancer les trois dés pour tenter d'obtenir un meilleur score.
Si un joueur choisit de relancer, il perd irréversiblement son score précédent, même si celui-ci était plus élevé. Chaque joueur peut relancer au maximum deux fois,  c'est-à-dire qu'il effectue entre un et trois lancers au total.  Les scores intermédiaires sont gardés secrets jusqu'à la fin de la partie. Lorsque tous les joueurs ont terminé, les scores sont révélés.  Le joueur qui possède le plus petit score est déclaré perdant.  En cas d'égalité pour le plus faible score, le perdant est choisi au hasard  parmi les ex~æquo. 

**Questions :**

1. 🌶️${}^{2.1}$💻${}^{2.9}$ Déterminez, en fonction de $K$, un profil de stratégies pures  (c’est-à-dire non aléatoires) tel que chaque joueur adopte  sa meilleure réponse compte tenu des choix des autres joueurs. 

2. 🌶️${}^{2.2}$ On considère un joueur isolé face à une coalition composée des $K-1$ autres joueurs, et on s’intéresse aux stratégies mixtes (le coup joué est sélectionné au hasard selon une certaine distribution de probabilité). Montrez que, sans perte de généralité, le problème peut se ramener à un jeu à somme nulle de taille $120\times120$ entre deux joueurs (le joueur isolé versus la coalition). 

3. 🌶️${}^{2.3}$ En généralisant à $\ell+1$ lancers, montrez qu'un joueur isolé face à une coalition composée des $K-1$ autres joueurs peut se ramener à un jeu à somme nulle  de dimension $\binom{14 + \ell}{\ell} \times \binom{14 + \ell}{\ell}$ entre deux joueurs. 

4. 🌶️${}^{1.1}$💻${}^{3.3}$ On considère de nouveau le cas du jeu en concurrence pure (sans coalition). On suppose qu’après chaque relance, tous les joueurs observent le nombre $L$ de joueurs encore en jeu (n’ayant pas arrêté). Pour trois lancers et pour tout $K\le 100$, déterminez un profil de stratégies pures tel que chaque joueur adopte sa meilleure réponse compte tenu des décisions des autres. 

&nbsp;

---