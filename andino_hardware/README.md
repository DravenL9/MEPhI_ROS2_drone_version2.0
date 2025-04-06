# MEPhI_ROS2_drone_hardware

Здесь содержится инструкция по изготовлению деталей робота, инструкция по его сборке и список используемых компонентов.

## Перечень компонентов

| Название | Назначение  | Количество | Ссылка |
|---------------------------|-------------------------------|------------|----------|
| Raspberry Pi 4 Model B 8GB | Управление моторами, датчиками и логикой; распознавание объектов, навигация; параллельная работа сенсоров, связи и алгоритмов; управление периферией; локальный сервер и облачная интеграция | 1 шт. | [ozon](https://www.google.com/url?q=https://www.ozon.ru/product/raspberry-pi-4-model-b-8gb-ram-mikrokompyuter-1163024753/?at%3DEqtk4OwkjcxyYBqDFYBJj5ATPY7ZDBhmA4mVztkmj4Wg%26keywords%3Draspberry%2Bpi%2B4%2B8%2Bgb&sa=D&source=editors&ust=1743930234230415&usg=AOvVaw20bc2E_yO2BzEhtXYiAFK-)|
| Датчик-сканер Slamtec RPLIDAR A1 2D          | Сканирует пространство (360°) для построения карты и навигации; помогает роботу ориентироваться в реальном времени             | 1 шт.      | [яндекс маркет](https://market.yandex.ru/product--skaner-slamtec-rplidar-a1-2d-360-gradusov-12-metrov/685634663?sku=103539320004&uniqueId=134799842&ysclid=m947l4wnwr247312525&wprid=1743857252452797-6248306153305500968-balancer-l7leveler-kubr-yp-sas-53-BAL&utm_source_service=web&src_pof=703&icookie=rPZ%2B10rPX3rnEAz267VHI1dleWoMDEWEEALOWV2zGUTH6g3eK%2F7VoUbFb6FyBi8dv9gNTIKhWNiUPHiMrkxG8ho7Ig0%3D&baobab_event_id=m947l4wnwr)|
| Понижающий DC-DC преобразователь RCNUN WG-48S1220 | Понижение напряжения; питание мощных модулей                                                                               | 1 шт.      |[яндекс маркет](https://market.yandex.ru/product--rcnun-ponizhaiushchii-modul-wg8-60s0510/1026632180?sku=103789709049&uniqueId=134799842&do-waremd5=QlmEajFgTw2-g7mo53ingA&ysclid=m947pm66x6512527512)|
| Аккумулятор LiPo Vant-11.1В 5200мАч 50C 3S1P | Питание                                                                                                                       | 1 шт.      |[wildberries](https://www.wildberries.ru/catalog/143636070/detail.aspx)|
| Гироскоп и акселерометр MPU-6050 (GY-521)     | Определение ориентации; стабилизация; инерциальная навигация                                                                  | 1 шт.      |[ozon](https://www.ozon.ru/product/giroskop-akselerometr-gy-521-arduino-mpu-6050-1142582502/?at=w0tglkK0YT3xDNxrFz6xKlpH8qDnGHX75w1wU4Q3PrZ&keywords=mpu+6050&reviewsVariantMode=2&tab=reviews)|
| Драйвер шагового двигателя L298N              | Управление двигателями; ШИМ-контроль                                                                                          | 1 шт.      |[ozon](https://www.ozon.ru/product/drayver-shagovogo-shchetochnogo-dvigatelya-l298n-arduino-1592815273/?at=Z8tXKAlPOIKGEOrLfx8D7xnigxkVoyczWOx7Ntq0R7Bx&keywords=l298n)|
| Мотор с редуктором и энкодером JGY-370B       | Привод с контролем положения; точное управление                                                                               | 1 шт.      |[ozon](https://www.ozon.ru/product/motor-reduktor-jgy-370b-s-enkoderom-12v-90-ob-min-1688683559/?oos_search=false)|
| Плата контроллера Arduino Uno R3 (ATMega 328 / CH340G) | Микроконтроллер; среда разработки; работа с драйверами                                                                    | 1 шт.      |[ozon](https://www.ozon.ru/product/mikrokontroller-arduino-uno-r3-type-c-atmega328-lgt8f328-ch340-1548397969/?at=LZtlBVKNEUX3GgDJUGxNKVMSRJoVEAFwM1VD0I7ARYB5&keywords=Arduino+Uno+R3+CH340G)|
| Винт ISO 7380 А2 М3х10 с полукруглой головкой | Крепежное изделие                                                                                                             | 50 шт.     |[ozon](https://www.ozon.ru/product/vint-iso-7380-a2-m3h10-s-polukrugloy-golovkoy-nerzhaveyka-50-sht-1309301713/)|
| Винт ISO 7380 А2 М3х8 с полукруглой головкой  | Крепежное изделие                                                                                                             | 20 шт.     |[ozon](https://www.ozon.ru/product/vint-iso-7380-a2-m3h8-s-polukrugloy-golovkoy-nerzhaveyka-20-sht-1309302016/?from_sku=1309301713&oos_search=false)|
| Винт ISO 7380 А2 М3х16 с полукруглой головкой | Крепежное изделие                                                                                                             | 10 шт.     |[ozon](https://www.ozon.ru/product/vint-iso-7380-a2-m3h16-s-polukrugloy-golovkoy-nerzhaveyka-10-sht-1088287603/?from_sku=1309301713&oos_search=false)|
| Гайка М3 шестигранная оцинкованная            | Крепежное изделие                                                                                                             | 200 шт.    |[ozon](https://www.ozon.ru/product/gayka-m3-shestigrannaya-200-sht-otsinkovannaya-1706097449/?at=46tR4ENErC81z33WFX71ZDOUWBw8BYsoy7jlGiLgj9m7&keywords=гайка+м3)|
| Стяжка (хомут) нейлоновая пластиковая         | Крепежное изделие                                                                                                             | 100 шт.    |[ozon](https://www.ozon.ru/product/styazhka-homut-neylonovaya-plastikovaya-krepezh-2-5h200mm-1045860514/?at=VvtzqmrmMhE1KADmuYGwqQGtPDZBz6tWJVZgMIo1K12Y&from_sku=1045867806&oos_search=false)|
| Универсальное опорное колесо с нейлоновым шаром | Опорное изделие                                                                                                             | 1 шт.      |[амперкот](https://amperkot.ru/msk/catalog/universalnoe_opornoe_koleso_s_neylonovyim_sharom_1587_mm-39388352.html)|
| Соединительные провода Dupont (Папа-мама)     | Межкомпонентное соединение                                                                                                    | 40 шт.     |[амперкот](https://amperkot.ru/msk/catalog/soedinitelnyie_provoda_dupont__papamama_40sht_raznotsvetnyie_30_sm-23875248.html)|
| Металлические стойки для крепления материнской платы | Крепежное изделие                                                                                                        | 10 шт.     |[ozon](https://www.ozon.ru/product/metallicheskie-prostavki-stoyki-dlya-krepleniya-materinskoy-platy-shestigrannyy-krepezh-m3-7-1020282755/?at=J8tg9l6QphyRZlnwclX78kPUkLr634hqzM9Z8fwM5wrm&keywords=стойка+м3%2A7)|





## Изготовление деталей
[`Изготовление деталей.pdf`](/andino_hardware/Изготовление%20деталей.pdf): инструкция по 3D печати и лазерной резке

Файлы деталей содержатся в [`3D`](/3D/)

## Сборка робота
[`Инструкция по сборке корпуса.pdf`](/andino_hardware/Инструкция%20по%20сборке%20корпуса.pdf): инструкция по сборке корпуса