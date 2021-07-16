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

type Current struct {
	CurrentWeather Weather `json:"current"` 
}

type AirQuality struct {
	OzoneLevel float64 `json:"o3"`
}

type Weather struct {
	AQI AirQuality `json:"air_quality"`
	Temperature float64 `json:"temp_c"`
	Humidity float64 `json:"humidity"`
	Pressure float64 `json:"pressure_mb"`
	Visibility float64 `json:"vis_km"`
	WindSpeed float64 `json:"gust_kph"`
}

func main() {
	key := getKey()
	for _, i := range call(29.8280859, -95.2840958, key){
		fmt.Println(i)
	}
}

func getKey() string {
	keyFile, err := os.Open("data/API_keys.json")

	if err != nil {
		fmt.Println(err)
	}

	defer keyFile.Close()

	byteValue, _ := ioutil.ReadAll(keyFile)

	var result map[string]interface{}

	json.Unmarshal(byteValue, &result)

	return result["WA_API"].(string)
}

func call(lat float64, long float64, key string) [6]float64 {
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

	return [6]float64{
		data.CurrentWeather.AQI.OzoneLevel,
		data.CurrentWeather.Temperature,
		data.CurrentWeather.Temperature - (100 - data.CurrentWeather.Humidity) / 5, // Simple dew-point approximation
		data.CurrentWeather.Pressure,
		data.CurrentWeather.Visibility,
		data.CurrentWeather.WindSpeed / 3.2, // Convert to m/s
	}
}