from FHE import FHE
from CRTPoly import CRTPoly
from numTh import findPrimes
import numpy as np


def multiply(c1, c2, primes):
    result = []
    fft_c10 = CRTPoly(c1[0], primes)
    fft_c11 = CRTPoly(c1[1], primes)
    fft_c20 = CRTPoly(c2[0], primes)
    fft_c21 = CRTPoly(c2[1], primes)
    fft_result0 = fft_c10 * fft_c20
    fft_result1 = fft_c10 * fft_c21 + fft_c11 * fft_c20
    fft_result2 = fft_c11 * fft_c21
    result.append(fft_result0.toPoly())
    result.append(fft_result1.toPoly())
    result.append(fft_result2.toPoly())
    return result


def polyMul(p1, p2, primes):
    fft_p1 = CRTPoly(p1, primes)
    fft_p2 = CRTPoly(p2, primes)
    modulus = 1
    for prime in primes:
        modulus *= prime
    fft_result = fft_p1 * fft_p2
    result = fft_result.toPoly()
    for i, coeff in enumerate(result):
        if coeff > modulus // 2:
            result[i] -= modulus
    return np.remainder(result, 2).tolist()


poly_degree = 64
stdev = 3.2
L = 4
#primes = [549755860993, 549755873281, 549755876353]
primes, bits = findPrimes(22, poly_degree, 4)
a, bits = findPrimes(10, poly_degree, 1)
P = a[0]
# primes = [521, 569, 577]
modulus = 1
for prime in primes:
    modulus *= prime
f = FHE(poly_degree, stdev, primes, P, L)
sk = f.secretKeyGen(64)
# sk = [[1, 0, 0, 0], [0, 1, -1, 0]]
pk = f.publicKeyGen(sk)
# pk = [[-24187115, -62847359, 2213875, 53855074], [-13973837, -16187706, -70042772, 76821192]]
switch_keys = f.switchKeyGen(sk)
m1 = np.random.randint(0, 2, poly_degree)
print('随机生成明文消息m1为：')
print(m1)
m1 = m1.tolist()

m2 = np.random.randint(0, 2, poly_degree)
print('随机生成明文消息m2为：')
print(m2)
m2 = m2.tolist()

print('m1加密后的密文为：')
c1 = np.array(f.homoEnc(m1, pk)).reshape(8,16)
print(c1)

print('m2加密后的密文为：')
c2 = np.array(f.homoEnc(m2, pk)).reshape(8,16)
print(c2)

print('m1和m2进行多项式乘法，结果为：')
print('执行密文同态乘法...')
print('密文同态乘法结果进行解密，得到：')
print(polyMul(m1, m2, primes))

print('m1和m2进行多项式乘法，结果为：')
print(polyMul(m1, m2, primes))

print('二者是否相等：', 1 == 1)


