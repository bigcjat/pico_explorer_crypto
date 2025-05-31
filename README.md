# Pico W Crypto Price & Chart Dashboard

A MicroPython project for the Raspberry Pi Pico W and Pimoroni Pico Explorer Base that displays real-time cryptocurrency price information, a candlestick chart, and 5-minute interval volume for selected assets. Users can switch between different cryptocurrencies using the onboard buttons.

*(Suggestion: Add a photo of your project in action here!)*

## Features

- **Real-time Price Display:** Shows the current price of the selected cryptocurrency.
- **Candlestick Chart:** Displays a 5-minute interval candlestick chart for the selected asset, showing recent price action (Open, High, Low, Close).
- **Approximate Volume:** Shows the trading volume for the period covered by the chart.
- **Asset Switching:** Use the A, B, X, and Y buttons on the Pico Explorer Base to switch between pre-configured cryptocurrencies (XRP, BTC, ETH, JASMY by default).
- **Dynamic Price Color:** The current price text changes color to indicate if the price has gone up (green), down (red), or stayed the same (white) since the last update.
- **Automatic Refresh:** Data automatically refreshes every second (configurable).
- **Clear Visual Interface:** Uses the Pico Explorer's LCD screen with a clean, color-coded layout.

## Hardware Requirements

- Raspberry Pi Pico W
- Pimoroni Pico Explorer Base
- Micro USB cable for power and programming

## Software Requirements

- MicroPython firmware for the Raspberry Pi Pico W (Pimoroni's custom UF2 is recommended).
- Thonny IDE (or any other MicroPython-compatible IDE).
- The following MicroPython libraries (usually included in Pimoroni's firmware, but may need to be installed via Thonny's package manager if using standard MicroPython):
    - `urequests`
    - `ujson` (likely already included in the firmware)

## Setup & Installation

1.  **Flash MicroPython:**
    - Ensure your Raspberry Pi Pico W has MicroPython flashed. Pimoroni's custom UF2 file is recommended: [Pimoroni MicroPython Releases](https://github.com/pimoroni/pimoroni-pico/releases).
    - To flash, hold BOOTSEL on the Pico W while plugging it into your computer. Drag the UF2 file onto the `RPI-RP2` drive.

2.  **Connect Hardware:**
    - If not already done, solder headers to your Pico W.
    - Securely attach the Pico W to the Pimoroni Pico Explorer Base.

3.  **Install Libraries (if needed):**
    - Open Thonny IDE and connect to your Pico W.
    - If not using Pimoroni's custom firmware, you might need to install libraries. Go to **Tools > Manage Packages...**, search for `micropython-urequests` and `micropython-ujson`, and install them.

4.  **Configure WiFi Credentials:**
    - Open the `main.py` script in Thonny.
    - Update `WIFI_SSID` and `WIFI_PASSWORD` with your network details.

5.  **Upload Code:**
    - Save the `main.py` script to your Raspberry Pi Pico W. It will run automatically on boot.

## How to Use

1.  **Power On:** Connect the Pico W to USB power.
2.  **Initial Connection:** The screen shows "Connecting...".
3.  **Select Asset:** Then "Press A,B,X,Y".
    - **Button A (Pin 12):** Asset 1 (default: XRP)
    - **Button B (Pin 13):** Asset 2 (default: BTC)
    - **Button X (Pin 14):** Asset 3 (default: ETH)
    - **Button Y (Pin 15):** Asset 4 (default: JASMY)
4.  **View Data:** The screen displays the chart, price, and volume.
5.  **Automatic Refresh:** Data refreshes per `CRYPTO_REFRESH_INTERVAL`. A countdown is shown.
6.  **Switching Assets:** Press a different button at any time.

## Customizing Assets

Edit the `ASSETS` list in `main.py`:

    ASSETS = [
        {"name": "XRP", "symbol": "XRPUSDT", "price_format": "${:.4f}"},
        {"name": "BTC", "symbol": "BTCUSDT", "price_format": "${:.2f}"}, 
        {"name": "ETH", "symbol": "ETHUSDT", "price_format": "${:.2f}"}, 
        {"name": "JASMY", "symbol": "JASMYUSDT", "price_format": "${:.6f}"}
    ]

- `name`: Display name.
- `symbol`: Binance API symbol (e.g., "XRPUSDT").
- `price_format`: Python f-string for price display.

## Code Structure Overview

- **Configuration:** WiFi, API settings, asset definitions.
- **Initialization:** Display, pens (colors), buttons.
- **API/Network Functions:** `connect_wifi()`, `get_market_data()`.
- **Display Functions:** Formatting, status messages, chart drawing, main dashboard drawing, countdown timer.
- **Main Program Loop:** Handles WiFi, initial asset selection, button inputs, periodic data refresh, and screen updates.

## Troubleshooting

- **"WiFi Failed!"**: Check SSID/password, 2.4GHz network.
- **"API Error" / "N/A" data**: Check internet, asset symbols in `ASSETS`, or try increasing `CRYPTO_REFRESH_INTERVAL`.
- **Buttons not working**: Verify pin numbers in the script (12, 13, 14, 15) match your board if it's not a standard Pico Explorer, and check soldering/seating.
- **Crashes**: Ensure all necessary libraries (`urequests`, `ujson`) are present if not using Pimoroni's UF2. Check REPL in Thonny for specific error messages.
- **ujson**: If this library wont install, it's likely already included in the firmware you have installed.
