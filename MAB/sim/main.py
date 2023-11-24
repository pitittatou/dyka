"""
Tool to simulate a user response to vibration patterns/frequency
Let's say that our frequency range is [0 - 1000]
"""

from user import *

def main():
    user = ComplexUser.new_random_user()
    print(user.get_state_with_memory())
    for _ in range (0, 5):
        print(user.get_next_state_with_memory(400))


if __name__ == '__main__':
    main()
