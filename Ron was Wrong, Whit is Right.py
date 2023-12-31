from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Util import number
import gmpy2
from itertools import combinations

# Initialize a dictionary to store RSA components
grps = {'n': [], 'c': [], 'e': []}

# Collect RSA components from files
for i in range(1, 51):
    # Read the RSA key and ciphertext from respective files
    key = RSA.importKey(open(f"keys_and_messages/{i}.pem", 'r').read())
    cipher = open(f"keys_and_messages/{i}.ciphertext", 'r').read()
    
    # Convert ciphertext to a long integer and store in the dictionary
    cipher = number.bytes_to_long(bytes.fromhex(cipher))
    grps['n'].append(key.n)  # Store modulus (n)
    grps['c'].append(cipher)  # Store ciphertext (c)
    grps['e'].append(key.e)  # Store public exponent (e)

N = 0

# Find a common factor between modulus pairs
for i in range(len(grps['n'])):
    for j in range(i + 1, len(grps['n'])):
        if i == j:  # Skip identical indices
            continue
        
        # Compute the greatest common divisor (GCD) of two moduli
        gcd = gmpy2.gcd(grps['n'][i], grps['n'][j])
        
        if gcd != 1:  # If a non-trivial GCD is found
            print(i, j, gcd)  # Display indices and the common factor
            N = int(gcd)  # Store the common factor
            ind = i  # Store the index

e = grps['e'][ind]
p = N
q = grps['n'][ind] // N

# Calculate the private key parameters
phi = (p - 1) * (q - 1)
d = number.inverse(e, phi)

# Reconstruct the RSA key using modulus and private exponent
key = RSA.construct((grps['n'][ind], e, d))
cipher = PKCS1_OAEP.new(key)

# Decrypt the ciphertext using the reconstructed key
flag = number.long_to_bytes(grps['c'][ind])
flag = cipher.decrypt(flag)
print(flag)  # Print the decrypted flag
