import network
import urequests
import ujson
import time
from picographics import PicoGraphics, DISPLAY_PICO_EXPLORER
import machine # For direct GPIO access for buttons

# --- CONFIGURE YOUR DETAILS HERE ---

WIFI_SSID = "SSID-HERE"
WIFI_PASSWORD = "PASSWORD-HERE"
CRYPTO_REFRESH_INTERVAL = 1
CHART_HISTORY_POINTS = 40 

# --- NEW: ASSET CONFIGURATION ---
ASSETS = [
    {"name": "XRP", "symbol": "XRPUSDT", "price_format": "${:.4f}"},
    {"name": "BTC", "symbol": "BTCUSDT", "price_format": "${:.2f}"}, 
    {"name": "ETH", "symbol": "ETHUSDT", "price_format": "${:.2f}"}, 
    {"name": "JASMY", "symbol": "JASMYUSDT", "price_format": "${:.6f}"}
]

# --- END OF CONFIGURATION ---


# --- INITIALIZE DISPLAY AND PENS ---
display = PicoGraphics(display=DISPLAY_PICO_EXPLORER)
WIDTH, HEIGHT = display.get_bounds()
BG_COLOR = display.create_pen(10, 20, 40)
TITLE_COLOR = display.create_pen(200, 200, 200)
VOLUME_COLOR = display.create_pen(0, 192, 255)
ERROR_COLOR = display.create_pen(255, 0, 0)
CHART_BG_COLOR = display.create_pen(20, 30, 50)
CANDLE_UP_COLOR = display.create_pen(0, 200, 100)
CANDLE_DOWN_COLOR = display.create_pen(200, 50, 50)
CANDLE_WICK_COLOR = display.create_pen(100, 100, 100)
PRICE_UP_COLOR = display.create_pen(0, 255, 128)      # Bright Green
PRICE_DOWN_COLOR = display.create_pen(255, 80, 80)     # Red
PRICE_SAME_COLOR = display.create_pen(255, 255, 255)   # White

# --- NEW: INITIALIZE BUTTONS USING MACHINE.PIN ---
# Using the pins: A=12, B=13, X=14, Y=15
button_a = machine.Pin(12, machine.Pin.IN, machine.Pin.PULL_UP)
button_b = machine.Pin(13, machine.Pin.IN, machine.Pin.PULL_UP)
button_x = machine.Pin(14, machine.Pin.IN, machine.Pin.PULL_UP)
button_y = machine.Pin(15, machine.Pin.IN, machine.Pin.PULL_UP)
BUTTONS = [button_a, button_b, button_x, button_y]


# --- API AND NETWORK FUNCTIONS ---

def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(WIFI_SSID, WIFI_PASSWORD)
    status_text("Connecting...")
    max_wait = 15
    while max_wait > 0:
        if wlan.status() >= 3: break
        max_wait -= 1
        print('Waiting for connection...')
        time.sleep(1)
    if wlan.status() != 3:
        status_text("WiFi Failed!", ERROR_COLOR)
        raise RuntimeError('WiFi connection failed')
    else:
        print('Connected to WiFi')
        return True

def get_market_data(api_symbol): 
    """Gets OHLC data for the chart, plus latest price and volume."""
    print(f"Fetching market data for {api_symbol}...")
    api_url = f"https://api.binance.com/api/v3/klines?symbol={api_symbol}&interval=5m&limit={CHART_HISTORY_POINTS}" # <<<< MODIFIED
    try:
        response = urequests.get(api_url)
        data = response.json()
        response.close()
        ohlc_list = [[float(k[1]), float(k[2]), float(k[3]), float(k[4])] for k in data]
        latest_candle = data[-1]
        latest_price = float(latest_candle[4])
        volume_in_period = sum([float(k[5]) for k in data])
        return ohlc_list, latest_price, volume_in_period
    except Exception as e:
        print(f"Error fetching market data for {api_symbol}: {e}") 
        return [], None, None

# --- DISPLAY FUNCTIONS ---

def format_price(price, fmt_string): 
    if price is None: return "   N/A    "
    return fmt_string.format(price) 

def format_volume(volume):
    if volume is None: return "    N/A    "
    if volume > 1_000_000: vol_str = f"${volume / 1_000_000:.2f}M"
    else: vol_str = f"${volume / 1000:.1f}K"
    return f"{vol_str:>11}"

def status_text(text, color=TITLE_COLOR):
    display.set_pen(BG_COLOR)
    display.clear()
    display.set_font("sans")
    text_width = display.measure_text(text, scale=3)
    display.text(text, (WIDTH - text_width) // 2, HEIGHT // 2 - 10, scale=3)
    display.update()

def draw_price_chart(ohlc_history):
    CHART_X, CHART_Y, CHART_WIDTH, CHART_HEIGHT = 10, 10, WIDTH - 20, 80
    display.set_pen(CHART_BG_COLOR)
    display.rectangle(CHART_X, CHART_Y, CHART_WIDTH, CHART_HEIGHT)
    if len(ohlc_history) < 1: return
    min_price = min([c[2] for c in ohlc_history])
    max_price = max([c[1] for c in ohlc_history])
    price_range = max_price - min_price
    if price_range == 0: price_range = 1
    CANDLE_WIDTH = (CHART_WIDTH / len(ohlc_history)) * 0.8
    CANDLE_GAP = (CHART_WIDTH / len(ohlc_history)) * 0.2
    def price_to_y(price):
        return int(CHART_Y + CHART_HEIGHT - ((price - min_price) / price_range) * CHART_HEIGHT)
    for i, candle in enumerate(ohlc_history):
        o, h, l, c = candle
        candle_x = int(CHART_X + (i * (CANDLE_WIDTH + CANDLE_GAP)))
        body_color = CANDLE_UP_COLOR if c >= o else CANDLE_DOWN_COLOR
        display.set_pen(CANDLE_WICK_COLOR)
        wick_x = int(candle_x + CANDLE_WIDTH // 2)
        display.line(wick_x, price_to_y(h), wick_x, price_to_y(l))
        display.set_pen(body_color)
        y_o, y_c = price_to_y(o), price_to_y(c)
        body_height = abs(y_o - y_c)
        if body_height < 1: body_height = 1
        display.rectangle(int(candle_x), min(y_o, y_c), int(CANDLE_WIDTH), body_height)

def draw_dashboard(asset, price_history, current_price, current_volume, price_color):
    display.set_pen(BG_COLOR)
    display.clear()
    draw_price_chart(price_history)
    display.set_font("bitmap8")

    display.set_pen(TITLE_COLOR)
    title1_text = f"{asset['name']} PRICE"
    title2_text = f"VOL ({CHART_HISTORY_POINTS*5} MIN)"
    title1_width, title2_width = display.measure_text(title1_text, scale=2), display.measure_text(title2_text, scale=2)
    display.text(title1_text, (WIDTH - title1_width) // 2, 105, scale=2)
    display.text(title2_text, (WIDTH - title2_width) // 2, 175, scale=2)

    display.set_pen(price_color)
    price_text = format_price(current_price, asset['price_format'])
    price_width = display.measure_text(price_text, scale=4)
    display.text(price_text, (WIDTH - price_width) // 2, 125, scale=4)

    display.set_pen(VOLUME_COLOR)
    volume_text = format_volume(current_volume)
    volume_width = display.measure_text(volume_text, scale=3)
    display.text(volume_text, (WIDTH - volume_width) // 2, 195, scale=3)
    
    display.update()

# --- MAIN PROGRAM LOOP  ---

try:
    connect_wifi()
    
    # --- NEW: State variables for current asset and button presses ---
    current_asset_index = 0 # Default to the first asset (XRP)
    asset = ASSETS[current_asset_index]
    button_pressed_state = [False] * len(BUTTONS) # To detect a single press
    
    # Initial data fetch for the default asset
    status_text(f"Loading {asset['name']}...") # Initial loading message
    price_history, xrp_price, xrp_volume = get_market_data(asset['symbol'])
    
    if xrp_price is None: # If initial fetch fails
        status_text(f"API Error: {asset['name']}", ERROR_COLOR)
        while True: time.sleep(1) # Halt on fatal error

    previous_price = xrp_price
    price_color = PRICE_SAME_COLOR
    last_crypto_update_time = time.time()
    
    # Initial draw of the dashboard
    draw_dashboard(asset, price_history, xrp_price, xrp_volume, price_color)

    while True:
        asset_changed_by_button = False

        # --- NEW: Check buttons for a new press ---
        for i, button in enumerate(BUTTONS):
            current_button_state = (button.value() == 0) # True if pressed
            if current_button_state and not button_pressed_state[i]: # New press
                button_pressed_state[i] = True # Mark as pressed for this cycle
                if i != current_asset_index:
                    print(f"Button for new asset {ASSETS[i]['name']} detected!")
                    current_asset_index = i
                    asset_changed_by_button = True # Signal that the asset changed
            elif not current_button_state:
                button_pressed_state[i] = False # Reset state when button is released
        
        time_to_refresh_periodically = (time.time() - last_crypto_update_time > CRYPTO_REFRESH_INTERVAL)
        
        if asset_changed_by_button or time_to_refresh_periodically:
            asset = ASSETS[current_asset_index] # Get current asset
            print(f"Updating data for {asset['name']}...")
            # NO status_text() call here, to prevent full screen clear for loading/refreshing
            
            new_history, new_price, new_volume = get_market_data(asset['symbol'])
            
            if new_price is not None:
                if asset_changed_by_button or previous_price is None: 
                    price_color = PRICE_SAME_COLOR
                elif new_price > previous_price: price_color = PRICE_UP_COLOR
                elif new_price < previous_price: price_color = PRICE_DOWN_COLOR
                else: price_color = PRICE_SAME_COLOR
                
                previous_price = new_price
                xrp_price = new_price         # Update the variable holding the current price
                xrp_volume = new_volume       # Update the variable holding the current volume
                price_history = new_history   # Update the variable holding the price history
            # If API failed, we keep displaying the old data, which is already in xrp_price etc.
            
            last_crypto_update_time = time.time()

        # Draw the screen with the latest data and dynamic color
        # This is called every loop iteration, just like your original script
        # Ensure 'asset' is the currently selected one
        asset = ASSETS[current_asset_index]
        draw_dashboard(asset, price_history, xrp_price, xrp_volume, price_color) # <<<< MODIFIED call
        
        time.sleep(1) # Loop runs once per second, matching your original script's refresh rate

except Exception as e:
    print(f"A critical error occurred: {e}")
    try:
        status_text("ERROR! See REPL", ERROR_COLOR)
    except:
        pass
