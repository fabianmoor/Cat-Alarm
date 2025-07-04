# Cat Alarm IoT Device
* Fabian Moor Pucar (fm222wi)
* Guided assembly: 5-7 hours
* Total project time: aprox. 100 hours

![Roll Counter](http://pi.fabbemhome.org/rick-roll-counter.png)

## Short project description
This project addresses an unwanted feline bathroom behavior through IoT technology. The Cat Alarm is a smart deterrent device that utilizes dual piezo buzzers to create an effective sound barrier, discouraging cats from using inappropriate bathroom locations like showers. The system combines hardware sensors with programmable logic to provide an automated, humane solution for pet behavior modification.

**Requirements**:
- WiFi
- Ubidots account

## Objective
This project was conceived after observing our cat "Gubben" consistently using the shower as an alternative bathroom facility. While preferable to furniture, this behavior created unpleasant odors and hygiene concerns. 

**Why I chose this project:**
- Addresses a real-world pet behavior problem
- Combines IoT principles with practical home automation
- Demonstrates sensor integration and automated response systems

**Purpose it serves:**
- Provides humane pet behavior modification
- Automates deterrent response without human intervention
- Creates a reusable solution for similar behavioral issues

**Insights expected:**
- Understanding of sound-based deterrent effectiveness
- Learning IoT sensor integration and response timing
- Exploring automated behavior modification through technology
- Insights into pet behavior. For instance, how many times he thinks I'm not looking at him, and how many times he actually uses the shower as a bathroom.

## List of material

All components needed for this project are readily available and affordable. Here's what you'll need:

| Component | Purpose | Specifications | Cost (SEK) |
|-----------|---------|----------------|----------------|
| Raspberry Pi Pico WH | Main microcontroller | WiFi enabled | 99:-  |
| HC-SR04 Ultrasonic Sensor | Distance detection | 3-5V operating voltage | 59:-  |
| Active Piezo Buzzer | Steady tone generation | 3-5V operating voltage | 32:-  |
| Passive Piezo Buzzer | Variable frequency tones | 3-5V operating voltage | 29:-  |
| Push Button | Manual trigger/testing | Momentary switch | 19:-  |
| Breadboard | Circuit assembly | Half-size, 400 tie points | 49:-  |
| Jumper Cables | Connections | Male-Male (8x), Female-Male (7x) | 40:-  |

**Total estimated cost: 320 <-> 340 SEK**

The Raspberry Pi Pico WH serves as the brain of the operation, providing GPIO pins for sensor input and buzzer control, plus WiFi capability for future enhancements. The dual buzzer setup creates a more effective deterrent by combining steady and variable tones.

*[Component photos. Press images for links]*


<a href="https://www.electrokit.com/raspberry-pi-pico-wh">
    <img src="./img/pico.jpg" alt="Pico" height="250" width="300">
</a>
<a href="https://www.electrokit.com/avstandsmatare-ultraljud-hc-sr04-2-400cm">
    <img src="./img/hc-sr04.jpg" alt="HC-SR04 Ultrasonic Sensor" height="250" width="300">
</a>
<br>
<a href="https://www.electrokit.com/piezohogtalare-aktiv">
    <img src="./img/activepiezo.jpg" alt="Active Piezo" height="250" width="300">
</a>
<a href="https://www.electrokit.com/piezohogtalare-passiv">
    <img src="./img/passivepiezo.jpg" alt="Passive Piezo" height="250" width="300">
</a>
<br>
<a href="https://www.electrokit.com/tryckknapp-momentan">
    <img src="./img/knapp.jpg" alt="Button" height="250" width="300">
<a href="https://www.electrokit.com/labbsladd-20-pin-15cm-hane/hane">
    <img src="./img/jumper.jpg" alt="Jumper Cables" height="250" width="300">
</a>
<br>
<a href="https://www.electrokit.com/labbsladd-20-pin-15cm-hona/hane">
    <img src="./img/jumper.jpg" alt="Jumper Cables" height="250" width="300">
</a>
<a href="https://www.electrokit.com/kopplingsdack-400-anslutningar">
    <img src="./img/breadboard.jpg" alt="BreadBoard" height="250" width="300">
</a>

## Computer setup

### Development Environment Setup

**Fill out the secrets in config_temp.py and rename it to config.py**

```python
# config.py
SSID = "WIFI NAME"
PASSWORD = "WIFI PASSWORD"
TOKEN = "UBIDOTS TOKEN"
UBIDOTS_BASE_URL = "https://industrial.api.ubidots.com/api/v1.6/devices/"
DEVICE_LABEL = "DEVICE LABEL"
VARIABLE_LABEL = "VARIABLE NAME"
VARIABLE_LABEL_2 = "VARIABLE NAME 2"

LED_PIN = "LED"
PUSH_BUTTON_PIN = 18

TONES = {
    "E5": 659,
    "E6": 1319,
}

TOGGLE_INTERVAL_MS = 50

MAX_WIFI_ATTEMPTS = 20
ULTRASONIC_TIMEOUT_US = 25000
```

**IDE:** NeoVim  
**Microcontroller:** Raspberry Pi Pico WH  
**Programming Language:** MicroPython  

**Libraries used:**
- `machine` - GPIO control and hardware interfaces
- `time` - Timing functions for delays
- `network` - WiFi connection management
- `urequests` - HTTP requests for Ubidots API communication
- `ujson` - JSON handling for data formatting

**Setup steps:**
1. Flash MicroPython firmware on Raspberry Pi Pico WH
   - Download the latest MicroPython firmware from the [official website](https://micropython.org/download/rp2-pico-w/)
   - Connect the Pico WH to your computer while holding the BOOTSEL button
   - Copy the firmware file to the Pico's mounted drive
2. Configure NeoVim with MicroPython support
    - Install the `nvim-micropython` plugin for NeoVim
3. Set up file transfer method (ampy or Thonny)
   - Use `ampy` to transfer files to the Pico WH
    - Install `ampy` via pip: `pip install adafruit-ampy`

**Code Upload Workflow:**
1. Write code in NeoVim with MicroPython syntax highlighting
2. Transfer files to Pico WH using ampy: `ampy --port /dev/ttyACM0 put main.py`
- **For Mac** use: `ampy --port /dev/tty.usbmodem* put main.py`
3. Reset the device to run the new code
4. Monitor output via serial connection: `screen /dev/ttyACM0 115200`

**Additional Requirements:**
- Python 3.x installed on development machine
- USB drivers for Raspberry Pi Pico (usually automatic on macOS)
- Serial terminal software for debugging (screen, minicom, or similar)

## Putting everything together

### Pin Connections:
* **Ultra Sonic Sensor**
    - VCC → Power Rail (3.3V)
    - GND → GND Rail
    - Trigger (T) → GPIO Pin 20
    - Echo (E) → GPIO Pin 21

* **Active Piezo Buzzer:**
  - Signal (S) → GPIO Pin 27
  - Negative (-) → GND Rail

* **Passive Piezo Buzzer:**
  - Signal (S) → GPIO Pin 26
  - Negative (-) → GND Rail

* **Button:**
  - Positive (+) -> Power Rail (3.3V)
  - Signal (S) → GPIO Pin 18
  - Negative (-) → GND Rail

* **Optional Jumpers:**
  - 3.3V to Power Rail
  - GND to GND Rail

### Assembly:
Follow the pin connections to wire the components on a breadboard.
Either by the Pin Connections above or the Circuit Diagram below.

*[Circuit diagram and connection photo]*
<img src="./img/Circuit ScreenShot.jpg" alt="BreadBoard" height="550" width="900">
<br>

I did not make use of any resistors, as the components are designed to work with the Pico's GPIO pins directly.
However, if you want to be extra careful, you can add a 1kΩ resistor in series with the button to limit current flow.

**Electrical Considerations:**
- All components operate at 3.3V, matching the Pico's GPIO output voltage
- Current consumption: HC-SR04 (~15mA), Active Buzzer (~30mA), Passive Buzzer (~20mA)
- Total system current draw: approximately 65-70mA during alarm activation
- This setup is suitable for development and prototyping; for production use, consider adding proper pull-up/pull-down resistors and decoupling capacitors

## Platform

### Platform Selection
I chose **Ubidots** as my IoT platform for several key reasons:

**Functionality:**
- RESTful API for easy HTTP-based data transmission
- Real-time dashboard visualization
- Free tier suitable for small-scale projects (up to 3 devices, 4000 dots/month)
- Built-in analytics and data aggregation features

**Why Ubidots over alternatives:**
- **vs ThingSpeak**: Better visualization options and more intuitive dashboard creation
- **vs AWS IoT Core**: Simpler setup without complex authentication protocols
- **vs Blynk**: More robust for data logging and historical analysis
- **vs Local solution**: Cloud-based ensures data persistence and remote access

**Scaling considerations:**
- Free tier: Suitable for personal/prototype use
- Industrial tier ($20/month): Supports unlimited devices and data points
- Enterprise options available for commercial deployment
- API-first design allows easy migration to custom solutions if needed

## The code

I decided to separate the code into multiple files for better organization. 
The main files are:
- `main.py`: Main program logic with button handling, sensor monitoring, and system control
- `ubidots_client.py`: Ubidots client for data transmission with connection warm-up and retry logic
- `config.py`: Configuration settings including pin assignments, network credentials, and tone frequencies
- `network_manager.py`: Network management functions with WiFi connection handling and bootsel button exit
- `sensors.py`: Sensor handling, featuring the ultrasonic sensor for distance detection with timeout protection
- `actuators.py`: Actuator control, including active/passive buzzers with timer-based tone switching and LED classes

I chose to use classes for the actuators and sensors to encapsulate their functionality 
and make the code more modular. This allows for easier expansion in the future, such 
as adding more sensors or actuators without cluttering the main logic.

The sleep mode functionality has been implemented as a simple loop that waits for button 
press to wake up, rather than using deep sleep mode to avoid USB connection issues during 
development. The system properly shuts down all components when entering sleep mode and 
reactivates them when waking up.

### How It Works

The system operates through a main event loop that monitors button presses and sensor 
readings. When activated, the ultrasonic sensor continuously measures distance every 
50ms. If an object is detected within 20cm, both buzzers activate - the active buzzer 
provides a steady tone while the passive buzzer alternates between E5 (659Hz) and E6 
(1319Hz) frequencies every 50ms using a timer-based approach. Simultaneously, the system 
sends activation data to Ubidots for remote monitoring with a 5-second cooldown to prevent 
API spam. The onboard LED indicates system status, and button handling supports single 
press (toggle sensor) and double press (sleep mode). The sleep mode properly shuts down 
all components and waits for a button press to wake up.

### Code Snippet

Each run we begin by connecting to the WiFi network, if it fails, we exit the program.
This is handled by the network_manager.

```python
# main.py
# Initialize network connection
print("Connecting to WiFi...")
if connect() is None:
    print("ERROR: WiFi connection failed, exiting")
    sys.exit()
```

We then initialize the Ubidots client which is responsible for sending our data to Ubidots.

```python
# Initialize Ubidots client
print("Initializing Ubidots client...")
ubidots_client = UbidotsClient()
```

Initialize the sensors and actuators, which are responsible for reading the distance and
activating the buzzers.

```python
# Initialize hardware components
print("Initializing hardware components...")
ultrasonic_sensor = UltrasonicSensor(trigger_pin=20, echo_pin=21)
active_buzzer = ActiveBuzzer(pin=27)
passive_buzzer = PassiveBuzzer(pin=26)
onboard_led = LED(pin=LED_PIN)
push_button = Pin(PUSH_BUTTON_PIN, Pin.IN, Pin.PULL_UP)
```

### Main Loop
The main loop constantly checks the button state. If pressed once, it toggles the sensor state on or off.
If pressed twice (within a second), it puts the device into sleep mode.
When the sensor is active, it reads the distance every 50ms to be quick to respond.
When the distance is less than 20cm, it activates the buzzers and sends an activation event to Ubidots.
If the sensor is inactive, the buzzers and LED are turned off, and no data is sent to Ubidots.

## Transmitting the data / connectivity

### Data Transmission Details

**Transmission Frequency:**
- Activation events: Sent immediately when alarm triggers (with 5-second cooldown)
- Distance measurements: Logged every 50ms locally, transmitted only during activations
- No continuous polling to preserve battery and reduce API calls

**Wireless Protocol:**
- **WiFi (802.11 b/g/n)**: Chosen for reliable indoor coverage and high data throughput
- Range: ~30-50 meters indoors (sufficient for home use)
- Power consumption: ~70mA during transmission (acceptable for USB-powered device)

**Transport Protocol:**
- **HTTP/HTTPS**: RESTful API calls to Ubidots endpoints
- **JSON payload**: Structured data format for easy parsing
- **POST requests**: Sending sensor data and activation events

**Design Choice Rationale:**
- **WiFi vs LoRaWAN**: WiFi chosen for indoor use with existing home network infrastructure
- **HTTP vs MQTT**: HTTP selected for simplicity and Ubidots compatibility
- **Security**: HTTPS ensures encrypted data transmission
- **Battery impact**: USB power eliminates battery concerns, allowing frequent transmissions

**Data Structure:**
```json
{
  "activation": 1,
  "distance": 15.2,
  "timestamp": 1625097600
}
```

For monitoring, I used Ubidots to visualize the data via HTTP requests. 
I chose Ubidots cause I'm pretty familair with HTTP requests from building scrapers
in python. Worked a lot with flask api's, so Ubidots felt the most natural to me.
The system sends activation events in the form of a value of 1 to the variable. This allows me to track how many times the 
alarm has been triggered and how often the cat attempts to use the shower.

In order to truly understand how to visualize the data, I added a graph that contains
at which distance the alarm has been triggered. This helps me understand if the cat at 
some point got used to the sound and starts to investigate it more closely. 

## Presenting the data

### Dashboard Visualization
The Ubidots dashboard provides real-time visualization of the Cat Alarm's activity:

<img src="./img/ubidots.png" alt="Ubidots Dashboard" height="400">

**Dashboard Features:**
- **Activation Counter**: Displays total number of times the alarm has been triggered
- **Distance Graph**: Shows the distance measurements when alarm activates
- **Real-time Updates**: Data refreshes automatically when new events occur
- **Historical Data**: Maintains logs for trend analysis over time

**Data Storage:**
- **Database**: Ubidots cloud database stores all sensor data
- **Frequency**: Data is saved immediately upon alarm activation (with 5-second cooldown)
- **Retention**: Free tier provides 1 month of data history
- **Format**: JSON format with timestamp, activation status, and distance measurements

**Automation Features:**
- **Triggers**: Could be configured to send email/SMS alerts when activation threshold is exceeded
- **Webhooks**: Available for integration with other services (IFTTT, Zapier)
- **API Access**: RESTful API allows custom applications to access data

### iOS App
I created a simple iOS app using SwiftUI to visualize the activity from Ubidots. The app
displays the total number of times the alarm has been triggered, providing a quick 
overview of the system's effectiveness. The app is designed to be user-friendly 
and responsive, allowing easy access to the data without needing to log into the 
Ubidots web interface.

I also made it possible to reset the counter from the app. This was a little hacky, as I 
had to make a request where I send the variable the negative value of the current counter.

Because it's just a simple summation of all values sent to the variable.
32 + (-32) = 0. This wasn't that big of an issue as I only intend
to track the number of times the alarm has been triggered. I don't intend to track it 
over time. So resetting it is fine.

The app is built with SwiftUI, making it compatible with iOS devices. It fetches data
via the Ubidots API and displays it in a clean, intuitive interface.

### Screenshot
*[Screenshot of application]*

### I don't have a paid Apple Developer account for the App Store but click the app icon to view the app on the Google Play Store.

<!-- <img src="./img/realIcon.icon/Assets/icon.png"  height="400"> -->

<a href="https://pi.fabbemhome.org/track-rickroll">
    <img src="./img/realIcon.icon/Assets/icon.png" height="400">
</a>

<img src="./img/iphone.png" alt="BreadBoard" height="800">
<br>

## Finalizing the design

### Final Results
The Cat Alarm project successfully achieved its primary objective of deterring unwanted feline bathroom behavior through automated IoT technology. The system demonstrates reliable operation with consistent sensor readings and effective sound-based deterrents.

**Project Outcomes:**
- Successfully detects cat presence within 20cm range
- Dual buzzer system provides effective deterrent without being harmful
- Real-time data transmission to Ubidots for monitoring
- iOS app provides convenient access to activation statistics
- Modular code design allows for future enhancements

**What Worked Well:**
- Ultrasonic sensor provides accurate distance measurements
- Dual buzzer approach creates more effective deterrent than single tone
- WiFi connectivity enables remote monitoring capabilities
- Ubidots platform offers excellent visualization tools
- MicroPython on Pico WH provides stable, reliable operation

**Areas for Improvement:**
- **Power Management**: Could implement deep sleep mode for battery operation
- **Enclosure**: Currently breadboard-based; production would need weatherproof housing
- **Sensitivity Adjustment**: Could add potentiometer for adjustable trigger distance
- **Multiple Zones**: Could expand to monitor multiple areas simultaneously
- **Machine Learning**: Could implement pattern recognition to distinguish between cat and other objects

**Alternative Approaches:**
- **PIR Motion Sensor**: Could use instead of ultrasonic for different detection pattern
- **Camera-based**: Computer vision could provide more accurate cat identification
- **MQTT Protocol**: Might offer better real-time performance than HTTP
- **Local Processing**: Edge computing could reduce cloud dependency

**Production Considerations:**
- Add proper PCB design with surface-mount components
- Implement proper power management and battery backup
- Include weatherproof enclosure for bathroom environment
- Add configuration interface for sensitivity adjustments
- Implement over-the-air (OTA) update capability

<img src="./img/irlimg.png" alt="Cat Alarm Final Setup" height="400">

The project successfully demonstrates the practical application of IoT technology to solve real-world problems, combining hardware sensors, cloud connectivity, and mobile applications into a cohesive solution.

