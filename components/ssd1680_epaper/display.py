import esphome.codegen as cg
import esphome.config_validation as cv
from esphome import pins
from esphome.components import display, spi
from esphome.const import (
    CONF_DC_PIN,
    CONF_ID,
    CONF_LAMBDA,
    CONF_PAGES,
    CONF_RESET_PIN,
    CONF_BUSY_PIN,
    CONF_HEIGHT,
    CONF_WIDTH,
    CONF_INVERT,
    CONF_FULL_UPDATE_EVERY
)

DEPENDENCIES = ["spi"]

ssd1680_epaper_ns = cg.esphome_ns.namespace("ssd1680_epaper")
SSD1680EPaper = ssd1680_epaper_ns.class_(
    "SSD1680EPaper", cg.PollingComponent, display.DisplayBuffer, spi.SPIDevice
)

# Per the SSD1680 datasheet, it can address at most 296 gate outputs (rows)
# and 176 source outputs (columns)
SSD1680_MAX_H = 296
SSD1680_MAX_W = 176

CONFIG_SCHEMA = (
    display.FULL_DISPLAY_SCHEMA.extend(
        {
            cv.GenerateID(): cv.declare_id(SSD1680EPaper),
            cv.Required(CONF_HEIGHT): cv.int_range(1, SSD1680_MAX_H),
            cv.Required(CONF_WIDTH): cv.int_range(1, SSD1680_MAX_W),
            cv.Required(CONF_DC_PIN): pins.gpio_output_pin_schema,
            cv.Optional(CONF_RESET_PIN): pins.gpio_output_pin_schema,
            cv.Optional(CONF_BUSY_PIN): pins.gpio_input_pin_schema,
            cv.Optional(CONF_INVERT): cv.boolean,
            cv.Optional(CONF_FULL_UPDATE_EVERY): cv.int_range(min=0)
        }
    )
    .extend(cv.polling_component_schema("60s"))
    .extend(spi.spi_device_schema(cs_pin_required=True))
)


async def to_code(config):
    var = cg.new_Pvariable(config[CONF_ID])
    await display.register_display(var, config)
    await spi.register_spi_device(var, config)

    cg.add(var.set_height(config[CONF_HEIGHT]))
    cg.add(var.set_width(config[CONF_WIDTH]))

    dc = await cg.gpio_pin_expression(config[CONF_DC_PIN])
    cg.add(var.set_dc_pin(dc))

    if CONF_INVERT in config:
        cg.add(var.invert_color(config[CONF_INVERT]))

    if CONF_FULL_UPDATE_EVERY in config:
        cg.add(var.set_full_update_count(config[CONF_FULL_UPDATE_EVERY]))

    if CONF_RESET_PIN in config:
        reset = await cg.gpio_pin_expression(config[CONF_RESET_PIN])
        cg.add(var.set_reset_pin(reset))

    if CONF_BUSY_PIN in config:
        busy = await cg.gpio_pin_expression(config[CONF_BUSY_PIN])
        cg.add(var.set_busy_pin(busy))

    if CONF_LAMBDA in config:
        lambda_ = await cg.process_lambda(
            config[CONF_LAMBDA], [(display.DisplayRef, "it")], return_type=cg.void
        )
        cg.add(var.set_writer(lambda_))
