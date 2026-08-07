"""
Author: Jieun Kwon
Date Created: 05/05/2026
Last Modified: 03/08/2026

Important Notice: 
Please ensure that Pygame-ce (Pygame community edition) speciifically has been installed prior to 
running this code, as it will not work otherwise!

As this program includes audio, please make sure your volume is set to an appropriate level.


Brief Description: 
This is a Maths Game for AS919106, AS91907
It covers basic addition, subtraction, multiplication, fractions, exponents, and algebra.
The target demographic for this game is year 9 students. (approx. 13 ~ 14 years old)

This program is 'pancake making' or baking themed and features various (handdrawn) design aspects.
The aim of the gameplay is to create baked goods by answering various maths questions.

For a more in-depth description and explanation, please view the README.md file provided.

                     ***    ******               
                    **.******.  +**              
                  **+   :**      =               
             ***  **     +*     -**              
              *****       .    .**               
               ****       *. .-*****             
      ***+:  .-****-     =**===--====***         
     **-          **   +*=-------------=**       
      **+           **+=--------------====**     
     ******.      **=--------=*=-------=+--**    
  ***:     :*****==-----------==-----------=**   
 **-         =*=----------------------------=*   
  ***-     .**=-----*=----------------------=**  
       ******=-------=--------------==-------**  
          **==----------------------=*=------=** 
          **===------------=*+---------------=** 
          **===-=*=--------------------------=** 
           +====-==---------------------------=  
           **====------------------------=*=-=** 
            **=====--------------------------=** 
              **=====*=-------=*=------------**  
               ***=======------==-----------=**  
                  ***+=======---------+=----+*   
                     ****=========----===--=**   
                         *****============***    
                              *************     
"""

import pygame
import random
import sys
import math
import time
from fractions import Fraction

# Initialising pygame.
pygame.init()
pygame.mixer.init()

# Setting variables for future use (currently unused).
clock = pygame.time.Clock()
delta_time = 0.1



#============================================================================
#   Audio
#----------------------------------------------------------------------------

# Background music. (non-copyrighted, View references for credit).
pygame.mixer.music.load("Assets/Audio/BGM.mp3")

# Background music volume.
pygame.mixer.music.set_volume(0.1)  

# Looping the background music to run forever.
pygame.mixer.music.play(-1)


# Button click sound effect. (non-copyrighted, View references for credit).
click_sound  = pygame.mixer.Sound("Assets/Audio/click.mp3")

# Button click sound effect volume.
click_sound.set_volume(0.1)

# Keyboard sound effect. (non-copyrighted, View references for credit).
kb_sound = pygame.mixer.Sound("Assets/Audio/kb_click.mp3")

# Keyboard sound effect volume.
kb_sound.set_volume(0.1)

blip = pygame.mixer.Sound("Assets/Audio/blipcat.mp3")
blip.set_volume(0.3)

blip2 = pygame.mixer.Sound("Assets/Audio/blipboy.wav")
blip2.set_volume(0.3)

blip3 = pygame.mixer.Sound("Assets/Audio/blipgirl.wav")
blip3.set_volume(0.3)
#============================================================================
#   Defining fonts
#----------------------------------------------------------------------------

#Header font (different sizes).
header_font_sml = pygame.font.Font('Assets/MonsterFriendFore.otf', size =18)
header_font = pygame.font.Font('Assets/MonsterFriendFore.otf', size =20)
header_font_lrg = pygame.font.Font('Assets/MonsterFriendFore.otf', size =22)
header_font_XL = pygame.font.Font('Assets/MonsterFriendFore.otf', size =26)

#Sub font (different sizes).
sub_font_sml = pygame.font.Font('Assets/monoMMM_5.ttf',size =20)
sub_font = pygame.font.Font('Assets/monoMMM_5.ttf',size =24)
sub_font_lrg = pygame.font.Font('Assets/monoMMM_5.ttf',size =26)

#============================================================================
#   Defining text files for file handling
#----------------------------------------------------------------------------

#file for storing user data for game over screen.
filename = 'Assets/PancakeProblemsData.txt'

#leaderboard files
easy_leader = 'Assets/EasyDifficultyLeaderboard.txt' 
med_leader = 'Assets/MedDifficultyLeaderboard.txt'
hard_leader = 'Assets/HardDifficultyLeaderboard.txt'

#============================================================================
#   Setting up display
#----------------------------------------------------------------------------

#Creating a screen / display and setting its size.
screen = pygame.display.set_mode((1200,675))

#Setting display name to 'Maths Game'.
pygame.display.set_caption('Pancake Problems - Maths Game')

#Changing the display's icon to icon.png (strawberry).
pygame.display.set_icon(pygame.image.load('Assets/Images/icon.png').convert_alpha())

#assigining variable to background image.
gingham = pygame.image.load('Assets/Images/gingham4.png').convert_alpha()

# ============================================================================
#   Class for buttons using header font
# ----------------------------------------------------------------------------

class Buttons():
    def __init__(self, x, y, width, height, text, colour):

        # Class variables.
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.colour = colour
            
    def draw(self, surface): 
        
        # Assigning variables to button size and coordinates.
        x = self.rect.x
        y = self.rect.y
        width = self.rect.width
        height = self.rect.height

        # Defining mouse / cursor position.
        mpos = pygame.mouse.get_pos()

        # Enlarging button rect if cursor collides with rect.
        if self.rect.collidepoint(mpos) == True:
            
            width += 10
            height += 10 
            x -= 5
            y -= 5

        # Variable for button rect.
        button_rect = pygame.Rect(x, y, width, height)

        #Creating button on screen.
        pygame.draw.rect(surface, self.colour, button_rect, border_radius=12)

        # Enlarging font if cursor collides with rect.
        if  self.rect.collidepoint(mpos) == True:
            text_surface = header_font_lrg.render(self.text, True, (115,70,55))
        else:
            text_surface = header_font.render(self.text, True, (115,70,55))
        
        # Variable for text rect (centered to button rect).
        text_rect = text_surface.get_rect(center=button_rect.center)

        # Blitting / drawing button and text onto screen.
        surface.blit(text_surface, text_rect)

    def is_clicked(self, event):
        
        # If a mouse button is pressed.
        if event.type == pygame.MOUSEBUTTONDOWN:

            # If button pressed is left click.
            if event.button == 1:

                # If cursor position collides with button rect.
                if self.rect.collidepoint(event.pos):

                    # Playing button sound effect.
                    click_sound.play()

                    # Button is clicked
                    return True
                
        # Button is not clicked
        return False
    
# ============================================================================
#   Class for buttons using sub-font
# ----------------------------------------------------------------------------

class Buttons2():
    def __init__(self, x, y, width, height, text, colour):

        # Class variables.
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.colour = colour

    def draw(self, surface):
        
        # Assigning variables to button size and coordinates. 
        x = self.rect.x
        y = self.rect.y
        width = self.rect.width
        height = self.rect.height

        # Defining mouse / cursor position.
        mpos = pygame.mouse.get_pos()

        # Enlarging button rect if cursor collides with rect.
        if self.rect.collidepoint(mpos) == True:
            
            width += 10
            height += 10 
            x -= 5
            y -= 5
            
        # Variable for button rect.
        button_rect = pygame.Rect(x, y, width, height)

        # Creating button on screen.
        pygame.draw.rect(surface, self.colour, button_rect, border_radius=12)

        # Enlarging font if cursor collides with rect.
        if  self.rect.collidepoint(mpos) == True:
            text_surface = sub_font_lrg.render(self.text, True, (115,70,55))
        else:
            text_surface = sub_font.render(self.text, True, (115,70,55))

        # Variable for text rect (centered to button rect).
        text_rect = text_surface.get_rect(center=button_rect.center)
        
        # Blitting / drawing button and text onto screen.
        surface.blit(text_surface, text_rect)

    def is_clicked(self, event):
        
        # If a mouse button is pressed.
        if event.type == pygame.MOUSEBUTTONDOWN:

            # If button pressed is left click.
            if event.button == 1:

                # If cursor position collides with button rect.
                if self.rect.collidepoint(event.pos):

                    # Playing button sound effect.
                    click_sound.play()

                    # Button is clicked.
                    return True

        # Button is not clicked.
        return False

# ============================================================================
#   Class for buttons for combobox
# ----------------------------------------------------------------------------

class Buttons3():
    def __init__(self, x, y, width, height, text,colour):

        # Class variables
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.colour = colour

    def draw(self, surface): 

        # Assigning variables to button size and coordinates. 
        x = self.rect.x
        y = self.rect.y
        width = self.rect.width
        height = self.rect.height

        # Defining mouse / cursor position.
        mpos = pygame.mouse.get_pos()

        # Defining button colour.
        self.colour = (255,237,203)
        
        # Changing button colour if cursor collides with rect.
        if self.rect.collidepoint(mpos) == True:
            self.colour = (240, 211, 168)

        # Variable for button rect.
        button_rect = pygame.Rect(x, y, width, height)

        # Creating button on screen.
        pygame.draw.rect(surface, self.colour, button_rect, border_radius=6)

        # Variable for text render.
        text_surface = sub_font_sml.render(self.text, True, (115,70,55))
        
        # Variable for text rect (centered to button rect).
        text_rect = text_surface.get_rect(center=button_rect.center)
        
        # Blitting / drawing button and text onto screen.
        surface.blit(text_surface, text_rect)

    def is_clicked(self, event):

        # If a mouse button is pressed.
        if event.type == pygame.MOUSEBUTTONDOWN:

            # If button pressed is left click.
            if event.button == 1:

                # If cursor position collides with button rect.
                if self.rect.collidepoint(event.pos):

                    # Playing button sound effect.
                    click_sound.play()

                    # Button is clicked.
                    return True

        # Button is not clicked.
        return False

#============================================================================
#   Class for input / entry box
#----------------------------------------------------------------------------

class Inputbox:
    def __init__(self, x, y, width, height, text, colour):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.colour = colour
        self.active = False
 
    def draw(self, surface):

        # drawing rect as input box
        pygame.draw.rect(surface, self.colour, self.rect, border_radius=6)

        #text
        text_surface = sub_font_sml.render(self.text, True, (158, 109, 63))
        text_rect = text_surface.get_rect(center=self.rect.center)

        #drawing text / textbox on screen
        surface.blit(text_surface, text_rect)

    def userinput(self, event):
        #if mouse button pressed
        if event.type == pygame.MOUSEBUTTONDOWN:
            #if mouse button is left click
            if event.button == 1:
                #if cursor collines with input box, text = ""
                self.active = self.rect.collidepoint(event.pos)
                if self.active:
                    self.text = ""

        #if a key is pressed and self.active is true

        elif event.type == pygame.KEYDOWN and self.active:
            kb_sound.play()
            #self.active false when return / enter key is pressed.
            if event.key == pygame.K_RETURN:
                self.active = False

            #when backspace key is pressed, text -1 character
            elif event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            #when any other key is pressed, add characters pressed to self.text
            else:
                self.text += event.unicode

#============================================================================
#   Class for menu / home page
#----------------------------------------------------------------------------

class Homepage:
    def __init__(self):

        #defining Buttons coordinates, sizes, text, and colour
        self.start_button = Buttons(800 ,210,280,50, "START",(230,188,140))
        self.leaderboard_button = Buttons(800,310,280,50, "LEADERBOARD",(230,188,140))
        self.quit_button = Buttons(800,410,280,50, "QUIT", (230,188,140))
        self.help_button = Buttons(915,510,50,50, "?", (230,188,140))

        #title image
        self.title = pygame.image.load('Assets/Images/title@3x.png').convert_alpha()
        self.title = pygame.transform.scale(self.title,
                                       (int(self.title.get_width()/2.2),int(self.title.get_height()/2.2)))
        
        
    
    def draw(self, surface):
        #filling screen with background colour 
        surface.fill((255,237,203,255))

        #drawing background image and title image
        screen.blit(gingham,(0,0))
        screen.blit(self.title,(50,20))

        #drawing rects as button shadows to create a 3d effect
        pygame.draw.rect(screen,(209, 162, 109),(800 ,220,280,50),border_radius=12)
        pygame.draw.rect(screen,(209, 162, 109),(800,320,280,50),border_radius=12)
        pygame.draw.rect(screen,(209, 162, 109),(800,420,280,50),border_radius=12)
        pygame.draw.rect(screen,(209, 162, 109),(915,520,50,50),border_radius=12)

        #drawing buttons
        self.start_button.draw(surface)
        self.leaderboard_button.draw(surface)
        self.quit_button.draw(surface)
        self.help_button.draw(surface)

        
    def handle_event(self, event):
         #checking if each button is clicked, returning according text, none if else
         if self.help_button.is_clicked(event):
             return "help"
         
         if self.start_button.is_clicked(event):
              return "character_select"
         
         if self.leaderboard_button.is_clicked(event):
              return "leaderboard"
         
         if self.quit_button.is_clicked(event):
              return "quit"
         return None

#============================================================================
#   Class for help / troubleshooting page
#----------------------------------------------------------------------------

class Help_Page():
    def __init__(self):

        self.audio = True
         #defining button coordinates, sizes, text, and colour
        self.close_button = Buttons(930,120,50,50, "X", (230,188,140))
        self.audio_button = Buttons2(380,120,80,40, "ON", (230,188,140))
        
        

    def draw(self, surface):

        #translucent screen fill
        overlay = pygame.Surface((screen.get_width(), screen.get_height()), pygame.SRCALPHA)
        overlay.fill((255, 237, 203, 120))  
        screen.blit(overlay, (0, 0))

        #drawing rect to create a small window
        pygame.draw.rect(screen,(158, 109, 63),(195,95,810,510),border_radius=12)
        pygame.draw.rect(screen,(255,237,203),(200 ,100,800,500),border_radius=12)

        #drawing button and button shadow
        pygame.draw.rect(screen,(209, 162, 109),(930,130,50,50),border_radius=12)
        self.close_button.draw(surface)

        screen.blit(header_font_lrg.render('Music :',True,(158, 109, 63)), (230,130))
        pygame.draw.rect(screen,(209, 162, 109),(380,130,80,40),border_radius=12)
        self.audio_button.draw(surface)

        screen.set_clip(pygame.Rect(195,95,810,510))
        pygame.draw.rect(screen,(200,150,79), (200, 300, 40, 500,))
        screen.set_clip(None)
        

    def handle_event(self,event):
        #checking if button is pressed, returning according text, none if else
        if self.close_button.is_clicked(event):
            return "home"
        
        if self.audio_button.is_clicked(event):
            if self.audio == True:
                pygame.mixer.music.pause()
                self.audio = False
                self.audio_button.text = "OFF"

            else:
                pygame.mixer.music.unpause()
                self.audio = True
                self.audio_button.text = "ON"

        return None
    
#============================================================================
#   Class for character selection page (name input & avater select)
#----------------------------------------------------------------------------

class Chara_Select():
    def __init__(self):
        
        #defining Buttons coordinates, sizes, text, and colour
        self.girl_button = Buttons2(175,425,150,50, "Select?", (230,188,140))
        self.boy_button = Buttons2(520,425,150,50, "Select?", (230,188,140))
        self.cat_button = Buttons2(880,425,150,50, "Select?", (230,188,140))
        
        self.input_box = Inputbox(545, 580, 300, 50, "e.g. John", (255, 238, 207))
        self.back_button = Buttons(30,580,50,50, "B", (230,188,140))
        self.next_button = Buttons(1060,580,100,50, "Next", (230,188,140))

        #variables
        self.chara_choice = ""
        self.warning_text = ""

        #loading images
        self.girl_icon = pygame.image.load('Assets/Images/girlICON@3x.png').convert_alpha()
        self.girl_icon = pygame.transform.scale(self.girl_icon,(int(self.girl_icon.get_width()/6.5),int(self.girl_icon.get_height()/6.5)))
        

        self.boy_icon = pygame.image.load('Assets/Images/boyICON@3x.png').convert_alpha()
        self.boy_icon = pygame.transform.scale(self.boy_icon, (int(self.boy_icon.get_width()/6.5),int(self.boy_icon.get_height()/6.5)))
        
        self.cat_icon = pygame.image.load('Assets/Images/catICON@3x.png').convert_alpha()
        self.cat_icon = pygame.transform.scale(self.cat_icon, (int(self.cat_icon.get_width()/6.5),int(self.cat_icon.get_height()/6.5)))

        self.girl_icon_alt = pygame.image.load('Assets/Images/girlICON_alt@3x.png').convert_alpha()
        self.girl_icon_alt = pygame.transform.scale(self.girl_icon_alt,(int(self.girl_icon_alt.get_width()/6.5),int(self.girl_icon_alt.get_height()/6.5)))

        self.boy_icon_alt = pygame.image.load('Assets/Images/boyICON_alt@3x.png').convert_alpha()
        self.boy_icon_alt = pygame.transform.scale(self.boy_icon_alt,(int(self.boy_icon_alt.get_width()/6.5),int(self.boy_icon_alt.get_height()/6.5)))

        self.cat_icon_alt = pygame.image.load('Assets/Images/catICON_alt@3x.png').convert_alpha()
        self.cat_icon_alt = pygame.transform.scale(self.cat_icon_alt,(int(self.cat_icon_alt.get_width()/6.5),int(self.cat_icon_alt.get_height()/6.5)))
        

    def draw(self, surface):
        #filling screen with background colour, then loadining background image in
        surface.fill((255,237,203,255))
        screen.blit(gingham,(0,0))

        #drawing text onto the screen.
        screen.blit(header_font_lrg.render('Choose a Character!', True, (158, 109, 63)), (415,40))
        screen.blit(header_font.render('Enter Name:',True,(158, 109, 63)), (320,600))
        #configurable warning text
        screen.blit(sub_font_sml.render(self.warning_text,True,(158, 109, 63)),(450,520))

        #button shadows
        pygame.draw.rect(screen,(209, 162, 109),(175,435,150,50),border_radius=12)
        pygame.draw.rect(screen,(209, 162, 109),(520,435,150,50),border_radius=12)
        pygame.draw.rect(screen,(209, 162, 109),(880,435,150,50),border_radius=12)

        pygame.draw.rect(screen,(230,188,140),(542, 577, 306, 56),border_radius=6)

       
        pygame.draw.rect(screen,(209, 162, 109),(30,590,50,50),border_radius=12)
        pygame.draw.rect(screen,(209, 162, 109),(1060,590,100,50),border_radius=12)

        #drawing buttons (and input box) onto screen
        self.girl_button.draw(surface)
        self.boy_button.draw(surface)
        self.cat_button.draw(surface)

        self.input_box.draw(surface)
        self.back_button.draw(surface)
        self.next_button.draw(surface)

        #loading icons onto screen
        screen.blit(self.girl_icon,(105, 100)) 
        screen.blit(self.boy_icon,(450, 100)) 
        screen.blit(self.cat_icon,(810, 100))
        
        #configuring button text and icons depending on variable result
        if self.chara_choice =="girl":
            self.boy_button.text = "Select?"
            self.cat_button.text = "Select?"
            self.girl_button.text = "Chosen!"
            screen.blit(self.boy_icon,(450, 100)) 
            screen.blit(self.cat_icon,(810, 100))
            screen.blit(self.girl_icon_alt,(103, 99)) 

        if self.chara_choice =="boy":
            self.girl_button.text = "Select?"
            self.cat_button.text = "Select?"
            self.boy_button.text = "Chosen!"
            screen.blit(self.girl_icon,(105, 100))  
            screen.blit(self.cat_icon,(810, 100))
            screen.blit(self.boy_icon_alt,(448, 99)) 
        
        if self.chara_choice =="cat":
            self.girl_button.text = "Select?"
            self.boy_button.text = "Select?"
            self.cat_button.text = "Chosen!"
            screen.blit(self.girl_icon,(105, 100)) 
            screen.blit(self.boy_icon,(450, 100)) 
            screen.blit(self.cat_icon_alt,(811, 100)) 


    def handle_event(self, event):
        def reset():
            self.girl_button.text = "Select?"
            self.boy_button.text = "Select?"
            self.cat_button.text = "Select?"
            self.input_box.text = "Enter Name:"
            self.chara_choice = ""
            self.warning_text=""

        #resetting all text and variables when back button is pressed
        if self.back_button.is_clicked(event):
            reset()
            return "home"
        
        #setting variable according to button pressed
        if self.girl_button.is_clicked(event):
            self.chara_choice ="girl"

        if self.boy_button.is_clicked(event):
            self.chara_choice ="boy"

        if self.cat_button.is_clicked(event):
            self.chara_choice ="cat"


        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                    if self.chara_choice == "":
                        self.warning_text = "Please choose a character."
        
                    elif self.input_box.text == "e.g. John":
                        self.warning_text = "Please enter your name."
        
                    elif self.input_box.text.strip() == "":
                        self.warning_text = "Please enter your name."
        
                    elif self.input_box.text.strip().isalpha() == False:
                        self.warning_text = "Please use only alphabets."
        
                    elif len(self.input_box.text.strip()) > 15:
                        self.warning_text = "Please do not exceed 15 characters."\
        
                    #writing user input into text file
                    else:
                        with open(filename,"a") as f:
                            f.write(str(self.chara_choice)+"," +(str(self.input_box.text.strip().capitalize())))
                        reset()
                        return "concept"
            
        if self.next_button.is_clicked(event):
            if self.chara_choice == "":
                self.warning_text = "Please choose a character."

            elif self.input_box.text == "e.g. John":
                self.warning_text = "Please enter your name."

            elif self.input_box.text.strip() == "":
                self.warning_text = "Please enter your name."

            elif self.input_box.text.strip().isalpha() == False:
                self.warning_text = "Please use only alphabets."

            elif len(self.input_box.text.strip()) > 15:
                self.warning_text = "Please do not exceed 15 characters."\

            #writing user input into text file
            else:
                with open(filename,"a") as f:
                    f.write(str(self.chara_choice)+"," +(str(self.input_box.text.strip().capitalize())))
                reset()
                return "concept"

        return None
    
#============================================================================
#   Class for mathematics concept selection page
#----------------------------------------------------------------------------

class Concept_Select():
    def __init__(self):
        #defining Buttons coordinates, sizes, text, and colour
        self.back_button = Buttons(30,580,50,50, "B", (230,188,140))
        self.next_button = Buttons(1060,580,100,50, "Next", (230,188,140))

        
        self.addition_button = Buttons2(150,150,250,180, "Addition\n 1+2=3", (230,188,140))
        self.subtraction_button = Buttons2(475,150,250,180, "Subtraction\n   3-2=1", (230,188,140))
        self.multiplication_button = Buttons2(800,150,250,180, "Multiplication\n    2x2=4", (230,188,140))
        self.fractions_button = Buttons2(150,360,250,180, "  Fractions\n(1/2)+(1/2)=1", (230,188,140))
        self.exponents_button = Buttons2(475,360,250,180, "Exponents\n  2²=4", (230,188,140))
        self.algebra_button = Buttons2(800,360,250,180, "Algebra\n x+x=2x", (230,188,140))

        #variables
        self.user_name = ""
        self.concept_choice=""
        self.warning_text=""

        #loading images
        self.pipingbag1 = pygame.image.load('Assets/Images/pipingbag_STRAWBERRY@3x.png').convert_alpha()
        self.pipingbag1 = pygame.transform.scale(self.pipingbag1,(int(self.pipingbag1.get_width()/7.5), int(self.pipingbag1.get_height()/7.5)))

        self.pipingbag2 = pygame.image.load('Assets/Images/pipingbag_CHOCO@3x.png').convert_alpha()
        self.pipingbag2 = pygame.transform.scale(self.pipingbag2,(int(self.pipingbag2.get_width()/7.5), int(self.pipingbag2.get_height()/7.5)))

        self.pipingbag3 = pygame.image.load('Assets/Images/pipingbag_LEMON@3x.png').convert_alpha()
        self.pipingbag3 = pygame.transform.scale(self.pipingbag3,(int(self.pipingbag3.get_width()/7.5), int(self.pipingbag3.get_height()/7.5)))

    
    def draw(self, surface):
        #filling screen with background oclour and loading background image
        surface.fill((255,237,203,255))
        screen.blit(gingham,(0,0))

        #loading text onto screen
        welcome_surf=header_font_XL.render(f"Welcome, {self.user_name}!",True,(158, 109, 63))
        screen.blit(welcome_surf,(100,50))
        screen.blit(sub_font.render('Pick a maths concept~', True, (158, 109, 63)),((welcome_surf.get_width()+140) ,50))

        #button shadows
        pygame.draw.rect(screen,(209, 162, 109),(30,590,50,50),border_radius=12)
        pygame.draw.rect(screen,(209, 162, 109),(1060,590,100,50),border_radius=12)

        pygame.draw.rect(screen,(209, 162, 109),(150,160,250,180),border_radius=12)
        pygame.draw.rect(screen,(209, 162, 109),(475,160,250,180),border_radius=12)
        pygame.draw.rect(screen,(209, 162, 109),(800,160,250,180),border_radius=12)
        pygame.draw.rect(screen,(209, 162, 109),(150,370,250,180),border_radius=12)
        pygame.draw.rect(screen,(209, 162, 109),(475,370,250,180),border_radius=12)
        pygame.draw.rect(screen,(209, 162, 109),(800,370,250,180),border_radius=12)

        #loading buttons onto screen
        self.back_button.draw(surface)
        self.next_button.draw(surface)

        self.addition_button.draw(surface)
        self.subtraction_button.draw(surface)
        self.multiplication_button.draw(surface)
        self.fractions_button.draw(surface)
        self.exponents_button.draw(surface)
        self.algebra_button.draw(surface)
        
        #loading text showing what maths concept the user chose
        if self.concept_choice != "":
            screen.blit(sub_font_sml.render(f"You Selected: {self.concept_choice.capitalize()}", True, (158, 109, 63)),(450,580))

        #configurable warning text
        screen.blit(sub_font_sml.render(self.warning_text, True, (158, 109, 63)),(100,620))

        #loading decoration images (piping bags)
        screen.blit(self.pipingbag1,(200,300))
        screen.blit(self.pipingbag2,(530,300))
        screen.blit(self.pipingbag3,(850,300))


    def handle_event(self,event):

        #getting user name from text file
        if self.user_name == "":
            try: 
                with open(filename,"r") as f:
                    lines = f.readlines()
                    if lines:
                        #variable for latest line
                        last_record = lines[-1].strip()
                        #variables to print list values.
                        chara, name = last_record.strip().split(",")
                        self.user_name = name.capitalize()

            except FileNotFoundError:
                return "quit"
        
        #setting variable according to button pressed, resetting warning text
        if self.addition_button.is_clicked(event):
            self.concept_choice = "addition"
            self.warning_text = ""
        
        if self.subtraction_button.is_clicked(event):
            self.concept_choice = "subtraction"
            self.warning_text = ""
        
        if self.multiplication_button.is_clicked(event):
            self.concept_choice = "multiplication"
            self.warning_text = ""
        
        if self.fractions_button.is_clicked(event):
            self.concept_choice = "fractions"
            self.warning_text = ""
        
        if self.exponents_button.is_clicked(event):
            self.concept_choice = "exponents"
            self.warning_text = ""

        if self.algebra_button.is_clicked(event):
            self.concept_choice = "algebra"
            self.warning_text = ""

        #deleting to current line from text file if back button is pressed to prevent crashes, returning home
        if self.back_button.is_clicked(event):
            self.user_name=""
            self.concept_choice = ""
            self.warning_text = ""
            try:
                with open(filename,"r") as f:
                    lines = f.readlines()
                    if lines:
                        lines = lines[:-1]
                        with open(filename,"w") as f:
                            f.writelines(lines)
                            return "home"
            except FileNotFoundError:
                return "quit"
        
        #writing concept choice into text file when next button is pressed, returning text for next page
        if self.next_button.is_clicked(event):
            if self.concept_choice != "":
                with open(filename,"a") as f:
                    f.write(","+str(self.concept_choice))

                    self.concept_choice = ""
                    self.warning_text = ""
                    return "difficulty"
            else:
                #cofiguring warning text if user atttempts to continue without choosing a concept.
                self.warning_text = "You have not selected a maths concept. Please choose one of the above."
        
        return None

#============================================================================
#   Class for difficulty selection page
#----------------------------------------------------------------------------


class Difficulty_Select():
    def __init__(self):

        self.warning_text = "You haven't chosen your \n difficulty level yet!"

        #variables
        self.difficulty_choice = ""
        self.chara = ""
        self.sprite = "normal"
        self.chara_img = ""

        self.base_y = -50
        self.bobbing = True
        self.time = 0
        self.pause_timer =0
        self.bobbing_active = False
        self.total_time = 0
        self.blip_played = False
        
        #defining buttons coordinates size, text, and colour
        self.easy_button = Buttons2(470,150,140,50,"Easy", (230,188,140))
        self.med_button = Buttons2(650,150,140,50,"Medium", (230,188,140))
        self.hard_button = Buttons2(830,150,140,50,"Hard", (230,188,140))

        self.back_button = Buttons(30,580,50,50, "B", (230,188,140))
        self.play_button = Buttons(1060,580,100,50, "Play", (230,188,140))
        
        
        #images
        self.girl_sprite = pygame.image.load('Assets/Images/girlspr_norm@3x.png').convert_alpha()
        self.girl_sprite = pygame.transform.scale(self.girl_sprite, (int(self.girl_sprite.get_width()/4),int(self.girl_sprite.get_height()/4)))

        self.girl_sprite_alt1 = pygame.image.load('Assets/Images/girlspr_frenzy@3x.png').convert_alpha()
        self.girl_sprite_alt1 = pygame.transform.scale(self.girl_sprite_alt1, (int(self.girl_sprite_alt1.get_width()/4),int(self.girl_sprite_alt1.get_height()/4)))

        self.boy_sprite = pygame.image.load('Assets/Images/boyspr_norm@3x.png').convert_alpha()
        self.boy_sprite = pygame.transform.scale(self.boy_sprite, (int(self.boy_sprite.get_width()/4),int(self.boy_sprite.get_height()/4)))

        self.boy_sprite_alt1 = pygame.image.load('Assets/Images/boyspr_frenzy@3x.png').convert_alpha()
        self.boy_sprite_alt1 = pygame.transform.scale(self.boy_sprite_alt1, (int(self.boy_sprite_alt1.get_width()/4),int(self.boy_sprite_alt1.get_height()/4)))

        self.cat_sprite = pygame.image.load('Assets/Images/catspr_norm@3x.png').convert_alpha()
        self.cat_sprite = pygame.transform.scale(self.cat_sprite, (int(self.cat_sprite.get_width()/4),int(self.cat_sprite.get_height()/4)))

        self.cat_sprite_alt1 = pygame.image.load('Assets/Images/catspr_frenzy@3x.png').convert_alpha()
        self.cat_sprite_alt1 = pygame.transform.scale(self.cat_sprite_alt1, (int(self.cat_sprite_alt1.get_width()/4),int(self.cat_sprite_alt1.get_height()/4)))

        self.speech_bubble = pygame.image.load('Assets/Images/speechbubble@3x.png').convert_alpha()
        self.speech_bubble = pygame.transform.scale(self.speech_bubble, (int(self.speech_bubble.get_width()/2.2),int(self.speech_bubble.get_height()/2.2)))


        
        #defining sprites according to variable
        self.sprites = {
            "girl": {
            "normal": self.girl_sprite,
            "happy": self.girl_sprite_alt1
            },
        "boy": {
            "normal": self.boy_sprite,
            "happy": self.boy_sprite_alt1
            },
        "cat": {
            "normal": self.cat_sprite,
            "happy": self.cat_sprite_alt1
            }
        }


    def draw(self, surface):
        surface.fill((255,237,203,255))
        
        screen.blit(gingham,(0,0))

        screen.blit(header_font_XL.render("Choose your difficulty!",True,(158, 109, 63)), (460,80))

        pygame.draw.rect(screen,(209, 162, 109),(470,160,140,50),border_radius=12)
        pygame.draw.rect(screen,(209, 162, 109),(650,160,140,50),border_radius=12)
        pygame.draw.rect(screen,(209, 162, 109),(830,160,140,50),border_radius=12)

        self.easy_button.draw(surface)
        self.med_button.draw(surface)
        self.hard_button.draw(surface)

        draw_y = self.base_y
        if self.bobbing_active:
            self.total_time += delta_time
        
            if self.difficulty_choice !=  "" and self.total_time<3:
                if self.bobbing:
                    if not self.blip_played:
                        if self.chara == "cat":
                            blip.play(loops=4)
                        elif self.chara == "boy":
                            blip2.play(loops=8)
                        elif self.chara == "girl":
                            blip3.play(loops=6)
                        self.blip_played = True

                    self.sprite = "happy"
                    
                    self.time += delta_time
                    draw_y = self.base_y + math.sin(self.time*20)*10

                    if self.time >= 1:
                        self.time = 0
                        self.bobbing = False
                        self.pause_timer = 0

                else:
                
                    self.sprite = "normal"
                    self.pause_timer += delta_time
                    if self.pause_timer >= 0.5:
                        self.blip_played = False
                        self.bobbing = True
            else:
                self.sprite = "normal"

                self.bobbing_active = False
                self.blip_played = True
                self.time = 0
                self.pause_timer =0
                self.total_time = 0
                draw_y = self.base_y

        if self.chara in self.sprites:
            self.chara_img = self.sprites[self.chara][self.sprite]
            screen.blit(self.chara_img, (-100, draw_y))
            


        screen.blit(self.speech_bubble,(350,100))

        screen.blit(sub_font_sml.render(self.warning_text, True, (158, 109, 63)),(570 ,360))

        pygame.draw.rect(screen,(209, 162, 109),(30,590,50,50),border_radius=12)
        pygame.draw.rect(screen,(209, 162, 109),(1060,590,100,50),border_radius=12)
        self.back_button.draw(surface)
        self.play_button.draw(surface)


    def handle_event(self, event):
        if self.easy_button.is_clicked(event):
            self.difficulty_choice = "easy"
            self.warning_text = "     You chose Easy!\n\nThis'll be a piece of cake!"
            
            self.bobbing_active = True
            self.blip_played = False
            

        if self.med_button.is_clicked(event):
            self.difficulty_choice = "medium"
            self.warning_text = "    You chose Medium!\n\n     We can do this!"
            
            self.bobbing_active = True
            self.blip_played = False
        
        if self.hard_button.is_clicked(event):
            self.difficulty_choice = "hard"
            self.warning_text = "     You chose Hard!\n\n   This is gonna be a \n       challenge..."
            
            self.bobbing_active = True
            self.blip_played = False

        if self.chara == "":
            try: 
                with open(filename,"r") as f:
                    lines = f.readlines()
                    if lines:
                        #variable for latest line
                        last_record = lines[-1].strip()
                        #variables to print list values.
                        chara, name, concept = last_record.strip().split(",")
                        self.chara = chara

            except FileNotFoundError:
                return "quit"

        if self.back_button.is_clicked(event):
            self.difficulty_choice = ""
            self.chara=""
            self.sprite = "normal"
            self.warning_text = "You haven't chosen your \n difficulty level yet!"
            self.bobbing = True
            self.time = 0
            self.pause_timer =0
            self.total_time = 0
            self.bobbing_active = False
            self.blip_played = False

            try:
                with open(filename,"r") as f:
                    lines = f.readlines()
                    if lines:
                        lines = lines[:-1]
                        with open(filename,"w") as f:
                            f.writelines(lines)
                            return "home"
            except FileNotFoundError:
                return "quit"
            
        if self.play_button.is_clicked(event):
            if self.difficulty_choice != "":
                with open(filename,"r") as f:
                    lines = f.readlines()
                    if lines:
                        #variable for latest line
                        last_record = lines[-1].strip()
                        #variables to print list values.
                        chara, name, concept = last_record.strip().split(",")

                        self.user_name = name

                    if self.difficulty_choice == "easy":
                        with open(easy_leader,"a") as f1:
                            f1.write(str(concept)+","+str(name)+"\n")

                    elif self.difficulty_choice == "medium":
                        with open(med_leader,"a") as f2:
                            f2.write(str(concept)+","+str(name)+"\n")
                    
                    elif self.difficulty_choice == "hard":
                        with open(hard_leader,"a") as f3:
                            f3.write(str(concept)+","+str(name)+"\n")

                    with open(filename,"a") as f:
                        f.write(","+str(self.difficulty_choice)+"\n") 

                    self.difficulty_choice = ""
                    self.chara=""
                    self.sprite = "normal"
                    self.warning_text = "You haven't chosen your \n difficulty level yet!"
                    pygame.time.set_timer(TIMER_EVENT, 1000)
                    return "gameplay"
        return None
        

#============================================================================
#   Class for gameplay
#----------------------------------------------------------------------------
class MultiQuestion():
    def __init__(self):
        self.ans_button1 = Buttons3(235,600,160,50, "Button 1", (230,188,140))
        self.ans_button2 = Buttons3(425,600,160,50, "Button 2", (230,188,140))
        self.ans_button3 = Buttons3(615,600,160,50, "Button 3", (230,188,140))
        self.ans_button4 = Buttons3(805,600,160,50, "Button 4", (230,188,140))
        self.back_button = Buttons(1110,590,50,50, "B", (230,188,140))
        
        self.question_text = ""
        self.question_answer = ""
        self.wrong_answer=""
        self.wrong_answer2=""
        self.wrong_answer3=""

        self.answers_order = random.randint(1,4)
        self.counter_text = ""
        self.timed_questions_text = ""

        self.difficulty_settings = {
            "easy": {
                "add_sub": (1, 15),
                "multiply": (1, 10),
                "divide" :(2,3),
                "power": (2,2),
                "symbol" : ""
                },
            "medium": {
                "add_sub": (10, 25),
                "multiply": (1, 15),
                "divide": (2,10),
                "power": (2,3),
                "symbol" : "x"

                },
            "hard": {
                "add_sub": (20, 70),
                "multiply": (10, 30),
                "divide": (2,10),
                "power": (2,3),
                "symbol": "÷",
                }
                }
        
    def draw(self, surface):
        global points, timed_questions
        pygame.draw.rect(screen,(209, 162, 109), (196, 496, 808,208), border_radius=12)
        pygame.draw.rect(screen,(255,237,203), (200,500,800,200,),border_radius=12)  

        #Back Button
        pygame.draw.rect(screen,(209, 162, 109),(1110,600,50,50),border_radius=12)
        self.back_button.draw(surface)

        #question box thing
        pygame.draw.rect(surface,(209, 162, 109), (380, 520, 450,50), border_radius=6)
        pygame.draw.rect(surface,(255, 238, 207), (382, 522, 446,46), border_radius=6)

        surface.blit(sub_font_lrg.render(self.question_text, True, (158, 109, 63)),(530 ,525))

        surface.blit(sub_font_lrg.render(self.timed_questions_text, True, (158, 109, 63)),(880 ,525))
        
        surface.blit(sub_font_sml.render(f"SCORE: {str(points)}", True, (158, 109, 63)),(230 ,525))
        surface.blit(sub_font_sml.render(self.counter_text, True, (158, 109, 63)),(230 ,550))

        pygame.draw.rect(surface,(209, 162, 109), (233, 598, 164,54), border_radius=6)
        pygame.draw.rect(surface,(209, 162, 109), (423, 598, 164,54), border_radius=6)
        pygame.draw.rect(surface,(209, 162, 109), (613, 598, 164,54), border_radius=6)
        pygame.draw.rect(surface,(209, 162, 109), (803, 598, 164,54), border_radius=6)
        self.ans_button1.draw(surface)
        self.ans_button2.draw(surface)
        self.ans_button3.draw(surface)
        self.ans_button4.draw(surface)

    def handle_event(self, event):
        global points, answer_combo, answer_correct, answer_wrong, timed_questions, bonus_points, counter
        
        if counter > 0 and timed_questions <5:
            self.counter_text = f"00 : {str(counter)}"
            self.timed_questions_text = f"{timed_questions} / 5"
        else: 
            self.counter_text = ""
            self.timed_questions_text = ""


        def format_number(numerator, denominator):
            frac = Fraction(numerator, denominator)
            if frac.is_integer():
                return int(frac)
            else:
                return str(frac)

        if self.question_text == "":
            try: 
                with open(filename,"r") as f:
                    lines = f.readlines()
                    if lines:
                        #variable for latest line
                        last_record = lines[-1].strip()
                        #variables to print list values.
                        chara, name, concept, difficulty = last_record.strip().split(",")
                        settings = self.difficulty_settings[difficulty]

                        if concept == "addition":

                            low, high = settings["add_sub"]

                            num1 = random.randint(low, high)
                            num2 = random.randint(low, high)
                            num3 = random.randint(low,high)

                            if num3 == num1 or num3 == num2: 
                                while num3 == num2 or num3 == num2:
                                    num3 = random.randint(low,high)

                            self.question_answer = f"{num1 + num2}"
                            self.wrong_answer= f"{num1 + num3}"
                            self.wrong_answer2 = f"{num1 - num2}"
                            self.wrong_answer3 = f"{num3}"

                            self.question_text = f"{num1}+{num2}"
                            
                        if concept == "subtraction":

                            low, high = settings["add_sub"]

                            num1 = random.randint(low, high)
                            num2 = random.randint(low, high)
                            num3 = random.randint(low,high)

                            if num3 == num1 or num3 ==num2: 
                                while num3 == num2 or num3 == num2:
                                    num3 = random.randint(low,high)

                            self.question_answer = f"{num1 - num2}"
                            self.wrong_answer= f"{num1 - num3}"
                            self.wrong_answer2 = f"{num1 + num2}"
                            self.wrong_answer3 = f"{num1*num3}"
                            
                            self.question_text = f"{num1}-{num2}"

                        if concept == "multiplication":

                            low, high = settings["multiply"]

                            num1 = random.randint(low, high)
                            num2 = random.randint(low, high)
                            num3 = random.randint(low,high)
                            
                            if num3 == num1 or num3 == num2: 
                                while num3 == num1 or num3 ==num2:
                                    num3 = random.randint(low,high)

                            self.question_answer = f"{num1 * num2}"
                            self.wrong_answer= f"{num1 * num3}"
                            self.wrong_answer2 = f"{num1 - num2}"
                            self.wrong_answer3 = f"{num2+num3}"

                            self.question_text = f"{num1}x{num2}"

                        if concept == "fractions":
                            low, high = settings["multiply"]
                            divide_low, divide_high = settings["divide"]
                            symbol = settings["symbol"]

                            num1 = random.randint(low,high)
                            num2 = random.randint(low,high)
                            denom = random.randint(divide_low, divide_high)
                            denom2 = random.randint(divide_low, divide_high)
                                
                            if difficulty == "easy":
                                self.question_text = f"({num1}/{denom}){symbol}({num2}/{denom})"

                                self.question_answer = format_number(num1+num2,denom)

                                self.wrong_answer = format_number(num1*num2,denom)

                                self.wrong_answer2 = f"{num2*denom}"

                                self.wrong_answer3 = format_number(num1-num2, denom)
                                                                
                            elif difficulty == "medium":
                                self.question_text = f"({num1}/{denom}){symbol}({num2}/{denom2})"

                                self.question_answer = format_number(num1*num2,denom*denom2)
                                self.wrong_answer = format_number(num1+num2,denom+denom2)
                                self.wrong_answer2 = format_number(num1*denom,num2*denom)
                                self.wrong_answer3 = f"{num2*denom}"
                                
                            elif difficulty == "hard":
                                self.question_text = f"({num1}/{denom}){symbol}({num2}/{denom2})"
                            
                                self.question_answer = format_number(num1*denom2,num2*denom)
                                self.wrong_answer = format_number(num1*denom,num2*denom2)
                                self.wrong_answer2 = format_number(num1-num2,denom-denom2)
                                self.wrong_answer3 = f"{num2*denom*num1}"
 

                        if concept == "exponents":
                            low, high = settings["multiply"]
                            power_low, power_high = settings["power"]

                            power_num = random.randint(power_low, power_high)

                            num1 = random.randint(low,high)
                            num2 = random.randint(low,high)
                            if num2 == num1 or num2 == power_num:
                                while num2 == num1 or num2 == power_num:
                                    num2 = random.randint(low,high)

                            if power_num == 1:
                                power_text = "\N{SUPERSCRIPT ONE}"
                                
                            elif power_num == 2:
                                power_text = "\N{SUPERSCRIPT TWO}"

                            elif power_num == 3:
                                power_text = "\N{SUPERSCRIPT THREE}"

                            self.question_answer = f"{num1**power_num}"

                            self.wrong_answer = f"{num1+num2}"

                            self.wrong_answer2 = format_number(num2,num1)
                            self.wrong_answer3 = f"{num2**power_num}"

                            self.question_text = f"{num1}{power_text}"

                        if concept == "algebra":
                            low, high = settings["multiply"]
                            low2, high2 = settings["divide"]
                            power_low, power_high = settings["power"]

                            num1 = random.randint(low,high)
                            num2 = random.randint(low,high)
                            num3 = random.randint(low, high)

                            if num3 == num1 or num3 == num2:
                                while num3 == num1 or num3 == num2:
                                    num3 = random.randint(low, high)

                            if difficulty == "easy":
                                self.question_text = f"{num1}a = {num2}, a=?"
                                self.question_answer = format_number(num2,num1)

                                self.wrong_answer = format_number(num2,num3)
                                self.wrong_answer2 = f"{num1-num3}"
                                self.wrong_answer3 = f"{num1+num3}"

                            if difficulty ==  "medium" or "hard":
                                hard_num1 = random.randint(low2,high2)
                                hard_num2 = random.randint(low2,high2)
                                hard_num3 = random.randint(low2,high2)
    
                                power_num = random.randint(power_low, power_high)
                                power_num2 = random.randint(power_low, power_high)
                                
                                if power_num == 1:
                                    power_text = "\N{SUPERSCRIPT ONE}"
                                    
                                elif power_num == 2:
                                    power_text = "\N{SUPERSCRIPT TWO}"

                                elif power_num == 3:
                                    power_text = "\N{SUPERSCRIPT THREE}"


                                if power_num2 == 1:
                                    power_text2 = "\N{SUPERSCRIPT ONE}"
                                    
                                elif power_num2 == 2:
                                    power_text2 = "\N{SUPERSCRIPT TWO}"
    
                                elif power_num2 == 3:
                                    power_text2 = "\N{SUPERSCRIPT THREE}"

                                if difficulty == "medium":
                                    self.question_text = f"{num1}a{power_text} x {num2}a{power_text2}"
    
                                    self.question_answer= f"{num1*num2}a^{power_num+power_num2}"
                                    self.wrong_answer = f"{num1*num2}a^{power_num**power_num2}"
                                    self.wrong_answer2 = f"{num1-num2}a^{power_num2}"
                                    self.wrong_answer3 = f"{num1+num2}a^{power_num-power_num2}"
                                    
                                elif difficulty == "hard":
                                    self.question_text = f"{hard_num1}a{power_text}({hard_num2}a + {hard_num3})"
    
                                    self.question_answer = f"{hard_num1*hard_num2}a^{power_num+1}+{hard_num1*hard_num3}a^{power_num}"
                                    self.wrong_answer = f"{hard_num1+hard_num2}a^{power_num}+{hard_num1+hard_num3}a^{power_num}"
                                    self.wrong_answer2 = f"{hard_num1*hard_num2}a+{hard_num1*hard_num3}a"
                                    self.wrong_answer3 = f"{hard_num1-hard_num2}a^{power_num*2}"
         
            except FileNotFoundError:
                return "quit"

        if self.wrong_answer == self.question_answer:
            while self.wrong_answer == self.question_answer:
                self.wrong_answer = random.randint(0,100)

        elif self.wrong_answer2 == self.question_answer:
            while self.wrong_answer2 == self.question_answer:
                self.wrong_answer2 = random.randint(0,100)

        elif self.wrong_answer3 == self.question_answer:
            while self.wrong_answer3 == self.question_answer:
                self.wrong_answer3 = random.randint(0,100)
            
        if self.answers_order ==1:
            self.ans_button1.text = str(self.question_answer)
            self.ans_button2.text = str(self.wrong_answer)
            self.ans_button3.text = str(self.wrong_answer2)
            self.ans_button4.text = str(self.wrong_answer3)

        elif self.answers_order == 2:
            self.ans_button1.text = str(self.wrong_answer3)
            self.ans_button2.text = str(self.question_answer)
            self.ans_button3.text = str(self.wrong_answer)
            self.ans_button4.text = str(self.wrong_answer2)

        elif self.answers_order == 3:
            self.ans_button1.text = str(self.wrong_answer2)
            self.ans_button2.text = str(self.wrong_answer3)
            self.ans_button3.text = str(self.question_answer)
            self.ans_button4.text = str(self.wrong_answer)

        elif self.answers_order == 4:
            self.ans_button1.text = str(self.wrong_answer)
            self.ans_button2.text = str(self.wrong_answer2)
            self.ans_button3.text = str(self.wrong_answer3)
            self.ans_button4.text = str(self.question_answer)

        def reset():
            self.question_text = ""
            self.question_answer = ""
            self.wrong_answer=""
            self.wrong_answer2=""
            self.wrong_answer3=""
            self.answers_order = random.randint(1,4)


        if self.ans_button1.is_clicked(event):
            if self.ans_button1.text == self.question_answer:
                points += 100 
                answer_combo +=1
                answer_correct = True
                if counter > 0 and timed_questions <= 5: 
                    timed_questions += 1
                    bonus_points += 100
                reset()
                         
            else:
                points -= 40
                answer_combo = 0
                answer_wrong = True
                reset()
            return True     

        if self.ans_button2.is_clicked(event):
            if self.ans_button2.text == self.question_answer:
                points += 100 
                answer_combo +=1
                answer_correct = True
                if counter > 0 and timed_questions <= 5: 
                    timed_questions += 1
                    bonus_points += 100
                
                reset()
            else:
                points -= 40 
                answer_combo = 0
                answer_wrong = True
                reset()
            return True

        if self.ans_button3.is_clicked(event):
            if self.ans_button3.text == self.question_answer:
                points += 100 
                answer_combo +=1
                answer_correct = True
                if counter > 0 and timed_questions <= 5: 
                    timed_questions += 1
                    bonus_points += 100
                reset()
            else:
                points -= 40
                answer_combo = 0
                answer_wrong = True
                reset()
            return True
            
        if self.ans_button4.is_clicked(event):
            if self.ans_button4.text == self.question_answer:
                points += 100
                answer_combo +=1
                answer_correct = True
                if counter > 0 and timed_questions <= 5: 
                    timed_questions += 1
                    bonus_points += 100
                reset()
            else:
                points -= 40
                answer_combo = 0
                answer_wrong = True
                reset()
            return True
        return None
    
    def back_event(self, event):
        global points, answer_combo, timed_questions, counter, bonus_points

        if self.back_button.is_clicked(event):
            points = 0
            answer_combo = 0
            bonus_points = 0
            timed_questions = 0

            self.question_text = ""
            self.question_answer = ""
            self.wrong_answer=""
            self.wrong_answer2=""
            self.wrong_answer3=""

            counter =30
            return "home"
        return None

class InputQuestion: 
    
    def __init__(self):
        self.input_box = Inputbox(325,600,450,50, "enter ans here", (255, 238, 207))
        self.inputbox_button = Buttons3(800,600,80,50, "ENTER", (230,188,140))
        self.back_button = Buttons(1110,590,50,50, "B", (230,188,140))

        self.question_text = ""
        self.question_answer = ""
        self.counter_text = ""
        self.timed_questions_text = ""

        self.difficulty_settings = {
            "easy": {
                "add_sub": (1, 15),
                "multiply": (1, 10),
                "divide" :(2,3),
                "power": (2,2),
                "symbol" : ""
                },
            "medium": {
                "add_sub": (10, 25),
                "multiply": (1, 15),
                "divide": (2,10),
                "power": (2,3),
                "symbol" : "x"

                },
            "hard": {
                "add_sub": (20, 70),
                "multiply": (10, 30),
                "divide": (2,10),
                "power": (2,3),
                "symbol": "÷",
                }
                }
                
    def draw(self, surface):
        global points, timed_questions

        pygame.draw.rect(screen,(209, 162, 109), (196, 496, 808,208), border_radius=12)
        pygame.draw.rect(screen,(255,237,203), (200,500,800,200,),border_radius=12) 

        #Back Button
        pygame.draw.rect(screen,(209, 162, 109),(1110,600,50,50),border_radius=12)
        self.back_button.draw(surface)

        #question box thing
        pygame.draw.rect(surface,(209, 162, 109), (380, 520, 450,50), border_radius=6)
        pygame.draw.rect(surface,(255, 238, 207), (382, 522, 446,46), border_radius=6)

        surface.blit(sub_font_lrg.render(self.question_text, True, (158, 109, 63)),(530 ,525))

        surface.blit(sub_font_lrg.render(self.timed_questions_text, True, (158, 109, 63)),(880 ,525))
        
        surface.blit(sub_font_sml.render(f"SCORE: {str(points)}", True, (158, 109, 63)),(230 ,525))
        surface.blit(sub_font_sml.render(self.counter_text, True, (158, 109, 63)),(230 ,550))

        
        pygame.draw.rect(surface,(209, 162, 109), (323, 598, 454,54), border_radius=6)
        pygame.draw.rect(surface,(209, 162, 109), (798, 598, 84,54), border_radius=6)
        self.input_box.draw(surface)
        self.inputbox_button.draw(surface)

    def handle_event(self, event):
        def format_number(numerator, denominator):
            frac = Fraction(numerator, denominator)
            if frac.is_integer():
                return int(frac)
            else:
                return str(frac)
            
        global counter, timed_questions

        if counter > 0 and timed_questions <5 :
            self.counter_text = f"00 : {str(counter)}"
            self.timed_questions_text = f"{timed_questions} / 5"
        else: 
            self.counter_text = ""
            self.timed_questions_text = ""

        if self.question_text == "":
            try: 
                with open(filename,"r") as f:
                    lines = f.readlines()
                    if lines:
                        #variable for latest line
                        last_record = lines[-1].strip()
                        #variables to print list values.
                        chara, name, concept, difficulty = last_record.strip().split(",")
                        settings = self.difficulty_settings[difficulty]
                        if concept == "addition":
                            low, high = settings["add_sub"]
                            num1 = random.randint(low, high)
                            num2 = random.randint(low, high)
                            self.question_answer = f"{num1 + num2}"
                            self.question_text = f"{num1}+{num2}"

                        elif concept == "subtraction":
                            low, high = settings["add_sub"]
                            num1 = random.randint(low, high)
                            num2 = random.randint(low, high)
                            self.question_answer = f"{num1 - num2}"
                            self.question_text = f"{num1}-{num2}"

                        elif concept == "multiplication":
                            low, high = settings["multiply"]
                            num1 = random.randint(low, high)
                            num2 = random.randint(low, high)
                            self.question_answer = f"{num1 * num2}"
                            self.question_text = f"{num1}×{num2}"

                        elif concept == "fractions":
                            low, high = settings["multiply"]
                            divide_low, divide_high = settings["divide"]
                            symbol = settings["symbol"]

                            num1 = random.randint(low,high)
                            num2 = random.randint(low,high)
                            denom = random.randint(divide_low, divide_high)
                            denom2 = random.randint(divide_low, divide_high)

                            if difficulty == "easy":
                                self.question_text = f"({num1}/{denom}){symbol}({num2}/{denom})"
                                self.question_answer = format_number(num1+num2,denom)
                    
                            elif difficulty == "medium":
                                self.question_text = f"({num1}/{denom}){symbol}({num2}/{denom2})"
                                self.question_answer = format_number(num1*num2,denom*denom2)


                            elif difficulty == "hard":
                                self.question_text = f"({num1}/{denom}){symbol}({num2}/{denom2})"
                                self.question_answer = format_number(num1*denom2,num2*denom)

                                
                        elif concept == "exponents":
                            low, high = settings["multiply"]
                            power_low, power_high = settings["power"]

                            num1 = random.randint(low,high)
                            power_num = random.randint(power_low, power_high)

                            if power_num == 1:
                                power_text = "\N{SUPERSCRIPT ONE}"
                                
                            elif power_num == 2:
                                power_text = "\N{SUPERSCRIPT TWO}"

                            elif power_num == 3:
                                power_text = "\N{SUPERSCRIPT THREE}"

                            self.question_answer = f"{num1**power_num}"
                            self.question_text = f"{num1}{power_text}"

                        elif concept == "algebra":
                            low, high = settings["multiply"]
                            low2, high2 = settings["divide"]
                            power_low, power_high = settings["power"]

                            num1 = random.randint(low,high)
                            num2 = random.randint(low,high)

                            hard_num1 = random.randint(low2,high2)
                            hard_num2 = random.randint(low2,high2)
                            hard_num3 = random.randint(low2,high2)


                            power_num = random.randint(power_low, power_high)
                            power_num2 = random.randint(power_low, power_high)

                            if power_num == 1:
                                power_text = "\N{SUPERSCRIPT ONE}"
                                
                            elif power_num == 2:
                                power_text = "\N{SUPERSCRIPT TWO}"

                            elif power_num == 3:
                                power_text = "\N{SUPERSCRIPT THREE}"

                            elif power_num == 4:
                                power_text = "\N{SUPERSCRIPT FOUR}"

                            if power_num2 == 1:
                                power_text2 = "\N{SUPERSCRIPT ONE}"
                                
                            elif power_num2 == 2:
                                power_text2 = "\N{SUPERSCRIPT TWO}"

                            elif power_num2 == 3:
                                power_text2 = "\N{SUPERSCRIPT THREE}"

                            if difficulty == "easy":
                                self.question_text = f"{num1}a = {num2}, a=?"
                                self.question_answer = format_number(num2,num1)


                            elif difficulty == "medium":
                                self.question_text = f"{num1}a{power_text} x {num2}a{power_text2}"
                                self.question_answer= f"{num1*num2}a^{power_num+power_num2}"
                                
                            elif difficulty == "hard":
                                self.question_text = f"{hard_num1}a{power_text}({hard_num2}a + {hard_num3})"

                                self.question_answer = f"{hard_num1*hard_num2}a^{power_num+1}+{hard_num1*hard_num3}a^{power_num}"
                                print(self.question_answer)
            except FileNotFoundError:
                return "quit"

        def submit_question():
            global points, answer_combo, answer_correct, answer_wrong, timed_questions, counter, bonus_points

            if str(self.input_box.text.strip()) == str(self.question_answer):
                points += 100
                answer_combo +=1
                answer_correct = True
                if counter > 0 and timed_questions <= 5: 
                    timed_questions += 1
                    bonus_points += 100
            else:
                points -= 40
                answer_combo =0
                answer_wrong = True


            self.input_box.text = "enter ans here"
            self.question_text = ""
            self.question_answer = ""

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                submit_question()
                return True

        if self.inputbox_button.is_clicked(event):
            submit_question()
            return True

    def back_event(self, event):
        global points, answer_combo, counter, timed_questions, bonus_points

        if self.back_button.is_clicked(event):
            print(answer_combo)
            points = 0
            answer_combo = 0
            timed_questions = 0
            bonus_points = 0
            self.question_text = ""
            self.input_box.text = "enter ans here"
            self.question_answer = ""
            counter =15
            return "home"
        return None

class GameScreen():
    def __init__(self):
        self.back_button = Buttons(1110,590,50,50, "B", (230,188,140))

        self.difficulty_choice = ""
        self.chara = ""
        self.sprite = "normal"
        self.chara_img = ""
        self.time = 0

        self.base_y = 310
        self.bobbing = False
        self.ani_time = 0

        self.bonus_given = False

        self.timed_finished = False
        self.rating_text = ""

        self.game_bg = pygame.image.load('Assets/Images/gameplay bg.png').convert()
        self.game_bg = pygame.transform.scale(self.game_bg, (int(self.game_bg.get_width()*3),int(self.game_bg.get_height()*3)))

        self.strwb_sauce = pygame.image.load('Assets/Images/strwb_sauce.png').convert_alpha()
        self.strwb_sauce = pygame.transform.scale(self.strwb_sauce, (int(self.strwb_sauce.get_width()*3),int(self.strwb_sauce.get_height()*3)))

        self.choco_sauce = pygame.image.load('Assets/Images/choco_sauce.png').convert_alpha()
        self.choco_sauce = pygame.transform.scale(self.choco_sauce, (int(self.choco_sauce.get_width()*3),int(self.choco_sauce.get_height()*3)))

        self.whip_cream = pygame.image.load('Assets/Images/whipping_cream.png').convert_alpha()
        self.whip_cream = pygame.transform.scale(self.whip_cream, (int(self.whip_cream.get_width()*3),int(self.whip_cream.get_height()*3)))

        self.sauces_active = False
        self.base_x = 1200

        self.hitbox_x = 1000
        self.strwb_sauce_hitbox = pygame.Rect(self.hitbox_x, 120, self.strwb_sauce.get_width(),self.strwb_sauce.get_height())
        self.choco_sauce_hitbox = pygame.Rect(self.hitbox_x, 220, self.choco_sauce.get_width(),self.choco_sauce.get_height())
        self.whip_cream_hitbox = pygame.Rect(self.hitbox_x, 320, self.whip_cream.get_width(),self.whip_cream.get_height())

        self.receipt_base = pygame.image.load('Assets/Images/receipt_base.png').convert_alpha()
        self.receipt_base = pygame.transform.scale(self.receipt_base, (int(self.receipt_base.get_width()*3),int(self.receipt_base.get_height()*3)))

        self.strwb_sauce_icon = pygame.image.load('Assets/Images/strwb_sauce_icon.png').convert_alpha()
        self.strwb_sauce_icon = pygame.transform.scale(self.strwb_sauce_icon, (int(self.strwb_sauce_icon.get_width()*3),int(self.strwb_sauce_icon.get_height()*3)))

        self.choco_sauce_icon = pygame.image.load('Assets/Images/choco_sauce_icon.png').convert_alpha()
        self.choco_sauce_icon = pygame.transform.scale(self.choco_sauce_icon, (int(self.choco_sauce_icon.get_width()*3),int(self.choco_sauce_icon.get_height()*3)))

        self.whip_cream_icon = pygame.image.load('Assets/Images/whip_cream_icon.png').convert_alpha()
        self.whip_cream_icon = pygame.transform.scale(self.whip_cream_icon, (int(self.whip_cream_icon.get_width()*3),int(self.whip_cream_icon.get_height()*3)))

        self.strawberries_icon = pygame.image.load('Assets/Images/strawberries_icon.png').convert_alpha()
        self.strawberries_icon = pygame.transform.scale(self.strawberries_icon, (int(self.strawberries_icon.get_width()*3),int(self.strawberries_icon.get_height()*3)))

        self.cookies_icon = pygame.image.load('Assets/Images/cookies_icon.png').convert_alpha()
        self.cookies_icon = pygame.transform.scale(self.cookies_icon, (int(self.cookies_icon.get_width()*3),int(self.cookies_icon.get_height()*3)))

        self.cherries_icon = pygame.image.load('Assets/Images/cherries_icon.png').convert_alpha()
        self.cherries_icon = pygame.transform.scale(self.cherries_icon, (int(self.cherries_icon.get_width()*3),int(self.cherries_icon.get_height()*3)))

        self.sauce_random = random.randint(1,2)
        self.topping_random = random.randint(1,3)
        self.sauce_choice = ""
        self.topping_choice = ""
        self.toppings_combo = ""

        self.girl_sprite = pygame.image.load('Assets/Images/girlspr_norm@3x.png').convert_alpha()
        self.girl_sprite = pygame.transform.scale(self.girl_sprite, (int(self.girl_sprite.get_width()/8),int(self.girl_sprite.get_height()/8)))

        self.girl_sprite_alt1 = pygame.image.load('Assets/Images/girlspr_frenzy@3x.png').convert_alpha()
        self.girl_sprite_alt1 = pygame.transform.scale(self.girl_sprite_alt1, (int(self.girl_sprite_alt1.get_width()/8),int(self.girl_sprite_alt1.get_height()/8)))

        self.girl_sprite_alt2 = pygame.image.load('Assets/Images/girlspr_sad@3x.png').convert_alpha()
        self.girl_sprite_alt2 = pygame.transform.scale(self.girl_sprite_alt2, (int(self.girl_sprite_alt2.get_width()/8),int(self.girl_sprite_alt2.get_height()/8)))


        self.boy_sprite = pygame.image.load('Assets/Images/boyspr_norm@3x.png').convert_alpha()
        self.boy_sprite = pygame.transform.scale(self.boy_sprite, (int(self.boy_sprite.get_width()/8),int(self.boy_sprite.get_height()/8)))

        self.boy_sprite_alt1 = pygame.image.load('Assets/Images/boyspr_frenzy@3x.png').convert_alpha()
        self.boy_sprite_alt1 = pygame.transform.scale(self.boy_sprite_alt1, (int(self.boy_sprite_alt1.get_width()/8),int(self.boy_sprite_alt1.get_height()/8)))

        self.boy_sprite_alt2 = pygame.image.load('Assets/Images/boyspr_sad@3x.png').convert_alpha()
        self.boy_sprite_alt2 = pygame.transform.scale(self.boy_sprite_alt2, (int(self.boy_sprite_alt2.get_width()/8),int(self.boy_sprite_alt2.get_height()/8)))
        

        self.cat_sprite = pygame.image.load('Assets/Images/catspr_norm@3x.png').convert_alpha()
        self.cat_sprite = pygame.transform.scale(self.cat_sprite, (int(self.cat_sprite.get_width()/8),int(self.cat_sprite.get_height()/8)))

        self.cat_sprite_alt1 = pygame.image.load('Assets/Images/catspr_frenzy@3x.png').convert_alpha()
        self.cat_sprite_alt1 = pygame.transform.scale(self.cat_sprite_alt1, (int(self.cat_sprite_alt1.get_width()/8),int(self.cat_sprite_alt1.get_height()/8)))

        self.cat_sprite_alt2 = pygame.image.load('Assets/Images/catspr_sad@3x.png').convert_alpha()
        self.cat_sprite_alt2 = pygame.transform.scale(self.cat_sprite_alt2, (int(self.cat_sprite_alt2.get_width()/8),int(self.cat_sprite_alt2.get_height()/8)))

        self.sprites = {
            "girl": {
            "normal": self.girl_sprite,
            "happy": self.girl_sprite_alt1,
            "sad": self.girl_sprite_alt2
            },
        "boy": {
            "normal": self.boy_sprite,
            "happy": self.boy_sprite_alt1,
            "sad": self.boy_sprite_alt2
            },
        "cat": {
            "normal": self.cat_sprite,
            "happy": self.cat_sprite_alt1,
            "sad": self.cat_sprite_alt2
            }
        }

    def draw(self, surface):
        
        surface.fill((255,237,203,255))
        surface.blit(self.game_bg,(0,0))
        surface.blit(self.receipt_base,(20,20))
        surface.blit(self.whip_cream_icon,(35,40))

        if self.sauce_random == 1:
            surface.blit(self.strwb_sauce_icon,(35,150))
        else:
            surface.blit(self.choco_sauce_icon,(35,150))

        if self.topping_random == 1:
            surface.blit(self.strawberries_icon,(40,250))

        elif self.topping_random == 2:
            surface.blit(self.cookies_icon,(40,250))
        else:
            surface.blit(self.cherries_icon,(40,250))


        global answer_correct, answer_wrong, answer_combo
        mpos = pygame.mouse.get_pos()

        if answer_correct:
            self.time += delta_time
            if self.time < 1:
                self.sprite = "happy"

            else:
                self.sprite = "normal"
                self.time = 0
                answer_correct = False
                
        elif answer_wrong:
            self.time += delta_time
            if self.time < 1:
                self.sprite = "sad"

            else:
                self.sprite = "normal"
                self.time = 0
                answer_wrong = False

        draw_y = self.base_y
        if self.bobbing:
            self.sprite = "happy"
            self.ani_time += delta_time
            draw_y = self.base_y + math.sin(self.ani_time*20)*2
       
        if self.chara in self.sprites:
            self.chara_img = self.sprites[self.chara][self.sprite]
            screen.blit(self.chara_img, (-80, draw_y))

        if self.timed_finished :
            self.sauces_active = True
            self.time += delta_time
            if self.time < 2:
                surface.blit(header_font_XL.render(self.rating_text, True, (255, 255, 255)),(500 ,50))

            if self.sauces_active:

                if self.base_x > 1000:
                    self.base_x -= delta_time*500
                    if self.base_x <1000:
                        self.base_x = 1000
                    
                surface.blit(self.strwb_sauce,(self.base_x,120))
                surface.blit(self.choco_sauce,(self.base_x,220))
                surface.blit(self.whip_cream,(self.base_x,320))
                
                
                if self.strwb_sauce_hitbox.collidepoint(mpos):
                    screen.blit(self.strwb_sauce,(970,120))
                    self.hitbox_x = 970

                if self.choco_sauce_hitbox.collidepoint(mpos):
                    screen.blit(self.choco_sauce,(970,220))
                    self.hitbox_x = 970
        
                if self.whip_cream_hitbox.collidepoint(mpos):
                    screen.blit(self.whip_cream,(970,320))
                    self.hitbox_x = 970
            else:
                print("AHHHHHHHHHHHHH")
        
    def handle_event(self, event):  
        global answer_combo, points, bonus_points, counter, timed_questions

        if self.chara == "":
            try: 
                with open(filename,"r") as f:
                    lines = f.readlines()
                    if lines:
                        #variable for latest line
                        last_record = lines[-1].strip()
                        #variables to print list values.
                        chara, name, concept, difficulty = last_record.strip().split(",")
                        self.chara = chara

            except FileNotFoundError:
                return "quit"
            
        if answer_combo >= 5: 
            self.bobbing = True
        else: 
            self.bobbing = False

        if counter == 0 and not self.bonus_given:
            if timed_questions == 5:
                points = int(points + (bonus_points*1.8)-500)
                self.rating_text = "Perfect!"

            elif timed_questions == 4:
                points = int(points + (bonus_points*1.5)-400)
                self.rating_text = "Great!"

            elif timed_questions == 3:
                points = int(points + (bonus_points*1.2)-300)
                self.rating_text = "Good!"

            self.timed_finished = True
            self.bonus_given = True

        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.timed_finished and self.sauces_active:
                    if self.strwb_sauce_hitbox.collidepoint(event.pos):
                        click_sound.play()
                        self.sauce_choice = "strwb_sauce"
                        print("strwb sauce clicked")
                        self.sauces_active = False

                    if self.choco_sauce_hitbox.collidepoint(event.pos):
                        click_sound.play()
                        self.sauce_choice = "choco_sauce"
                        print("choco sauce clicked")
                        self.sauces_active = False

                    if self.whip_cream_hitbox.collidepoint(event.pos):
                        click_sound.play()
                        print("whipcream clicked")
                        self.sauces_active = False


        if self.sauce_random == 1 and self.topping_random == 1:
            self.toppings_combo = "strwb_sauce,strawberries"

        elif self.sauce_random == 1 and self.topping_random == 2:
            self.toppings_combo = "strwb_sauce,cookies"

        elif self.sauce_random == 1 and self.topping_random == 3:
            self.toppings_combo = "strwb_sauce,cherries"

        elif self.sauce_random == 2 and self.topping_random == 1:
            self.toppings_combo = "choco_sauce,strawberries"

        elif self.sauce_random == 2 and self.topping_random == 2:
            self.toppings_combo = "choco_sauce,cookies"

        elif self.sauce_random == 2 and self.topping_random == 3:
            self.toppings_combo = "choco_sauce,cherries"


        if self.back_button.is_clicked(event):
            self.chara=""
            self.sprite = "normal"
            
            self.sauce_random = random.randint(1,2)
            self.topping_random = random.randint(1,3)
            self.sauces_active = False
            bonus_points = 0
            points = 0
            timed_questions = 0 
        if question_type == 1:
            return "multichoice"
        if question_type == 0:
            return "inputquestion"
        return None

#============================================================================
#   Class for combobox
#----------------------------------------------------------------------------

class ComboBox():
    def __init__(self):
        self.wheel_scrolling = False
        self.wheel_scroll = 420
        self.combo_scroll=420
        self.addition = Buttons3(40, 0, 200,30, "Addition",(255,237,203))
        self.subtraction = Buttons3(40, 0, 200,30, "Subtraction",(255,237,203))
        self.multiplication = Buttons3(40, 0, 200,30, "Multiplication",(255,237,203))
        self.fractions = Buttons3(40, 0, 200,30, "Fractions",(255,237,203))
        self.exponents = Buttons3(40, 0, 200,30, "Exponents",(255,237,203))
        self.algebra = Buttons3(40, 0, 200,30, "Algebra",(255,237,203))

    def draw(self,surface):
        
        self.addition.rect.y = self.combo_scroll
        self.subtraction.rect.y = self.combo_scroll + 40
        self.multiplication.rect.y = self.combo_scroll + 80
        self.fractions.rect.y = self.combo_scroll + 120
        self.exponents.rect.y = self.combo_scroll + 160
        self.algebra.rect.y = self.combo_scroll + 200

        pygame.draw.rect(surface,(158, 109, 63),(27,407,256,126),border_radius=12)
        
        pygame.draw.rect(surface,(255,237,203),(30,410,250,120),border_radius=12)
        screen.set_clip(pygame.Rect(30,410,250,120))
        pygame.draw.rect(surface,(158, 109, 63),(265,self.wheel_scroll,10,40),border_radius=12)
        

        pygame.draw.rect(surface,(209, 162, 109),(38,self.combo_scroll-2,204,34),border_radius=6)
        pygame.draw.rect(surface,(209, 162, 109),(38,self.combo_scroll+38,204,34),border_radius=6)
        pygame.draw.rect(surface,(209, 162, 109),(38,self.combo_scroll+78,204,34),border_radius=6)
        pygame.draw.rect(surface,(209, 162, 109),(38,self.combo_scroll+118,204,34),border_radius=6)
        pygame.draw.rect(surface,(209, 162, 109),(38,self.combo_scroll+158,204,34),border_radius=6)
        pygame.draw.rect(surface,(209, 162, 109),(38,self.combo_scroll+198,204,34),border_radius=6)
        

        self.addition.draw(surface)
        self.subtraction.draw(surface)
        self.multiplication.draw(surface)
        self.fractions.draw(surface)
        self.exponents.draw(surface)
        self.algebra.draw(surface)

        screen.set_clip(None)
    
    def scroll(self,event):
        if event.type == pygame.MOUSEWHEEL:
    
            if event.y <0 :
                self.wheel_scrolling = True
                self.wheel_scroll -=5
                self.combo_scroll +=10
            
            elif event.y>0 :
                self.wheel_scrolling = True
                self.wheel_scroll +=5
                self.combo_scroll -=10

            self.wheel_scroll = max(420, min(self.wheel_scroll, 485))
            self.combo_scroll = max(290, min(self.combo_scroll, 420))
            


    def handle_event(self, event):
        if self.addition.is_clicked(event):
            return "leaderboard"
        
        if self.subtraction.is_clicked(event):
            return "leaderboard"
        
        if self.multiplication.is_clicked(event):
            return "leaderboard"
        
        if self.fractions.is_clicked(event):
            return "leaderboard"
        
        if self.exponents.is_clicked(event):
            return "leaderboard"
        
        if self.algebra.is_clicked(event):
            return "leaderboard"

        return None
    
    def combo_event(self, event):
        if self.addition.is_clicked(event):
            return "addition"
        
        if self.subtraction.is_clicked(event):
            return "subtraction"
        
        if self.multiplication.is_clicked(event):
            return "multiplication"
        
        if self.fractions.is_clicked(event):
            return "fractions"
        
        if self.exponents.is_clicked(event):
            return "exponents"
        
        if self.algebra.is_clicked(event):
            return "algebra"
        
        return None
    

#============================================================================
#   Class for leaderboard page 
#----------------------------------------------------------------------------

class Leaderboard():
    def __init__(self):

        self.back_button = Buttons(30,580,50,50, "B", (230,188,140))
        self.confirm_button = Buttons(110,580,200,50, "CONFIRM", (230,188,140))

        self.easy_button = Buttons(30, 110, 40, 40, "*", (230,188,140))
        self.med_button = Buttons(30, 180, 40, 40, "*", (230,188,140))
        self.hard_button = Buttons(30, 250, 40, 40, "*", (230,188,140))

        self.concept_combobox = Buttons3(290, 370, 40, 30, "v",(255,237,203))

        self.difficulty_choice = ""
        self.leader_text = ""

    def draw(self, surface):
        surface.fill((255,237,203,255))
        surface.blit(gingham,(0,0))
        pygame.draw.rect(surface,(158, 109, 63),(345,45,810,585),border_radius=12)
        pygame.draw.rect(surface,(255,237,203),(350,50,800,575),border_radius=12)

        surface.blit(header_font_lrg.render(f'Leaderboard:  {self.difficulty_choice}   {combo_choice}', True, (158, 109, 63)), (380,70))
        surface.blit(sub_font.render(self.leader_text, True, (158, 109, 63)), (380,130))


        pygame.draw.rect(surface,(209, 162, 109),(30, 120, 40, 40),border_radius=12)
        pygame.draw.rect(surface,(209, 162, 109),(30, 190, 40, 40),border_radius=12)
        pygame.draw.rect(surface,(209, 162, 109),(30, 260, 40, 40),border_radius=12)
        
        self.easy_button.draw(surface)
        self.med_button.draw(surface)
        self.hard_button.draw(surface)

        pygame.draw.rect(surface,(209, 162, 109),(287, 367, 46, 36),border_radius=6)
        self.concept_combobox.draw(surface)
        
        screen.blit(header_font_sml.render('Enter Difficulty:',True,(158, 109, 63)), (30,70))

        screen.blit(header_font_sml.render('EASY',True,(158, 109, 63)), (100,130))
        screen.blit(header_font_sml.render('MEDIUM',True,(158, 109, 63)), (90,200))
        screen.blit(header_font_sml.render('HARD',True,(158, 109, 63)), (100,270))

        screen.blit(header_font_sml.render('Enter Concept:',True,(158, 109, 63)), (30,330))

        pygame.draw.rect(surface,(158, 109, 63),(27,367,256,36),border_radius=12)
        pygame.draw.rect(surface,(255,237,203),(30,370,250,30),border_radius=12)

        surface.blit(sub_font_sml.render(combo_choice.capitalize(), True, (158, 109, 63)), (50,372))

        pygame.draw.rect(screen,(209, 162, 109),(30,590,50,50),border_radius=12)
        pygame.draw.rect(screen,(209, 162, 109),(110,590,200,50),border_radius=12)
        self.back_button.draw(surface)
        self.confirm_button.draw(surface)

    def handle_event(self, event):
         
         if self.easy_button.is_clicked(event):
             self.difficulty_choice = "easy"

         if self.med_button.is_clicked(event):
             self.difficulty_choice = "medium"
    
         if self.hard_button.is_clicked(event):
             self.difficulty_choice = "hard"

         if self.concept_combobox.is_clicked(event):
             return "leader_combo"

         if self.back_button.is_clicked(event):
              self.leader_text = ""
              self.difficulty_choice = ""
              return "home"
         
         if self.confirm_button.is_clicked(event):
            if not self.difficulty_choice:
                self.leader_text = "Please pick a difficulty and maths concept!"
            if self.difficulty_choice == "easy":
                if combo_choice != "":  
                    try: 
                        with open (easy_leader,"r") as f1:
                            lines = f1.readlines()
                        if lines:
                            found = False
                            for line in lines:
                                if line.startswith(combo_choice+","):
                                    found = True
                                    concept, name = line.strip().split(",")
                                    if concept == combo_choice:
                                        line = f"\n\n {name} - 100 pts"
                                        self.leader_text = line
                                    else:
                                        self.leader_text = "No records~ be the first to set one!"
                            if not found:
                                self.leader_text ="No records~ be the first to set one!"
                                
                        if not lines:
                            self.leader_text = "No records~ be the first to set one!"

                    except FileNotFoundError:
                        self.leader_text = "file not found"
                else:
                    self.leader_text = "Please pick a maths concept!"
            
            elif self.difficulty_choice == "medium":
                if combo_choice != "":
                    try:
                        with open (med_leader,"r") as f2:
                            lines = f2.readlines()
                        if lines:
                            found = False
                            for line in lines:
                                if line.startswith(combo_choice+","):
                                    found = True
                                    concept, name = line.strip().split(",")
                                    if concept == combo_choice:
                                        line = f"\n\n {name} - 100 pts"
                                        self.leader_text = line
                                    else:
                                        self.leader_text = "No records~ be the first to set one!"
                            if not found:
                                self.leader_text ="No records~ be the first to set one!"
                                
                        if not lines:
                            self.leader_text = "No records~ be the first to set one!"

                    except FileNotFoundError:
                        self.leader_text = "file not found"
                else: 
                    self.leader_text = "Please pick a maths concept!"
            
            elif self.difficulty_choice == "hard":
                if combo_choice != "":
                    try:
                        with open (hard_leader,"r") as f3:
                            lines = f3.readlines()
                        if lines:
                            found = False
                            for line in lines:
                                if line.startswith(combo_choice+","):
                                    found = True
                                    concept, name = line.strip().split(",")
                                    if concept == combo_choice:
                                        line = f"\n\n {name} - 100 pts"
                                        self.leader_text = line
                                    else:
                                        self.leader_text = "No records~ be the first to set one!"
                            if not found:
                                self.leader_text ="No records~ be the first to set one!"
                                
                        if not lines:
                            self.leader_text = "No records~ be the first to set one!"

                    except FileNotFoundError:
                        self.leader_text = "file not found"
                else:
                    self.leader_text = "Please pick a maths concept!"
         return None
    

    def combo_event(self,event):
        if self.back_button.is_clicked(event):
            return ""
        return None
        

current_screen = "home"
homepage = Homepage()
help_page = Help_Page()
chara_select =Chara_Select()
leader = Leaderboard()
concept = Concept_Select()
difficulty = Difficulty_Select()
game = GameScreen()
combobox = ComboBox()
multiquestion = MultiQuestion()
input_question = InputQuestion()

combo_choice =""
question_type = random.randint(0,1)
points = 0 
answer_combo = 0
answer_correct = False
answer_wrong = False

TIMER_EVENT = pygame.event.custom_type()
counter = 60
timed_questions = 0
bonus_points = 0


#============================================================================
# Running Code.
#----------------------------------------------------------------------------

running = True 
while running:
    for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                pygame.time.set_timer(TIMER_EVENT, 0)
                if current_screen != "home":
                    try:
                        with open(filename,"r") as f:
                            lines = f.readlines()
                            if lines:
                                lines = lines[:-1]
                                with open(filename,"w") as f:
                                    f.writelines(lines)
                                    running = False
                            else:
                                running = False
                    except FileNotFoundError:
                        running = False

            if event.type == TIMER_EVENT:
                counter-=1
                if counter == 0:
                    print("boom!")
                    pygame.time.set_timer(TIMER_EVENT, 0)

                if timed_questions == 5:
                    counter = 0
                    
            
            if current_screen == "home":
                result = homepage.handle_event(event)
                if result == "quit":
                     running = False
                elif result:
                     current_screen = result
                
            elif current_screen == "help":
                result = help_page.handle_event(event)
                if result:
                    current_screen = result
            
            elif current_screen == "character_select":
                chara_select.input_box.userinput(event)
                result = chara_select.handle_event(event)
                if result:
                     current_screen = result

            elif current_screen == "leaderboard":
                
                result = leader.handle_event(event)
                if result:
                     current_screen = result
                combo_result = leader.combo_event(event)
                if combo_result == "":
                    combo_choice = combo_result
            
            elif current_screen == "leader_combo":
                combobox.scroll(event)
                result = combobox.handle_event(event)
                if result:
                    current_screen = result
                    
                combo_result = combobox.combo_event(event)
                if combo_result:
                    combo_choice = combo_result

                result = leader.handle_event(event)
                if result:
                     current_screen = result

            elif current_screen == "concept":
                result = concept.handle_event(event)
                if result:
                    current_screen = result
            
            elif current_screen == "difficulty":
                result = difficulty.handle_event(event)
                if result:
                    current_screen = result
            
            elif current_screen == "gameplay":
                result = game.handle_event(event)
                if result:
                    current_screen = result
                
                
            elif current_screen == "multichoice":
                result = game.handle_event(event)
                if result:
                    current_screen = result

                multi_result = multiquestion.handle_event(event)
                if multi_result:
                    question_type = random.randint(0,1)
                    if question_type == 1:
                        current_screen = "multichoice"

                    if question_type == 0:
                        current_screen = "inputquestion"

                back_result = multiquestion.back_event(event)
                if back_result:
                    current_screen = back_result

            elif current_screen == "inputquestion":
                result = game.handle_event(event)
                if result:
                    current_screen = result

                input_question.input_box.userinput(event)
                input_result = input_question.handle_event(event)
                if input_result:
                    question_type = random.randint(0,1)
                    if question_type == 1:
                        current_screen = "multichoice"
                    if question_type == 0:
                        current_screen = "inputquestion"

                back_result = input_question.back_event(event)
                if back_result:
                    current_screen = back_result

            
    if current_screen =="home":
        homepage.draw(screen)
        
    elif current_screen == "help":
        homepage.draw(screen)
        help_page.draw(screen)
    
    elif current_screen == "character_select":
        chara_select.draw(screen)

    elif current_screen == "leaderboard":
        leader.draw(screen)
    
    elif current_screen == "leader_combo":
        leader.draw(screen)
        combobox.draw(screen)

    elif current_screen == "concept":
        concept.draw(screen)
    
    elif current_screen == "difficulty":
        difficulty.draw(screen)
    
    elif current_screen == "gameplay":
        game.draw(screen)

    elif current_screen == "multichoice":
        game.draw(screen)
        multiquestion.draw(screen)

    elif current_screen == "inputquestion":
        game.draw(screen)
        input_question.draw(screen)

    pygame.display.flip()

    delta_time = clock.tick(60) / 1000
    delta_time =max(0.001,min(0.1, delta_time))

pygame.quit()
sys.exit()
