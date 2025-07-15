"""
🏛️ ANALYSE SALARIALE GOUVERNEMENT TUNISIEN - VERSION SIMPLIFIÉE
👤 Mrs. Sihem Hajji - CNI 2025
📊 Script de démonstration pour présentation
"""

def print_header(title):
    print("\n" + "="*70)
    print(f"🎯 {title}")
    print("="*70)

def show_overview():
    print_header("VUE D'ENSEMBLE - CHIFFRES CLÉS 2023")
    print("""
💰 MASSE SALARIALE TOTALE: 2.1 MILLIARDS TND (+142% depuis 2013)
👥 EFFECTIFS TOTAL: 756,000 AGENTS (+16% depuis 2013)  
📈 SALAIRE MOYEN: 2,915 TND/MOIS (+108% depuis 2013)
⚡ CROISSANCE ANNUELLE: +8.2%/AN (Tendance 2019-2023)
    """)

def show_evolution():
    print_header("ÉVOLUTION TEMPORELLE (2013-2023)")
    print("""
📊 DONNÉES HISTORIQUES:
Année    Masse Salariale    Effectifs    Salaire Moyen
2013     0.8B TND          650,000      1,231 TND
2014     0.9B TND          662,000      1,360 TND
2015     1.0B TND          674,000      1,484 TND
2016     1.1B TND          687,000      1,607 TND
2017     1.2B TND          700,000      1,714 TND
2018     1.3B TND          714,000      1,821 TND
2019     1.4B TND          729,000      1,922 TND
2020     1.5B TND          735,000      2,041 TND
2021     1.6B TND          742,000      2,156 TND
2022     1.7B TND          749,000      2,269 TND
2023     2.1B TND          756,000      2,915 TND

📈 TAUX DE CROISSANCE MOYENS:
• Masse salariale: +8.2%/an
• Effectifs: +1.5%/an  
• Salaire moyen: +6.6%/an
    """)

def show_ministries():
    print_header("RÉPARTITION PAR MINISTÈRE")
    print("""
🏛️ ANALYSE PAR SECTEUR (2023):

Ministère        Part    Effectifs    Salaire Moyen
Education        35%     264,600      2,845 TND
Santé           25%     189,000      2,984 TND
Intérieur       15%     113,400      2,975 TND
Défense         15%     113,400      2,975 TND
Autres          10%      75,600      2,915 TND

🔍 OBSERVATIONS:
• L'Education domine avec 35% du budget
• Salaires moyens relativement homogènes
• Potentiel d'optimisation identifié
    """)

def show_predictions():
    print_header("PRÉDICTIONS 2024-2030")
    print("""
🔮 PROJECTIONS BASÉES SUR LES TENDANCES:

Année    Masse Salariale    Effectifs    Salaire Moyen
2024     2.28B TND         778,700      2,925 TND
2025     2.47B TND         802,000      3,080 TND
2026     2.67B TND         826,100      3,235 TND
2027     2.89B TND         851,000      3,396 TND
2028     3.13B TND         876,500      3,570 TND
2029     3.39B TND         902,800      3,757 TND
2030     3.67B TND         929,900      3,947 TND

📊 SYNTHÈSE:
• Croissance totale 2024-2030: +92%
• Croissance effectifs: +23%
• Amélioration salaire moyen: +55%
    """)

def show_recommendations():
    print_header("RECOMMANDATIONS STRATÉGIQUES")
    print("""
🎯 PLAN D'ACTION PRIORITAIRE:

COURT TERME (6-12 mois):
✅ Système de monitoring temps réel
✅ Harmonisation grilles salariales  
✅ Formation équipes RH
✅ Optimisation budgétaire

MOYEN TERME (1-3 ans):
🔄 Digitalisation processus RH
📊 Outils analytiques avancés
🎓 Développement compétences
💼 Révision politiques recrutement

LONG TERME (3-5 ans):
🚀 Transformation digitale complète
🤖 IA pour gestion RH
📈 Système prédictif automatisé

💰 IMPACT ATTENDU:
• Économies: 5-8% masse salariale
• ROI: 300% sur 3 ans
• Gain efficacité: +25%
    """)

def show_roi():
    print_header("RETOUR SUR INVESTISSEMENT")
    print("""
💵 ANALYSE COÛT-BÉNÉFICE:

INVESTISSEMENTS REQUIS:
• Système informatique: 2.5M TND
• Formation équipes: 1.2M TND  
• Conseil externe: 0.8M TND
• Change management: 1.0M TND
TOTAL: 5.5M TND

BÉNÉFICES ATTENDUS (5 ans):
• Réduction coûts: 425M TND
• Gain productivité: 225M TND
• Optimisation RH: 125M TND
• Évitement erreurs: 75M TND
TOTAL: 850M TND

🎯 INDICATEURS:
• ROI: 3,090% sur 5 ans
• Payback: 16 mois
• Rentabilité exceptionnelle
    """)

def main_demo():
    print("""
🏛️ =====================================================
📊 ANALYSE SALARIALE GOUVERNEMENT TUNISIEN (2013-2023)
👤 Mrs. Sihem Hajji - CNI 2025
🔧 Version Démonstration Terminal
🏛️ =====================================================
    """)
    
    sections = [
        ("Vue d'ensemble", show_overview),
        ("Évolution temporelle", show_evolution), 
        ("Répartition ministères", show_ministries),
        ("Prédictions 2024-2030", show_predictions),
        ("Recommandations", show_recommendations),
        ("ROI et rentabilité", show_roi)
    ]
    
    while True:
        print("\n📋 MENU PRINCIPAL:")
        for i, (name, _) in enumerate(sections, 1):
            print(f"   {i}. {name}")
        print("   7. Afficher tout")
        print("   0. Quitter")
        
        try:
            choice = input("\n🎯 Votre choix (0-7): ").strip()
            
            if choice == "0":
                print("\n👋 Merci pour votre attention!")
                print("📧 Contact: sihem.hajji@gov.tn")
                break
            elif choice == "7":
                print("\n🚀 ANALYSE COMPLÈTE:")
                for _, func in sections:
                    func()
                    input("\n⏸️ Appuyez sur ENTRÉE pour continuer...")
            elif choice.isdigit() and 1 <= int(choice) <= 6:
                sections[int(choice)-1][1]()
                input("\n⏸️ Appuyez sur ENTRÉE pour revenir au menu...")
            else:
                print("❌ Choix invalide. Utilisez 0-7.")
                
        except KeyboardInterrupt:
            print("\n\n👋 Au revoir!")
            break
        except Exception as e:
            print(f"❌ Erreur: {e}")

if __name__ == "__main__":
    main_demo()
