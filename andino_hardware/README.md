# andino_hardware

Здесь содержится инструкция по изготовлению деталей робота, инструкция по его сборке и список используемых компонентов.

## Перечень компонентов

| Название | Назначение  | Количество | Ссылка |
|---------------------------|-------------------------------|------------|----------|
| Raspberry Pi 4 Model B 8GB | Управление моторами, датчиками и логикой; распознавание объектов, навигация; параллельная работа сенсоров, связи и алгоритмов; управление периферией; локальный сервер и облачная интеграция. | 1 шт. | [ozon](https://www.google.com/url?q=https://www.ozon.ru/product/raspberry-pi-4-model-b-8gb-ram-mikrokompyuter-1163024753/?at%3DEqtk4OwkjcxyYBqDFYBJj5ATPY7ZDBhmA4mVztkmj4Wg%26keywords%3Draspberry%2Bpi%2B4%2B8%2Bgb&sa=D&source=editors&ust=1743930234230415&usg=AOvVaw20bc2E_yO2BzEhtXYiAFK-)|
| Датчик-сканер Slamtec RPLIDAR A1 2D          | Сканирует пространство (360°) для построения карты и навигации; помогает роботу ориентироваться в реальном времени.             | 1 шт.      | [яндекс маркет](https://market.yandex.ru/product--skaner-slamtec-rplidar-a1-2d-360-gradusov-12-metrov/685634663?sku=103539320004&uniqueId=134799842&ysclid=m947l4wnwr247312525&wprid=1743857252452797-6248306153305500968-balancer-l7leveler-kubr-yp-sas-53-BAL&utm_source_service=web&src_pof=703&icookie=rPZ%2B10rPX3rnEAz267VHI1dleWoMDEWEEALOWV2zGUTH6g3eK%2F7VoUbFb6FyBi8dv9gNTIKhWNiUPHiMrkxG8ho7Ig0%3D&baobab_event_id=m947l4wnwr)|
| Понижающий DC-DC преобразователь RCNUN WG-48S1220 | Понижение напряжения; питание мощных модулей.                                                                               | 1 шт.      |[яндекс маркет](https://market.yandex.ru/product--rcnun-ponizhaiushchii-modul-wg8-60s0510/1026632180?sku=103789709049&uniqueId=134799842&do-waremd5=QlmEajFgTw2-g7mo53ingA&ysclid=m947pm66x6512527512)|
| Аккумулятор LiPo Vant-11.1В 5200мАч 50C 3S1P | Питание.                                                                                                                       | 1 шт.      |[wildberries](https://www.wildberries.ru/catalog/143636070/detail.aspx)|
| Гироскоп и акселерометр MPU-6050 (GY-521)     | Определение ориентации; стабилизация; инерциальная навигация.                                                                  | 1 шт.      |[ozon](https://www.ozon.ru/product/giroskop-akselerometr-gy-521-arduino-mpu-6050-1142582502/?at=w0tglkK0YT3xDNxrFz6xKlpH8qDnGHX75w1wU4Q3PrZ&keywords=mpu+6050&reviewsVariantMode=2&tab=reviews)|
| Драйвер шагового двигателя L298N              | Управление двигателями; ШИМ-контроль.                                                                                          | 1 шт.      |[ozon](https://www.ozon.ru/product/drayver-shagovogo-shchetochnogo-dvigatelya-l298n-arduino-1592815273/?at=Z8tXKAlPOIKGEOrLfx8D7xnigxkVoyczWOx7Ntq0R7Bx&keywords=l298n)|
| Мотор с редуктором и энкодером JGY-370B       | Привод с контролем положения; точное управление.                                                                               | 1 шт.      |[ozon](https://www.ozon.ru/product/motor-reduktor-jgy-370b-s-enkoderom-12v-90-ob-min-1688683559/?oos_search=false)|
| Плата контроллера Arduino Uno R3 (ATMega 328 / CH340G) | Микроконтроллер; среда разработки; работа с драйверами.                                                                    | 1 шт.      |[ozon](https://www.ozon.ru/product/mikrokontroller-arduino-uno-r3-type-c-atmega328-lgt8f328-ch340-1548397969/?at=LZtlBVKNEUX3GgDJUGxNKVMSRJoVEAFwM1VD0I7ARYB5&keywords=Arduino+Uno+R3+CH340G)|
| Винт ISO 7380 А2 М3х10 с полукруглой головкой | Крепежное изделие.                                                                                                             | 50 шт.     |[ozon](https://www.ozon.ru/product/vint-iso-7380-a2-m3h10-s-polukrugloy-golovkoy-nerzhaveyka-50-sht-1309301713/)|
| Винт ISO 7380 А2 М3х8 с полукруглой головкой  | Крепежное изделие.                                                                                                             | 20 шт.     |[ozon](https://www.ozon.ru/product/vint-iso-7380-a2-m3h8-s-polukrugloy-golovkoy-nerzhaveyka-20-sht-1309302016/?from_sku=1309301713&oos_search=false)|
| Винт ISO 7380 А2 М3х16 с полукруглой головкой | Крепежное изделие.                                                                                                             | 10 шт.     |[ozon](https://www.ozon.ru/product/vint-iso-7380-a2-m3h16-s-polukrugloy-golovkoy-nerzhaveyka-10-sht-1088287603/?from_sku=1309301713&oos_search=false)|
| Гайка М3 шестигранная оцинкованная            | Крепежное изделие.                                                                                                             | 200 шт.    |[ozon](https://www.ozon.ru/product/gayka-m3-shestigrannaya-200-sht-otsinkovannaya-1706097449/?at=46tR4ENErC81z33WFX71ZDOUWBw8BYsoy7jlGiLgj9m7&keywords=гайка+м3)|
| Стяжка (хомут) нейлоновая пластиковая         | Крепежное изделие.                                                                                                             | 100 шт.    |[ozon](https://www.ozon.ru/product/styazhka-homut-neylonovaya-plastikovaya-krepezh-2-5h200mm-1045860514/?at=VvtzqmrmMhE1KADmuYGwqQGtPDZBz6tWJVZgMIo1K12Y&from_sku=1045867806&oos_search=false)|
| Универсальное опорное колесо с нейлоновым шаром | Опорное изделие.                                                                                                             | 1 шт.      |[амперкот](https://amperkot.ru/msk/catalog/universalnoe_opornoe_koleso_s_neylonovyim_sharom_1587_mm-39388352.html)|
| Соединительные провода Dupont (Папа-мама)     | Межкомпонентное соединение.                                                                                                    | 40 шт.     |[амперкот](https://amperkot.ru/msk/catalog/soedinitelnyie_provoda_dupont__papamama_40sht_raznotsvetnyie_30_sm-23875248.html)|
| Металлические стойки для крепления материнской платы | Крепежное изделие.                                                                                                        | 10 шт.     |[ozon](https://www.ozon.ru/product/metallicheskie-prostavki-stoyki-dlya-krepleniya-materinskoy-platy-shestigrannyy-krepezh-m3-7-1020282755/?at=J8tg9l6QphyRZlnwclX78kPUkLr634hqzM9Z8fwM5wrm&keywords=стойка+м3%2A7)|





## Изготовление деталей
[`Изготовление деталей.pdf`](/andino_hardware/Изготовление%20деталей.pdf): инструкция по 3D печати и лазерной резке

Файлы деталей содержатся в [`3D`](/3D/)

## Сборка робота
[`Инструкция по сборке корпуса.pdf`](/andino_hardware/Инструкция%20по%20сборке%20корпуса.pdf): инструкция по сборке корпуса



## Single Board Computer (SBC)

The SBC used in this project is a Raspberry Pi 4b so the guidelines here will refer particularly to this family of on-board computers, however extending its use to other families is possible as well.

This section details the required configuration that is needed in the SBC.
You can either follow these steps or **rely on community contribution (Recommended) for installing this via ansible playbooks**: See https://github.com/garyservin/andino_ansible_config

### Operative System

Ubuntu Mate 22.04 ARM64 is the recommended operative system for this project. This OS provides good capabilities for a educational platform as well as good performance.

For installing this OS in the Raspberry:
1. Download the image from here: [ubuntu mate download](https://ubuntu-mate.org/download/arm64/)


2. Install OS to a microSD card using [Raspberry Pi Imager](https://www.raspberrypi.com/software/).
   - No extra configuration should be necessary.

3. Boot your raspberry using the microSD and a HDMI connection. Some initial configuration is necessary. Follow the wizard for a proper set up. It is recommended to use simple User and Password combinations for the user. For example:
    - user: pi
    - password: admin

4. Once is done, run `sudo apt update && sudo apt upgrade` in a terminal for updating the system. Then reboot.

### Installing dependencies

Some packages are necessary to be installed towards a correct set up of the robot's on-board computer.

#### ssh-server

In general, you will want to access to the Raspberry remotely via `ssh` connection while being connected in the same network.
So we need to install `ssh-server`;
```
sudo apt-get install openssh-server
```
Enable it if it is not enabled yet:
```
sudo systemctl enable ssh --now
```

After this you will be able to access this device from a remote computer by doing:
```
ssh <user>@<ip>
```
For example if the user is `pi` and the ip is `192.168.0.102`
```
ssh pi@192.168.0.102
```


#### Common utilities

Install some common utilities that will be required later on.

```
sudo apt update
```

```
sudo apt install git net-tools software-properties-common build-essential -y
```
```
sudo apt install python3-rosdep2 python3-catkin-pkg python3-catkin-pkg-modules python3-rospkg-modules python3-rospkg  -y
```

#### Install ROS

Follow suit the instructions for installing next dependencies from binaries:
 - [ROS 2 Humble](https://docs.ros.org/en/humble/Installation/Ubuntu-Install-Debians.html)
 - [Colcon](https://colcon.readthedocs.io/en/released/user/installation.html)

To automatically source ROS installation, it is recommended to add `source /opt/ros/humble/setup.bash` line to the `~/.bashrc` file.

#### Arduino

Arduino drivers are necessary for the SBC (Raspberry) <--> Microcontroller(Arduino) serial communication.

```
sudo apt install arduino
```

Configure it properly:
1. Add user to `dialout` and `plugdev` groups:
   ```
   sudo usermod -a -G dialout $USER
   ```
   ```
   sudo usermod -a -G plugdev $USER
   ```
   Note you will need a reboot after this to be effective.
2. Remove `brltty` from the system
   ```
   sudo apt remove brltty
   ```
   In Ubuntu 22.04 seems to be an issue with some chip drivers and the `brltty` daemon. To avoid this conflict we remove `brltty` as suggested. See [this stackoverflow post](https://stackoverflow.com/questions/70123431/why-would-ch341-uart-is-disconnected-from-ttyusb) for further information.



#### Raspberry Camera Module V2

After connecting the camera module to the Raspberry's camera port.
```
sudo apt install libraspberrypi-bin v4l-utils
```
```
sudo usermod -aG video $USER
```

Check camera status:
```
vcgencmd get_camera
```

If the output of the previous command is `supported=1 detected=1', everything is fine. If not, your camera won't work correctly, you need to perform some configuration first.

Modify the `config.txt` file for the boot:

```sh
 sudo nano /boot/firmware/config.txt
```

And add these lines:

```
# Autoload overlays for any recognized cameras or displays that are attached
# to the CSI/DSI ports. Please note this is for libcamera support, *not* for
# the legacy camera stack
start_x=1
gpu_mem=128
```

Save and close the file. Then we need to enable the camera support for the raspberry:

```sh
sudo raspi-config
```

Go to `Interface Options`, select `camera` and enable it.

Finally, you just need to reboot and the camera should be working fine.

#### RPLidar installation

The installation of the A1M8 RPLidar sensor is quite straight forward and a ros integration package will be installed later on via `rosdep`.

For now, after connecting it to the usb port:
 1. Verify USB connection: Green light in the usb conversor(A1M8 side board) should be turned on.
 2. Check the authority of RPLidar's serial-port:
    - `ls -l /dev |grep ttyUSB`
    - Add extra bits by doing `sudo chmod 666 /dev/ttyUSB<number_of_device>`

### USB Port name configuration

#### Fixed USB port names

As having multiple USB devices connected to the USB ports of the Raspberry Pi, the automatically assigned USB port numbers could unexpectedly change after a reboot.
To avoid assigning your device to a `tty_USBX` number that isn't the correct one we should assign fixed USB port name for each connected device.

The idea is to be able to generate a link between the real `ttyUSBX` port and an invented one. For this we will need to create rules, that every time the Raspberry Pi boots are executed, and therefore we
always point to the correct port name.

In order to create fixed names for the USB devices follow the instructions:

1. Check the devices you have connected:
    ```
    sudo dmesg | grep ttyUSB
    ```

    ```
    [  10.016170] usb 1-1.2: ch341-uart converter now attached to ttyUSB0
    [ 309.186487] usb 1-1.1: cp210x converter now attached to ttyUSB1
    ```
    In the setup where this was tested we have:
      -> Arduino Microcontroller -> _usb 1-1.2: ch341-uart converter now attached to ttyUSB0_
      -> A1M8 Lidar Scanner -> _usb 1-1.1: cp210x converter now attached to ttyUSB1_

    _Note: If you don't know how to identify each one you can simply connect them one by one and check this output._

2. Look for attributes for each device that we will use to anchor a particular device with a name.
  We will use the `idProduct` and `idVendor` of each device.
   - Arduino Microcontroller:
      ```
      udevadm info --name=/dev/ttyUSB0 --attribute-walk
      ```
      You should look for the `idProduct` and `idVendor` under the category that matches the usb number(1-1.X):
      In this case the `ttyUSB0` was referenced to the `usb 1-1.2`, so go to that section and find the ids:
      ```
        ATTRS{idProduct}=="7523"
        ATTRS{idVendor}=="1a86"
      ```
   - Lidar Scanner
      ```
      udevadm info --name=/dev/ttyUSB1 --attribute-walk
      ```
      In this case the `ttyUSB0` was referenced to the `usb 1-1.1`, so go to that section and find the ids:
      ```
        ATTRS{idProduct}=="ea60"
        ATTRS{idVendor}=="10c4"
      ```

3. Create the rules:

    Open the file:
    ```
    sudo nano /etc/udev/rules.d/10-usb-serial.rules
    ```

    Add the following:

    ```
    SUBSYSTEM=="tty", ATTRS{idProduct}=="7523", ATTRS{idVendor}=="1a86", SYMLINK+="ttyUSB_ARDUINO"
    SUBSYSTEM=="tty", ATTRS{idProduct}=="ea60", ATTRS{idVendor}=="10c4", SYMLINK+="ttyUSB_LIDAR"
    ```
    Note that in the `symlink` field a fixed name is indicated.

4. Re-trigger the device manager:
    ```
    sudo udevadm trigger
    ```

5. Verify
    ```
    ls -l /dev/ttyUSB*
    ```
    ```
    crw-rw---- 1 root dialout 188, 0 Sep  2 15:09 /dev/ttyUSB0
    crw-rw---- 1 root dialout 188, 1 Sep  2 15:09 /dev/ttyUSB1
    lrwxrwxrwx 1 root root         7 Sep  2 15:09 /dev/ttyUSB_ARDUINO -> ttyUSB0
    lrwxrwxrwx 1 root root         7 Sep  2 15:09 /dev/ttyUSB_LIDAR -> ttyUSB1
    ```

Done! You can always use your devices by the fixed names without using the port number.
Here, `ttyUSB_ARDUINO` and `ttyUSB_LIDAR` are fixed names for the Arduino Microcontroller and the Lidar Scanner respectively.

For more information you can take a look at this external tutorial: [Here](https://www.freva.com/assign-fixed-usb-port-names-to-your-raspberry-pi/)

### Create robot workspace

Let's create our workspace and build from source this repository.

```
cd ~
```
```
mkdir robot_ws/src -p
```
Clone this repository in the `src` folder
```
cd robot_ws/src
```
```
git clone <repository_address>
```
Install dependencies via rosdep:
```
cd ~/robot_ws
```
When it is the first time you run `rosdep`:
```
rosdep update
```
Make sure to export the `ROS_DISTRO` environment variable:
```
export ROS_DISTRO=humble
```
And then proceed to install the workspace dependencies:
```
rosdep install --from-paths src -i -y -r
```
Note that option `-r` has been added. For ARM based processors, there are missing packages, e.g. those related to simulation. We would not try to run the simulation in the compute platform of andino, however for convenience it is added here.

Let' source the ROS Humble installation:
```
source /opt/ros/humble/setup.bash
```
Let's build the packages (`andino_gz_classic` and `andino_apps` work only in simulation):
```
colcon build --packages-skip andino_gz_classic andino_apps
```
After building is completed:
```
source install/setup.bash
```

After this, you are good to go and use the robot!
Refer to [`usage`](../README.md#usage) section.

### Extra Recommendations & Tools

#### Network
Via terminal the wifi connection can be switched by doing:

List available wifi networks:
```
sudo nmcli dev wifi list
```
Connect to the desired one:
```
sudo nmcli --ask dev wifi connect <SSID>
```

#### Copy files remotely

Using `scp` is a useful tool when copying files remotely over `ssh`.

For copying a folder from host to remote unit:
```
scp -r <path/to/folder> <remote_user>@<remote_ip>:<remote_path_to_folder>
```

#### ROS Domain ID

The domain ID is used by DDS to compute the UDP ports that will be used for discovery and communication.

When using a "public" network using the domain id is a good technique to avoid extra noise with other ROS 2 system in the same network.

See [ROS_DOMAIN_ID](https://docs.ros.org/en/humble/Concepts/Intermediate/About-Domain-ID.html)

TLDR? Export an environment variable with the same ID in **all** ROS 2 clients in the network for a correct discovery.
```
export ROS_DOMAIN_ID=<a_number_between_0_and_101>
```

#### Using joystick for teleoperation

[`andino_bringup`](../andino_bringup/launch/teleop_joystick.launch.py) package provides a launch file for launching the corresponding `ROS 2` nodes for teleoperating the robot using a joystick.

It is worth mentioning that a set up might be needed depending on the gamepad you are using. Here some general guidelines:
 - In case you are using a _Xbox One Controller_ and you want use it wireless (via USB Wirless Dongle) installing [Xone](https://github.com/medusalix/xone) is recommended.
 - Verify that your joystick is actually working on Ubuntu:
    - Some tools that might be useful:
      - `sudo apt install joystick jstest-gtk evtest`
    - Run `evtest` to check if your pad is connected:
      ```
      $ evtest
        No device specified, trying to scan all of /dev/input/event*
        Not running as root, no devices may be available.
        Available devices:
          /dev/input/event22:	Microsoft X-Box One pad

      ```
    - Alternatively, you can use `jstest-gtk` to check the controller, you will find a pretty GUI to play with.
