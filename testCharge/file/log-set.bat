adb wait-for-device
adb root
adb logcat -c
adb shell  setprop persist.iauto.appupdate true
adb shell setprop persist.vendor.iauto.log.switch 31
#adb shell setprop persist.log.tag S
adb shell logcat -G 200M

adb shell setprop persist.log.tag.AndroidRuntime  V

#L
adb shell setprop persist.log.tag.libvehiclesolarchargingservice V
adb shell setprop persist.log.tag.libvehiclecharging V

# T1
adb shell setprop persist.log.tag.HSAE_VHAL_DataAdapter_v2_0 V
adb shell setprop persist.log.tag. HSAE_VHAL_MetadataContext_v2_0 V
adb shell setprop sys.usb.config adb

# T2
adb shell setprop persist.log.tag.VehiclePlatform V
adb shell setprop persist.log.tag.vehiclehal-PrintHelper V
adb shell setprop persist.log.tag.vehiclehal-proto V
adb shell setprop persist.sv.debug.adb_enable 1

adb shell setprop persist.log.tag.VLogicSvc V
adb shell setprop persist.log.tag.VLogicMgr V
adb shell setprop persist.log.tag.VSettingModel V

adb shell setprop persist.log.tag.VLogicSvc-SOL V
adb shell setprop persist.log.tag.VLogicMgr-SOL V
adb shell setprop persist.log.tag.VSettingModel-SOL V

adb shell setprop persist.log.tag.VLogicSvc-CHARGING V
adb shell setprop persist.log.tag.VLogicMgr-CHARGING V
adb shell setprop persist.log.tag.VSettingModel-CHARGING V

adb shell setprop persist.log.tag.VLogicSvc-CHARGING V
adb shell setprop persist.log.tag.VLogicMgr-CHARGING V
adb shell setprop persist.log.tag.VSettingModel-CHARGING V
adb shell setprop persist.log.tag.VLogicSvc-VLogicSvc-WLC V
adb shell setprop persist.log.tag.VLogicSvc-VSettingModel-WLC V

adb shell setprop persist.log.tag.VLogicSvc-VLogicSvc-VS V
adb shell setprop persist.log.tag.VLogicSvc-VLogicSvc-CUSTOM V

adb shell setprop persist.log.tag.VLogicSvc-VSettingModel-CUSTOM V
adb shell setprop persist.log.tag.VLogicSvc-VSettingModel-ILL V
# APP
adb shell setprop persist.log.tag.vehiclesettingCOM V
adb shell setprop persist.log.tag.UI-VEHICLE-CHARGE V
adb shell setprop persist.log.tag.UI-VEHICLE-VEHICLEEXTERIOR V
adb shell setprop persist.log.tag.vehiclesettingcharge V
adb shell setprop persist.log.tag.vehiclesettingvehicleexterior V
adb shell setprop persist.log.tag.CustomPicker V
adb shell setprop persist.log.tag S

# T2
# setprop persist.sv.debug.adb_enable 1
# setprop persist.sv.debug.adb_enable 0
# T1
# setprop sys.usb.config adb
# setprop sys.usb.config mtp
# L
# sh /vendor/bin/usb_func_role.sh normal
# sh /vendor/bin/usb_func_role.sh adb

rem adb shell "logcat -s SYS_HWH_VINFO_VEHICLE | grep -i 'broadcast propid' & logcat -s libvehiclesolarchargingservice &  logcat -s ChargecontrolModel ChargecontrolModelAPIImpl ChargecontrolFC & logcat -s vehiclesettingCOM | grep -i 'Chargecontrol' & logcat -s vehiclesettingCOM | grep -i 'Solar' &  logcat -s  UI-VEHICLE-CHARGE & logcat -s AndroidRuntime &  logcat -s IVI-VEHICLELOGIC-SVC | grep -i 'VehicleChargingService' & logcat -s VLogicSvc-SOL VLogicMgr-SOL VSettingModel-SOL & logcat -s VLogicSvc-CHARGING VLogicMgr-CHARGING VSettingModel-CHARGING&"
rem logcat -s SYS_HWH_VINFO_VEHICLE | grep -i 'broadcast propid' &
start "ADB Logcat" cmd /c "C:\Users\hyw\Desktop\outlog.bat"
rem adb shell " logcat -s libvehiclesolarchargingservice &  logcat -s ChargecontrolModel ChargecontrolModelAPIImpl ChargecontrolFC & logcat -s vehiclesettingCOM | grep -i 'Chargecontrol' & logcat -s vehiclesettingCOM | grep -i 'Solar' &  logcat -s  UI-VEHICLE-CHARGE & logcat -s VLogicSvc-SOL VLogicMgr-SOL VSettingModel-SOL & logcat -s VLogicSvc-CHARGING VLogicMgr-CHARGING VSettingModel-CHARGING& logcat -s libvehiclecharging & logcat -s libvehiclesolarcharging & logcat -s HSAE_VHAL_DataAdapter_v2_0 & logcat -s VehiclePlatform & logcat -s vehiclehal-PrintHelper & logcat -s vehiclehal-proto &"