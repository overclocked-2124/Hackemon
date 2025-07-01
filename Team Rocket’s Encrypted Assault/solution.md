# Silph Co. Network Under Attack: The Cyber Trainer’s Challenge

## Challenge Description

Team Rocket has launched a cunning cyberattack on the Silph Co. network, embedding secret messages deep inside malicious network packets. As a skilled Cyber Trainer, you have intercepted the network capture file `packets.pcap` and received a mysterious encoded string — your key to unlocking the hidden payload.

Your mission is to:

- Analyze the intercepted network capture.
- Use the provided encoded key to decrypt the concealed payload.
- Reveal the full secret message Team Rocket desperately wants to keep hidden.

---

## How to Solve

1. Use `tshark` to analyze the capture file and extract protocol fields:  
tshark -r packets.pcap -T fields -e frame.protocols | grep -v ^$ | sort | uniq
# Tshark Command Explained

The command reads the network capture file `packets.pcap` using Tshark and extracts the protocol stacks from each packet (`-T fields -e frame.protocols`). It then filters out empty lines (`grep -v ^$`), sorts the output alphabetically (`sort`), and removes duplicates (`uniq`) to list unique protocol combinations. Think of it as identifying Team Rocket’s distinct battle moves without repeats. This helps Trainers analyze the variety of protocols used in the intercepted traffic.

2. From the output, you will obtain the Base64 encoded string:  aGFja2Vtb257VGVhbVJvY2tlZEZhaWxlZFRvRXh0cmFjdH0=
3. Decode this Base64 string using any Base64 decoder (e.g., `base64` command line tool or online decoder).  
4. The decoded message is the hidden flag:  hackemon{TeamRockedFailedToExtract}
