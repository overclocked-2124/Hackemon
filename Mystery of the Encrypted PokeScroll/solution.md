# Mystery of the Encrypted PokeScroll - Solution

## Challenge Overview
Team Rocket has hidden a secret message inside a password-protected PokéScroll (PDF) and left behind a mysterious image as a clue. The challenge involves decoding the image to find the password, then unlocking the PDF to retrieve the encrypted flag.

## Solution Steps

### 1. Image Analysis
- Examine the provided `Hackemon.jpeg` image
- The image contains text encrypted using **Unown Pokémon letters**
- Unown letters are a special alphabet from the Pokémon universe that resemble the English alphabet

### 2. Manual Decoding
- **Manually identify** each Unown letter in the image
- Translate each Unown letter to its corresponding English letter
- This requires careful observation and knowledge of the Unown alphabet
- Use the **Pokémon script decoder** in **dcode.fr** to verify your translations

### 3. Password Extraction
- After decoding all the Unown letters, read the complete message
- The **last 2 letters** of the decoded message spell out **"hi"**
- This is the **password** needed to unlock the PDF

### 4. PDF Decryption
- Use the password **"hi"** to unlock the `Password Protect PDF Hackemon.pdf`
- The PDF contains the encrypted flag

### 5. Flag Decryption
- The flag inside the PDF is encrypted using **5 levels of encryption**
- Apply decryption techniques to each layer:
  - Layer 1: [First encryption method]
  - Layer 2: [Second encryption method]
  - Layer 3: [Third encryption method]
  - Layer 4: [Fourth encryption method]
  - Layer 5: [Fifth encryption method]

### 6. Final Flag
- After decrypting all 5 layers, you'll reveal the final flag

## Final Flag
```
hackemon{cy3pt0_1s_t00_e2sy}
```

## Tools Used
- **dcode.fr**: Pokémon script decoder for verifying Unown letter translations
- **PDF reader**: To open and decrypt the password-protected PDF
- **Decryption tools**: Various tools for the 5-layer encryption (specific tools depend on encryption methods used)

## Challenge Theme
This challenge combines:
- **Pokémon lore**: Unown letters and PokéScroll concept
- **Steganography**: Hidden messages in images
- **Cryptography**: Multiple layers of encryption
- **Password cracking**: Finding the key to unlock protected content

## Learning Points
- Understanding Unown Pokémon alphabet and its translation to English
- Manual image analysis and character recognition
- Working with password-protected PDFs
- Multi-layer decryption techniques
- The importance of attention to detail in cryptographic challenges

## Difficulty Level
This challenge tests multiple skills:
- **Observation**: Carefully identifying Unown letters
- **Patience**: Manual decoding process
- **Cryptographic knowledge**: Understanding various encryption methods
- **Tool proficiency**: Using appropriate decryption tools 