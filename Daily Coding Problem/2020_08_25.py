# Good morning! Here's your coding interview problem for today.
#
# This problem was recently asked by Google.
#
# Given a list of numbers and a number k, return whether any two numbers from
# the list add up to k.
#
# For example, given [10, 15, 3, 7] and k of 17, return true since 10 + 7 is 17.

print("Give me a number please! Let me know when you want to stop.", end = ' ')

numbers = []
number = int(input())
numbers.append(number)

while True:
  print("Do you have any more numbers?", end = ' ')
  answer = input()
  if answer == "Yes" or answer == "yes":
      print("Give me another number!", end = ' ')
      number = int(input())
      numbers.append(number)
  else:
      print("Give me a special number.", end = ' ')
      specialNumber = int(input())
      break

for i in range(len(numbers)):
    for j in range(len(numbers)):
        if i != j and numbers[i] + numbers[j] == specialNumber:
            return True
        else:
            return False
