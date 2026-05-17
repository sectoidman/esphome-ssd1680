# ESPHome SSD1680 E-Paper Display Component

A custom ESPHome component for SSD1680-based e-paper displays, specifically developed for the **Elecrow CrowPanel ESP32 2.9" E-Paper HMI Display** but compatible with other SSD1680/SSD1680Z displays.

## Features

- Full support for 128x296 pixel 2.9" e-paper displays
- Compatible with SSD1680 and SSD1680Z driver chips
- Proper full refresh using internal LUT
- Handles inverted pixel polarity common in these displays
- Deferred initialization for reliable startup logging
- Watchdog-friendly long refresh operations

## Supported Hardware

### Tested
- [Elecrow CrowPanel ESP32 2.9" E-Paper HMI Display](https://www.elecrow.com/crowpanel-esp32-2-9-e-paper-hmi-display-with-128-296-resolution-black-white-color-driven-by-spi-interface.html)
  - Resolution: 128x296 pixels
  - Driver: SSD1680Z
  - ESP32-S3 based

- [Elecrow CrowPanel ESP32 2.13" E-Paper HMI Display](https://www.elecrow.com/wiki/CrowPanel_ESP32_E-Paper_HMI_2.13-inch_Display.html)
  - Resolution: 122x250 pixels
  - Driver: SSD1680Z
  - ESP32-S3 based

### Should Work (Untested)
- Other SSD1680-based e-paper displays
- Good Display GDEW029T5
- Waveshare 2.9" V2 (SSD1680)

## Installation

### Using External Components (Recommended)

Add this to your ESPHome YAML configuration:

```yaml
external_components:
  - source:
      type: git
      url: https://github.com/apadua/esphome-ssd1680
      ref: main
    components: [ssd1680_epaper]
```

### Manual Installation

1. Copy the `components/ssd1680_epaper` folder to your ESPHome configuration directory
2. Reference it as a local external component:

```yaml
external_components:
  - source:
      type: local
      path: components
```

## Configuration

### Basic Configuration

```yaml
spi:
  clk_pin: GPIO12
  mosi_pin: GPIO11

display:
  - platform: ssd1680_epaper
    id: epaper_display
    width: 122
    height: 250
    cs_pin: GPIO45
    dc_pin: GPIO46
    reset_pin: GPIO47
    busy_pin: GPIO48
    rotation: 270
    update_interval: 60s
    full_update_every: 0
    invert: false
    lambda: |-
      it.printf(64, 148, id(my_font), TextAlign::CENTER, "Hello World!");
```

### CrowPanel ESP32 2.9" Full Example

```yaml
esphome:
  name: crowpanel-epaper
  friendly_name: CrowPanel E-Paper

esp32:
  board: esp32-s3-devkitc-1
  framework:
    type: esp-idf
  flash_size: 8MB

psram:
  mode: octal
  speed: 80MHz

logger:

api:
  encryption:
    key: !secret api_encryption_key

ota:
  - platform: esphome
    password: !secret ota_password

wifi:
  ssid: !secret wifi_ssid
  password: !secret wifi_password

external_components:
  - source:
      type: git
      url: https://github.com/apadua/esphome-ssd1680
      ref: main
    components: [ssd1680_epaper]

spi:
  clk_pin: GPIO12
  mosi_pin: GPIO11

display:
  - platform: ssd1680_epaper
    id: epaper_display
    width: 128
    height: 296
    cs_pin:
      number: GPIO45
      ignore_strapping_warning: true
    dc_pin:
      number: GPIO46
      ignore_strapping_warning: true
    reset_pin: GPIO47
    busy_pin: GPIO48
    rotation: 270
    update_interval: 60s
    lambda: |-
      // Fill background with white
      it.fill(COLOR_OFF);

      // Draw title
      it.printf(it.get_width()/2, 10, id(font_title), COLOR_ON, TextAlign::TOP_CENTER, "E-Paper Display");

      // Draw time if available
      if (id(ha_time).now().is_valid()) {
        it.strftime(it.get_width()/2, 50, id(font_large), COLOR_ON, TextAlign::TOP_CENTER, "%H:%M", id(ha_time).now());
        it.strftime(it.get_width()/2, 100, id(font_medium), COLOR_ON, TextAlign::TOP_CENTER, "%A", id(ha_time).now());
        it.strftime(it.get_width()/2, 130, id(font_medium), COLOR_ON, TextAlign::TOP_CENTER, "%B %d, %Y", id(ha_time).now());
      }

font:
  - file: "gfonts://Roboto@700"
    id: font_title
    size: 24
  - file: "gfonts://Roboto@700"
    id: font_large
    size: 48
  - file: "gfonts://Roboto@400"
    id: font_medium
    size: 20

time:
  - platform: sntp
    id: ha_time
    timezone: America/New_York
```

## Pin Configuration

### Elecrow CrowPanel ESP32 2.9"

| Function | GPIO |
|----------|------|
| SPI CLK  | GPIO12 |
| SPI MOSI | GPIO11 |
| CS       | GPIO45 |
| DC       | GPIO46 |
| RESET    | GPIO47 |
| BUSY     | GPIO48 |

### CrowPanel Buttons (Optional)

| Button | GPIO |
|--------|------|
| Exit   | GPIO1 |
| Home   | GPIO2 |
| Up     | GPIO6 |
| Down   | GPIO4 |
| Center | GPIO5 |

## Configuration Options

| Option | Required | Description |
|--------|----------|-------------|
| `cs_pin` | Yes | SPI Chip Select pin |
| `dc_pin` | Yes | Data/Command pin |
| `width` | Yes | Display width |
| `height` | Yes | Display height |
| `reset_pin` | No | Hardware reset pin (recommended) |
| `busy_pin` | No | Busy status pin (recommended) |
| `rotation` | No | Display rotation (0, 90, 180, 270) |
| `update_interval` | No | How often to refresh (default: 60s) |
| `invert` | No | Invert pixel color, e.g. pixel ON = WHITE, OFF = BLACK (default: false) |
| `full_update_every` | No | How many partial refreshes until a full refresh (default: 0 - always do a full refresh) |
| `lambda` | No | Drawing code |

## Drawing

The display uses a binary color model:
- `COLOR_ON` (or `Color::BLACK`) - Black pixels
- `COLOR_OFF` (or `Color::WHITE`) - White pixels

### Examples

```yaml
lambda: |-
  // Fill entire screen white
  it.fill(COLOR_OFF);
  
  // Draw black rectangle
  it.filled_rectangle(10, 10, 50, 30, COLOR_ON);
  
  // Draw text
  it.printf(64, 100, id(my_font), COLOR_ON, TextAlign::CENTER, "Hello!");
  
  // Draw line
  it.line(0, 0, 128, 296, COLOR_ON);
  
  // Draw circle
  it.circle(64, 148, 30, COLOR_ON);
```

## Troubleshooting

### Display not updating
0. Is the device powered?
1. Check all pin connections
2. Verify the BUSY pin is connected - without it, timing may be off
3. E-paper full refresh takes about 1 second.

### Inverted colors
You can use the `invert:` configuration option to turn on or off the pixel inversion feature controlled by command `0x21` "display update control 1" bits 0-3

### Timeout warnings in logs
Messages like "Update timeout after 5000 ms" are often normal. The SSD1680's BUSY pin doesn't always behave as expected, but the display typically still updates correctly.

### Ghosting or artifacts
E-paper displays can retain previous images. Try:
- Doing full refreshes instead of partial ones
- Power cycling the device
- ~~This is normal e-paper behavior, not a driver issue~~ skill issue, claude - you can always write a better driver that takes into account the properties of what it's driving.

## Technical Notes

- Uses 0xF7 update sequence for full refresh with internal LUT on full refreshes, and the 0xFF update sequence for partial refreshes
- ~~Pixel data is inverted before sending (this display uses inverted polarity)~~ The chip *has* the ability to invert the display ram, you just need to configure it properly.
- BUSY pin behavior varies; timeout is handled gracefully
- Full refresh takes approximately 1 second now that it's been optimized a bit
- Display height and width are now customizable (and indeed, mandatory configuration options) for different panel sizes using this chip - tested with the Elecrow DIE01021S 122x250 2.13in E-Paper display ESP32-S3 dev board that also uses the SSD1680.
- I recommend using an `update_interval` of `never` and directly calling the `component.update` action on the screen when you want to update it, e.g. as an action in an `on_value` automation for a sensor with appropriate filtering - this is going to be the most power-efficient way if you're running on batteries, and cause the least wear and tear to the screen.

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

## License

MIT License - See [LICENSE](LICENSE) file for details.

## Acknowledgments

- Developed with assistance from Claude (Anthropic)
- Based on SSD1680 datasheet and Elecrow's Arduino examples
- Thanks to the ESPHome community
