class Field():
    # screen was already created by using FIELD_WIDTH, FIELD_HEIGHT and BLOCK_SIZE
    def __init__(self, screen, field_color, start_x, width, height, block_size):
        # visual display
        self.screen = screen
        self.fieldColor = field_color

        # below data will be referenced by other objects
        self.start_x = start_x   # start position of gaming area in pixels
        self.width = width       # in unit of blocks
        self.height = height     # in unit of blcoks
        self.block_size = block_size  # in pixels

    def draw(self):
        # Only fills the playing area
        rect = (self.start_x, 0, self.width * self.block_size, self.height * self.block_size)
        self.screen.fill(self.fieldColor, rect)
