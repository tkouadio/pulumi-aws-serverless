# 🚀 Infrastructure as Code avec Pulumi – Serverless AWS (CI/CD)

## 📌 Contexte

Ce projet est réalisé dans le cadre d’un **cours DevOps (MGL869)** à la **maîtrise en génie logiciel**.
Il a pour objectif de démontrer concrètement les principes de **Infrastructure as Code (IaC)** et de **CI/CD** à l’aide de **Pulumi** et d’**AWS**.

Le projet illustre la chaîne DevOps complète :

> **commit → pipeline CI/CD → infrastructure cloud déployée automatiquement**

## 🎯 Objectifs du projet

* Décrire une infrastructure cloud **entièrement en code** (Python).
* Déployer automatiquement l’infrastructure via un **pipeline CI/CD**.
* Mettre en œuvre une architecture **serverless** moderne.
* Comparer implicitement l’approche Pulumi avec Terraform et Ansible (présentés par d’autres membres de l’équipe).

## 🏗️ Architecture déployée

L’infrastructure AWS créée par Pulumi comprend :

* **API Gateway (HTTP API)**
  → Expose une API REST publique.
* **AWS Lambda (Python)**
  → Traite les requêtes HTTP GET / POST.
* **DynamoDB**
  → Stockage NoSQL des messages.
* **IAM Roles & Policies**
  → Sécurité selon le principe du moindre privilège.

L’ensemble est déployé et détruit automatiquement par **Pulumi via GitHub Actions**.

## ⚙️ Technologies utilisées

* **Pulumi** (IaC)
* **Python 3.11**
* **AWS** : Lambda, API Gateway, DynamoDB, IAM
* **GitHub Actions** (CI/CD)
* **Pulumi Cloud** (state backend & stack management)

## 📁 Structure du projet

- app/
  - lambda_handler.py          # Code de la fonction Lambda
- __main__.py                  # Définition de l’infrastructure Pulumi
- Pulumi.yaml                  # Configuration du projet Pulumi
- requirements.txt             # Dépendances Python
- .github/
  - workflows/
    - deploy.yml               # Pipeline CI/CD de déploiement
    - destroy.yml              # Pipeline CI/CD de destruction
- README.md


## 🔁 Workflow CI/CD

### Déploiement automatique

Le pipeline **deploy.yml** est déclenché à chaque `push` sur la branche `main` :

1. Checkout du code
2. Installation de Python et des dépendances
3. Configuration des credentials AWS
4. Sélection / création du stack Pulumi (`dev`)
5. Définition de la région AWS
6. Exécution de `pulumi up`

➡️ L’infrastructure est automatiquement **créée ou mise à jour**.

### Destruction de l’infrastructure

Le pipeline **destroy.yml** est déclenché manuellement (`workflow_dispatch`) :

* Exécution de `pulumi destroy`
* Suppression complète des ressources AWS
* Le **stack Pulumi reste présent**, mais sans ressources (comportement normal)

## 📤 Outputs Pulumi

Après un déploiement réussi, Pulumi expose les outputs suivants :

* **endpoint_url** : URL publique de l’API Gateway
* **table_name** : Nom de la table DynamoDB créée

Ces outputs sont visibles :

* dans les logs du pipeline CI/CD
* dans l’interface **Pulumi Cloud**


## 🧪 Tester l’API

### GET – Lire les données

```bash
curl https://<endpoint_url>
```

### POST – Ajouter un message

```bash
curl -X POST https://<endpoint_url>
```

Les données sont stockées dans DynamoDB et retournées via l’API.

## 🔐 Gestion des secrets

Les secrets sont gérés via :

* **GitHub Secrets** :

  * `AWS_ACCESS_KEY_ID`
  * `AWS_SECRET_ACCESS_KEY`
  * `PULUMI_ACCESS_TOKEN`
* **Pulumi Config** pour la configuration de la région AWS

Aucun secret n’est stocké en clair dans le dépôt.

## 💡 Pourquoi Pulumi ?

* Utilisation de **langages de programmation complets** (Python)
* Logique impérative (conditions, fonctions, boucles)
* **Multi-cloud**
* Intégration native avec les pipelines CI/CD
* Approche “**Infrastructure as Software**”

## 📚 Apports pédagogiques

Ce projet démontre :

* la reproductibilité des infrastructures cloud
* l’automatisation complète du cycle de vie
* la convergence entre **développement logiciel** et **infrastructure**
* les bonnes pratiques DevOps modernes

👤 Auteur
Thierry Kouadio
Maîtrise en génie logiciel
Projet académique – DevOps / Infrastructure as Code
