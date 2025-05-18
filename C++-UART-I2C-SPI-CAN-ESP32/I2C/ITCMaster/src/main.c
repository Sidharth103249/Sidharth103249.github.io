#include <stdio.h>
#include "driver/i2c.h"
#include "esp_log.h"
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"

#define I2C_MASTER_SCL_IO           22          // GPIO for SCL
#define I2C_MASTER_SDA_IO           21          // GPIO for SDA
#define I2C_MASTER_NUM              I2C_NUM_0
#define I2C_MASTER_FREQ_HZ          100000      // 100 kHz
#define I2C_MASTER_TX_BUF_DISABLE   0
#define I2C_MASTER_RX_BUF_DISABLE   0
#define I2C_TIMEOUT_MS              1000

#define SLAVE_ADDR                  0x42        // Example Slave Address

static const char *TAG = "I2C_MASTER";

esp_err_t i2c_master_init() {
    i2c_config_t conf;
    conf.mode = I2C_MODE_MASTER;
    conf.sda_io_num = I2C_MASTER_SDA_IO;
    conf.scl_io_num = I2C_MASTER_SCL_IO;
    conf.sda_pullup_en = GPIO_PULLUP_ENABLE;
    conf.scl_pullup_en = GPIO_PULLUP_ENABLE;
    conf.master.clk_speed = I2C_MASTER_FREQ_HZ;
    conf.clk_flags = 0;  // Use default clock flags

    esp_err_t res = i2c_param_config(I2C_MASTER_NUM, &conf);
    if (res != ESP_OK) return res;

    return i2c_driver_install(I2C_MASTER_NUM, conf.mode,
                              I2C_MASTER_RX_BUF_DISABLE,
                              I2C_MASTER_TX_BUF_DISABLE, 0);
}

esp_err_t i2c_master_send_command(uint8_t command) {
    i2c_cmd_handle_t cmd = i2c_cmd_link_create();
    i2c_master_start(cmd);
    i2c_master_write_byte(cmd, (SLAVE_ADDR << 1) | I2C_MASTER_WRITE, true);
    i2c_master_write_byte(cmd, command, true);
    i2c_master_stop(cmd);
    esp_err_t ret = i2c_master_cmd_begin(I2C_MASTER_NUM, cmd,
                                          pdMS_TO_TICKS(I2C_TIMEOUT_MS));
    i2c_cmd_link_delete(cmd);
    return ret;
}

esp_err_t i2c_master_read_response(uint8_t *data, size_t len) {
    if (len == 0) return ESP_ERR_INVALID_ARG;

    i2c_cmd_handle_t cmd = i2c_cmd_link_create();
    i2c_master_start(cmd);
    i2c_master_write_byte(cmd, (SLAVE_ADDR << 1) | I2C_MASTER_READ, true);

    if (len > 1) {
        i2c_master_read(cmd, data, len - 1, I2C_MASTER_ACK);
    }
    i2c_master_read_byte(cmd, data + len - 1, I2C_MASTER_NACK);
    i2c_master_stop(cmd);

    esp_err_t ret = i2c_master_cmd_begin(I2C_MASTER_NUM, cmd,
                                          pdMS_TO_TICKS(I2C_TIMEOUT_MS));
    i2c_cmd_link_delete(cmd);
    return ret;
}

void app_main() {
    ESP_ERROR_CHECK(i2c_master_init());
    ESP_LOGI(TAG, "I2C Master Initialized.");

    while (1) {
        uint8_t command = 0x01;  // Example command
        esp_err_t res = i2c_master_send_command(command);

        if (res == ESP_OK) {
            ESP_LOGI(TAG, "Command 0x%02X sent successfully.", command);
        } else {
            ESP_LOGE(TAG, "Failed to send command: %s", esp_err_to_name(res));
        }

        vTaskDelay(pdMS_TO_TICKS(50));  // 50 ms delay before reading response


        uint8_t response = 0;
        res = i2c_master_read_response(&response, 1);

        if (res == ESP_OK) {
            ESP_LOGI(TAG, "Received response: %d", response);
        } else {
            ESP_LOGE(TAG, "Failed to read response: %s", esp_err_to_name(res));
        }

        vTaskDelay(pdMS_TO_TICKS(1000));
    }
}
