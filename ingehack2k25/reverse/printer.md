# IngeHack2k25 - reverse/mjsc Write-up

## Challenge Overview
**Challenge Name**: reverse/mjsc  
**Category**: Reverse Engineering  
**Event**: IngeHack 2k25  
**Difficulty**: Medium  
**Flag**: `ingehack{i_hate_js_rev_chals_they_never_have_a_new_idea}`  

We’re given an encrypted file (`enc`) and tasked with recovering the original image. The challenge involves reversing a Discrete Fourier Transform (DFT)-based encryption process implemented in JavaScript.
    IFFT: np.fft.ifft reverses the DFT, converting frequency-domain data back to the original pixel values.

    Byte Conversion: After IFFT, the real parts are rounded and clamped to valid pixel values (0-255).

Why This Works

    The encryption process used DFT to transform image data into the frequency domain.

    The enc file stores these frequency components as complex numbers.

    By applying IFFT, we reverse the transformation and recover the original image bytes.

Flag Extraction

Running the script produces decrypted.png, which displays the flag:
Decrypted Flag
Conclusion

This challenge tested reverse engineering skills focused on understanding DFT-based encryption. The key takeaways:

    Recognizing the use of Fourier Transforms in data obfuscation.

    Leveraging numpy’s FFT utilities for efficient decryption.

    Handling binary data and type conversions in Python.

Flag: ingehack{i_hate_js_rev_chals_they_never_have_a_new_idea}
Copy

New chat
AI-generated, for reference only
---

## Solution Approach
The encryption process converts pixel data from an image into the frequency domain using a DFT. To decrypt it, we:
1. Read the DFT coefficients from `enc` (stored as complex numbers).
2. Apply the **Inverse Fast Fourier Transform (IFFT)** to reconstruct the original pixel data.
3. Convert the numerical data back into a valid PNG image.

---

## Step-by-Step Solution

### 1. Understanding the Encryption
The challenge uses JavaScript to:
- Read an image file (e.g., PNG).
- Split its bytes into pairs of `double` values (real/imaginary parts).
- Apply DFT to convert the data into the frequency domain.
- Save the transformed complex numbers to `enc`.

### 2. Decryption Strategy
To reverse this:
- **Step 1**: Extract the complex numbers from `enc`.  
- **Step 2**: Compute the Inverse DFT (or IFFT) to recover the time-domain signal (original image bytes).  
- **Step 3**: Convert the numerical output to valid image bytes and save as a PNG.

### 3. Python Code Implementation
```python
import numpy as np

def decrypt_image():
    # Read encrypted data
    with open("enc", "rb") as f:
        data = f.read()
    
    # Convert bytes to array of doubles (float64)
    doubles = np.frombuffer(data, dtype=np.float64)
    
    # Reshape into complex numbers (real, imaginary pairs)
    complex_data = doubles.reshape(-1, 2)
    complex_numbers = complex_data[:, 0] + 1j * complex_data[:, 1]
    
    # Apply Inverse FFT
    time_domain_data = np.fft.ifft(complex_numbers)
    
    # Convert to valid bytes (0-255 range)
    byte_data = np.clip(np.round(np.real(time_domain_data)), 0, 255).astype(np.uint8)
    
    # Save as PNG
    with open("decrypted.png", "wb") as f:
        f.write(bytes(byte_data))

decrypt_image()
