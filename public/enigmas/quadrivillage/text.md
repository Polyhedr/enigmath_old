## Énoncé


Le village de Quadrivillage est organisé selon un quadrillage de rues.  
À certaines intersections se trouve une maison, pour un total de $n$ maisons dans le village (chaque maison abrite exactement un habitant).  
Le maire souhaite construire une Grande Allée : une route traversant le village en ligne droite, de façon oblique.  
Son objectif est de placer cette route de manière à réduire au maximum le temps de trajet des habitants pour s’y rendre.




**Questions :**

1. 🌶️${}^{\color{red}0.4}$ En supposant que les habitants se déplacent uniquement le long des rues du quadrillage, 
déterminez, pour une Grande Allée donnée, le temps de trajet d'un habitant jusqu'à celle-ci. 

2. 🌶️${}^{\color{red}2.1}$ Proposez un algorithme en temps  quasi-quadratique en $n$, 
permettant de déterminer la position optimale de la Grande Allée, 
de manière à minimiser la somme des temps de trajet de tous les habitants 
jusqu’à celle-ci.

3. 🌶️${}^{\color{red}2.5}$ Avant le début de la construction, plusieurs villages voisins (organisés eux aussi en quadrillage) souhaitent 
bâtir leur Grande Allée selon le même objectif. Cependant, selon la tradition locale, toutes ces Grandes Allées doivent  
être parallèles entre elles. Les maires se réunissent donc pour déterminer conjointement la position optimale 
de chaque Grande Allée. Si l'on considère $d$ villages et $n$ habitants par village, décrivez un algorithme  
de complexité $\mathcal O(dn^2\log(dn))$ permettant de résoudre ce problème de minimisation. 



&nbsp;

---