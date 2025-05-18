#pragma once
#include <Arduino.h>

class RingBuffer {
public:
    RingBuffer(size_t size);
    ~RingBuffer();

    bool push(uint8_t byte);
    bool pop(uint8_t &byte);
    size_t available() const;
    void clear();

private:
    uint8_t* buffer;
    size_t capacity;
    size_t head;
    size_t tail;
    size_t count;
};
