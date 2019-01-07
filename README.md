# customjson [![Build Status](https://travis-ci.com/ludeeus/customjson.svg?branch=master)](https://travis-ci.com/ludeeus/customjson)

_Create json with information for custom_updater._  

## Install

**Require Python version 3.5.3+**

```bash
python3 -m pip install -U customjson
```

### Example

```bash
customjson --token aaabbbccc111222333 --mode component
```

```bash
customjson --token aaabbbccc111222333 --mode component --repo sensor.trakt
```

```bash
customjson --token aaabbbccc111222333 --mode component --repo sensor.trakt --repo sensor.brewdog
```

#### CLI options

param | alias | description
-- | -- | --
`--token` | `-T` | An GitHub `access_token` with `repo` permissions.
`--repo` | `-R` | The repo you want to show info for, can be added multiple times, is optional.
`--push` | `-P` | Push a new `repos.json` file to the information repo.
`--mode` | `-M` | Must be `card` or `component`.
`--version` | `-V` | Print the installed version.

***

[![BuyMeCoffee](https://camo.githubusercontent.com/cd005dca0ef55d7725912ec03a936d3a7c8de5b5/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f6275792532306d6525323061253230636f666665652d646f6e6174652d79656c6c6f772e737667)](https://www.buymeacoffee.com/ludeeus)