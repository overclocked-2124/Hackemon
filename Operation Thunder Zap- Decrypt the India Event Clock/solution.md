# Team Rocket’s Encrypted Schedule

Welcome, Trainer! Team Rocket has encrypted the schedule of a secret Pokémon event in India inside a heavily layered file. Your mission is to decrypt the file, uncover the hidden author’s name who leaked the event details, and submit it as the flag.

---

## Challenge Overview

Team Rocket’s file contains multiple text blocks, each encrypted using a unique combination of Base64, hex, and hexdump encodings. You must carefully decode each layer to reveal the hidden information.

---

## Decryption Clues

1. Each text block uses a different recipe of Base64, hex, and hexdump layers, requiring step-by-step decoding.

2. One decrypted block reveals the event timing:  
   *“Saturday, June 28, at 10:00 am until Sunday, June 29, 2025, at 11:59 pm local time.”*

3. Another decrypted block contains key event details that, when searched online, lead to the official Pokémon GO Fest 2025 India webpage.

4. The official webpage URL is:  
   `https://pokemongohub.net/post/article/special-pokemon-go-fest-2025-global-celebrations-at-nexus-malls-india/`

5. By investigating this page, you discover the secret author who leaked the schedule:  
   **MeteorAsh15**

---

## Flag Format

Submit the author’s name in the following format:  hackemon{MeteorAsh15}
