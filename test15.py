# 测试键盘键位的捕获和输入
from pynput import keyboard,mouse
m_handler = mouse.Controller()
k_handler = keyboard.Controller()
m_handler.position = (700, 300)
m_handler.click(mouse.Button.left)
# k_handler.press(keyboard.KeyCode.from_vk(49))
# k_handler.release(keyboard.KeyCode.from_vk(49))
# k_handler.press(keyboard.KeyCode.from_vk(13))
# k_handler.release(keyboard.KeyCode.from_vk(13))

# 111111111

a = [keyboard.Key.enter, keyboard.Key.alt]
b = [keyboard.Key.alt, keyboard.Key.enter]
print(a == b)
# key = keyboard.KeyCode.from_vk(108)
# c = getattr(key, 'vk')1
# print('+'.join(['1','2','3']))
try:
    int('yyy')
except ValueError:
    pass
