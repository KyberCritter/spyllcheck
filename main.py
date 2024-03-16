# Scott Ratchford, 2024

import sys
import numpy as np
import json

def lev(a: str, b: str) -> int:
    """Returns the Levenshtein distance from the first string to the second string. This is a recursive implementation with O(3^n) time complexity, so it is not recommended for use.

    Args:
        a (str): String to calculate from
        b (str): String to calculate to

    Returns:
        int: The Levenshtein distance from the first string to the second string
    """
    if len(b) == 0:
        return len(a)
    elif len(a) == 0:
        return len(b)
    elif a[0] == b[0]:
        return lev(a[1:], b[1:])
    else:
        return 1 + min(lev(a[1:], b), lev(a, b[1:]), lev(a[1:], b[1:]))
    
def wag_fis(a: str, b: str) -> np.ndarray[int]:
    """Returns array of the Levenshtein distances from the first string to the second string, using the Wagner-Fischer algorithm.

    Args:
        a (str): String to calculate from
        b (str): String to calculate to

    Returns:
        np.ndarray[int]: The array of the Levenshtein distances from the first string to the second string
    """
    if len(b) == 0:
        return len(a)
    elif len(a) == 0:
        return len(b)
    arr = np.full((len(a)+1, len(b)+1), -1, int)
    # set first row and col of arr to increment by 1
    arr[0] = range(0, len(b)+1)
    arr[:, 0][1:] = range(1, len(a)+1)
    for i in range(1, arr.shape[0]):
        for j in range(1, arr.shape[1]):
            # for every element in arr, check the values for deletion, insertion, and substitution operations
            if a[i-1] == b[j-1]:    # letters are equal, use min of the operations
                arr[i][j] = min(arr[i-1][j-1], arr[i][j-1], arr[i-1][j])
            else:                   # letters are not equal, use min of the operations + 1
                arr[i][j] = min(arr[i-1][j-1], arr[i][j-1], arr[i-1][j]) + 1
    # only appears as expected using print(arr.T) (transposed array)
    # arr[-1][-1] is the distance
    return arr

def wag_fis_dist(a: str, b: str) -> int:
    """Returns the Levenshtein distance from the first string to the second string, using the Wagner-Fischer algorithm.

    Args:
        a (str): String to calculate from
        b (str): String to calculate to

    Returns:
        int: The Levenshtein distance from the first string to the second string
    """
    return wag_fis(a, b)[-1][-1]+1

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python main.py <input_word>")
        sys.exit(1)
    word = sys.argv[1]
    
    with open("words_dictionary.json", "rb") as f:
        english = json.load(f)
    assert type(english) == dict

    if word in english.keys():
        print("Spelled correctly")
    else:
        suggestions = []
        for i, dict_word in enumerate(english):
            suggestions.append((dict_word, wag_fis_dist(word, dict_word)))
        suggestions.sort(key=lambda x: x[1])
        print(f"Top 10 suggested words:")
        for x in suggestions[:10]:
            print(x[0])
