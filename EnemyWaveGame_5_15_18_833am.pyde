'''
known bugs . . .
 - bullets with enough hp not going through units
 - bullets with not enough hp going through units

to do list . . .
 - fix known bugs
 - fix spread mechanic, so it isnt just a change in y axis
 - make a shop
 - make highscore list
 - ORGANIZE AND COMMENT YOUR CODE
 - save file system for progress
 - OPTIMISE
 - Boss levels
 - map for progression through levels
 
Ideas for the shop
 - unlock different weapons
 - different kinds of auto turrets
 - exploding/bouncing bullets?
 - air support for person
 - gun that shoots a bullet that goes slow then accelerates really fast
 - guided missles
'''

from random import randint
import os
import datetime

global directory
directory = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'bin/')
if os.name == 'nt':
    directory = directory[2:]

#-------------------------------------------------------------------------

class enemy(object):
    maxspeed = 0.4
    startHp = 10.0
    waveCount = 50
    waveUsed = 0
    siz = 20
    objs = []  # registrar
    onscreen = 0

    def __init__(self, style, y=randint(0, 11)):
        # squares
        if style == 1:
            self.xspeed = 4 * random(enemy.maxspeed / 2, enemy.maxspeed)
            self.hp = enemy.startHp

        # ellipses
        elif style == 2:
            self.xspeed = 8 * random(enemy.maxspeed / 2, enemy.maxspeed)
            self.hp = enemy.startHp / 2.5

        # triangles
        elif style == 3:
            self.xspeed = 2 * random(enemy.maxspeed / 2, enemy.maxspeed)
            self.hp = enemy.startHp * 12

        self.y = (60 * y) + 30
        self.style = style
        self.x = -10
        self.colr = color(random(0, 100), random(0, 255), random(0, 200))
        enemy.objs.append(self)
        enemy.waveUsed += 1
        enemy.onscreen += 1

    def display(self):
        fill(self.colr)

        # square
        if self.style == 1:
            rect(self.x, self.y, enemy.siz, enemy.siz)
            startHp = enemy.startHp
            if self.hp != startHp:
                fill(255, 0, 0)
                rect(self.x, self.y - 15, 26, 5)
                fill(0, 255, 0)
                rect(self.x - (13 - (self.hp / startHp) * 13),
                     self.y - 15, (self.hp / startHp) * 26, 5)

        # ellipses
        elif self.style == 2:
            ellipse(self.x, self.y, enemy.siz, enemy.siz)
            startHp = enemy.startHp / 2.5
            if self.hp != startHp:
                fill(255, 0, 0)
                rect(self.x, self.y - 15, 26, 5)
                fill(0, 255, 0)
                rect(self.x - (13 - (self.hp / startHp) * 13),
                     self.y - 15, (self.hp / startHp) * 26, 5)

        # triangles
        elif self.style == 3:
            triangle(self.x - (enemy.siz / 1.3), self.y + (enemy.siz / 1.3), self.x +
                     (enemy.siz / 1.3), self.y + (enemy.siz / 1.3), self.x, self.y - (enemy.siz / 1.3))
            startHp = enemy.startHp * 12
            if self.hp != startHp:
                fill(255, 0, 0)
                rect(self.x, self.y - 15, 26, 5)
                fill(0, 255, 0)
                rect(self.x - (13 - (self.hp / startHp) * 13),
                     self.y - 15, (self.hp / startHp) * 26, 5)

    def update(self):
        global health
        self.x += self.xspeed
        if self.x >= width + 10:
            self.kill()
            health -= 0.01

    def kill(self):
        self.xspeed = 0
        self.x = -200
        self.y = -200
        enemy.onscreen -= 1
        enemy.maxspeed += 0.001
        enemy.objs.remove(self)
        del self

    def score(self):
        global triscore, squarescore, cirscore, score, money
        if self.style == 1:
            squarescore += 1
            money += 10
        elif self.style == 2:
            cirscore += 1
            money += 7
        elif self.style == 3:
            triscore += 1
            money += 100
        score += 1

#-------------------------------------------------------------------------

class projectile(object):
    global itemBuys
    objs = []
    weapon = 0  # decides which weapon you have
    spread = 0  # the amount of spread on the weapon
    machine = 0  # makes machinegun true so draw loop can make new shots
    speed = 11.0
    health = 1.0
    calib = 10.0  # size
    ready = True

    def __init__(self):
        self.x = width
        self.y = 360
        self.mx = 0
        self.my = 0
        self.disp = 1
        self.tx = 0
        self.ty = 0
        self.hp = projectile.health
        self.calib = projectile.calib
        self.alreadyHit = False
        projectile.objs.append(self)

    def calc(self, xOr=1280, yOr=360, tx=0, ty=0):
        global ammo
        if ammo > 0:
            if tx == 0 and ty == 0:
                self.tx = mouseX
                self.ty = mouseY + projectile.spread
            else:
                self.tx = tx
                self.ty = ty + projectile.spread
            self.x = xOr
            self.y = yOr
            self.mx = (xOr - self.tx) / \
                dist(xOr, yOr, self.tx, self.ty) * projectile.speed
            self.my = (yOr - self.ty) / \
                dist(xOr, yOr, self.tx, self.ty) * projectile.speed
            itemBuys[4] -= 1

    def kill(self):
        try:
            projectile.objs.remove(self)
        except:
            pass
        del self

    def display(self):
        rect(self.x, self.y, self.calib, self.calib)
        self.x -= self.mx
        self.y -= self.my
        if self.x <= 0 or self.hp <= 0:
            self.kill()
        if self.y+(self.calib/2.0) >= 654 or self.y <= 0:
            #self.my *= -1
            self.kill()

#-------------------------------------------------------------------------

class button():
    reg = []

    def __init__(self, x, y, w, h, col, type='txt', input='placeholder', fontSize=18, buttonShape='rect', textColor=color(0, 0, 0),textX=0,textY=0):
        self.x, self.y = x, y
        self.textX, self.textY = textX, textY
        self.pos = PVector(x, y)
        self.w, self.h, self.col = w, h, col
        self.type, self.input = type, input
        self.fontSize, self.textColor = fontSize, textColor
        self.buttonShape = buttonShape
        self.Hover, self.pressed = False, False                                                                 
        self.dtx = self.textX + self.x
        self.dty = self.textY + self.y
        self.inactive = False
        button.reg.append(self)

    def display(self):  
        textSize(self.fontSize)
        textAlign(CENTER)
        if self.buttonShape == 'rect':
            fill(self.col)
            rect(self.pos.x,self.pos.y,self.w,self.h)
            fill(self.col)
            rect(self.x, self.y, self.w, self.h)
            fill(self.textColor)
            text(self.input, self.dtx, self.dty)
            if self.inactive == True:
                fill(220, 220, 220, 95)
                rect(self.x, self.y, self.w, self.h)
            elif self.Hover == True and self.pressed == False:
                fill(220, 220, 220, 32)
                rect(self.x, self.y, self.w, self.h)
            elif self.pressed == True:
                fill(0, 0, 0, 27)
                rect(self.x, self.y, self.w, self.h)
        if self.inactive == True:
            self.x = self.pos.x
            self.y = self.pos.y
            self.dtx = self.textX + self.x
            self.dty = self.textY + self.y
            self.Hover = False
            self.pressed = False

    def update(self):
        if self.buttonShape == 'rect':
            if self.inactive == False:
                if(mouseX >= self.x - (self.w / 2.0) and mouseX <= self.x + (self.w / 2.0) and
                mouseY >= self.y - (self.h / 2.0) and mouseY <= self.y + (self.h / 2.0)):
                    self.x = self.pos.x - 1
                    self.y = self.pos.y - 1
                    self.dtx = self.textX + self.x - 1
                    self.dty = self.textY + self.y - 1
                    self.Hover = True
                    if mousePressed and mouseButton == LEFT:
                        self.x = self.pos.x + 1
                        self.y = self.pos.y + 1
                        self.dtx = self.textX + self.x + 1
                        self.dty = self.textY + self.y + 1
                        #self.pressed = True
                    else:
                        self.pressed = False
                else:
                    self.x = self.pos.x
                    self.y = self.pos.y
                    self.dtx = self.textX + self.x
                    self.dty = self.textY + self.y
                    self.Hover = False

#-------------------------------------------------------------------------

class shopItem():
    global mWheelOffset, itemBuys, money
    page = 1
    reg = []
    
    def __init__(self,number,page,itemI,price=0,txt='',fontSize=12):
        if number <= 4:
            self.column = number
            self.row = 0
        elif (number >= 5 and number <= 8):
            self.column = number - 4
            self.row = 1
        self.w = width/8
        self.h = height/4
        self.page = page
        self.price = price
        self.x = ((self.column+2)*(width/8))-(15-(6*self.column))-80
        self.y = -118 + (height/2) + ((8+height/4)*self.row)
        self.buyButton = button(self.x-25-13,self.y+63,74,47,color(0,255,100),input="Buy it!",textY=6,fontSize=20)
        self.item = itemI
        self.txt = txt
        self.fontSize = fontSize
        shopItem.reg.append(self)
        
    def display(self):
        global money
        if self.page == shopItem.page:
            fill(200)
            rect(self.x,self.y,self.w,self.h)
            fill(250)
            rect(self.x-(self.w/6.4),self.y-(self.h/6.4)+3,self.w/1.6,6+(self.h/1.6))
            fill(0)
            textSize(self.fontSize)
            text(self.txt,self.x-(self.w/6.4),self.y-(self.h/6.4)+3)
            self.buyButton.display()
            self.buyButton.update()
            if self.buyButton.Hover == True and mouseRel == True and money >= self.price:
                if itemBuys[self.item] == False:
                    itemBuys[self.item] = True
                    money -= self.price
                elif itemBuys[self.item] <= 0 or itemBuys[self.item] > 0:
                    if self.item == 4:
                        itemBuys[self.item] += 25
                    else:
                        itemBuys[self.item] += 1
                    money -= self.price
                    

#-------------------------------------------------------------------------

class turret():
    global time
    reg = []
    
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.reach = 1300
        self.type = 2
        self.shotTimer = time
        self.shotTimerReset = 0.1
        self.closestDist = 100000.0
        self.closestIndex = 0
        self.checkDist = 0
        self.tx = 10
        self.ty = 10
        self.prevtx = 0
        self.nearEnemies = []
        turret.reg.append(self)

    def display(self):
        strokeWeight(3)
        try:
            if len(self.nearEnemies) > 0:
                stroke(255,0,0,50)
                line(self.x,self.y,enemy.objs[self.closestIndex].x,enemy.objs[self.closestIndex].y)
        except:
            pass
        strokeWeight(1)
        stroke(0,0,0)
        fill(255)
        ellipse(self.x,self.y,30,30)
        noFill()
        ellipse(self.x,self.y,self.reach,self.reach)
        line(self.x,self.y,self.x,self.y+200)
        line(self.x,self.y,self.x,self.y-200)
        line(self.x+200,self.y,self.x,self.y)
        line(self.x-200,self.y,self.x,self.y)
        ellipse(self.x,self.y,self.reach*2,self.reach*2)
        
    def shootAt(self,tx1,ty1):
        if time >= self.shotTimer:
            projectile().calc(xOr=self.x,yOr=self.y,tx=tx1,ty=ty1)
            self.shotTimer += 0.3
            
    def closestEnemy(self):
        if enemy.onscreen != 0:
            self.nearEnemies = []
            for e in range(len(enemy.objs)):
                l = dist(self.x,self.y,enemy.objs[e].x,enemy.objs[e].y)
                if l <= self.reach:
                    self.nearEnemies.append([int(l),e])
            self.nearEnemies.sort()
            try:
                self.closestIndex = self.nearEnemies[0][1]
                line(self.x,self.y,enemy.objs[self.closestIndex].x,enemy.objs[self.closestIndex].y)
                line(self.x,self.y,enemy.objs[self.closestIndex].x+(dist(self.x,self.y,enemy.objs[self.closestIndex].x,enemy.objs[self.closestIndex].y)/80.0),enemy.objs[self.closestIndex].y)
                self.tx = enemy.objs[self.closestIndex].x+(dist(self.x,self.y,enemy.objs[self.closestIndex].x,enemy.objs[self.closestIndex].y)/73.0)+((abs(self.y-enemy.objs[self.closestIndex].y)*enemy.objs[self.closestIndex].xspeed)/15.0)
                line(self.x,self.y,self.tx,enemy.objs[self.closestIndex].y)
                self.ty = enemy.objs[self.closestIndex].y
                self.prevtx = enemy.objs[self.closestIndex].x
            except:
                self.tx = 0
                self.ty = 0
            if len(self.nearEnemies) > 0:
                self.shootAt(self.tx,self.ty)
            else:
                self.shotTimer = time

#-------------------------------------------------------------------------

def showScoreboard():
    global triscore, squarescore, cirscore, score, money, ammo, time
    fill(253)
    textMode(SHAPE)
    rect(width / 2, height / 2, width * 0.45, height * 0.45)
    translate((width/2) + 190,(height/2)+20)
    fill(0)
    textSize(30)
    text('Score', -330, -120)
    text('Other', -60, -120)
    textSize(16)
    text('Enemies Defeated:', -340, -50)
    text('Triangles Defeated:', -340, 0)
    text('Squares Defeated:', -340, 50)
    text('Circles Defeated:', -340, 100)
    text(score, -240, -50)
    text(triscore, -240, 0)
    text(squarescore, -240, 50)
    text(cirscore, -240, 100)
    text('Total Money:', -80, -50)
    text('$' + str(money), 0, -50)
    text('Ammo:', -89, 0)
    text(ammo, -22, 0)
    text(time,0,100)

#-------------------------------------------------------------------------

def showShop():
    global money, mWheelOffset, tim, openShop
    fill(253)
    rect(width/2,height/2,(width*0.5)+32,height*0.6)
    fill(140)
    rect(width/2,(height/2)-228,(width*0.5)+32,24)
    fill(0)
    textSize(16)
    text("The Game Shop",width/2,(height/2)-222)
    rectMode(CENTER)
    for item in shopItem.reg:
        item.display()
        
    for but in button.reg[6:9]:
        but.display()
        but.update()

    if button.reg[8].Hover == True and mouseRel == True:
        openShop = False

    if button.reg[7].Hover == True and mouseRel == True:
        shopItem.page += 1
    
    if button.reg[6].Hover == True and mouseRel == True:
        shopItem.page -= 1
    
#-------------------------------------------------------------------------

def defShop():
    button(28.5+width/4,8+(3*height/4),75,46,color(185,230,255),input='Previous',fontSize=16,textY=6)
    button((3*width/4)-28.5,8+(3*height/4),75,46,color(185,250,200),input='Next',fontSize=18,textY=6)
    button(960,132,18,18,color(255,100,100),input='X',fontSize=14,textY=5)
    shopItem(1,1,1,price=200,txt='Shotgun',fontSize=17)
    shopItem(2,1,4,price=1,txt='Normal Ammo')
    shopItem(3,1,2,price=500,txt='Machine Gun')

#-------------------------------------------------------------------------

def setup():
    global money, score, scoreboard, ammo, gamestart, inStart, health, openShop, itemBuys
    global triscore, squarescore, cirscore, highScores, inScore, timeStarted, spawnTimer
    global currWave, trispawn, squarespawn, cirspawn, gameStartTime, waveReady
    global nextWaveTimer, nWTStart, mouseRel, mWheelOffset, mWheelPos, time
    health, triscore, squarescore, cirscore = 0.5, 0, 0, 0
    scoreboard, score, money, ammo = 0, 0, 0, 1000
    gamestart, inStart, highScores, inScore = 0, 0, 0, 0
    spawnTimer, currWave, gameStartTime = 0.5,0,0
    trispawn, squarespawn, cirspawn, waveReady = 0, 0, 0, True
    nWTStart, nextWaveTimer, mouseRel, openShop = 0,0,False,False
    mWheelOffset, mWheelPos, time = 0,0,0
    #pistol, shotgun, machine gun then number of turrets
    itemBuys = [True,False,False,0,1000]
    size(1280, 720)
    rectMode(CENTER)
    projectile.weapon = 1
    button(100, 200, 100, 50, color(250, 120, 120))
    button(30, 60, 30, 40, color(255, 120, 120))
    button(640,687,60,60,color(255,120,120),input = 'Next \nWave', fontSize = 18, textY = -6)
    button(width/2.0,(height/2.0)+100,150,75,color(24, 234, 74), input = 'Start Game', fontSize = 26, textY = 8)
    button(width/2.0,(height/2.0)+157,100,30,color(245, 180, 90), input = 'Highscores', textY = 5)
    button(570,687,60,60,color(255,204,36),input='Store',textY=6.5)
    
    turret(500,360)
    
    timeStarted = millis()
    with open(os.path.join(directory,'waveFile.txt'),'r') as waveFile:
        global waveFC
        waveFC = waveFile.read()
    waveFC = waveFC.split('\n')
    for index in range(len(waveFC)):
        waveFC[index] = waveFC[index].split(',')
    print(waveFC)
    for j in range(len(waveFC)):
        waveFC[j] = [int(i) for i in waveFC[j]]
    print(waveFC)
    enemy.waveCount = waveFC[currWave][0]
    defShop()

#-------------------------------------------------------------------------

def draw():
    global money, score, scoreboard, gamestart, inStart, health, directory, openShop
    global highScores, inScore, timeStarted, time, spawnTimer, waveFC, waveReady, bg
    global currWave, trispawn, squarespawn, cirspawn, nextWaveTimer, nWTStart, mouseRel
    global mWheelOffset, mWheelPos, itemBuys, ammo
    
    print(frameRate)

    background(204)
    ammo = itemBuys[4]
    
    time = (millis() - timeStarted) / 1000.0

    for turr in turret.reg:
        turr.closestEnemy()
        turr.display()
        
    if button.reg[3].Hover == True and mouseRel == True and gamestart == 0:
        gamestart = 1
    
    if button.reg[4].Hover == True and mouseRel == True and highScores == 0:
        highScores = 1
    
    if time >= spawnTimer and enemy.waveUsed < enemy.waveCount and gamestart == 1 and waveReady == True:
        randnum = randint(1,waveFC[currWave][0])
        if randnum <= waveFC[currWave][2] and cirspawn < waveFC[currWave][2]:
            enemy(2, randint(1, 10))
            cirspawn += 1
        elif randnum > waveFC[currWave][2] and randnum <= waveFC[currWave][1] and squarespawn < waveFC[currWave][1]:
            enemy(1, randint(1, 10))
            squarespawn += 1
        elif randnum > waveFC[currWave][3] and trispawn < waveFC[currWave][3]:
            enemy(3, randint(1, 10))
            trispawn += 1
        spawnTimer += 0.5
        
    if enemy.waveUsed >= enemy.waveCount and enemy.onscreen == 0:
        if currWave == len(waveFC):
            with open(os.path.join(directory, 'highscores.txt'), 'a+') as hsFile:
                hsFile.write('\n' + str(score) + '  |  ' + str(datetime.datetime.now()))
            exit()
        currWave += 1
        waveReady = False
        enemy.waveUsed = 0
        try:
            enemy.waveCount = waveFC[currWave][0]
        except:
            exit()
        squarespawn = 0
        cirspawn = 0
        trispawn = 0
        spawnTimer = 99999

    if button.reg[2].Hover == True and mouseRel == True and waveReady == False and spawnTimer == 99999:
        waveReady = True
        spawnTimer = time + 0.5
        
    if button.reg[5].Hover == True and mouseRel == True:
        openShop = True
    
    if waveReady == True:
        button.reg[2].inactive = True
        #button.reg[5].inactive = True
    else:
        button.reg[2].inactive = False
        #button.reg[5].inactive = False
    
#-------------------------------------------------------------------------
    
    if gamestart == 0 and highScores == 0:   
        textAlign(CENTER)     
        button.reg[3].display()
        button.reg[3].update()
        button.reg[4].display()
        button.reg[4].update()
        
#-------------------------------------------------------------------------
        
    elif gamestart == 0 and highScores == 1:
        button.reg[1].display()
        print(str(button.reg[1].update()))
        translate(width / 2, height / 2)
        fill(240)
        rect(0, 0, width * 0.85, height * 0.85)
        translate(-width / 2, -height / 2)
        button.reg[0].display()
        button.reg[0].update()
        
        if button.reg[1].Hover == True and mouseRel == True and highScores == 1:
            highScores = 0
    
#-------------------------------------------------------------------------
        
    elif gamestart == 1 and highScores == 0:
        rectMode(CORNER)
        fill(120)
        rect(0,654,width,66)
        
        rectMode(CENTER)
        button.reg[2].display()
        button.reg[2].update() 
        button.reg[5].display()
        button.reg[5].update()
        
        if openShop == True:
            showShop()
        
        # for the shot projectile
        fill(0)
        for obj in projectile.objs:
            obj.display()

        # for the wave display and movement
        for obj in enemy.objs:
            obj.update()
            obj.display()

        # all the healthbar, first green then red
        fill(35, 250, 72)
        rectMode(CORNER)
        rect(0, 0, 2 * health * width, 10)
        fill(255, 0, 0)
        rect(2 * width * health, 0, width - (2 * width * health), 10)

        # this is the end statement for if health is less than 0
        if health <= 0:
            print(score)
            with open(os.path.join(directory, 'highscores.txt'), 'a+') as hsFile:
                hsFile.write('\n' + str(score) + '  |  ' + str(datetime.datetime.now()))
        
        # this is for the turret at the back
        rectMode(CENTER)
        fill(255)
        translate(width, height / 2)
        rotate(atan(((height / 2) - mouseY) / (width - mouseX + 0.0001)))
        rect(0, 0, 75, 75)
        rotate(-1 * atan(((height / 2) - mouseY) / (width - mouseX + 0.0001)))
        translate(-width, -height / 2)

        if scoreboard == True:
            showScoreboard()

        # this is the new hitreg code
        for shot in projectile.objs:
            for enmy in enemy.objs:
                if dist(shot.x, shot.y, enmy.x, enmy.y) <= ((1.75 * shot.calib / 2.0) + enemy.siz / 2.0):
                    if shot.alreadyHit == False:
                        shot.alreadyHit = True
                        shothp = shot.hp
                        shot.hp -= abs(obj.hp)
                        enmy.hp -= abs(shothp)
                        if enmy.hp <= 0:
                            enmy.kill()
                            enmy.score()

        # machine gun code
        if projectile.weapon == 3 and projectile.machine == 1:
            projectile.spread = random(-45, 45)
            if projectile.ready == True:
                projectile().calc()
                projectile.ready = False
            else:
                projectile.ready = True
            
    mouseRel = False
#-------------------------------------------------------------------------

def mousePressed():
    global waveReady, openShop
    if waveReady == True:
        if projectile.weapon == 1 and openShop == False:
            projectile.spread = 0
            projectile().calc()
        elif projectile.weapon == 2  and openShop == False:
            for i in range(8):
                projectile.spread = random(-125, 125)
                projectile().calc()
        elif projectile.weapon == 3  and openShop == False:
            projectile.machine = 1

#-------------------------------------------------------------------------

def mouseReleased():
    global mouseRel
    if mouseButton == LEFT:
        mouseRel = True
    if projectile.weapon == 3:
        projectile.machine = 0

#-------------------------------------------------------------------------

def keyPressed():
    global scoreboard, openShop, itemBuys
    if key == "1" and itemBuys[0] == True:
        projectile.weapon = 1
        projectile.speed = 20.0
        projectile.health = 4
    if key == "2" and itemBuys[1] == True:
        projectile.weapon = 2
        projectile.speed = 9.0
        projectile.health = 5
    if key == "3" and itemBuys[2] == True:
        projectile.weapon = 3
        projectile.speed = 11.0
        projectile.health = 1
    if keyCode == 9:
        scoreboard = True
    if key == 'q':
        frameRate(1)
    if key == 'e':
        frameRate(60)

#-------------------------------------------------------------------------

def keyReleased():
    global scoreboard
    if keyCode == 9:
        scoreboard = False

#-------------------------------------------------------------------------

def mouseClicked():
    global inStart, gamestart, highScores, inScore, spawnTimer, time
    if inStart == 1:
        gamestart = 1
        spawnTimer = 0.5+time
    if inScore == 1:
        highScores = 1
        
#-------------------------------------------------------------------------
        
def mouseWheel(event):
    global mWheelPos
    e = event.getCount()
    mWheelPos += 15*e
    