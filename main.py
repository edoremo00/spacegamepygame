import pygame as py
import os

#definisco larghezza finestra di gioco. sono costanti in maiuscolo
WIDTH,HEIGTH=900,500
WINDOWSIZE=py.display.set_mode((WIDTH,HEIGTH))#metodo set mode per dire a pygame di creare una finestra larga con miei parametri.
#doppie tonde sono una tupla in Python
py.display.set_caption("Space Battle!")


#fps per dire quante volte al secondo deve eseguire il ciclo del gioco

FPS=60
SPACESHIP_WIDTH,SPACESHIP_HEIGTH=55,40
VEL=5
BORDER=py.Rect(WIDTH/2-5,0,10,HEIGTH)#x,y,larghezza,altezza
BORDERCOLOR=(0,0,0)

#uso os perchè in base a so cambiano separatori path
REDSPACESHIP_IMAGE=py.image.load(os.path.join('Assets','spaceship_red.png'))
YELLOWSPACESHIP_IMAGE=py.image.load(os.path.join('Assets','spaceship_yellow.png'))
YELLOWSPACESHIP=py.transform.rotate(py.transform.scale(YELLOWSPACESHIP_IMAGE,(SPACESHIP_WIDTH,SPACESHIP_HEIGTH)),90)
REDSPACESHIP=py.transform.rotate(py.transform.scale(REDSPACESHIP_IMAGE,(SPACESHIP_WIDTH,SPACESHIP_HEIGTH)),270)#siccome immagine è troppo grande la rimpiccioliamo per disegnarla e la ruotiamo

def drawobjects(red,yellow):
    WINDOWSIZE.fill((255,255,255))
    py.draw.rect(surface=WINDOWSIZE,color=BORDERCOLOR,rect=BORDER)
    WINDOWSIZE.blit(YELLOWSPACESHIP,(yellow.x,yellow.y))
     #in pygame coordinate partono da angolo sinistro. primo valore è la x secondo e la y
    #se aumento valore x vado verso destra
    #se aumento valore y vado verso sinistra(giu)
    WINDOWSIZE.blit(REDSPACESHIP,(red.x,red.y))
    py.display.update()
    
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

#questa funzione è il ciclo principale del gioco. tutti i giochi sono cicli
def main():
    red=py.Rect(700,300,SPACESHIP_WIDTH,SPACESHIP_HEIGTH)
    yellow=py.Rect(100,300,SPACESHIP_WIDTH,SPACESHIP_HEIGTH)
    clock=py.time.Clock()
    rungame=True
    while rungame:
        clock.tick(FPS)
        py.display.update()
        for event in py.event.get():#qui catturo l'evento di uscita dal gioco. se esco termino ciclo 
            if event.type==py.QUIT:
                rungame=False
        keys_pressed=py.key.get_pressed()
        moveyellow(keys_pressed,yellow)
        movered(keys_pressed,red)
        
        
        drawobjects(red,yellow)
    py.quit()

if __name__=="__main__":#serve se importo questo file in un altro file python per non fare eseguire funzione main in altro file
    main()