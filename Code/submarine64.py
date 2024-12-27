import tkinter as tk
import random
import math

class Submarine64:
    def __init__(self, root):
        self.root = root
        self.root.title("Submarine-64")

        # Initialize game variables
        self.grid_size = 8
        self.total_tiles = self.grid_size ** 2
        self.remaining_tiles = self.total_tiles
        self.submarine_position = random.randint(0, self.total_tiles - 1)
        self.tiles = []
        self.H = math.log(self.total_tiles, 2)
        self.radar_mode = False
        self.selected_tiles = []

        # Create UI elements
        self.create_grid()
        self.info_frame = tk.Frame(self.root)
        self.info_frame.pack()
        self.entropy_label = tk.Label(self.info_frame, text="H = {:.2f}".format(self.H))
        self.entropy_label.pack()
        self.outcome_entropy_label = tk.Label(self.info_frame, text="h(x) = 0")
        self.outcome_entropy_label.pack()
        self.previous_entropy_label = tk.Label(self.info_frame, text="")
        self.previous_entropy_label.pack()
        self.radar_button = tk.Button(self.info_frame, text="Start Radar", command=self.toggle_radar_mode)
        self.radar_button.pack()

    def create_grid(self):
        self.canvas = tk.Canvas(self.root, width=450, height=450, bg="white")
        self.canvas.pack()

        # Create header row (A, B, ..., H)
        for i in range(self.grid_size):
            x0, y0 = (i + 1) * 50, 0
            x1, y1 = x0 + 50, 50
            self.canvas.create_rectangle(x0, y0, x1, y1, fill="white", outline="black")
            self.canvas.create_text(x0 + 25, y0 + 25, text=chr(65 + i), font=("Arial", 16))

        # Create header column (1, 2, ..., 8)
        for j in range(self.grid_size):
            x0, y0 = 0, (j + 1) * 50
            x1, y1 = 50, y0 + 50
            self.canvas.create_rectangle(x0, y0, x1, y1, fill="white", outline="black")
            self.canvas.create_text(x0 + 25, y0 + 25, text=str(j + 1), font=("Arial", 16))

        # Create grid tiles
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                x0, y0 = (i + 1) * 50, (j + 1) * 50
                x1, y1 = x0 + 50, y0 + 50
                tile = self.canvas.create_rectangle(x0, y0, x1, y1, fill="lightblue", outline="black")
                self.tiles.append(tile)

        self.canvas.bind("<Button-1>", self.handle_click)
        self.canvas.bind("<B1-Motion>", self.handle_motion)

    def handle_click(self, event):
        if self.radar_mode:
            self.select_tile(event.x, event.y)
        else:
            self.click_tile(event.x, event.y)

    def handle_motion(self, event):
        if self.radar_mode:
            self.select_tile(event.x, event.y)

    def select_tile(self, x, y):
        tile_index = ((x // 50) - 1) * self.grid_size + ((y // 50) - 1)

        if tile_index < 0 or tile_index >= self.total_tiles or self.tiles[tile_index] is None:
            return  # Ignore invalid or already clicked tiles

        if tile_index not in self.selected_tiles:
            self.canvas.itemconfig(self.tiles[tile_index], fill="yellow")
            self.selected_tiles.append(tile_index)

    def click_tile(self, x, y):
        tile_index = ((x // 50) - 1) * self.grid_size + ((y // 50) - 1)

        if tile_index < 0 or tile_index >= self.total_tiles or self.tiles[tile_index] is None:
            return  # Ignore invalid or already clicked tiles

        if tile_index == self.submarine_position:
            self.canvas.itemconfig(self.tiles[tile_index], fill="green")
            self.show_message("You found the submarine! You win!")
            h_x = math.log(self.remaining_tiles, 2)  # h(x) for hit
            self.remaining_tiles = 0
        else:
            self.canvas.itemconfig(self.tiles[tile_index], fill="red")
            h_x = math.log(1 / ((self.remaining_tiles - 1) / self.remaining_tiles), 2)  # h(x) for miss
            self.remaining_tiles -= 1

        self.tiles[tile_index] = None

        # Update entropy values
        self.previous_entropy_label.config(text=f"previous H = {self.H:.5f}")
        self.H = math.log(self.remaining_tiles, 2) if self.remaining_tiles > 0 else 0
        self.entropy_label.config(text=f"H = {self.H:.5f}")
        self.outcome_entropy_label.config(text=f"h(x) = {h_x:.5f}")

    def toggle_radar_mode(self):
        if not self.radar_mode:
            self.radar_mode = True
            self.radar_button.config(text="Scan")
        else:
            self.radar_check()
            self.radar_mode = False
            self.radar_button.config(text="Start Radar")

    def radar_check(self):
        if any(tile == self.submarine_position for tile in self.selected_tiles):
            self.show_message("The submarine is in the selected set!")
            for i in range(self.total_tiles):
                if i not in self.selected_tiles:
                    self.canvas.itemconfig(self.tiles[i], fill="orange")
            # Reset selected tiles to lightblue
            for tile_index in self.selected_tiles:
                self.canvas.itemconfig(self.tiles[tile_index], fill="lightblue")
            probability = len(self.selected_tiles) / self.remaining_tiles
            self.remaining_tiles = len(self.selected_tiles)
        else:
            self.show_message("The submarine is not in the selected set!")
            for tile_index in self.selected_tiles:
                self.canvas.itemconfig(self.tiles[tile_index], fill="orange")
            probability = 1. - len(self.selected_tiles) / self.remaining_tiles
            self.remaining_tiles = self.remaining_tiles - len(self.selected_tiles)

        h_x = math.log(1. / probability , 2)

        self.previous_entropy_label.config(text=f"previous H = {self.H:.5f}")
        self.H = math.log(self.remaining_tiles, 2) if self.remaining_tiles > 0 else 0
        self.entropy_label.config(text=f"H = {self.H:.5f}")
        self.outcome_entropy_label.config(text=f"h(x) = {h_x:.5f}")

        # Reset selected tiles
        self.selected_tiles = []

    def show_message(self, message):
        win_message = tk.Label(self.info_frame, text=message, fg="green")
        win_message.pack()
        if not self.radar_mode:
            self.canvas.unbind("<Button-1>")
            self.canvas.unbind("<B1-Motion>")

if __name__ == "__main__":
    root = tk.Tk()
    game = Submarine64(root)
    root.mainloop()