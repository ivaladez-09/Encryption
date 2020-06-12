"""Kicker project for decrypting and encrypting"""
import string


class CryptKicker:
    """This Class give us the methods for decrypting and encrypting"""

    def __init__(self, key=None):
        """
        Init variables needed for the methods of the class

        :param:  String with the characters used as key for encrypt or decrypt.
                 If no param is passed, it uses a default one.
        :return:
        """
        self.key = "The quick brown fox jumps over the lazy dog".lower() if key is None else str(key).lower()
        self.key_length = len(self.key)

    @staticmethod
    def __generate_encrypted_dictionary(key):
        """
        Generates a dictionary with the values used for encryption.
        Just encrypt the letters present in the key, anything else as special characters
        are just copied. It allows me to identify the key later in decryption methods.

        :param key:  String with the characters uses as key for the encryption
        :return: Return Dictionary with characters encrypted
        """
        # Make sure the type of variables
        key = str(key)
        encrypted_dictionary = dict()

        # Generate unordered alphabet from [a-zA-Z]
        unordered_alphabet = list(set(string.ascii_letters))

        # Generates the encrypted dictionary. -> Key=msg_char: val=encrypt_char
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

        :param message: String with the message to encrypt
        :param encrypted_dictionary: Dictionary with the values to encrypt each character
        :param key: String used to identify the message and being able to encrypt or decrypt
        :return: Return String with encrypted key
        """
        # Make sure of the type of parameters
        encrypted_message, message = list(), str(message)
        encrypted_dictionary = dict(encrypted_dictionary)

        # Insert the key as part of the message
        middle = int(len(message) / 2)
        message = message[:middle] + ' ' + key + ' ' + message[middle:]

        # Insert the value for each dictionary key to encrypt the message
        for char in message:
            if char in encrypted_dictionary:
                encrypted_message.append(encrypted_dictionary[char])
            else:
                encrypted_message.append(char)

        # Convert the encrypted message into a string
        return "".join(encrypted_message)

    def encrypt(self, message=None, key=None):
        """
        Generates the message encrypted.

        :param message: String with the message to encrypt
        :param key: String used to identify the message and being able to encrypt or decrypt
        :return: Return String with encrypted key
        """
        message = str(message).lower()
        key = self.key if key is None else str(key).lower()
        encrypted_dictionary = self.__generate_encrypted_dictionary(key)
        encrypted_message = self.__generate_encrypted_message(message, encrypted_dictionary, key)
        print("Message:           {}\n"
              "Encrypted Message: {}".format(message, encrypted_message))
        return encrypted_message


if __name__ == "__main__":
    my_message = "Hello everyone!!! I am a Python Developer....."
    crypt_kicker = CryptKicker()
    my_encrypted_message = crypt_kicker.encrypt(my_message)
