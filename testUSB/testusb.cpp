#include <iostream>
#include "include/libusb.h"
#include <windows.h>

using namespace std;

#define ADB_CLASS 0xFF
#define ADB_SUB_CLASS 0x42
#define ADB_PROTOCAL 0x01
void print_decs(libusb_device_descriptor dev) {
    cout << endl;
    cout << "-----------device-------" << endl;
    cout << "------------------" << endl;
    printf(" length \t%x\n",dev.bLength);
    printf(" bDescriptorType \t%x\n",dev.bDescriptorType);
    printf(" bcdUSB \t%x\n",dev.bcdUSB);
    printf(" bDeviceClass \t%x\n",dev.bDeviceClass);
    printf(" bDeviceProtocol \t%x\n",dev.bDeviceProtocol);
    printf(" bMaxPacketSize0 \t%x\n",dev.bMaxPacketSize0);
    printf(" idVendor \t%x\n",dev.idVendor);
    printf(" idProduct \t%x\n",dev.idProduct);
    printf(" bcdDevice \t%x\n",dev.bcdDevice);
    printf(" iManufacturer \t%x\n",dev.iManufacturer);
    printf(" iProduct \t%x\n",dev.iProduct);
    printf(" iSerialNumber \t%x\n",dev.iSerialNumber);
    printf(" bNumConfigurations \t%x\n",dev.bNumConfigurations);
    cout << endl;
}

void print_config(libusb_config_descriptor inter) {
    cout << "--------config----------" << endl;
    printf("bLength\t%x\n",inter.bLength);
    printf("bDescriptorType\t%x\n",inter.bDescriptorType);
    printf("wTotalLength\t%x\n",inter.wTotalLength);
    printf("bNumInterfaces\t%x\n",inter.bNumInterfaces);
    printf("bConfigurationValue\t%x\n",inter.bConfigurationValue);
    printf("iConfiguration\t%x\n",inter.iConfiguration);
    printf("bmAttributes\t%x\n",inter.bmAttributes);
    printf("MaxPower\t%x\n",inter.MaxPower);
    printf("extra\t%x\n",inter.extra);
    printf("extra_length\t%x\n",inter.extra_length);
}

void print_interface(libusb_interface_descriptor inter) {
    cout << "----------inter--------" << endl;
    printf("bLength\t%x\n",inter.bLength);
    printf("bDescriptorType\t%x\n",inter.bDescriptorType);
    printf("bInterfaceNumber\t%x\n", inter.bInterfaceNumber);
    printf("bAlternateSetting\t%x\n", inter.bAlternateSetting);
    printf("bNumEndpoints\t%x\n", inter.bNumEndpoints);
    printf("bInterfaceClass\t%x\n", inter.bInterfaceClass);
    printf("bInterfaceSubClass\t%x\n", inter.bInterfaceSubClass);
    printf("bInterfaceProtocol\t%x\n", inter.bInterfaceProtocol);
    printf("iInterface\t%x\n", inter.iInterface);
    printf("extra\t%x\n", inter.extra);
    printf("extra_length\t%x\n", inter.extra_length);
}

void print_endpoint(libusb_endpoint_descriptor point) {
    cout << "----------end point--------" << endl;
    printf("bLength\t%x\n",point.bDescriptorType);
    printf("bDescriptorType\t%x\n",point.bDescriptorType);
    printf("bEndpointAddress\t%x\n",point.bEndpointAddress);
    printf("bmAttributes\t%x\n",point.bmAttributes);
    printf("wMaxPacketSize\t%x\n",point.wMaxPacketSize);
    printf("bInterval\t%x\n",point.bInterval);
    printf("bRefresh\t%x\n",point.bRefresh);
    printf("bSynchAddress\t%x\n",point.bSynchAddress);
    printf("extra\t%x\n",point.extra);
    printf("extra_length\t%x\n",point.extra_length);
}

bool is_adb_interface(uint8_t interClass, uint8_t interSubClass, uint8_t interProtocal) {
    return interClass == ADB_CLASS && interSubClass == ADB_SUB_CLASS && interProtocal == ADB_PROTOCAL;
}


int main() {
    libusb_context *context;
    cout << "Initializing libusb..." << endl;
    int i = libusb_init(&context);
    if (i != 0) {
        cerr << "Error initializing libusb: " << i << endl;
        return 1; // Return non-zero value to indicate failure
    }
    cout << "Libusb initialized successfully." << endl;
    libusb_device **device;
    size_t t =  libusb_get_device_list(context, &device);
    int cnt = 0;

    
    while (device[cnt] != NULL && cnt < t) {
        cout << endl;
        // cout << "print  " << cnt << endl;
        libusb_device_descriptor decs;
        libusb_get_device_descriptor(device[cnt], &decs);
        // printf("idproduct .. %x" , decs.idProduct);
        // if (decs.idProduct != 0x901d) {
        //     cnt++;
        //     continue;
        // }
        // if (decs.iSerialNumber != 3) {
        //     cnt++;
        //     continue;
        // }
        // print_decs(decs);
        libusb_config_descriptor *config;
        libusb_get_config_descriptor(device[cnt], 0, &config);
        // print_config(*config);
        // printf("\tinterface num %x \n", config->bNumInterfaces);
        for(int i = 0; i < config->bNumInterfaces; i++) {
            libusb_interface interface = config->interface[i];
            // printf("\tinter dec index %x \n", i);
            for (int y = 0; y < interface.num_altsetting; y++) {
                libusb_interface_descriptor inter = interface.altsetting[y];
                if (!is_adb_interface(interface.altsetting[y].bInterfaceClass, 
                interface.altsetting[y].bInterfaceSubClass, 
                interface.altsetting[y].bInterfaceProtocol) || inter.bNumEndpoints != 2)
                {
                    continue;
                }
                print_decs(decs);
                print_interface(inter);
                for (int j = 0; j < inter.bNumEndpoints ; j++) {
                    print_endpoint(inter.endpoint[j]);
                }
                
            }
            // print_interface(interface->altsetting);
        }
        
                
        cnt++;
    }    
    
    libusb_exit(context);
    cout << "lisb usb exit...." << endl;
    return 0;
}
