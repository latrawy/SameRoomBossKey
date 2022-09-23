# SameRoomBossKey(only Windows system)

同一个局域网内的老板键，只要当前局域网内有一个用户快速按下三次【Caps Lock】键（大小写键），则所有运行此程序的其他用户桌面都会被切换到一个新建的桌面中（Windows系统）。

程序源码在`Keyboard Assistant1.8.py`中，局域网内的用户通过socket通讯，可以得知当前多少用户在线。但是为了确保及时触发多用户的老板键，数据包采用广播方式发送。

源码相关参数：
- **need_reminder:** 是否需要被切桌面，False的话只触发别人自身不会被触发。
- **reminder_myself:** 是否需要让提醒人自身也切桌面。
- **listen_key:** 连续按三下触发老板键的键位。
- **reminder_text:** 提醒别人时发送的密文，因为采用的是广播，所以有必要采用唯一密文防止干扰。
- **online_text:** 心跳包对应的密文。

运行源码：
首先安装python相关的库，pynput是监听键盘的python库。

```bash
pip install -r requirements.txt
```

运行程序

```python
python Keyboard Assistant1.8.py
```


python文件导出exe可执行文件：

```bash
pip install pyinstaller
pyinstaller -F Keyboard Assistant1.8.py
```

