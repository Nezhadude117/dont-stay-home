print("STARTED")
import random, time, asyncio
from pygame import FULLSCREEN,font,display,mixer,image,surface,key,time,Rect,Surface,event,QUIT,KEYUP,MOUSEMOTION,MOUSEBUTTONDOWN,MOUSEBUTTONUP,mouse,SRCALPHA,transform,draw,K_c,K_m,K_d,K_SPACE,K_c,K_l,K_r,K_ESCAPE,K_UNDERSCORE

font.init()
display.init()
mixer.init()
music = mixer.Channel(0)
musicsfx = mixer.Sound("music.ogg")
music.set_volume(0.1)

#creating variables

width,height = (1000,700)
if False:
    window = display.set_mode((width,height))
else:
    window = display.set_mode((width,height),FULLSCREEN)
display.set_caption("dont stay home")
clock = time.Clock()

def imload(name):
    imgdir = ""
    try:
        resul = image.load(imgdir+name).convert_alpha()
    except:
        resul = image.load(imgdir+name+".png").convert_alpha()
    return resul

title = imload("TITLE.png")
pointer = imload("pointer.png")
desk = imload("desk.png")
desk_door = imload("desk-door.png")
door_none = imload("door_none.png")
desk_box = imload("desk-box.png")
box_closed = imload("box_closed.png")
box_open_up = imload("box_open_up.png")
box_open_down = imload("box_open_down.png")
flash = imload("flash.png")
rob1jump = imload("rob1_jumpscare")
sun = imload("sun.png")
sky = imload("sky.png")
silo = imload("silo.png")

hide_frames = [imload("hide1.png"),imload("hide2.png"),imload("hide3.png")]
hide_final = imload("hide.png")

cams = [[imload("A1_none.png"),imload("A2.png"),imload("A3_none.png")],[imload("B1_none.png"),imload("B2_none.png"),imload("B3_none.png")],[imload("O1_none.png"),imload("O2_none.png"),imload("O3_none.png")]]

static1 = [imload("s1"),imload("s2"),imload("s3"),imload("s4"),imload("s5")]
static2 = [imload("c1"),imload("c2"),imload("c3"),imload("c4")]

hacked = [imload("hacked"),imload("hacked-c"),imload("hacked-cm"),imload("hacked-cmd"),imload("hacked-cmd_"),imload("hacked-cmd_c"),imload("hacked-cmd_cl"),imload("hacked-cmd_clr")]

robber1_poses = [imload("robber1_living.png"),imload("robber1_dining.png"),imload("robber1_stair.png"),imload("robber1_bed.png"),imload("robber1_game.png"),imload("robber1_door.png")]

robber2_img = imload("rope_climb.png")

rob2_rope = imload("rope.png")

robber3_img = imload("rob3.png")


floor1 = imload("floor1.png")
floor2 = imload("floor2.png")
floor3 = imload("Floor3.png")

F1 = imload("F1.png")
F2 = imload("F2.png")
O = imload("O.png")

powerch = mixer.Channel(1)
breath = mixer.Channel(2)
screaming = mixer.Channel(3)
steping = mixer.Channel(4)
staticsfc = mixer.Channel(5)
camswitchch = mixer.Channel(7)
camswitchsfx = mixer.Sound("cam_switch.ogg")
staticsfx = mixer.Sound("static.ogg")
flashsfx = mixer.Sound("flash.ogg")
knock = mixer.Sound("knock.ogg")
scream = mixer.Sound("scream.ogg")
breathing = mixer.Sound("breath.ogg")
steps = mixer.Sound("run.ogg")
glass = mixer.Sound("break.ogg")
power_down = mixer.Sound("power_down.ogg")

mouserect = Rect(0,0,10,10)
mouse_down = False
door_pointer = pointer.get_rect()
door_pointer.center = (width-pointer.get_size()[0]//2,height//2)

done = False
mouseymove = 0
mousexmove = 0

power_font = font.SysFont('roboto', width//10)
time_font = font.SysFont('roboto', width//17)

poses = {
    0: desk,
    0.5: desk_door,
    1: door_none,
    1.5: desk_box,
    2: box_open_up,
    2.5: box_open_down,
    3.1: hide_frames[0],
    3.2: hide_frames[1],
    3.3: hide_frames[2],
    3: hide_final
}

do_title = True
fade = 50


robber1_pose = "kitchen"
robber1_lastmove = 0

robber2_climbing = ""
robber2_pose = 0
robber2_status = 0
robber2_lastmove = 0

flashed = False

robber3_status = False
robber3_lastmove = 0

robber4_status = False
robber4_lastmove = 0
robber4_progress = 0

power = 100
power_text = power_font.render(str(power),True,(0,0,0))

power_done = False

move_1 = False
move_2 = False
move_3 = False
move_4 = False

office_pose = 0
old = 0


hiding = 0
hide = False

box_open = False

time_s = 0
time_h = 0

dark = Surface((width,height))
dark.fill(0)
dark.set_alpha(150)


def genimg(img,x,y,xsize,ysize,rotation=0):
    img = transform.rotate(img,(rotation))
    img = transform.scale(img,(xsize,ysize))
    rect = img.get_rect()
    rect.center = (x,y)
    return [img,rect]

def genstatic(wind,sta1al,sta2al):
    subwidth = wind.get_width()
    subheight = wind.get_height()
    staticsf = surface.Surface((subwidth,subheight),SRCALPHA)
    staticch = genimg(random.choice(static1),subwidth//2,subheight//2,subwidth,subheight)
    staticsf.blit(staticch[0],staticch[1])
    staticsf.set_alpha(sta1al)
    wind.blit(staticsf,(0,0))
    staticsf = surface.Surface((subwidth,subheight),SRCALPHA)
    staticch = genimg(random.choice(static2),subwidth//2,subheight//2,subwidth,subheight)
    staticsf.blit(staticch[0],staticch[1])
    staticsf.set_alpha(sta2al)
    wind.blit(staticsf,(0,0))

camnumf1 = 0
camnumf2 = 0
camnumf3 = 0
floornum = 1

def rob3move(reset=False):
    global robber3_status, robber3_lastmove,power
    if reset:
        robber3_status = False
        robber3_lastmove = 0

    if robber3_status:
        if power > 0:
            power -= 0.02

    chance = 0
    try: chance = 2000//time_h
    except: chance = 2000
    if random.randint(200,chance) < robber3_lastmove:
        robber3_status = True
    else: robber3_lastmove += 1

def rob4move():
    global robber4_status, robber4_lastmove
    chance = 0
    try: chance = 4000//time_h
    except: chance = 2000
    if random.randint(200,chance) < robber4_lastmove:
        robber4_status = True
    else: robber4_lastmove += 1

def rendcams(x, y, xsize, ysize, controls):
    try:
        global floornum, camnumf1, camnumf2, camnumf3, robber4_status, robber4_progress,robber4_lastmove
        subwindow = window.subsurface((x, y), (xsize, ysize))
        subwidth, subheight = subwindow.get_width(), subwindow.get_height()
        subwindow.fill(0)

        if robber4_status:
            hack = genimg(hacked[robber4_progress],subwidth//2,subheight//2,subwidth,subheight)
            subwindow.blit(hack[0],hack[1])
            if robber4_progress == 7:
                robber4_status = False
                robber4_progress = 0
                robber4_lastmove = 0
            else:
                keys = key.get_pressed()
                prog = [K_c,K_m,K_d,K_SPACE,K_c,K_l,K_r]
                if keys[prog[robber4_progress]]:
                    robber4_progress += 1
        else:

            # Get the correct camera for the current floor
            cameras = [camnumf1, camnumf2, camnumf3]
            camera = cams[floornum - 1][cameras[floornum - 1]]

            # Render the camera image
            mg = genimg(camera, subwidth // 2, subheight // 2, subwidth, subheight)
            subwindow.blit(mg[0], mg[1])
            fourth = subwidth//4
            # Robber images
            robber_poses = {
                (1, 0, "dining"): robber1_poses[1],
                (1, 2, "living"): robber1_poses[0],
                (2, 0, "bedroom"): robber1_poses[3],
                (2, 1, "gameroom"): robber1_poses[4],
                (2, 2, "stair"): robber1_poses[2],

                (3, 0, True): robber3_img,
                (3, 0, False): None,

                (3, 0, "O1"): robber2_img,
                (3, 1, "O2"): robber2_img,
                (3, 1, "O3"): robber2_img,
                (3, 2, "O4"): robber2_img,
                (3, 2, "O5"): robber2_img
            }

            heights = {
                (1): subheight*0.9,
                (2): subheight*0.8,
                (3): subheight*0.6,
                (4): subheight*0.5,
            }

            xs = {
                ("O1"): fourth*2,
                ("O2"): fourth//3.7,
                ("O3"): fourth*3.014,
                ("O4"): fourth//1.36,
                ("O5"): fourth*3.48 ,
            }

            rob_image = robber_poses.get((floornum, cameras[floornum - 1], robber1_pose))
            if rob_image:
                rob = genimg(rob_image, subwidth // 2, subheight // 2, subwidth, subheight)
                subwindow.blit(rob[0], rob[1])

            rob_image = robber_poses.get((floornum, cameras[floornum - 1], robber3_status))
            if rob_image and robber3_status:
                rob = genimg(rob_image, subwidth // 2, subheight // 2, subwidth, subheight)
                subwindow.blit(rob[0], rob[1])

            rob_image = robber_poses.get((floornum, cameras[floornum - 1], robber2_climbing))
            if rob_image:
                rope = genimg(rob2_rope,xs.get((robber2_climbing),0), subheight / 2, subwidth, subheight)
                if not robber2_status > 5:
                    rob = genimg(rob_image, xs.get((robber2_climbing),0), heights.get((robber2_status),0), subwidth, subheight)
                subwindow.blit(rope[0],rope[1])
                if not robber2_status == 5:
                    subwindow.blit(rob[0], rob[1])

            # Control buttons and floor switch
            if controls:
                controls_img = [(F1, 0.97, 0.9), (F2, 0.97, 0.8), (O, 0.97, 0.7)]
                for img, wx, wy in controls_img:
                    ctrl_img = genimg(img, subwidth * wx, subheight * wy, subwidth * 0.08, subheight * 0.08)
                    subwindow.blit(ctrl_img[0], ctrl_img[1])
                    if mouserect.colliderect(ctrl_img[1]) and mouse_down and floornum != controls_img.index((img, wx, wy)) + 1:
                        camswitchch.play(camswitchsfx)
                        floornum = controls_img.index((img, wx, wy)) + 1

                floor_imgs = [floor1, floor2, floor3]
                mg = genimg(floor_imgs[floornum - 1], subwidth * 0.75, subheight * 0.8, subwidth * 0.3, subheight * 0.3)
                subwindow.blit(mg[0], mg[1])

                # Camera switching areas
                camera_areas = {
                    1: [(0.85, 0.8), (0.625, 0.835), (0.625, 0.71)],
                    2: [(0.857, 0.737), (0.7, 0.91), (0.623, 0.778)],
                    3: [(0.590, 0.802), (0.78, 0.652), (0.879, 0.802)]
                }

                for idx, (wx, wy) in enumerate(camera_areas[floornum]):
                    rect = Rect(width * wx, height * wy, width * 0.025, height * 0.025)
                    if mouserect.colliderect(rect) and mouse_down:
                        # Only play the sound if switching to a new camera
                        if floornum == 1 and camnumf1 != idx:
                            camswitchch.play(camswitchsfx)
                            camnumf1 = idx
                        elif floornum == 2 and camnumf2 != idx:
                            camswitchch.play(camswitchsfx)
                            camnumf2 = idx
                        elif floornum == 3 and camnumf3 != idx:
                            camswitchch.play(camswitchsfx)
                            camnumf3 = idx


        genstatic(subwindow,10,50)
        draw.rect(subwindow,(0,0,0),(0,0,subwidth,subheight),subwidth//200)
    except: pass




async def main():
    global window, done, mouserect, mousexmove, mouseymove, mouse_down
    global clock, do_title, robber1_pose, robber1_lastmove
    global robber2_climbing, robber2_pose, robber2_status, robber2_lastmove
    global flashed, robber3_status, robber3_lastmove, robber4_status, robber4_lastmove, robber4_progress
    global power, power_text, power_done, move_1, move_2, move_3, move_4
    global office_pose, old, hiding, hide, box_open, time_s, time_h
    global staticsfc, staticsfx, breath, breathing, floornum, camnumf1, camnumf3
    global power_font, time_font, next_pos, fade, poses, pointer, robber1_poses
    global power_down, background, lever, width, height

    while not done:
        clock.tick(20)
        window.fill(0)
        for events in event.get():
            if events.type == QUIT:
                exit(0)
            elif events.type == KEYUP:
                if events.key == K_ESCAPE:
                    exit(0)
            elif events.type == MOUSEMOTION:
                mouserect.center = mouse.get_pos()
                mousexmove,mouseymove = mouse.get_rel()
                if mouseymove < 0:
                    mouseymove = 1
                elif mouseymove > 0:
                    mouseymove = -1
                else: mouseymove = 0
                if mousexmove < 0:
                    mousexmove = -1
                elif mousexmove > 0:
                    mousexmove = 1
                else: mousexmove = 0
            elif events.type == MOUSEBUTTONDOWN or MOUSEBUTTONUP:
                if not mouse_down: mouse_down = mouse.get_pressed()[0]
                else: mouse_down = False
        width,height = window.get_size()

        if do_title:

            robber1_pose = "kitchen"
            robber1_lastmove = 0

            robber2_climbing = ""
            robber2_pose = 0
            robber2_status = 0
            robber2_lastmove = 0

            flashed = False

            robber3_status = False
            robber3_lastmove = 0

            robber4_status = False
            robber4_lastmove = 0
            robber4_progress = 0

            power = 100
            power_text = power_font.render(str(power),True,(0,0,0))

            power_done = False

            move_1 = False
            move_2 = False
            move_3 = False
            move_4 = False

            office_pose = 0
            old = 0


            hiding = 0
            hide = False

            box_open = False

            time_s = 0
            time_h = 0

            if not music.get_busy():
                music.play(musicsfx)
            surf = surface.Surface((width,height),SRCALPHA)
            tite = genimg(title,width//2,height//2,width,height)
            surf.set_alpha(255-(255-fade*5))
            surf.blit(tite[0],tite[1])
            window.blit(surf,(0,0))
            if not staticsfc.get_busy():
                staticsfc.play(staticsfx)
            keys = key.get_pressed()
            if keys[K_SPACE] or fade != 50:
                fade -= 1
            staticsfc.set_volume((fade*0.015))
            music.set_volume((fade*0.01))
            if fade <= 0:
                fade = 50
                do_title = False
                staticsfc.stop()
                music.stop()
                staticsfc.set_volume(0.5)
                music.set_volume(0.2)


        else:

            #time ------------------------
            if time_h == 6:
                timed = 0
                yheight = 0
                skysuf = surface.Surface((width,height*3))
                skyimg = genimg(sky,width//2,height//1.2,width,height*4)
                sunimg = genimg(sun,width//2,height+height//4,width//1.5,height)
                skysuf.blit(skyimg[0],skyimg[1])
                skysuf.blit(sunimg[0],sunimg[1])
                siloimg = genimg(silo,width//2,height//2,width,height)
                while yheight <= height//2:
                    clock.tick(10)
                    yheight += 1
                    window.blit(skysuf,(0,(-yheight)))
                    window.blit(siloimg[0],siloimg[1])
                    display.update()
                    await asyncio.sleep(0)
                while not (timed == 100 or key.get_pressed()[K_SPACE] or mouse.get_pressed):
                    clock.tick(10)
                a = 50
                while a != 0:
                    clock.tick(20)
                    skysuf.set_alpha(255-(255-a*5))
                    window.blit(skysuf,(0,(-yheight)))
                    window.blit(siloimg[0],siloimg[1])
                    display.update()
                    await asyncio.sleep(0)
                    a -= 1
                do_title = True
            time_s += 1
            if time_s >= 1000:
                time_h += 1
                time_s = 0
            power_font = font.SysFont('roboto', width//20)
            time_font = font.SysFont('roboto', width//35)
            positions = {
            (0, 1): (width - width // 40, height // 2, width // 20, height // 2, 0), # Right
            (0, 3): (width // 4, height - height // 40, width // 2.5, height // 20, -90),  # Bottom (office_pose 0 or 3)
            (0, 4): (3 * width // 4, height - height // 40, width // 2.5, height // 20, -90), # Bottom (office_pose 0 or 4)
            (0, 2): (width // 40, height // 2, width // 20, height // 2, 180) # Left
            }

            #robber movenment ----------------------------------------------

            #rob1
            
            #reset
            # robber1_pose = "none"
            # robber1_lastmove = 0

            chance = 0
            try: chance = 1000//time_h
            except: chance = 1000
            if chance <100:
                chance = 100
            minchance = 100
            if power <= 0: minchance = minchance//5
            if random.randint(minchance,chance) < robber1_lastmove:
                robber1_lastmove = 0
                #floor 1
                if robber1_pose == "none": robber1_pose = random.choice(["dining","kitchen","none"])
                elif robber1_pose == "living": robber1_pose = random.choice(["dining","kitchen","stair","living"])
                elif robber1_pose == "kitchen": robber1_pose = random.choice(["living","kitchen"])
                elif robber1_pose == "dining": robber1_pose = random.choice(["living","stair","dining"])

                #floor 2
                elif robber1_pose == "stair": robber1_pose = random.choice(["bedroom","gameroom","door","stair"])
                elif robber1_pose == "bedroom": robber1_pose = random.choice(["stair","bedroom","gameroom"])
                elif robber1_pose == "gameroom": robber1_pose = random.choice(["stair","door","gameroom"])

            
                #at door
                elif robber1_pose == "door":
                    if not hide:
                        screaming.play(scream)
                        red = 100
                        while red != 50:
                            red-=1
                            widthchange = (width//10)
                            heightchange = (height//10)
                            jump = genimg(rob1jump,width//2+random.randint(-widthchange,widthchange),height//2+random.randint(-heightchange,heightchange),width,height)
                            if red < 0:
                                red = 0
                            window.fill((red,0,0))
                            window.blit(jump[0],jump[1])
                            genstatic(window,1,2)
                            display.update()
                            await asyncio.sleep(0)
                        while red != 0:
                            red-=1
                            widthchange = (width//10)
                            heightchange = (height//10)
                            jump = genimg(rob1jump,width//2+random.randint(-widthchange,widthchange),height//2+random.randint(-heightchange,heightchange),width,height)
                            newsurf = surface.Surface((width,height),SRCALPHA)
                            newsurf.blit(jump[0],jump[1])
                            newsurf.set_alpha(255-(255-red*5))
                            if red < 0:
                                red = 0
                            window.fill((red,0,0))
                            window.blit(newsurf,(0,0))
                            
                            genstatic(window,1,2)
                            display.update()
                            await asyncio.sleep(0)

                        do_title = True
                    else:
                        knock.play()
                        robber1_pose = "none"
            else: robber1_lastmove += 1
            #rob1 end
            #rob2
            chance = 0
            try: chance = 2000//time_h
            except: chance = 2000
            minchance = 300
            if power <= 0: minchance = minchance//5
            if random.randint(minchance,chance) < robber2_lastmove or robber2_status > 5:
                robber2_lastmove = 0
                if robber2_status == 0:
                    robber2_climbing = random.choice(["O1","O2","O3","O4","O5"])
                    if robber2_climbing == "O1": robber2_pose = 1
                    elif robber2_climbing == "O2" or robber2_climbing == "O3": robber2_pose = 2
                    elif robber2_climbing == "O4" or robber2_climbing == "O5": robber2_pose = 3
                    robber2_status = 1
                else:
                    if robber2_status > 5 and not robber1_pose == "door":
                        steping.play(glass)
                        while steping.get_busy():
                            if office_pose in poses:
                                background = genimg(poses[office_pose], width//2, height//2, width, height)

                            if office_pose == 0.5 and old == 0.5:
                                office_pose = next_pos
                            elif office_pose == 1.5 and old == 1.5:
                                office_pose = 0 if next_pos == 0 else 1.7
                            elif office_pose == 1.7 and old == 1.7:
                                office_pose = 1.5 if next_pos == 0 else 2
                            elif office_pose == 3.1 and old == 3.1:
                                office_pose = 0 if hiding == -1 else 3.2
                            elif office_pose == 3.2 and old == 3.2:
                                office_pose = 3.1 if hiding == -1 else 3.3
                            elif office_pose == 3.3 and old == 3.3:
                                office_pose = 3.2 if hiding == -1 else 3
                                if office_pose == 3:
                                    hiding = 0
                                hide = False
                            elif office_pose == 3:
                                hide = True

                            window.blit(background[0], background[1])

                            if office_pose == 1 and robber1_pose == "door":
                                rob = genimg(robber1_poses[5],width//2,height//2,width,height)
                                window.blit(rob[0],rob[1])

                            #render camera -------------------------------------------------------
                            if power > 0:
                                if office_pose == 4:
                                    rendcams(0,0,width,height,True)
                                elif office_pose == 0:
                                    rendcams(width*0.3241,height*0.224,width*0.383,height*0.29,False)
                            elif office_pose == 4: office_pose = 0
                            old = office_pose
                            if office_pose == 0:
                                time_text = time_font.render(str(int(time_h))+":00",True,(0,200,0))
                                window.blit(time_text,(width*0.71,height*0.592))

                            window.blit(dark,(0,0))
                            if power <= 0:
                                power = 0
                                window.blit(dark,(0,0))

                            if not office_pose == 4:
                                genstatic(window,1,2)
                            display.update()
                            await asyncio.sleep(0)
                        steping.play(steps)
                        while steping.get_busy():
                            if office_pose in poses:
                                background = genimg(poses[office_pose], width//2, height//2, width, height)

                            if office_pose == 0.5 and old == 0.5:
                                office_pose = next_pos
                            elif office_pose == 1.5 and old == 1.5:
                                office_pose = 0 if next_pos == 0 else 1.7
                            elif office_pose == 1.7 and old == 1.7:
                                office_pose = 1.5 if next_pos == 0 else 2
                            elif office_pose == 3.1 and old == 3.1:
                                office_pose = 0 if hiding == -1 else 3.2
                            elif office_pose == 3.2 and old == 3.2:
                                office_pose = 3.1 if hiding == -1 else 3.3
                            elif office_pose == 3.3 and old == 3.3:
                                office_pose = 3.2 if hiding == -1 else 3
                                if office_pose == 3:
                                    hiding = 0
                                hide = False
                            elif office_pose == 3:
                                hide = True

                            window.blit(background[0], background[1])

                            if office_pose == 1 and robber1_pose == "door":
                                rob = genimg(robber1_poses[5],width//2,height//2,width,height)
                                window.blit(rob[0],rob[1])

                            #render camera -------------------------------------------------------
                            if power > 0:
                                if office_pose == 4:
                                    rendcams(0,0,width,height,True)
                                elif office_pose == 0:
                                    rendcams(width*0.3241,height*0.224,width*0.383,height*0.29,False)
                            elif office_pose == 4: office_pose = 0
                            old = office_pose
                            if office_pose == 0:
                                time_text = time_font.render(str(int(time_h))+":00",True,(0,200,0))
                                window.blit(time_text,(width*0.71,height*0.592))

                            window.blit(dark,(0,0))
                            if power <= 0:
                                power = 0
                                window.blit(dark,(0,0))

                            if not office_pose == 4:
                                genstatic(window,1,2)
                            display.update()
                            await asyncio.sleep(0)
                        screaming.play(scream)
                        red = 100
                        while red != 50:
                            red-=1
                            widthchange = (width//10)
                            heightchange = (height//10)
                            jump = genimg(rob1jump,width//2+random.randint(-widthchange,widthchange),height//2+random.randint(-heightchange,heightchange),width,height)
                            if red < 0:
                                red = 0
                            window.fill((red,0,0))
                            window.blit(jump[0],jump[1])
                            genstatic(window,1,2)
                            display.update()
                            await asyncio.sleep(0)
                        while red != 0:
                            red-=1
                            widthchange = (width//10)
                            heightchange = (height//10)
                            jump = genimg(rob1jump,width//2+random.randint(-widthchange,widthchange),height//2+random.randint(-heightchange,heightchange),width,height)
                            newsurf = surface.Surface((width,height),SRCALPHA)
                            newsurf.blit(jump[0],jump[1])
                            newsurf.set_alpha(255-(255-red*5))
                            if red < 0:
                                red = 0
                            window.fill((red,0,0))
                            window.blit(newsurf,(0,0))
                            
                            genstatic(window,1,2)
                            display.update()
                            await asyncio.sleep(0)

                        do_title = True
                    else: robber2_status += 1
            else: robber2_lastmove += 1
            #rob2 end
            rob3move()
            rob4move()

            #sfx ----------------------------------------------

            if (not power_done) and power <= 0:
                powerch.play(power_down)
                power_done = True

            if floornum == 1 and camnumf1 == 1 and robber1_pose == "kitchen":
                if not breath.get_busy():
                    breath.play(breathing)
            else:
                breathing.stop()

            if not music.get_busy():
                music.play(musicsfx)
            if hide or power <= 0:
                if not music.get_volume() >= 0.8:
                    music.set_volume(music.get_volume()+0.009)
            elif not music.get_volume() <= 0.2:
                music.set_volume(music.get_volume()-0.01)
            
            if not staticsfc.get_busy():
                staticsfc.play(staticsfx)

            if power <= 0:
                if not staticsfc.get_volume() <= 0:
                    staticsfc.set_volume(staticsfc.get_volume()-0.02)
            elif office_pose == 4:
                if not staticsfc.get_volume() >= 0.9:
                    staticsfc.set_volume(staticsfc.get_volume()+0.02)
            elif office_pose == 0 or (office_pose >= 3 and office_pose <= 3.3):
                if not staticsfc.get_volume() <= 0.8:
                    staticsfc.set_volume(staticsfc.get_volume()-0.02)
                elif not staticsfc.get_volume() >= 0.8:
                    staticsfc.set_volume(staticsfc.get_volume()+0.02)
            else:
                if not staticsfc.get_volume() <= 0.6:
                    staticsfc.set_volume(staticsfc.get_volume()-0.02)
            
            #rendering  ------------------------------------------------------------------------------------------------------------

            

            #render office -------------------------------------------------

            if office_pose in poses:
                background = genimg(poses[office_pose], width//2, height//2, width, height)

            if office_pose == 0.5 and old == 0.5:
                office_pose = next_pos
            elif office_pose == 1.5 and old == 1.5:
                office_pose = 0 if next_pos == 0 else 1.7
            elif office_pose == 1.7 and old == 1.7:
                office_pose = 1.5 if next_pos == 0 else 2
            elif office_pose == 2:
                lever = Rect(width*0.4, height*0.3, width*0.25, height*0.2)
                if mouserect.colliderect(lever) and mouse_down:
                    office_pose = 2.5
            elif office_pose == 2.5:
                if power > 0:
                    power -= 2.5
                    mixer.Channel(6).play(flashsfx)
                    maxalpha = 25
                    fullscrnrect = genimg(flash, width//2, height//2, width, height)
                    flashscr = Surface(fullscrnrect[0].get_size())
                    flashscr.fill((190,190,190))
                    flashscr.blit(fullscrnrect[0], (0, 0))
                    background = genimg(box_open_down, width//2, height//2, width, height)
                    rob1caught = False
                    if floornum == 1:
                        if camnumf1 == 0 and robber1_pose == "dining":
                            rob1caught = True
                        if camnumf1 == 1 and robber1_pose == "kitchen":
                            rob1caught = True
                        if camnumf1 == 2 and robber1_pose == "living":
                            rob1caught = True
                    elif floornum == 2:
                        if camnumf2 == 0 and robber1_pose == "bedroom":
                            rob1caught = True
                        if camnumf2 == 1 and robber1_pose == "gameroom":
                            rob1caught = True
                        if camnumf2 == 2 and robber1_pose == "stair":
                            rob1caught = True
                    elif floornum == 3:
                        if camnumf3 == 0 and robber3_status:
                            rob3move(True)
                    
                        if camnumf3+1 == robber2_pose:
                            robber2_lastmove = 0
                            robber2_status = 0
                            robber2_climbing = 0
                            robber2_pose = 0
                    
                    if rob1caught:
                        robber1_lastmove = 0
                        if robber1_pose == "dining": robber1_pose = "none"
                        elif robber1_pose == "living": robber1_pose = random.choice(["dining","kitchen"])
                        elif robber1_pose == "kitchen": robber1_pose = "none"
                        elif robber1_pose == "stair": robber1_pose = "living"
                        elif robber1_pose == "bedroom": robber1_pose = "stair"
                        elif robber1_pose == "gameroom": robber1_pose = "stair"
                    

                    for alpha in range(maxalpha):
                        clock.tick(20)
                        flashscr.set_alpha((maxalpha - alpha) * 4)
                        window.blit(background[0], background[1])
                        window.blit(flashscr, fullscrnrect[1])
                        window.blit(dark,(0,0))
                        genstatic(window,1,2)
                        display.update()
                        await asyncio.sleep(0)
                office_pose = 2
            elif office_pose == 3.1 and old == 3.1:
                office_pose = 0 if hiding == -1 else 3.2
            elif office_pose == 3.2 and old == 3.2:
                office_pose = 3.1 if hiding == -1 else 3.3
            elif office_pose == 3.3 and old == 3.3:
                office_pose = 3.2 if hiding == -1 else 3
                if office_pose == 3:
                    hiding = 0
                hide = False
            elif office_pose == 3:
                hide = True

            window.blit(background[0], background[1])

            if office_pose == 1 and robber1_pose == "door":
                rob = genimg(robber1_poses[5],width//2,height//2,width,height)
                window.blit(rob[0],rob[1])

            #render camera -------------------------------------------------------
            if power > 0:
                if office_pose == 4:
                    rendcams(0,0,width,height,True)
                elif office_pose == 0:
                    rendcams(width*0.3241,height*0.224,width*0.383,height*0.29,False)
            elif office_pose == 4: office_pose = 0
            old = office_pose

            #office movement --------------------------------------------------------

            # Right side movement (office_pose 0 or 1)
            if office_pose in (0, 1):
                sidebar = genimg(pointer, *positions[(0, 1)])  # Using * to unpack position arguments
                window.blit(sidebar[0], sidebar[1])

                if mouserect.colliderect(sidebar[1]):
                    if mousexmove > 0 and not move_4:
                        if office_pose == 1:
                            next_pos = 0
                        elif office_pose == 0:
                            next_pos = 1
                        office_pose = 0.5
                        move_4 = True
                else:
                    move_4 = False

            # Bottom movement (office_pose 0 or 3)
            if office_pose in (0, 3):
                sidebar = genimg(pointer, *positions[(0, 3)])
                window.blit(sidebar[0], sidebar[1])

                if mouserect.colliderect(sidebar[1]):
                    if mouseymove < 0 and not move_2:
                        if office_pose == 0:
                            office_pose = 3.1
                            hiding = 1
                        else:
                            office_pose = 3.3
                            hiding = -1
                        move_2 = True
                else:
                    move_2 = False

            # Bottom movement (office_pose 0 or 4)
            if office_pose in (0, 4):
                sidebar = genimg(pointer, *positions[(0, 4)])
                window.blit(sidebar[0], sidebar[1])

                if mouserect.colliderect(sidebar[1]):
                    if mouseymove < 0 and not move_3:
                        if office_pose == 0:
                            office_pose = 4
                        elif office_pose == 4:
                            office_pose = 0
                        move_3 = True
                else:
                    move_3 = False

            # Left side movement (office_pose 0 or 2)
            if office_pose in (0, 2):
                sidebar = genimg(pointer, *positions[(0, 2)])
                window.blit(sidebar[0], sidebar[1])

                if mouserect.colliderect(sidebar[1]):
                    if mousexmove < 0 and not move_1:
                        if office_pose == 0:
                            next_pos = 2
                            office_pose = 1.5
                        elif office_pose == 2:
                            next_pos = 0
                            office_pose = 1.7
                        move_1 = True
                else:
                    move_1 = False
            power_text = power_font.render(str(int(power)),True,(0,200,0))
            window.blit(power_text,(width*0.03,height*0.01))

            if office_pose == 0:
                time_text = time_font.render(str(int(time_h))+":00",True,(0,200,0))
                window.blit(time_text,(width*0.71,height*0.592))

            window.blit(dark,(0,0))
            if power <= 0:
                power = 0
                window.blit(dark,(0,0))

        if not office_pose == 4:
            genstatic(window,1,2)

        display.update()
        await asyncio.sleep(0)

if __name__ == "__main__":
    asyncio.run(main())