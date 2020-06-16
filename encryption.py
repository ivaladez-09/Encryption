"""Kicker project for decrypting and encrypting"""
import string
import random


class Encryption:
    """This Class give us the methods for decrypting and encrypting"""

    def __init__(self, key=None):
        """
        Init variables needed for the methods of the class

        :param:  String with the characters used as key for encrypt or decrypt.
                 If no param is passed, it uses a default one.
        :return:
        """
        self.key = "The quick brown fox jumps over the lazy dog,!." if key is None else str(key)
        self.key_length = len(self.key)

    @staticmethod
    def __generate_encrypted_dictionary(key):
        """
        Generates a dictionary with the values used for encryption.
        Encrypt all the characters present in the key, less the (space).
        It allows me to identify the key later in decryption methods.

        :param key: String with the characters uses as key for the encryption
        :return: Return Dictionary with characters encrypted
        """
        # Make sure the type of variables
        key = str(key)
        encrypted_dictionary = dict()

        # Generate unordered alphabet from [a-zA-Z]
        unordered_alphabet = list(set(string.ascii_letters))

        # Generates the encrypted dictionary. -> Key=message_char: val=encrypt_char
        index = 0
        alphabet_length = len(unordered_alphabet)
        for char in key:
            if char not in encrypted_dictionary:
                if char == " ":
                    encrypted_dictionary[char] = char
                elif index < alphabet_length:
                    encrypted_dictionary[char] = unordered_alphabet[index]
                    index += 1
                else:
                    # If the unordered_alphabet comes to the end and there are more
                    # chars in the key that are not in the dictionary yet, the rest of
                    # chars will not be added to the dictionary.
                    break

        return encrypted_dictionary

    @staticmethod
    def __verify_encrypted_dictionary(message, encrypted_dictionary):
        """
        Modify the encrypted dictionary to avoid getting encrypted values that are
        already in the original message but that were not in the key.
        For example:
        - Key: 'Hello you'
        - Message: 'Good bye all'
        - Where 'G, b, a' are not in the key, and one of the encrypted characters
          can be 'G, b, a'. In that case when we will try to decrypt the message
          we can substitute characters that were not in the key.

        :param message:  String with the message to be encrypted.
        :param encrypted_dictionary:  Dictionary with the characters uses to
                                      replace original characters in message.
        :return: Return Dictionary with characters encrypted
        """
        while True:
            modifications_count = 0
            # Simplify the requests
            encrypted_chars = encrypted_dictionary.values()
            registered_chars = encrypted_dictionary.keys()

            # Get a list of no registered characters for encryption.
            # If list empty, it means the dictionary is ready
            no_registered_chars = [char for char in message if char not in registered_chars]
            if not no_registered_chars:
                break

            # Get a list of no registered characters for encryption that are as encrypted characters
            # If list empty, it means the dictionary is ready
            no_registered_chars_encrypted = [char for char in no_registered_chars
                                             if char in encrypted_chars]
            if not no_registered_chars_encrypted:
                break

            # Replace encrypted characters that are in the list of no_registered_chars_encrypted
            # from the encrypted dictionary
            for char in no_registered_chars_encrypted:
                for en_key, en_val in encrypted_dictionary.items():
                    if en_val == char:
                        while True:
                            random_char = random.choice(string.ascii_letters)
                            if random_char not in encrypted_dictionary.values():
                                encrypted_dictionary[en_key] = random_char
                                modifications_count += 1
                                break

            # If any modification was not needed, it means the dictionary is ready
            if modifications_count == 0:
                break

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
        message_length = len(message)
        position = int(message_length - random.randint(1, message_length))
        message = message[:position] + key + message[position:]

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
        # Make sure of types and values for variables
        message = str(message)
        key = self.key if key is None else str(key)

        # Functional logic
        encrypted_dictionary = self.__generate_encrypted_dictionary(key)
        encrypted_dictionary = self.__verify_encrypted_dictionary(message, encrypted_dictionary)
        encrypted_message = self.__generate_encrypted_message(message, encrypted_dictionary, key)

        return encrypted_message

    @staticmethod
    def __generate_decrypted_dictionary(message, key):
        """
        Look for a specific string in the encrypted message that is equivalent to the key.

        :param message: String with the message where to look for.
        :param key: String used to identify the message and being able to decrypt
        :return: Return Tuple of None on failure.
                 Return Tuple with a decrypted dictionary and the encrypted key found in message.
        """
        message, key = str(message), str(key)
        message_length, key_length = len(message), len(key)

        # Matching the sequence of characters equivalent to the key
        for position in range(0, message_length):
            max_length = position + key_length
            if max_length >= message_length:
                return None
            encrypted_key = message[position: max_length]
            # Comparing characters and spaces
            if all(list(map(lambda chars: chars[0].isspace() == chars[1].isspace(),
                            zip(encrypted_key, key)))):
                decrypted_dictionary = {k: v for k, v in zip(encrypted_key, key)}
                # Debug prints
                print("\n - Encrypted key: {}\n"
                      " - Decrypted key: {}\n"
                      " - Dictionary: {}\n".format(encrypted_key, key, decrypted_dictionary))
                return decrypted_dictionary, encrypted_key

        return None, None

    @staticmethod
    def __generate_decrypted_message(message, decrypted_dictionary):
        """
        Replace characters from message with found chars in decrypted_dictionary.
        It substitute one at the time, to avoid substitute a valid character.

        param message: String with the characters to be replaced
        param decrypted_dictionary: Dictionary with values of decrypted characters

        return: String with the values of dictionary instead of keys
        """
        decrypted_dictionary = dict(decrypted_dictionary)

        message_decrypted = message[:]
        tem_message = list()
        for char in message_decrypted:
            if char in decrypted_dictionary.keys():
                tem_message.append(decrypted_dictionary[char])
            else:
                tem_message.append(char)
        message_decrypted = "".join(tem_message)

        return message_decrypted

    def decrypt(self, message=None, key=None):
        """
        Method to discover the meaning of an encrypted message.

        :param message: String with the encrypted message
        :param key: String
        :return: Return 'No solution found' on failure.
                 Return string with the decrypted message on success.
                 Return None on invalid message
        """
        # Make sure of types and values for variables
        message = str(message)
        key = self.key if key is None else str(key)

        # Get dictionary with the meaning of encrypted characters and
        # a piece of message that represents the key
        decrypted_dictionary, encrypted_key = self.__generate_decrypted_dictionary(message, key)
        if decrypted_dictionary is None or encrypted_key is None:
            return "No solution found"

        # Remove encrypted_key and white spaces
        message = message.replace(encrypted_key, "")
        message = message.replace("  ", " ").strip()

        # Substitute characters in messages based on dictionary
        message_decrypted = self.__generate_decrypted_message(message, decrypted_dictionary)

        return message_decrypted


if __name__ == "__main__":
    MESSAGE = "Hello everyone!!! I am a Python Developer.."
    encryption = Encryption()  # Use default key
    ENCRYPTED_MESSAGE = encryption.encrypt(MESSAGE)
    print(" - Original Message:  {}\n"
          " - Encrypted Message: {}".format(MESSAGE, ENCRYPTED_MESSAGE))
    DECRYPTED_MESSAGE = encryption.decrypt(ENCRYPTED_MESSAGE)
    print(" - Encrypted Message: {}\n"
          " - Decrypted Message: {}".format(ENCRYPTED_MESSAGE, DECRYPTED_MESSAGE))
