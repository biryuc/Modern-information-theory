# -*- coding: UTF-8 -*-
# Алгоритм Хаффмана по одному символу

from collections import Counter
import time
from sys import argv
import math

import sys


class Tree:
    __slots__ = ('leaf', 'right', 'left')

    def __init__(self, leaf=None, right=None, left=None):
        self.right = right
        self.left = left
        self.leaf = leaf

    def step(self, dict_code, arr_code):
        if self.left:
            self.left.step(dict_code, arr_code + '0')
        if self.right:
            self.right.step(dict_code, arr_code + '1')
        if self.leaf:
            dict_code[self.leaf] = arr_code

    def get_value(self):
        return self.leaf

    def set_value(self, value):
        self.leaf = value


class Huffman:
    def sort_by_two(self, arr):
        lenght = len(arr)
        sort_arr = []
        for i in range(0, lenght, 2):
            sort_arr.append(tuple(arr[i:i + 2]))

        return sort_arr

    def get_code(self, data):
        dict_ = {}
        data = self.sort_by_two(data)
        for byte, freq in Counter(data).items():
            if byte == 0:
                leaf = Tree(leaf='0')
                dict_.update({leaf: freq})
                continue
            leaf = Tree(leaf=byte)
            dict_.update({leaf: freq})

        sorted_dict = dict(sorted(dict_.items(), key=lambda item: item[1]))
        lenght = len(sorted_dict) - 1
        j = 0
        for i in range(lenght):
            sorted_dict = dict(sorted(sorted_dict.items(), key=lambda item: item[1]))
            arr = list(sorted_dict.keys())
            freq1 = sorted_dict.pop(arr[j])
            j += 1
            freq2 = sorted_dict.pop(arr[j])
            sorted_dict.update({Tree(left=arr[j - 1], right=arr[j]): freq1 + freq2})
            j = 0
        arr = list(sorted_dict.keys())
        code = {}
        arr[0].step(code, "")
        arr = list(code.values())
        code_str = "".join(arr)
        return [code_str, code, dict_]

    def encode(self, data, dict_code):
        lenght = int(len(data))
        encode = []
        # for i in range(lenght):
        #   if data[i]==0:
        #       encode.append(dict_code['0'])
        #       continue
        #   encode.append(dict_code[data[i]])

        for i in range(0, lenght, 2):
            encode.append(dict_code[tuple(data[i:i + 2])])
        return "".join(encode)

    def decode(self, byte_str, dict_code):
        decode = []
        reverse_dict = dict(map(reversed, dict_code.items()))
        code_str = ""
        for i in byte_str:
            code_str += i
            if code_str in reverse_dict.keys():
                decode.append(reverse_dict[code_str][0])
                decode.append(reverse_dict[code_str][1])
                code_str = ""
        return decode

    def get_unique_numbers(self, numbers):
        list_of_unique_numbers = []
        numbers = self.sort_by_two(numbers)
        unique_numbers = set(numbers)

        for number in unique_numbers:
            list_of_unique_numbers.append(number)

        return list_of_unique_numbers

    def prepare_last_byte(self, last_b, flag):
        last_b = last_b[8 - flag:]
        return last_b

    def get_correct_read_encode(self, read_encode, last_b):
        read_encode[-2] = self.prepare_last_byte(read_encode[-2], last_b)
        read_encode = read_encode[:-1]
        return read_encode


class File:

    def get_binary_data(self, filepath):
        # try:
        flag = 0
        with open(filepath, "rb") as f:
            buff = []
            byte = f.read(1)

            buff.append(byte)
            while byte:
                byte = f.read(1)
                buff.append(byte)
        buff = buff[:-1]
        lenght = len(buff)

        if (lenght % 2 != 0):
            buff.append(buff[1])
            flag = 1
        lenght = len(buff)
        f.close()

        for i in range(len(buff)):
            buff[i] = int.from_bytes(buff[i], byteorder='big')
        return [buff, lenght, flag]

    def write_encode_and_tree(self, filepath, dict_code, data, flag):

        arr_code = []
        arr_ = []

        ch_ = 58  #:
        for i in dict_code:
            arr_.append(int(i[0]))
            # arr_.append(int(ch_))
            arr_.append(int(i[1]))
            # arr_.append(int(ch_))
            arr_.append(len(dict_code[i]))
            for j in dict_code[i]:
                arr_.append(j)
            # arr_.append(int(ch_))

        lenght_arr = len(arr_)

        str_ = (lenght_arr).to_bytes(3, byteorder="big")
        arr_code.append(flag)
        for i in range(len(str_)):
            buff = bin(str_[i])[2:].zfill(8)
            arr_code.append(int(buff, 2))

        arr_code.append(int(ch_))
        for i in arr_:
            arr_code.append(int(i))

        with open(filepath, "wb") as file:
            flag = len(data) % 8
            len_byte = 8
            arr_data = [int((data[i:i + len_byte]), 2) for i in range(0, len(data) - flag, len_byte)]

            if flag != 0:
                last_byte = data[-flag:]
                for i in range(len_byte - flag):
                    last_byte = '0' + last_byte

                arr_data.append(int(last_byte, 2))

            else:
                arr_data.append(int(data[-len_byte:], 2))
            arr_data.append(flag)
            for i in arr_data:
                arr_code.append(i)

            bytes_ = bytes(arr_code)
            file.write(bytes_)
        file.close()
        return [flag, arr_data, bytes_, arr_code, arr_]

    def write_like_binary(self, filepath, data):
        with open(filepath, "wb") as file:
            flag = len(data) % 8
            len_byte = 8
            arr_data = [int((data[i:i + len_byte]), 2) for i in range(0, len(data) - flag, len_byte)]

            if flag != 0:
                last_byte = data[-flag:]
                for i in range(len_byte - flag):
                    last_byte = '0' + last_byte

                arr_data.append(int(last_byte, 2))

            else:
                arr_data.append(int(data[-len_byte:], 2))
            arr_data.append(flag)
            bytes_ = bytes(arr_data)
            file.write(bytes_)
        file.close()
        return [flag, arr_data, bytes_]

    def parse_encode_and_tree(self, buff):
        flag = int(buff[0], 2)
        for i in range(1, len(buff)):
            if int(buff[i], 2) == 58:
                break

        lenght_dict = int("".join(buff[1:i]), 2)

        parse_dict = buff[4:lenght_dict + 5]

        dict = {}

        j = 0

        for i in range(1, len(parse_dict)):
            if i == 0:
                key1 = int(parse_dict[i], 2)
                key2 = int(parse_dict[i + 1], 2)
                step = int(parse_dict[i + 2], 2)
                dict.update({(key1, key2): ''})
                i_tmp = (key1, key2)
                j = 1
            elif j == 0 and i > 0:
                key1 = int(parse_dict[i], 2)
                key2 = int(parse_dict[i + 1], 2)
                step = int(parse_dict[i + 2], 2)
                dict.update({(key1, key2): ''})
                i_tmp = (key1, key2)
                j = 1
            elif j == 1 or j == 2:
                j += 1
            elif j == 3 and step != 0:
                tmp = str(int(parse_dict[i], 2))
                # tmp = str(int(parse_dict[i],2))
                dict[i_tmp] = dict[i_tmp] + tmp
                step -= 1
                if step == 0: j = 0


        encode = buff[lenght_dict + 5:]

        return encode, dict, flag

    def read_like_binary(self, filepath):
        with open(filepath, "rb") as binary_file:
            buff = []

            bytes = binary_file.read()

            for i in range(len(bytes)):
                data = bin(bytes[i])[2:].zfill(8)
                a = int(data, 2)
                buff.append(data)

        binary_file.close()
        return [buff, int(buff[-1], 2)]

    def write_dict(self, filename, dict):
        with open(filename, 'w') as out:
            for key, val in dict.items():
                out.write('{} {}\n'.format(key, val))
        out.close()

    def read_dict(self, filename):
        read_dict = {}
        with open(filename, 'r') as file:
            for line in file:
                key, value = line.split()
                read_dict[key] = value
        return read_dict

    def final_write(self, filename, data, flag):
        if flag == 1:
            data = data[:-1]
        for i in range(len(data)):
            data[i] = int(data[i])

        with open(filename, 'wb') as out:
            bytes_ = bytes(data)
            # print(len(bytes_))
            out.write(bytes_)
        out.close()


def H_x(dict, N):
    h_x = 0
    arr = list(dict.keys())
    for i in range(len(dict)):
        h_x += -(dict[arr[i]] / N) * math.log2((dict[arr[i]] / N))
    return h_x


def H_x_x(dict, N, h_x):
    h_x_x = 0
    h_x_x_tmp = 0
    arr = list(dict.keys())
    for i in range(len(dict)):
        h_x_x = -h_x_x_tmp * (dict[arr[i]] / N)
        for j in range(len(dict)):
            h_x_x_tmp += (dict[arr[j]] / N) * math.log2((dict[arr[j]] / N))
    return h_x_x

def main_decode(filepath_read,filepath_write):
    huf_obj = Huffman()
    file_obj = File()
    '''Чтение закодированного файла'''
    read_encode, last_b = file_obj.read_like_binary(filepath_read)
    [encode, dict_code,flag] = file_obj.parse_encode_and_tree(read_encode)
    read_encode = huf_obj.get_correct_read_encode(encode, last_b)
    '''Декодирование'''
    decode = huf_obj.decode("".join(read_encode), dict_code)
    '''Запись декодированных данных в файл'''
    file_obj.final_write(filepath_write, decode,flag)
    print("Декодированные данные записаны в файл ", filepath_write)
    return len(read_encode)



if __name__ == '__main__':

    script, filepath_read, filepath_write = argv

    main_decode(filepath_read,filepath_write)


