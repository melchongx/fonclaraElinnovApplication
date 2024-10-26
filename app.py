from flask import Flask, render_template, request, redirect, url_for
import time, math
from multiprocessing import Pool

app = Flask(__name__)

#render the page
@app.route('/')
def home():
    number = request.args.get('number', type=int, default=None)
    prime_time = request.args.get('prime_time', type=str, default=None)
    prime = request.args.get('prime', type=str, default=None)
    factorial_time = request.args.get('factorial_time', type=str, default=None)
    factorial = request.args.get('factorial', type=int, default=None)

    return render_template('index.html',
                           number= number, 
                           prime_time=prime_time, 
                           prime=prime, 
                           factorial_time=factorial_time, 
                           factorial=factorial)

# function to check if the input parameter is a prime number
def is_prime(x):
    if x <= 1:
        return False
        
    factors = []
    #loop for as much times as the input parameter and
    for i in range(1, x + 1):
        # check if i is a factor of the input parameter
        if x % i == 0:
            if len(factors) <= 2:
                # add the factor to the array if the array has less than 3 elements
                factors.append(i)
            else:
                # break out of the loop if the array has more than 2 elements
                break
        
    # if there are only 2 factors, number is a prime
    if len(factors) <= 2:
        return True
    
    return False
    
    
################################################################################
# - initial logic for getting the factorial, replaced to use multiprocessing - #

# # function to get the factorial of the input parameter
# def get_factorial(x):
#     factorial = 1
    
#     # loop for as much times as the input parameter
#     for y in range(1, x +1 ):
#         # multiply factorial to the value of y
#         factorial *= y
     
#     return factorial
################################################################################

#function to get the factorial of the chunks defined in the get_factorial function
def get_factorial_in_chunk(start, end):
    product = 1
    
    for x in range(start, end + 1):
        product *= x
        
    return product

# function to get the factorial of the input parameter using parallel processing
def get_factorial(x):
    
    # define the number of processes to use in parallel
    num_processes = 8
    
    # divide the range into chunks
    chunk_size = x // num_processes
    
    # creates ranges for the chunks eg. 1-5, 6-10
    ranges = [(i * chunk_size + 1, (i + 1) * chunk_size) for i in range(num_processes)]
    
    # adjust the last range to include any remaining numbers if not equal
    ranges[-1] = (ranges[-1][0], x)
    
    # define the process pool
    with Pool(processes=num_processes) as pool:
        results = pool.starmap(get_factorial_in_chunk, ranges)
    
    # multiply the results together using the chunks from the divided range
    factorial = 1
    for result in results:
        factorial *= result
    
    return factorial

# form action that accepts the submitted number
@app.route('/submit', methods=['POST'])
def submit():
    # get the number from input with the name post
    number = int(request.form.get('number'))
    
    prime_start_time = time.perf_counter()
    prime = is_prime(number)
    
    prime_end_time = time.perf_counter()
    prime_execution_time = prime_end_time - prime_start_time
    formatted_prime_time = f"{prime_execution_time:.6f}"
    
    # get the starting time before the get_factorial(x) function is called
    factorial_start_time = time.perf_counter()
    
    # instantiate the variable 'factorial' with the return value from get_factorial(x) function
    factorial = get_factorial(number)
    
    # get the end time after the get_factorial(x) function has returned a result and calculate for the execution time
    factorial_end_time = time.perf_counter()
    factorial_execution_time = factorial_end_time - factorial_start_time
    formatted_factorial_time = f"{factorial_execution_time:.6f}"
    
    print(f"PRIME TIME: {prime_execution_time:.6f} seconds")
    print(f"PRIME: {prime}")
    print(f"FACTORIAL TIME: {factorial_execution_time:.6f} seconds")
        
    return redirect(url_for('home',
                            number = number, 
                            prime_time=formatted_prime_time, 
                            prime=prime, 
                            factorial_time=formatted_factorial_time, 
                            factorial=factorial))
    

if __name__ == '__main__':
    app.run(debug=True)
