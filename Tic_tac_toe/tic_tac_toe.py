import pygame
import sys

# Initialisation de Pygame
pygame.init()

# Paramètres du jeu
largeur, hauteur = 600, 600
taille_case = 200
ligne_epaisseur = 15
couleur_fond = (255, 255, 255)
couleur_ligne = (0, 0, 0)
couleur_texte = (0, 0, 0)
couleur_joueur1 = (255, 0, 0)
couleur_joueur2 = (0, 0, 255)
font = pygame.font.Font(None, 74)

# Initialisation de la fenêtre
ecran = pygame.display.set_mode((largeur, hauteur))
pygame.display.set_caption("Tic Tac Toe")

# Initialisation du plateau de jeu
plateau = [['' for _ in range(3)] for _ in range(3)]

# Gestion des utilisateurs et des scores (version simplifiée)
utilisateurs = []
scores = {}

# Niveaux d'IA
NIVEAU_IA = {
    'Facile': 1,
    'Moyen': 3,
    'Difficile': 5
}

# Fonction pour dessiner la grille
def dessiner_grille():
    for i in range(1, 3):
        pygame.draw.line(ecran, couleur_ligne, (i * taille_case, 0), (i * taille_case, hauteur), ligne_epaisseur)
        pygame.draw.line(ecran, couleur_ligne, (0, i * taille_case), (largeur, i * taille_case), ligne_epaisseur)

# Fonction pour dessiner les X et O sur le plateau
def dessiner_symboles():
    for ligne in range(3):
        for colonne in range(3):
            if plateau[ligne][colonne] == 'X':
                x_centre = colonne * taille_case + taille_case // 2
                y_centre = ligne * taille_case + taille_case // 2
                pygame.draw.line(ecran, couleur_joueur1, (x_centre - 50, y_centre - 50), (x_centre + 50, y_centre + 50), 10)
                pygame.draw.line(ecran, couleur_joueur1, (x_centre + 50, y_centre - 50), (x_centre - 50, y_centre + 50), 10)
            elif plateau[ligne][colonne] == 'O':
                x_centre = colonne * taille_case + taille_case // 2
                y_centre = ligne * taille_case + taille_case // 2
                pygame.draw.circle(ecran, couleur_joueur2, (x_centre, y_centre), 50, 5)

# Fonction pour vérifier s'il y a un gagnant
def verifier_gagnant():
    for i in range(3):
        if plateau[i][0] == plateau[i][1] == plateau[i][2] != '':
            return plateau[i][0]  # Gagnant sur une ligne
        if plateau[0][i] == plateau[1][i] == plateau[2][i] != '':
            return plateau[0][i]  # Gagnant sur une colonne
    if plateau[0][0] == plateau[1][1] == plateau[2][2] != '':
        return plateau[0][0]  # Gagnant sur la diagonale principale
    if plateau[0][2] == plateau[1][1] == plateau[2][0] != '':
        return plateau[0][2]  # Gagnant sur l'autre diagonale
    return None

# Fonction pour vérifier s'il y a un match nul
def verifier_match_nul():
    return all(plateau[i][j] != '' for i in range(3) for j in range(3))

# Fonction pour afficher le menu
def afficher_menu():
    font_menu = pygame.font.Font(None, 36)
    choix = None

    while choix is None:
        ecran.fill(couleur_fond)

        texte_titre = font_menu.render('Tic Tac Toe', True, couleur_texte)
        ecran.blit(texte_titre, (largeur // 2 - 100, 50))

        texte_joueur_vs_joueur = font_menu.render('1. Joueur vs Joueur', True, couleur_texte)
        texte_joueur_vs_ia = font_menu.render('2. Joueur vs IA', True, couleur_texte)

        ecran.blit(texte_joueur_vs_joueur, (largeur // 2 - 150, 200))
        ecran.blit(texte_joueur_vs_ia, (largeur // 2 - 150, 250))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    choix = 'Joueur vs Joueur'
                elif event.key == pygame.K_2:
                    choix = 'Joueur vs IA'

    return choix

# Fonction pour l'IA
def ia(board, signe):
    # L'algorithme Minimax peut être inséré ici
    def evaluer(board):
        # Fonction d'évaluation pour le Minimax
        # Retourne 10 si l'IA gagne, -10 si le joueur gagne, 0 si match nul
        gagnant = verifier_gagnant()
        if gagnant == signe:
            return 10
        elif gagnant:
            return -10
        else:
            return 0

    def minimax(board, profondeur, is_maximizing):
        score = evaluer(board)

        if score == 10 or score == -10:
            return score

        if not any('' in ligne for ligne in board) or verifier_match_nul():
            return 0

        if is_maximizing:
            meilleur_score = float('-inf')
            for i in range(3):
                for j in range(3):
                    if board[i][j] == '':
                        board[i][j] = signe
                        score = minimax(board, profondeur + 1, False)
                        board[i][j] = ''
                        meilleur_score = max(meilleur_score, score)
            return meilleur_score
        else:
            pire_score = float('inf')
            for i in range(3):
                for j in range(3):
                    if board[i][j] == '':
                        board[i][j] = 'X' if signe == 'O' else 'O'
                        score = minimax(board, profondeur + 1, True)
                        board[i][j] = ''
                        pire_score = min(pire_score, score)
            return pire_score

    meilleur_move = None
    meilleur_score = float('-inf')

    for i in range(3):
        for j in range(3):
            if board[i][j] == '':
                board[i][j] = signe
                score = minimax(board, 0, False)
                board[i][j] = ''
                if score > meilleur_score:
                    meilleur_score = score
                    meilleur_move = (i, j)

    return meilleur_move

# Fonction principale du jeu
def jouer_tic_tac_toe():
    mode = afficher_menu()

    if mode == 'Joueur vs Joueur':
        joueur_actuel = 'X'
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    colonne = event.pos[0] // taille_case
                    ligne = event.pos[1] // taille_case

                    if plateau[ligne][colonne] == '':
                        plateau[ligne][colonne] = joueur_actuel
                        if joueur_actuel == 'X':
                            joueur_actuel = 'O'
                        else:
                            joueur_actuel = 'X'
            ecran.fill(couleur_fond)
            dessiner_grille()
            dessiner_symboles()

            gagnant = verifier_gagnant()
            if gagnant:
                texte_gagnant = font.render(f'Le joueur {gagnant} a gagné !', True, couleur_texte)
                ecran.blit(texte_gagnant, (50, hauteur // 2 - 50))
            elif verifier_match_nul():
                texte_match_nul = font.render('Match nul !', True, couleur_texte)
                ecran.blit(texte_match_nul, (150, hauteur // 2 - 50))

            pygame.display.flip()

    elif mode == 'Joueur vs IA':
        joueur_actuel = 'X'
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    colonne = event.pos[0] // taille_case
                    ligne = event.pos[1] // taille_case

                    if plateau[ligne][colonne] == '':
                        plateau[ligne][colonne] = joueur_actuel
                        if joueur_actuel == 'X':
                            joueur_actuel = 'O'
                        else:
                            joueur_actuel = 'X'
            ecran.fill(couleur_fond)
            dessiner_grille()
            dessiner_symboles()

            gagnant = verifier_gagnant()
            if gagnant:
                texte_gagnant = font.render(f'Le joueur {gagnant} a gagné !', True, couleur_texte)
                ecran.blit(texte_gagnant, (50, hauteur // 2 - 50))
            elif verifier_match_nul():
                texte_match_nul = font.render('Match nul !', True, couleur_texte)
                ecran.blit(texte_match_nul, (150, hauteur // 2 - 50))
            elif joueur_actuel == 'O':
                # Tour de l'IA
                ia_move = ia(plateau, 'O')
                if ia_move:
                    plateau[ia_move[0]][ia_move[1]] = 'O'
                    joueur_actuel = 'X'

            pygame.display.flip()

# Lancer le jeu
jouer_tic_tac_toe()
