import threading
import io
import pyaudio

is_playing = False
thread = None


def play(np_array, sampling_rate):
    global is_playing
    global thread

    if is_playing:
        stop()
    bytesio = io.BytesIO(np_array)

    is_playing = True
    thread = threading.Thread(target=lambda: play_thread(bytesio, sampling_rate))
    thread.start()


def stop():
    global is_playing
    global thread

    if is_playing:
        is_playing = False
        thread.join()


def play_thread(bytesio, sampling_rate):
    global is_playing
    chunk = 1024
    p = pyaudio.PyAudio()

    stream = p.open(
        format=p.get_format_from_width(2),
        channels=1,
        rate=sampling_rate,
        output=True)

    while is_playing:
        data = bytesio.read(chunk)
        if data == '':
            break
        stream.write(data)

    stream.stop_stream()
    stream.close()
    p.terminate()
