from pynput import keyboard,mouse
m_handler = mouse.Controller()
k_handler = keyboard.Controller()
m_handler.position = (700, 300)
m_handler.click(mouse.Button.left)
k_handler.press(keyboard.KeyCode.from_vk(49))
k_handler.release(keyboard.KeyCode.from_vk(49))
k_handler.press(keyboard.KeyCode.from_vk(13))
k_handler.release(keyboard.KeyCode.from_vk(13))

# print(chr('d'))111111111



# key = keyboard.KeyCode.from_vk(108)
# c = getattr(key, 'vk')1
print('+'.join(['1','2','3']))
try:
    int('yyy')
except ValueError:
    pass
