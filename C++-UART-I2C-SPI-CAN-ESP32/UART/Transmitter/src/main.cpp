#include <Arduino.h>
#include <driver/uart.h>
#define TX_PIN 17
#define RX_PIN 16
const int BUF_SZ = (1024 * 2);
const char* test_str = "Hello!\n";
const uart_port_t uart_num = UART_NUM_2;

void setup() {
  Serial.begin(115200);
  Serial.println("🚀 Transmitter code Booted");  // For transmitter
uart_config_t uart_config = {
    .baud_rate = 115200,
    .data_bits = UART_DATA_8_BITS,
    .parity = UART_PARITY_DISABLE,
    .stop_bits = UART_STOP_BITS_1,
    .flow_ctrl = UART_HW_FLOWCTRL_DISABLE,
    .rx_flow_ctrl_thresh = 0,
};
// Configure UART parameters
ESP_ERROR_CHECK(uart_param_config(uart_num, &uart_config));
uart_set_pin(uart_num, TX_PIN, RX_PIN, UART_PIN_NO_CHANGE, UART_PIN_NO_CHANGE);
uart_driver_install(uart_num, BUF_SZ, BUF_SZ, 0, NULL, 0);

}

void loop() {
  delay(2000);
  uart_write_bytes(uart_num, (const char *)test_str, strlen(test_str));
}

