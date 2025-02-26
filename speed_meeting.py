#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Organisateur de Speed Meeting

Ce programme génère une planification pour un speed meeting de 50 personnes
réparties sur 10 tables de 5 personnes, en maximisant les rencontres uniques.
"""

import random
import csv
from collections import defaultdict

# Configuration
NB_PARTICIPANTS = 50
NB_TABLES = 10
PERSONNES_PAR_TABLE = 5
NB_TOURS = 10  # Vous pouvez augmenter jusqu'à 13 pour plus de rencontres uniques

def generer_planning():
    # Initialiser les participants
    participants = list(range(1, NB_PARTICIPANTS + 1))
    
    # Initialiser le suivi des rencontres
    rencontres = defaultdict(set)
    
    # Générer les tours
    tours = []
    
    for tour in range(NB_TOURS):
        # Mélanger les participants à chaque tour
        random.shuffle(participants)
        
        # Répartir les participants sur les tables
        tables = [participants[i:i+PERSONNES_PAR_TABLE] for i in range(0, NB_PARTICIPANTS, PERSONNES_PAR_TABLE)]
        
        # Mettre à jour le suivi des rencontres
        for table in tables:
            for p1 in table:
                for p2 in table:
                    if p1 != p2:
                        rencontres[p1].add(p2)
        
        # Ajouter le tour au planning
        tours.append(tables)
    
    # Calculer les statistiques
    total_rencontres = 0
    min_rencontres = NB_PARTICIPANTS
    max_rencontres = 0
    
    for participant, ses_rencontres in rencontres.items():
        nb_rencontres = len(ses_rencontres)
        total_rencontres += nb_rencontres
        min_rencontres = min(min_rencontres, nb_rencontres)
        max_rencontres = max(max_rencontres, nb_rencontres)
    
    avg_rencontres = total_rencontres / NB_PARTICIPANTS
    
    return tours, rencontres, {
        'total': total_rencontres,
        'moyenne': avg_rencontres,
        'min': min_rencontres,
        'max': max_rencontres
    }

def exporter_csv(tours, nom_fichier="planning_speed_meeting.csv"):
    with open(nom_fichier, 'w', newline='', encoding='utf-8') as fichier:
        writer = csv.writer(fichier)
        
        # En-tête
        header = ['Tour', 'Table', 'Participants']
        writer.writerow(header)
        
        # Données
        for num_tour, tour in enumerate(tours, 1):
            for num_table, table in enumerate(tour, 1):
                row = [f"Tour {num_tour}", f"Table {num_table}", ", ".join(map(str, table))]
                writer.writerow(row)

def afficher_planning(tours):
    for num_tour, tour in enumerate(tours, 1):
        print(f"\n=== TOUR {num_tour} ===")
        for num_table, table in enumerate(tour, 1):
            print(f"Table {num_table}: {', '.join(map(str, table))}")

def afficher_statistiques(stats, rencontres):
    print("\n=== STATISTIQUES ===")
    print(f"Nombre total de rencontres : {stats['total']}")
    print(f"Moyenne de rencontres par participant : {stats['moyenne']:.2f}")
    print(f"Minimum de rencontres par participant : {stats['min']}")
    print(f"Maximum de rencontres par participant : {stats['max']}")
    
    # Calcul de couverture
    rencontres_possibles = NB_PARTICIPANTS * (NB_PARTICIPANTS - 1)
    couverture = (stats['total'] / rencontres_possibles) * 100
    print(f"Couverture des rencontres possibles : {couverture:.2f}%")

def main():
    print("Génération du planning de speed meeting...")
    tours, rencontres, stats = generer_planning()
    
    afficher_planning(tours)
    afficher_statistiques(stats, rencontres)
    
    exporter_csv(tours)
    print("\nPlanning exporté dans 'planning_speed_meeting.csv'")

if __name__ == "__main__":
    random.seed(42)  # Pour reproductibilité
    main()
