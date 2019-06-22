import pyxel
from PIL import Image, ImageFont, ImageDraw
import string

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

class Anatta:
    # -- インスタンス変数で使うメリデメの理解がないので使用保留します。
    # def __init__(self):
    #     self.dot_x = 64
    #     self.dot_y = 64

    # -- Display coodinates in a window. (DCW)
    dot_x = 64
    dot_y = 64

    # -- Display coodinates in a map. (DCM)
    tile_x = 64
    tile_y = 64

    x_change_quantity = 0
    y_change_quantity = 0

class Parson:
    tile_x = Anatta.tile_x + ( 16 * 2 )
    tile_y = Anatta.tile_y + ( 16 * 2 )

class App:
    base_x = 0
    base_y = 0
    window_size_x = 256
    window_size_y = 256
    map_size_x = 32
    quantity_move_x = 0
    quantity_move_y = 0
    count_move_x = 0
    count_move_y = 0
    cant_go = ( 5, 7, 96, 128 )
    is_rect = 0

    fontfile = 'font/x8y12pxTheStrongGamer.ttf'
    letter_size = (8, 12)
    ascii_chars = string.punctuation + string.digits + string.ascii_letters
    ひらがな = "".join(chr(c) for c in range(ord('ぁ'), ord('ゔ')+1))+"ー"
    カタカナ = "".join(chr(c) for c in range(ord('ァ'), ord('ヶ')+1))+"ー"
    alphabet = ascii_chars + ひらがな + カタカナ + "、。「」"
    font = Font(fontfile, letter_size, alphabet)

    def __init__(self):
        # init(width, height, [caption], [fps])
        pyxel.init(self.window_size_x,self.window_size_y,caption="Anicca",scale=4, fps=25)
        # pyxel.init(self.window_size_x,self.window_size_y,caption="Anicca", scale=2, fps=25)

        pyxel.load('samsara.pyxres')

        self.draw_font(2, self.font)

        pyxel.run(self.update, self.draw)

    def collision_detection(self,tile_x,tile_y,direction):
        if direction == "r":
            add_num = (2,0)
        elif direction == "d":
            add_num = (0,2)
        if direction == "l":
            add_num = (-2,0)
        elif direction == "u":
            add_num = (0,-2)
        # print(pyxel.tilemap(0).get(tile_x/8 + add_num[0], tile_y/8 + add_num[1]))# show img pallet code.

        if pyxel.tilemap(0).get(tile_x/8 + add_num[0], tile_y/8 + add_num[1]) not in self.cant_go and\
        pyxel.tilemap(0).get(tile_x/8+ add_num[0] +1, tile_y/8 + add_num[1]) not in self.cant_go and\
        pyxel.tilemap(0).get(tile_x/8+ add_num[0], tile_y/8 + add_num[1] +1) not in self.cant_go and\
        pyxel.tilemap(0).get(tile_x/8+ add_num[0] +1, tile_y/8 + add_num[1] +1) not in self.cant_go:
            return True
        else:
            return False

    def update(self):
        # qキーが押されたらゲームを終了する。
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

        # -- Map's movement below a window.
        if self.quantity_move_x == 0 and self.quantity_move_y == 0 and self.is_rect == 0:
            if pyxel.btn(pyxel.KEY_D) or pyxel.btn(pyxel.KEY_RIGHT):
                if self.base_x > -(self.window_size_x):
                    if self.collision_detection(Anatta.tile_x, Anatta.tile_y, "r"):
                    # if pyxel.tilemap(0).get(Anatta.tile_x/8+2,Anatta.tile_y/8) not in self.cant_go:
                        # -- Map move opposite to the btn.
                        self.quantity_move_x = -4
                        # -- DCM move same direction.
                        Anatta.tile_x += 16
            if pyxel.btn(pyxel.KEY_A) or pyxel.btn(pyxel.KEY_LEFT):
                if self.base_x < 0:
                    if self.collision_detection(Anatta.tile_x, Anatta.tile_y, "l"):
                        self.quantity_move_x = 4
                        Anatta.tile_x -= 16
            if pyxel.btn(pyxel.KEY_S) or pyxel.btn(pyxel.KEY_DOWN):
                if self.base_y > -(self.window_size_y):
                    if self.collision_detection(Anatta.tile_x, Anatta.tile_y, "d"):
                        self.quantity_move_y = -4
                        Anatta.tile_y += 16
            if pyxel.btn(pyxel.KEY_W) or pyxel.btn(pyxel.KEY_UP):
                if self.base_y < 0:
                    if self.collision_detection(Anatta.tile_x, Anatta.tile_y, "u"):
                        self.quantity_move_y = 4
                        Anatta.tile_y -= 16

        # -- The map stops when it moved 16px. x-axis.
        if self.quantity_move_x != 0:
            if self.count_move_x >= 4:
                self.quantity_move_x = 0
                self.count_move_x = 0
            else:
                self.count_move_x += 1
            self.base_x += self.quantity_move_x
            Parson.tile_x += self.quantity_move_x

        # -- Same as above. y-axis.
        if self.quantity_move_y != 0:
            if self.count_move_y >= 4:
                self.quantity_move_y = 0
                self.count_move_y = 0
            else:
                self.count_move_y += 1
            self.base_y += self.quantity_move_y
            Parson.tile_y += self.quantity_move_y

        self.update_anatta_state()
        
    # ゲーム内で描画されるドット絵の処理をする
    def draw(self):
        # 真っ黒に背景をする
        pyxel.cls(0)
        # タイルマップを描画する
        self.draw_tilemap()

        self.draw_anatta()
        self.draw_parson()

        # -- draw comment
        if self.is_rect == 1 and pyxel.btnr(pyxel.KEY_SPACE):
            self.is_rect = 0
        elif self.is_rect == 0 and pyxel.btnr(pyxel.KEY_SPACE):
            self.is_rect = 1
        if self.is_rect == 1:
            pyxel.rect(1,1,126,48,0)
        
        if self.is_rect ==1:
            self.text(self.font, 4, 0, """
Samsara
くりかえす せかい
やあ　おでかけですか?""".strip())

    # タイルマップの描画処理(タイルマップの時点で1/8サイズになっている？)
    def draw_tilemap(self):
        tm = 0
        u = 0
        v = 0
        w = self.map_size_x
        h = 32
        # 指定したtm(template)番号の(u,v)座標から
        # サイズ(w,h)の大きさを(base_x,base_y)座標に描画する
        pyxel.bltm(self.base_x,self.base_y,tm,u,v,w,h)

    def draw_anatta(self):
        # anatta = Anatta()
        if pyxel.frame_count % 25 > 12:
            pyxel.blt(Anatta.dot_x,Anatta.dot_y,0,16,0,16,16,12)
        else:
            pyxel.blt(Anatta.dot_x,Anatta.dot_y,0,0,0,16,16,12)
    
    def draw_parson(self):
        if pyxel.frame_count % 25 > 12:
            pyxel.blt(Parson.tile_x,Parson.tile_y,0,48,0,16,16,12)
        else:
            pyxel.blt(Parson.tile_x,Parson.tile_y,0,32,0,16,16,12)

    def update_anatta_state(self):
        # temp_tile_type = pyxel.tilemap(0).get(Anatta.tile_x/8+2,Anatta.tile_y/8)
        # temp_tile_type = pyxel.tilemap(0).get(Anatta.tile_x,Anatta.tile_y)
        # -- when drawing is over, the next judgment.
        # if Anatta.dot_x % 16 == 0:

        # -- Case the destination is a water.
        # if temp_tile_type == 96:
        #     print("water")

        # elif pyxel.btn(pyxel.KEY_D) or pyxel.btn(pyxel.KEY_RIGHT):
        #     Anatta.x_change_quantity = 1
        #     Anatta.count_move = 1
        # elif pyxel.btn(pyxel.KEY_A) or pyxel.btn(pyxel.KEY_LEFT):
        #     Anatta.x_change_quantity = -1
        #     Anatta.count_move = 1

        # if Anatta.x_change_quantity != 0:
        #     if Anatta.count_move >= 16:
        #         Anatta.x_change_quantity = 0
        #         Anatta.count_move = 0
        #     else:
        #         Anatta.count_move += Anatta.count_move
        # Anatta.dot_x += Anatta.x_change_quantity
        pass

    def draw_font(self,img, font, col=7):
        img_bank = pyxel.image(img)
        for y in range(256):
            for x in range(256):
                img_bank.set(x,y,col if font.data[y][x] else 0)

    def text(self,font,x,y,s):
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

App()