extends Label
var time := 0.0

func _process(delta):
	time += delta
	self.text = str(snapped(time,0.01))
