from gmun_tests.settings import LINE_STORAGE_PATH
import os.path


def f(success_count_limit, count_limit, result, filename):
    if result:
            try:
                call=0

                if not os.path.isfile(f'{LINE_STORAGE_PATH}\\{filename}'):
                    with open(f"{LINE_STORAGE_PATH}\\{filename}", 'w') as f:
                        a = "0"
                        i = 0
                        while i < count_limit-1:
                            i += 1
                            a += ", 0"
                        a = f"[{a}]"
                        f.write(a)

                with open(f"{LINE_STORAGE_PATH}\\{filename}", 'r') as f:
                    l = f.readline().rstrip()[1:-1].replace(",", "").replace(" ", "")
                    m = []
                    for i in l:
                        m.append(int(i))
                    line = m

                if result.find('fail') != -1:
                    line.insert(0, 1)
                else:
                    line.insert(0, 0)
                line.pop()

                sum_rest = 0
                for i in line[success_count_limit:]:
                    sum_rest += i

                sum_count = 0
                i = 0
                while i <= success_count_limit - 1:
                    sum_count = sum_count + line[i]
                    i += 1

                trig = 0
                if sum_rest == 0 and sum_count == success_count_limit:
                    trig = 1

                with open(f"{LINE_STORAGE_PATH}\\{filename}", 'w') as f:
                    f.write(str(line))

                return trig

            except Exception as e:
                print("ошибка в modules.pars_line.f ", e)


if __name__ == '__main__':
    filename = '222.txt'
    result = "fail"
    success_count_limit = 4
    count_limit = 15
    trig = f(success_count_limit, count_limit, result, filename)
    print(trig)
