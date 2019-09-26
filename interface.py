# -*- coding: utf-8 -*-

import pygame
import pygame.locals as ev
import sys

import transformjson

#############################################

#定数

#画面の大きさ
width=int(640*1.2)
height=int(480*1.2)


#マップの情報
Empty=0
Enemy=1
Ally=2
EnemyColor=(255,84,0)
AllyColor=(0,84,255)

#プレイヤーの動き
stay=0
Move=1
Remove=2

#############################################

#エージェント情報
class Agent():
    x=0
    y=0
    agentId=0
    teamId=0
    
    def __init__(self,_x,_y,agentId,teamId):
        self.x=_x
        self.y=_y
        self.agentId=agentId
        self.teamId=teamId
    
    def isEnemy(self):
        if self.teamId==Enemy:
            return True
        else:
            return False
        
    def isAlly(self):
        return not self.isEnemy()
###############################################

#フィールド情報
class Grid():
    grid=[]
    area=[]
    x=0
    y=0

    def __init__(self,jsonContent):
        self.grid=jsonContent['points']
        self.tiled=jsonContent['tiled']
         #x,yサイズ
        self.y=len(self.grid)
        if self.y !=0:
            self.x=len(self.grid[0])
    
        #領域情報の確保
        self.area=[[Empty for i in range(self.x)]for j in range(self.y)]
        
        print("x={0},y={1}".format(self.x,self.y))
    
    def outGrid(self,xy):
        x=xy[0]
        y=xy[1]
        if x>=0 and x<self.x and y>=0 and y<self.y:
            return False
        else:
            return True
        
    def inArea(self,xy,teamId):
        x=xy[0]
        y=xy[1]
        if not self.outGrid(xy):
            self.area[y][x]=teamId
        
    
    def draw(self,screen,font,agent):
        #四角の幅
        w=min([(height/self.y),(width/self.x)])
        wx=w*(self.x)
        wy=w*(self.y)
        
        for y in range(self.y):
            for x in range(self.x):
                #領域の描画
                if self.tiled[y][x]==Enemy:
                    pygame.draw.rect(screen,EnemyColor,(x*w,y*w,w,w))
                elif self.tiled[y][x]==Ally:
                    pygame.draw.rect(screen,AllyColor,(x*w,y*w,w,w))
                
                #マスの点数を描画
                text=font.render("{0}".format(self.grid[y][x]),False,(255,255,255))
                screen.blit(text,[x*w+1,y*w+1])
         
        #agentの表示
        for p in agent:
            pygame.draw.circle(screen,(255,255,0),(int(p.x*w+w/2),int(p.y*w+w/2)),int(w*2/6))
        
        #線の描画
        for i in range(self.x+1):
            pygame.draw.line(screen,(255,0,0),(i*w,0),(i*w,wy)) 
        for i in range(self.y+1):
            pygame.draw.line(screen,(255,0,0),(0,i*w),(wx,i*w))
    
#######################################################################
        
#ゲームクラス
class Game():
    grid=None
    agent=[]
    
    def __init__(self):
        #subGrid=[[0 for i in range(10)] for j in range(10)]
        jsonContent=transformjson.r_transform("F-2.json")
        teams = jsonContent['teams']
        team1 = teams[0]
        team2 = teams[1]
        agents1 = team1['agents']
        agents2 = team2['agents']
        self.grid=Grid(jsonContent)
        for i in range(len(agents1)):
            agentsi = agents1[i]
            agentID = agentsi['agentID']
            x = agentsi['x']
            y = agentsi['y']
            self.agent.append(Agent(x-1,y-1,agentID,1))
        for i in range(len(agents2)):
            agentsi = agents2[i]
            agentID = agentsi['agentID']
            x = agentsi['x']
            y = agentsi['y']
            self.agent.append(Agent(x-1,y-1,agentID,2))
        #
        for p in self.agent:
            self.grid.inArea((p.x,p.y),p.teamId)
    
    def draw(self,screen,font):
        self.grid.draw(screen,font,self.agent)
    
    #一人の動きしか考慮してないので注意
    def onemove(self,pnum,mnum,vxvy):
        vx=vxvy[1]
        vy=vxvy[0]
        x=self.agent[pnum].x+vx
        y=self.agent[pnum].y+vy
        if not self.grid.outGrid([x,y]):
            if mnum==Move:
                self.agent[pnum].x=x
                self.agent[pnum].y=y
                self.grid.inArea([x,y],self.agent[pnum].teamId)
            elif mnum==Remove:
                self.grid.inArea([x,y],Empty)
        
######################################################
    
#メイン
def main():
    pygame.init()
    screen=pygame.display.set_mode((width,height),pygame.RESIZABLE)
    pygame.display.set_caption("procon2019")
    
    font=pygame.font.Font(None,25)
    
    game=Game()
    
    while True:
        screen.fill((0,0,0))
        
        game.draw(screen,font)
        
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type==ev.QUIT:
                pygame.quit()
                sys.exit(0)
            if event.type==ev.KEYDOWN:
                if event.key==ev.K_ESCAPE:
                    pygame.quit()
                    return
                elif event.key==ev.K_x:
                    game.onemove(0,Move,[1,1])
                
if __name__=="__main__":
    main()
    