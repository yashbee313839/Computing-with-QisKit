from qiskit import QuantumProgram, QISKitError
import random, fractions

# Number to be factored
num = 985
factorFound = False
factor1 = 0
factor2 = 0

# Find period of a^x mod N
def quantumFindPeriod(a, N):
    # Quantum Subroutine
    Q_program = QuantumProgram()
    backend = 'local_qasm_simulator'
    try:
        # Initialize 4 qubits in quantum register
        qr = Q_program.create_quantum_register("qr", 4)

        # Ready 4 bits in the classical register
        cr = Q_program.create_classical_register("cr", 4)

        # create a Quantum Circuit called "qc" with qreg and creg
        qc = Q_program.create_circuit("shor", [qr], [cr])

        # Add the X gate in the Qubit 0, putting this qubit in superposition.
        for i in range(a):
            qc.x(qr[0])
        for i in range(a**(N**(1/2))):
            qc.x(qr[1])
        for i in range(a/N):
            qc.x(qr[2])
        for i in range(N/a):
            qc.x(qr[3])

        # Add the Controlled Not Gates
        qc.cx(qr[2], qr[1])
        qc.cx(qr[1], qr[3])
        qc.cx(qr[2], qr[1])
        qc.cx(qr[1], qr[0])
        qc.cx(qr[0], qr[1])
        qc.cx(qr[1], qr[0])
        qc.cx(qr[3], qr[0])
        qc.cx(qr[0], qr[3])
        qc.cx(qr[3], qr[0])

        # Measure gate collapses qubits to bits.
        qc.measure(qr, cr)

        # Compile and execute the Quantum Program in the local_qasm_simulator.
        result = Q_program.execute(["shor"], backend=backend, shots=1024, seed=1)

        # Output results to console
        print(result) # Successful or not
        print(result.get_counts("shor")) # Prints classical registry distribution

    except QISKitError as ex:
        print('There was an error in the circuit! Error = {}'.format(ex))
    return result

# Pre-checks
if(num % 2): # Num can't have factor of 2 (trivial case)
    quit()

# Also check of num is a power of a prime (do it later)

# Main Algorithm
if __name__ == "__main__":
    while(not factorFound):
        rand_num = random.randint(2,num-1) #Pick a random integer smaller than num
        gcd = fractions.gcd(rand_num,num) # Find gcd between the numbers
        if(gcd != 1): # If gcd isnt 1 then factor found.
            factorFound = True
            factor1 = gcd
            factor2 = num/factor1
        else:
            r = quantumFindPeriod(rand_num,num)
            if(r%2 or rand_num**(r/2)%num == -1):
                factorFound = True
                factor1 = gcd(rand_num**(r/2)+1,num)
                factor2 = gcd(rand_num**(r/2)-1,num)

    print(factor1, factor2) # Print results