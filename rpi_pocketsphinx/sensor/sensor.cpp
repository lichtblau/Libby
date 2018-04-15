#include "sensor.h"
#include <VL53L0X.hpp>

static VL53L0X sensor;

void sensor_init() {
    sensor.init();
    sensor.setTimeout(200);
}

uint16_t sensor_read() {
    return sensor.readRangeSingleMillimeters();
}
