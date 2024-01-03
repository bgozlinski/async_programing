# National Bank of Poland Exchange Rates Tool

## Description
This console tool allows users to fetch the current exchange rates for EUR and USD from the National Bank of Poland (Narodowy Bank Polski). The program uses the public API of the National Bank of Poland to retrieve exchange rate information from the past several days.

## Features
- Fetching exchange rates for EUR and USD up to 10 days.
- Displaying both selling and buying rates.
- Handling network and API query-related errors.

## Requirements
- Python 3.6 or newer
- `aiohttp` library

## Installation
To run the tool, you first need to install the required dependencies. This can be done by running the following command:

```console
pip install  -r requirements.txt
 ```


## Usage
To run the program, use the following command in the console:

```python
python main.py <number_of_days>
```
Where `<number_of_days>` is the number of days backward from which you want to get the currency exchange rates (up to 10 days maximum).
```python
python main.py 5
```
This command will return the exchange rates for EUR and USD from the National Bank of Poland for the past 5 days.

## License
This project is made available under the MIT License. Details can be found in the LICENSE file.

