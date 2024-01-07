import pygame as pg
import modelPh
import math
from typing import ClassVar
from typing import Final
from button import Button



pg.init()

#константы
WIDTH, HEIGHT = 800, 700
FPS : Final = 60

modelColor : Final = pg.Color('black')
textColor : Final = pg.Color('black')
objectColor : Final = (73,16,139)
buttonNoactive : Final = (226,110,229)
buttonActive : Final = (126,48,225)
windowCol : Final = pg.Color('#F3F8FF')
color_inactive : Final = pg.Color('#E26EE5')
color_active : Final = pg.Color('#49108B')
font : Final = pg.font.Font(None, 32)
font2 : Final = pg.font.Font(None, 20)

#создание окна
window = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption('Modeling')
window.fill(windowCol)
clock = pg.time.Clock()

# данные для визуализации модели
v = 8
a = 0

distPix: Final = 300
posStart: Final = 150
heigh : Final = 400
mnozh : Final = 20
rad : Final = 5

LineEnd = posStart + distPix

Model = modelPh.MyClass(posStart, heigh, distPix/mnozh, v, a)

# отрисовка модели
def drawBase(col = windowCol):
    window.fill(col)

    R = Model.R*mnozh + rad
    alpha = Model.alpha
    pg.draw.line(window, modelColor, [0, heigh+rad], [LineEnd, heigh+rad], 3)
    pg.draw.arc(window, modelColor,(LineEnd-R, heigh+rad-2*R,2*R , 2*R), 3*math.pi/2, 3*math.pi/2 + alpha, 1)

    Button.buttons.draw(window)


drawBase()
el = pg.draw.circle(window,objectColor,(posStart,heigh),rad)


# создание кнопочек и полей с текстом
input_box = pg.Rect(600, 100, 100, 32)
input_boxA = pg.Rect(600, 150, 100, 32)
input_boxM = pg.Rect(100, 600, 100, 32)
input_boxR = pg.Rect(250, 600, 100, 32)
input_boxAL = pg.Rect(400, 600, 100, 32)
input_boxT = pg.Rect(550, 600, 100, 32)

color = color_inactive
active = False

active2 = False
color2 = color_inactive

colorM = color_inactive
activeM = False

colorR = color_inactive
activeR = False

colorAL = color_inactive
activeAL = False

colorT = color_inactive
activeT = False

textInputBoxV = 'Vo = 8'
textInputBoxA = 'Ao = 0'
textInputBoxM = 'm = 3'
textInputBoxR = 'R = 5'
textInputBoxT = r'μ = 0.04'
textInputBoxAL = r'απ/6 = 4'


Uans = font2.render('Минимальное v_0 при данных параметрах, когда тело проходит всю кривую: ' + str(Model.v_0_ans), True,  textColor)
window.blit(Uans, (100,550))


textT = 't: '
textV = '|v|: '
textA = '|a|: '

window.blit(font.render(textT, True,  textColor), (600,200))
window.blit(font.render(textV, True,  textColor), (600,250))
window.blit(font.render(textA, True,  textColor), (600,300))


# отрисовка движения модели
def model():
    posY = heigh
    posx = posStart

    Model.v_0 = v
    Model.a_0 = a
    Model.DO()
    drawBase()
    pg.draw.circle(window,objectColor,(posx, posY),5)


    for i in range (0, len(Model.x_)):
        drawBase()

        forX = posx+(Model.x_[i]-posx)*mnozh
        forY = posY-(Model.y_[i]-posY)*mnozh
        if (forX < -5 or forY < -5):
            continue
        pg.draw.circle(window,objectColor,(forX, posY-(Model.y_[i]-posY)*mnozh),5)

        # отрисовка полей с текстом
        txt_surface = font.render(textInputBoxV, True, color_inactive)
        width = max(100, txt_surface.get_width()+10)
        input_box.w = width
        window.blit(txt_surface, (input_box.x+5, input_box.y+5))
        pg.draw.rect(window, color, input_box, 2)

        txt_surface = font.render(textInputBoxA, True, color_inactive)
        width = max(100, txt_surface.get_width()+10)
        input_boxA.w = width
        window.blit(txt_surface, (input_boxA.x+5, input_boxA.y+5))
        pg.draw.rect(window, color2, input_boxA, 2)

        txt_surface = font.render(textInputBoxT, True, color_inactive)
        width = max(100, txt_surface.get_width()+10)
        input_boxT.w = width
        window.blit(txt_surface, (input_boxT.x+5, input_boxT.y+5))
        pg.draw.rect(window, colorT, input_boxT, 2)

        txt_surface = font.render(textInputBoxR, True, color_inactive)
        width = max(100, txt_surface.get_width()+10)
        input_boxR.w = width
        window.blit(txt_surface, (input_boxR.x+5, input_boxR.y+5))
        pg.draw.rect(window, colorR, input_boxR, 2)

        txt_surface = font.render(textInputBoxAL, True, color_inactive)
        width = max(100, txt_surface.get_width()+10)
        input_boxAL.w = width
        window.blit(txt_surface, (input_boxAL.x+5, input_boxAL.y+5))
        pg.draw.rect(window, colorAL, input_boxAL, 2)

        txt_surface = font.render(textInputBoxM, True, color_inactive)
        width = max(100, txt_surface.get_width()+10)
        input_boxM.w = width
        window.blit(txt_surface, (input_boxM.x+5, input_boxM.y+5))
        pg.draw.rect(window, colorM, input_boxM, 2)

        Uans = font2.render('Минимальное v_0 при данных параметрах, когда тело проходит всю кривую: ' + str(Model.v_0_ans), True,  textColor)
        window.blit(Uans, (50,550)) 

        
        textT = str(Model.t_[i])
        point = textT.find('.')
        textT = 't: ' + textT[:point+3]+ ' c'
        textV = '|v|: ' + f'{Model.v_[i]:.2f}' + ' м/с'
        textA = '|a|: ' + f'{Model.a_[i]:.2f}'+ ' м/с^2'

        window.blit(font.render(textT, True,  textColor), (600,200))
        window.blit(font.render(textV, True,  textColor), (600,250))
        window.blit(font.render(textA, True, textColor), (600,300))


        pg.display.update()



b1 = Button("RUN", pos=(350,40),
            fontsize=30,
            colors="black on green",
            hover_colors="black on red",
            command=lambda: model())
b1.setColors(textColor,buttonActive, textColor, buttonNoactive)

while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            quit()
        if event.type == pg.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    # Toggle the active variable.
                    active = not active
                    active2 = False
                    activeM = False
                    activeR = False
                    activeT = False
                    activeAL = False
                elif input_boxA.collidepoint(event.pos):
                    active = False
                    activeM = False
                    activeT = False
                    activeR = False
                    activeAL = False
                    active2 = not active2
                elif input_boxM.collidepoint(event.pos):
                    activeM = not activeM
                    active = False
                    activeT = False
                    activeR = False
                    active2 = False
                    activeAL = False
                elif input_boxR.collidepoint(event.pos):
                    activeR = not activeR
                    active = False
                    activeM = False
                    active2 = False
                    activeT = False
                    activeAL = False
                elif input_boxAL.collidepoint(event.pos):
                    activeAL = not activeAL
                    active = False
                    activeR = False
                    activeM = False
                    activeT = False
                    active2 = False
                elif input_boxT.collidepoint(event.pos):
                    activeAL = False
                    active = False
                    activeR = False
                    activeT = not activeT
                    activeM = False
                    active2 = False
                else:
                    activeM = False
                    activeT = False
                    activeAL = False
                    activeR = False
                    active = False
                    active2 = False

                # Change the current color of the input box.
                color = color_active if active else color_inactive
                color2 = color_active if active2 else color_inactive
                colorM = color_active if activeM else color_inactive
                colorR = color_active if activeR else color_inactive
                colorT = color_active if activeT else color_inactive
                colorAL = color_active if activeAL else color_inactive
        if event.type == pg.KEYDOWN:
                if active:
                    if event.key == pg.K_RETURN:
                        print(textInputBoxV)
                        color = color_active
                        try:
                            v = textInputBoxV.find("Vo = ")
                            v = textInputBoxV[(v+5) :]
                            v = int(v)
                            print(v)
                        except:
                            textInputBoxV = 'Vo = '
                        
                    elif event.key == pg.K_BACKSPACE:
                        textInputBoxV = textInputBoxV[:-1]
                    else:
                        textInputBoxV += event.unicode
                if activeR:
                    if event.key == pg.K_RETURN:
                        print(textInputBoxR)
                        colorR = color_active
                        try:
                            r = textInputBoxR.find("R = ")
                            r = textInputBoxR[(r+4) :]
                            r = int(r)
                            print(r)
                            Model.R = r
                            Model.BinPoisk()
                        except:
                            textInputBoxR = 'R = '
                        
                    elif event.key == pg.K_BACKSPACE:
                        textInputBoxR = textInputBoxR[:-1]
                    else:
                        textInputBoxR += event.unicode
                if activeM:
                    if event.key == pg.K_RETURN:
                        print(textInputBoxM)
                        colorM = color_active
                        try:
                            m = textInputBoxM.find("m = ")
                            m = textInputBoxM[(m+4) :]
                            m = int(m)
                            print(m)
                            Model.m = m
                            Model.BinPoisk()
                        except:
                            textInputBoxM = 'm = '
                        
                    elif event.key == pg.K_BACKSPACE:
                        textInputBoxM = textInputBoxM[:-1]
                    else:
                        textInputBoxM += event.unicode
                if active2:
                    if event.key == pg.K_RETURN:
                        print(textInputBoxA)
                        color2 = color_active
                
                        try:
                            a = textInputBoxA.find("Ao = ")
                            a = textInputBoxA[(a+5) :]
                            a = int(a)
                            print(a)
                            Model.a_0 = a
                            Model.BinPoisk()
                        except:
                            textInputBoxA = 'Ao = '
                        
                    elif event.key == pg.K_BACKSPACE:
                        textInputBoxA = textInputBoxA[:-1]
                    else:
                        textInputBoxA += event.unicode
                if activeAL:
                    if event.key == pg.K_RETURN:
                        print(textInputBoxAL)
                        colorAL = color_active
                        try:
                            alpha = textInputBoxAL.find("απ/6 = ")
                            alpha = textInputBoxAL[(alpha+7) :]
                            alpha = int(alpha)
                            print(alpha)
                            Model.alpha = math.pi*alpha/6
                            Model.BinPoisk()
                        except:
                            textInputBoxAL = 'απ/6 = '
                        
                    elif event.key == pg.K_BACKSPACE:
                        textInputBoxAL = textInputBoxAL[:-1]
                    else:
                        textInputBoxAL += event.unicode
                if activeT:
                    if event.key == pg.K_RETURN:
                        print(textInputBoxT)
                        colorT = color_active
                        try:
                            tr = textInputBoxT.find("μ = ")
                            tr = textInputBoxT[(tr+4) :]
                            tr = float(tr)
                            print(tr)
                            Model.mu = tr
                            Model.BinPoisk()
                        except:
                            textInputBoxT = 'μ = '
                        
                    elif event.key == pg.K_BACKSPACE:
                        textInputBoxT = textInputBoxT[:-1]
                    else:
                        textInputBoxT += event.unicode
    #модель
    drawBase()
    el = pg.draw.circle(window,objectColor,(posStart,heigh),5)

    # Vo =
    txt_surface = font.render(textInputBoxV, True, color)
    width = max(100, txt_surface.get_width()+10)
    input_box.w = width
    window.blit(txt_surface, (input_box.x+5, input_box.y+5))
    pg.draw.rect(window, color, input_box, 2)

    # R =
    txt_surface = font.render(textInputBoxR, True, colorR)
    width = max(100, txt_surface.get_width()+10)
    input_boxR.w = width
    window.blit(txt_surface, (input_boxR.x+5, input_boxR.y+5))
    pg.draw.rect(window, colorR, input_boxR, 2)

    # mu =
    txt_surface = font.render(textInputBoxT, True, colorT)
    width = max(100, txt_surface.get_width()+10)
    input_boxT.w = width
    window.blit(txt_surface, (input_boxT.x+5, input_boxT.y+5))
    pg.draw.rect(window, colorT, input_boxT, 2)

    # alpha =
    txt_surface = font.render(textInputBoxAL, True, colorAL)
    width = max(100, txt_surface.get_width()+10)
    input_boxAL.w = width
    window.blit(txt_surface, (input_boxAL.x+5, input_boxAL.y+5))
    pg.draw.rect(window, colorAL, input_boxAL, 2)


    # m =
    txt_surface = font.render(textInputBoxM, True, colorM)
    width = max(100, txt_surface.get_width()+10)
    input_boxM.w = width
    window.blit(txt_surface, (input_boxM.x+5, input_boxM.y+5))
    pg.draw.rect(window, colorM, input_boxM, 2)

    # Ao =
    txt_surface = font.render(textInputBoxA, True, color2)
    width = max(100, txt_surface.get_width()+10)
    input_boxA.w = width
    window.blit(txt_surface, (input_boxA.x+5, input_boxA.y+5))
    pg.draw.rect(window, color2, input_boxA, 2)

    # Run
    pg.draw.rect(window,  buttonActive, (350, 40, 65,33))
    txt_surface = font.render("RUN", True,  textColor)
    window.blit(txt_surface, (355, 45))

    # v_ans =
    Vans = font2.render('Минимальное v_0 при данном ускорении, когда тело проходит всю кривую: ' + str(Model.v_0_ans), True,  textColor)
    window.blit(Vans, (50,550))   

    window.blit(font.render(textT, True,  textColor), (600,200))
    window.blit(font.render(textV, True,  textColor), (600,250))
    window.blit(font.render(textA, True,  textColor), (600,300))

    Button.buttons.update()
    Button.buttons.draw(window)
    
    pg.display.update()
    clock.tick(FPS)
pg.ex
pg.quit()

