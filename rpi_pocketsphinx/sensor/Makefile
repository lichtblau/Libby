TARGET := libsensor.so

CFLAGS := -fPIC $(shell pkg-config --cflags vl53l0x)
LDFLAGS := -shared -fPIC $(shell pkg-config --libs vl53l0x)

all: $(TARGET)

$(TARGET): sensor.o
	gcc -o $@ $^ $(LDFLAGS) -lstdc++

%.o: %.cpp $(wildcard *.h)
	gcc -Wall -c -o $@ $< $(CFLAGS)

.PHONY: clean
clean:
	rm -f *.o $(TARGET)
