import time

list1 = ['a', 'b', 'c']
list2 = [1, 2, 3]

if __name__ == "__main__":
	startTime = time.time()
	list1 = list1.extend(list2)
	print("Time:",time.time()-startTime)
