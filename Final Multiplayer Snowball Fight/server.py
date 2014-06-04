from network import Listener, Handler, poll
from time import sleep
from random import randint


users = {}  # map client handler to user name
scoreboard={}
killscore=15
deathscore=50
snowballs =[]
SCREENWIDTH,SCREENHEIGHT = 1200, 800
playerspeed=5
playerheight=40
playerwidth=30

#snowballlife/playerthrowcooldown=1 snowball per person
playerthrowcooldown=30
snowballlife=30

snowballspeed=10
snowballsize=10

deathstuntime=50

def update():
    for i,snowball in reversed(list(enumerate(snowballs))):
        snowball[3]-=1
        if snowball[3]<=0:
            snowballs.pop(i)
        else:
            if snowball[2]:
                snowball[0]+=snowballspeed
            else:
                snowball[0]-=snowballspeed
    for username,user in users.iteritems():
        userx,usery,going_right,deathtimer=user[1]
        if deathtimer==0:
            if user[2][0]==1:
                usery-=playerspeed
            if user[2][1]==1:
                usery+=playerspeed
            if user[2][2]==1:
                userx-=playerspeed
                going_right=False
            if user[2][3]==1:
                userx+=playerspeed
                going_right=True
                
            if userx<0:
                userx=0
            elif userx+playerwidth>SCREENWIDTH:
                userx=SCREENWIDTH-playerwidth
    
            if usery<0:
                usery=0
            elif usery+playerheight>SCREENHEIGHT:
                usery=SCREENHEIGHT-playerheight
        if user[3]>0:
            user[3]-=1
        if deathtimer==1:
            deathtimer=0
            userx=randint(0,SCREENWIDTH-playerwidth)
            usery=randint(0,SCREENHEIGHT-playerheight)
        elif deathtimer>0:
            deathtimer-=1
        else:
            hit=[]
            for snowball in snowballs:
                if userx<snowball[0]+snowballsize and userx+playerwidth>snowball[0]\
                            and usery<snowball[1]+snowballsize and usery+playerheight>snowball[1]:
                    hit+=[snowball[4]]
            if len(hit)>0:
                scoreboard[username]=scoreboard[username]-deathscore if scoreboard[username]>deathscore else 0
                deathtimer=deathstuntime
                for username2 in hit:
                    scoreboard[username2]+=killscore/len(hit)
        user[1]=(userx,usery,going_right,deathtimer)
def send_data():
    userstosend=[]
    for user in users.itervalues():
        userstosend+=[user[1]]
    for i,user in enumerate(users.itervalues()):
        user[0].do_send(("positions:",i,userstosend,len(users),snowballs,scoreboard))

class MyHandler(Handler):
    
    def on_open(self):
        print "open"
        
    def on_close(self):
        for username in users.iterkeys():
            if users[username][0] is self:
                users.pop(username)
                break
        print "close"
    def on_msg(self, msg):
        print "recieving:",msg
        if 'join' in msg:
            if msg['join'] in users:
                self.do_send(("username taken",0))
                self.do_close()
            else:
                #handler,playerdata,buttons depressed,snowball cooldown,deathtimer
                #playerdata=(x,y,facing right,deathtime)
                users[msg['join']]=[self,(randint(0,SCREENWIDTH-playerwidth),randint(0,SCREENHEIGHT-playerheight),True,0),[0,0,0,0],0]
                scoreboard[msg['join']]=0
                for user in users.itervalues():
                    user[0].do_send(("userjoin",len(users)))
        if 'speak' in msg:
            if msg['txt'] == 'quit':
                for user in users.itervalues():
                    if user is not self:
                        user[0].do_send(("userleave",len(users)))
            else:
                user=users[msg['speak']]
                if msg['txt'].startswith("No"):
                    if msg['txt'].endswith("Up"):
                        user[2][0]=0
                    elif msg['txt'].endswith("Down"):
                        user[2][1]=0
                    elif msg['txt'].endswith("Left"):
                        user[2][2]=0
                    elif msg['txt'].endswith("Right"):
                        user[2][3]=0
                elif msg['txt']=="Spacebar":
                    if user[3]==0:
                        user[3]=playerthrowcooldown
                        if user[1][2]:
                            snowballs.append([user[1][0]+playerwidth,user[1][1],user[1][2],snowballlife,msg['speak']])
                        else:
                            snowballs.append([user[1][0]-snowballsize,user[1][1],user[1][2],snowballlife,msg['speak']])
                else:
                    if msg['txt']==("Up"):
                        user[2][0]=1
                    elif msg['txt']==("Down"):
                        user[2][1]=1
                    elif msg['txt']==("Left"):
                        user[2][2]=1
                    elif msg['txt']==("Right"):
                        user[2][3]=1

    
class Serv(Listener):
    def on_accept(self,h):
        pass


port = 8888
server = Serv(port,MyHandler)
try:
    while 1:
        poll()
        update()
        send_data()
        print scoreboard
        sleep(.04)  # seconds
except KeyboardInterrupt:
    print users
    for user in users.values():
        user[0].do_close()
    print "closed all users"
    raise