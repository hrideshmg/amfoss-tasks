extends CharacterBody3D
class_name Player
var mouse_sensitivity := 0.005
var twist_input := 0.0
var pitch_input := 0.0

const SPEED = 5.0
const JUMP_HEIGHT := 1.4
const TIME_TO_PEAK := 0.35
const FRICTION := 0.8
var gravity: float
var JUMP_VELOCITY: float


func _ready():
	Input.set_mouse_mode(Input.MOUSE_MODE_CAPTURED)
	# Applying the equations for projectile motion to calculate gravity and initial velocity
	# h = 1/2*(g*t^2)
	gravity = (2*JUMP_HEIGHT)/pow(TIME_TO_PEAK, 2)
	# v = gt
	JUMP_VELOCITY = gravity * TIME_TO_PEAK

func _physics_process(delta):
	# Add the gravity if player is in the air
	if not is_on_floor():
		velocity.y -= gravity * delta
	
	# Handle Jump.
	if Input.is_action_just_pressed("jump") and is_on_floor():
		velocity.y = JUMP_VELOCITY

	# Get the input direction and handle the movement/deceleration.
	var input_dir = Input.get_vector("right", "left", "backward", "forward")
	var direction = Vector3(-input_dir.x, 0, -input_dir.y)

	direction = direction.rotated(Vector3.UP, $TwistPivot.rotation.y).normalized()
	if direction:
		$Model/AnimationPlayer.play("run")
		# Updates the rotation of the model
		$Model.rotation.y = ($TwistPivot.rotation.y)
		velocity.x = direction.x * SPEED
		velocity.z = direction.z * SPEED
	else:
		$Model/AnimationPlayer.play("IDLE")
		velocity.x = move_toward(velocity.x, 0, FRICTION)
		velocity.z = move_toward(velocity.z, 0, FRICTION)
		

	move_and_slide()
	# Rotates the camera based on mouse input
	$TwistPivot.rotate_y(twist_input)
	$TwistPivot/PitchPivot.rotate_x(pitch_input)
	$TwistPivot/PitchPivot.rotation.x = clamp($TwistPivot/PitchPivot.rotation.x, -0.45, 0.45)
	twist_input = 0
	pitch_input = 0
	
func _input(event: InputEvent):
	if event is InputEventMouseMotion:
		if Input.get_mouse_mode() == Input.MOUSE_MODE_CAPTURED:
			twist_input = - event.relative.x * mouse_sensitivity
			pitch_input = event.relative.y * mouse_sensitivity

func lock_movement():
	$Model/AnimationPlayer.play("IDLE")
	set_physics_process(false)
