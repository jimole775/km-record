from pynput import keyboard,mouse
m_handler = mouse.Controller()
k_handler = keyboard.Controller()
m_handler.position = (500, 100)
m_handler.click(mouse.Button.left)
# k_handler.press(keyboard.KeyCode.from_vk(49))
# k_handler.release(keyboard.KeyCode.from_vk(49))

print(keyboard.Key['ctrl'])
try:
    int('yyy')
except ValueError:
    pass
