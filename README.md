Push
```
git init; git add .; git commit -m "Initial commit: enigmas processing + tags.txt"; git push origin main

```

Pull
```
git pull origin main
```

Voici les étapes à suivre pour soumettre votre énigme :

1. **Édition de l’énigme**

    Commencez par éditer le fichier `/enigmas/l-enigme-de-freudenthal/text.tex`.

    Vous pouvez aussi :
    - modifier l’image associée à l’énigme : `/enigmas/l-enigme-de-freudenthal/image.jpg`
    - inclure du code Python :
        - `1.py` pour la question 1,
        - `2.py` pour la question 2, etc.
        - si plusieurs fichiers de code correspondent à une même question, utilisez par exemple `2a.py`, `2b.py` pour la question 2.

    Dans le fichier `.tex`, le code Python doit être inclus avec la syntaxe suivante :

    ```latex
    \begin{lstlisting}
    (*@\codeheader{\currfiledir/1.py}@*)
    (*@ @*)
    \end{lstlisting}
    \vspace{-.455cm}
    \lstinputlisting{\currfiledir/1.py}
    ```
    Pour chaque question, n’oubliez pas de spécifier les indices de **difficulté** et d’**exigence en calcul** (valeurs $x$ comprises entre 0 et 5) à l’aide de `\indicators{DIFFICULTE}{EXIGENCE_CALCUL}`.
    Ces indices sont affichés avec les symboles suivants :

    - 🌶️${}^x$ : **indice de difficulté** (avec $x \in [0,5]$)
        - $x < 1$ : facile  
        - $x \in [1,2]$ : moyen  
        - $x \in [2,3]$ : difficile  
        - $x \in [3,4]$ : très difficile  
        - $x \in [4,5]$ : niveau recherche  

    - 💻${}^x$ : **indice d’exigence en calcul** (avec $x \in [0,5]$)
        - $x < 1$ : l’ordinateur peut aider, mais la résolution reste possible entièrement à la main  
        - $x \in [1,2]$ : code élémentaire  
        - $x \in [2,3]$ : code plutôt avancé  
        - $x \in [3,4]$ : code très difficile  
        - $x \in [4,5]$ : code reposant sur des algorithmes de niveau recherche 

2. **Renommage du dossier**

    Une fois l’énigme éditée, vous pouvez renommer le dossier `l-enigme-de-freudenthal`.

    Pour de bonnes pratiques, limitez-vous aux caractères suivants :
    - lettres (`a–z`, `A–Z`)
    - chiffres (`0–9`)
    - tirets (`-`)

3. **Titre et tags**

    Modifiez le titre de l’énigme dans le fichier `.tex`.
    
    Ajoutez des tags en haut du fichier pour catégoriser l’énigme, par exemple :

    ```latex
    % logique épistémique
    % arithmétique
    \section*{TITRE DE MON ÉNIGME}
    ```

4. **Références**

    Incluez des références relatives à l’énigme dans la sous-section :

        ```latex
        \subsection*{Notes et références}
        ```

    Citez vos sources en ajoutant la ligne suivante dans le fichier `.tex` :

        ```latex
        \bibliography{\currfiledir/sources.bib}
        ```

5. **Compilation**

    Revenez dans le dossier racine parent et modifiez `solution.tex`, en mettant à jour la ligne :

        ```latex
        \input{enigmas/l-enigme-de-freudenthal/text.tex}
        ```

        afin d’inclure la version correcte de votre énigme.

    Lancez ensuite les commandes suivantes dans votre terminal :

        ```bash
        lualatex solution
        bibtex solution
        lualatex solution
        lualatex solution
        ```

    Cela générera le fichier `solution.pdf`. Copiez-le dans le dossier de votre énigme, zippez ce dossier, et envoyez-le par mail à **contact.enigmath@proton.me**.