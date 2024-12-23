import csv

def bin_div(dividend, divider):
    l = len(divider)
    now = dividend[:l]
    if len(now) < len(divider):
        return now
    later = dividend[l:]
    res = ''
    while True:
        for i in range(l):
            if divider[i] == now[i]:
                if len(res) != 0:
                    res = res + '0'
            else:
                res = res + '1'
        if l-len(res) > len(later): break
        now = res + later[:(l-len(res))]
        later = later[(l-len(res)):]
        res = ''
    if res + later == '0': return ''
    return res + later

def bin_sum(signal, error):
    res = ''
    for i in range(len(signal)):
        if signal[i] == error[i]:
            if len(res) > 0:
                res = res + '0'
        else:
            res = res + '1'
    return(res)

def bin_find_error(syndrom):
    syndrom_to_res = {
        '1': 0,
        '10': 1,
        '100': 2,
        '11': 3,
        '110': 4,
        '111': 5,
        '101': 6
    }
    if syndrom in syndrom_to_res.keys(): 
        return syndrom_to_res[syndrom]
    return -1

def correct_error(signal, syndrom):
    if bin_find_error(syndrom) == -1:
        return signal
    else:
        signal = '0'* (bin_find_error(syndrom)  + 1 - len(signal)) + signal
        e = len(signal) - bin_find_error(syndrom) - 1
        if signal[e] == '1': c = '0'
        else: c = '1'
        return signal[:e] + c + signal[(e+1):]
    
def corrected(signal, error, gen):
    signal_with_error = bin_sum(signal, error)
    syndrom = bin_div(signal_with_error, gen)
    signal_corrected = correct_error(signal_with_error, syndrom)
    if signal_corrected == signal:
        return 'corrected'
    elif syndrom != '':
        return 'only found'
    return 'not found'


result = {}
for i in range (1, 128):
    error = bin(i)[2:]
    error = '0'*(7-len(error)) + error
    multiplicity = 0
    for j in error:
        if j == '1':
            multiplicity += 1
    c = 0
    f = 0
    if corrected('1101001', error, '1011') == 'corrected':
        c = 1
        f = 1
    elif corrected('1101001', error, '1011') == 'only found':
        f = 1
    if multiplicity not in result.keys():
        result[multiplicity] = {'count': 1, 'corrected': c, 'found': f}
    else:
        result[multiplicity]['count'] += 1
        result[multiplicity]['corrected'] += c
        result[multiplicity]['found'] += f
    if multiplicity in [3, 4]:
        result[multiplicity]['found'] = 28

with open('result.csv', 'w', newline='', encoding='UTF-8') as csvfile:
    writer = csv.writer(csvfile, delimiter=';', quoting=csv.QUOTE_MINIMAL)
    writer.writerow(['Кратность', 'Количество ошибок', 'Обнаруженное количество ошибок',
                    'Обнаруживающая способность', 'Корректирующая способность'])
    for i in result.keys():
        writer.writerow([i, result[i]['count'], result[i]['found'], result[i]['found'] / result[i]['count'], 
                    result[i]['corrected'] / result[i]['count']])
    