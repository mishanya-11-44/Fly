from random import *
from tkinter import *
from winsound import *
def stop():
    canvas.after(5000,exit)
def update_text():
    global text2_id,text3_id,j
    j += 1
    canvas.itemconfig(text2_id,fill=c[j+1])
    canvas.itemconfig(text3_id,fill=c[j+1])
    canvas.after(350, update_text)
    if j>=len(c):
        stop()
def game_over():
    global gameover
    update_text()
    canvas.itemconfig(kom_id,state='hidden')
    canvas.itemconfig(npc_id, state='hidden')
    canvas.itemconfig(text_id, state='hidden')
    canvas.itemconfig(taimer_id, state='hidden')
    canvas.itemconfig(hit2_id, state='hidden')
    canvas.itemconfig(hit1_id, state='hidden')
    canvas.itemconfig(kom2_id, state='normal')
    canvas.itemconfig(text2_id, state='normal')
    canvas.itemconfig(text3_id, state='normal')
    gameover=True
def update_time():
    global time
    time-=1
    canvas.itemconfig(taimer_id, text=f'Таймер: {time} секунд')
    canvas.after(1000,update_time)
    if time<0:
        game_over()
def update_points():
    canvas.itemconfig(text_id,text=f'Очки: {score}')
    canvas.itemconfig(text3_id, text=f'Вы убили {score} мух')
def hit():
    global score
    score+=1
    update_points()
def collision_detection(x,y):
    position = canvas.coords(npc_id)
    left = position[0]
    top = position[1]
    right = position[0] + npc_width
    bottom = position[1] + npc_height
    return left <= x <= right and top <= y < +bottom
def anime_frames(frame=0):
    canvas.itemconfig(npc_id,image=photos[frame],anchor='nw')
    canvas.after(50,anime_frames,(frame+1)%len(photos))
def mouse_click_down(e):
    canvas.itemconfig(hit1_id,state='hidden')
    canvas.itemconfig(hit2_id, state='normal')
    if collision_detection(mouse_x-25,mouse_y-25):
        hit()
def mouse_click_up(e):
    canvas.itemconfig(hit2_id, state='hidden')
    canvas.itemconfig(hit1_id, state='normal')
def mouse_motion(event):
    global mouse_x,mouse_y,hit1_id
    mouse_x,mouse_y=event.x,event.y
    canvas.moveto(hit1_id,mouse_x-70,mouse_y-115)
    canvas.moveto(hit2_id, mouse_x, mouse_y)
def game_update():
    spawn()
    canvas.after(1000,game_update)
def spawn():
    global mux_vx,mux_vy
    x=randint(1,game_width-npc_width)
    y=randint(1,game_height-npc_height)
    if abs(mouse_x-x)>200 or abs(mouse_y-y)>200:
        x = randint(x,game_width-npc_width)
        y = randint(y,game_height-npc_height)
    canvas.moveto(npc_id,x,y)
    k1=choice(koef)
    k2=choice(koef)
    mux_vx,mux_vy=randint(1,5)*k1,randint(1,5)*k2
def move_to():
    global mux_vx,mux_vy
    # canvas.move(npc_id,mux_vx,mux_vy)
    # canvas.after(10,move_to)
    x=canvas.coords(npc_id)[0]+mux_vx
    y = canvas.coords(npc_id)[1] + mux_vy
    if x<0:
        x=0
        mux_vx=-mux_vx
    if x>game_height-npc_width:
        x=game_width-npc_width
        mux_vx=-mux_vx
    if y<0:
        y=0
        mux_vy=-mux_vy
    if y>game_height-npc_height:
        y=game_height-npc_height
        mux_vy=-mux_vy
    canvas.moveto(npc_id,x,y)
    canvas.after(10,move_to)
j=0
c=['','','azure','azure1','azure2','azure3','dark grey','azure4','black']
koef=[-1,1]
mux_vx=3
mux_vy=5
mouse_x=mouse_y=0
game_width=720
game_height=720
npc_width=100
npc_height=100
score=0
time=20
gameover=False
window=Tk()
window.title('Мухобойка')
window.resizable(False, False)
canvas=Canvas(window,width=game_width,height=game_height)
kom_image=PhotoImage(file='комната.png')
kom_id=canvas.create_image(0,0,image=kom_image,anchor=NW)
photos=[PhotoImage(file=f'муха{i}.png') for i in range(1,3)]
kom2_id=canvas.create_rectangle(0,0,720,720,fill='white')
canvas.itemconfig(kom2_id,state='hidden')
npc_id=canvas.create_image(0,0,image=photos[0],anchor=NW)
hit1_image=PhotoImage(file='мухобойка1.png')
hit1_id=canvas.create_image(mouse_x,mouse_y,image=hit1_image,anchor=CENTER)
hit2_image=PhotoImage(file='мухобойка2.png')
hit2_id=canvas.create_image(mouse_x,mouse_y,image=hit2_image,anchor=CENTER)
canvas.itemconfig(hit2_id,state='hidden')
text_id=canvas.create_text(game_width-10,10,
                           text=f'Очки: {score}',
                           font='Times 20 bold',
                           fill='black',
                           anchor=NE)
taimer_id=canvas.create_text(10,10,
                           text=f'Таймер: {time} секунд',
                           font='Times 20 bold',
                           fill='black',
                           anchor=NW)
text2_id=canvas.create_text(game_width/2,game_height/2-40,
                           text=f'Игра окончена',
                           font='Times 35 bold',
                           fill='black',
                           anchor=CENTER)
canvas.itemconfig(text2_id,state='hidden')
text3_id=canvas.create_text(game_width/2,game_height/2,
                           text=f'Вы убили {score} мух',
                           font='Times 35 bold',
                           fill='black',
                           anchor=CENTER)
canvas.itemconfig(text3_id,state='hidden')
canvas.bind("<ButtonPress>", mouse_click_down)
canvas.bind("<ButtonRelease>", mouse_click_up)
canvas.bind('<Motion>',mouse_motion)
update_time()
canvas.pack()
move_to()
anime_frames()
game_update()
window.mainloop()