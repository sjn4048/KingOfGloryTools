# author: sjn4048@NGAbbs
# toy tool!

import random

display = True
loop_times = 1
diandao_frame_cd = 3
diandao_percentage = 0.3 


class Hero:
	name = 0
	max_hp = 0
	hp = 0
	phy_attack = 0
	phy_defense = 0
	phy_penetration = 0
	mag_attack = 0
	mag_defense = 0
	mag_penetration = 0
	crit_rate = 0
	crit_effect = 0 
	vampire_rate = 0

	
	def attack(self, name, original, target, vampire_percentage, critable, attack_type):
		if attack_type == 'phy':
			damage = original if self.phy_penetration >= target.phy_defense else original * 602 / (target.phy_defense - self.phy_penetration + 602) # 物理伤害
		elif attack_type == 'mag':
			damage = original if self.mag_penetration >= target.mag_defense else original * 602 / (target.mag_defense - self.mag_penetration + 602) # 法术伤害
		elif attack_type == 'true':
			damage = orginal # 真实伤害
		else:
			raise Exception()

		if critable and random.uniform(0,1) < self.crit_rate: # 可暴击且暴击了
			damage *= self.crit_effect

		damage = int(damage) # 取整
		target.hp -= damage

		vampire_cnt = int(damage * self.vampire_rate * vampire_percentage) # 吸血量 = 伤害量*可吸血比例*吸血率
		self.hp += vampire_cnt
		
		if display:
			print('%s\tmade %d damage to %s\t, and vampired %d\t. Name: %s' % (self.name, damage, target.name, vampire_cnt, name))
			if (target.is_dead()):
				print("%s died." % target.name)


	def __init__(self, name, max_hp, phy_attack, phy_defense, phy_penetration, mag_attack, mag_defense, mag_penetration, crit_rate, crit_effect, vampire_rate):
		self.name = name
		self.max_hp = max_hp
		self.hp = max_hp
		self.phy_attack = phy_attack
		self.phy_defense = phy_defense
		self.phy_penetration = phy_penetration
		self.mag_attack = mag_attack
		self.mag_defense = mag_defense
		self.mag_penetration = mag_penetration
		self.crit_rate = crit_rate
		self.crit_effect = crit_effect
		self.vampire_rate = vampire_rate


	def reset(self):
		self.hp = self.max_hp


	def is_dead(self):
		return self.hp <= 0
	

if __name__ == '__main__':
	# 以7级为例
	diandao = Hero(name='diandao', max_hp=4383, phy_attack=298, phy_defense=193, phy_penetration=64, mag_attack=0, mag_defense=101, mag_penetration=0, crit_rate=0.64, crit_effect=2.4, vampire_rate=0.16)
	moshi = Hero(name='moshi', max_hp=4383, phy_attack=358, phy_defense=193, phy_penetration=64, mag_attack=0, mag_defense=101, mag_penetration=0, crit_rate=0.36, crit_effect=2.4, vampire_rate=0.26)

	dd_cnt = 0
	ms_cnt = 0
	draw_cnt = 0

	for i in range(loop_times):
		diandao.reset()
		moshi.reset() # 重置体力上限
		dd_loop_cnt = 0
		ms_loop_cnt = 0
		loop_cnt = 0

		while (True):
			loop_cnt += 1
			if loop_cnt <= 3: # 前三发普攻
				diandao.attack(name='Normal A', original=320+0.5*diandao.phy_attack, target=moshi, vampire_percentage=1, critable=True, attack_type='phy') # 电刀平A
				moshi.attack(name='Normal A', original=320+0.5*moshi.phy_attack, target=diandao, vampire_percentage=1, critable=True, attack_type='phy') # 末世平A
				moshi.attack(name='Moshi effect', original=diandao.hp * 0.08, target=diandao, vampire_percentage=0, critable=False, attack_type='phy') # 末世特效
				if random.uniform(0, 1) < diandao_percentage:
					diandao.attack(name='Diandao effect', original=100+0.3*diandao.phy_attack, target=moshi, vampire_percentage=0, critable=True, attack_type='mag') # 电刀特效
			else: # 之后的三连发
				diandao.attack(name='Splitted A', original=0.4*(320+0.5*diandao.phy_attack), target=moshi, vampire_percentage=1, critable=True, attack_type='phy') # 电刀三连发A
				moshi.attack(name='Splitted A', original=0.4*(320+0.5*moshi.phy_attack), target=diandao, vampire_percentage=1, critable=True, attack_type='phy') # 末世三连发A

				if dd_loop_cnt == 0: # 电刀此刻冷却好了
					if random.uniform(0, 1) < diandao_percentage: # 电刀判定命中
						dd_loop_cnt = diandao_frame_cd - 1 # cd计数器重置
						diandao.attack(name='Diandao effect', original=100+0.3*diandao.phy_attack, target=moshi, vampire_percentage=0, critable=True, attack_type='mag') # 电刀特效
				else:
					dd_loop_cnt -= 1 # cd计数器减一

				ms_loop_cnt += 1
				if ms_loop_cnt == 3: # 每3发中2发特效
					ms_loop_cnt = 0
				else:
					moshi.attack(name='Moshi effect', original=diandao.hp * 0.08, target=diandao, vampire_percentage=0, critable=False, attack_type='phy') # 末世特效

			if diandao.is_dead() and moshi.is_dead():
				draw_cnt += 1
				break
			elif diandao.is_dead():
				ms_cnt += 1
				break
			elif moshi.is_dead():
				dd_cnt += 1
				break
			else:
				continue

	print("diandao wins: %d, moshi wins: %d, draw: %d" % (dd_cnt, ms_cnt, draw_cnt))