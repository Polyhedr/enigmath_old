## Énoncé


Vous avez été enfermés dans une prison formant un anneau parfait de $n$ cellules (vous ne connaissez pas $n$), toutes identiques, isolées, et chacune contenant exactement un prisonnier.
Dans chaque cellule se trouvent un interrupteur et une ampoule, mais le câblage a été manifestement conçu par un ingénieur fou.
Si, à midi pile, l’interrupteur d'une cellule est en position "on", alors l’ampoule de la cellule voisine (dans le sens horaire) émet un bref flash. Sinon, la lampe reste éteinte.

Afin d’empêcher toute forme de communication, chaque nuit à minuit, le gardien diffuse du gaz anesthésiant dans tout l’anneau, remet tous les interrupteurs sur "off", et réarrange les prisonniers comme bon lui semble. Mais il garde une règle immuable&nbsp;: une personne par cellule.

Un jour, le gardien entre dans votre cellule et vous lance un défi. Pour gagner votre liberté — et celle de tous les autres — une seule règle&nbsp;:
à n’importe quel moment, n’importe quel prisonnier peut crier "Nous sommes $n$ prisonniers&nbsp;!"
S’il dit vrai&nbsp;: tout le monde est libre.
S’il se trompe&nbsp;: tout le monde est exécuté.

Le gardien vous autorise à envoyer un unique message écrit à tous les autres prisonniers, dans lequel vous pouvez expliquer les règles et proposer un plan. Eux n’ont pas le droit de répondre.
Naturellement, le gardien lira soigneusement votre note... et ensuite, il mélangera les prisonniers autant que nécessaire pour tenter de faire échouer votre stratégie.




**Questions :**

1. 🌶️${}^{\color{red}2.2}$ On admet que les prisonniers peuvent lancer des pièces, ce qui leur permet de prendre des décisions aléatoires que le gardien ne peut pas prévoir, même s’il connaît leur stratégie. Décrivez une stratégie permettant aux prisonniers de déterminer $n$ (presque sûrement).

2. 🌶️${}^{\color{red}2.9}$ Donnez une solution qui n’utilise aucune forme d’aléatoire et qui garantit d’aboutir en un nombre déterminé de jours.

3. 🌶️${}^{\color{red}3.0}$ On suppose que la prison n’est plus circulaire, mais forme un graphe orienté fortement connexe, chaque cellule contenant au moins un interrupteur et une lumière, et chaque lumière étant contrôlée par exactement un interrupteur situé dans une autre cellule. Décrivez une stratégie permettant aux prisonniers de déterminer $n$.



&nbsp;

---