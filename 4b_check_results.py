import os
import glob
import matplotlib.pyplot as plt
import numpy as np
config = __import__('0_config')


def check_param_topic(k=8):
    print('Plot Analysis')
    print('')
    results = glob.glob(os.path.join(config.OUTPUT_FOLDER, 'topics') + '/*.txt')
    parsed_data = {}
    for r in results:
        vals = r[:r.rfind('.')].split('_')
        section = vals[0]
        section = section[section.rfind('/')+1:]
        if section not in parsed_data:
            parsed_data[section] = []

        t = {}
        for v in vals:
            key = ''
            if v.startswith('cu'):
                key = 'cu'
            elif v.startswith('cv'):
                key = 'cv'
            elif v.startswith('topics'):
                key = 'topics'

            if key != '':
                t[key] = float(v.split(':')[1])
        parsed_data[section].append(t)

    parsed_data = {section:sorted(parsed_data_, key=lambda t: int(t['topics'])) for section, parsed_data_ in parsed_data.items()}
    num_topics = {section:[int(t['topics']) for t in parsed_data_] for section, parsed_data_ in parsed_data.items()}
    x = range(min([min(v) for v in num_topics.values()]), max([max(v) for v in num_topics.values()]) + 1)
    for i, (section, parsed_data_) in enumerate(parsed_data.items()):
        print('{} best in Section {}'.format(k, section))
        print('cv')
        for t in sorted(parsed_data_, key=lambda x:-x['cv'])[:k]:
            print('\t', t)
        print('cu')
        for t in sorted(parsed_data_, key=lambda x:-x['cu'])[:k]:
            print('\t', t)
        print('')

        cu = [float(t['cu']) for t in parsed_data_]
        cv = [float(t['cv']) for t in parsed_data_]
        idx_max_cu, max_cu = np.argmax(cu) + min(num_topics[section]), max(cu)
        idx_max_cv, max_cv = np.argmax(cv) + min(num_topics[section]), max(cv)

        plt.figure(i+1)
        plt.legend('Section ' + str(section))
        plt.title('Section ' + str(section))
        plt.suptitle('Section ' + str(section))
        plt.subplot(211)
        plt.plot(x, cv, 'b')
        plt.plot(idx_max_cv, max_cv, 'ro')
        plt.legend(('c_v', 'best c_v ({})'.format(idx_max_cv)), loc='best')
        plt.xlabel('number of topics')
        plt.ylabel('Coherence score (CV)')
        plt.xticks(np.arange(min(x) - 1, max(x) + 1, 5.0))

        plt.subplot(212)
        plt.plot(x, cu, 'r')
        plt.plot(idx_max_cu, max_cu, 'bo')
        plt.legend(('c_u', 'best c_u ({})'.format(idx_max_cu)), loc='best')
        plt.xlabel('number of topics')
        plt.ylabel('Coherence score (CU)')
        plt.xticks(np.arange(min(x) - 1, max(x) + 1, 5.0))

        plt.draw()
    plt.show()
    print('')
    print('')
    print('')


def check_tuning(k=10):
    print('Tuning analysis')
    print('')
    results = glob.glob(os.path.join(config.OUTPUT_FOLDER, 'tuning') + '/*.txt')
    parsed_data = {}
    for r in results:
        vals = r[:r.rfind('.')].split('_')
        section = vals[0]
        section = section[section.rfind('/') + 1:]
        t = {k:v for k,v in [v.split(':') for v in vals if ':' in v]}

        if section not in parsed_data:
            parsed_data[section] = []
        parsed_data[section].append(t)

    parsed_data_sorted_by_cu = {section:sorted(parsed_data_, key=lambda x:-float(x['cu'])) for section, parsed_data_ in parsed_data.items()}
    parsed_data_sorted_by_cv = {section:sorted(parsed_data_, key=lambda x:-float(x['cv'])) for section, parsed_data_ in parsed_data.items()}

    for section in parsed_data.keys():
        print('Section {}'.format(section))
        for i, (cu, cv) in enumerate(zip(parsed_data_sorted_by_cu[section][:k], parsed_data_sorted_by_cv[section][:k])):
            cu_sorted = sorted(cu.items(), key=lambda x:x[0])
            cv_sorted = sorted(cv.items(), key=lambda x:x[0])

            print('Best #{} (cu, cv)'.format(i+1))
            for a, b in zip(cu_sorted, cv_sorted):
                assert a[0] == b[0]
                print('\t', '\t', a[0], '\t', '\t', round(a[1], 4) if not isinstance(a[1], str) else a[1], '\t', '\t', round(b[1], 4) if not isinstance(b[1], str) else b[1])
    print('')
    print('')
    print('')


if __name__ == "__main__":
    check_param_topic()
    check_tuning()
