# Team Rocket’s Vault Coin Count Challenge

## Challenge Description

Team Rocket’s vault image is divided into sixteen quadrants by thick black lines forming a 4x4 grid. Each quadrant contains a unique number of golden coins scattered randomly. Your mission is to:

- Count the number of golden coins in **each quadrant**.
- Interpret each count as an **ASCII decimal value**.
- Convert these ASCII values into characters.
- Combine these characters in **left-to-right, top-to-bottom** order to reveal the secret flag.
- Submit the flag in the format:  hackemon{decoded_string}


---

## ASCII Decoding Sequence Across Quadrants

The quadrants encode the flag in this order:

| Quadrant Order | Coin Count (ASCII Decimal) | ASCII Character |
|----------------|----------------------------|-----------------|
| 1              | 104                        | h               |
| 2              | 97                         | a               |
| 3              | 99                         | c               |
| 4              | 107                        | k               |
| 5              | 101                        | e               |
| 6              | 109                        | m               |
| 7              | 111                        | o               |
| 8              | 110                        | n               |
| 9              | 123                        | {               |
| 10             | 109                        | m               |
| 11             | 51                         | 3               |
| 12             | 119                        | w               |
| 13             | 116                        | t               |
| 14             | 119                        | w               |
| 15             | 111                        | o               |
| 16             | 125                        | }               |

---

## Final Flag

Putting it all together, the decoded string is:  hackemon{m3wtwo}

