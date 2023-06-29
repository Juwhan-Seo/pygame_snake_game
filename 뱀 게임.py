import pygame
from pygame.locals import QUIT, KEYDOWN, K_LEFT, K_RIGHT, K_DOWN, K_UP
import sys
from random import randint as ri
import time








pygame.init()
size = 40
W, H = 20, 20




print(pygame.font.get_fonts())




SUR = pygame.display.set_mode((W*size, H*size))
FPS = pygame.time.Clock()
mess = pygame.font.SysFont("haansaleb", 60)
mu_mess = pygame.font.SysFont("haansaleb", 30)
re_mess = pygame.font.SysFont("haansaleb", 30)




S = [(W//2, H//2)]
F = []
E = []
score = 0




def add_food():
    while True:
        pos = ri(0,W-1), ri(0,H-1)
        if pos in S or pos in F: # 음식이 뱀의 위치이거나 기존에 음식이 있던 장소라면 다시 뽑겠다!
            continue
        F.append(pos)




        per = ri(1,100)
        if per <= 30:
            E.append(0)
        elif per <= 40:
            E.append(1)
        elif per <= 50:
            E.append(2)
        elif per <= 60:
            E.append(3)
        elif per <= 70:
            E.append(4)
        elif per <= 80:
            E.append(5)
        elif per <= 90:
            E.append(6)
        else:
            E.append(7)
        break




def move(idx):
    del F[idx]
    del E[idx]
    add_food()




for i in range(10):
    add_food()
print(F, E)




sp = 3
mapstart = 0
revstart = 0
foodstart = 0




map_state = False
rev = False
foody = False




key = K_DOWN
gameover = False








while True:
    SUR.fill((0,0,0))
    for i in pygame.event.get():
        if i.type == QUIT:
            pygame.quit()
            sys.exit()
        elif i.type == KEYDOWN:
            key = i.key
            if rev:
                if key == K_UP:
                    key = K_DOWN
                elif key == K_DOWN:
                    key = K_UP
                elif key == K_RIGHT:
                    key = K_LEFT
                elif key == K_LEFT:
                    key = K_RIGHT




    if not gameover:




        if key == K_UP:
            head = S[0][0], S[0][1]-1
        elif key == K_DOWN:
            head = S[0][0], S[0][1]+1
        elif key == K_RIGHT:
            head = S[0][0]+1, S[0][1]
        elif key == K_LEFT:
            head = S[0][0]-1, S[0][1]








        if head in S:
            gameover = True








        for num, i in enumerate(F,0):
            if E[num] == 0:
                pygame.draw.ellipse(SUR, (255,255,255), (i[0]*size, i[1]*size, size, size))
            elif E[num] == 1:
                pygame.draw.ellipse(SUR, (0,255,255), (i[0]*size, i[1]*size, size, size))
            elif E[num] == 2:
                pygame.draw.ellipse(SUR, (0, 190, 255), (i[0]*size, i[1]*size, size, size))
            elif E[num] == 3:
                pygame.draw.ellipse(SUR, (0, 60, 255), (i[0]*size, i[1]*size, size, size))
            elif E[num] == 4:
                pygame.draw.ellipse(SUR, (149, 82, 255), (i[0]*size, i[1]*size, size, size))
            elif E[num] == 5:
                pygame.draw.ellipse(SUR, (254, 29, 0), (i[0]*size, i[1]*size, size, size))
            elif E[num] == 6:
                pygame.draw.ellipse(SUR, (254, 168, 0), (i[0]*size, i[1]*size, size, size))
            elif E[num] == 7:
                pygame.draw.ellipse(SUR, (255, 195, 255), (i[0]*size, i[1]*size, size, size))




        S.insert(0, head)








        if head[0] < 0 or head[0] > 19 or head[1] < 0 or head[1] > 19:
            if map_state:
                for num,i in enumerate(S,0):
                    S[num] = i[0]%20, i[1]%20
            else:
                gameover = True












        if time.time() - mapstart >= 4:
            map_state = False
        if time.time() - revstart >= 5:
            rev = False




        if head in F:
            fidx = F.index(head)




            # 0 일 때는 그냥 + 100
            # 1 일 때는 추가 + 100 (즉, )
            if E[fidx] == 1:
                score += 100
            elif E[fidx] == 2:
                sp = 3
            elif E[fidx] == 3:
                S = [head]
            elif E[fidx] == 4:
                map_state = True
                mapstart = time.time()
            elif E[fidx] == 5:
                sp += 6
            elif E[fidx] == 6:
                if rev:
                    rev = False
                else:
                    rev = True
                    revstart = time.time()
                score += 500
            elif E[fidx] == 7:
                foody = True
                foodstart = time.time()
           
            score += 100
            print(score)
            sp += 1
            move(fidx)
        else:
            S.pop()




       




        for i in S:
            if foody:
                pygame.draw.ellipse(SUR, (255,255,255), (i[0]*size, i[1]*size, size, size))
            else:
                pygame.draw.rect(SUR, (0,255,0), (i[0]*size, i[1]*size, size, size))
       
        for i in range(1,W):
            if map_state:
                pygame.draw.line(SUR, (100,100,100), (size*i, 0), (size*i, H*size), 2)
            else:
                pygame.draw.line(SUR, (255,255,255), (size*i, 0), (size*i, H*size), 2)




        for i in range(1,H):
            if map_state:
                pygame.draw.line(SUR, (100,100,100), (0, size*i), (W*size, size*i), 2)
            else:
                pygame.draw.line(SUR, (255,255,255), (0, size*i), (W*size, size*i), 2)




        if rev:
            remess = re_mess.render(f"헤롱헤롱 해제까지 {round(5-(time.time() - revstart))}", True, (255,255,0))
            SUR.blit(remess, (0,0))
        if map_state:
            mumess = mu_mess.render(f"맵 무적 상태 해제까지 {round(4-(time.time() - mapstart))} ", True, (154, 0, 255))
            SUR.blit(mumess, (0,30))
   




    else:
        m = mess.render("GAME OVER", True, (255,0,0))
        mx, my = m.get_width(), m.get_height()
        SUR.blit(m, (W*size//2 - mx//2,  H*size//2 - my//2))




    pygame.display.flip()
    FPS.tick(sp)










