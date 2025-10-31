// switchPin = 9
// pausePin = 10 Both are active HIGH
// leaveOn = 11
// leaveOn2 = 12

void setup() {
    Serial.begin(9600);
    pinMode(9, INPUT);
    pinMode(10, INPUT);
    pinMode(11, OUTPUT);
    pinMode(12, OUTPUT);
}

void loop() {
    if (digitalRead(10) == LOW) {
        char statement;

        if (digitalRead(9) == HIGH) {
            statement = 'True';
        } else {
            statement = 'False';
        }

        char reading = char(analogRead(A0));

        Serial.println((statement + ', ' + reading));
    }
    
    delay(200);
}