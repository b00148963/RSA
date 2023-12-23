from sympy import factorint

number = 510143758735509025530880200653196460532653147
factors = factorint(number)

# Get smaller prime factor
smallerPrime = min(factors.keys())
print(smallerPrime)
