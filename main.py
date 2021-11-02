import pygame as py
import os
import sys

from models.buttons import Buttons
py.font.init()#per libreria font
py.mixer.init()#per libreria suoni



#definisco larghezza finestra di gioco. sono costanti in maiuscolo
WIDTH,HEIGTH=900,500
WINDOWSIZE=py.display.set_mode((WIDTH,HEIGTH))#metodo set mode per dire a pygame di creare una finestra larga con miei parametri.
#doppie tonde sono una tupla in Python
py.display.set_caption("Space Battle!")
py.display.set_icon(py.image.load(os.path.join("Assets","spaceicon.png")))

HEALTHFONT=py.font.SysFont('segoeui',40)
FPSFONT=py.font.SysFont('consolas',14)
WINNERFONT=py.font.SysFont('segoeui',100)

BULLETHITSOUND=py.mixer.Sound(os.path.join("Assets","Grenade+1.mp3"))
FIRESOUND=py.mixer.Sound(os.path.join("Assets","Gun+Silencer.mp3"))


#fps per dire quante volte al secondo deve eseguire il ciclo del gioco
GAMESONG=py.mixer.Sound(os.path.join("Assets","spacesong.mp3"))
FPS=60
SPACESHIP_WIDTH,SPACESHIP_HEIGTH=55,40
VEL=5
BULLETVEL=10#velocita proiettile
MAXBULLETS=10#numero di proiettili
REDBULLETSCOLOR=(255,0,0)
YELLOWBULLETSCOLOR=(255,255,0)
BORDER=py.Rect(WIDTH/2-5,0,10,HEIGTH)#x,y,larghezza,altezza
BORDERCOLOR=(0,0,0)
TEXTCOLOR=(255,255,255)

YELLOW_HIT=py.USEREVENT+1
RED_HIT=py.USEREVENT+2#numero serve per differenziare eventi con id

EXITBUTTONPRESSED=py.USEREVENT+3
RESTARTBUTTONPRESSED=py.USEREVENT+4
PLAYAGAINBUTTONIMAGE=py.transform.scale(py.image.load(os.path.join("Assets","replaybutton.png")),(130,100))
EXITGAMEBUTTONIMAGE=py.transform.scale(py.image.load(os.path.join("Assets","quitgamebutton.png")),(130,100))
#uso os perchè in base a so cambiano separatori path
REDSPACESHIP_IMAGE=py.image.load(os.path.join('Assets','spaceship_red.png')).convert_alpha()
YELLOWSPACESHIP_IMAGE=py.image.load(os.path.join('Assets','spaceship_yellow.png')).convert_alpha()
SPACEBACKGROUND=py.transform.scale(py.image.load(os.path.join("Assets",'space.png')),(WIDTH,HEIGTH)).convert()
YELLOWSPACESHIP=py.transform.rotate(py.transform.scale(YELLOWSPACESHIP_IMAGE,(SPACESHIP_WIDTH,SPACESHIP_HEIGTH)),90)
REDSPACESHIP=py.transform.rotate(py.transform.scale(REDSPACESHIP_IMAGE,(SPACESHIP_WIDTH,SPACESHIP_HEIGTH)),270)#siccome immagine è troppo grande la rimpiccioliamo per disegnarla e la ruotiamo



def drawobjects(red,yellow,redbullets,yellowbullets,redhealth,yellowhealth,actualfps):
    WINDOWSIZE.blit(SPACEBACKGROUND,(0,0))
    py.draw.rect(WINDOWSIZE,BORDERCOLOR,BORDER,5,5)
    redhealthtext=HEALTHFONT.render(f"Salute:{str(redhealth)}",True,TEXTCOLOR)
    yellowhealthtext=HEALTHFONT.render(f"Salute:{str(yellowhealth)}",True,TEXTCOLOR)
    actualfps=FPSFONT.render(f"FPS:{str(int(actualfps))}",True,TEXTCOLOR)
    WINDOWSIZE.blit(redhealthtext,(WIDTH-redhealthtext.get_width()-10,10))
    WINDOWSIZE.blit(yellowhealthtext,(10,10))
    WINDOWSIZE.blit(YELLOWSPACESHIP,(yellow.x,yellow.y))
    WINDOWSIZE.blit(actualfps,(820,480))
    #capire come disegnarlo solo in caso di fine gioco
     #in pygame coordinate partono da angolo sinistro. primo valore è la x secondo e la y
    #se aumento valore x vado verso destra
    #se aumento valore y vado verso sinistra(giu)
    WINDOWSIZE.blit(REDSPACESHIP,(red.x,red.y))
    for bullet in redbullets:
        py.draw.rect(surface=WINDOWSIZE,color=REDBULLETSCOLOR,rect=bullet)
    for bullet in yellowbullets:
        py.draw.rect(surface=WINDOWSIZE,color=YELLOWBULLETSCOLOR,rect=bullet)

    
    
def moveyellow(keys_pressed,yellow):
    if keys_pressed[py.K_a] and yellow.x-VEL>0:#sinistra
        yellow.x-=VEL
    if keys_pressed[py.K_d] and yellow.x+VEL+yellow.width<BORDER.x:#destra
        yellow.x+=VEL
    if keys_pressed[py.K_w] and yellow.y-VEL>0:#su
        yellow.y-=VEL
    if keys_pressed[py.K_s] and yellow.y+VEL+yellow.height<HEIGTH-10:#giu
        yellow.y+=VEL

def movered(keys_pressed,red):
    if keys_pressed[py.K_LEFT] and red.x-VEL>BORDER.x+BORDER.width:#sinistra
        red.x-=VEL
    if keys_pressed[py.K_RIGHT]and red.x+VEL+red.width<WIDTH:#destra
        red.x+=VEL
    if keys_pressed[py.K_UP]and red.y-VEL>0:#su
        red.y-=VEL
    if keys_pressed[py.K_DOWN]and red.y+VEL+red.height<HEIGTH-10:#giu
        red.y+=VEL

def firebullets(yellowbullets,yellow,redbullets,red):
    for bullet in yellowbullets:
        bullet.x+=BULLETVEL
        if red.colliderect(bullet):
            py.event.post(py.event.Event(RED_HIT))
            yellowbullets.remove(bullet)
        elif bullet.x>WIDTH:
            yellowbullets.remove(bullet)

    for bullet in redbullets:
        bullet.x-=BULLETVEL
        if yellow.colliderect(bullet):
            py.event.post(py.event.Event(YELLOW_HIT))
            redbullets.remove(bullet)
        elif bullet.x<0:
            redbullets.remove(bullet)

def drawwinner(WIN,wintext,replaybutton,quitgamebutton):
    drawtext=WINNERFONT.render(wintext,True,TEXTCOLOR)
    if(WIN):
        WINDOWSIZE.blit(drawtext,(WIDTH/2-drawtext.get_width()/2,HEIGTH/2-drawtext.get_height()/2))
        replaybuttonrect=replaybutton.image.get_rect()
        replaybuttonrect.center=(drawtext.get_width()/2-80+80,replaybutton.y+50)
        WINDOWSIZE.blit(replaybutton.image,replaybuttonrect)#a blit puoi passare un rect che ottengo da immagine facendo metodo get_rect()
        quitgamebuttonrect=quitgamebutton.image.get_rect()
        quitgamebuttonrect.center=(drawtext.get_width()/2+80+quitgamebutton.x,quitgamebutton.y+50)
        WINDOWSIZE.blit(quitgamebutton.image,quitgamebuttonrect)
        if replaybuttonrect.collidepoint(py.mouse.get_pos()):
            #so he sono sopra il bottone con il mouse
            if py.mouse.get_pressed()[0]==1 and replaybutton.everclicked==False:#becca più di un click
               #tasto di posizione 0 è mouse sinistro se è 1 significa che è premuto
                replaybutton.everclicked=True
                #codice per fare nuova partita
                main()#ricomincio ciclo
            elif py.mouse.get_pressed()[0]==0:
                replaybutton.everclicked=False
               
           
        if quitgamebuttonrect.collidepoint(py.mouse.get_pos()):
            if py.mouse.get_pressed()[0]==1 and quitgamebutton.everclicked==False:
                quitgamebutton.everclicked=True
                return True
                
    else:#qua posso pure lasciare disegnare delle surface tanto non sono visibili
        #  e non m'interessa avere metodi collisioni dei rect 
        #  per sapere se utente è sopra il bottone
        WINDOWSIZE.blit(drawtext,(WIDTH+10,HEIGTH+10))
        WINDOWSIZE.blit(replaybutton.image,(WIDTH+10,HEIGTH+10))
        WINDOWSIZE.blit(quitgamebutton.image,(WIDTH+10,HEIGTH+10))
        

#questa funzione è il ciclo principale del gioco. tutti i giochi sono cicli
def main():
    red=py.Rect(700,300,SPACESHIP_WIDTH,SPACESHIP_HEIGTH)
    yellow=py.Rect(100,300,SPACESHIP_WIDTH,SPACESHIP_HEIGTH)
    replaybutton=Buttons(200,300,PLAYAGAINBUTTONIMAGE)
    quitgamebutton=Buttons(200,300,EXITGAMEBUTTONIMAGE)
    replaybuttonrect=PLAYAGAINBUTTONIMAGE.get_rect()
    quitgamebuttonrect=EXITGAMEBUTTONIMAGE.get_rect()
    redbullets=[]
    yellowbullets=[]
    yellowhealth=100
    redhealth=100
    WIN=False;#se WIN è false i bottoni vengono disegnati fuori dallo schermo. qunado vince qualcuno diventa true e bottoni diventano visibili
    clock=py.time.Clock()
    GAMESONG.play()
    #capire come far partire canzone da un punto preciso
    rungame=True
    
   
    
    while rungame and quitgamebutton.everclicked==False:#io so che bottone non è mai stato cliccato. everclicked è true. poi fine gioco
                                                         #viene visualizzato dialog. premo su quit valore everclicked diventa false. condizione
                                                         #qui del ciclo non è più vera di conseguenza esce dal ciclo chiudendo il gioco
        clock.tick(FPS)
        actualfps=clock.get_fps()
        for event in py.event.get():#qui catturo l'evento di uscita dal gioco. se esco termino ciclo 
            if event.type==py.QUIT:
                rungame=False
                GAMESONG.stop()
            if event.type==py.KEYDOWN:
                if event.key==py.K_LCTRL and len(yellowbullets)<MAXBULLETS:
                    bullet=py.Rect(yellow.x+yellow.width,yellow.y+yellow.height//2,10,5)
                    yellowbullets.append(bullet)
                    FIRESOUND.play()

                if event.key==py.K_RCTRL and len(redbullets)<MAXBULLETS:
                    bullet=py.Rect(red.x,red.y+red.height//2,10,5)
                    redbullets.append(bullet)
                    FIRESOUND.play()
            if event.type==RED_HIT and redhealth>0:
                redhealth-=10
                BULLETHITSOUND.play()
            
            if event.type==YELLOW_HIT and yellowhealth>0:
                yellowhealth-=10
                BULLETHITSOUND.play()
        wintext=''
        if redhealth<=0:
            GAMESONG.stop()
            py.mixer.music.unload();
            WIN=True
            wintext="YELLOW WINS"
            drawwinner(WIN,wintext,replaybutton,quitgamebutton)
            

        if yellowhealth<=0:
            GAMESONG.stop()
            py.mixer.music.unload();
            WIN=True
            wintext="RED WINS"
            drawwinner(WIN,wintext,replaybutton,quitgamebutton)
            

        keys_pressed=py.key.get_pressed()
        moveyellow(keys_pressed,yellow)
        movered(keys_pressed,red)
        firebullets(yellowbullets,yellow,redbullets,red)
        drawobjects(red,yellow,redbullets,yellowbullets,redhealth,yellowhealth,actualfps)
        drawwinner(WIN,wintext,replaybutton,quitgamebutton)
        py.display.update()
    py.font.quit()
    py.mixer.stop()
    py.quit()
    sys.exit()

if __name__=="__main__":#serve se importo questo file in un altro file python per non fare eseguire funzione main in altro file
    main()