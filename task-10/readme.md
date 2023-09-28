## RuskOS
### Summary
First thing i did was create a config.toml file for cargo, in which i instructed cargo to recompile the core library and its dependency: compiler_builtins. I did this because the core library is implicitly linked to all no_std crates but since we are using a custom target, it is not available as a precompiled library.

Next i noticed that cargo could not find memcpy so i enabled it in config.toml. It's disabled by default so as to not clash with the memcpy from the precompiled C library

I observed that the background color was already set to black in vga_buffer.rs however the the color code given to black in the Color Enum actually corresponded to red, i fixed it by merely swapping the codes for black and red.

The keyboard port was already set to 0x60 (96) so no change was necessary

As for the reversed character input, i noticed that the add_character() function defined in interrupts.rs was responsible for adding characters to the character array, upong inspecting the code, it appeared that the index was being updated from 5->0 (in reverse). After modifying the code to make it 0->5, it works as expected.
### Conclusion
To be honest, a lot of the things flew over my head when i was reading the guide to make a rust kernel, like the fields for the target specification or how exactly the VGA buffer works, but despite that i was able to learn a fair bit about the boot process and kernel development, i would love to read more about this topic.

PS: I caught that sneaky reference to Youjo Senki btw :p
