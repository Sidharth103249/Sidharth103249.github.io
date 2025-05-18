#include <Arduino.h>
#include <driver/uart.h>
#define TX_PIN 17
#define RX_PIN 16
#define LED 2
const int BUF_SZ = (1024 * 2);
const uart_port_t uart_num = UART_NUM_2;
uint8_t data[BUF_SZ];
int length = 0;
bool ledFlag = false;
const char test_str[] = "Hello!\n";
constexpr size_t test_len = sizeof(test_str) - 1;

void setup() {
  Serial.begin(115200);
  Serial.println("Reciever Code.");
  pinMode(LED,OUTPUT);
uart_config_t uart_config = {
    .baud_rate = 115200,
    .data_bits = UART_DATA_8_BITS,
    .parity = UART_PARITY_DISABLE,
    .stop_bits = UART_STOP_BITS_1,
    .flow_ctrl = UART_HW_FLOWCTRL_DISABLE,
    .rx_flow_ctrl_thresh = 0,
};
ESP_ERROR_CHECK(uart_param_config(uart_num, &uart_config));
uart_set_pin(uart_num, TX_PIN, RX_PIN, UART_PIN_NO_CHANGE, UART_PIN_NO_CHANGE);
uart_driver_install(uart_num, BUF_SZ, BUF_SZ, 0, NULL, 0);

}

void loop() {
  delay(100);
  length = uart_read_bytes(uart_num, data, BUF_SZ, 100/ portTICK_PERIOD_MS);
  if (length>0) {
    Serial.print("Recieved data is: ");
    Serial.write(data, length);
    Serial.println();
        if (length == test_len && memcmp(data, test_str, test_len) == 0) {
      // matched "Hello!\n" exactly!
      ledFlag = !ledFlag;
      digitalWrite(LED, ledFlag ? HIGH : LOW);
      Serial.println("Matched Hello! Toggling LED.");
  }
}
}
