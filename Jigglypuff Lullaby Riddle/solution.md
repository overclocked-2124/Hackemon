# Jigglypuff Lullaby Riddle - Solution

## Steps to solve:

1. **Base64 Decode**: Take the content from `file.txt` and decrypt it using base64
2. **Reverse Brainfuck**: Apply reverse brainfuck to the decoded content
3. **Extract Hidden Text**: After reverse brainfuck, you'll find:
   ```
   bhai'ye'hai'chhupa_hua_flag'="unpxrzba{cvxncvxncvxnpuh}
   ```
4. **ROT13 Decrypt**: The flag is encrypted using ROT13 cipher

## Final Flag:
```
hackemon{pikapikapikachu}
```

## Explanation:
The challenge involves multiple layers of encoding:
- Base64 encoding
- Brainfuck obfuscation
- ROT13 cipher

By reversing each layer, we uncover the hidden flag that follows the pattern of the classic Pokémon catchphrase "Pikachu" repeated three times. 