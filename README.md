# Pi-Eon

##DHT22 Temperature and Humidity Sensor with the Raspberry Pi

###Introduction

Not another blog with a Pi and a temperature sensor you think. But wait, this is different. This includes the Eon, which gives you the power to view the temperature readings in a beautiful graph that updates itself in real time. From anywhere in the world, with just a few lines of code. Real time dashboards, its happening! Who doesnt love a great visualization notifying you in real time!!! 

#GIFS OF THE GRAPHS WITH THE SENSOR

There are 3 parts to this blog;

1. The circuit to sense temperature and humidity.
2. PubNub that lets you publish this value to a browser any where in the world.
3. Eon that is a Javascript library that allows you to chart the data into a  real time graph.

Lets not waste any more time and jump straight into it.


#### What you will need

1.  The DHT22 sensor

![image](images/dht22.png)
2.  3 jumper wires 
3.  Breadboard  
4.  4.7kΩ (or 10kΩ) resistor
5.  Raspberry Pi 2 loaded with the Raspbian OS. 


## what this sensor does?

I chose the DHT22 for this project. The DHT22 is a basic, low-cost digital temperature and humidity sensor. It uses a capacitive humidity sensor and a thermistor to measure the surrounding air, and spits out a digital signal on the data pin.
Simply connect the first pin on the left to 3-5V power, the second pin to your data input pin and the right most pin to ground. 


### Hardware Setup

Set up the circuit according to the following figure: 

![image](images/circuitdht22.png)

which translates to 

![image](images/breadboard.png)

I have connected to GPIO4 (pin7), pin 1 for the voltage (3v3) and pin 6 for ground. The resistor goes between the first two pins of the sensor. The third pin of the sensor need not be connected to anything.

### Script to read the sensor values

Lets quickly go through the python script to see how to stream realtime temperature readings collected by the DHT22. In order to run PubNub on the Pi, you will have to run the following commands on your terminal.


Import the necessary libraries, and also PubNub to be able to send and receive messages to/from the Pi to any other device. 

####Installing PubNub


Open LXTerminal, and download and install the followings:

**Install Python:**
`pi@raspberrypi ~$ sudo apt-get install python-dev`

**Install pip:**
`pi@raspberrypi ~$ sudo apt-get install python-pip`

**install PubNub:**
`pi@raspberrypi ~$ sudo pip install pubnub`

For an in depth introduction to the Pi and PubNub, check this [blog](http://www.pubnub.com/blog/internet-of-things-101-getting-started-w-raspberry-pi/) by [Tomomi](ADD LINK TO HER BIO HERE)

Make sure you have [signed up for PubNub](https://www.pubnub.com/get-started/) to obtain your pub/sub keys.

We need to use Adafruits DHT library to be able to read the temperature values from the sensor.

The Python code to work with Adafruit's DHT sensors is available on Github at https://github.com/adafruit/Adafruit_Python_DHT. 

**Downloading the Adafruit DHT liibrary:**

`pi@raspberrypi ~$ git clone https://github.com/adafruit/Adafruit_Python_DHT.git`
`pi@raspberrypi ~$ cd Adafruit_Python_DHT`

#### Code walk through

We need to import the libraries required for this project. We also need to initialize a PubNub object and use the publish subscribe keys which you got while signing up.

```
	import os
	import time
	import sys
	from Pubnub import Pubnub
	import Adafruit_DHT as dht
	pubnub = Pubnub(publish_key='Enter_your_publish_keys', 	subscribe_key='Enter_your_subscribe_keys')
	channel = 'tempeon'
```

##### The exciting part of the project : 

Using the `read.retry` method from the Adafruit_DHT library, we can obtain the temperature denoted by 't' and 'h' respectively. 

The rest is just publishing these values in a way that **Eon** understands. We publish the temperaure on a channel called **temp_eon** and the humidity on **hum_eon**. This whole thing repeats till the program is terminated so this way you can get constant temperature and humidity readings. 

**PubNub** lets you view these readings remotely and with **Eon** you can create beautiful real time graphs in a matter of minutes. In this example, I am plotting the temperature as a line graph, and the humidity on a gauge graph.

```     
def callback(message):
    print(message)

while True:
    h,t = dht.read_retry(dht.DHT22, 4)
    pubnub.publish('tempeon', {
        'columns': [
            ['x', time.time()],
            ['temperature_celcius', t]
            ]

        })
    pubnub.publish('humeon', {
        'columns': [
            ['humidity', h]
            ]

        })
```


### What is Eon, ease of use

So what is this magical [Eon](http://www.pubnub.com/developers/eon/)? PubNub's Project EON connects C3 charts and Mapbox's map widget to the [PubNub Data Stream Network](http://www.pubnub.com).

```

eon.chart({
	history: true,
    channel: 'tempeon',
    flow: true,
    generate: {
    	bindto: '#chart',
    	data: {
      		x: 'x',
      		labels: false
    	},
    	axis : {
      		x : {
        		type : 'timeseries',
        		tick: {
          			format: '%H:%M:%S'
        		}
      		}
    	}
  	}
});


```
Project Eon provides very easy to understand code, that can be copy pasted. You can choose from different types of [charts](https://github.com/pubnub/eon-chart) - Spline, Donut, Gauge and Bar chart. 
visualization is always easier than seeing a bunch of text on the screen, and with Eon you just need a browser. Doesn't matter what you are working with; as long as the hardware, sensors, chips or mobile devices talks PubNub, you can publish to Eon and create great real time dashboards.



### What can you do with Project Eon?

Now you can collect data from countless devices and publish data in realtime to live-updating charts, maps and graphs. You can react immediately to the data that you are seeing. This data can be from several sensors, all on one graph, so you can see it in one place. You can also use it for vehicle location and state on a live-updating map. Or even financial data in a stock trading application.


You can find detailed documentation at [Project EON homepage](http://www.pubnub.com/blog/project-eon-open-source-javascript-framework-for-realtime-dashboard-charts-and-maps/) or [check out the Project EON GitHub repository](https://github.com/pubnub/eon). 


GO EON"-ify"" your next cool project. 
