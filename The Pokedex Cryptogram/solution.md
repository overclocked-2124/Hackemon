# Team Rocket’s Intercepted Pokédex Transmission

## Challenge Description

Team Rocket has intercepted a top-secret Pokédex transmission, now stored as a cryptic ciphertext in the file `encrypted_pokedex.texts`. Your mission is to decrypt this ciphertext to reveal the hidden Pokédex entry before Team Rocket can exploit the information.

---

## How to Solve

1. **Convert the provided `encrypted_pokedex.texts` file into a standard `.txt` format** — this may involve manual renaming or reformatting.  
2. **Use the CyberChef website** (https://gchq.github.io/CyberChef/) to decrypt the ciphertext.  
   - Experiment with common operations such as Base64 decoding, ROT13, Caesar cipher shifts, or XOR, depending on the ciphertext’s characteristics.  
3. Once decrypted, you will uncover a Pokédex entry describing a Pokémon.  
4. The decrypted message reads:  
   > *"Bulbasaur can be seen napping in bright sunlight. There is a seed on its back. By soaking up the sun's rays, the seed grows progressively larger."*  
5. The  flag is embedded in the decrypted text.

---

## Flag Submission

Submit the flag in the format:  hackemon{Bulbasaur_napping}
