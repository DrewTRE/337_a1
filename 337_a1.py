import sys
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
k1 	= [[0,0,0,1], [0,0,1,1], [0,0,1,0], [1,0,0,0]]
k2	= [[1,0,1,1], [1,1,0,1], [1,0,0,0], [0,0,0,1]]

encryptArrExample	= [None] * 4
encryptArr1			= [None] * 4
encryptArr2			= [None] * 4
encryptArr3			= [None] * 4
encryptArr4			= [None] * 4
encryptArr5			= [None] * 4

class functions:
	bitCounter = 0
	calculations = 0 
	fullXorArray = []

	def returnCalculations(self):
		return functions.calculations

	def returnBitCounter(self):
		return functions.bitCounter

	def returnXorArray(self):
		return functions.fullXorArray

	def resetBitCounter(self):
		functions.bitCounter = 0

	def resetCalculations(self):
		functions.calculations = 0

	def calculateAvalanche(self):
		avalanche = functions.bitCounter / float(16 * 16 * 5 * 2)
		
		return avalanche

	def xor (self, plain, key):
		xorArray = [None] * 4
		for arrayIndex in range(4): 
			int1 				= plain[arrayIndex]
			int2 				= key[arrayIndex]
			xorNum 				= int1 ^ int2
			xorArray[arrayIndex]= xorNum
			functions.calculations += 1
			if int1 != xorNum:
				functions.bitCounter += 1
			# functions.fullXorArray[arrayIndex] = functions.fullXorArray.append(xorNum)
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

		cipherText = sbox[index2][index1]
		
		return cipherText

	def encryptionFeed (self, array, sbox1, sbox2, plainText, key):
		array[0] = self.encrypt(sbox1, plainText[1], key[0])
		array[1] = self.encrypt(sbox2, plainText[3], key[2])
		array[2] = self.encrypt(sbox1, plainText[0], key[1])
		array[3] = self.encrypt(sbox2, plainText[2], key[3])
		print(array)
		binary = []
		for data in array: 
			convert = ('{:04b}'.format(data))
			binary.append(convert)
		print(binary)
		print(" ")

def Test():
	print("Example")
	a = functions()
	a.encryptionFeed(encryptArrExample, s1, s2, p, k)
	print "Bits Changed: " , a.returnBitCounter()
	print "Reset calculations and bitCounter"
	a.resetCalculations()
	a.resetBitCounter()

	print("\nPlain 1")
	a1 = functions()
	a1.encryptionFeed(encryptArr1, s1, s2, p1, k1)
	print "Bits Changed: " , a.returnBitCounter()
	print "Number of Calculations: " , a.returnCalculations()
	a1.encryptionFeed(encryptArr1, s1, s2, p1, k2)
	print "Bits Changed: " , a.returnBitCounter()
	print "Number of Calculations: " , a.returnCalculations()
	
	print("\nPlain 2")
	a2 = functions()
	a2.encryptionFeed(encryptArr2, s1, s2, p2, k1)
	a2.encryptionFeed(encryptArr2, s1, s2, p2, k2)
	print "Bits Changed: " , a.returnBitCounter()
	print "Number of Calculations: " , a.returnCalculations()

	print("\nPlain 3")
	a3 = functions()
	a3.encryptionFeed(encryptArr3, s1, s2, p3, k1)
	a3.encryptionFeed(encryptArr3, s1, s2, p3, k2)
	print "Bits Changed: " , a.returnBitCounter()
	print "Number of Calculations: " , a.returnCalculations()
	
	print("\nPlain 4")
	a4 = functions()
	a4.encryptionFeed(encryptArr4, s1, s2, p4, k1)
	a4.encryptionFeed(encryptArr4, s1, s2, p4, k2)
	print "Bits Changed: " , a.returnBitCounter()
	print "Number of Calculations: " , a.returnCalculations()
	
	print("\nPlain 5")
	a5 = functions()
	a5.encryptionFeed(encryptArr5, s1, s2, p5, k1)
	a5.encryptionFeed(encryptArr5, s1, s2, p5, k2)
	print "Bits Changed: " , a.returnBitCounter()
	print "Number of Calculations: " , a.returnCalculations()
	print "Average Avalanche: " , a.calculateAvalanche() 
	
#===============================================
Test()


# encryptArrExample[0] = encrypt(s1, p[1], k[0])
# encryptArrExample[1] = encrypt(s2, p[3], k[2])
# encryptArrExample[2] = encrypt(s1, p[0], k[1])
# encryptArrExample[3] = encrypt(s2, p[2], k[3])

# encryptArr1[0] = encrypt(s1, p1[1], k[0])
# encryptArr1[1] = encrypt(s2, p1[3], k[2])
# encryptArr1[2] = encrypt(s1, p1[0], k[1])
# encryptArr1[3] = encrypt(s2, p1[2], k[3])

# print(encryptArrExample)
# print(encryptArr1)



