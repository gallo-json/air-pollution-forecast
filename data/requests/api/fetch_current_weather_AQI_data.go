/* 
Fetch DAILY weather and AQI data
https://www.weatherapi.com


Written in Go because I am trying to learn Go.
*/
package main

import (
	"fmt"
	"net/http"
	"os"
	"encoding/json"
	"io/ioutil"
	"log"
)

type API struct {
	Key string `json:"WA_API"`
}

type Weather struct {
	AQI string `json:"o3"`
	Humidity string `json:"humidity"`
	Pressure string `json:"pressure_mb"`
	Visibility string `json:"vis_km"`
	WindSpeed string `json:"gust_kph"`
}

func main() {
	key := getKey()
	call(29.8280859, -95.2840958, key)
}

func getKey() string {
	keyFile, err := os.Open("data/API_keys.json")

	if err != nil {
		fmt.Println(err)
	}

	defer keyFile.Close()

	byteValue, _ := ioutil.ReadAll(keyFile)

	var key API

	json.Unmarshal(byteValue, &key)
	return key.Key
}

func call(lat float32, long float32, key string) {
	resp, err := http.Get(fmt.Sprintf("http://api.weatherapi.com/v1/current.json?key=%s&q=%f,%f&aqi=yes", key, lat, long))
	if err != nil {
		log.Fatalln(err)
	}
	 
	body, err := ioutil.ReadAll(resp.Body)

	if err != nil {
		log.Fatalln(err)
	}

	var data Current

	json.Unmarshal(body, &data)
}