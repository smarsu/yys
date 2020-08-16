import cbg
from parse import *
import time
import numpy as np


class YYS:
  def __init__(self, reqst):
    self.reqst = reqst

    self.types = []
    self.attrs = []

  
  def clean(self):
    self.types = []
    self.attrs = []


  def add_type(self, type, num):
    if self._type_num_sum() + num > 6:
      return -1
    self.types.append((type, num))


  def _type_num_sum(self):
    return sum([num for _, num in self.types])


  def add_attr(self, attr, min=None, max=None):
    assert min != None or max != None
    min = min if min != None else -np.inf
    max = max if max != None else np.inf
    assert max >= min
    self.attrs.append([attr, min, max])


  def find(self, param):
    # TODO: Use database.
    pos, type = param
    res = []
    for value in self.reqst.values():
      if value['pos'] == pos:
        if type == None or value['name'] == type:
          res.append(value)
    return res


  def choose_position(self, positions, num, res, choosed_pos=None):
    assert len(positions) >= num, '{} ... {}'.format(positions, num)

    if choosed_pos == None:
      choosed_pos = []

    if num == 0:
      res.append(set(choosed_pos))
      return 

    positions = list(positions)
    for n in range(len(positions) - num + 1):
      choosed_pos.append(positions[n])
      self.choose_position(set(positions[n+1:]), num - 1, res, list(choosed_pos))
      choosed_pos.pop()


  def map_index(self, types, positions):
    if len(types) == 0:
      return [{pos: None for pos in positions}]

    num_positions = len(positions)
    type, num = types[0]
    assert num_positions >= num, '{} ... {}'.format(num_positions, num)

    res = []
    self.choose_position(positions, num, res)

    maps = []
    for choosed_pos in res:
      remain_pos = positions - choosed_pos
      map = {}
      assert len(choosed_pos) == num, '{} ... {}'.format(len(choosed_pos), num)
      for pos in choosed_pos:
        map[pos] = type

      for inner_map in self.map_index(types[1:], remain_pos):
        maps.append({**map, **inner_map})

    return maps


  def contain(self, yh, yuhun):
    for collected_yh in yuhun:
      if yh['uuid'] == collected_yh['uuid']:
        return True
    return False


  def show(self):
    time_cu = time.time()
    print('{}/{} ... {}/{}'.format(self.comp, self.prob, round(time_cu - self.time_st, 2), round((time_cu - self.time_st) / self.comp * (self.prob - self.comp), 2)))


  def collocate(self, yuhun_hub, selected_yuhun, yuhun=None):
    if yuhun == None:
      yuhun = []
    if len(yuhun_hub) == 0:
      assert len(yuhun) == 6, len(yuhun)
      attrs = self.compute(yuhun)

      self.comp += 1
      self.show()

      if self.filte(attrs):
        selected_yuhun.append(list(yuhun))
        print(len(selected_yuhun), attrs)
      return

    key = yuhun_hub[0][0]
    for idx, yh in enumerate(yuhun_hub[0][1]):
      # print(key, idx, len(yuhun_hub[0][1]))
      # if self.contain(yh, yuhun):
      #   continue

      yuhun.append(yh)
      self.collocate(yuhun_hub[1:], selected_yuhun, yuhun)
      yuhun.pop()

  
  def match(self, maps):
    self.comp = 0
    self.time_st = time.time()

    selected_yuhun = []
    yuhun_hub_list = []
    for map in maps:
      yuhun_hub = []
      for key, value in map.items():
        yuhuns = self.find((key, value))
        yuhun_hub.append((key, yuhuns))
      yuhun_hub_list.append(yuhun_hub)

    self.prob = sum([np.prod([len(yuhuns) for key, yuhuns in yuhun_hub]) for yuhun_hub in yuhun_hub_list])
    print(self.prob)

    for yuhun_hub in yuhun_hub_list: 
      print([len(yuhuns) for key, yuhuns in yuhun_hub])
      # self.collocate(yuhun_hub, selected_yuhun)
    return selected_yuhun


  def addition_attr(self, attrs_map, attr):
    attrs_map[attr[0]] += float(attr[1].replace('%', ''))


  def compute(self, yuhun):
    assert len(yuhun) == 6, len(yuhun)
    attrs_map = {attr: 0 for attr in attr2value.keys()}
    for yh in yuhun:
      if 'single_attr' in yh:
        single_attr = yh['single_attr']
        self.addition_attr(attrs_map, single_attr)
      main_attr = yh['attrs'][0]
      self.addition_attr(attrs_map, main_attr)

      for rattr, value in yh['rattr']:
        attr = rattr2attr[rattr]
        attr_value = attr2value[attr] * value
        attrs_map[attr] += attr_value

    yh_map = {}
    for yh in yuhun:
      yh_map[yh['name']] = yh_map.get(yh['name'], 0) + 1
    
    for key, value in yh_map.items():
      if value >= 2:
        if yunhuns_base_attr[key] != None:
          attrs_map[yunhuns_base_attr[key][0]] += yunhuns_base_attr[key][1]

    return attrs_map


  def filte(self, attrs):
    for attr, min, max in self.attrs:
      value = attrs[attr]
      if not (min <= value < max):
        return False
    return True

  
  def atack(self, types, attrs, reqst):
    pass
