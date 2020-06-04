from dronekit import connect, VehicleMode, LocationGlobalRelative
import time

# 機体接続                                                                            
vehicle = connect('127.0.0.1:14550', wait_ready=True)

print("connected")
print(vehicle)

# アーミング可能かチェック
while not vehicle.is_armable:
          print "Waiting for vehicle to initialize..."
          time.sleep(1)

# アーミング
print "Arming motors"
vehicle.mode = VehicleMode("GUIDED")
vehicle.armed = True

# モードがGUIDEDになり、アーミングされるまで待つ
while not vehicle.mode.name == 'GUIDED' and not vehicle.armed:
          time.sleep(1)

print "Armed"         

# Listener
#def location_callback(self, attr_name, value):
#    print(attr_name)
#    print(value)

# Regist listener
#vehicle.add_attribute_listener("location.global_frame", location_callback)
#time.sleep(10)

# Unregist listener
#vehicle.remove_attribute_listener("location.global_frame", location_callback)

# vehicle.home_locationに値がセットされるまで
# downloadを繰り返し実行する
while not vehicle.home_location:
          cmds = vehicle.commands
          cmds.download()
          cmds.wait_ready()

          if not vehicle.home_location:
                     print "Waiting for home location..."

# ホームロケーションの取得完了
print "\n Home lacation: %s" % vehicle.home_location

# 目標コード設定
targetAltitude = 20

# テイクオフ実行
# 20mの高さまで離陸する
print "Take off!!"
vehicle.simple_takeoff(targetAltitude)

# 目標の高度に達するまで待つ
while True:
          print "Altitude:", vehicle.location.global_relative_frame.alt

          if vehicle.location.global_relative_frame.alt >= targetAltitude *0.95:
                      print "Reached target altitude"
                      break
          time.sleep(1)

# 目標１の緯度・経度、高度を設定する
# aLocation = LocationGlobalRelative(-35.333221765, 149.165237427, 20)

# simple_gotoを実行する
# vehicle.simple_goto(aLocation, groundspeed=20)

print("Set default/target airspeed to 3")
vehicle.airspeed = 3

print("Going towards first point for 30 seconds ...")
point1 = LocationGlobalRelative(-35.361354, 149.165218, 20)
vehicle.simple_goto(point1)

# sleep so we can see the change in map
time.sleep(30)

print("Going towards second point for 30 seconds (groundspeed set to 10 m/s) ...")
point2 = LocationGlobalRelative(-35.363244, 149.168801, 20)
vehicle.simple_goto(point2, groundspeed=10)

# sleep so we can see the change in map
time.sleep(30)

print("Going towards third point for 30 seconds (groundspeed set to 10 m/s) ...")
point2 = LocationGlobalRelative(-35.358244, 149.168801, 20)
vehicle.simple_goto(point2, groundspeed=10)

# sleep so we can see the change in map
time.sleep(30)

print("Returning to Launch")
vehicle.mode = VehicleMode("RTL")

# Close vehicle object before exiting script
print("Close vehicle object")
vehicle.close()