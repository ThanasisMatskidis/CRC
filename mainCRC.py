import numpy as np
import random


# XOR: Συνάρτηση που δέχεται δύο αριθμούς και υλοποιεί την πράξη XOR.
def XOR(x, y):
    if x == y:
        return 0
    else:
        return 1


# CRC: Συνάρτηση που υλοποιεί την αριθμητική modulo-2 και με αυτήν υπολογίζεται τόσο το FCS όσο και το υπόλοιπο (R).
def CRC(a, b):
    temp = np.zeros(k + n - 1, dtype=int)
    for i in range(0, k + n - 1):
        temp[i] = a[i]
    step = 0
    while (n + step) <= k + n - 1:
        guard = True
        j = 0
        for i in range(0, n):
            if XOR(temp[step + i], b[i]) == 0:
                if guard:
                    j += 1
                    temp[step + i] = XOR(temp[step + i], b[i])
                else:
                    temp[step + i] = XOR(temp[step + i], b[i])
            else:
                guard = False
                temp[step + i] = XOR(temp[step + i], b[i])
        step += j
    return temp


# BER: Υλοποίηση του bit error rate.
def BER(a, stop):
    temp = np.zeros(k + n - 1, dtype=int)
    for i in range(0, k + n - 1):
        temp[i] = a[i]
    for i in range(0, stop):
        prob = random.uniform(0.0, 1000.0)
        if prob < 1:
            if temp[i] == 1:
                temp[i] = 0
            else:
                temp[i] = 1
    return temp


# check1: έλεγχος για το αν η εκάστοτε περίπτωση θα ανήκει στο ποσοστό του πρώτου ερωτήματος.
def check1(a, a_error, stop):
    guard = True
    for i in range(0, stop):
        if a[i] != a_error[i]:
            guard = False

    if guard:
        return 0
    else:
        return 1


# check2: έλεγχος για το αν η εκάστοτε περίπτωση θα ανήκει στο ποσοστό του δεύτερου ερωτήματος.
def check2(a, stop):
    guard = True
    for i in range(0, stop):
        if a[i] == 1:
            guard = False

    if guard:
        return 0
    else:
        return 1


# main
finish = 100000
firstSum = 0
secondSum = 0
thirdSum = 0
for i in range(0, finish):
    k = 10
    D = np.zeros(k, dtype=int)
    n = 6
    # P: ο προκαθορισμένος αριθμός με τον οποίο θα γίνει η διαίρεση, αποθηκευμένος σε μορφή πίνακα.
    P = [1, 1, 0, 1, 0, 1]
    T = np.zeros(k + n - 1, dtype=int)

    # Δημιουργία του αριθμού D.
    for i in range(0, k):
        D[i] = random.randint(0, 9) % 2

    # Δημιουργία του αριθμού 2^(n-k)D.
    for i in range(0, k):
        T[i] = D[i]

    FCS = CRC(T, P)

    # Δημιουργία του αριθμού Τ.
    for i in range(k, k + n - 1):
        T[i] = FCS[i]

    T_error = BER(T, k + n - 1)
    firstSum += check1(T, T_error, k + n - 1)

    # Υπολογισμός υπολοίπου της διαίρεσης T XOR P.
    R = CRC(T_error, P)
    secondSum += check2(R, k + n - 1)

    # Έλεγχος για τη το αν η εκάστοτε περίπτωση θα ανήκει στο ποσοστό του τρίτου ερωτήματος.
    if check1(T, T_error, k + n - 1) == 1:
        if check2(R, k + n - 1) == 0:
            thirdSum += 1

print("\n")

# Εκτύπωση αποτελεσμάτων.
print("Percentage of messages with error at receiver: ", (firstSum / finish) * 100, "%")
print("Percentage of messages with error detected by CRC: ", (secondSum / finish) * 100, "%")
print("Percentage of messages with error at receiver not detected by CRC: ", (thirdSum / finish) * 100, "%")
