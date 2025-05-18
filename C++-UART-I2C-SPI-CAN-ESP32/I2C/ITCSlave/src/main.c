#include <stdio.h>
#include "driver/i2c.h"
#include "esp_log.h"
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"

#define I2C_SLAVE_SCL_IO            22           // GPIO for SCL
#define I2C_SLAVE_SDA_IO            21           // GPIO for SDA
#define I2C_SLAVE_NUM               I2C_NUM_1    // Using I2C_NUM_1 for Slave
#define I2C_SLAVE_TX_BUF_LEN        512
#define I2C_SLAVE_RX_BUF_LEN        512
#define SLAVE_ADDR                  0x42          // Slave Address (matches Master's target)

static const char *TAG = "I2C_SLAVE";

esp_err_t i2c_slave_init() {
    i2c_config_t conf;
    conf.mode = I2C_MODE_SLAVE;
    conf.sda_io_num = I2C_SLAVE_SDA_IO;
    conf.scl_io_num = I2C_SLAVE_SCL_IO;
    conf.sda_pullup_en = GPIO_PULLUP_ENABLE;
    conf.scl_pullup_en = GPIO_PULLUP_ENABLE;
    conf.slave.addr_10bit_en = 0;
    conf.slave.slave_addr = SLAVE_ADDR;
    conf.clk_flags = 0;

    esp_err_t res = i2c_param_config(I2C_SLAVE_NUM, &conf);
    if (res != ESP_OK) return res;

    return i2c_driver_install(I2C_SLAVE_NUM, conf.mode,
                              I2C_SLAVE_RX_BUF_LEN,
                              I2C_SLAVE_TX_BUF_LEN, 0);
}

void app_main() {
    ESP_ERROR_CHECK(i2c_slave_init());
    ESP_LOGI(TAG, "===== I2C SLAVE CODE RUNNING =====");

    uint8_t rx_buffer[128];
    uint8_t tx_data = 0;

    while (1) {
        // 1. Wait for command from Master
        int len = i2c_slave_read_buffer(I2C_SLAVE_NUM, rx_buffer, sizeof(rx_buffer), pdMS_TO_TICKS(1000));

        if (len > 0) {
            ESP_LOGI(TAG, "Received %d bytes from Master.", len);
            ESP_LOG_BUFFER_HEXDUMP(TAG, rx_buffer, len, ESP_LOG_INFO);

            // 2. Process Command & Prepare Response
            switch (rx_buffer[0]) {
                case 0x01:
                    tx_data = 30;  // Fake Temperature
                    break;
                case 0x02:
                    tx_data = 55;  // Fake Humidity
                    break;
                default:
                    tx_data = 0xFF;  // Unknown Command
                    break;
            }

            ESP_LOGI(TAG, "Prepared Response: %d", tx_data);

            // 3. Clear TX FIFO before writing new response
            i2c_reset_tx_fifo(I2C_SLAVE_NUM);

            // 4. Write Response for Master to Read
            int bytes_written = i2c_slave_write_buffer(I2C_SLAVE_NUM, &tx_data, 1, pdMS_TO_TICKS(1000));
            if (bytes_written > 0) {
                ESP_LOGI(TAG, "Response sent to Master.");
            } else {
                ESP_LOGE(TAG, "Failed to write response.");
            }

            // 5. Small Delay to Ensure Master Reads the Prepared Data
            vTaskDelay(pdMS_TO_TICKS(50));
        }

        vTaskDelay(pdMS_TO_TICKS(100));  // Avoid tight polling loop
    }
}
