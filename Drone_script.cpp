
#include <Servo.h>

// Hardware interface
Servo actuator;
int reading_delay = 1000;

// Recent Readings
int reading_t1;
int reading_t2;
int reading_t3;
int reading_t4;
int reading_t5;

// Logistic regression model (P(event) = ax + b)

float a = 0.012345502479605237;
float b = -9.889030577785928;
float threshold_probability = 0.8;

// Failsafe information
double threshold_reading = 500;
int failsafe_delay = 10000;

// Stack Functions
void populate_stack() {
    int v1 = analogRead(A0);
    int v2 = analogRead(A0);
    int v3 = analogRead(A0);
    int v4 = analogRead(A0);
    int v5 = analogRead(A0);

    reading_t1 = v1;
    reading_t2 = v2;
    reading_t3 = v3;
    reading_t4 = v4;
    reading_t5 = v5;
}
void update_stack(int reading) {
    reading_t5 = reading_t4;
    reading_t4 = reading_t3;
    reading_t3 = reading_t2;
    reading_t2 = reading_t1;
    reading_t1 = reading;
}
float stack_average() {
    int sum = reading_t1 + reading_t2 + reading_t3 + reading_t4 + reading_t5;

    return (float(sum)/5.0)
}

// Data handling functions
bool process_data(int data) {
    float P = float(data)*(a) + float(b);

    return (P >= threshold_probability);
}
bool failsafe(int input) {
    return (input >= threshold_reading)
}

void setup() {
    actuator.attach(10);
    actuator.write(180);

    populate_stack();
}

void loop() {

    int data = analogRead(A0);

    update_stack(data);
    processed_data = stack_average();

    bool decision = process_data(processed_data);

    if (decision) {
        bool safe_to_fire = failsafe(processed_data);

        if (safe_to_fire) {
            actuator.write(0);
            delay(5000);
            actuator.write(180)
            populate_stack();
        } else {
            delay(failsafe_delay);
            populate_stack();
        }
    }
    
    delay(reading_delay);
}




