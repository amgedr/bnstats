# bnstats
Command-line tool for listing Bitcoin network stats from Bitnodes. Documentation
for the API used to get the details of nodes can be found at:

https://bitnodes.21.co/api/

To keep the script responsive the data is downloaded automatically only if the 
file _bnstats.json_ does not exist. To download the latest snapshot manually, 
run bnstats with the _refresh_ command. 

Currently the data can be summerized by countries and service providers hosting 
the Bitcoin nodes. I plan to add more later on.

### Installation
You can download the script by cloning the GitHub repo:
```shell
git clone https://github.com/codehill/bnstats.git
```

bnstats was developed using Python 3 and uses requests and docopt packages. 
To install the requirements run the following command:
```shell
pip3 install -r requirements.txt
```

### Usage
```
bnstats.py [-rt <num>] countries
bnstats.py [-rt <num>] networks
bnstats.py refresh
bnstats.py -h, --help
bnstats.py -v, --version

Options:
  countries                 List total nodes by country
  networks                  List total nodes by ISP
  refresh                   Redownload the data from bitnodes.21.co
  -t <num>, --top <num>     Number of rows returned [default: 10]
  -r, --raw                 Return raw output
  -h, --help                Show this help screen
  -v, --version             Print the version number
```

### Examples
```shell
# Download the latest snapshot from Bitnodes:
bnstats.py refresh

# Output list of top 10 countries
bnstats.py countries

# Output list of top 50 countries
bnstats.py countries -t 50

# Output the top 10 countries in raw format
bnstats.py countries -r
```

### Contributing
* If you've got any suggestions or questions, [please create an issue here](https://github.com/codehill/nbstats/issues).
* If you want to fix a bug or implement a feature, please feel free to do so. Just send me a pull request.

### License
This project is licensed under a MIT license. See the included [LICENSE file](LICENSE) for more details.
