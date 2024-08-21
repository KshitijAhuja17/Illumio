# Project Title
Illumio Engineering Assessment

## Project Overview
This project was done by Kshitij Ahuja as part of his assessment with Illumio. The project challenged him to complete **two mappings**, one from the input flow logs to a provided lookup table, and the other from the input logs to its corresponding protocol and tag.


## Assumptions

- The flow logs and lookup table are clean and follow the specified format and stored in *input.txt*. The flow logs should be Version 2 fom the provided [link](https://docs.aws.amazon.com/vpc/latest/userguide/flow-log-records.html). A new log starts from a new line and there are no additional spaces.

- The lookup table is provided as a CSV as per the challenge instructions and stored in *lookup.csv*. The lookup table can also be a text file with minor code modifications.

- The lookup table should have unique keys with the keys being a combination of (dstport, protocol). If a duplicate occurs, the latest key:value pair will be considered from the lookup table.

- In order to map protocol number to protocol name, the *protocol-number.csv* file from the above link is used. This is essential to map protocol number from the flow logs to the corresponding protocol names. In the given example, the protocol is only 6 (TCP) but that may not always be the case.

- 
## Approach
The first aspect of the assessment was to map the destination port and protool number from the flow logs to its corresponding tag.

For example,

 2 123456789012 eni-1a2b3c4d 10.0.1.102 172.217.7.228 1030 ___443 6___ 8 4000 1620140661 1620140721 ACCEPT OK 

In this log, the destination port is 443 and the protocol number is 6. There are the only 2 fields needed for the mapping.

First, the protocol number is converted to its protocol name. In order to do that, I made a function named *make_protocolmapping(file):*. This first read the file - _protocol-numbers.csv_ and creates a dictionary that maps the protocol number to the protocol name.

Then, using this dictionary, the protocol number from the logs is converted to its name. Once we have the destination port and protocol name, we can map it to the provided lookup table.

In order to use the lookup table, I made a function titled *make_lookup(file):*. This first reads the CSV storing the lookup, and then coverts it to a dictionary with the key being  (dstport, protocol) and value being the tag.

Using this lookup table, I can get the count of matching tags. I made a function titled - *count_tags(logs, lookup_table, protocol_mapping):* for this. For each log, it tries to find a matching key in the lookup table and increases the count of that pair by 1. It also accounts for non-matching tags and marks them as "Untagged".

The same function also the count of each (dstport, protocol name) combination.

The next step is to write the tag count to a text file as output. The first required output is stored as *output1.txt* when the Python file is run.

The Port,Protocol,Count is also written to a text file titled *output2.txt*.



## Technologies Used
**Python** was the programming language used for this challenge. 

I also got the protocol-numbers to keyword mapping from the provided [link](https://www.iana.org/assignments/protocol-numbers/protocol-numbers.xhtml). I downloaded it as a CSV and used that.

## Installation
- Ensure Python 3 is installed on the system.
- The files -- *code1.py*, *lookup.csv*, *input.txt*, and *protocol-numbers.csv* must be in the same folder.
- Run the file *code1.py* via an IDE or type *python code1.py* into the terminal.
- The output files are generated as *output1.txt* and output2.txt*, as per the instructions.