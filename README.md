# Commutes

Calculates distances between address pairs

## Usage

Create data files:

`homes.json` - list of starting addresses
```json
[
  {
    "name": "home",
    "address": "12375 SW 5th St, Beaverton, OR 97005"
  }
]
```

`destinations.json` - List of destination addresses
```json
[
  {
    "name": "work",
    "address": "4033 SW Canyon Rd, Portland, OR 97221"
  },
  {
    "name": "airport",
    "address": "7000 NE Airport Way, Portland, OR 97218"
  }
]
```

Run:
```shell
poetry run commutes
```