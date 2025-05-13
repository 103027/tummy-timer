const int trigPin = 2;  
const int echoPin = 3;

const int MIN_DISTANCE_CM = 5;   //minimum distance in cm
const int MAX_DISTANCE_CM = 40;  //maximum distance in cm

void setup() {
  Serial.begin(9600);
  
  delay(1000);
  
  // Set pin modes
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
}

void loop() {
  long duration;
  float distanceCm;
  
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
  
  duration = pulseIn(echoPin, HIGH);
  
  // Calculate the distance
  distanceCm = duration * 0.034 / 2;
  
  // Check distance
  if (distanceCm >= MIN_DISTANCE_CM && distanceCm <= MAX_DISTANCE_CM) {
    Serial.write('T');  // Send T for true
  } else {
    Serial.write('F');  // Send F for false
  }
 
  delay(100);
}