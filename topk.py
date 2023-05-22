'''    
1. Replace folder name "202312345" with your student !! 
   !!WARNING!! you will get 0 score, 
   if your folder name is "202312345"
2. Implement Fagin method
3. Implement TA method
4. Implement NRA method

Input: num_dim, top_k
    num_dim: Number of dimension
    top_k: Variable k in top-'k' query
Output: uids_result, cnt_access
    uid_result: Result of top-k uids of the scores. 
                The summation function is used 
                for the score function.

                i.e., num_dim = 4, k = 2
                ----------------------------
                 uid    D0   D1    D2    D3
                ----------------------------
                "001"    1    1     1     1
                "002"    2    2     2     2
                "003"    3    3     3     3
                "004"    5    5     5     5
                ----------------------------                
                
                score("001") = 1 + 1 + 1 + 1 = 4
                score("002") = 2 + 2 + 2 + 2 = 8
                score("003") = 3 + 3 + 3 + 3 = 12  --> top-2
                score("004") = 4 + 4 + 4 + 4 = 16  --> top-1
                
                uids_result: ["004", "003"]

    cnt_access: Number of access in each algorithm

Tip: Use Naive method to check your code
     Naive method is the free gift for the code understanding
'''
from collections import defaultdict
from typing import Tuple


def get_score(list_values) -> float:
    result = 0.0
    for v in list_values:
        result += v
    return result


class Algo():
    def __init__(self, list_sorted_entities, uid2dim2value):
        self.list_sorted_entities = list_sorted_entities

        '''
        variable for random access,
        but please do not use this variable directly.
        If you want to get the value of the entity,
        use method 'random_access(uid, dim)'
        '''
        self.__uid2dim2value__ = uid2dim2value

    def random_access(cls, uid, dim) -> float:
        return cls.__uid2dim2value__[uid][dim]

    def Naive(cls, num_dim, top_k) -> Tuple[list, int]:
        uids_result = []
        cnt_access = 0

        # read all values from the sorted lists
        uid2dim2value = defaultdict(dict)
        for dim in range(num_dim):
            for uid, value in cls.list_sorted_entities[dim]:
                uid2dim2value[uid][dim] = value
                cnt_access += 1

        # compute the score and sort it
        uid2score = defaultdict(float)
        for uid, dim2value in uid2dim2value.items():
            list_values = []
            for dim in range(num_dim):
                list_values.append(dim2value[dim])
            score = get_score(list_values)
            uid2score[uid] = score

        sorted_uid2score = sorted(uid2score.items(), key=lambda x: -x[1])
        # print(sorted_uid2score[0:5])

        # get the top-k results
        for i in range(top_k):
            uids_result.append(sorted_uid2score[i][0])

        return uids_result, cnt_access

    # Please use random_access(uid, dim) for random access

    def Fagin(cls, num_dim, top_k) -> Tuple[list, int]:
        uids_result = []
        cnt_access = 0

        appearance_count = 0

        uid2time = defaultdict(list)
        uid2score = defaultdict(float)

        for row in range(len(cls.list_sorted_entities[0])):
            for dim in range(num_dim):
                tuple = cls.list_sorted_entities[dim][row]
                cnt_access += 1
                uid2time[tuple[0]].append(dim)
                uid2score[tuple[0]] += tuple[1]
                if (len(uid2time[tuple[0]]) == num_dim):
                    appearance_count += 1
            if (appearance_count >= top_k):
                break
        for uid, l in uid2time.items():
            if (len(l) != num_dim):
                for dim in range(num_dim):
                    if dim not in l:
                        uid2score[uid] += cls.random_access(uid, dim)
                        cnt_access += 1
        sorted_uid2score = sorted(uid2score.items(), key=lambda x: -x[1])
        for i in range(top_k):
            uids_result.append(sorted_uid2score[i][0])

        return uids_result, cnt_access

    # Please use random_access(uid, dim) for random access
    def TA(cls, num_dim, top_k) -> Tuple[list, int]:
        uids_result = []
        cnt_access = 0

        uid2access = defaultdict(list)
        uid2row = defaultdict(lambda: -1)
        score = list()
        uid2score = defaultdict(float)

        for row in range(len(cls.list_sorted_entities[0])):
            threshold = 0
            for dim in range(num_dim):
                tuple = cls.list_sorted_entities[dim][row]
                threshold += tuple[1]
                cnt_access += 1
                if uid2row[tuple[0]] == row or uid2row[tuple[0]] == -1:
                    uid2row[tuple[0]] = row
                    uid2score[tuple[0]] += tuple[1]
                    uid2access[tuple[0]].append(dim)
            for uid, ls in uid2access.items():
                if uid2row[uid] == row:
                    for dim in range(num_dim):
                        if dim not in ls:
                            uid2score[uid] += cls.random_access(uid, dim)
                            uid2access[uid].append(dim)
                            cnt_access += 1
                    score.append((uid, uid2score[uid]))
            score = sorted(score, key=lambda x: -x[1])
            if len(score) >= top_k:
                if score[top_k-1][1] >= threshold:
                    for i in range(top_k):
                        uids_result.append(score[i][0])
                    break
            if len(score) > top_k:
                del score[top_k:]

        return uids_result, cnt_access

    # You cannot use random access in this method

    def NRA(cls, num_dim, top_k) -> Tuple[list, int]:
        uids_result = []
        cnt_access = 0

        uid2lbub = defaultdict(lambda: [float(0), float(0)])
        uid2access = defaultdict(list)
        for row in range(len(cls.list_sorted_entities[0])):
            eachrow = dict()
            for dim in range(num_dim):
                tuple = cls.list_sorted_entities[dim][row]
                cnt_access += 1
                uid2access[tuple[0]].append(dim)
                uid2lbub[tuple[0]][0] += tuple[1]
                eachrow[dim] = tuple[1]
            for uid, ls in uid2access.items():
                temp_ub = uid2lbub[uid][0]
                for dim, score in eachrow.items():
                    if (dim not in ls):
                        temp_ub += score
                uid2lbub[uid][1] = temp_ub
            sorted_uid2lbub = sorted(uid2lbub.items(), key=lambda x: -x[1][0])

            if len(sorted_uid2lbub) > top_k:
                temp_sorted = max(
                    sorted_uid2lbub[top_k:], key=lambda x: x[1][1])

                if round(sorted_uid2lbub[top_k-1][1][0], 2) >= round(temp_sorted[1][1], 2):
                    for i in range(top_k):
                        uids_result.append(sorted_uid2lbub[i][0])
                    break

        return uids_result, cnt_access
