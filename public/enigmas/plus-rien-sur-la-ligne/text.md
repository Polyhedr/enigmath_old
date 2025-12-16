## Énoncé


On considère une ligne infinie de cases indexées par les entiers relatifs
$\mathbb{Z}\triangleq\{
\dots, -2, -1, 0, 1, 2, \dots \}
$, initialement avec un seul jeton sur la case $0$, toutes les autres étant vides.
Au cours du jeu, chaque case peut contenir une pile quelconque de jetons, et l'objectif est de retirer tous les jetons de la ligne en appliquant une suite d'actions autorisées.  

Une action $A$ est définie comme une transformation appliquée à une portion de la ligne, que l'on note
$$
\begin{align*}
A\triangleq(a_0, \dots, a_k) 
\longleftrightarrow  (a'_0, \dots, a'_k),
\end{align*}
$$
où $k \in \mathbb{N},$ $a_0, \dots, a_k,a'_0, \dots, a'_k \in \mathbb{N}$ et $(a_0, \dots, a_k)\neq (a'_0, \dots, a'_k)$. Pour $i\in\mathbb Z$, appliquer $A$ sur les $k+1$ cases consécutives d'indices $i,\dots,i+k$ signifie qu'on retire $a_j$ jetons de la case $i+j$ et qu'on ajoute $a'_j$ jetons à la même case, pour tout $0\le j\le k$. L'opération n'est permise que si chaque case $i+j$ contient au moins $a_j$ jetons, suffisants pour effectuer les retraits requis (aucun nombre négatif de jetons n'est autorisé, même temporairement). L'action $A$ peut également être effectuée dans le sens inverse en échangeant les $a_j$ et les $a'_j$.





**Questions :**

1. 🌶️${}^{\color{red}0.4}$ Résolvez le jeu en utilisant les deux actions autorisées&nbsp;:
    $$
    \begin{align*}
    & A\triangleq(1,3,1,0,0) \longleftrightarrow (0,2,1,1,2) \\& \text{et} \\& B\triangleq(0,0) \longleftrightarrow (1,1).
    \end{align*}
    $$

2. 🌶️${}^{\color{red}0.5}$ Montrez que, pour que le jeu soit résoluble, il est nécessaire qu'une des actions autorisées ait un côté constitué uniquement de zéros.

3. 🌶️${}^{\color{red}0.7}$ Avec les deux actions
    $$
    \begin{align*}
    A\triangleq(1,0,0,0) \longleftrightarrow (0,1,1,1) \quad \text{et} \quad B\triangleq(0,0) \longleftrightarrow (1,1),
    \end{align*}
    $$
    le jeu est-il résoluble&nbsp;? 

4. 🌶️${}^{\color{red}1.0}$ Avec les deux actions
    $$
    \begin{align*}
    A\triangleq(1,0,0,0,0,0) \longleftrightarrow (0,1,1,1,1,1) \quad \text{et} \quad B\triangleq(0,0,0) \longleftrightarrow (1,1,1),
    \end{align*}
    $$
    le jeu est-il résoluble&nbsp;? 

5. 🌶️${}^{\color{red}1.5}$ 
À chaque action
    $$
    \begin{align*}
    A\triangleq(a_0, \dots, a_k) \longleftrightarrow (a'_0, \dots, a'_k)
    \end{align*}
    $$
    on associe le polynôme
    $$
    \begin{align*}
    A(X) \triangleq \sum_{j=0}^k (a'_j - a_j) X^{j} \in \mathbb{Z}[X].
    \end{align*}
    $$
    Montrez que, pour que le jeu soit résoluble, il est nécessaire et suffisant qu'au moins une des actions autorisées ait un côté constitué uniquement de zéros, et que l'idéal de $\mathbb{Z}[X]$ engendré par les polynômes associés aux actions autorisées
    contienne une puissance de $X$. 

6. 🌶️${}^{\color{red}1.5}$ On suppose que les coefficients constants des polynômes associés aux actions autorisées 
sont premiers entre eux dans leur ensemble. 
Trouvez alors une condition nécessaire et suffisante plus forte que la précédente.

7. 🌶️${}^{\color{red}1.9}$ On suppose maintenant qu'il y a exactement deux actions, 
auxquelles on associe les polynômes $P$ et $Q$, 
avec l'un des deux à coefficients positifs et correspondant à une action dont un côté est le vecteur nul.  
On suppose que $P(0)$ et $Q(0)$ sont premiers entre eux, 
et que le coefficient dominant de l’un des polynômes $P$ ou $Q$ appartient à $\{\pm 1\}$.  Montrez alors qu’une condition nécessaire et suffisante de résolubilité du jeu 
est que le résultant 
$
\operatorname{Res}(P,Q)
$
soit égal à $\pm 1$.

8. 🌶️${}^{\color{red}2.4}$ Soient $P$ et $Q$ deux polynômes de $\mathbb Z[X]$ dont les coefficients sont croissants,  
avec $P$ à coefficients positifs et $Q$ à coefficients négatifs.
On suppose que le coefficient dominant de $P$ est strictement supérieur à $1$, 
et que le coefficient dominant de $Q$ est égal à $-1$.  
Montrez que le jeu associé aux polynômes $P(X)$ et $1 + XQ(X)$
n'est pas résoluble.

9. 🌶️${}^{\color{red}1.9}$ Soient 
$
a=(1,0,\dots,0)\in \{0,1\}^{q+1} 
$ et $
b=(0,\dots,0)\in \{0,1\}^{p}.
$
Avec les deux actions
    $$
    \begin{align*}
    & A \triangleq a \longleftrightarrow 1-a 
    \\& \text{et} \\& 
    B \triangleq b \longleftrightarrow 1-b,
    \end{align*}
    $$
    montrez que le jeu est résoluble si et seulement si $p$ divise $q$.

10. 🌶️${}^{\color{red}1.5}$ On considère une grille infinie de cases indexées par les paires $(i,j) \in \mathbb{Z} \times \mathbb{Z}$.  
Initialement, un unique jeton est placé en $(0,0)$, toutes les autres cases étant vides.  
On définie une action $A$ par
    $$
    \begin{align*}
    A \triangleq 
    \begin{bmatrix}
    a_{00} & \cdots & a_{0k} \\
    \vdots & \ddots & \vdots \\
    a_{k0} & \cdots & a_{kk}
    \end{bmatrix}
    \longleftrightarrow
    \begin{bmatrix}
    a'_{00} & \cdots & a'_{0k} \\
    \vdots & \ddots & \vdots \\
    a'_{k0} & \cdots & a'_{kk}
    \end{bmatrix}.
    \end{align*}
    $$
    Trouvez une condition nécessaire et suffisante pour que le jeu soit résoluble dans cette grille bidimensionnelle, en fonction de l’ensemble d’actions autorisées.

11. 🌶️${}^{\color{red}1.4}$ Avec les deux actions (de taille non nécessairement égale)
    $$
    \begin{align*}
    & A \triangleq 
    \begin{bmatrix}
    0 & 0 &\cdots & 0 \\
    1 & 0 &\cdots & 0
    \end{bmatrix}
    \longleftrightarrow
    \begin{bmatrix}
    1 & 1 &\cdots & 1 \\
    0 & 0 &\cdots & 0
    \end{bmatrix}
    \\& \text{et} \\& 
    B \triangleq  \begin{bmatrix}
    0 &\cdots & 0
    \end{bmatrix}
    \longleftrightarrow
    \begin{bmatrix}
    1 & \cdots & 1 
    \end{bmatrix},
    \end{align*}
    $$
    le jeu est-il résoluble&nbsp;?



&nbsp;

---