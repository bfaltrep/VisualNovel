import sys, pygame, os, time
from random import randrange

################################################
    ##   VARIABLES                        ##
################################################

#chaque case fait 80 pixel
size = width, height = 320, 320

back_color = pygame.Color(0,0,0)
text_color = pygame.Color(255,255,255)
#back_separator = pygame.Color(230, 230, 230)

case_colors = {0: pygame.Color(234, 197, 176),
               2: pygame.Color(204, 196, 146),
               4: pygame.Color(213, 234, 176),
               8: pygame.Color(176, 234, 226),
               16: pygame.Color(176, 234, 197),
               32: pygame.Color(176, 184, 234),
               64: pygame.Color(197, 176, 234),
               128: pygame.Color(176, 213, 234),
               256: pygame.Color(239, 228, 176),
               512: pygame.Color(187,157,140),
               1024: pygame.Color(187,140,147),
               2048: pygame.Color(247, 249, 219)}

table = [[0, 0, 0, 0],[0, 0, 0, 0],[0, 0, 0, 0],[0, 0, 0, 0]]
visual_table = [[pygame.Rect(8, 8, 70, 70), pygame.Rect(86, 8, 70, 70), pygame.Rect(164, 8, 70, 70), pygame.Rect(242, 8, 70, 70)],
                [pygame.Rect(8, 86, 70, 70), pygame.Rect(86, 86, 70, 70), pygame.Rect(164, 86, 70, 70), pygame.Rect(242, 86, 70, 70)],
                [pygame.Rect(8, 164, 70, 70), pygame.Rect(86, 164, 70, 70), pygame.Rect(164, 164, 70, 70),pygame.Rect(242, 164, 70, 70)],
                [pygame.Rect(8, 242, 70, 70), pygame.Rect(86, 242, 70, 70), pygame.Rect(164, 242, 70, 70), pygame.Rect(242, 242, 70, 70)]]

#text centers
text_table = [43, 121, 199, 277]

titre = "2048"
file = "2048_debug.txt"
win_msg = "Bravo !"
lose_msg = "haow... PERDU..."
ExcNotGoodArgument = "can_one_move - not good argument"

################################################
    ##   FONCTIONS                        ##
################################################

#----------------------------
#--- écriture fichier log ---

def write_log(msg):
    fichier = open(file, "a")
    fichier.write(msg)
    fichier.close()

#-----------------------
#--- Affichage Shell ---

def print_table():
    str_list = []
    for x in range(4):
        for y in range(4):
            str_list.append(format(table[x][y],'04d'))
            if y < 3:
                str_list.append(" ")
        str_list.append(os.linesep)
        
    str_list.append("-")
    str_list.append(os.linesep)
    return "".join(str_list)

#-----------------------
#---Affichage Visuel ---
    
def visual_init(titre):
    #320 : 8 - 70 - 8 - 70 - 8 - 70 - 8 - 70 - 8 
    #affichage
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption(titre)
    screen.fill(back_color)
    visual_print_table(screen)
    return screen

def visual_print_table(screen):
    for y in range(4):
        for x in range(4):
            screen.fill(case_colors[table[x][y]], visual_table[x][y])
            visual_print_text(screen, table[x][y], y, x)
    pygame.display.update()

def visual_print_text(screen, texte, x, y):
    font = pygame.font.SysFont(None, 25)
    text = font.render(str(texte), True, text_color)
    textRect = text.get_rect()
    textRect.center = (text_table[x], text_table[y])
    screen.blit(text, textRect)
    pygame.display.update()

def visual_print_msg(screen, msg, x, y):
    font = pygame.font.SysFont(None, 55)
    text = font.render(str(msg), True, text_color, back_color)
    textRect = text.get_rect()
    textRect.center = (x, y)
    screen.blit(text, textRect)
    pygame.display.update()
    
#-----------------------
#---       Jeu       ---

def can_move():
    if have_empty_case():
        return True
    else:
        if can_one_move("horizontal") : return True
        elif can_one_move("vertical") : return True
        else:
            return False

def can_one_move(direction):
    for y in range(4):
        if direction == "right" or direction == "left" :
            #recherche déplacement sans combinaison
            liste = table[y].copy()
            if direction == "right":
                liste.reverse()
            find_zero = False
            z = 0
            while z < len(liste):
                if find_zero and liste[z] > 0:
                    return True
                if not find_zero and liste[z] == 0:
                    find_zero = True
                z += 1
            #recherche combinaison
            liste = [e for e in table[y] if e != 0]
            z = 0
            while z < len(liste)-1:
                if liste[z] == liste[z+1]:
                    return True
                z += 1

        elif direction == "up" or direction == "down" :
            #recherche déplacement sans combinaison
            liste = []
            for x in range(4):
                liste.append(table[x][y])
            if direction == "down":
                liste.reverse()
            find_zero = False
            z = 0
            while z < len(liste):
                if find_zero and liste[z] > 0:
                    return True
                if not find_zero and liste[z] == 0:
                    find_zero = True
                z += 1
            #recherche combinaison
            liste = []
            for x in range(4):
                if table[x][y] != 0:
                    liste.append(table[x][y])
            z = 0
            while z < len(liste)-1:
                if liste[z] == liste[z+1]:
                    return True
                z += 1

        else :
            name = ExcNotGoodArgument + " " + direction
            raise Exception(name)
    return False

def have_empty_case():
    nb_zero = 0
    for x in range(4):
        for y in range(4):
            if table[x][y] == 0:
                nb_zero = nb_zero+1
    return nb_zero != 0

def init_table():
    table[randrange(3)][randrange(3)] = 2
    x = randrange(3)
    y = randrange(3)
    while (table[x][y] != 0):
        x = randrange(3)
        y = randrange(3)
    table[x][y] = 2

def good_end():
    for x in range(4):
        for y in range(4):
            if table[x][y] == 2048:
                return True
    return False

def bad_end():
    if not can_move():
        return True
    return False

def move(direction):
    moved = False
    if can_one_move(direction):
        moved = True
    
    if (direction == "right"):
        for x in range(4):
            liste = [e for e in table[x] if e!=0]
            liste.reverse()
            liste = treat_line(liste)
            liste.reverse()
            table[x] = liste.copy()
            
    elif (direction == "left"):
        for x in range(4):
            liste = [e for e in table[x] if e!=0]
            liste = treat_line(liste)
            table[x] = liste.copy()
        
    elif (direction == "up"):
        for y in range(4):
            liste = []
            for x in range(4):
                if table[x][y] != 0:
                    liste.append(table[x][y])
            liste = treat_line(liste)
            for x in range(4):
                if x < len(liste):
                    table[x][y] = liste[x]
                else:
                    table[x][y] = 0

    elif (direction == "down"):
        for y in range(4):
            liste = []
            for x in range(4):
                if table[x][y] != 0:
                    liste.append(table[x][y])
            liste.reverse()
            liste = treat_line(liste)
            liste.reverse()
            for x in range(4):
                if x < len(liste):
                    table[x][y] = liste[x]
                else:
                    table[x][y] = 0
    return moved

def treat_line(liste):
    y = 0
    while y < len(liste)-1:
        if liste[y] == liste[y+1]:
            liste[y] = liste[y]*2
            del liste[y+1]
        y += 1
    while len(liste) < 4:
        liste.append(0)
    return liste

def new_case():
    if have_empty_case():
        x = randrange(3)
        y = randrange(3)
        while (table[x][y] != 0):
            x = randrange(3)
            y = randrange(3)
        table[x][y] = 2

def init_game():
    #init pygame
    pygame.init()
    
    #input acceptés
    pygame.event.set_blocked(None)
    pygame.event.set_allowed(pygame.KEYDOWN)
    pygame.event.set_allowed(pygame.QUIT)

    init_table()


def game():
    init_game()
    screen = visual_init(titre)
    clock = pygame.time.Clock()

    write_log(time.strftime("%Y/%m/%d %H:%M:%S")+" - lancement du jeu"+os.linesep)
    write_log(print_table())
    iteration = 0
    quit_game = False
    while not quit_game and not good_end() and not bad_end():
        clock.tick(60)
        event = pygame.event.wait()
        pygame.event.clear()
        if event.type == pygame.QUIT:
            quit_game = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                if move("left") :
                    new_case()
                    iteration = iteration +1
                    write_log("tour "+str(iteration)+" left"+os.linesep)
                    write_log(print_table())
                visual_print_table(screen)
            elif event.key == pygame.K_UP:
                if move("up") :
                    new_case()
                    iteration = iteration +1
                    write_log("tour "+str(iteration)+" up"+os.linesep)
                    write_log(print_table())
                visual_print_table(screen)
            elif event.key == pygame.K_RIGHT:
                if move("right"):
                    new_case()
                    iteration = iteration +1
                    write_log("tour "+str(iteration)+" right"+os.linesep)
                    write_log(print_table())
                visual_print_table(screen)
            elif event.key == pygame.K_DOWN:
                if move("down"):
                    new_case()
                    iteration = iteration +1
                    write_log("tour "+str(iteration)+" down"+os.linesep)
                    write_log(print_table())
                visual_print_table(screen)
            elif event.key == pygame.K_SPACE:
                print(print_table())

    #end
    if quit_game:
        pygame.quit()
        sys.exit()
    if good_end():
        visual_print_msg(screen, win_msg, width/2, height/2)
        write_log(win_msg)
        print(win_msg)
    else:
        visual_print_msg(screen, lose_msg, width/2, height/2)
        write_log(lose_msg)
        print(lose_msg)

################################################
    ##   MAIN                              ##
################################################

game()
