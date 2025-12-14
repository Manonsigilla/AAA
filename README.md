# 🎄 Challenge Triple A - Dashboard de Monitoring Système

<div align="center">

![HTML](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white)
![CSS](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)

**Dashboard de monitoring système en temps réel avec interface web moderne et thème de Noël** 🎅

[Fonctionnalités](#-fonctionnalités) • [Installation](#-installation) • [Utilisation](#-utilisation) • [Structure](#-structure-du-projet)

</div>

---

## 📋 Description

**Challenge Triple A** est un outil de monitoring système qui collecte et affiche en temps réel les statistiques d'une machine (Linux/Windows) via une interface web élégante et interactive.

Le projet combine trois compétences essentielles :
- **🔧 Administration** : Gestion et monitoring système
- **🧮 Algorithmique** : Collecte de données avec Python
- **🎨 Affichage** : Interface web moderne et responsive

## ✨ Fonctionnalités

### 📊 Informations Système Collectées

| Catégorie | Données |
|-----------|---------|
| **Système** | Nom machine, OS, uptime, utilisateurs connectés |
| **CPU** | Nombre de cœurs, fréquence, utilisation globale et par cœur |
| **Mémoire** | RAM totale/utilisée/disponible avec visualisation |
| **Réseau** | Adresse IP principale |
| **Processus** | Top 3 + liste complète des processus par utilisation |
| **Fichiers** | Analyse par type (`.txt`, `.py`, `.pdf`, `.jpg`, etc.) |
| **Load Average** | Charge système sur 1, 5 et 15 minutes (Linux) |

### 🎨 Interface Web Moderne

- ✅ **Design responsive** adapté à tous les écrans
- ✅ **Sidebar navigation** avec navigation fluide
- ✅ **Thème sombre** cyan/teal par défaut
- ✅ **Thème de Noël** 🎄 avec animation de flocons de neige
- ✅ **Horloge temps réel** mise à jour en direct
- ✅ **Visualisations** :  gauges circulaires, barres de progression
- ✅ **Animations** : transitions fluides et effets visuels
- ✅ **Export JSON** des données collectées

### 🎅 Thème de Noël

- 🎄 Palette de couleurs festives (rouge, vert, or)
- ❄️ Animation de flocons de neige
- 🌟 Effets de glow et transitions spéciales
- 🔄 Basculement thème en un clic

## 🛠️ Prérequis

- **Python** 3.8+ 
- **Module Python** :  `psutil`
- **Système d'exploitation** : Ubuntu 22.04+ / Windows 10+
- **Navigateur web** : Firefox, Chrome, Edge ou Safari

## 📥 Installation

### 1. Cloner le repository

```bash
git clone https://github.com/Manonsigilla/AAA. git
cd AAA
```

### 2. Installer les dépendances Python

**Sur Ubuntu/Linux :**

```bash
sudo apt update
sudo apt install python3-pip python3-psutil
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

**Sortie console :**

```
============================================================
  Challenge Triple A - System Monitor
============================================================
[>>] Collecting system information... 

[>>] Collecting system info...
[>>] Collecting load average...
[>>] Collecting CPU info...
[>>] Collecting memory info...
[>>] Collecting network info...
[>>] Collecting process info...
   [INFO] Measuring CPU usage (this takes a moment)...
[>>] Analyzing files...
   [>>] Scanning:  /home/user/Documents
   [OK] Total files scanned: 1523
   [OK] Found:  342 matching files

[>>] Saving data to JSON... 
[OK] system_data.json generated successfully! 
[>>] Generating HTML dashboard...
[OK] index.html generated successfully! 

============================================================
[OK] Done! Open index.html in your browser to view the dashboard.
[>>] HTML file:  /path/to/AAA/index.html
[>>] JSON file: /path/to/AAA/system_data.json
============================================================
```

### 2. Ouvrir le dashboard

**Sur Linux :**

```bash
firefox index.html
# ou
xdg-open index.html
```

**Sur Windows :**

```bash
start index.html
```

**Sur macOS :**

```bash
open index.html
```

### 3. Basculer vers le thème de Noël 🎄

Cliquez sur le bouton flottant en bas à droite pour activer/désactiver le thème de Noël avec ses animations de flocons ! 

## 📂 Structure du Projet

```
AAA/
├── 📄 README.md                  # Documentation du projet
├── 🐍 monitor.py                 # Script Python principal de collecte
├── 🌐 template.html              # Template HTML avec variables
├── 🎨 template.css               # Feuille de style principale
├── 🎄 christmas-theme.css        # Thème de Noël
├── ⚡ dashboard.js               # JavaScript interactif
├── 📄 index.html                 # HTML généré (créé après exécution)
├── 📊 system_data.json           # Données système en JSON
├── 🖼️ assets/                    # Ressources (images, icônes)
├── 🚫 . gitignore                 # Fichiers ignorés par Git
└── ⚙️ . hintrc                    # Configuration Webhint
```

## 🎨 Personnalisation

### Changer le dossier analysé

Dans `monitor.py`, lignes 395-402 :

```python
# Windows
analyze_directory = os.path.join(os.path.expanduser("~"), "Documents")

# Linux/macOS
analyze_directory = os.path.expanduser("~/Documents")
```

### Modifier les couleurs du thème par défaut

Dans `template.css`, modifiez les variables CSS :

```css
:root {
    --primary-color: #00d4aa;      /* Cyan principal */
    --secondary-color:  #0ea5e9;     /* Bleu secondaire */
    --bg-primary: #0a0e27;          /* Fond sombre */
}
```

### Personnaliser le thème de Noël

Dans `christmas-theme.css` :

```css
:root. christmas-theme {
    --christmas-red: #c41e3a;
    --christmas-green: #2d5f3f;
    --christmas-gold:  #e8b86d;
}
```

## 🔧 Architecture Technique

### Backend (Python)

- **`monitor.py`** : Script principal avec 8 fonctions de collecte
  - `get_system_info()` : Informations système de base
  - `get_cpu_info()` : Statistiques CPU détaillées
  - `get_memory_info()` : Utilisation RAM
  - `get_network_info()` : Configuration réseau
  - `get_load_average()` : Charge système (Linux)
  - `get_processes()` : Liste et classement des processus
  - `analyze_files()` : Analyse récursive des fichiers
  - `generate_html()` : Génération du dashboard

### Frontend

- **HTML5** : Structure sémantique avec template variables
- **CSS3** :  Animations, grids, flexbox, variables CSS
- **Vanilla JavaScript** : Interactivité sans framework
  - Horloge temps réel
  - Animations des barres de progression
  - Navigation fluide
  - Basculement de thème

## 🚀 Améliorations Possibles

### Fonctionnalités

- [ ] Auto-refresh toutes les 30 secondes
- [ ] Alertes colorées (vert/orange/rouge) selon seuils
- [ ] Graphiques historiques avec Chart.js
- [ ] Export CSV des statistiques
- [ ] Dashboard multi-machines
- [ ] API REST pour accès distant
- [ ] Mode serveur avec Flask/FastAPI
- [ ] Notifications par email si seuils dépassés

### Interface

- [ ] Mode clair/sombre additionnel
- [ ] Plus de thèmes saisonniers
- [ ] Graphiques interactifs (hover, zoom)
- [ ] Page de configuration
- [ ] Mode plein écran

## 👥 Auteurs

Projet réalisé en équipe par : 

| Nom | GitHub |
|-----|--------|
| **Manon Sigaud** | [@Manonsigilla](https://github.com/Manonsigilla) |
| **Alex Taylor** | [@ALex-taYlor-os](https://github.com/ALex-taYlor-os) |
| **Angie Valencia** | [@angie-valencia](https://github.com/angie-valencia) |

## 🎓 Contexte

Projet réalisé dans le cadre de la formation **Bachelor IT - La Plateforme Marseille**. 

**Date** : Décembre 2025

**Compétences développées** :
- ✅ Virtualisation (VMware Workstation Pro 17)
- ✅ Administration système (Ubuntu 22.04 LTS)
- ✅ Développement Python (psutil, JSON)
- ✅ Web design moderne (HTML5/CSS3/JavaScript)
- ✅ Gestion de version (Git/GitHub)
- ✅ Documentation technique

## 📄 Licence

Ce projet est réalisé dans un cadre éducatif. 

---

<div align="center">

**© 2025 Challenge Triple A Team** 

*Made with ❤️, ☕ and ❄️*

</div>
