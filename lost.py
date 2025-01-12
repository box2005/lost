import secrets
import random
from bitcoin import *
from multiprocessing import Pool, cpu_count

# Define the Bitcoin address
desired_address = '1CNzW7z2s4n6n2gNBqXo2nuXddNGQrp5px'

# Set the missing characters in the public key
#missing_characters = '03***********************************************a8204c1f394511f74'
missing_characters = '03*3b3a6ac47250715f0def72b224023e3c727d49581bedd2a8204c1f394511f74'
#0323b3a6ac47250715f0def72b224023e3c727d49581bedd2a8204c1f394511f74
#

# Number of CPU cores
num_cores = cpu_count()

#batch_size = num_cores * 4 # Adjust batch size based on the number of CPU cores
batch_size = 20 * 4 # Adjust batch size based on the number of CPU cores

print("Searching...\n")
#print(num_cores)

def bitcoin_address_match(params):
    public_key, desired_address = params
    try:
        compressed_public_key = compress(public_key)
        bitcoin_address = pubtoaddr(compressed_public_key)
        if bitcoin_address == desired_address:
            print("Public key found!")
            key_pair = f"Public Key: {public_key}\nBitcoin Address: {bitcoin_address}"
            print(key_pair)
            with open('PUBLIC-KEY-FOUND.txt', 'a') as file:
                file.write(key_pair + '\n')
            return True
        else:
            return False
    except Exception:
        return False

def generate_random_public_key(missing_characters):
    random_chars = [(secrets.choice('0123456789abcdef') if char == '*' else char) for char in missing_characters]
    public_key = ''.join(random_chars)
    return public_key

while True:
    public_key_batch = [generate_random_public_key(missing_characters) for _ in range(batch_size)]
    params_batch = [(public_key, desired_address) for public_key in public_key_batch]

    found = False
    for params in params_batch:
        if bitcoin_address_match(params):
            found = True
            break

    if found:
        break

print("Public key found and saved in PUBLIC-KEY-FOUND.txt")
