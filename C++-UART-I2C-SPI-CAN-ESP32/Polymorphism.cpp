#include<iostream>
using namespace std;

class Device {
    private:
        int baud_rate;

    public:
        Device(int x) : baud_rate{x}
        {
        }
    ~Device (){

    }
    virtual void sendData() {
        cout << "From Device" << endl;
    }
};
class UART : public Device {
    public:
        UART (int x) : Device{x}{
        
    }
    void sendData() override {
        cout << "from UART" << endl;
    }
};

class I2C : public Device {
    public:
    I2C (int x) : Device{x}{

    }
    void sendData() override {
        cout << "from I2C" << endl;
    }
};

int main() {
    Device d {9600};
    UART U {115200};
    I2C I {400000};
    Device *Uptr = &U;
    Device *Iptr = &I;
    Uptr->sendData();
    Iptr->sendData();
    Device{9600};
    return 0;
}