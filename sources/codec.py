# coding=utf-8
import Tkinter as tk
import easygui
import webbrowser
import os
import numpy as np


def main():
    # Window management, size, colors, title ..
    root = tk.Tk()
    root.geometry('440x140')
    root.title('CODEC GUI')
    root.configure(bg='black')
    root.iconbitmap('../assets/icon/icon.ico')

    # Row 1 -> Encode / Decode file
    row_2 = tk.Frame(root)
    tk.Button(row_2, text='Chiffrer', command=encode, fg='white', bg='black', width="30", height="4").pack(side=tk.LEFT)
    tk.Button(row_2, text='Déchiffrer', command=decode, fg='white', bg='black', width="30", height="4").pack(side=tk.LEFT)
    row_2.pack()

    # Row 2 -> Github or leave
    row_2 = tk.Frame(root)
    tk.Button(row_2, text='Github', command=github, fg='white', bg='black', width="30", height="4").pack(side=tk.LEFT)
    tk.Button(row_2, text='Quitter', command=root.quit, bg='red', fg='white', width="30", height="4").pack(side=tk.LEFT)
    row_2.pack()
    root.mainloop()


# Encoding function
def encode():
    # Instructions
    easygui.msgbox("Selectionner une matrice", "Instructions from CODEC GUI")

    # Matrix recovery
    matrix = np.array(getMatrice(), dtype=bool)

    # Instructions
    easygui.msgbox("Selectionner le fichier à encoder", "Instructions from CODEC GUI")

    # Opening the window for choosing the file to be encoded
    filename = easygui.fileopenbox('', '', '*.txt')
    filename = os.path.relpath(filename)

    # Preparing the name of the encoded file
    filename_enc = filename
    filename_enc += "c"

    # Opening the file in `r` mode
    f = open(filename, mode='r')
    contents = f.read()

    # Converting the characters in the file to bits
    contents = string2bits(contents)
    for content in contents:
        # Bit blocks are tabulated
        content = list(content)
        # Convert all data in (int) (because list() function return str)
        content = [int(i) for i in content]

        # Calculate X1 from U1 * G4c
        u1 = np.array(content[:4], dtype=bool)
        x1 = str(np.array_str(1 * np.dot(u1, matrix))).strip('[]').replace(' ', '')

        # Calculate X2 from U2 * G4c
        u2 = np.array(content[4:], dtype=bool)
        x2 = str(np.array_str(1 * np.dot(u2, matrix))).strip('[]').replace(' ', '')

        # Insertion of the encoded data in the encoded file, in `a` mode
        with open(filename_enc, 'a') as text:
            text.write(x1)
            text.write(x2)

    print('Encoding success, exit.')
    return True


# Decoding function
def decode():
    # Instructions
    easygui.msgbox("Selectionner une matrice", "Instructions from CODEC GUI")

    # Open matrice to decode the file
    matrix = getMatrice()

    # Instructions
    easygui.msgbox("Selectionner le fichier à décoder", "Instructions from CODEC GUI")

    # Opening the window for choosing the file to be decoded
    filename = easygui.fileopenbox('', '', '*.txtc')
    filename = os.path.relpath(filename)

    # Preparing the name of the decoded file
    filename_dec = filename
    filename_dec += "d"

    # Opening the file to decode
    f = open(filename, mode='r')
    contents = f.read()

    # 16-bit block segmentation to decode character by character
    contents = [contents[i:i + 16] for i in range(0, len(contents), 16)]

    # Get matrix identity
    identity = getMatrixIdentity(matrix)

    full_decoded = ""
    for content in contents:
        # Get the first 8 elements of our 16-bit block
        x1 = content[:8]
        # Get the last 8 elements of our 16-bit block
        x2 = content[8:]

        # Retrieves the bits of the blocks encoded by their index from the identity matrix
        for i in range(4):
            full_decoded += x1[(identity[i])]
        for i in range(4):
            full_decoded += x2[(identity[i])]

    # Write decoded data into decoded file
    with open(filename_dec, 'a') as file:
        file.write(bits2strings(full_decoded))

    print('Decoding success, exit.')
    return True


# Redirect to our project's github
def github():
    webbrowser.open('https://github.com/MaaximeLH/codec-gui')


# Get bits from strings
def string2bits(s=''):
    return [bin(ord(x))[2:].zfill(8) for x in s]


# Get strings from bits
def bits2strings(bits):
    message = ""
    while bits != "":
        i = chr(int(bits[:8], 2))
        message = message + i
        bits = bits[8:]
    return message


# Get matrice from file and parse it
def getMatrice():
    # Open window dialog
    filename = easygui.fileopenbox('', '', '*.txt')
    filename = os.path.relpath(filename)
    # Get matrix
    matrix = open(filename, 'r').read().split('[')[1].split(']')[0]
    matrix = matrix.replace(' ', '')
    # Insert of matrix into Array
    amatrix = []
    amatrix.append(list(matrix[:8]))
    amatrix[0] = [int(i) for i in amatrix[0]]
    amatrix.append(list(matrix[8:16]))
    amatrix[1] = [int(i) for i in amatrix[1]]
    amatrix.append(list(matrix[16:24]))
    amatrix[2] = [int(i) for i in amatrix[2]]
    amatrix.append(list(matrix[24:32]))
    amatrix[3] = [int(i) for i in amatrix[3]]
    return amatrix


# Get matrix identity
def getMatrixIdentity(matrice):
    matrix = np.array(matrice, dtype=int)

    first = 0
    second = 0
    third = 0
    fouth = 0
    i = 0

    while i < 7:
        if matrix[0][i] == 1 and matrix[1][i] == 0 and matrix[2][i] == 0 and matrix[3][i] == 0:
            first = i
        if matrix[0][i] == 0 and matrix[1][i] == 1 and matrix[2][i] == 0 and matrix[3][i] == 0:
            second = i
        if matrix[0][i] == 0 and matrix[1][i] == 0 and matrix[2][i] == 1 and matrix[3][i] == 0:
            third = i
        if matrix[0][i] == 0 and matrix[1][i] == 0 and matrix[2][i] == 0 and matrix[3][i] == 1:
            fouth = i
        i += 1

    return [first, second, third, fouth]


# Main function
if __name__ == "__main__":
    main()