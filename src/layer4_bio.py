# layer4_bio.py
# Layer 4: Bio-Translation

def string_to_binary(text: str) -> str:
    """Converts a string to its 8-bit binary representation."""
    return ''.join(format(ord(c), '08b') for c in text)

def binary_to_string(binary: str) -> str:
    """Converts a binary string back to text."""
    chars = [chr(int(binary[i:i+8], 2)) for i in range(0, len(binary), 8) if len(binary[i:i+8]) == 8]
    return ''.join(chars)

def binary_to_dna(binary_string: str) -> str:
    """
    Translates binary to DNA bases:
    00 -> A
    01 -> C
    10 -> G
    11 -> T
    """
    mapping = {'00': 'A', '01': 'C', '10': 'G', '11': 'T'}
    bases = []
    # Ensure binary length is even
    if len(binary_string) % 2 != 0:
        binary_string = '0' + binary_string
        
    for i in range(0, len(binary_string), 2):
        bits = binary_string[i:i+2]
        bases.append(mapping.get(bits, 'A'))
    return ''.join(bases)

def dna_to_binary(dna_sequence: str) -> str:
    """
    Translates DNA bases back to binary.
    """
    reverse_mapping = {'A': '00', 'C': '01', 'G': '10', 'T': '11'}
    bits = [reverse_mapping.get(base, '00') for base in dna_sequence]
    return ''.join(bits)

def encode_message_to_dna(message: str) -> str:
    """Full encoding from string to DNA."""
    binary = string_to_binary(message)
    dna = binary_to_dna(binary)
    return dna

def decode_dna_to_message(dna: str) -> str:
    """Full decoding from DNA to string."""
    binary = dna_to_binary(dna)
    message = binary_to_string(binary)
    return message
