import pandas as pd
import numpy as np

outcomeSpace = {'r1': ['r2', 'r3', 'r4', 'r7'],
                'r2': ['r1', 'r4', 'r3', 'r8'],
                'r3': ['r1', 'r7', 'r2', 'c1'],
                'r4': ['r2', 'r8', 'r9', 'r1'],
                'r5': ['r6', 'r9', 'c3', 'r10', 'r11', 'r13', 'r15',
                       'r16', 'r17', 'r18', 'r19', 'r20', 'r21', 'o1'],
                'r6': ['r5', 'c3', 'r9', 'r10', 'r11', 'r15',
                       'r16', 'r17', 'r18', 'r19', 'r20', 'r21', 'o1'],
                'r7': ['r3', 'c1', 'r1', 'r25', 'c2'],
                'r8': ['r4', 'r9', 'r2', 'r5', 'r13'],
                'r9': ['r5', 'r8', 'r13'],
                'r10': ['c3', 'r5', 'r6', 'r11', 'r15', 'r16', 'r17', 'r18', 'r19', 'r20', 'r21', 'o1'],
                'r11': ['c3', 'r5', 'r6', 'r10', 'r15', 'r16', 'r17', 'r18', 'r19', 'r20', 'r21', 'o1'],
                'r12': ['r22', 'r25', 'outside'],
                'r13': ['r9', 'r24', 'r5', 'r8', 'r14', 'r23'],
                'r14': ['r24', 'r13', 'r23'],
                'r15': ['c3', 'r5', 'r6', 'r10', 'r11', 'r16', 'r17', 'r18', 'r19', 'r20', 'r21', 'o1'],
                'r16': ['c3', 'r5', 'r6', 'r10', 'r11', 'r15', 'r17', 'r18', 'r19', 'r20', 'r21', 'o1'],
                'r17': ['c3', 'r5', 'r6', 'r10', 'r11', 'r15', 'r16', 'r18', 'r19', 'r20', 'r21', 'o1'],
                'r18': ['c3', 'r5', 'r6', 'r10', 'r11', 'r15', 'r16', 'r17', 'r19', 'r20', 'r21', 'o1'],
                'r19': ['c3', 'r5', 'r6', 'r10', 'r11', 'r15', 'r16', 'r17', 'r18', 'r20', 'r21', 'o1'],
                'r20': ['c3', 'r5', 'r6', 'r10', 'r11', 'r15', 'r16', 'r17', 'r18', 'r19', 'r21', 'o1'],
                'r21': ['c3', 'r5', 'r6', 'r10', 'r11', 'r15', 'r16', 'r17', 'r18', 'r19', 'r20', 'o1'],
                'r22': ['r12', 'r25', 'r26', 'c1', 'outside'],
                'r23': ['r24', 'r13', 'r14'],
                'r24': ['r9', 'r13', 'r14', 'r23'],
                'r25': ['r22', 'r26', 'c1', 'r12', 'r27', 'r7', 'c2'],
                'r26': ['r25', 'r27', 'r22', 'c1', 'r32'],
                'r27': ['r26', 'r32', 'r25', 'r31', 'r33'],
                'r28': ['c4', 'r29', 'r35', 'c2', 'o1'],
                'r29': ['r30', 'c4', 'r28', 'r35', 'c2', 'o1'],
                'r30': ['r29', 'c4'],
                'r31': ['r32', 'r27', 'r33'],
                'r32': ['r27', 'r31', 'r33', 'r26'],
                'r33': ['r32', 'r27', 'r31'],
                'r34': ['c2', 'c1', 'c4'],
                'r35': ['c4', 'r28', 'r29', 'c2', 'o1'],
                'c1': ['r7', 'c2', 'r25', 'r3', 'r34', 'c4', 'r22', 'r26'],
                'c2': ['r34', 'c1', 'c4', 'r7', 'r25', 'r28', 'r29', 'r35', 'o1'],
                'c3': ['r5', 'r6', 'r10', 'r11', 'r15', 'r16', 'r17', 'r18', 'r19',
                       'r20', 'r21', 'o1', 'r9', 'c4'],
                'c4': ['r28', 'r29', 'r35', 'c2', 'o1', 'r30', 'r34', 'c1', 'c3'],
                'o1': ['c3', 'c4', 'r5', 'r6', 'r10', 'r11', 'r15', 'r16', 'r17', 'r18',
                       'r19', 'r20', 'r21', 'r28', 'r29', 'r35', 'c2'],
                'outside': ['r12', 'r22']
                }

def get_out_probability_for_room(data, room):
    d = list(data[room])
    change_sum = 0
    if sum(d) == 0:
        return 0
    for i in range(len(d) - 1):
        change = int(d[i]) - int(d[i + 1])
        if change > 0:
            change_sum += change
    return change_sum / sum(d)

if __name__ == "__main__":
    #index is the dictionary, key is the space and value is the corresponding index number.
    index = {}
    start = 0
    for key in outcomeSpace.keys():
        index[key] = start
        start+=1

    data = pd.read_csv('data.csv')
    output = {}
    
    data_partial_info = [(data[0:2279], '_s1'), (data[2279:], '_s2')]
    
    for data_partial in data_partial_info:
        for key in outcomeSpace.keys():
            room_in_out_info = [0] * len(outcomeSpace.keys())
            #count the possiblity of moving to other rooms
            for i in range(len(data_partial[0])-1):
                data_now = data_partial[0].iloc[i]
                data_next = data_partial[0].iloc[i+1]
                
                # Here it indicates that someone has left this rooms
                if int(data_next[key]) < int(data_now[key]):
                    diff = int(data_now[key]) - int(data_next[key])
                    
                    # Get different rooms change data
                    rooms_people_diffs = data_next[outcomeSpace.keys()] - data_now[outcomeSpace.keys()]
                    rooms_people_diffs = dict(rooms_people_diffs)
                    rooms_people_diffs = {k: v for k, v in sorted(rooms_people_diffs.items(), key=lambda item: item[1], reverse=True)}
                    
                    for room in rooms_people_diffs.keys():
                        if rooms_people_diffs[room] >= diff:
                            room_in_out_info[index[room]] += diff
                            break
                        else:
                            if rooms_people_diffs[room] > 0:
                                room_in_out_info[index[room]] += rooms_people_diffs[room]
                                diff -= rooms_people_diffs[room]
            key_data = list(data_partial[0][key])
            if sum(key_data) != 0:
                room_in_out_info = [x/sum(key_data) for x in room_in_out_info]
            room_in_out_info[index[key]] = 1 - get_out_probability_for_room(data_partial[0], key)
            output[key+data_partial[1]] = room_in_out_info

    out_csv = pd.DataFrame(output)
    out_csv.to_csv('tran_matrix.csv',index=False)
