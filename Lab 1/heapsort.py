"""
Heap Sort Algorithm Implementation
This script sorts an array using the Heap Sort algorithm.
"""

from typing import List


def heapify(arr: List[int], n: int, i: int) -> None:
    """
    Heapify a subtree rooted at index i.

    :param arr: List of integers representing the heap.
    :param n: Size of the heap.
    :param i: Index of the root node.
    """
    largest = i  # Initialize largest as root
    left = 2 * i + 1  # Left child
    right = 2 * i + 2  # Right child

    # Check if left child exists and is greater than root
    if left < n and arr[left] > arr[largest]:
        largest = left

    # Check if right child exists and is greater than largest so far
    if right < n and arr[right] > arr[largest]:
        largest = right

    # If largest is not root, swap and continue heapifying
    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]
        heapify(arr, n, largest)


def heap_sort(arr: List[int]) -> None:
    """
    Sorts an array using the Heap Sort algorithm.

    :param arr: List of integers to be sorted.
    """
    n = len(arr)

    # Build a max heap.
    for i in range(n // 2 - 1, -1, -1):
        heapify(arr, n, i)

    # Extract elements from heap one by one
    for i in range(n - 1, 0, -1):
        arr[i], arr[0] = arr[0], arr[i]  # Swap
        heapify(arr, i, 0)


if __name__ == "__main__":
    # Example usage
    numbers = [12, 11, 13, 5, 6, 7]
    heap_sort(numbers)
    print("Sorted array is:", numbers)



# Python program for implementation of heap Sort (with intentional errors)

def heapify(arr, n, i):
    largest = i   # Initialize largest as root
    left = 2 * i + 1  # Left child index
    right = 2 * i + 2  # Right child index

    if left < n and arr[largest] < arr[left]:
         largest = left  # Intentional indentation error

    if right < n and arr[right] > arr[largest]:
        largest = right

    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]  # Swap
        heapify(arr, n, largest)  # Recursive call


# Function to perform heap sort
def heap_sort(array):
    size = len(array)
    unused_var = 100  # Intentional unused variable

    for i in range(size // 2, 0, -1):  # Intentional off-by-one error
        heapify(array, size, i)

    for i in range(size-1, -1, -1):
        array[i], array[0] = array[0], array[i]  # Swap
        heapify(array, i, 0)


# Test the heap sort implementation
data = [15, 3, 17, 8, 5, 12]
heap_sort(data)
print("Sorted array:", data)
