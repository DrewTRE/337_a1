import sys
import copy
# S-Boxes
#		 00  01  10  11
s1 = [	[15, 10,  2,  5], 	#00
		[ 8,  4, 11,  6],	#01
		[ 1,  0, 14,  7],	#10
		[ 9,  3, 12, 13]]	#11

#		 00  01  10  11
s2 = [	[ 4,  0, 10, 15], 	#00
		[ 9,  8,  7, 13],	#01
		[ 5,  1,  6, 11],	#10
		[ 2,  3, 14, 12]]	#11

# Plain Text
p 	= [[1,0,0,0], [1,1,0,0], [1,1,0,1], [0,1,1,0]]
p1 	= [[1,1,1,1], [0,1,0,1], [0,1,1,0], [0,1,1,0]]
p2	= [[0,0,1,0], [1,0,0,1], [1,1,0,0], [0,0,1,0]]
p3	= [[0,1,0,1], [1,1,0,0], [1,1,1,0], [0,0,1,0]]
p4	= [[1,1,1,0], [0,1,1,1], [1,1,0,0], [0,0,1,1]]
p5 	= [[0,0,1,1], [1,1,1,0], [1,1,1,1], [0,0,1,0]]
# Keys
k 	= [[0,0,0,1], [0,0,1,1], [0,0,1,0], [1,1,1,1]]
k1 	= [[1,1,1,0], [1,0,1,0], [0,0,1,1], [1,0,0,0]]
k2	= [[1,0,1,1], [1,1,0,1], [1,0,0,0], [0,0,0,1]]

ex 	= [None] * 4
ex2 	= [None] * 4
check	= []
a1		= [None] * 4
a2	 	= [None] * 4
b1		= [None] * 4
b2		= [None] * 4
c1		= [None] * 4
c2		= [None] * 4
d1		= [None] * 4
d2		= [None] * 4
e1		= [None] * 4
e2		= [None] * 4

class functions:
	bitCounter = 0
	calculations = 0 

	def returnCalculations(self):
		return functions.calculations

	def returnBitCounter(self):
		return functions.bitCounter

	def resetBitCounter(self):
		functions.bitCounter = 0

	def xor (self, plain, key):
		xorArray = [None] * 4
		for arrayIndex in range(4): 
			int1 				= plain[arrayIndex]
			int2 				= key[arrayIndex]
			xorNum 				= int1 ^ int2
			xorArray[arrayIndex]= xorNum
			functions.calculations += 1
		
		return xorArray

	def encrypt(self, sbox, plain, key):
		newNum = self.xor(plain, key)

		if newNum[0] == 0 and newNum[1] == 0:
			index1 = 0 
		if newNum[2] == 0 and newNum[3] == 0:
			index2 = 0 
		if newNum[0] == 0 and newNum[1] == 1:
			index1 = 1 
		if newNum[2] == 0 and newNum[3] == 1:
			index2 = 1 
		if newNum[0] == 1 and newNum[1] == 0:
			index1 = 2 
		if newNum[2] == 1 and newNum[3] == 0:
			index2 = 2 
		if newNum[0] == 1 and newNum[1] == 1:
			index1 = 3 
		if newNum[2] == 1 and newNum[3] == 1:
			index2 = 3 

		cipher = sbox[index2][index1]	
		return cipher

	def encryptionFeed (self, array, array2, sbox1, sbox2, plainText, key):	
		array[0] 		= self.encrypt(sbox1, plainText[1], key[0])
		array[1]		= self.encrypt(sbox2, plainText[3], key[2])
		array[2] 		= self.encrypt(sbox1, plainText[0], key[1])
		array[3] 		= self.encrypt(sbox2, plainText[2], key[3])
		
		array3 	= []
		array4 	= []
		array5 	= []

		for data in array: 
			convert = ('{:04b}'.format(data))	
			array3.append(convert)

		for i in range(4):
			for j in range(4):
				number = int(array3[i][j])
				array4.append(number) 

		for i in range(4):
			array5.append(array4[i])
		array2[0] = array5
		array5 	= []

		for i in range(4,8):
			array5.append(array4[i])
		array2[1] = array5
		array5 	= []

		for i in range(8,12):
			array5.append(array4[i])
		array2[2] = array5
		array5 	= []

		for i in range(12,16):
			array5.append(array4[i])
		array2[3] = array5

		return array

	def bitCheck(self, array, array2):
		for i in range(4):
			for j in range(4):
				if array[i][j] != array2[i][j]: 
					functions.bitCounter += 1
		return functions.bitCounter

	def calculateAvalanche(self, array, array2, sbox1, sbox2, plainText, key):	
		for i in range(4):
			for j in range(len(key)):
				if key[i][j] == 0:				
					key[i][j] = 1	
					
					self.encryptionFeed (array, array2, sbox1, sbox2, plainText, key)
					self.shiftBits(array2)
					self.bitCheck(plainText, array2)
					key[i][j] = 0
				
				else: 			
					key[i][j] = 0	
					self.encryptionFeed (array, array2, sbox1, sbox2, plainText, key)	
					self.shiftBits(array2)	
					self.bitCheck(plainText, array2)
					key[i][j] = 1
	
	def calculateAvgAv(self):
		average = functions.bitCounter / float(2560)
		print "Avalanche Average is: "
		return average

	def shiftBits(self, array2):
		copyArray 	= copy.deepcopy(array2)
		array2[0]	= copyArray[2]
		array2[1]	= copyArray[3]
		array2[2]	= copyArray[1]	
		array2[3]	= copyArray[0]	 

		return array2

def Test():
	
	print("Example")
	a = functions()
	a.encryptionFeed(ex, ex2, s1, s2, p, k)
	a.calculateAvalanche(ex, ex2, s1, s2, p, k)

	print("Plain 1")
	a1f = functions()
	print a1f.encryptionFeed(a1, a2, s1, s2, p1, k1)
	print a2, "\n"
	print a1f.encryptionFeed(a1, a2, s1, s2, p1, k2)
	print a2, "\n"
	a1f.calculateAvalanche(a1, a2, s1, s2, p1, k1)
	a1f.calculateAvalanche(a1, a2, s1, s2, p1, k2)

	print("Plain 2")
	a2f = functions()
	print a2f.encryptionFeed(b1, b2, s1, s2, p2, k1)
	print b2, "\n"
	print a2f.encryptionFeed(b1, b2, s1, s2, p2, k2)
	print b2, "\n"
	a2f.calculateAvalanche(b1, b2, s1, s2, p1, k1)
	a2f.calculateAvalanche(b1, b2, s1, s2, p1, k2)

	print("Plain 3")
	a3f = functions()
	print a3f.encryptionFeed(c1, c2, s1, s2, p3, k1)
	print c2, "\n"
	print a3f.encryptionFeed(c1, c2, s1, s2, p3, k2)
	print c2, "\n"
	a3f.calculateAvalanche(c1, c2, s1, s2, p1, k1)
	a3f.calculateAvalanche(c1, c2, s1, s2, p1, k2)
	
	print("Plain 4")
	a4f = functions()
	print a4f.encryptionFeed(d1, d2, s1, s2, p4, k1)
	print d2, "\n"
	print a4f.encryptionFeed(d1, d2, s1, s2, p4, k2)
	print d2, "\n"
	a4f.calculateAvalanche(d1, d2, s1, s2, p1, k1)
	a4f.calculateAvalanche(d1, d2, s1, s2, p1, k2)
	
	print("Plain 5")
	a5f = functions()
	print a5f.encryptionFeed(e1, e2, s1, s2, p5, k1)
	print e2, "\n"
	print a5f.encryptionFeed(e1, e2, s1, s2, p5, k2)
	print e2, "\n"
	a5f.calculateAvalanche(e1, e2, s1, s2, p1, k1)
	a5f.calculateAvalanche(e1, e2, s1, s2, p1, k2)
	
	print a.calculateAvgAv()
	
#===============================================
Test()




