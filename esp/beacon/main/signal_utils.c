#include "signal_utils.h"
#include <math.h>

float compute_coefficient(signal_emitter_t* signal_emitter, float x, float y, float measured_power) {
    float x_diff = x - signal_emitter->x;
    float y_diff = y - signal_emitter->y;
    int base_power = signal_emitter->signal->base_power;
    float real_distance = sqrt((x_diff * x_diff) + (y_diff * y_diff));
    return ((base_power - measured_power)/(10*log10(real_distance)));

}
