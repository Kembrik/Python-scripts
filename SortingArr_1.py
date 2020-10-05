arrItem = [10,5,8,7,6,10,5,8,7,6,10,5,8,7,6,10,5,8,7,6,10,5,8,7,6,10,5,8,7,6]
# arrItem = [8,11,6,9,7,13,8,14,9,8,6,6,9,9,7,12,5,6,8,8,12,9,9,14,8,9,6,13,12,8,8,5,12,8,7,8,12,8,7,13,8,9,6,8,14,7,6]


# arrQuality = [1,2,3,4,5,9,11,30]
# numbers = len(arrQuality)
summa = 40
# tmp_num = []
# tmp_sol = []

def SortQuality(arrItem):
	arrQuality = [0 for i in range(1, 19)]
	for i in arrItem:
		arrQuality[i] +=1
	return arrQuality

def GroupingItems(arrQuality):
	arrGroupQual = []
	tmpArr = [1]
	# numQuality = len(arrQuality)-1
	numQuality = 1
	while tmpArr:
		tmpArr = []
		summa = 40
		tmpQual, tmpArr, arrQuality = rec(summa, numQuality, tmpArr, arrQuality)
		if tmpQual:
			tmpArr.append(tmpQual)
			arrGroupQual.append(tmpArr)
			numQuality = tmpQual
	return arrGroupQual, arrQuality

def rec(summa, numQual, tmpArr, arr1):
	# for quality in range(numQual, 0, -1):
	for quality in range(numQual, len(arr1) - 1):
		if arr1[quality] > 0:
			if quality > summa:	break
			if (summa-quality) == 0:
				arr1[quality] -= 1
				return quality, tmpArr, arr1
			elif (summa-quality) > 0:
				arr2 = arr1.copy()
				arr2[quality] -= 1

				if (summa - quality) > quality:
					tmpQual, tmpArr, arr2 = rec(summa - quality, quality, tmpArr, arr2)
				else:
					tmpQual, tmpArr, arr2 = rec(summa - quality, summa - quality, tmpArr, arr2)
				if tmpQual > 0:
					arr1 = arr2.copy()
					tmpArr.append(tmpQual)
					return quality, tmpArr, arr1
	return 0, tmpArr, arr1

if __name__ == "__main__":
	arrQuality = SortQuality(arrItem)
	print(sum(arrQuality), arrQuality)
	arrGroupQual, arrQuality = GroupingItems(arrQuality)
	print(len(arrGroupQual),arrGroupQual)
	print(sum(arrQuality), arrQuality)
