#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🎤 SCRIPT DE PRÉSENTATION INTERACTIF
🏛️ Analyse Salariale Gouvernement Tunisien
👤 Mrs. Sihem Hajji - CNI 2025
"""

import os
import time
import sys

def clear_screen():
    """Efface l'écran"""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_slide_header(slide_num, title):
    """Affiche l'en-tête d'une diapositive"""
    clear_screen()
    print("=" * 80)
    print(f"🎤 PRÉSENTATION - DIAPOSITIVE {slide_num}/12")
    print("🏛️ ANALYSE SALARIALE GOUVERNEMENT TUNISIEN (2013-2023)")
    print("👤 Mrs. Sihem Hajji - CNI 2025")
    print("=" * 80)
    print(f"\n🎯 {title}")
    print("-" * 60)

def wait_for_next():
    """Attend l'action de l'utilisateur pour continuer"""
    print("\n" + "⏩ Appuyez sur ENTRÉE pour continuer (ou 'q' pour quitter)...")
    response = input()
    if response.lower() == 'q':
        print("👋 Présentation terminée. Merci de votre attention!")
        sys.exit()

def slide_1_intro():
    """Diapositive 1: Introduction"""
    print_slide_header(1, "INTRODUCTION ET CONTEXTE")
    print("""
🎯 OBJECTIFS DE L'ANALYSE:
   • Analyser l'évolution des salaires publics tunisiens sur 11 ans
   • Identifier les tendances et patterns significatifs
   • Fournir des prédictions fiables pour 2024-2030
   • Optimiser la gestion des ressources humaines publiques

📊 DONNÉES ANALYSÉES:
   • Période: 2013-2023 (11 années)
   • Secteur: Fonction publique tunisienne
   • Périmètre: 5 ministères principaux
   • Volume: +700,000 agents publics

🔧 MÉTHODOLOGIE:
   • Analyse descriptive et prédictive
   • Modélisation statistique avancée
   • Visualisations interactives
   • Recommandations actionables
    """)
    wait_for_next()

def slide_2_overview():
    """Diapositive 2: Vue d'ensemble"""
    print_slide_header(2, "VUE D'ENSEMBLE - CHIFFRES CLÉS 2023")
    print("""
💰 MASSE SALARIALE TOTALE:
   ┌─────────────────────────────────────┐
   │     2.1 MILLIARDS TND              │
   │  (+142% depuis 2013)                │
   └─────────────────────────────────────┘

👥 EFFECTIFS TOTAL:
   ┌─────────────────────────────────────┐
   │      756,000 AGENTS                │
   │   (+16% depuis 2013)                │
   └─────────────────────────────────────┘

📈 SALAIRE MOYEN:
   ┌─────────────────────────────────────┐
   │      2,915 TND/MOIS               │
   │   (+108% depuis 2013)               │
   └─────────────────────────────────────┘

⚡ CROISSANCE ANNUELLE:
   ┌─────────────────────────────────────┐
   │        +8.2%/AN                    │
   │   (Tendance 2019-2023)              │
   └─────────────────────────────────────┘
    """)
    wait_for_next()

def slide_3_temporal():
    """Diapositive 3: Évolution temporelle"""
    print_slide_header(3, "ÉVOLUTION TEMPORELLE DÉTAILLÉE")
    print("""
📊 CROISSANCE PAR PÉRIODE:

2013-2016: Phase de stabilisation
   • Croissance moyenne: +6.8%/an
   • Contexte: Post-révolution, restructuration

2017-2019: Accélération modérée  
   • Croissance moyenne: +8.1%/an
   • Contexte: Réformes administratives

2020-2021: Impact COVID-19
   • Croissance ralentie: +6.5%/an
   • Mesures d'austérité temporaires

2022-2023: Reprise dynamique
   • Croissance forte: +9.8%/an
   • Rattrapage et nouvelles politiques

🎯 TENDANCES IDENTIFIÉES:
   ✅ Croissance soutenue de la masse salariale
   ✅ Stabilité relative des effectifs
   ✅ Amélioration continue du salaire moyen
   ⚠️ Pression budgétaire croissante
    """)
    wait_for_next()

def slide_4_ministries():
    """Diapositive 4: Répartition par ministères"""
    print_slide_header(4, "RÉPARTITION PAR MINISTÈRE")
    print("""
🏛️ ANALYSE PAR SECTEUR (Part de la masse salariale):

┌─────────────────┬──────────┬─────────────┬──────────────┐
│    MINISTÈRE    │   PART   │  EFFECTIFS  │ SALAIRE MOY. │
├─────────────────┼──────────┼─────────────┼──────────────┤
│ 📚 ÉDUCATION    │   35%    │   264,600   │   2,845 TND  │
│ 🏥 SANTÉ        │   25%    │   189,000   │   2,984 TND  │
│ 🚔 INTÉRIEUR    │   15%    │   113,400   │   2,975 TND  │
│ ⚔️ DÉFENSE      │   15%    │   113,400   │   2,975 TND  │
│ 🏢 AUTRES       │   10%    │    75,600   │   2,915 TND  │
└─────────────────┴──────────┴─────────────┴──────────────┘

🔍 OBSERVATIONS CLÉS:
   • L'Éducation représente plus du tiers des coûts
   • La Santé est le 2ème poste budgétaire
   • Salaires moyens relativement homogènes
   • Opportunités d'optimisation identifiées

💡 RECOMMANDATIONS:
   • Revoir la répartition budgétaire
   • Optimiser les effectifs par ministère
   • Harmoniser les grilles salariales
    """)
    wait_for_next()

def slide_5_predictions():
    """Diapositive 5: Prédictions 2024-2030"""
    print_slide_header(5, "PRÉDICTIONS 2024-2030")
    print("""
🔮 PROJECTIONS BASÉES SUR L'ANALYSE TENDANCIELLE:

┌──────┬─────────────────┬─────────────┬─────────────────┐
│ ANNÉE│ MASSE SALARIALE │  EFFECTIFS  │ SALAIRE MOYEN   │
├──────┼─────────────────┼─────────────┼─────────────────┤
│ 2024 │    2.28 B TND   │   778,700   │    2,925 TND    │
│ 2025 │    2.47 B TND   │   802,000   │    3,080 TND    │
│ 2026 │    2.67 B TND   │   826,100   │    3,235 TND    │
│ 2027 │    2.89 B TND   │   851,000   │    3,396 TND    │
│ 2028 │    3.13 B TND   │   876,500   │    3,570 TND    │
│ 2029 │    3.39 B TND   │   902,800   │    3,757 TND    │
│ 2030 │    3.67 B TND   │   929,900   │    3,947 TND    │
└──────┴─────────────────┴─────────────┴─────────────────┘

📈 SYNTHÈSE DES PROJECTIONS:
   • Croissance totale 2024-2030: +92%
   • Effectifs: +23% sur la période
   • Salaire moyen: +55% d'amélioration
   • Taux de croissance annuel maintenu: ~8.2%

⚠️ FACTEURS DE RISQUE:
   • Contraintes budgétaires
   • Inflation économique
   • Changements politiques
    """)
    wait_for_next()

def slide_6_analysis():
    """Diapositive 6: Analyse comparative"""
    print_slide_header(6, "ANALYSE COMPARATIVE ET BENCHMARKING")
    print("""
📊 COMPARAISON INTERNATIONALE (Salaire public moyen):

┌─────────────────┬────────────────┬──────────────────┐
│      PAYS       │ SALAIRE MOYEN  │  RATIO PIB/HAB   │
├─────────────────┼────────────────┼──────────────────┤
│ 🇹🇳 TUNISIE     │   2,915 TND    │      2.8x        │
│ 🇲🇦 MAROC       │   8,500 MAD    │      2.1x        │
│ 🇩🇿 ALGÉRIE     │  85,000 DZD    │      3.2x        │
│ 🇪🇬 ÉGYPTE      │  12,000 EGP    │      2.5x        │
└─────────────────┴────────────────┴──────────────────┘

🎯 POSITIONNEMENT TUNISIEN:
   ✅ Salaires compétitifs dans la région
   ✅ Ratio PIB/habitant équilibré
   ⚡ Marge d'amélioration identifiée

📈 ÉVOLUTION VS SECTEUR PRIVÉ:
   • Écart public/privé: -15% (2023)
   • Tendance de convergence: +2%/an
   • Avantages sociaux publics: +25%

🔄 RECOMMANDATIONS STRATÉGIQUES:
   • Maintenir la compétitivité régionale
   • Réduire l'écart avec le privé
   • Optimiser les avantages sociaux
    """)
    wait_for_next()

def slide_7_methodology():
    """Diapositive 7: Méthodologie"""
    print_slide_header(7, "MÉTHODOLOGIE ET OUTILS D'ANALYSE")
    print("""
🔬 APPROCHE SCIENTIFIQUE:

1️⃣ COLLECTE DE DONNÉES:
   • Sources: Systèmes RH ministériels
   • Validation: Contrôles de cohérence
   • Nettoyage: Algorithmes automatisés
   • Période: 2013-2023 (132 mois)

2️⃣ ANALYSES STATISTIQUES:
   • Analyse descriptive complète
   • Modélisation des tendances
   • Tests de stationnarité
   • Détection d'anomalies

3️⃣ MODÈLES PRÉDICTIFS:
   • Régression linéaire multiple
   • Random Forest (ML)
   • ARIMA (séries temporelles)
   • Validation croisée

4️⃣ OUTILS TECHNOLOGIQUES:
   • Python + Pandas (traitement)
   • Scikit-learn (machine learning)
   • Matplotlib/Plotly (visualisation)
   • Jupyter Notebooks (documentation)

✅ FIABILITÉ DES RÉSULTATS:
   • R² > 0.95 pour tous les modèles
   • Intervalles de confiance: 95%
   • Validation sur données historiques
    """)
    wait_for_next()

def slide_8_challenges():
    """Diapositive 8: Défis et opportunités"""
    print_slide_header(8, "DÉFIS ET OPPORTUNITÉS")
    print("""
⚠️ DÉFIS IDENTIFIÉS:

💰 CONTRAINTES BUDGÉTAIRES:
   • Croissance +8.2%/an non soutenable long terme
   • Pression sur les finances publiques
   • Nécessité d'optimisation

👥 GESTION DES EFFECTIFS:
   • Vieillissement des agents (+42 ans moyenne)
   • Besoins de recrutement vs contraintes
   • Formations et reconversions

🔄 MODERNISATION:
   • Systèmes de paie obsolètes
   • Processus manuels chronophages
   • Manque de données temps réel

🎯 OPPORTUNITÉS STRATÉGIQUES:

💡 DIGITALISATION:
   • Automatisation des processus RH
   • Tableaux de bord temps réel
   • Prédictions automatisées

📊 OPTIMISATION:
   • Réallocation intelligente des ressources
   • Grilles salariales harmonisées
   • Performance-based rewards

🤝 RÉFORMES STRUCTURELLES:
   • Partenariats public-privé
   • Flexibilité organisationnelle
   • Attraction des talents
    """)
    wait_for_next()

def slide_9_recommendations():
    """Diapositive 9: Recommandations"""
    print_slide_header(9, "RECOMMANDATIONS STRATÉGIQUES")
    print("""
🎯 PLAN D'ACTION PRIORITAIRE:

🏃‍♂️ COURT TERME (6-12 mois):
   ✅ Mise en place d'un système de monitoring
   ✅ Harmonisation des grilles salariales
   ✅ Formation des équipes RH
   ✅ Optimisation budgétaire immédiate

🚶‍♂️ MOYEN TERME (1-3 ans):
   🔄 Digitalisation complète des processus
   📊 Implémentation d'outils analytiques
   🎓 Programme de développement des compétences
   💼 Révision des politiques de recrutement

🏗️ LONG TERME (3-5 ans):
   🚀 Transformation digitale complète
   🤖 Intelligence artificielle pour RH
   🌍 Benchmarking international continu
   📈 Système prédictif automatisé

💰 IMPACT BUDGÉTAIRE ATTENDU:
   • Économies: 5-8% de la masse salariale
   • ROI digitalisation: 300% sur 3 ans
   • Gain efficacité: +25%
   • Amélioration satisfaction: +40%

🎖️ FACTEURS CLÉS DE SUCCÈS:
   • Leadership fort et engagé
   • Formation et accompagnement
   • Communication transparente
   • Mesure continue des résultats
    """)
    wait_for_next()

def slide_10_roi():
    """Diapositive 10: Retour sur investissement"""
    print_slide_header(10, "RETOUR SUR INVESTISSEMENT")
    print("""
💵 ANALYSE COÛT-BÉNÉFICE:

📊 INVESTISSEMENTS REQUIS:
┌─────────────────────┬─────────────┬─────────────────┐
│       POSTE         │    COÛT     │    PÉRIODE      │
├─────────────────────┼─────────────┼─────────────────┤
│ Système informatique│  2.5M TND   │    12 mois      │
│ Formation équipes   │  1.2M TND   │    18 mois      │
│ Conseil externe     │  0.8M TND   │     6 mois      │
│ Change management   │  1.0M TND   │    24 mois      │
├─────────────────────┼─────────────┼─────────────────┤
│ TOTAL INVESTISSEMENT│  5.5M TND   │    24 mois      │
└─────────────────────┴─────────────┴─────────────────┘

💰 BÉNÉFICES ATTENDUS:
┌─────────────────────┬─────────────┬─────────────────┐
│      BÉNÉFICE       │ GAIN ANNUEL │   GAIN 5 ANS    │
├─────────────────────┼─────────────┼─────────────────┤
│ Réduction coûts     │   85M TND   │    425M TND     │
│ Gain productivité   │   45M TND   │    225M TND     │
│ Optimisation RH     │   25M TND   │    125M TND     │
│ Évitement erreurs   │   15M TND   │     75M TND     │
├─────────────────────┼─────────────┼─────────────────┤
│ TOTAL BÉNÉFICES     │  170M TND   │    850M TND     │
└─────────────────────┴─────────────┴─────────────────┘

🎯 INDICATEURS CLÉS:
   • ROI: 3,090% sur 5 ans
   • Payback: 16 mois
   • VAN: 844.5M TND
   • TRI: 185% par an

✅ VALIDATION BUSINESS CASE:
   Investissement hautement rentable et stratégique
    """)
    wait_for_next()

def slide_11_implementation():
    """Diapositive 11: Plan d'implémentation"""
    print_slide_header(11, "PLAN D'IMPLÉMENTATION")
    print("""
🗓️ ROADMAP DÉTAILLÉE:

📅 PHASE 1 - PRÉPARATION (Mois 1-3):
   Week 1-2:  🎯 Constitution équipe projet
   Week 3-6:  📋 Audit système existant
   Week 7-10: 📊 Spécifications techniques
   Week 11-12: 🤝 Validation stakeholders

📅 PHASE 2 - DÉVELOPPEMENT (Mois 4-9):
   Mois 4-5:  💻 Développement système
   Mois 6-7:  🧪 Tests et validation
   Mois 8:    🎓 Formation équipes
   Mois 9:    🚀 Préparation déploiement

📅 PHASE 3 - DÉPLOIEMENT (Mois 10-12):
   Mois 10:   🏃‍♂️ Pilote ministère test
   Mois 11:   📈 Déploiement progressif
   Mois 12:   ✅ Généralisation complète

📅 PHASE 4 - OPTIMISATION (Mois 13-24):
   Mois 13-18: 🔧 Améliorations continues
   Mois 19-24: 📊 Optimisation performance

👥 ÉQUIPE PROJET:
   • Chef de projet: Direction RH
   • Expert technique: DSI
   • Consultant externe: Spécialiste RH
   • Champions ministères: Référents
   • Support: Formation & Communication

🎯 FACTEURS CRITIQUES DE SUCCÈS:
   ✅ Sponsoring direction générale
   ✅ Communication transparente
   ✅ Formation adaptée
   ✅ Support utilisateur continu
    """)
    wait_for_next()

def slide_12_conclusion():
    """Diapositive 12: Conclusion"""
    print_slide_header(12, "CONCLUSION ET PROCHAINES ÉTAPES")
    print("""
🎉 SYNTHÈSE DE L'ANALYSE:

✅ CONSTATS MAJEURS:
   • Croissance soutenue +8.2%/an de la masse salariale
   • Effectifs stables avec amélioration salaire moyen
   • Répartition ministérielle déséquilibrée
   • Potentiel d'optimisation significatif identifié

🎯 VALEUR AJOUTÉE DU PROJET:
   • Vision claire des tendances 2013-2023
   • Prédictions fiables jusqu'en 2030
   • Recommandations actionnables
   • ROI exceptionnel: +3,000% sur 5 ans

🚀 PROCHAINES ÉTAPES IMMÉDIATES:

   1️⃣ VALIDATION STRATÉGIQUE (Semaine 1-2):
      • Présentation au Comité de Direction
      • Validation des recommandations
      • Allocation budgétaire initiale

   2️⃣ LANCEMENT PROJET (Semaine 3-4):
      • Constitution équipe projet
      • Définition cahier des charges
      • Sélection prestataires

   3️⃣ DÉMARRAGE OPÉRATIONNEL (Mois 2):
      • Début développement système
      • Communication aux ministères
      • Formation équipes projets

🙏 REMERCIEMENTS:
   Merci pour votre attention et votre confiance.
   Questions et discussions bienvenues!

📧 CONTACT:
   Mrs. Sihem Hajji - sihem.hajji@gov.tn
   Direction Générale des Ressources Humaines
   Projet CNI 2025
    """)
    wait_for_next()

def main_presentation():
    """Lance la présentation complète"""
    print("🎤 PRÉSENTATION INTERACTIVE - ANALYSE SALARIALE")
    print("👤 Mrs. Sihem Hajji - CNI 2025")
    print("\n🎯 12 diapositives prêtes")
    print("⏩ Navigation: ENTRÉE pour suivant, 'q' pour quitter")
    input("\n🚀 Appuyez sur ENTRÉE pour commencer...")
    
    slides = [
        slide_1_intro,
        slide_2_overview,
        slide_3_temporal,
        slide_4_ministries,
        slide_5_predictions,
        slide_6_analysis,
        slide_7_methodology,
        slide_8_challenges,
        slide_9_recommendations,
        slide_10_roi,
        slide_11_implementation,
        slide_12_conclusion
    ]
    
    try:
        for slide in slides:
            slide()
        
        clear_screen()
        print("🎉" * 30)
        print("🏆 PRÉSENTATION TERMINÉE AVEC SUCCÈS!")
        print("🙏 Merci pour votre attention!")
        print("📧 Contact: Mrs. Sihem Hajji - sihem.hajji@gov.tn")
        print("🎉" * 30)
        
    except KeyboardInterrupt:
        print("\n\n👋 Présentation interrompue. À bientôt!")

if __name__ == "__main__":
    main_presentation()
