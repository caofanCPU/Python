"""
Problem Statement:
If we list all the natural numbers below 10 that are multiples of 3 or 5,
we get 3,5,6 and 9. The sum of these multiples is 23.
Find the sum of all the multiples of 3 or 5 below N.
"""
from __future__ import print_function

N = 10
N_limit = 101
while N < N_limit:
    # raw_input = input("请输入一个大于3的自然数:")
    # n = int(filter(str.isdigit(), raw_input))
    n = N
    sum_ = 0
    for e in range(3, n):
        if e % 3 == 0 or e % 5 == 0:
            sum_ += e
    print(sum_)
    N += 10
