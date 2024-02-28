import tkinter as tk
import random

class SnakeGame:
    def __init__(self, master, width=400, height=400, cell_size=20):
        self.master = master
        self.master.title("Snake Game")

        self.width = width
        self.height = height
        self.cell_size = cell_size

        self.canvas = tk.Canvas(self.master, width=self.width, height=self.height, bg="black")
        self.canvas.pack()

        self.snake = [(100, 100), (90, 100), (80, 100)]
        self.direction = "Right"

        self.food = self.spawn_food()
        self.growth_pending = 0

        self.joystick_center = (self.width // 2, self.height // 2)
        self.joystick_radius = 50  # Puedes ajustar el tamaño del joystick

        self.canvas.bind("<B1-Motion>", self.on_joystick_move)

        self.update_interval = 100
        self.master.after(self.update_interval, self.update)

    def spawn_food(self):
        x = random.randrange(0, self.width - self.cell_size, self.cell_size)
        y = random.randrange(0, self.height - self.cell_size, self.cell_size)
        food = self.canvas.create_rectangle(x, y, x + self.cell_size, y + self.cell_size, fill="red", tags="food")
        return food

    def move(self):
        head = self.snake[0]
        if self.direction == "Up":
            new_head = (head[0], head[1] - self.cell_size)
        elif self.direction == "Down":
            new_head = (head[0], head[1] + self.cell_size)
        elif self.direction == "Left":
            new_head = (head[0] - self.cell_size, head[1])
        elif self.direction == "Right":
            new_head = (head[0] + self.cell_size, head[1])

        self.snake.insert(0, new_head)

        # Check if snake eats food
        if self.check_collision(self.snake[0], "food"):
            self.canvas.delete("food")
            self.food = self.spawn_food()
            self.growth_pending += 1

        # Check if snake collides with itself or its tail
        if self.check_self_collision():
            self.game_over()

        # Check if snake collides with walls
        if not (0 <= new_head[0] < self.width and 0 <= new_head[1] < self.height):
            self.game_over()

        # Draw the snake
        self.canvas.delete("snake")
        for segment in self.snake:
            x, y = segment
            self.canvas.create_rectangle(x, y, x + self.cell_size, y + self.cell_size, fill="green", tags="snake")

        self.master.update_idletasks()

        # Handle snake growth
        if self.growth_pending > 0:
            self.growth_pending -= 1
        else:
            # If not growing, remove the tail
            self.canvas.delete(self.snake[-1])
            self.snake.pop()

    def check_collision(self, obj1, tag):
        try:
            coords_obj1 = self.canvas.coords(obj1)
        except tk.TclError:
            # El objeto ya no existe en el canvas
            return False

        x1, y1, x2, y2 = coords_obj1

        objects = self.canvas.find_withtag(tag)
        for obj in objects:
            x3, y3, x4, y4 = self.canvas.coords(obj)
            if x1 < x4 and x2 > x3 and y1 < y4 and y2 > y3:
                return True

        return False

    def check_self_collision(self):
        return any(segment == self.snake[0] for segment in self.snake[1:])

    def on_joystick_move(self, event):
        x, y = event.x, event.y
        distance = ((x - self.joystick_center[0])**2 + (y - self.joystick_center[1])**2)**0.5

        if distance > self.joystick_radius:
            angle = self.calculate_angle(self.joystick_center, (x, y))
            self.update_direction(angle)

    def calculate_angle(self, point1, point2):
        x1, y1 = point1
        x2, y2 = point2
        radians = tk.math.atan2(y2 - y1, x2 - x1)
        angle = tk.math.degrees(radians)
        return angle

    def update_direction(self, angle):
        if -45 < angle <= 45:
            self.direction = "Right"
        elif 45 < angle <= 135:
            self.direction = "Up"
        elif -135 <= angle <= -45:
            self.direction = "Down"
        else:
            self.direction = "Left"

    def update(self):
        self.move()
        self.master.after(self.update_interval, self.update)

    def game_over(self):
        self.canvas.create_text(self.width // 2, self.height // 2, text="Game Over", fill="white", font=("Helvetica", 16))
        self.master.unbind("<B1-Motion>")

if __name__ == "__main__":
    root = tk.Tk()
    game = SnakeGame(root)
    root.mainloop()
