import time
import cbg
import collocate


def test_collocate(case):
  if case == 0:
    reqst = cbg.yuhun('https://yys.cbg.163.com/cgi/mweb/equip/7/202007292101616-7-AVS8BKAONKILEO')
    yys = collocate.YYS(reqst)

    yys.add_type('针女', 4)
    yys.add_type('荒骷髅', 2)
    yys.add_attr('暴击', min=100)
    maps = yys.map_index(yys.types, {1, 2, 3, 4, 5, 6})
    print('maps:', maps)
    print('maps size:', len(maps))
    yuhun = yys.match(maps)
    print(yuhun)

  if case == 1:
    reqst = cbg.yuhun('https://yys.cbg.163.com/cgi/mweb/equip/7/202007292101616-7-AVS8BKAONKILEO')
    yys = collocate.YYS(reqst)

    yys.add_type('针女', 2)
    yys.add_type('荒骷髅', 2)
    yys.add_type('破势', 2)
    maps = yys.map_index(yys.types, {1, 2, 3, 4, 5, 6})
    print('maps:', maps)
    print('maps size:', len(maps))
    yuhun = yys.match(maps)
    print(yuhun)


  if case == 2:
    reqst = cbg.yuhun('https://yys.cbg.163.com/cgi/mweb/equip/7/202007292101616-7-AVS8BKAONKILEO')
    yys = collocate.YYS(reqst)

    yys.add_type('狂骨', 4)
    yys.add_type('荒骷髅', 2)
    yys.add_attr('暴击', min=88)
    yys.add_attr('速度', min=41, max=43)
    maps = yys.map_index(yys.types, {1, 2, 3, 4, 5, 6})
    print('maps:', maps)
    print('maps size:', len(maps))
    yuhun = yys.match(maps)
    print(yuhun)

  if case == 3:
    t1 = time.time()

    reqst = cbg.yuhun('https://yys.cbg.163.com/cgi/mweb/equip/7/202007292101616-7-AVS8BKAONKILEO')
    yys = collocate.YYS(reqst)

    # yys.add_type('破势', 4)
    yys.add_type('地震鲶', 2)
    # yys.add_attr('暴击', min=92)
    yys.add_attr('速度', min=54, max=55)
    maps = yys.map_index(yys.types, {1, 2, 3, 4, 5, 6})
    print('maps:', maps)
    print('maps size:', len(maps))
    yuhun = yys.match(maps)
    print(yuhun)
    t2 = time.time()

    print('total time:', t2 - t1)


if __name__ == '__main__':
  test_collocate(case=3)
