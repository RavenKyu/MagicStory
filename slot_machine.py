__author__ = 'raven'
import random
import numpy

class Slots(object):
	def __init__(self, slot_n=3*3):
		self.slot_number = slot_n
		self.default_value = 11


		self.grade = [x / 11 for x in range(1,self.default_value + 1)]
		grade_sum = sum(self.grade)
		self.grade = [x / grade_sum * 1.0 for x in self.grade]
		self.grade.reverse()

		self.item = [x for x in range(1,self.default_value + 1)]

	@staticmethod
	def random_pick(some_list, probabilities):
		x = random.uniform(0, 1)
		cumulative_probability = 0.0
		for item, item_probability in zip(some_list, probabilities):
			cumulative_probability += item_probability
			if x < cumulative_probability: break
		return item

	def get_random_pick(self):
		slot = list()
		for i in range(self.slot_number):
			slot.append(self.random_pick(self.item, self.grade))
		return slot




class MachineSlots(object):
	def __init__(self):
		self._slots = list()
		self.s = Slots()

		# self 변수 초기화
		self.bet_lines = set()

		# Slot 초기화
		self.init_machine()

	def init_machine(self):
		self.bet_lines = set()

	def _roll_up(self):
		self._slots = self.s.get_random_pick()

	def _bet_up(self, n: int):
		self.bet_lines = set()
		line_numbers = [x for x in range(1, n + 1)]
		self.bet_lines ^= set(line_numbers)

	def get_matched_item(self):
		LINE = {
			1: [3, 4, 5], 2: [0, 1, 2],
			3: [6, 7, 8], 4: [0, 4, 8],
			5: [2, 4, 6], 6: [0, 3, 6],
			7: [1, 4, 7], 8: [2, 5, 8]
		}

		matched_number = list()
		matched_line = list()
		for bl in list(self.bet_lines):
			if not self._slots[LINE[bl][0]] == self._slots[LINE[bl][1]]:
				continue
			if not self._slots[LINE[bl][1]] == self._slots[LINE[bl][2]]:
				continue
			matched_number.append(self._slots[LINE[bl][0]])
			matched_line.append(bl)
		return {"matched_number": matched_number, "matched_line": matched_line}

	def get_slots(self):
		return self._slots





class MachineView(object):
	emoji = {
		1: "\U0001F352",  # 체리
		2: "\U0001F95D",  # 키위
		3: "\U0001F347",  # 포도
		4: "\U0001F3B2",  # 주사위

		5: "\U0001F4B0",  # 돈뭉치
		6: "\U0001F48E",  # 다이아
		7: "\U0001F381",  # 선물상

		8: "\U0001F949",  # 동메달
		9: "\U0001F948",  # 은메달
		10: "\U0001F947",  # 금메달

		11: "\U0001F3C6",  # 트로피
	}

	def __init__(self, slot=None):
		self._slot_data = slot

	def paint(self):
		slot = " | \ | / |\n".join([u"{:^3s}-{:^3s}-{:^3s}\n"] * 3)
		print(slot.format(*[self.emoji[x] for x in self._slot_data.get_slots()]))


class Machine(object):
	ODD = {1: 2, 2: 20, 3: 40, 4: 50, 5: 100, 6: 200, 7: 500, 8: 500, 9:500, 10: 500, 11:1000}

	def __init__(self):
		self.slot = MachineSlots()
		self.view = MachineView(self.slot)
		self._coin = 250
		self.bet = 8

	def run(self):
		win_number = {x: 0 for x in range(1, 12)}
		game_cnt = 0
		win_cnt = 0
		self.slot._bet_up(self.bet)

		while True:

			# cmd = input("%d :: %s>> " % (self._coin, str(self.slot.bet_lines)))
			# if 'c' == cmd:
			# 	self._coin += 20
			# 	continue

			self._coin -= self.bet
			self.slot._roll_up()
			game_cnt += 1
			matched_info = self.slot.get_matched_item()

			# 	self._coin += sum([self.bet * self.ODD[x] for x in matched_info["matched_number"]])
			for n in matched_info["matched_number"]:
				win_number[n] += 1
				win_cnt += 1

			if game_cnt == 100000:
				print("GAMES: %d\tWIN: %d\tW/G: %.2f" % (game_cnt, win_cnt, win_cnt / game_cnt * 1.0))
				a = ["%s: %d (%.2f%%)" % (self.view.emoji[x], win_number[x], win_number[x]/win_cnt * 100.0) for x in win_number.keys() if x]
				print(", ".join(a))

				with open("data.txt", "a") as f:
					a = ["%d" % (win_number[x]) for x in win_number.keys() if x]
					print(", ".join(a))

				break

			# self.view.paint()


if __name__ == "__main__":
	s = Machine()
	s.run()



