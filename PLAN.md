# PLAN.md

## 1. Objectif du projet

Le but du projet est de réaliser et tester le micro-service **Triangulator**.

Le Triangulator reçoit un `PointSetID`, récupère le `PointSet` correspondant auprès du `PointSetManager`, calcule la triangulation, puis renvoie les triangles au client.

Notre objectif principal est de mettre en place des tests pertinents avant de terminer l'implémentation, dans une démarche **test first**.

Les tests devront vérifier :
- la conversion des données binaires ;
- le calcul de la triangulation ;
- le comportement de l'API ;
- la gestion des erreurs ;
- les performances ;
- la couverture et la qualité du code.

---

## 2. Organisation des tests

Nous prévoyons plusieurs niveaux de tests :

- **Tests unitaires** : tester chaque partie du programme séparément.
- **Tests d'API / intégration** : vérifier le comportement du service dans son ensemble.
- **Tests de performance** : mesurer le temps de calcul sur différentes tailles de données.

Les tests de performance seront séparés des autres tests pour pouvoir les lancer indépendamment.

---

## 3. Tests de la représentation binaire `PointSet`

Le `PointSet` est représenté en binaire avec :

- 4 octets pour le nombre de points ;
- 8 octets par point ;
- 4 octets pour `X` et 4 octets pour `Y`.

### Tests prévus

Nous allons tester :

1. Un ensemble vide de points.
2. Un ensemble avec un seul point.
3. Un ensemble avec plusieurs points.
4. Des coordonnées positives.
5. Des coordonnées négatives.
6. Des coordonnées décimales.
7. La conversion d'un `PointSet` Python vers le format binaire.
8. La conversion du binaire vers le format Python.
9. La conservation des coordonnées après encodage puis décodage.
10. Les données trop courtes ou incomplètes.
11. Un nombre de points incohérent avec la taille des données.

Le but est de vérifier que les échanges binaires sont corrects et que les données invalides sont correctement détectées.

---

## 4. Tests de la représentation binaire `Triangles`

La structure `Triangles` contient :

- la liste des sommets, au même format qu'un `PointSet` ;
- le nombre de triangles ;
- pour chaque triangle, trois indices de sommets.

### Tests prévus

Nous allons tester :

1. Aucun triangle.
2. Un seul triangle.
3. Plusieurs triangles.
4. La bonne conservation des sommets.
5. Le bon nombre de triangles.
6. Des indices de sommets valides.
7. La conversion Python -> binaire.
8. La conversion binaire -> Python.
9. La conservation des données après encodage puis décodage.
10. Les données binaires incomplètes ou incohérentes.
11. Des indices qui ne correspondent pas à un sommet existant.

Le but est de vérifier que le résultat produit par le Triangulator peut être correctement envoyé au client.

---

## 5. Tests du calcul de triangulation

Le calcul de triangulation sera testé séparément du reste du programme.

Nous commencerons par des cas simples avec un résultat facile à prévoir.

### Cas prévus

1. **Moins de 3 points**
   - 0 point ;
   - 1 point ;
   - 2 points.

   Aucun triangle ne doit être possible.

2. **Trois points non alignés**
   - on attend un triangle.

3. **Quatre points formant un carré**
   - on attend une triangulation du carré en deux triangles.

4. **Plusieurs points**
   - vérifier que les triangles obtenus utilisent uniquement les sommets fournis.

5. **Points colinéaires**
   - vérifier le comportement du programme lorsqu'aucun triangle valide ne peut être formé.

6. **Points en double**
   - vérifier que le programme ne produit pas de triangle dégénéré ou de résultat incohérent.

7. **Cas avec des coordonnées négatives et décimales**
   - vérifier que le calcul fonctionne aussi avec des coordonnées variées.

### Vérifications générales

Pour chaque résultat, nous vérifierons notamment :

- que les indices des triangles sont valides ;
- qu'un triangle ne référence pas un sommet inexistant ;
- que les triangles produits correspondent aux points fournis ;
- que le programme ne plante pas sur les cas limites.

---

## 6. Tests de communication avec le `PointSetManager`

Le Triangulator dépend du `PointSetManager` pour récupérer les points.

Nous allons donc tester plusieurs réponses possibles du `PointSetManager`.

### Cas prévus

- réponse `200` avec un `PointSet` valide ;
- réponse `404` si le `PointSetID` n'existe pas ;
- réponse `400` si la requête est invalide ;
- réponse `503` si le stockage du `PointSetManager` est indisponible ;
- absence de réponse / problème de communication ;
- réponse avec des données invalides.

Pour ces tests, nous utiliserons un faux service ou des réponses simulées afin de tester le Triangulator sans dépendre en permanence d'un vrai `PointSetManager`.

---

## 7. Tests de l'API du Triangulator

L'endpoint principal est :

`GET /triangulation/{pointSetId}`

Nous allons tester les différents codes de réponse prévus dans l'API.

### Cas de succès

### `200 OK`

Avec un `PointSetID` valide et un `PointSet` valide :

- la réponse doit avoir le code HTTP `200` ;
- le contenu doit être en `application/octet-stream` ;
- le résultat doit respecter le format binaire `Triangles`.

### Cas d'erreur

#### `400 Bad Request`

Tester un `PointSetID` avec un format invalide.

#### `404 Not Found`

Tester le cas où le `PointSetID` est valide mais n'existe pas dans le `PointSetManager`.

#### `500 Internal Server Error`

Tester une erreur provenant du calcul de triangulation.

#### `503 Service Unavailable`

Tester un problème de communication avec le `PointSetManager`.

Pour les erreurs, nous vérifierons aussi que la réponse contient un objet JSON avec :

- `code`
- `message`

---

## 8. Tests bout en bout

Nous voulons également tester le scénario complet :

1. Un `PointSet` est disponible dans le `PointSetManager`.
2. Le client appelle le Triangulator avec son `PointSetID`.
3. Le Triangulator récupère le `PointSet`.
4. Le Triangulator calcule la triangulation.
5. Le Triangulator renvoie le résultat binaire.
6. Le résultat est décodé et vérifié.

Cela permettra de vérifier que les différentes parties fonctionnent correctement ensemble.

---

## 9. Tests de performance

Les tests de performance devront mesurer principalement :

- le temps de décodage d'un `PointSet` ;
- le temps d'encodage d'un résultat `Triangles` ;
- le temps de calcul de la triangulation.

Nous utiliserons plusieurs tailles de jeux de points, par exemple :

- petite taille ;
- taille moyenne ;
- grande taille.

Le but est de comparer le comportement du programme quand le nombre de points augmente.

Ces tests seront séparés des tests classiques pour pouvoir les lancer uniquement avec :

`make perf_test`

---

## 10. Couverture des tests

Nous utiliserons `coverage` pour mesurer la couverture du code.

Objectif :

- couvrir toutes les parties importantes du code ;
- notamment les cas normaux et les cas d'erreur ;
- éviter de chercher uniquement un pourcentage élevé sans vérifier la pertinence des tests.

La commande prévue sera :

`make coverage`

---

## 11. Qualité du code et documentation

Nous utiliserons `ruff` avec les règles définies dans `pyproject.toml`.

Nous vérifierons en particulier :

- la qualité générale du code ;
- les imports ;
- les erreurs courantes ;
- la documentation des fonctions et classes.

La commande prévue sera :

`make lint`

La documentation sera générée avec `pdoc3` avec :

`make doc`

---

## 12. Commandes `make`

Le projet devra fournir les commandes suivantes :

- `make test` : tous les tests ;
- `make unit_test` : tous les tests sauf les tests de performance ;
- `make perf_test` : uniquement les tests de performance ;
- `make coverage` : rapport de couverture ;
- `make lint` : vérification avec `ruff` ;
- `make doc` : génération de la documentation.

---

## 13. Évolution prévue du plan

Ce plan sera notre base de départ pour le développement.

Il pourra être modifié si nous découvrons, pendant l'implémentation, des cas supplémentaires ou des problèmes qui n'avaient pas été prévus.

L'idée est cependant de commencer l'implémentation avec une stratégie de test déjà définie.
