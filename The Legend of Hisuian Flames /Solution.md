1. Decode the message hidden in the Pokédex-style PDF.
2. Use that decoded word as a *Steghide* passphrase to free the final flag from the PNG.

### 🥇 Stage 1 — Reading the Pokédex (PDF)

1. **Open `Pokemon_Ultimate_Edition.pdf`.**
Near the bottom margin of the last page you’ll spot a lone string that doesn’t belong in normal prose:

```
Y0c5cGJuUmxjbk09
```

Its jumble of upper/lower-case letters, digits, and an equals sign is a classic *Base64* tell.
2. **Head to CyberChef** (the Poké Mart for digital ingredients).
    - Drag in a *“From Base64”* recipe.
    - Paste the suspicious text.

CyberChef instantly cooks up the plaintext:

```
pointers
```

This is your secret move—the passphrase you’ll unleash on the next battlefield.

> *Professor’s Note*: Always eyeball strange blobs in documents first; many CTF PDFs hide Base64 or hex right in plain sight. No terminal commands needed—just keen Trainer eyesight!

### 🥈 Stage 2 — Unleashing Steghide on Arcanine (PNG)

1. **Interrogate the image** (`arcanine.png`) with Steghide:

```bash
steghide info arcanine.png
```

The tool confirms data is embedded and politely asks for a passphrase—exactly what Team Rocket tried to guard.
2. **Extract the hidden payload** using the word you just decoded:

```bash
steghide extract -sf arcanine.png -p pointers
```

Steghide drops a tiny file, typically `flag.txt`, into your current directory.
3. **Read the file**:

```bash
cat flag.txt
```

Output:

```
hackemon{Kingambit}
```

Victory! Kingambit, the Supreme Overlord of blades, has cut through Team Rocket’s ruse.
