# IP Geolocator
A simple API that lets you fetch geolocation based on ip address or URL.

Geolocation the data is stored in database and can be retrieved, listed and deleted.


## Dev environment
1. Place your Ipstack api key the `IPSTACK_ACCESS_KEY` env variable within `/config/dev/config.env` file.
2. `make build`
3. `make run`
4. `make migrate`

You can access the API at `localhost:8000`

## Docs
Openapi specification can be found at `localhost:8000/docs`.