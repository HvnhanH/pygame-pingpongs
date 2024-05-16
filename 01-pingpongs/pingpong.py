import pygame
import time
import random
import math

from define import*


pygame.init()

pygame.font.init()
SCORE_FONT = pygame.font.SysFont("comicsans",50)

WIN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("PingPong")


font = pygame.font.Font('freesansbold.ttf',24)

#tao class btn 
class Button:
    def __init__(self,win,txt,pos):
        self.win=win
        self.text=txt
        self.pos = pos
        self.default_color=COLOR_AQUA
        self.hover_color=COLOR_RED
        self.button = pygame.rect.Rect((self.pos[0],self.pos[1]),(120,40))

    def draw(self):
        if self.button.collidepoint(pygame.mouse.get_pos()):
            color = self.hover_color
        else:
            color = self.default_color
        pygame.draw.rect(self.win, color,self.button,0 , 5)
        pygame.draw.rect(self.win,COLOR_GRAY,self.button, 2, 5)
        text = font.render(self.text,True, 'black')
        self.win.blit(text,(self.pos[0]+15, self.pos[1] +7))

    def check_clicked(self):
        if self.button.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
            return True
        else:
            return False
        
class Ball():
    def __init__(self,x,y,radius):
        self.x=self.original_x = x
        self.y= self.original_y = y
        self.radius = radius
        self.x_vel = MAX_VEL
        self.y_vel =0

    def draw(self,win):
        pygame.draw.circle(win, COLOR_WHITE, (self.x,self.y),self.radius)

    def move(self):
        self.x += self.x_vel
        self.y += self.y_vel

    def reset(self):
        self.x = self.original_x
        self.y = self.original_y
        self.y_vel=0
        self.x_vel *=-1

class Player():
    x=0
    y=0
    color=""
    def __init__(self,color,x,y,height) -> None:
        self.x=self.original_x=x
        self.y=self.original_y=y
        self.color=color
        self.height=height
    #ve nguoi choi
    def draw(self,win):
        pygame.draw.rect(win,self.color,(self.x,self.y,PLAYER_WIDTH,self.height))

    def move(self,up=True):
        if up:
            self.y -= PLAYER_V
        else:
            self.y += PLAYER_V
    
    def reset(self):
        self.x = self.original_x
        self.y = self.original_y
        
#ham ve man hinh va nguoi choi
def draw_game(win,players, ball,left_score, right_score):
    win.fill(COLOR_BLACK)

    left_score_text = SCORE_FONT.render(f"{left_score}",1, COLOR_WHITE)
    right_score_text = SCORE_FONT.render(f"{right_score}",1, COLOR_WHITE)
    win.blit(left_score_text,(WINDOW_WIDTH//4-left_score_text.get_width()//2, 20))
    win.blit(right_score_text,(WINDOW_WIDTH * (3/4) - right_score_text.get_width()//2,20))

    for Player in players:
        Player.draw(win)
    
    for i in range (10,WINDOW_HEIGHT,WINDOW_HEIGHT//20):
        if i % 2 ==1:
            continue
        pygame.draw.rect(win,COLOR_YELLOW,(WINDOW_WIDTH//2 -5,i,LINE_WIDTH,WINDOW_HEIGHT//20))
    ball.draw(win)
    pygame.display.update()
#ham tinh kc item va ball
def check_item(item,ball):
    kc=math.sqrt((ball.x-item[0])**2 + (ball.y-item[1])**2)
    return kc <= 8+ BALL_RADIUS
#ham su ly va cham
def handle_collision(win,ball,left_player,right_player,items,left_score, right_score):
    if ball.y + BALL_RADIUS >= WINDOW_HEIGHT:
        ball.y_vel *= -1
    elif ball.y - BALL_RADIUS <=0:
        ball.y_vel *= -1
    
    #bong cham player
    if ball.x_vel <0:
        if ball.y>= left_player.y and ball.y <= left_player.y + left_player.height:
            if ball.x - BALL_RADIUS <= left_player.x +PLAYER_WIDTH:
                ball.x_vel *= -1

                middle_y = left_player.y + left_player.height /2
                difference_in_y = middle_y - ball.y
                reduction_factor = (left_player.height/2)/ MAX_VEL
                y_vel= difference_in_y / reduction_factor
                ball.y_vel= y_vel * -1
    else:
        if ball.y >= right_player.y and ball.y <= right_player.y + right_player.height:
            if ball.x + BALL_RADIUS >= right_player.x:
                ball.x_vel *= -1

                middle_y = right_player.y + right_player.height /2
                difference_in_y = middle_y - ball.y
                reduction_factor = (right_player.height/2)/ MAX_VEL
                y_vel= difference_in_y / reduction_factor
                ball.y_vel= y_vel * -1

def handle_player_movement(keys,left_player,right_player):
    if keys[pygame.K_w] and left_player.y - PLAYER_V >=0:
        left_player.move(up=True)
    if keys[pygame.K_s] and left_player.y + PLAYER_V +PLAYER_HEIGHT<=WINDOW_HEIGHT:
        left_player.move(up=False)

    if keys[pygame.K_UP] and right_player.y - PLAYER_V >=0:
        right_player.move(up=True)
    if keys[pygame.K_DOWN] and right_player.y + PLAYER_V +PLAYER_HEIGHT<=WINDOW_HEIGHT:
        right_player.move(up=False)
#ham tao item
def create_item():
        itemx = round(random.randrange(150, 550) ) 
        itemy = round(random.randrange(10, 490))
        item_chucnang = round(random.randrange(1,4))
        return [itemx,itemy,item_chucnang]
#ham ve item
def draw_item(win,items):
    for item in items:
        if item [2]==1:
            pygame.draw.circle(win, COLOR_GREEN, (item[0],item[1]),8)
        if item[2]==2:
            pygame.draw.circle(win, COLOR_YELLOW, (item[0],item[1]),8)
        if item[2] == 3:
            pygame.draw.circle(win, COLOR_BLUE, (item[0],item[1]),8)
    pygame.display.update()

def draw_menu():
    background_image = pygame.image.load(PATH_IMAGES+"/pingpong.jpg")
    background_suface=pygame.transform.scale(background_image,(WINDOW_WIDTH,WINDOW_HEIGHT))
    WIN.blit(background_suface,(0,0))
    command=0
    play_btn1=Button(WIN,'Play 1P',(WINDOW_WIDTH//2 - 40 ,150))
    play_btn1.draw()
    play_btn2=Button(WIN,'Play 2P',(WINDOW_WIDTH//2 - 40 ,200))
    play_btn2.draw()
    exit_btn=Button(WIN,'Exit',(WINDOW_WIDTH//2 -40 ,250))
    exit_btn.draw()
    pygame.display.update()
    if play_btn1.check_clicked():
        command = 1
    if play_btn2.check_clicked():
        command = 2
    if exit_btn.check_clicked():
        command = 3 
    return command

def draw_pause():
    WIN.fill(COLOR_WHITE)
    command = 0
    Resume_btn=Button(WIN,'Resume',(WINDOW_WIDTH//2 - 60 ,150))
    Resume_btn.draw()
    Restart_btn=Button(WIN,'Restart',(WINDOW_WIDTH//2 - 60 ,200))
    Restart_btn.draw()
    quit_btn=Button(WIN,'Quit',(WINDOW_WIDTH//2 - 60 ,400))
    quit_btn.draw()
    pygame.display.update()
    if Resume_btn.check_clicked():
        command = 1
    if Restart_btn.check_clicked():
        command = 2
    if quit_btn.check_clicked():
        command = 3
    pygame.display.update()
    return command

#ham ai
def handle_ai_movement(ball, right_player):
    if ball.y < right_player.y and right_player.y - PLAYER_V >= 0:
        right_player.move(up=True)
    elif ball.y > right_player.y + right_player.height and right_player.y + PLAYER_V + PLAYER_HEIGHT <= WINDOW_HEIGHT:
        right_player.move(up=False)

def main():
    run = True
    clock = pygame.time.Clock()
    items = []
    last_item_time = time.time()

    #tao player
    left_player= Player(COLOR_REDBTN,10,WINDOW_HEIGHT//2-PLAYER_HEIGHT//2,PLAYER_HEIGHT)
    right_player= Player(COLOR_BLUE,WINDOW_WIDTH-10-PLAYER_WIDTH,WINDOW_HEIGHT//2-PLAYER_HEIGHT//2,PLAYER_HEIGHT)

    #tao ball
    ball = Ball(WINDOW_WIDTH//2, WINDOW_HEIGHT//2, BALL_RADIUS)

    time_item2=time.time()
    time_item1=time.time()
    paused = False
    left_score =0
    right_score =0
    main_menu=True
    while run:
        #gioi han so khung hinh no chay tren s
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type== pygame.QUIT:
                run = False
                break
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    paused = not paused
                    time_item2=time.time()
                    time_item1=time.time()
                    last_item_time = time.time()

        if main_menu:
            command = draw_menu()
            if command ==1:
                single_player = True
                main_menu=False
                last_item_time = time.time()
            if command ==2:
                single_player = False
                main_menu=False
                last_item_time = time.time()
            if command == 3:
                run=False
        else:
            if paused == True:
                t_pause=draw_pause()
                if t_pause==1:
                    paused= not paused
                    time_item2=time.time()
                    time_item1=time.time()
                    last_item_time = time.time()
                if t_pause==2:
                    ball.reset()
                    left_player.reset()
                    right_player.reset()
                    left_score=0
                    right_score=0
                    items = []
                    last_item_time = time.time()
                    paused= not paused
                if t_pause==3:
                    ball.reset()
                    left_player.reset()
                    right_player.reset()
                    left_score=0
                    right_score=0
                    items = []
                    last_item_time = time.time()
                    main_menu=True

                continue
            
            draw_game(WIN, [left_player,right_player], ball, left_score,right_score)
            #lay phim dc nhan
            keys = pygame.key.get_pressed()
            handle_player_movement(keys,left_player,right_player)

            ball.move()
            handle_collision(WIN,ball,left_player,right_player,items,left_score,right_score)
            if time.time() - last_item_time>3:
                if len(items)<5:
                    items.append(create_item())
                last_item_time=time.time()
            draw_item(WIN,items)
                
            if single_player:
                handle_ai_movement(ball,right_player)

            if ball.x <0:
                right_score +=1
                ball.reset()
                draw_game(WIN, [left_player,right_player], ball, left_score,right_score)
            
            elif ball.x>WINDOW_WIDTH:
                left_score +=1
                ball.reset()
                draw_game(WIN, [left_player,right_player], ball, left_score,right_score)
            #bong cham item
            for item in items:
                if check_item(item,ball):
                    if item [2] ==1:
                        if ball.x_vel <0:
                            right_score +=1
                        else:
                            left_score +=1
                    if item [2] ==2:
                        if ball.x_vel <0:
                            right_player.height=PLAYER_HEIGHT*2
                            time_item2=time.time()
                        else:
                            left_player.height=PLAYER_HEIGHT*2
                            time_item1=time.time()
                    if item [2] ==3:
                        if ball.x_vel <0 and right_score>0:
                            right_score -=1
                        if ball.x_vel >0 and left_score>0:
                            left_score -=1
                        
                    items.remove(item)
            if time.time()-time_item2>5:
                right_player.height=PLAYER_HEIGHT
            if time.time()-time_item1>5:
                left_player.height=PLAYER_HEIGHT
            won = False
            if left_score >= WINING_SCORE:
                won = True
                win_text = "Left Player Won!"
            elif right_score >= WINING_SCORE:
                won = True
                win_text = "Right Player Won!"

            if won: 
                text = SCORE_FONT.render(win_text,1,COLOR_WHITE)
                WIN.blit(text, (WINDOW_WIDTH//2 - text.get_width()//2, WINDOW_HEIGHT//2 - text.get_height()//2))
                pygame.display.update()
                pygame.time.delay(5000)
                last_item_time=time.time()
                items=[]
                ball.reset()
                left_player.reset()
                right_player.reset()
                left_score=0
                right_score=0

    pygame.quit()

if __name__=="__main__":
    main()
