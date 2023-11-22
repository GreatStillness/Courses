# Problem Set 4A
# Name: <your name here>
# Collaborators:
# Time Spent: x:xx

def get_permutations(sequence):
    '''
    Enumerate all permutations of a given string

    sequence (string): an arbitrary string to permute. Assume that it is a
    non-empty string.  

    You MUST use recursion for this part. Non-recursive solutions will not be
    accepted.

    Returns: a list of all permutations of sequence

    Example:
    >>> get_permutations('abc')
    ['abc', 'acb', 'bac', 'bca', 'cab', 'cba']

    Note: depending on your implementation, you may return the permutations in
    a different order than what is listed here.
    '''
    if len(sequence) == 1:
        return [sequence]
    else:
        substring_permutations = get_permutations(sequence[1:])
        permutations = []
        first_character = sequence[0]
        for substring_permutation in substring_permutations:
            for i in range(0, len(substring_permutation) + 1):
                permutations.append(substring_permutation[0:i] + first_character + substring_permutation[i:])
        return permutations


def run_test(test_input, expected):
    print('Input: ', test_input)
    print('Expected Output: ', expected)
    print('Actual Output: ', get_permutations(test_input))


if __name__ == '__main__':
    run_test("a", ["a"])
    run_test("ej", ["ej", "je"])
    run_test("abc", ["abc", "acb", "bac", "bca", "cab", "cba"])
