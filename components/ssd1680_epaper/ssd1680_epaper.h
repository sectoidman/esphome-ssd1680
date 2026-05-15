#pragma once

#include "esphome/core/component.h"
#include "esphome/components/spi/spi.h"
#include "esphome/components/display/display_buffer.h"

namespace esphome {
namespace ssd1680_epaper {

// VERSION 2 - with deferred init
class SSD1680EPaper : public display::DisplayBuffer,
                      public spi::SPIDevice<spi::BIT_ORDER_MSB_FIRST, spi::CLOCK_POLARITY_LOW,
                                           spi::CLOCK_PHASE_LEADING, spi::DATA_RATE_4MHZ> {
 public:
  void set_dc_pin(GPIOPin *dc_pin) { dc_pin_ = dc_pin; }
  void set_reset_pin(GPIOPin *reset_pin) { reset_pin_ = reset_pin; }
  void set_busy_pin(GPIOPin *busy_pin) { busy_pin_ = busy_pin; }
  void set_height(int height) { height_ = height; }
  void set_width(int width) { width_ = width; }
  void invert_colors(bool invert) { invert_colors_ = invert; }
  void set_full_update_count(int count) { full_update_count_ = count; }

  void setup() override;
  void dump_config() override;
  float get_setup_priority() const override { return setup_priority::PROCESSOR; }
  void update() override;

  display::DisplayType get_display_type() override { return display::DisplayType::DISPLAY_TYPE_BINARY; }

 protected:
  void draw_absolute_pixel_internal(int x, int y, Color color) override;
  int get_height_internal() override { return height_; }
  int get_width_internal() override { return width_; }

  void init_display_();
  void hw_reset_();
  void wait_until_idle_();
  void command_(uint8_t cmd);
  void data_(uint8_t data);
  void send_data_(const uint8_t *data, size_t len);
  void full_update_();
  void fast_update_();
  void display_frame_();
  void configure_address_space_();
  void configure_driver_output_();


  GPIOPin *dc_pin_{nullptr};
  GPIOPin *reset_pin_{nullptr};
  GPIOPin *busy_pin_{nullptr};

  bool initialized_{false};
  bool invert_colors_{false};

  int height_{0};
  int width_{0};
  int display_size{0};
  int full_update_count_{0};
  int full_update_counter_{0};
};

}  // namespace ssd1680_epaper
}  // namespace esphome
