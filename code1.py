# Function to read the lookup table from a CSV file
def make_lookup(file):
    lookup_table = {}
    with open(file, 'r') as f:
        next(f)  # Skip the header row
        for line in f:
            row = line.strip().split(',')  # Split the line by comma
            dst_port = row[0]
            protocol = row[1].lower()  # Convert protocol to lowercase to match with logs
            tag = row[2]
            lookup_table[(dst_port, protocol)] = tag
    return lookup_table


def make_protocolmapping(file):
    protocol_mapping = {}
    with open(file, 'r') as f:
        next(f)  # Skip the header row
        for line in f:
            # Remove leading/trailing whitespace and strip newline characters
            line = line.strip()
            # Find the first two commas, which separate the first two fields
            first_comma = line.find(',')
            second_comma = line.find(',', first_comma + 1)
            # Extract the first two fields
            number = line[:first_comma]
            name = line[first_comma + 1:second_comma].strip().lower()
            # The rest of the line after the second comma is treated as one field (could be large with commas)
            rest_of_line = line[second_comma + 1:].strip()
            # Store the mapping
            protocol_mapping[number] = name

    return protocol_mapping



# Function to read and process the logs from the file
def read_flow_logs(file):
    with open(file, 'r') as f:
        lines = f.readlines()
    logs = []
    for l in lines:
        parts = l.split()
        log = {
            "Destination Port": parts[6],
            "Protocol": parts[7]
        }
        logs.append(log)
    return logs

# Function to count the tags based on logs, lookup table, and protocol mapping
def count_tags(logs, lookup_table, protocol_mapping):
    tag_counts = {}
    untagged_count = 0
    port_protocol_counts = {}

    for log in logs:
        dst_port = log["Destination Port"]
        protocol_number = log["Protocol"]
        
        # Map protocol number to protocol name
        protocol_name = protocol_mapping.get(protocol_number, 'undefined')
        
        # Lookup the tag
        tag = lookup_table.get((dst_port, protocol_name), 'Untagged')
        
        if tag == 'Untagged':
            untagged_count += 1
        else:
            tag_counts[tag] = tag_counts.get(tag, 0) + 1
        
        # Count port/protocol combinations
        port_protocol_key = (dst_port, protocol_name)
        port_protocol_counts[port_protocol_key] = port_protocol_counts.get(port_protocol_key, 0) + 1

    return tag_counts, untagged_count, port_protocol_counts

# Function to write the output to a text file
def write_output_to_file(output_file, tag_counts, untagged_count):
    with open(output_file, 'w') as file:
        file.write("Tag,Count\n")
        for tag, count in tag_counts.items():
            file.write(f"{tag},{count}\n")
        file.write(f"Untagged,{untagged_count}\n")


# Function to write port/protocol combination counts to a text file
def write_port_protocol_counts_to_file(output_file, port_protocol_counts):
    with open(output_file, 'w') as file:
        file.write("Port,Protocol,Count\n")
        for (port, protocol), count in port_protocol_counts.items():
            file.write(f"{port},{protocol},{count}\n")

# Read the lookup table and protocol mapping
lookup_table = make_lookup('lookup.csv')
protocol_mapping = make_protocolmapping('protocol-numbers.csv')

# Read and process the logs
logs = read_flow_logs('input.txt')

# Count the tags
tag_counts, untagged_count, port_protocol_counts = count_tags(logs, lookup_table, protocol_mapping)

# Write the output to the file
write_output_to_file('output1.txt', tag_counts, untagged_count)

write_port_protocol_counts_to_file('output2.txt', port_protocol_counts)

print("\n\nOutput has been written to the output files\n\n")
