import pygame.display
from pynput import keyboard, mouse
from pynput.keyboard import Key
import time
import config

try:
    from pydub import AudioSegment
    from pydub.playback import play
except:
    pass

_record_string = ''
_record_move = False
_running = False
_include_time = True
_timer = 0
_keys = [Key.alt, Key.alt_l, Key.alt_r, Key.alt_gr, Key.backspace, Key.caps_lock, Key.cmd, Key.cmd_l, Key.cmd_r,
         Key.ctrl, Key.ctrl_l, Key.ctrl_r, Key.delete, Key.down, Key.end, Key.enter, Key.esc, Key.f1, Key.f2, Key.f3,
         Key.f4, Key.f5, Key.f6, Key.f7, Key.f8, Key.f9, Key.f10, Key.f11, Key.f12, Key.f13, Key.f14, Key.f15, Key.f16,
         Key.page_up, Key.right, Key.shift, Key.shift_l, Key.shift_r, Key.space, Key.tab, Key.up, Key.media_play_pause,
         Key.media_volume_mute, Key.media_volume_down, Key.media_volume_up, Key.media_previous, Key.media_next, Key.left]
try:
    _keys.append(Key.insert)
except:
    pass
try:
    _keys.append(Key.menu)
except:
    pass
try:
    _keys.append(Key.num_lock)
except:
    pass
try:
    _keys.append(Key.pause)
except:
    pass
try:
    _keys.append(Key.print_screen)
except:
    pass
try:
    _keys.append(Key.scroll_lock)
except:
    pass

key_names = ['alt', 'alt_l', 'alt_r', 'alt_gr', 'backspace', 'caps_lock', 'cmd', 'cmd_l', 'cmd_r', 'ctrl', 'ctrl_l',
             'ctrl_r', 'delete', 'down', 'end', 'enter', 'esc', 'f1', 'f2', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8', 'f9',
             'f10', 'f11', 'f12', 'f13', 'f14', 'f15', 'f16', 'page_up', 'right', 'shift', 'shift_l', 'shift_r',
             'space', 'tab', 'up', 'media_play_pause', 'media_volume_mute', 'media_volume_down', 'media_volume_up',
             'media_previous', 'media_next', 'insert', 'menu', 'num_lock', 'pause', 'print_screen', 'scroll_lock',
             'left']
_alphabet = 'abcdefghijklmnopqrstuvxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
try:
    _end_sound = AudioSegment.from_file('assets/sounds/end.wav')
    _split_sound = AudioSegment.from_file('assets/sounds/split.wav')
    _cancel_sound = AudioSegment.from_file('assets/sounds/cancel.mp3')
except:
    pass


def get_key_name(key):
    try:
        if key[0] == 'k':
            return key_names[_alphabet.index(key[1])]
        elif key[0] == 'c':
            return key[1]
        elif key[0] == 'v':
            return key[1:-1]
        else:
            return 'undefined'
    except:
        return 'undefined'


def _on_press(key):
    global _record_string
    if _include_time:
        _record_string += str(time.perf_counter_ns() // 1000000 - _timer) + ','
    else:
        _record_string += '0,'
    _record_string += 'p'
    if isinstance(key, keyboard.Key):
        _record_string += 'k' + _alphabet[_keys.index(key)]
    elif isinstance(key, keyboard.KeyCode):
        # if key.char is not None:
        #     _record_string += 'c' + key.char
        # else:
        _record_string += f'v{str(key.vk)},'
    else:
        print("Error: This key is not supported")


def _on_release(key):
    global _record_string
    if _include_time:
        _record_string += str(time.perf_counter_ns() // 1000000 - _timer) + ','
    else:
        _record_string += '0,'
    _record_string += 'r'
    if isinstance(key, keyboard.Key):
        _record_string += 'k' + _alphabet[_keys.index(key)]
    elif isinstance(key, keyboard.KeyCode):
        # if key.char is not None:
        #     _record_string += 'c' + key.char
        # else:
        _record_string += f'v{str(key.vk)},'
    else:
        print("Error: This key is not supported")


def _on_move(x, y):
    if _record_move:
        global _record_string
        if _include_time:
            _record_string += str(time.perf_counter_ns() // 1000000 - _timer) + ','
        else:
            _record_string += '0,'
        _record_string += 'm'
        _record_string += f'{x},{y},'
        # print(x, y)


def _on_click(x, y, button, pressed):
    global _record_string
    if _include_time:
        _record_string += str(time.perf_counter_ns() // 1000000 - _timer) + ','
    else:
        _record_string += '0,'
    if pressed:
        _record_string += 'P'
    else:
        _record_string += 'R'

    if button == mouse.Button.left:
        _record_string += 'l'
    elif button == mouse.Button.right:
        _record_string += 'r'
    elif button == mouse.Button.middle:
        _record_string += 'm'

    _record_string += f'{x},{y},'


def _on_scroll(x, y, dx, dy):
    global _record_string
    if _include_time:
        _record_string += str(time.perf_counter_ns() // 1000000 - _timer) + ','
    else:
        _record_string += '0,'
    if dy < 0:
        _record_string += 'd'
    elif dy > 0:
        _record_string += 'u'

    _record_string += f'{x},{y},'


def record(include_time=True, record_move=False):
    print('Recording started')
    pygame.display.iconify()
    global _record_string, _timer, _include_time, _record_move
    _record_string = ''
    _include_time = include_time
    _record_move = record_move

    _keyboard_listener = keyboard.Listener(
        on_press=_on_press,
        on_release=_on_release)

    _mouse_listener = mouse.Listener(
        on_click=_on_click,
        on_scroll=_on_scroll,
        on_move=_on_move)
    _keyboard_listener.start()
    _mouse_listener.start()
    _timer = time.perf_counter_ns() // 1000000
    while _record_string.endswith(config.end_key) is False:
        try:
            if _record_string.endswith('p'+config.save_key):
                play(_split_sound)
        except:
            pass
    _keyboard_listener.stop()
    _mouse_listener.stop()

    try:
        play(_end_sound)
    except:
        pass
    print('Recording ended')
    return _record_string


def record_key():
    global _record_string, _timer, _include_time, _record_move
    _record_string = ''
    _include_time = False
    _record_move = False

    _keyboard_listener = keyboard.Listener(
        on_press=_on_press,
        on_release=_on_release)
    _keyboard_listener.start()

    while True:
        if _record_string:
            if not _record_string.startswith('0,p'):
                _record_string = ''
            else:
                break
        time.sleep(0.1)
    _keyboard_listener.stop()
    print('Key Recorded')

    return _record_string[3:]


def simulate(simulate_string, speedup=1, use_mouse=True, include_sound=True):
    global _record_string
    _record_string = ''
    # simulate_string = re.sub(r'\d+,[pr]'+config.save_key, '', simulate_string)
    # simulate_string = re.sub(r'\d+,[pr]'+config.end_key, '', simulate_string)
    pygame.display.iconify()
    keyboard_controller = keyboard.Controller()
    mouse_controller = mouse.Controller()

    _keyboard_listener = keyboard.Listener(
        on_press=_on_press)
    _keyboard_listener.start()

    current_time = 0
    while simulate_string:
        if _record_string.endswith(config.cancel_key):
            _keyboard_listener.stop()
            try:
                play(_cancel_sound)
            except:
                pass
            return True
        t = int(simulate_string[:simulate_string.find(',')])
        simulate_string = simulate_string[simulate_string.find(',') + 1:]
        print(f'{current_time=} {t=}')
        time.sleep((t - current_time) / (1000*speedup))
        current_time = t

        try:
            if simulate_string.startswith('p'+config.save_key) and include_sound:
                play(_split_sound)
        except:
            pass

        type = simulate_string[0]
        simulate_string = simulate_string[1:]
        no_press = simulate_string.startswith(config.save_key) or simulate_string.startswith(config.end_key)
        if not type: break

        if type in 'pr':  # key press or release
            button = simulate_string[0]
            simulate_string = simulate_string[1:]
            if button == 'k':
                key = _keys[_alphabet.index(simulate_string[0])]
                simulate_string = simulate_string[1:]
            elif button == 'c':
                raise Exception('WHAT')
            elif button == 'v':
                key = keyboard.KeyCode.from_vk(int(simulate_string[:simulate_string.find(',')]))
                simulate_string = simulate_string[simulate_string.find(',') + 1:]
            else:
                continue

            if not no_press:
                if type == 'p':
                    keyboard_controller.press(key)
                elif type == 'r':
                    keyboard_controller.release(key)

        elif type == 'm':  # mouse move
            x = int(simulate_string[:simulate_string.find(',')])
            simulate_string = simulate_string[simulate_string.find(',') + 1:]
            y = int(simulate_string[:simulate_string.find(',')])
            simulate_string = simulate_string[simulate_string.find(',') + 1:]
            if use_mouse:
                mouse_controller.position = (x, y)

        elif type in 'PR':
            button = simulate_string[0]
            simulate_string = simulate_string[1:]
            if button == 'l':
                button = mouse.Button.left
            elif button == 'r':
                button = mouse.Button.right
            elif button == 'm':
                button = mouse.Button.middle

            x = int(simulate_string[:simulate_string.find(',')])
            simulate_string = simulate_string[simulate_string.find(',') + 1:]
            y = int(simulate_string[:simulate_string.find(',')])
            simulate_string = simulate_string[simulate_string.find(',') + 1:]
            mouse_controller.position = (x, y)
            if type == 'P':
                mouse_controller.press(button)
            elif type == 'R':
                mouse_controller.release(button)

        elif type in 'ud':  # mouse scroll
            x = int(simulate_string[:simulate_string.find(',')])
            simulate_string = simulate_string[simulate_string.find(',') + 1:]
            y = int(simulate_string[:simulate_string.find(',')])
            simulate_string = simulate_string[simulate_string.find(',') + 1:]
            mouse_controller.position = (x, y)
            if type == 'u':
                mouse_controller.scroll(0, -1)
            elif type == 'd':
                mouse_controller.scroll(0, 1)

        else:
            break
    try:
        if include_sound:
            play(_end_sound)
    except:
        pass
    _keyboard_listener.stop()
    print('Simulation ended')
    return False


def merge_recordings(*recordings, speedups=None, mouses=None):
    print('merge', recordings, speedups, mouses)
    result = ''
    last_time = 0
    if speedups is None:
        speedups = [1] * len(recordings)
    if mouses is None:
        mouses = [True] * len(recordings)
    for simulate_string, speedup, use_mouse in zip(recordings, speedups, mouses):
        current_time = 0
        while simulate_string:
            t = int(simulate_string[:simulate_string.find(',')])//speedup
            simulate_string = simulate_string[simulate_string.find(',') + 1:]
            current_time = t
            type = simulate_string[0]
            simulate_string = simulate_string[1:]
            if not type: break
            if type != 'm' or use_mouse:
                result += str(current_time + last_time) + ','
                result += type

            if type in 'pr':  # key press or release
                button = simulate_string[0]
                result += button
                simulate_string = simulate_string[1:]
                if button == 'k':
                    result += simulate_string[0]
                    simulate_string = simulate_string[1:]
                elif button == 'c':
                    result += simulate_string[0]
                    simulate_string = simulate_string[1:]
                elif button == 'v':
                    result += simulate_string[:simulate_string.find(',')+1]
                    simulate_string = simulate_string[simulate_string.find(',') + 1:]
                else:
                    continue

            elif type == 'm':  # mouse move
                x = int(simulate_string[:simulate_string.find(',')])
                simulate_string = simulate_string[simulate_string.find(',') + 1:]
                y = int(simulate_string[:simulate_string.find(',')])
                simulate_string = simulate_string[simulate_string.find(',') + 1:]
                if use_mouse:
                    result += f'{x},{y},'

            elif type in 'PR':
                button = simulate_string[0]
                result += button
                simulate_string = simulate_string[1:]

                x = int(simulate_string[:simulate_string.find(',')])
                simulate_string = simulate_string[simulate_string.find(',') + 1:]
                y = int(simulate_string[:simulate_string.find(',')])
                simulate_string = simulate_string[simulate_string.find(',') + 1:]
                result += f'{x},{y},'

            elif type in 'ud':  # mouse scroll
                x = int(simulate_string[:simulate_string.find(',')])
                simulate_string = simulate_string[simulate_string.find(',') + 1:]
                y = int(simulate_string[:simulate_string.find(',')])
                simulate_string = simulate_string[simulate_string.find(',') + 1:]
                result += f'{x},{y},'

            else:
                break
        last_time += current_time
    return result


def split_recording(recording, delimiter):
    recordings = recording.split('p' + delimiter)
    for i in range(len(recordings)):
        t = int(recordings[i][:recordings[i].find(',')])
        add = '' if i == len(recordings) - 1 else 'p' + delimiter
        recordings[i] = merge_recordings(str(-t) + ',p' + delimiter, recordings[i] + add)
        recordings[i] = recordings[i][recordings[i].find('p' + delimiter) + len(delimiter)+1:]
    return recordings
