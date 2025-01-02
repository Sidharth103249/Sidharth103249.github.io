#define IOT_CONFIG_WIFI_SSID "*******"
#define IOT_CONFIG_WIFI_PASSWORD "*******"


#ifdef IOT_CONFIG_USE_X509_CERT

 */
#define IOT_CONFIG_DEVICE_CERT "Device Certificate"

/*
 */
#define IOT_CONFIG_DEVICE_CERT_PRIVATE_KEY "Device Certificate Private Key"

#endif // IOT_CONFIG_USE_X509_CERT

// Azure IoT Central
#define DPS_ID_SCOPE "0ne00E33D61"
#define IOT_CONFIG_DEVICE_ID "esp32-dht11"
// Use device key if not using certificates
#ifndef IOT_CONFIG_USE_X509_CERT
#define IOT_CONFIG_DEVICE_KEY "cDyyYtMDh9WSPZGPMp7uxNprajSzRk0WQS55POAUtp8="
#endif // IOT_CONFIG_USE_X509_CERT

#define AZURE_SDK_CLIENT_USER_AGENT "c%2F" AZ_SDK_VERSION_STRING "(ard%3Besp32)"

// Publish 1 message every 10 seconds.
#define TELEMETRY_FREQUENCY_IN_SECONDS 10

#define MQTT_PASSWORD_LIFETIME_IN_MINUTES 60
