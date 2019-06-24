import pyxel
from PIL import Image, ImageFont, ImageDraw
import string

WINDOW_SIZE_X = 256
WINDOW_SIZE_Y = 256
MAP_SIZE_X = 64
MAP_SIZE_Y = 64
is_rect = 0

IS_MODE_TERMINATE = 0
MODE_OPENING = 1000
MODE_PROLOGUE = 1500
MODE_MAP = 2000
MODE_TALK = 3000
MODE_EPILOGUE = 4000
MODE_ENDING = 5000
MODE = MODE_OPENING
# MODE = MODE_MAP

# ===== move parameters =====
TILE_X = 64
TILE_Y = 64
MAP_BASE_X = 0
MAP_BASE_Y = 0

MUSIC = 5
TEMP_FRAMES = 0



class Font:
    def __init__(self, file, size, alphabet):
        import numpy as np
        self.file = file
        self.size = size
        self.alphabet = alphabet

        px_w, px_h = size
        font = ImageFont.truetype(file, size=px_h)
        img = Image.new('1', size=(256, 256))
        draw = ImageDraw.Draw(img)
        coords = {}
        x, y = 0, 0
        for c in alphabet:
            if x + px_w > 256:
                x = 0
                y += px_h
            draw.text((x, y), c, font=font, fill=1)
            coords[c] = (x, y)
            x += px_w
        self.coords = coords
        self.img = img
        self.data = np.array(img.getdata()).reshape(256, 256)

class Text:
    fontfile = 'font/x8y12pxTheStrongGamer.ttf'
    letter_size = (8, 12)
    ascii_chars = string.punctuation + string.digits + string.ascii_letters
    ひらがな = "".join(chr(c) for c in range(ord('ぁ'), ord('ゔ')+1))+"ー"
    カタカナ = "".join(chr(c) for c in range(ord('ァ'), ord('ヶ')+1))+"ー"
    alphabet = ascii_chars + ひらがな + カタカナ + "、。「」"
    font = Font(fontfile, letter_size, alphabet)

    def draw_font(self,img, font, col=7):
        img_bank = pyxel.image(img)
        for y in range(256):
            for x in range(256):
                img_bank.set(x,y,col if font.data[y][x] else 0)
    
    def display(self,font,x,y,s):
        w, h = font.size
        left = x

        for ch in s:
            if ch == '\n':
                x = left
                y += h
                continue
            if ch == ' ':
                x += w
                continue
            if ch in font.coords.keys():
                u, v = font.coords[ch]
                pyxel.blt(x, y, 2, u, v, w, h, 0)
            x += w

    def display_rect(self):
        global is_rect
        if is_rect == 1 and pyxel.btnr(pyxel.KEY_SPACE):
            is_rect = 0
        elif is_rect == 0 and pyxel.btnr(pyxel.KEY_SPACE):
            is_rect = 1
        if is_rect == 1:
            pyxel.rect(1,1,254,48,0)
            self.display(self.font, 4, 0, "Samsara\nくりかえす せかい\nやあ　おでかけですか?")

class Anatta:
    # -- インスタンス変数で使うメリデメの理解がないので使用保留します。
    # def __init__(self):
    #     self.dot_x = 64
    #     self.base_y = 64

    # -- Display coodinates in a window. (DCW)
    base_x = 64
    base_y = 64
    # -- Display coodinates in a map. (DCM)
    tile_x_org = 64
    tile_y_org = 64
    tile_x = tile_x_org
    tile_y = tile_y_org
    tile_move_x = 0
    tile_move_y = 0
    x_change_quantity = 0
    y_change_quantity = 0
    move_x = 0
    move_y = 0
    count_move_x1 = 0
    count_move_y = 0

    def __init__(self):
        self.Utilities = Utilities()

    def display(self):
        if pyxel.frame_count % 25 > 12:
            pyxel.blt(self.base_x, self.base_y,0,16,0,16,16,12)
        else:
            pyxel.blt(self.base_x, self.base_y,0,0,0,16,16,12)

    def move(self):
        global TILE_X, TILE_Y, MAP_BASE_X, MAP_BASE_Y
        if self.move_x == 0 and self.move_y == 0:
            if TILE_X < 64 or (TILE_X >= 256+64 and TILE_X < 496):
            # if TILE_X < 64 or MAP_BASE_X <= -(WINDOW_SIZE_X):
            # if self.tile_x < self.tile_x_org and self.move_x == 0:
                if pyxel.btn(pyxel.KEY_D) or pyxel.btn(pyxel.KEY_RIGHT):
                    if self.Utilities.collision_detection(TILE_X, TILE_Y, "r"):
                        self.move_x = 4
                #     self.base_x += 8
                        self.tile_move_x = 16
            if (TILE_X <= 64 and TILE_X > 0) or TILE_X > 256+64:
            # if (TILE_X <= 64 and TILE_X > 0) or MAP_BASE_X < -(WINDOW_SIZE_X):
            # if self.tile_x <= self.tile_x_org and self.move_x == 0:
                if pyxel.btn(pyxel.KEY_A) or pyxel.btn(pyxel.KEY_LEFT):
                    # self.base_x -= 8
                    if self.Utilities.collision_detection(TILE_X, TILE_Y, "l"):
                        self.move_x = -4
                        self.tile_move_x = -16
            if TILE_Y < 64 or (TILE_Y >= 256+64 and TILE_Y < 496):
                if pyxel.btn(pyxel.KEY_S) or pyxel.btn(pyxel.KEY_DOWN):
                    if self.Utilities.collision_detection(TILE_X, TILE_Y, "d"):
                        self.move_y = 4
                        self.tile_move_y = 16
            if (TILE_Y <= 64 and TILE_Y > 0) or TILE_Y > 256+64:
                if pyxel.btn(pyxel.KEY_W) or pyxel.btn(pyxel.KEY_UP):
                    if self.Utilities.collision_detection(TILE_X, TILE_Y, "u"):
                        self.move_y = -4
                        self.tile_move_y = -16

        # -- The map stops when it moved 16px by btn. x-axis.
        if self.move_x != 0:
            if self.count_move_x1 >= 4:
                self.move_x = 0
                self.count_move_x1 = 0
                self.tile_x += self.tile_move_x# 入れかえ完了後不要
                TILE_X += self.tile_move_x
                # print("TILE_X:"+str(TILE_X))
            else:
                self.count_move_x1 += 1
                self.base_x += self.move_x

        # -- The map stops when it moved 16px by btn. y-axis.
        if self.move_y != 0:
            if self.count_move_y >= 4:
                self.move_y = 0
                self.count_move_y = 0
                self.tile_y += self.tile_move_y# 入れかえ完了後不要
                # print(self.tile_x)
                TILE_Y += self.tile_move_y
                # print("TILE_Y:"+str(TILE_Y))
            else:
                self.count_move_y += 1
                self.base_y += self.move_y
        

class Satta:
    tile_x = Anatta.tile_x + ( 16 * 2 )
    tile_y = Anatta.tile_y + ( 16 * 2 )

class Map:
    base_x = 0
    base_y = 0
    quantity_move_x = 0
    quantity_move_y = 0
    tile_move_x = 0
    tile_move_y = 0
    count_move_x = 0
    count_move_y = 0

    def __init__(self):
        self.Utilities = Utilities()

    """タイルマップの描画処理(タイルマップの時点で1/8サイズになっている？)"""
    def display(self):
        global MUSIC
        if MUSIC != 3:
            pyxel.stop()
            MUSIC = 3
            pyxel.playm(MUSIC, loop=True)
        tm = 0
        u = 0
        v = 0
        w = MAP_SIZE_X
        h = MAP_SIZE_Y
        # 指定したtm(template)番号の(u,v)座標から
        # サイズ(w,h)の大きさを(base_x,base_y)座標に描画する
        pyxel.bltm(self.base_x,self.base_y,tm,u,v,w,h)

    # -- Map's movement below a window.
    def move(self):
        global TILE_X, TILE_Y, MAP_BASE_X, MAP_BASE_Y
        if self.quantity_move_x == 0 and self.quantity_move_y == 0 and is_rect == 0:
            if MAP_BASE_X > -(WINDOW_SIZE_X) and TILE_X >= 64:
                if pyxel.btn(pyxel.KEY_D) or pyxel.btn(pyxel.KEY_RIGHT):
                    if self.Utilities.collision_detection(TILE_X, TILE_Y, "r"):
                    # if pyxel.tilemap(0).get(Anatta.tile_x/8+2,Anatta.tile_y/8) not in self.cant_go:
                        # -- Map move opposite to the btn.
                        self.quantity_move_x = -4
                        # -- DCM move same direction.
                        self.tile_move_x = 16
            if TILE_X > 64 and TILE_X <= 256+64:
            # if (MAP_BASE_X < 0 and TILE_X > 64) or (MAP_BASE_X >= -(WINDOW_SIZE_X) and TILE_X < 256+64):
                if pyxel.btn(pyxel.KEY_A) or pyxel.btn(pyxel.KEY_LEFT):
                    if self.Utilities.collision_detection(TILE_X, TILE_Y, "l"):
                        self.quantity_move_x = 4
                        self.tile_move_x = -16
            if pyxel.btn(pyxel.KEY_S) or pyxel.btn(pyxel.KEY_DOWN):
                if TILE_Y >= 64 and TILE_Y < 256+64:
                # if self.base_y > -(WINDOW_SIZE_Y):
                    if self.Utilities.collision_detection(TILE_X, TILE_Y, "d"):
                        self.quantity_move_y = -4
                        self.tile_move_y = 16
            if pyxel.btn(pyxel.KEY_W) or pyxel.btn(pyxel.KEY_UP):
                if TILE_Y > 64 and TILE_Y <= 256+64:
                # if self.base_y < 0:
                    if self.Utilities.collision_detection(TILE_X, TILE_Y, "u"):
                        self.quantity_move_y = 4
                        self.tile_move_y = -16
        # -- The map stops when it moved 16px by btn. x-axis.
        if self.quantity_move_x != 0:
            if self.count_move_x >= 4:
                self.quantity_move_x = 0
                self.count_move_x = 0
                TILE_X += self.tile_move_x
                # print("TILE_X:"+str(TILE_X))
            else:
                self.count_move_x += 1
                self.base_x += self.quantity_move_x# 入れかえ完了後不要
                MAP_BASE_X += self.quantity_move_x
                Satta.tile_x += self.quantity_move_x

        # -- Same as above. y-axis.
        if self.quantity_move_y != 0:
            if self.count_move_y >= 4:
                self.quantity_move_y = 0
                self.count_move_y = 0
                TILE_Y += self.tile_move_y
                # print("TILE_Y:"+str(TILE_Y))
            else:
                self.count_move_y += 1
                self.base_y += self.quantity_move_y# 入れかえ完了後不要
                MAP_BASE_Y += self.quantity_move_y
                Satta.tile_y += self.quantity_move_y

class Opening_scene:

    def __init__(self):
        self.Text = Text()

    def display(self):
        global MUSIC, IS_MODE_TERMINATE, TEMP_FRAMES
        # -- Opening credit.
        if pyxel.frame_count < 51:
            self.Text.display(self.Text.font, 30, 128, "Created by\nNaoki\nin 2019.")
            if MUSIC != 0:
                MUSIC = 0
                pyxel.play(0,5, loop=False)
                pyxel.play(1,7, loop=False)
        if pyxel.frame_count > 17:
            pyxel.pal(7,6)
        if pyxel.frame_count > 34:
            pyxel.pal(7,5)
        if pyxel.frame_count > 52:
            pyxel.pal()

        # -- Opening scene.
        if pyxel.frame_count >= 68 and TEMP_FRAMES == 0:
            self.Text.display(self.Text.font, 100, 128, "はじめから\nつづきから".strip())
            
            if MUSIC != 1:
                MUSIC = 1
                pyxel.playm(MUSIC, loop=True)
            
            if pyxel.btn(pyxel.KEY_SPACE):
                IS_MODE_TERMINATE =1


class Prologue:

    def __init__(self):
        self.Text = Text()
    
    def display(self):
        global MUSIC, IS_MODE_TERMINATE
        if MUSIC != 2:
            pyxel.stop()
            MUSIC = 2
            pyxel.playm(MUSIC, loop=True)

        pyxel.cls(5)
        if pyxel.btn(pyxel.KEY_SPACE):
                IS_MODE_TERMINATE =1

class Epilogue:

    def __init__(self):
        self.Text = Text()
    
    def display(self):
        global MUSIC, IS_MODE_TERMINATE

        if MUSIC != 0:
            pyxel.stop()
            MUSIC = 0
            # pyxel.playm(MUSIC, loop=True)
            pyxel.play(0,6, loop=True)
            pyxel.play(1,8, loop=True)

        pyxel.cls(10)
        if pyxel.btn(pyxel.KEY_SPACE):
                IS_MODE_TERMINATE =1

class Utilities:
    cant_go = ( 5, 7, 96, 128, 130, 132 )
    dead_tile = 130

    def collision_detection(self,tile_x,tile_y,direction):
        global IS_MODE_TERMINATE
        if direction == "r":
            add_num = (2,0)
        elif direction == "d":
            add_num = (0,2)
        if direction == "l":
            add_num = (-2,0)
        elif direction == "u":
            add_num = (0,-2)

        if pyxel.tilemap(0).get(tile_x/8 + add_num[0], tile_y/8 + add_num[1]) == self.dead_tile:
            IS_MODE_TERMINATE = 1

        # -- To debug.
        print(pyxel.tilemap(0).get(tile_x/8 + add_num[0], tile_y/8 + add_num[1]))# show img pallet code.

        if pyxel.tilemap(0).get(tile_x/8 + add_num[0], tile_y/8 + add_num[1]) not in self.cant_go and\
        pyxel.tilemap(0).get(tile_x/8+ add_num[0] +1, tile_y/8 + add_num[1]) not in self.cant_go and\
        pyxel.tilemap(0).get(tile_x/8+ add_num[0], tile_y/8 + add_num[1] +1) not in self.cant_go and\
        pyxel.tilemap(0).get(tile_x/8+ add_num[0] +1, tile_y/8 + add_num[1] +1) not in self.cant_go:
            return True
        else:
            # print("CantGo")
            return False
        
    def change_mode(self, next_mode, delay_frames=10):
        global MODE, IS_MODE_TERMINATE, TEMP_FRAMES
        if IS_MODE_TERMINATE == 1:#pyxel.btn(pyxel.KEY_SPACE):
            IS_MODE_TERMINATE = 0
            TEMP_FRAMES = pyxel.frame_count
            pyxel.stop()
        if TEMP_FRAMES != 0 and pyxel.frame_count == TEMP_FRAMES + delay_frames:
            MODE = next_mode

class App:

    def __init__(self):
        # init(width, height, [caption], [fps])
        pyxel.init(WINDOW_SIZE_X,WINDOW_SIZE_Y,caption="Anicca", scale=2, fps=25)

        pyxel.load('samsara.pyxres')
        self.Map = Map()
        self.Opening_scene = Opening_scene()
        self.Prologue = Prologue()
        self.Epilogue = Epilogue()
        self.Utilities = Utilities()
        self.Text = Text()
        self.Anatta = Anatta()

        self.Text.draw_font(2, self.Text.font)

        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

        if MODE == MODE_OPENING:
            self.Utilities.change_mode(MODE_PROLOGUE)
        elif MODE == MODE_PROLOGUE:
            self.Utilities.change_mode(MODE_MAP)
        elif MODE == MODE_MAP:
            self.Map.move()
            self.Anatta.move()
            self.Utilities.change_mode(MODE_EPILOGUE)
        elif MODE == MODE_EPILOGUE:
            self.Utilities.change_mode(MODE_PROLOGUE)
        
    # ゲーム内で描画されるドット絵の処理をする
    def draw(self):
        pyxel.cls(0)
        if MODE == MODE_OPENING:
            self.Opening_scene.display()
        elif MODE == MODE_PROLOGUE:
            self.Prologue.display()
        elif MODE == MODE_MAP:
            self.Map.display()
            self.Anatta.display()
            self.draw_Satta()
            self.Text.display_rect()
        elif MODE == MODE_EPILOGUE:
            self.Epilogue.display()
    
    def draw_Satta(self):
        if pyxel.frame_count % 25 > 12:
            pyxel.blt(Satta.tile_x,Satta.tile_y,0,48,0,16,16,12)
        else:
            pyxel.blt(Satta.tile_x,Satta.tile_y,0,32,0,16,16,12)


App()