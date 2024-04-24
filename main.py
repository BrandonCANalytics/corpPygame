import pygame, asyncio
import random
from sys import exit

screen_size = (800, 600)

pygame.init()

screen = pygame.display.set_mode(screen_size) ## creates the display surface - the game window where anything displayed goes
pygame.display.set_caption("Climbing the Corporate Ladder")
clock = pygame.time.Clock() ## creates a clock object to help with fps optimization
title_font = pygame.font.Font('fonts/CourierPrime.ttf', 24)
obj_font = pygame.font.Font('fonts/CourierPrime.ttf', 16)

async def main():
    score = 0
    game_title = title_font.render("Climbing the Corporate Ladder", True, "black")
    game_over_title = title_font.render("GAME OVER", True, "black")
    continue_title = title_font.render("Press Space to Continue", True, "black")
    coll_text = title_font.render("BURNOUT!", True, "red")
    sky_background = pygame.image.load('graphics/skybackground.jpg').convert() ## .convert() converts the image file into something easier for pygame to handle
    building = pygame.image.load('graphics/building.jpg').convert()
    building2 = pygame.image.load('graphics/building2.jpg').convert()
    obstacles = ['Meetings', "You're muted.", 'No bonus this year', "Hover Boss", "Org Silos", "This", "That", "These", "Those"]
    game_active = True
    man_x_pos = 350
    man_y_pos = 440
    man = pygame.image.load('graphics/man.png').convert_alpha() ## using convert_alpha for this transparent image to take out the background 
    man_rect = man.get_rect(topleft=(man_x_pos,man_y_pos))

    #obstacle
    meetings = obj_font.render(obstacles[random.randint(0,4)], True, "black")
    meetings_rect = meetings.get_rect(topleft=(random.randint(0,700),-50))

    obstacle_rect_list = []

    def obstacle_movement(list):
        if list:
            for obj in list:
                obj.y += 3
                screen.blit(meetings, obj)
            list = [obstacle for obstacle in list if obstacle.y < 500] 
            
            return obstacle_rect_list
        else: return []

    def reset_obj (obj):
        obj.top = -50

    def collisions(player, obstacles):
        if obstacles:
            for obstacle_rect in obstacles:
                if player.colliderect(obstacle_rect): 
                    screen.blit(coll_text, (350,150))
                    return -10
                #elif not player.colliderect(obstacle_rect): return 0
    # timer
    game_speed = 700
    obstacle_timer = pygame.USEREVENT + 1
    pygame.time.set_timer(obstacle_timer, game_speed)

    #async def run

    while True:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if not game_active:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE: ##  press space to restart game
                    reset_obj(meetings_rect)
                    game_active = True
                    rand = random.randint(0,4)
                    

            if event.type == obstacle_timer and game_active:
                meetings = obj_font.render(obstacles[random.randint(0,4)], True, "black")
                obstacle_rect_list.append(meetings.get_rect(topleft=(random.randint(0,700),-10)))
        
        if game_active:
            score_text = title_font.render("Score: "+str(score), True, "black")        
            score += 1 ## increments score +1 every frame
            if score < 0: score = 0
            screen.blit(sky_background, (0,0))  
            screen.blit(building, (0,0))  
            screen.blit(building2, (675,0))  
            screen.blit(game_title, (200,50))

            obstacle_rect_list = obstacle_movement(obstacle_rect_list)

            ##spawn(meetings, meetings_rect)

            #screen.blit(meetings, meetings_rect) 
            #meetings_rect.y += 3 # moves the Meetings obstacle down through the screen
            #if meetings_rect.y >= 600: meetings_rect.top = -10

            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]: ## left arrow key moves man left
                man_rect.left -=4
            if keys[pygame.K_RIGHT]: ## right arrow key moves man right
                man_rect.left +=4
                
            if man_rect.x >= 800: man_rect.left = -20   ## this line and the bottom ensure that the man returns back to the opposite side of the screen when out of bounds
            if man_rect.x <= -75: man_rect.right = 900 
            screen.blit(man, man_rect)
            screen.blit(meetings, meetings_rect) 
            screen.blit(score_text, (350,100))

            #collisions
            if collisions(man_rect, obstacle_rect_list) == -10:
                score = score + collisions(man_rect, obstacle_rect_list)
            if score < 0: 
                score = 0 
                game_active = False
                reset_obj(meetings_rect)
                for obj in obstacle_rect_list:
                    obstacle_rect_list.pop()
                    reset_obj(obj)
            if score == 300: game_speed -= 200  
            elif score == 700: game_speed -= 300     
            
        else:
            for obj in obstacle_rect_list:
                    obstacle_rect_list.pop()
            screen.blit(sky_background, (0,0))  
            screen.blit(building, (0,0))  
            screen.blit(building2, (675,0))  
            screen.blit(game_title, (200,50))
            screen.blit(game_over_title, (320,250))
            screen.blit(continue_title, (235,200))
                    
        pygame.display.update()
        clock.tick(60) ## tells clock not to run faster than 60 fps, sets the framerate
        await asyncio.sleep(0)

asyncio.run(main())