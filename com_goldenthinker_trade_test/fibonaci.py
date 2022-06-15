import time


def fib_a(n):
    fibs = [0, 1]
    for i in range(2, n+1):
        fibs.append(fibs[-1] + fibs[-2])
    return fibs


def fib_b(n, computed = {0: 0, 1: 1}):
    if n not in computed:
        computed[n] = fib_b(n-1, computed) + fib_b(n-2, computed)
    return computed[n]


start = time.time()
print("Fibonacci 400 a:" + str(fib_a(400)))
end = time.time()
print("It took: " + str(end - start))

start = time.time()
print("Fibonacci 400 b:" + str(fib_b(400)))
end = time.time()
print("It took: " + str(end - start))



# Python program to find equilibrium
# index of an array

# function to find the equilibrium index
def equilibrium(arr):
    leftsum = 0
    rightsum = 0
    n = len(arr)

    # Check for indexes one by one
    # until an equilibrium index is found
    for i in range(n):
        leftsum = 0
        rightsum = 0
        
        # get left sum
        for j in range(i):
            leftsum += arr[j]
            
        # get right sum
        for j in range(i + 1, n):
            rightsum += arr[j]
        
        # if leftsum and rightsum are same,
        # then we are done
        if leftsum == rightsum:
            return i
    
    # return -1 if no equilibrium index is found
    return -1
            
# driver code
arr = [-7, 1, 5, 2, -4, 3, 0]
print (equilibrium(arr))

# This code is contributed by Abhishek Sharama