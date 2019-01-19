import time

def is_prime(num):
	if num < 2:
		return False
	elif num == 2:
		return True
	else:
		for i in range(2, num):
			if num % i == 0:
				return False
		return True

def display_time(func):
	def wrapper():
		t1 = time.time()
		result = func()
		t2 = time.time()
		print(t2 - t1)
		return result
	return wrapper

@display_time
def prime_nums():
	count = 0
	for i in range(2, 10000):
		if is_prime(i):
			count += 1
	return count

count = prime_nums()
print(count)

def demo(name='zhh'):
	print(name)

# zhh = demo
# zhh('zhd')
class Person():
	def __init__(self):
		print('zhh1')

# my_class = Person
# my_class()

# objs = []
# objs.append(demo)
# objs.append(Person)
# for item in objs:
# 	print(item())

def pasta():
	print('dnf')
	return demo

# my_def = pasta()
# my_def('hello world')
