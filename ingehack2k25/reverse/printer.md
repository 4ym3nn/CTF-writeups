# IngeHack2k25 - reverse/mjsc Write-up

## Challenge Overview
**Challenge Name**: reverse/printer  
**Category**: Reverse Engineering  
**Event**: IngeHack 2k25  
**Difficulty**: Medium  
**Flag**: `ingehack{...}`  
## Fourier Transformation-Based Image Decryption

### **Challenge Analysis**

Upon analyzing the provided files, we observed the following directory structure:
```
➜  solver ls 
decrypted.png  enc  main  reconstructed_data.txt  sol.py
```
The main objective is to decrypt the file `enc` to retrieve an image. By inspecting `main`, we determined that it applies a Fourier transformation, meaning the encryption likely involves transforming the image into the frequency domain. 

To recover the original image, we need to apply the **Inverse Fourier Transform (IFFT)** to `enc` and reconstruct the original pixel data.

### **Decryption Process**
The `decrypt_image()` function in `sol.py` implements the decryption using NumPy’s FFT functions. Below is a step-by-step breakdown of how it works:

1. **Read the Encrypted File**
   - The function reads `enc` as a binary file.
   - The binary data is interpreted as an array of `float64` values.

2. **Reshape into Complex Numbers**
   - The data is reshaped into pairs of real and imaginary components.
   - These are converted into complex numbers representing frequency-domain data.

3. **Apply Inverse FFT (IFFT)**
   - The inverse Fourier transform is applied to reconstruct the time-domain (original pixel) data.

4. **Convert Back to Byte Values**
   - The real part of the transformed data is extracted.
   - Values are rounded, clipped between 0-255, and converted to `uint8` format.

5. **Save as PNG File**
   - The decrypted image is written to `decrypted.png`.

### **Execution**
To decrypt the image, simply run:
```sh
python sol.py
```
If successful, it prints:
```
Image decrypted successfully. Saved as 'decrypted.png'
```

### **Flag**
After running the decryption, examining `decrypted.png` reveals the flag:
![decrypted](https://github.com/user-attachments/assets/a7723893-ea29-4ca2-a527-b2a7e4662af5)


---
This challenge demonstrates how Fourier transformations can be used in encryption and how applying inverse transformations can recover the original data.

