#include <iostream>
#include "include/libusb.h"
#include <windows.h>

using namespace std;

#define ADB_CLASS 0xFF
#define ADB_SUB_CLASS 0x42
#define ADB_PROTOCAL 0x01
void print_decs(libusb_device_descriptor dev, libusb_device *device) {
    cout << endl;
    cout << "-----------device-------" << endl;
    cout << "------------------" << endl;
    printf(" PID %x, VID %x VID %d (bus %d, device %d)"
            , dev.idProduct, dev.idVendor, dev.idVendor, libusb_get_bus_number(device), libusb_get_device_address(device));
    uint8_t path[8];
    int ret = libusb_get_port_numbers(device, path, sizeof(path));
    if (ret > 0) {
        printf(" portNum %d, path: %d", ret, path[0]);    
        for (int i = 1; i < ret; i++)
        {
            printf(".%d", path[i]);
        }
    }    
    // printf(" length \t%x\n",dev.bLength);
    // printf(" bDescriptorType \t%x\n",dev.bDescriptorType);
    // printf(" bcdUSB \t%x\n",dev.bcdUSB);
    // printf(" bDeviceClass \t%x\n",dev.bDeviceClass);
    // printf(" bDeviceProtocol \t%x\n",dev.bDeviceProtocol);
    // printf(" bMaxPacketSize0 \t%x\n",dev.bMaxPacketSize0);
    // printf(" idVendor \t%x\n",dev.idVendor);
    // printf(" idProduct \t%x\n",dev.idProduct);
    // printf(" bcdDevice \t%x\n",dev.bcdDevice);
    // printf(" iManufacturer \t%x\n",dev.iManufacturer);
    // printf(" iProduct \t%x\n",dev.iProduct);
    // printf(" iSerialNumber \t%x\n",dev.iSerialNumber);
    // printf(" bNumConfigurations \t%x\n",dev.bNumConfigurations);
    cout << endl;
}

void print_config(libusb_config_descriptor inter) {
    cout << "--------config----------" << endl;
    printf("len: %d, descriptor type: %d, num interface: %d\n", inter.bLength, inter.bDescriptorType, inter.bNumInterfaces);
    // printf("bLength\t%x\n",inter.bLength);
    // printf("bDescriptorType\t%x\n",inter.bDescriptorType);
    // printf("wTotalLength\t%x\n",inter.wTotalLength);
    // printf("bNumInterfaces\t%x\n",inter.bNumInterfaces);
    // printf("bConfigurationValue\t%x\n",inter.bConfigurationValue);
    // printf("iConfiguration\t%x\n",inter.iConfiguration);
    // printf("bmAttributes\t%x\n",inter.bmAttributes);
    // printf("MaxPower\t%x\n",inter.MaxPower);
    // printf("extra\t%x\n",inter.extra);
    // printf("extra_length\t%x\n",inter.extra_length);
}

void print_interface(libusb_interface_descriptor inter) {
    // printf("%d\t\t%d\t\t%d\t\t%d\t%d\t\t%d\t\t%d\t\t%d\n"
    //     , inter.bLength, inter.bDescriptorType, inter.bInterfaceNumber, inter.bAlternateSetting
    //     , inter.bNumEndpoints, inter.bInterfaceClass, inter.bInterfaceSubClass,inter.bInterfaceProtocol);
    printf("%d\t\t%d\t\t%d\t\t%d\n"
        , inter.bInterfaceClass, inter.bInterfaceSubClass, inter.bInterfaceProtocol, inter.bNumEndpoints);
    // printf("bLength\t%x\n",inter.bLength);
    // printf("bDescriptorType\t%x\n",inter.bDescriptorType);
    // printf("bInterfaceNumber\t%x\n", inter.bInterfaceNumber);
    // printf("bAlternateSetting\t%x\n", inter.bAlternateSetting);
    // printf("bNumEndpoints\t%x\n", inter.bNumEndpoints);
    // printf("bInterfaceClass\t%x\n", inter.bInterfaceClass);
    // printf("bInterfaceSubClass\t%x\n", inter.bInterfaceSubClass);
    // printf("bInterfaceProtocol\t%x\n", inter.bInterfaceProtocol);
    // printf("iInterface\t%x\n", inter.iInterface);
    // printf("extra\t%x\n", inter.extra);
    // printf("extra_length\t%x\n", inter.extra_length);
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
    // device init
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
        libusb_config_descriptor *config;
        libusb_interface_descriptor interface;
        // get descriptor
        int r = libusb_get_device_descriptor(device[cnt], &decs);
        if (r < 0) {
            printf("get device descriptor failed");
            continue;
        }
        print_decs(decs, device[cnt]);
        r = libusb_get_config_descriptor(device[cnt], 0, &config);
        if (r < 0) {
            printf("get config descriptor failed");
            continue;
        }        
        // print_config(*config);

        for(int i = 0; i < config->bNumInterfaces; i++) {
            // cout << "----------inter--------" << endl;
            // printf("len\tdescriptor type\tnum interface\talter setting\tendpoint\tinter class\titer sub class\tinter proto1\n");    
            // printf("bInterfaceClass\tbInterfaceSubClass\tbInterfaceProtocol\tbNumEndpoints\n");           
            for (int j = 0; j < config->interface[i].num_altsetting; j++) {
                interface = config->interface[i].altsetting[j];
                // libusb_get_string_descriptor
                if (!is_adb_interface(interface.bInterfaceClass, 
                interface.bInterfaceSubClass, 
                interface.bInterfaceProtocol) || interface.bNumEndpoints != 2)
                {
                    continue;
                }
                // print_decs(decs);
                print_interface(interface);
        //         for (int j = 0; j < inter.bNumEndpoints ; j++) {
        //             print_endpoint(inter.endpoint[j]);
        //         }                
            }
        }        
                
        cnt++;
    }    
    
    libusb_exit(context);
    cout << "lisb usb exit...." << endl;
    return 0;
}
