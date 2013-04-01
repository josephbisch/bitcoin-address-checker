import sys
import getopt
import urllib2
import json

""" This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>."""

# Usage: python check_addresses.py <addresses>
# Example: python check_addresses.py 1dice97ECuByXAvqXpaYzSaQuPVvrtmz6 1dice5wwEZT2u6ESAdUGG6MHgCpbQqZiy

def main(argv):
    if argv == []:
        print '###Example###'
        print 'Usage: python check_addresses.py <addresses>'
    try:
        opts, args = getopt.getopt(argv, "h")
    except getopt.GetoptError:
        print 'Usage: python check_addresses.py <addresses>'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print 'Usage: python check_addresses.py <addresses>'
            sys.exit()
    addresses = []
    for arg in args:
        addresses.append(arg)
            
    exchange_url = "https://blockchain.info/ticker"
    if(addresses == []):
        addresses = ["1933phfhK3ZgFQNLGSDXvqCn32k2buXY8a","1FeexV6bAHb8ybZjqQMjJrcCrHGW9sb6uF","1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa"]

    # Key is bitcoin address, value is list containing BTC balance,
    # last price, 15 minute price, 24 hour price.
    data = {}

    # The length of the longest BTC balance, last price, 15 min price,
    # 24 hour price (used for printing output).
    max_lengths = [0,0,0,0]

    # The total BTC balance, last price, 15 minute price, 24 hour price.
    totals = [0,0,0,0]

    # The length of the longest address (used for printing output).
    max_address_length = 0    

    # Figure out longest address
    for address in addresses:
        if len(address) > max_address_length:
            max_address_length = len(address)

    exchange_rates = json.loads(urllib2.urlopen(exchange_url).read())["USD"]

    print "\n"
    print "last: $" + str(exchange_rates["last"])
    print "15m:  $" + str(exchange_rates["15m"])
    print "24h:  $" + str(exchange_rates["24h"])

    for address in addresses:
        data[address] = []
        f = urllib2.urlopen("https://blockchain.info/q/addressbalance/"+address)
        data[address].append(int(f.read())/1e8)
        data[address].append(data[address][0]*exchange_rates["last"])
        data[address].append(data[address][0]*exchange_rates["15m"])
        data[address].append(data[address][0]*exchange_rates["24h"])
        # Calculate totals and figure out maximum length
        for i in range(len(data[address])):
            if len(str(int(data[address][i]))) > max_lengths[i]:
                max_lengths[i] = len(str(int(data[address][i])))
            totals[i] += data[address][i]
            if len(str(int(totals[i]))) > max_lengths[i]:
                max_lengths[i] = len(str(int(totals[i])))

    for address in addresses:    
        print address + " - " + ("{:"+str(max_lengths[0]+9)+".8f}").format(data[address][0]) + " BTC" \
              + " - " + "$" + ("{:"+str(max_lengths[1]+3)+".2f}").format(data[address][1])\
              + " - " + "$" + ("{:"+str(max_lengths[2]+3)+".2f}").format(data[address][2]) \
              + " - " + "$" + ("{:"+str(max_lengths[3]+3)+".2f}").format(data[address][3])

    print "Total" + " "*(max_address_length-5) + " - " + ("{:"+str(max_lengths[0]+9)+".8f}").format(totals[0]) + " BTC" \
          + " - " + "$" + ("{:"+str(max_lengths[1]+3)+".2f}").format(totals[1])\
          + " - " + "$" + ("{:"+str(max_lengths[2]+3)+".2f}").format(totals[2]) \
          + " - " + "$" + ("{:"+str(max_lengths[3]+3)+".2f}").format(totals[3])

if __name__ == "__main__":
    main(sys.argv[1:])

