# skillmenu.py

import pygame
import global_var  # Import global variables

# SETTINGS #
from settings.settings import screen, screen_width
from settings.colors import colors
from settings.fonts import font_skills, font_TNR
from settings.images import skill_menu_img

# CLASSES #
from classes.fighter import knight
from classes.skilltext import SkillText

# EVENTS #
from events.BattleEvent import damage_text_group, DamageText

# Button dimensions for skills
button_width = 64
button_height = 64

class SkillMenu:
    def __init__(self):
        self.skill_menu_open = False
        self.skills = [
            {"name": "Shield Bash", "mana_cost": 10, "effect": "Mana Drain + DMG 10% HP"},
            {"name": "Vampire Slash", "mana_cost": 15, "effect": "LifeSteal"},
            {"name": "Sharpness", "mana_cost": 30, "effect": "STRENGTH++ (50%)"},
        ]

        # Position of the skill menu button
        self.skill_button_rect = pygame.Rect(65, screen.get_height() - button_height - 10, button_width, button_height)
        self.skill_menu_rect = pygame.Rect(0, 0, screen_width, 100)  # Skill menu area
        self.skill_button_img = skill_menu_img  # Button image

        # Target and skill tracking
        self.current_skill = None
        self.current_target = None
        self.skill_name_display_time = 0
        self.current_skill_name = None

    def draw_skill_button(self):
        # Draw the button to open the skill menu
        screen.blit(self.skill_button_img, self.skill_button_rect.topleft)

        # If the menu is open, draw the skill menu
        if self.skill_menu_open:
            pygame.draw.rect(screen, colors['gray']['dark'], self.skill_menu_rect)  # Menu background
            
            num_skills = len(self.skills)
            skill_box_width = screen_width / num_skills  # Width for each skill

            for i, skill in enumerate(self.skills):
                skill_rect = pygame.Rect(self.skill_menu_rect.left + i * skill_box_width - (skill_box_width - 375) / 2, self.skill_menu_rect.top + 10, 300, 30)
                pygame.draw.rect(screen, colors['gray']['light'], skill_rect)
                self.draw_text_skill(f"{skill['name']} (Mana: {skill['mana_cost']})", font_TNR, colors['white'], skill_rect.centerx - 140, skill_rect.top)
                self.draw_text_skill(f"Effect: {skill['effect']}", font_skills, colors['yellow']['opaque'], skill_rect.centerx - 150, skill_rect.top + 30)

    def draw_text_skill(self, text, font, color, x, y):
        text_surface = font.render(text, True, color)
        screen.blit(text_surface, (x, y))

    def handle_skill_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()

            # Toggle skill menu
            if self.skill_button_rect.collidepoint(pos):
                self.skill_menu_open = not self.skill_menu_open

            # Handle skill selection
            if self.skill_menu_open:
                num_skills = len(self.skills)
                skill_box_width = screen_width / num_skills
                for i, skill in enumerate(self.skills):
                    skill_rect = pygame.Rect(self.skill_menu_rect.left + i * skill_box_width - (skill_box_width - 375) / 2, self.skill_menu_rect.top + 10, 300, 30)
                    if skill_rect.collidepoint(pos):
                        if knight.mana >= skill['mana_cost']:
                            self.current_skill = skill
                            self.skill_menu_open = False
                        break

    def select_target(self, pos, bandit_list):
        for bandit in bandit_list:
            if bandit.rect.collidepoint(pos):
                if self.current_skill and knight.mana >= self.current_skill['mana_cost']:
                    knight.mana -= self.current_skill['mana_cost']
                    self.current_skill_name = self.current_skill['name']
                    self.skill_name_display_time = 100

                    # Skill name appears on screen
                    skill_text = SkillText(knight.rect.centerx, knight.rect.y - 50, self.current_skill_name, font_TNR, colors['yellow']['dark'])
                    damage_text_group.add(skill_text)

                    ### SHIELD BASH (KNIGHT) ###
                    if self.current_skill['name'] == "Shield Bash":
                        damage = round(bandit.max_hp * 0.10)
                        bandit.hp -= damage
                        bandit.mana = max(bandit.mana - 3, 0)
                        
                        DMG_text = DamageText(bandit.rect.centerx, bandit.rect.y + 20, str(damage), colors['yellow']['opaque'])
                        damage_text_group.add(DMG_text)

                    ### VAMPIRE SLASH (KNIGHT) ###
                    elif self.current_skill['name'] == "Vampire Slash":

                        # Activate LifeSteal
                        global_var.lifeStealActive = True

                    ### SHARPNESS (KNIGHT) ###
                    elif self.current_skill['name'] == "Sharpness":
                        knight.strength *= 1.5

                    self.current_skill = None
                break

    def draw_skill_name(self):
        if self.current_skill_name and self.skill_name_display_time > 0:
            skill_name_surface = font_TNR.render(self.current_skill_name, True, colors['white'])

            screen.blit(skill_name_surface, (screen_width // 2 - skill_name_surface.get_width() // 2, screen.get_height() // 2 - skill_name_surface.get_height() // 2))

            self.skill_name_display_time -= 1
