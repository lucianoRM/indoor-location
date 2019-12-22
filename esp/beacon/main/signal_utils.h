#ifndef BEACON_SIGNAL_UTILS_H
#define BEACON_SIGNAL_UTILS_H

#include "parser.h"

/**
 * Given the current measurements, compute the medium coefficient
 * @param signal_emitter
 * @param x
 * @param y
 * @param measured_power
 * @return
 */
float compute_coefficient(signal_emitter_t* signal_emitter, float x, float y, float measured_power);

#endif //BEACON_SIGNAL_UTILS_H
