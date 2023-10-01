shader_type sky;
uniform sampler2D skyTexture;
void sky() {
	// Place sky code here.
	COLOR = texture(skyTexture, SKY_COORDS).rgb;
}
