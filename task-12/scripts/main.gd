extends Node3D
class_name Game
@export var treasure_chest: Area3D
@export var ui: UI
@export var player: Player
var game_over := false

func _ready():
	# Connects the body entered signal of the treasure chest to the display win screen function
	if !treasure_chest.body_entered.is_connected(_game_over):
		treasure_chest.body_entered.connect(_game_over)


func _process(delta):
	# Restarts the game on keypress if game is over
	if game_over:
		if Input.is_action_pressed("restart"):
			get_tree().reload_current_scene()
			
	if Input.is_action_pressed("ui_cancel"):
		Input.set_mouse_mode(Input.MOUSE_MODE_VISIBLE)
	if Input.is_action_pressed("ui_accept"):
		Input.set_mouse_mode(Input.MOUSE_MODE_CAPTURED)

func _game_over(body):
	game_over = true
	player.lock_movement()
	ui.display_win_screen()
