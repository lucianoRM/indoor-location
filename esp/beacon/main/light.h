#ifndef BEACON_LIGHT_H
#define BEACON_LIGHT_H

/**
 * Turn on the light
 */
void turn_on_led();

/**
 * Turn off the light
 */
void turn_off_led();

/**
 * start blinking
 */
void start_blinking_led();

/**
 * stop blinking
 */
void stop_blinking_led();

void set_burst_mode_led(int burst_length, long delay);

void set_blink_mode_led(long delay);

#endif //BEACON_LIGHT_H
