import arcade
import random

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Платформер"

PLAYER_SCALING = 0.5
GRAVITY = 1
PLAYER_MOVEMENT_SPEED = 5
PLAYER_JUMP_SPEED = 20

PLATFORM_SCALING = 0.5

ENEMY_SCALING = 0.5
ENEMY_SPEED = 2


class MyGame(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        self.player_list = None
        self.platform_list = None
        self.enemy_list = None

        self.player_sprite = None

        self.physics_engine = None

    def setup(self):

        self.player_list = arcade.SpriteList()
        self.platform_list = arcade.SpriteList()
        self.enemy_list = arcade.SpriteList()

        self.player_sprite = arcade.AnimatedWalkingSprite()

        self.player_sprite.stand_right_textures = []
        self.player_sprite.stand_right_textures.append(arcade.load_texture("images/player_stand.png"))

        self.player_sprite.stand_left_textures = []
        self.player_sprite.stand_left_textures.append(arcade.load_texture("images/player_stand.png", mirrored=True))

        self.player_sprite.walk_right_textures = []

        self.player_sprite.walk_right_textures.append(arcade.load_texture("images/player_walk1.png"))
        self.player_sprite.walk_right_textures.append(arcade.load_texture("images/player_walk2.png"))

        self.player_sprite.walk_left_textures = []

        self.player_sprite.walk_left_textures.append(arcade.load_texture("images/player_walk1.png", mirrored=True))
        self.player_sprite.walk_left_textures.append(arcade.load_texture("images/player_walk2.png", mirrored=True))

        self.player_sprite.jump_right_textures = []
        self.player_sprite.jump_right_textures.append(arcade.load_texture("images/player_jump.png"))

        self.player_sprite.jump_left_textures = []
        self.player_sprite.jump_left_textures.append(arcade.load_texture("images/player_jump.png", mirrored=True))

        self.player_sprite.texture_change_distance = 20

        self.player_sprite.center_x = 64
        self.player_sprite.center_y = 96
        self.player_list.append(self.player_sprite)

        for x in range(0, SCREEN_WIDTH, 64):
            platform = arcade.Sprite("images/obstacle.png", PLATFORM_SCALING)
            platform.center_x = x
            platform.center_y = 32
            self.platform_list.append(platform)

            if random.randrange(5) == 0:
                enemy = arcade.Sprite("images/enemy.png", ENEMY_SCALING)
                enemy.bottom = platform.top
                enemy.center_x = platform.center_x
                enemy.change_x = ENEMY_SPEED * (random.random() * 2 - 1)
                enemy.boundary_right = platform.right - 10
                enemy.boundary_left = platform.left + 10
                enemy.change_x *= -1 if enemy.center_x > enemy.boundary_right else 1 if enemy.center_x < enemy.boundary_left else enemy.change_x
                self.enemy_list.append(enemy)

            if random.randrange(5) == 0:
                obstacle = arcade.Sprite("images/obstacle.png", PLATFORM_SCALING)
                obstacle.bottom = platform.top
                obstacle.center_x = platform.center_x + random.randint(-20,20)
                self.platform_list.append(obstacle)

        self.physics_engine = arcade.PhysicsEnginePlatformer(self.player_sprite,
                                                             self.platform_list,
                                                             GRAVITY)

    def on_draw(self):

        arcade.start_render()

        self.platform_list.draw()
        self.enemy_list.draw()
        self.player_list.draw()

    def on_key_press(self, key, modifiers):

        if key == arcade.key.UP:
            if self.physics_engine.can_jump():
                self.player_sprite.change_y = PLAYER_JUMP_SPEED
                if not (self.player_sprite.change_x == -PLAYER_MOVEMENT_SPEED or
                        self.player_sprite.change_x == PLAYER_MOVEMENT_SPEED):
                    if (self.player_sprite.character_face_direction == arcade.FACE_RIGHT):
                        self.player_sprite.texture = self.player_sprite.jump_right_textures[0]
                    else:
                        self.player_sprite.texture = self.player_sprite.jump_left_textures[0]
        elif key == arcade.key.LEFT:
            self.player_sprite.change_x = -PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.RIGHT:
            self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED

    def on_key_release(self, key, modifiers):

        if key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.player_sprite.change_x = 0

    def on_update(self, delta_time):

        self.physics_engine.update()

        self.player_list.update_animation()

        for enemy in self.enemy_list:
            if enemy.center_x >= enemy.boundary_right or enemy.center_x <= enemy.boundary_left:
                enemy.change_x *= -1

def main():
    window = MyGame()
    window.setup()
    arcade.run()

if __name__ == "__main__":
    main()