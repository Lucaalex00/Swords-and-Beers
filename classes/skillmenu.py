import pygame

# SETTINGS #
from settings.settings import screen
from settings.colors import colors
from settings.fonts import font_TNR
from settings.images import skill_menu_img
# CLASSES #
from classes.fighter import knight

# GLOBAL VAR #
import global_var

# Dimensioni del bottone delle skill, uguali a quelle del bottone della pozione
button_width = 64
button_height = 64

class SkillMenu:
    def __init__(self):
        self.skill_menu_open = False
        self.skills = [
            {"name": "Skill 1", "mana_cost": 10, "effect": "Danno Extra"},
            {"name": "Skill 2", "mana_cost": 15, "effect": "Cura"},
            {"name": "Skill 3", "mana_cost": 20, "effect": "Protezione"},
        ]

        # Posizione del bottone per aprire il menu delle skill
        self.skill_button_rect = pygame.Rect(65, screen.get_height() - button_height - 10, button_width, button_height)
        self.skill_menu_rect = pygame.Rect(70, screen.get_height() - button_height - 85 - button_height - 70, 200, 120)  # Area del menu delle skill
        self.skill_button_img = skill_menu_img  # Immagine del bottone

    def draw_skill_button(self):
        # Disegna il bottone per aprire il menu delle skill
        screen.blit(self.skill_button_img, self.skill_button_rect.topleft)

        # Se il menu è aperto, disegna il menu delle skill
        if self.skill_menu_open:
            pygame.draw.rect(screen, colors['blue']['opaque'], self.skill_menu_rect)  # Riquadro per il menu delle skill

            for i, skill in enumerate(self.skills):
                skill_rect = pygame.Rect(self.skill_menu_rect.left + 10, self.skill_menu_rect.top + 10 + i * 40, 180, 30)
                pygame.draw.rect(screen, colors['gray']['light'], skill_rect)  # Riquadro per la skill
                self.draw_text_skill(f"{skill['name']} (Mana: {skill['mana_cost']})", font_TNR, colors['white'], skill_rect.topleft[0] + 5, skill_rect.topleft[1] + 5)

    def draw_text_skill(self, text, font, color, x, y):
        text_surface = font.render(text, True, color)
        screen.blit(text_surface, (x, y))

    def handle_skill_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()

            if self.skill_button_rect.collidepoint(pos):
                self.skill_menu_open = not self.skill_menu_open  # Apri/chiudi il menu delle skill
                print("Skill menu toggled")

            if self.skill_menu_open:
                for i, skill in enumerate(self.skills):
                    skill_rect = pygame.Rect(self.skill_menu_rect.left + 10, self.skill_menu_rect.top + 10 + i * 40, 180, 30)
                    if skill_rect.collidepoint(pos) and knight.mana >= skill['mana_cost']:
                        # Applica l'effetto della skill
                        knight.mana -= skill['mana_cost']  # Sottrai mana
                        if skill['name'] == "Skill 1":
                            # Esempio: Danno extra
                            global_var.attackAction = True
                            global_var.target.hp -= 10  # Danno fisso
                        elif skill['name'] == "Skill 2":
                            # Esempio: Cura
                            knight.hp = min(knight.hp + 20, knight.max_hp)  # Cura fino al massimo
                        elif skill['name'] == "Skill 3":
                            # Esempio: Protezione
                            knight.strength += 5  # Aumenta la forza temporaneamente
                        self.skill_menu_open = False  # Chiudi il menu dopo aver usato una skill
