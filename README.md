# Trade AI - Trading IA Forex & Or

Une plateforme d'intelligence artificielle spécialisée dans le trading automatisé sur le Forex et l'Or.

## 🎯 Objectifs

- Prédiction de prix avec modèles ML avancés
- Génération de signaux d'achat/vente automatiques
- Gestion des risques et des portefeuilles
- Backtesting de stratégies
- Monitoring en temps réel
- Exécution automatique des ordres (optionnel)

## 🛠️ Stack Technologique

- **Backend**: Python 3.10+, FastAPI
- **ML/AI**: TensorFlow, PyTorch, scikit-learn
- **Base de données**: PostgreSQL, Redis
- **Data**: pandas, numpy, ta-lib
- **Conteneurisation**: Docker, Docker Compose
- **Testing**: pytest
- **API Forex/Or**: Alpha Vantage, OANDA, IQFeed, etc.

## 📁 Structure du Projet

```
trade/
├── src/
│   ├── data/              # Collecte et prétraitement des données
│   ├── models/            # Modèles ML et stratégies
│   ├── trading/           # Logique de trading
│   ├── backtesting/       # Framework de backtesting
│   ├── api/               # API REST FastAPI
│   └── utils/             # Utilitaires
├── tests/                 # Tests unitaires et intégration
├── config/                # Configuration
├── notebooks/             # Jupyter notebooks pour exploration
├── docker/                # Dockerfiles
├── requirements.txt       # Dépendances Python
├── docker-compose.yml     # Configuration Docker Compose
└── README.md
```

## 🚀 Démarrage Rapide

### Prérequis
- Python 3.10+
- Docker & Docker Compose
- Git

### Installation

```bash
# Cloner le repo
git clone https://github.com/mengoloraphael/trade.git
cd trade

# Créer l'environnement virtuel
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows

# Installer les dépendances
pip install -r requirements.txt

# Lancer avec Docker Compose
docker-compose up -d
```

### Configuration

1. Copier `.env.example` en `.env`
2. Remplir les clés API (Forex, Or, etc.)
3. Configurer la base de données

## 📊 Modules Principaux

### 1. Data Module (`src/data/`)
- Collecte en temps réel
- Nettoyage et normalisation
- Feature engineering
- Stockage en base de données

### 2. Models Module (`src/models/`)
- LSTM pour prédictions de séries temporelles
- Transformer Models
- Ensemble methods
- Feature importance analysis

### 3. Trading Module (`src/trading/`)
- Générateur de signaux
- Risk management
- Position sizing
- Portfolio management

### 4. Backtesting Module (`src/backtesting/`)
- Simulation de stratégies
- Métriques de performance
- Optimisation de paramètres

### 5. API Module (`src/api/`)
- Endpoints REST
- WebSocket pour données en temps réel
- Dashboard

## 📈 Fonctionnalités Plannifiées

- [ ] Collecte de données en temps réel
- [ ] Modèles de prédiction LSTM
- [ ] Système de signaux intelligents
- [ ] Backtesting framework
- [ ] API REST complète
- [ ] Dashboard de monitoring
- [ ] Gestion automatique des positions
- [ ] Risk management avancé
- [ ] Machine learning auto-tuning
- [ ] Intégration brokers (OANDA, etc.)

## 🔒 Sécurité

⚠️ **Attention**: Ne jamais commiter les clés API ou secrets.
- Utiliser `.env` pour les secrets
- Activer 2FA sur les comptes de trading
- Valider en demo avant production

## 📝 Documentation

Voir `/docs` pour la documentation détaillée.

## 🤝 Contribution

Les contributions sont bienvenues ! Voir CONTRIBUTING.md

## 📄 Licence

MIT License - Voir LICENSE

## ⚠️ Disclaimer

Ce projet est à but éducatif et expérimental. Le trading comporte des risques.
Testez toujours en mode démo avant utilisation réelle. L'auteur ne sera pas responsable des pertes financières.

---

**Développé par**: mengoloraphael  
**Dernière mise à jour**: 2026-06-09
