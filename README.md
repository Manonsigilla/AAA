# Challenge Triple A - Dashboard de Monitoring

## 📋 Description

Outil de monitoring système avec dashboard web qui affiche en temps réel les statistiques d'une machine virtuelle Linux (Ubuntu).

**Challenge Triple A** combine trois compétences :
- **Administration** : Gestion d'une machine virtuelle Linux
- **Algorithmique** : Développement Python pour la collecte de données système
- **Affichage** : Création d'une interface web avec HTML5/CSS3

## 🎯 Fonctionnalités

### Informations collectées : 
- ✅ **Système** :  Nom de la machine, système d'exploitation, uptime, nombre d'utilisateurs connectés
- ✅ **CPU** : Nombre de cœurs, fréquence, pourcentage d'utilisation
- ✅ **Mémoire** : RAM totale/utilisée/pourcentage avec barres de progression visuelles
- ✅ **Réseau** : Adresse IP principale
- ✅ **Processus** : Top 3 des processus les plus gourmands en ressources
- ✅ **Fichiers** : Analyse et statistiques sur les types de fichiers (. txt, .py, .pdf, .jpg)

### Interface web moderne :
- 🎨 Design moderne avec sidebar navigation
- 📊 Visualisations avec gauges circulaires et barres de progression
- 🌓 Thème sombre avec couleurs cyan/teal
- 📱 Interface responsive

## 🛠️ Prérequis

- **Python** 3.8 ou supérieur
- **Module Python** :  `psutil`
- **Système d'exploitation** : Ubuntu 22.04 LTS (ou version plus récente) / Windows 10+
- **Navigateur web** : Firefox, Chrome, Edge ou équivalent

## 📥 Installation

### 1. Cloner le repository

```bash
git clone https://github.com/votre-nom/Challenge-AAA.git
cd Challenge-AAA
```

### 2. Installer les dépendances

**Sur Ubuntu/Linux :**

```bash
sudo apt update
sudo apt install python3-pip
sudo apt install python3-psutil
```

Ou avec pip :

```bash
pip3 install psutil
```

**Sur Windows :**

```bash
pip install psutil
```

**Avec Conda :**

```bash
conda install psutil
```

## 🚀 Utilisation

### 1. Lancer le script de monitoring

```bash
python3 monitor.py
```

**Sortie attendue :**

```
🖥️  Challenge Triple A - System Monitor
==================================================
Collecting system information... 
📊 Collecting system info... 
⚙️  Collecting CPU info... 
🧠 Collecting memory info... 
🌐 Collecting network info... 
📈 Collecting process info...
   ⏳ Measuring CPU usage (this takes a moment)...
📁 Analyzing files... 
🎨 Generating HTML dashboard...
✅ index.html generated successfully!
==================================================
✨ Done! Open index.html in your browser to view the dashboard. 
```

### 2. Ouvrir le dashboard dans le navigateur

**Sur Linux :**

```bash
firefox index.html
```

ou

```bash
xdg-open index.html
```

**Sur Windows :**

```bash
start index.html
```

Le fichier `index.html` est généré automatiquement avec les données système collectées en temps réel.

## 📂 Structure du projet

```
Challenge-AAA/
├── README.md              ← Documentation du projet
├── monitor.py             ← Script Python principal
├── template.html          ← Template HTML avec variables
├── template.css           ← Feuille de style
├── index.html             ← HTML généré (créé après exécution)
├── screenshots/           ← Captures d'écran
│   ├── terminal. png
│   └── dashboard.png
└── . gitignore             ← Fichiers à ignorer par Git
```

## 🎨 Personnalisation

### Changer le dossier analysé

Dans `monitor.py`, ligne ~273, modifiez : 

```python
analyze_directory = "~/Documents"  # Changez ce chemin
```

### Modifier les couleurs (thème)

Dans `template.css`, modifiez les variables CSS :

```css
:root {
    --primary-color: #00d4aa;     /* Couleur principale */
    --secondary-color:  #0ea5e9;   /* Couleur secondaire */
    --bg-primary:  #0a0e27;        /* Fond principal */
}
```

## 📊 Captures d'écran

*Les captures d'écran seront ajoutées prochainement.. .*

## 🔧 Difficultés rencontrées

- Configuration de la machine virtuelle avec les bonnes ressources
- Gestion des permissions pour l'accès aux informations système
- Mesure précise du CPU sur Windows (processus "System Idle")
- Templating HTML/Python avec remplacement de variables
- Adaptation cross-platform (Windows/Linux)

## 🚀 Améliorations possibles

### Fonctionnalités : 
- [ ] Rafraîchissement automatique toutes les 30 secondes
- [ ] Code couleur pour les niveaux d'utilisation (vert/orange/rouge)
- [ ] Analyse système avancée (load average)
- [ ] Pourcentage d'utilisation par cœur CPU
- [ ] Analyse récursive complète des fichiers
- [ ] Calcul de l'espace disque par type de fichier
- [ ] Graphiques d'historique des performances
- [ ] Export des données en JSON/CSV
- [ ] Alertes par email si seuils dépassés
- [ ] Dashboard multi-machines

### Interface :
- [ ] Thème de Noël (rouge/vert/or)
- [ ] Mode clair/sombre
- [ ] Graphiques interactifs avec Chart.js
- [ ] Animation des transitions

## 👥 Auteurs

- **[Nom Membre 1]** - [GitHub](https://github.com/membre1)
- **[Nom Membre 2]** - [GitHub](https://github.com/membre2)
- **[Nom Membre 3]** - [GitHub](https://github.com/membre3)

## 🎓 Contexte

Projet réalisé dans le cadre de la formation **[Nom de votre école/formation]**.

**Date** : Décembre 2025

**Compétences développées** :
- Virtualisation (VMware Workstation Pro 17)
- Administration système Linux (Ubuntu)
- Développement Python
- Web design (HTML5/CSS3)
- Gestion de version (Git/GitHub)

## 📄 Licence

Ce projet est réalisé dans un cadre éducatif. 

---

**© 2025 Challenge Triple A Team** - Made with ❤️ and ☕
