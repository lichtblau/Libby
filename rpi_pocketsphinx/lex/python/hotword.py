from abc import ABCMeta
from os import getenv, path
from ctypes import cdll
import pyaudio
from pocketsphinx.pocketsphinx import Decoder

class TofSensor(object):
    __metaclass__ = ABCMeta
    THRESHOLD = 100

    def initialize(self):
        pass

    def get_distance(self):
        pass

class VL6180(TofSensor):
    LIBRARY = cdll.LoadLibrary('/usr/local/lib/libvl6180_pi.so')

    def initialize(self):
        self.sensor_handle = self.LIBRARY.vl6180_initialise(1)

    def get_distance(self):
        return self.LIBRARY.get_distance(sensor_handle)

class VL53L0X(TofSensor):
    LIBRARY = cdll.LoadLibrary('/build/sensor/libsensor.so')

    def initialize(self):
        self.LIBRARY.sensor_init()

    def get_distance(self):
        return self.LIBRARY.sensor_read() / 2

MODELDIR = "/rpi/lex/python/model/"
PATHDIR = "/rpi/lex/python/"
p = pyaudio.PyAudio()
# Create a decoder with certain model
config = Decoder.default_config()
config.set_string('-hmm', path.join(MODELDIR, 'en-us/'))
config.set_string('-dict', path.join(PATHDIR, '0963.dic'))
# config.set_string('-logfn', '/dev/null')
decoder = Decoder(config)

decoder.set_kws("kws", path.join(PATHDIR, 'keywords.txt'))
decoder.set_lm_file("lm", path.join(PATHDIR, '0963.lm'))
decoder.set_search("kws")

DEFAULT_SENSOR_NAME = 'VL6180'
sensor_name = getenv("TOF_SENSOR", DEFAULT_SENSOR_NAME)
sensor_class = {'VL53L0X': VL53L0X, 'VL6180': VL6180}.get(sensor_name)
sensor = sensor_class()
sensor.initialize()

def start(callback):
    # Decode streaming data.
    decoder.start_utt()
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000,
                    input=True, input_device_index=None,
                    frames_per_buffer=20480)
    stream.start_stream()

    while True:
        if(sensor.get_distance() < sensor.THRESHOLD):
            break;
        buf = stream.read(1024, exception_on_overflow=False)
        if buf:
            decoder.process_raw(buf, False, False)
        else:
            break
        if decoder.hyp() is not None:
            print("Found keyword")
            print(decoder.hyp().hypstr)
            break
    stream.stop_stream()
    stream.close()
    decoder.end_utt()
    callback()
