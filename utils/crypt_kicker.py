"""Kicker project for decrypting and encrypting"""
import string


class CryptKicker:
    """This Class give us the methods for decrypting and encrypting"""

    def __init__(self, key=None):
        """Initialize needed variables to encrypt or decrypt"""
        self.key = "The quick brown fox jumps over the lazy dog,.?!".lower() if key is None else str(key).lower()
        self.key_length = len(self.key)

    @staticmethod
    def __generate_encrypted_dictionary(key):
        """
        Generates a dictionary with the values used for encryption

        :param:
        :return: Return Dict with characters encrypted
        """
        # Generate unordered alphabet
        unordered_alphabet = list(set(string.ascii_letters))

        # Generate dictionary
        key = str(key)
        encrypted_dictionary = dict()
        index = 0
        alphabet_length = len(unordered_alphabet)
        for char in key:
            if not char.isalpha():
                encrypted_dictionary[char] = char
            elif char not in encrypted_dictionary:
                encrypted_dictionary[char] = unordered_alphabet[index]
                if index < alphabet_length:
                    index += 1

        return encrypted_dictionary

    @staticmethod
    def __generate_encrypted_message(message, encrypted_dictionary, key):
        """
        Generates the message encrypted using the dictionary

        :param:
        :return: Return String with encrypted key
        """
        encrypted_message, message = list(), str(message)
        middle = int(len(message) / 2)
        message = message[:middle] + ' ' + key + ' ' + message[middle:]
        encrypted_dictionary = dict(encrypted_dictionary)
        for char in message:
            if char in encrypted_dictionary:
                encrypted_message.append(encrypted_dictionary[char])

        return "".join(encrypted_message)

    def encrypt(self, message=None, key=None):
        """"fdg"""
        message = str(message).lower()
        key = self.key if key is None else str(key).lower()
        encrypted_dictionary = self.__generate_encrypted_dictionary(key)
        encrypted_message = self.__generate_encrypted_message(message, encrypted_dictionary, key)
        print("Message:           {}\n"
              "Encrypted Message: {}".format(message, encrypted_message))
        return encrypted_message


if __name__ == "__main__":
    my_message = "Hello everyone! I am a Python Developer."
    crypt_kicker = CryptKicker()
    my_encrypted_message = crypt_kicker.encrypt(my_message)
