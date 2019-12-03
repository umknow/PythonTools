# -*- coding=utf-8 -*-
# author: king
# datetime: 2019/11/27 15:14
# describtion: 
"""
    常规排序算法Python实现
"""
import math
import copy


def print_tree(array):  # 打印堆排序使用
    """
        【树打印函数】
        深度 前空格 元素间空格
        1     7       0
        2     3       7
        3     1       3
        4     0       1
    :param array: 数组
    :return: 
    """
    # first=[0]
    # first.extend(array)
    # array=first
    index = 0
    depth = math.ceil(math.log2(len(array)))  # 因为补0了，不然应该是math.ceil(math.log2(len(array)+1))
    sep = '  '
    for i in range(depth):
        offset = 2 ** i
        print(sep * (2 ** (depth - i - 1) - 1), end='')
        line = array[index:index + offset]
        for j, x in enumerate(line):
            print("{:>{}}".format(x, len(sep)), end='')
            interval = 0 if i == 0 else 2 ** (depth - i) - 1
            if j < len(line) - 1:
                print(sep * interval, end='')
        index += offset
        print()


class Sorted(object):
    """排序类"""
    def __init__(self, alist=[]):
        self._alist = alist
        if not self._alist:
            raise ImportError("输入不能为空！")

    def bubbling_sort(self):
        """【交换排序类】冒泡排序"""
        __alist = copy.deepcopy(self._alist)
        l = len(__alist)-1
        for i in range(l):
            flag = False
            for j in range(i, l):
                if __alist[j] > __alist[j+1]:
                    __alist[j], __alist[j+1] = __alist[j+1], __alist[j]
                    flag = True
                else:
                    continue
            else:
                if not flag:
                    break
        return __alist

    def fast_sort(self):
        """【交换排序类】快速排序
            基本原理：左右遍历，找出符合条件的值替换，当游标重合时再度拆分重合处左右两个区间进行下一步循环
            如法递归下去，回归得到最终排序好的列表
        """
        __alist = copy.deepcopy(self._alist)
        start = 0
        end = len(__alist) - 1

        def __builtin_sort(alist, start, end):
            if start >= end:
                return
            low = start
            high = end
            base = alist[low]
            while low < high:
                while low < high and alist[high] >= base:
                    high -= 1
                alist[low] = alist[high]
                while low < high and alist[low] < base:
                    low += 1
                alist[high] = alist[low]
            alist[low] = base

            __builtin_sort(alist, low+1, end)
            __builtin_sort(alist, start, low-1)

        __builtin_sort(__alist, start, end)
        return __alist

    def insert_sort(self):
        """【插入排序类】直接插入排序
            基本原理：从 _ 开始维护一个排序好的列表，然后在一个个遍历向维护好的队列中插入
            实现很类似冒泡，但是冒泡需要优化重复交换问题
        """
        __alist = copy.deepcopy(self._alist)
        l = len(__alist)
        for i in range(l):
            for j in range(i, 0, -1):
                if __alist[j] < __alist[j-1]:
                    __alist[j], __alist[j-1] = __alist[j-1], __alist[j]
                else:
                    break
        return __alist

    def hill_sort(self):
        """【插入排序类】希尔排序
            是对插入排序的优化
            实现原理：按照一定的间隙将原序列分成多个子序列，在子序列中完成插入排序
        """
        __alist = copy.deepcopy(self._alist)
        n = len(__alist)
        gap = n//2
        while gap >= 1:
            for i in range(gap, n):
                while (i-gap) >= 0:
                    if __alist[i] < __alist[i-gap]:
                        __alist[i], __alist[i-gap] = __alist[i-gap], __alist[i]
                        i -= gap
                    else:
                        break
            gap //= 2

        return __alist

    def select_sort(self):
        """【选择排序类】简单选择排序
            原理：假设一个最小值对应的索引，每趟比较都会更新/选择最小值对应的索引
            在每趟比较中，找到本趟中最小的元素放在本趟比较的第1个位置
        """
        __alist = copy.deepcopy(self._alist)
        n = len(__alist)
        for i in range(n-1):  # 游标（从左到右）
            min_index = i
            for j in range(i+1, n):
                if __alist[j] < __alist[min_index]:
                    min_index = j
            if min_index != i:
                __alist[min_index], __alist[i] = __alist[i], __alist[min_index]

        return __alist

    def heap_sort(self):
        """【选择排序类】堆排序 （小顶堆）（升序）
            小顶堆特点：
                1、完全二叉树
                2、根节点小于对应子节点
            小顶堆的创建：
                1、初始化加载序列（就是将列表中的元素加载成完全二叉树格式）
                2、重复下沉操作（格式化成小顶堆的格式）
            此时，并没有完成排序操作，还要进一步对
        """

        def min_heapify(heap, heapSize, root):
            left = 2 * root + 1
            right = 2 * root + 2
            # 父节点i的左子节点在位置(2*i+1);
            # 父节点i的右子节点在位置(2*i+2);
            max_node = root
            if left < heapSize and heap[left] < heap[max_node]:  # 可调整升序或降序(即大顶/小顶)
                max_node = left
            if right < heapSize and heap[right] < heap[max_node]:
                max_node = right
            if max_node != root:
                heap[max_node], heap[root] = heap[root], heap[max_node]
                min_heapify(heap, heapSize, max_node)

        def build_min_heap(heap):
            """构建小顶堆（因为我们需要升序排序）层次遍历以数组的方式呈现"""
            n = len(heap)
            # 从(heapSize -2)//2处开始调整，一直调整到第一个根节点
            for i in range((n - 2) // 2, -1, -1):
                min_heapify(heap, n, i)
            return heap

        # 构建大根堆
        __alist = copy.deepcopy(self._alist)
        min_heap = build_min_heap(__alist)  # 格式化成小顶堆
        print(min_heap)
        print_tree(min_heap)  # 直观的查看一下最大堆格式化的准确性
        n = len(min_heap)
        __new_alist = []
        for i in range(n-1):
            min_heap[0], min_heap[-1] = min_heap[-1], min_heap[0]
            __new_alist.append(min_heap.pop(-1))
            min_heapify(min_heap, len(min_heap), 0)
        __new_alist += min_heap

        return __new_alist

    def merge_sort(self):
        """【归并排序类】归并排序
        实现原理：
            把表依次对折拆分，直到拆成单个元素
            通过两两比较原路合并
            递归调用，最终终止条件
        """
        def __sort(alist):
            n = len(alist)
            if n == 1:
                return alist
            left, right = 0, 0
            mid = n // 2
            # 拆分
            left_list = __sort(alist[:mid])
            right_list = __sort(alist[mid:])

            # 合并
            merge_sorted_list = []
            lcount = len(left_list)
            rcount = len(right_list)
            while left < lcount and right < rcount:
                if left_list[left] < right_list[right]:
                    merge_sorted_list.append(left_list[left])
                    left += 1
                else:
                    merge_sorted_list.append(right_list[right])
                    right += 1
            # 追加左右两个列表中没有比较完的元素
            merge_sorted_list += left_list[left:]
            merge_sorted_list += right_list[right:]

            return merge_sorted_list

        __alist = copy.deepcopy(self._alist)
        return __sort(__alist)


if __name__ == '__main__':

    alist = [4, 2, 6, 10, 7, 8]
    # alist = [1, 2, 6, 10, 17, 18]
    s = Sorted(alist)
    print("【original list】", alist)
    print("【bubbling_sort】", s.bubbling_sort())
    print("【fast_sort】", s.fast_sort())
    print("【heap_sort】", s.heap_sort())
    print("【hill_sort】", s.hill_sort())
    print("【insert_sort】", s.insert_sort())
    print("【merge_sort】", s.merge_sort())
    print("【select_sort】", s.select_sort())
