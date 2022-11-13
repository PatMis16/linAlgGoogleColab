import HammingCode
import numpy as np

def main():
    k = 3
    hamming = HammingCode(k)
    print("Length: ", hamming.get_length())
    print("Payload: ", hamming.get_payload())
    print("Generator Matrix: ", hamming.get_generator_matrix())
    print("Check Matrix: ", hamming.get_check_matrix())
    print("Encoding Matrix: ", hamming.get_encoding_matrix())

    for w in range(hamming.get_payload()**2):
        encode_decode(hamming, w)

    # Hamminc Code with error:
    print("Hamming-Code with error")
    codeword_with_error = "0111011"
    print("Codeword with error: ", codeword_with_error)
    hamming.check(codeword_with_error)

     # Hamminc Code with error:
    print("Hamming-Code with error")
    codeword_with_error = "1100011"
    print("Codeword with error: ", codeword_with_error)
    hamming.check(codeword_with_error)


def encode_decode(hamming, word):
    print("Word: ", word)
    encoded_word = hamming.encode(word)
    print("Encoded Word: ", encoded_word)
    check = hamming.check(encoded_word)
    print("Check Result: ", check)
    decoded_word = hamming.decode(encoded_word)
    print("Decoded Word: ", decoded_word)


if __name__ == '__main__':
    main()
