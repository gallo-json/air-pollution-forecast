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
)

type AQI struct {
	Key string `json:"WA_API"`
}

func main() {
	jsonFile, err := os.Open("data/API_keys.json")

	if err != nil {
		fmt.Println(err)
	}
	fmt.Println("Successfully Opened users.json")
	// defer the closing of our jsonFile so that we can parse it later on
	defer jsonFile.Close()
}

func call(lat int, long int) {
	resp, err := http.Get("http://api.weatherapi.com/v1/current.json?key=55f31beac75e4bd09e7135959210303&q=London&aqi=yes")
	if err != nil {
		// handle error
	}
	fmt.Println(resp)
}