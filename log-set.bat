adb root
adb wait-for-device
@REM adb shell logcat -c
adb shell  setprop persist.iauto.appupdate true
adb shell setprop persist.vendor.iauto.log.switch 31
adb shell setprop persist.log.tag S
adb shell setprop persist.log.tag.IVI-VEHICLELOGIC-SVC V
adb shell logcat -G 200M
adb shell setprop persist.log.tag V

adb shell setprop persist.log.tag.AndroidRuntime  V

adb shell setprop persist.log.tag.libvehiclesolarchargingservice V
adb shell setprop persist.log.tag.libvehiclecharging V
adb shell setprop persist.log.tag.VehicleAdapterManager V

adb shell setprop persist.log.tag.VLogicSvc V
adb shell setprop persist.log.tag.VLogicMgr V
adb shell setprop persist.log.tag.VSettingModel V

adb shell setprop persist.log.tag.VLogicSvc-SOL V
adb shell setprop persist.log.tag.VLogicMgr-SOL V
adb shell setprop persist.log.tag.VSettingModel-SOL V

adb shell setprop persist.log.tag.VLogicSvc-CHARGING V
adb shell setprop persist.log.tag.VLogicMgr-CHARGING V
adb shell setprop persist.log.tag.VSettingModel-CHARGING V

adb shell setprop persist.log.tag.SolarChargingModel V
adb shell setprop persist.log.tag.SolarChargingModelAPIImpl V
adb shell setprop persist.log.tag.SolarChargingFC V

adb shell setprop persist.log.tag.ChargecontrolModel V
adb shell setprop persist.log.tag.ChargecontrolModelAPIImpl V
adb shell setprop persist.log.tag.ChargecontrolModelAPIImpl V
adb shell setprop persist.log.tag.ChargecontrolFC V

adb shell setprop persist.log.tag.vehiclesettingCOM V
adb shell setprop persist.log.tag.UI-VEHICLE-CHARGE V
adb shell setprop persist.log.tag.vehiclesettingcharge V

# T2
setprop persist.sv.debug.adb_enable 1
setprop persist.sv.debug.adb_enable 0
# T1
setprop sys.usb.config adb
setprop sys.usb.config mtp
# L
sh /vendor/bin/usb_func_role.sh normal
sh /vendor/bin/usb_func_role.sh adb

@REM adb logcat -c

@REM am start -n com.iauto.diag/.screens.screen.MAINACTIVITY --es targetView "FactoryDiagTop"