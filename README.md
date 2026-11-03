# NR-D3CK
a portable cyberdeck that has built in sensors and tracks live plane data as well as displays a live radio spectrum and planes positions

this is a portable device built with a rpi 5 and a touchscreen in a fully 3d printed case it picks up radio signals from planes overhead and then shows them on a live map, it will also show the radio spectrum nearby wifi and bluetooth connections and statistics such as temperature, humidity, and C02 levels, this will basically make radio signals visible as well as provide other useful information

it features a live plane map with details such as callsigns altitude speed and direction. wifi and bluetooth scanning. sensors and most importantly works completly offline

it works as a plane constantly broadcasts its position speed and id by radio on high frequency and our own decoder finds each message in the raw signal and checks it, a esp32s3 with a custom antenna and software will scan wifi and bluetooth anf send the results to the pi and then the screen will display all of it 

Hardware used will be a pi 5 a toucscreen or just normal screen a sd card esp32s3 and various sensors a 3d printer will be needed for the case as well as a battery pack to power the pi and the esp32s3