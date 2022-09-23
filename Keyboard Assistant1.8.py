import time
import socket
import threading
from pynput import keyboard
from pynput.keyboard import Key, Controller, KeyCode

# 用户自定义参数
need_reminder = True
gentle_reminder = False
reminder_myself = True

listen_key = Key.caps_lock
# listen_key = KeyCode.from_char('`')
press_key_number = 0
last_three_press_time = [0, 0, 0]
last_three_key_list = [0, 0, 0]
cur_time = 0
reminder_text = "as52d4f42awe54fg50a233e41rg6546az4d1v2"
online_text = "82722471_online"
online_user_num = 0
online_user_ip = {}
heart_beat_time = 15
PORT = 15247
test_model = False

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
s.bind(('', PORT))
network = '127.0.0.1' if test_model else '<broadcast>'


def listen_key_nblock():
    listener = keyboard.Listener(on_press=on_press)
    listener.start()  # 启动线程


def on_press(key):
    global listen_key
    global last_three_press_time
    global cur_time
    global network
    global reminder_text
    global last_three_key_list
    last_three_key_list.pop(0)
    last_three_key_list.append(key)
    if key == listen_key:
        last_three_press_time.pop(0)
        last_three_press_time.append(time.time())
        if last_three_press_time[2] - last_three_press_time[0] < 2 and last_three_key_list[0] == listen_key \
           and last_three_key_list[1] == listen_key and last_three_key_list[2] == listen_key:
            # 发送者，可以选择不切自己桌面
            if not reminder_myself:
                cur_time = time.time()
            s.sendto(reminder_text.encode('utf-8'), (network, PORT))
            print(get_format_time(), 'Send reminder to everyone.')
            # 重置按键信息
            last_three_press_time = [0, 0, 0]
            last_three_key_list = [0, 0, 0]


def heart_beat():
    global heart_beat_time
    global online_user_ip
    global online_user_num
    global online_text
    while True:
        cur_heart_beat_time = time.time()
        for ip in list(online_user_ip.keys()):
            if cur_heart_beat_time - online_user_ip[ip] > heart_beat_time + 5:
                del online_user_ip[ip]
        s.sendto(online_text.encode('utf-8'), (network, PORT))
        if len(online_user_ip) != online_user_num:
            online_user_num = len(online_user_ip)
            print(get_format_time(), "当前在线人数：", online_user_num)
            print("在线用户：", list(online_user_ip.keys()))
        time.sleep(heart_beat_time)


def get_format_time():
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))


if __name__ == "__main__":
    listen_key_nblock()
    t1 = threading.Thread(target=heart_beat)
    t1.start()
    while True:
        data, address = s.recvfrom(65535)
        recstr = data.decode('utf-8')
        if time.time() - cur_time > 5 and need_reminder and recstr == reminder_text:
            print(get_format_time(),
                  'Server received reminder from {}'.format(address))
            keyboardCtl = Controller()
            if gentle_reminder:
                keyboardCtl.press(Key.cmd)
                keyboardCtl.release(Key.cmd)
            else:
                keyboardCtl.release(Key.cmd)
                keyboardCtl.release(Key.ctrl_l)
                keyboardCtl.release("d")
                keyboardCtl.press(Key.cmd)
                keyboardCtl.press(Key.ctrl_l)
                keyboardCtl.press("d")
                keyboardCtl.release(Key.cmd)
                keyboardCtl.release(Key.ctrl_l)
                keyboardCtl.release("d")
            cur_time = time.time()
        if recstr == online_text:
            online_user_ip[address] = time.time()
