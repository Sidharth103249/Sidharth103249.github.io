#include<stdio.h>
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "driver/gpio.h"
#include "esp_log.h"

#define GPIO GPIO_NUM_2

void task_blink (void *pv) {
    gpio_reset_pin(GPIO);
    gpio_set_direction(GPIO, GPIO_MODE_OUTPUT);
    for (;;) {
        gpio_set_level(GPIO, 1);
        vTaskDelay(pdMS_TO_TICKS(2000));
        gpio_set_level(GPIO, 0);
        vTaskDelay(pdMS_TO_TICKS(2000));
    }
}

void task_uart(void *pv) {
    const char *TAG = "UARTTaskDaMama";
    for(;;) {
        ESP_LOGI(TAG, "Inside UART for loop");
        vTaskDelay((pdMS_TO_TICKS(2000)));
    }
}

void app_main() {
    xTaskCreate(task_blink, "BLINK", 2048, NULL, 2, NULL);
    xTaskCreate(task_uart, "UART", 2048, NULL, 3, NULL);
}