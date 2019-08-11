<template>
  <a-locale-provider :locale="zhCN">
    <div>
      <h1>战令计算器</h1>
      <p id="deadline">S{{seasonIndex}}战令截止日期: {{toDateString(deadline)}}<br>
        距离本赛季战令截止还有{{leftWeekCnt}}周</p>
      <a-col :span="formMargin"></a-col>
      <a-col :span="24 - 2 * formMargin">
        <a-form
          :form="form"
          @submit="calc"
          style="text-align: center;"
        >
          <a-form-item
            label="当前战令等级"
            v-bind="formItemLayout"
          >
            <a-input
              v-decorator="[
                'curLv',
                {
                  rules: [{
                    required: true,
                    messageBrief: '请输入当前战令等级' }
                  ]
                }
              ]"
            >
            </a-input>
          </a-form-item>
          <a-form-item
            label="等级内部经验"
            v-bind="formItemLayout"
          >
            <a-input
              v-decorator="[
                  'curLvExp',
                  {
                    rules: [{ required: true, messageBrief: '请输入等级内部经验' }]
                  }
                ]"
            >
            </a-input>
          </a-form-item>
          <a-form-item
            label="赛季任务完成数"
            v-bind="formItemLayout"
          >
            <a-input
              v-decorator="[
                'seasonTaskFinCnt',
                  {
                    rules: [
                      {
                        required: true, messageBrief: '请输入赛季任务完成数量'
                      }
                    ]
                  }
                ]"
            >
            </a-input>
          </a-form-item>
          <a-form-item
            label="本周已刷经验"
            v-bind="formItemLayout"
          >
            <a-row>
              <a-col :span="15">
                <a-input
                  v-decorator="[
                'curWeekExp',
                {
                  rules: [{ required: false, messageBrief: '请输入本周已刷经验' }]
                }
              ]"
                  :disabled=curWeekFull
                >
                </a-input>
              </a-col>
              <a-col :span="1"></a-col>
              <a-col :span="8">
                <a-checkbox
                  @change="handleCurWeekFull"
                >
                  已满
                </a-checkbox>
              </a-col>
            </a-row>
          </a-form-item>
          <a-form-item>
            <a-checkbox
              v-decorator="[
                  'isVipUser',
                  {
                    valuePropName: 'checked',
                    initialValue: false,
                  }
                ]"
            >
              已购买进阶战令(388/1288)
            </a-checkbox>
          </a-form-item>
          <a-form-item>
            <a-button
              type="primary"
              html-type="submit"
              :compact=true
              style="width: 20%; min-width: 100px"
            >
              开始计算
            </a-button>
          </a-form-item>
        </a-form>
        <p id="result" v-if="resultStr">{{resultStr}}</p>
      </a-col>
      <a-col :span="formMargin"></a-col>
      <a-divider></a-divider>
      <a-col :xs="1" :sm="2" :md="3" :lg="4" :xl="5"></a-col>
      <a-col :xs="22" :sm="20" :md="18" :lg="16" :xl="14">
        <a-alert message="未计算开箱抽到的100/200战令经验" banner></a-alert>
        <a-alert message="默认已经打开本周的经验宝箱" banner></a-alert>
        <a-alert message="本工具默认可以完成所有赛季任务，但[累计登陆]任务可能会由于已登录天数过少而无法完成" banner></a-alert>
        <a-divider></a-divider>
        <b>如果这个程序有帮助到你，请将网址分享给你的朋友，或前往<a href="https://ngabbs.com/read.php?tid=16549128&_ff=516">NGA论坛</a>回复顶帖，让更多人看到这个工具。</b>
      </a-col>
      <a-col :xs="1" :sm="2" :md="3" :lg="4" :xl="5"></a-col>
    </div>
  </a-locale-provider>
</template>

<script>
  import global from '@/components/GlobalStyle'
  import {index, date, exp, seasonTask, level, skin} from '@/components/S16Data'
  import zhCN from 'ant-design-vue/lib/locale-provider/zh_CN'
  import {Button, LocaleProvider, Row, Col, Form, Input, Checkbox, Divider, Alert} from 'ant-design-vue'

  export default {
    name: 'Zhanling',
    components: {
      AButton: Button,
      ALocaleProvider: LocaleProvider,
      ARow: Row,
      ACol: Col,
      AForm: Form,
      AInput: Input,
      ACheckbox: Checkbox,
      ADivider: Divider,
      AAlert: Alert,
      AFormItem: Form.Item
    },
    data () {
      return {
        zhCN,
        deadline: date.END_DATE,
        formMargin: global.formMargin,
        formItemLayout: global.formItemLayout,
        currentTime: new Date(),
        resultStr: null,
        curWeekFull: false,
        leftWeekCnt: null,
        seasonIndex: index,
        loginDays: seasonTask.LOGIN_DAYS
      }
    },
    beforeCreate () {
      this.form = this.$form.createForm(this)
    },
    mounted () {
      this.leftWeekCnt = parseInt((this.deadline.getTime() - this.currentTime.getTime()) / (24 * 3600 * 1000 * 7)) + 1
    },
    methods: {
      toDateString: function (d) {
        return d.getFullYear() + '/' + (d.getMonth() + 1) + '/' + d.getDate()
      },
      handleCurWeekFull (e) {
        this.curWeekFull = e.target.checked
      },
      calc (e) {
        e.preventDefault()
        this.form.validateFields((err, values) => {
          if (!err) {
            console.log(values)
            // 表单输入数据
            // 战令等级
            const curLv = parseInt(values.curLv, 10)
            if (curLv > level.MAX_LV || curLv < 0 || isNaN(curLv)) {
              alert('当前战令等级填写错误！（范围：0-200）')
              return
            }
            // 等级内部经验
            var curLvExp = parseInt(values.curLvExp, 10)
            if (curLvExp >= exp.MAX_EXP_PER_LV || curLvExp < 0 || isNaN(curLvExp)) {
              alert('当前等级经验填写错误！（范围：0-1999）')
              return
            }

            // 赛季任务完成数量
            var seasonTaskFinCnt = parseInt(values.seasonTaskFinCnt, 10)
            if (seasonTaskFinCnt > seasonTask.SEASON_TASK_TOTAL || seasonTaskFinCnt < 0 || isNaN(seasonTaskFinCnt)) {
              alert('赛季任务完成数量填写错误！（范围：0-5）')
              return
            }

            // 是否氪金
            var isVip = values.isVipUser

            let MAX_EXP_CUR_WEEK = exp.MAX_EXP_LAST_WEEK - (this.leftWeekCnt - 1) * exp.WEEK_INCR
            console.log(MAX_EXP_CUR_WEEK)
            // 本周战令经验
            var curWeekExp = this.curWeekFull ? MAX_EXP_CUR_WEEK : parseInt(values.curWeekExp, 10)
            if (curWeekExp > MAX_EXP_CUR_WEEK || curWeekExp < 0 || isNaN(curWeekExp)) {
              alert('本周战令经验填写错误！（范围：0-' + MAX_EXP_CUR_WEEK + '）')
              return
            }

            // 进行计算
            var totalCurExp = curLv * exp.MAX_EXP_PER_LV + curLvExp // 当前总经验
            if (curWeekExp + seasonTaskFinCnt * seasonTask.SEASON_TASK_AWARD > totalCurExp) {
              alert('数据填写错误！本周经验+赛季任务经验不应大于已获得的总经验')
              return
            }
            // 剩余可以获得的普通经验
            var leftOrdinaryExp = (exp.MAX_EXP_LAST_WEEK + MAX_EXP_CUR_WEEK) / 2 * this.leftWeekCnt - curWeekExp

            // 剩余可以获得的赠送经验（进阶版），默认本周已经领取，因此不再计算本周
            var leftVipExp = ((isVip ? exp.VIP_WEEK_AWARD : 0) + exp.NORMAL_WEEK_AWARD) * (this.leftWeekCnt - 1)

            // 剩余的赛季任务经验
            var leftSeasonTaskExp = (seasonTask.SEASON_TASK_TOTAL - seasonTaskFinCnt) * seasonTask.SEASON_TASK_AWARD

            // 总的剩余经验
            var totalLeftExp = leftOrdinaryExp + leftVipExp + leftSeasonTaskExp

            // 加上已有经验之后获得总经验上限
            var afterwardsExp = totalLeftExp + totalCurExp
            var afterwardsLv = Math.floor(afterwardsExp / exp.MAX_EXP_PER_LV)
            var afterwardsLvExp = afterwardsExp % exp.MAX_EXP_PER_LV
            var resultStr = '如果刷满未来的全部战令任务+赛季任务，本赛季战令系统截止时，你将到达' + afterwardsLv + '级+' + afterwardsLvExp + '经验。\n'
            if (!isVip) {
              resultStr += '如果现在买 388战令，可以到达' + (this.leftWeekCnt + afterwardsLv) + '级。\n如果现在买1288战令，可以到达' + (level.BONUS_LEVEL_1288 + this.leftWeekCnt + afterwardsLv) + '级。\n'
            }

            if (curLv < skin.SECOND_SKIN_LEVEL) { // 还没拿到战令皮，计算还要多久
              var targetExp = skin.SECOND_SKIN_LEVEL * exp.MAX_EXP_PER_LV
              if (isVip) { // 是进阶版的情况
                let leftExp = targetExp - totalCurExp - leftSeasonTaskExp - (MAX_EXP_CUR_WEEK - curWeekExp)
                if (leftExp < 0) {
                  resultStr += '再加把劲，这星期你就可以拿到战令皮了！\n'
                } else {
                  // 解一元二次方程ax^2+bx+c=0
                  let a = exp.WEEK_INCR / 2
                  let b = exp.WEEK_INCR / 2 + MAX_EXP_CUR_WEEK + exp.VIP_WEEK_AWARD
                  let c = -leftExp
                  let delta = b * b - 4 * a * c
                  let res = Math.ceil(-b / (2 * a) + Math.sqrt(delta) / (2 * a))
                  if (res < this.leftWeekCnt) { // 不氪金就拿得到
                    var earliestDate = new Date(this.currentTime)
                    earliestDate.setDate(earliestDate.getDate() + (7 - earliestDate.getDay()) % 7 + (res - 1) * 7 + 1)
                    resultStr += '你距离80级战令皮肤还剩' + res + '周的时间~(' + this.toDateString(earliestDate) + ')\n'
                  } else {
                    let mustBuyExp = targetExp - afterwardsExp
                    let dq = Math.ceil(mustBuyExp / exp.MAX_EXP_PER_LV) * level.MONEY_PER_LEVEL
                    resultStr += '按照现在的进度，你必须要刷满所有经验且氪金' + dq + '点券才有可能在截止前拿到战令皮肤。\n'
                  }
                }
              }
            }
            this.resultStr = resultStr
          } else {
            console.log(err)
          }
        })
      }
    }
  }
</script>
