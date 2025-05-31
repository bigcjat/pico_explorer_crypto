Pico W Crypto Price & Chart Dashboard
A MicroPython project for the Raspberry Pi Pico W and Pimoroni Pico Explorer Base that displays real-time cryptocurrency price information, a candlestick chart, and 5-minute interval volume for selected assets. Users can switch between different cryptocurrencies using the onboard buttons.


(Suggestion: Replace the placeholder above with an actual photo of your project in action!)

Features
Real-time Price Display: Shows the current price of the selected cryptocurrency.

Candlestick Chart: Displays a 5-minute interval candlestick chart for the selected asset, showing recent price action (Open, High, Low, Close).

Approximate Volume: Shows the trading volume for the period covered by the chart.

Asset Switching: Use the A, B, X, and Y buttons on the Pico Explorer Base to switch between pre-configured cryptocurrencies (XRP, BTC, ETH, JASMY by default).

Dynamic Price Color: The current price text changes color to indicate if the price has gone up (green), down (red), or stayed the same (white) since the last update.

Automatic Refresh: Data automatically refreshes every 30 seconds (configurable).

Clear Visual Interface: Uses the Pico Explorer's LCD screen with a clean, color-coded layout.

Hardware Requirements
Raspberry Pi Pico W

Pimoroni Pico Explorer Base

Micro USB cable for power and programming

Software Requirements
MicroPython firmware for the Raspberry Pi Pico W (Pimoroni's custom UF2 is recommended as it includes necessary libraries).

Thonny IDE (or any other MicroPython-compatible IDE) for uploading code to the Pico W.

The following MicroPython libraries (usually included in Pimoroni's firmware, but may need to be installed via Thonny's package manager if using standard MicroPython):

urequests (for making HTTP API calls)

ujson (for parsing JSON API responses)

Setup & Installation
Flash MicroPython:

Ensure your Raspberry Pi Pico W has MicroPython flashed. It's highly recommended to use the custom Pimoroni MicroPython UF2 file, as it often includes necessary drivers and libraries.

To flash, hold the BOOTSEL button on the Pico W while plugging it into your computer. It will appear as a USB drive. Drag the UF2 file onto this drive. The Pico W will reboot.

Connect Hardware:

If not already done, solder headers to your Pico W.

Securely attach the Pico W to the Pimoroni Pico Explorer Base.

Install Libraries (if needed):

Open Thonny IDE.

Connect to your Pico W (Interpreter set to "MicroPython (Raspberry Pi Pico)").

If you are not using Pimoroni's custom firmware, you might need to install urequests and ujson. Go to Tools > Manage Packages..., search for micropython-urequests and micropython-ujson, and install them.

Configure WiFi Credentials:

Open the main.py script in Thonny.

Locate the "CONFIGURE YOUR DETAILS HERE" section at the top of the script.

Update the WIFI_SSID and WIFI_PASSWORD variables with your Wi-Fi network name and password:

WIFI_SSID = "SSID-HERE"
WIFI_PASSWORD = "PASSWORD-HERE"

Upload Code:

Save the main.py script to your Raspberry Pi Pico W. If you save it as main.py, it will run automatically when the Pico W is powered on.

How to Use
Power On: Connect the Pico W (attached to the Explorer Base) to a USB power source.

Initial Connection: The screen will display "Connecting..." while it connects to your Wi-Fi network.

Select Asset: Once connected, it will display "Press A,B,X,Y".

Button A (Pin 12): Selects the first asset in the ASSETS list (default: XRP).

Button B (Pin 13): Selects the second asset (default: BTC).

Button X (Pin 14): Selects the third asset (default: ETH).

Button Y (Pin 15): Selects the fourth asset (default: JASMY).

View Data: The screen will display the candlestick chart, current price, and volume for the selected asset.

Automatic Refresh: The data for the currently displayed asset will refresh automatically every 30 seconds (or as configured by CRYPTO_REFRESH_INTERVAL). A countdown timer is shown at the bottom of the screen.

Switching Assets: You can press a different button at any time to switch to
