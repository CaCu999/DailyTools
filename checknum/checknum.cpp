#include <iostream>
#include <vector>
#include <cstdint>
using namespace std;

uint8_t calculate_checksum(uint16_t can_id, const std::vector<uint8_t>& data_bytes, uint8_t dlc) {
    uint8_t checksum = 0;
    
    // Add the individual bytes of the CAN ID
    checksum += (can_id & 0xFF); // Lower byte
    checksum += ((can_id >> 8) & 0xFF); // Upper byte
    
    // Add the data bytes
    for (uint8_t byte : data_bytes) {
        checksum += byte;
    }
    
    // Add the DLC
    checksum += dlc;
    
    return checksum;
}

int main() {
    uint16_t can_id = 0x294;
    std::vector<uint8_t> data_bytes = {0x00, 0x00, 0x00, 0x00, 0x40, 0x00, 0x00, 0x00};
    uint8_t dlc = 8;
    
    uint8_t checksum = calculate_checksum(can_id, data_bytes, dlc);
    
    std::cout << "Checksum: " << std::hex << +checksum << std::endl;
    
    return 0;
}
