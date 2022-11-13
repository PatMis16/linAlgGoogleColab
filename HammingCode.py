import numpy as np

class HammingCode:
    """
    Klasse zur verarbeitung von Hamming-Codes
    """

    def __init__(self, k):
        """
        Initialisierung einer HammingCode-Instanz
        :param k: Anzahl der Paritätsbits im HammingCode
        """
        self.k = k  # number of parity bits
        self.N = 2**k - 1  # code length
        self.p = 2 ** k - k - 1  # payload bits
        self.__construct_chk_matrix()  # construct the check matrix
        self.__construct_gen_matrix()  # construct the generator matrix
        self.__construct_encode_matrix()  # construct the encode matrix

    def __construct_gen_matrix(self):
        """
        Konstruktion der Generator-Matrix für die HammingCode-Instanz
        :return: none
        """
        id_matrix = np.identity(self.p)
        self.gen_matrix = np.append(id_matrix, self.parity_matrix, axis=0)

    def __construct_chk_matrix(self):
        """
        Konstruktion der Prüfmatrix für die HammingCode-Instanz
        :return: none
        """
        id_matrix = np.identity(self.k)
        self.chk_matrix = ""
        tmp_check_matrix = ""
        for i in range(1, self.N+1):
            bin_num_rep = bin(i)[2:]
            bin_num_arr = self.__to_array(bin_num_rep)
            while len(bin_num_arr) < self.k:
                bin_num_arr.insert(0, 0)
            if i == 1:
                tmp_check_matrix = np.array([bin_num_arr[::-1]])
            else:
                tmp_check_matrix = np.vstack((tmp_check_matrix, bin_num_arr[::-1]))
        nonsy_chk_matrix = tmp_check_matrix.T
        one_pos = []
        for i in range(self.N):
            if np.sum(nonsy_chk_matrix[:, i]) == 1:
                one_pos.append(i)
        self.parity_matrix = np.delete(nonsy_chk_matrix, one_pos, 1)
        self.chk_matrix = np.hstack((self.parity_matrix, id_matrix))

    def __construct_encode_matrix(self):
        """
        Konstruktion der Decodierungs-Matrix fir die HammingCode-Instanz
        :return: none
        """
        id_matrix = np.identity(self.p)
        null_matrix = np.zeros((self.p, self.k))
        self.encode_matrix = np.hstack((null_matrix, id_matrix))

    @staticmethod
    def __to_array(input_string):
        """
        Methode zur Rückgabe eines Integers aus für jedes Zeichen eines Strings
        :param input_string: Eingabe-String
        :return: Integer
        """
        return [int(x) for x in str(input_string)]

    def get_length(self):
        """
        Methode zur Rückgabe der Code-Länge
        :return: Code-Länge als Integer
        """
        return self.N

    def get_payload(self):
        return self.p

    def get_generator_matrix(self):
        """
        Method to return the generator matrix for hamming code
        :return: generator matrix
        """
        return self.gen_matrix

    def get_check_matrix(self):
        """
        Method to return the check matrix for hamming code
        :return: check matrix
        """
        return self.chk_matrix
    
    def get_encoding_matrix(self):
        """
        Metode zur rückgabe der Entcodierungs-Matrix
        :return: encoding matrix
        """
        return self.encode_matrix

    def encode(self, word):
        """
        Method to encode the given word
        :param word: word to encode
        :return: encoded word (codeword)
        """
        word_array = [int(x) for x in str(bin(word)[2:])]
        word_array_len = len(word_array)
        if word_array_len < self.p:
            for i in range(self.p - word_array_len):
                word_array.insert(0, 0)
        tmp_encode = np.matmul(self.gen_matrix, word_array)
        for i in range(tmp_encode.size):
            if tmp_encode[i] > 1:
                if tmp_encode[i] % 2 == 0:
                    tmp_encode[i] = 0
                else:
                    tmp_encode[i] = 1
        return ''.join(map(str, [int(x) for x in tmp_encode]))

    def decode(self, codeword):
        """
        Method to decode the given codeword
        :param codeword: codeword to decode
        :return: decoded codeword
        """
        codeword_array = self.__to_array(codeword)
        tmp_decode = np.matmul(self.encode_matrix, codeword_array)
        decoded_word = []
        for d in tmp_decode:
            if d != 0 and d % 2 == 0:
                bit_d = 0
            else:
                bit_d = 1
            decoded_word.append(bit_d)
        return decoded_word

    def check(self, codeword):
        """
        Methode to check if the given codeword is a correct codeword
        :param codeword: codeword to check
        :return: True if codeword is correct, False if codeword has errors
        """
        codeword_array = self.__to_array(codeword)
        tmp_check = np.matmul(self.chk_matrix, codeword_array)
        check = []
        for e in tmp_check:
            if e != 0 and e % 2 == 0:
                bit_e = 0
            else:
                bit_e = 1
            check.append(bit_e)
        error = sum(int(check) * (2 ** i) for i, check in enumerate(check[::-1]))
        print("Error in bit: ", error)
        return ''.join(map(str, [int(x) for x in check]))