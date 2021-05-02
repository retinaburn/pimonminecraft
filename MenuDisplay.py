import time
from board import SCL, SDA
import busio
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306

class MenuDisplay:
    text_block = ["Dadda", "Test", "Lily", "Xander"]
    selected_level = 0
    dy = 2             # The number of pixes to move each step of scroll animation
    time_diff = 0.001  # time to sleep each step of scroll animation
    y_movement = 0     # holds the value of which way the scroll animation will go for next scroll
    triangle_width = 8 # width of triangle

    i2c = busio.I2C(SCL, SDA)
    disp = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c)

    image = 0
    draw = 0

    def draw_triangle(self, draw, width, height, screen_height):
        mid_height = screen_height / 2
        triangle_left_x = 0
        #top left 
        triangle_p0 = (triangle_left_x, mid_height - (height / 2))
        #bottom left
        triangle_p1 = (triangle_left_x, mid_height + (height / 2))
        #middle right
        triangle_p2 = (triangle_left_x + width, mid_height)

        draw.polygon( [triangle_p0, triangle_p1, triangle_p2], fill=255)

    def __init__(self):

        
        self.disp.fill(0)
        self.disp.show()

        self.width = self.disp.width
        self.height = self.disp.height
        self.midheight = self.height / 2

        self.image = Image.new("1", (self.width, self.height))
        self.draw = ImageDraw.Draw(self.image)

        self.disp.fill(0)

        self.padding = -2
        self.top = self.padding
        self.bottom = self.height - self.padding

        self.font_size = 16

        print("Width = %d, Height = %d" % (self.width, self.height))

        self.font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf', self.font_size)

        self.draw_triangle(self.draw, self.triangle_width, self.font_size, self.height)
        self.disp.image(self.image)
        self.disp.show()

        self.x = self.triangle_width + 4
        self.y = self.midheight - self.font_size / 2

        self.text_position = []
        
        for i in range(len(self.text_block)):
            self.text_position.append( ( self.x, self.y + (self.font_size * i) ) )

        for i in range(len(self.text_position)):
            self.text_position[i] = (self.text_position[i][0], self.text_position[i][1])
            self.draw.text( self.text_position[i], self.text_block[i], font=self.font, fill=255)
        self.disp.image(self.image)
        self.disp.show()

        print("Selected level: %s %s" % (self.selected_level, self.text_block[self.selected_level]))

    def animate(self):
        for i in range(int(self.font_size / self.dy)):
            time.sleep(self.time_diff)

            self.draw.rectangle((0, 0, self.width, self.height), outline=0, fill=0)
            self.draw_triangle(self.draw, self.triangle_width, self.font_size, self.height)
            for i in range(len(self.text_position)):
                self.text_position[i] = (self.text_position[i][0], self.text_position[i][1] + self.y_movement)
                self.draw.text( self.text_position[i], self.text_block[i], font=self.font, fill=255)
            self.disp.image(self.image)
            self.disp.show()
        self.y_movement = 0

    def up_action(self):
        if(self.y_movement == 0 and self.selected_level > 0):
            print ("Up moving")
            self.y_movement = self.dy
            self.selected_level -= 1

    def down_action(self):
        if (self.y_movement == 0 and self.selected_level < (len(self.text_block) - 1)):
            print ("Down moving")
            self.y_movement = -1 * self.dy
            self.selected_level += 1

    def level_name(self):
        return self.text_block[self.selected_level]



