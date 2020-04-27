const index = 19

const date = {
  START_DATE: new Date(2020, 2, 31, 0, 0, 0),
  END_DATE: new Date(2020, 5, 21, 23, 59, 59)
}

const exp = {
  MAX_EXP_PER_LV: 2000,
  MAX_EXP_FIRST_WEEK: 13600,
  VIP_WEEK_AWARD: 2000,
  NORMAL_WEEK_AWARD: 1000,
  WEEK_INCR: 700
}

const seasonTask = {
  SEASON_TASK_TOTAL: 5,
  SEASON_TASK_AWARD: 3500,
  LOGIN_DAYS: 30
}

const level = {
  MAX_LV: 200,
  BONUS_LEVEL_1288: 30,
  MONEY_PER_LEVEL: 80
}

const awards = {
  FIRST_AWARD_NAME: '刘邦·夺宝奇兵',
  FIRST_AWARD_LEVEL: 1,
  SECOND_AWARD_NAME: '阿轲·银河之约',
  SECOND_AWARD_LEVEL: 80,
  THIRD_AWARD_NAME: '拖尾特效·蒸蒸日上',
  THIRD_AWARD_LEVEL: 120
}

export {
  index, date, exp, seasonTask, level, awards
}
