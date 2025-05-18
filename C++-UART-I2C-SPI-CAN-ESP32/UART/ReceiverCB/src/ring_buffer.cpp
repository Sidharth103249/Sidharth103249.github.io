#include "ring_buffer.h"
#include <cstring>

RingBuffer::RingBuffer(size_t size)
    : capacity(size), head(0), tail(0), count(0) {
    buffer = new uint8_t[size];
    memset(buffer, 0, size);
}

RingBuffer::~RingBuffer() {
    delete[] buffer;
}

bool RingBuffer::push(uint8_t byte) {
    if (count == capacity) return false; // Buffer full
    buffer[head] = byte;
    head = (head + 1) % capacity;
    count++;
    return true;
}

bool RingBuffer::pop(uint8_t &byte) {
    if (count == 0) return false; // Buffer empty
    byte = buffer[tail];
    tail = (tail + 1) % capacity;
    count--;
    return true;
}

size_t RingBuffer::available() const {
    return count;
}

void RingBuffer::clear() {
    head = tail = count = 0;
}
