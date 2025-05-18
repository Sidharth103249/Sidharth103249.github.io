#include<Arduino.h>
#include<driver/uart.h>
#define UART_NUM UART_NUM_2
#define TX_PIN 17
#define RX_PIN 16
#define LED 2
constexpr int BUF_SZ = 256;
volatile uint8_t uartBuff[BUF_SZ];
volatile int uartHead = 0;
volatile int uartTail = 0;
volatile bool dataReady = false;
bool ledFlag = false;

IRAM_ATTR void handleInterrupt (void *arg) {
  ledFlag = !ledFlag; 
  uint8_t ByteIn;
  if (uart_read_bytes(UART_NUM_2, &ByteIn, 1, 0) == 1){
      uartBuff[uartHead] = ByteIn;
      uartHead = (uartHead + 1) % BUF_SZ;
      dataReady = true;
    }
}
void setup (){
  Serial.begin(115200);
  Serial.println("Hello, ESP32!");
  pinMode(LED,OUTPUT);
  uart_config_t uart_config = {
    .baud_rate = 115200,
    .data_bits = UART_DATA_8_BITS,
    .parity = UART_PARITY_DISABLE,
    .stop_bits = UART_STOP_BITS_1,
    .flow_ctrl = UART_HW_FLOWCTRL_DISABLE,
    .source_clk = UART_SCLK_APB,

  };
ESP_ERROR_CHECK(uart_param_config(UART_NUM_2, &uart_config));  
  uart_set_pin(UART_NUM_2, TX_PIN, RX_PIN, UART_PIN_NO_CHANGE, UART_PIN_NO_CHANGE);
  uart_driver_install(UART_NUM_2, BUF_SZ, 0, 0, NULL, 0);
  uart_enable_rx_intr(UART_NUM_2);
  uart_isr_register(UART_NUM_2, handleInterrupt, NULL, ESP_INTR_FLAG_IRAM, NULL);
    }
void loop () {
  uart_write_bytes(UART_NUM_2, "65\n", 2);
  delay(1000);
  if (ledFlag) {
  ledFlag = false;
  digitalWrite(LED, !digitalRead(LED));
}
  if (dataReady) {
    dataReady = false;
    uint8_t B = uartBuff[uartTail];
    uartTail = (uartTail + 1) % BUF_SZ;
    Serial.write(B);
    }
  if (((uartHead + 1) % BUF_SZ) == uartTail) {
    Serial.println("Error: Buffer Overflow");
}
    }
