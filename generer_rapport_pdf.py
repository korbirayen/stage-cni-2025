#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de génération automatique du rapport PDF
Créé par : Rayen Korbi
Supervisée par : Mme Sihem Hajji
Centre National de l'Informatique (CNI) - 2025
"""

import os
import subprocess
import sys
from pathlib import Path

def install_required_packages():
    """Installe les packages LaTeX requis si nécessaire"""
    required_packages = [
        'texlive-latex-base',
        'texlive-fonts-recommended',
        'texlive-latex-extra',
        'texlive-lang-french'
    ]
    
    print("🔧 Vérification des packages LaTeX...")
    
    # Pour Windows avec MiKTeX
    if os.name == 'nt':
        print("💡 Système Windows détecté. Assurez-vous que MiKTeX est installé.")
        print("📥 Téléchargement : https://miktex.org/download")
        return True
    
    # Pour Linux
    try:
        subprocess.run(['which', 'pdflatex'], check=True, capture_output=True)
        print("✅ LaTeX est déjà installé")
        return True
    except subprocess.CalledProcessError:
        print("❌ LaTeX n'est pas installé. Installation automatique...")
        try:
            subprocess.run(['sudo', 'apt-get', 'update'], check=True)
            subprocess.run(['sudo', 'apt-get', 'install', '-y'] + required_packages, check=True)
            print("✅ LaTeX installé avec succès")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Erreur lors de l'installation : {e}")
            return False

def compile_latex_to_pdf(tex_file_path):
    """Compile le fichier LaTeX en PDF"""
    tex_file = Path(tex_file_path)
    
    if not tex_file.exists():
        print(f"❌ Fichier LaTeX non trouvé : {tex_file_path}")
        return False
    
    print(f"📄 Compilation de {tex_file.name}...")
    
    # Changer vers le répertoire du fichier
    original_dir = os.getcwd()
    os.chdir(tex_file.parent)
    
    try:
        # Première compilation
        print("🔄 Première compilation...")
        result1 = subprocess.run(['pdflatex', '-interaction=nonstopmode', tex_file.name], 
                                capture_output=True, text=True)
        
        # Deuxième compilation pour les références croisées
        print("🔄 Deuxième compilation (références croisées)...")
        result2 = subprocess.run(['pdflatex', '-interaction=nonstopmode', tex_file.name], 
                                capture_output=True, text=True)
        
        if result2.returncode == 0:
            pdf_file = tex_file.with_suffix('.pdf')
            print(f"✅ PDF généré avec succès : {pdf_file}")
            
            # Nettoyage des fichiers temporaires
            cleanup_temp_files(tex_file.stem)
            
            return True
        else:
            print(f"❌ Erreur lors de la compilation :")
            print(result2.stderr)
            return False
            
    except FileNotFoundError:
        print("❌ pdflatex non trouvé. Veuillez installer LaTeX.")
        print("💡 Windows : Installez MiKTeX")
        print("💡 Linux : sudo apt-get install texlive-full")
        print("💡 macOS : brew install --cask mactex")
        return False
    
    finally:
        os.chdir(original_dir)

def cleanup_temp_files(base_name):
    """Nettoie les fichiers temporaires générés par LaTeX"""
    temp_extensions = ['.aux', '.log', '.toc', '.out', '.fls', '.fdb_latexmk']
    
    for ext in temp_extensions:
        temp_file = Path(f"{base_name}{ext}")
        if temp_file.exists():
            temp_file.unlink()
    
    print("🧹 Fichiers temporaires supprimés")

def generate_html_report():
    """Génère un rapport HTML supplémentaire"""
    html_content = f"""
    <!DOCTYPE html>
    <html lang="fr">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Rapport de Génération PDF - CNI 2025</title>
        <style>
            body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 40px; background: #f8f9fa; }}
            .container {{ max-width: 800px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
            h1 {{ color: #2c3e50; border-bottom: 3px solid #3498db; padding-bottom: 10px; }}
            .success {{ background: #d4edda; color: #155724; padding: 15px; border-radius: 5px; margin: 20px 0; }}
            .info {{ background: #d1ecf1; color: #0c5460; padding: 15px; border-radius: 5px; margin: 20px 0; }}
            .code {{ background: #f8f9fa; padding: 10px; border-radius: 5px; font-family: monospace; }}
            .signature {{ margin-top: 40px; padding: 20px; background: #f8f9fa; border-left: 4px solid #3498db; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>📊 Rapport de Génération PDF - Analyse Salariale CNI</h1>
            
            <div class="success">
                <strong>✅ Génération Réussie !</strong><br>
                Le rapport PDF complet a été généré avec succès.
            </div>
            
            <h2>📁 Fichiers Générés</h2>
            <ul>
                <li><strong>rapport_complet.pdf</strong> - Rapport académique complet (25+ pages)</li>
                <li><strong>analyse_salariale_web.html</strong> - Dashboard interactif</li>
                <li><strong>rapport_complet.tex</strong> - Code source LaTeX</li>
            </ul>
            
            <h2>🎯 Contenu du Rapport PDF</h2>
            <div class="info">
                <ul>
                    <li>Analyse complète des données salariales 2013-2023</li>
                    <li>Modélisation prédictive multi-algorithmes</li>
                    <li>Analyse d'impact des variables explicatives</li>
                    <li>Scénarios d'optimisation avec projections financières</li>
                    <li>Recommandations stratégiques détaillées</li>
                    <li>Documentation technique complète</li>
                </ul>
            </div>
            
            <h2>🚀 Utilisation</h2>
            <p>Le rapport peut être utilisé pour :</p>
            <ul>
                <li>Présentation aux décideurs</li>
                <li>Documentation de projet</li>
                <li>Base pour futures analyses</li>
                <li>Formation et partage de connaissances</li>
            </ul>
            
            <div class="signature">
                <strong>🏢 Projet CNI 2025</strong><br>
                <strong>Créé par :</strong> Rayen Korbi<br>
                <strong>Supervisé par :</strong> Mme Sihem Hajji<br>
                <strong>GitHub :</strong> <a href="https://github.com/RayenKorbi">github.com/RayenKorbi</a><br>
                <strong>Date :</strong> {Path(__file__).stat().st_mtime}
            </div>
        </div>
    </body>
    </html>
    """
    
    with open('rapport_generation.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print("📄 Rapport HTML de génération créé : rapport_generation.html")

def main():
    """Fonction principale"""
    print("=" * 60)
    print("🎯 GÉNÉRATEUR DE RAPPORT PDF - CNI 2025")
    print("👨‍💻 Créé par : Rayen Korbi")
    print("👩‍🏫 Supervisé par : Mme Sihem Hajji")
    print("=" * 60)
    
    # Chemin du fichier LaTeX
    tex_file = Path(__file__).parent / "rapport_complet.tex"
    
    # Vérification des prérequis
    if not install_required_packages():
        print("❌ Impossible d'installer les prérequis LaTeX")
        return 1
    
    # Compilation du PDF
    if compile_latex_to_pdf(tex_file):
        print("\n🎉 SUCCESS : Rapport PDF généré avec succès !")
        print(f"📁 Fichier : {tex_file.with_suffix('.pdf')}")
        
        # Génération du rapport HTML
        generate_html_report()
        
        print("\n📋 RÉSUMÉ :")
        print("✅ Rapport PDF académique complet")
        print("✅ Dashboard web interactif")
        print("✅ Documentation technique")
        print("✅ Code source disponible")
        
        print(f"\n🔗 GitHub : https://github.com/RayenKorbi")
        print("🏢 Centre National de l'Informatique (CNI)")
        
        return 0
    else:
        print("\n❌ ERREUR : Échec de la génération du PDF")
        print("💡 Vérifiez l'installation de LaTeX")
        return 1

if __name__ == "__main__":
    exit(main())
