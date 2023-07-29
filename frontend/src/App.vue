<template>
  <div class="flex background-blue" @keyup.ctrl.enter="addArea" @keyup.ctrl.backspace="resetForm"
    @keyup.ctrl.\="submitForm">
    <div class="flex-grow-1">
      <div v-for="e in inputCount" class="w-45% my-10 ml-30vw">
        <a-card class="border-#d9d9d9">
          <div class="flex">
            <h1 class="align-top mt-0 mr-10">{{ e % 2 === 1 ? 'Q' : 'A' }}</h1>
            <a-textarea v-model:value="inputValue[e - 1]" placeholder="请输入" :auto-size="{ minRows: 5, maxRows: 8 }"
              class="mr-10" ref="areaRef" @keydown.tab.prevent="tabDown($event)" />
          </div>
        </a-card>
      </div>
    </div>
    <a-card class="w-550px mt-20 border-#d9d9d9">
      <h4 class="text-center mb-8">策略选择</h4>
      <a-form :model="formSettings" :label-col="labelCol" :wrapper-col="wrapperCol" class="w-80% mx-auto mb-10">
        <a-form-item label="对话主题">
          <a-input v-model:value="formSettings.title" class="w-80% ml-5" placeholder="可选项" />
        </a-form-item>
        <a-form-item label="数据作者">
          <a-input v-model:value="formSettings.author" class="w-80% ml-5" placeholder="可选项" />
        </a-form-item>
        <a-form-item label="轮次上限">
          <a-input v-model:value="formSettings.maxTurns" type="textarea" class="w-80% ml-5" />
        </a-form-item>
        <a-form-item label="首轮增强">
          <a-radio-group v-model:value="formSettings.firstAugmentation" button-style="solid" class="ml-5">
            <a-radio-button :value="true">开启</a-radio-button>
            <a-radio-button :value="false">关闭</a-radio-button>
          </a-radio-group>
        </a-form-item>
        <a-form-item label="开启配置">
          <a-switch v-model:checked="formSettings.enable" class="ml-5" />
        </a-form-item>
        <a-form-item label="增强范围">
          <a-radio-group v-model:value="formSettings.scope" :disabled="formSettings.enable ? false : true" class="ml-5">
            <a-radio value="question">仅问句</a-radio>
            <a-radio value="all">问&答句</a-radio>
          </a-radio-group>
        </a-form-item>
        <a-form-item label="增强策略">
          <a-checkbox-group v-model:value="formSettings.strategy" :disabled="formSettings.enable ? false : true"
            class="w-80% ml-5">
            <a-checkbox value="homoPhones">同音字替换</a-checkbox>
            <a-checkbox value="equivalentChar">等价字替换</a-checkbox>
            <a-checkbox value="characterDelete">随机字删除</a-checkbox>
            <a-checkbox value="characterExchange">邻近字换序</a-checkbox>
            <a-checkbox value="similarWord">同义词替换</a-checkbox>
            <a-checkbox value="randomWord">实体词替换</a-checkbox>
          </a-checkbox-group>
        </a-form-item>
        <a-form-item label="增强数量">
          <a-slider v-model:value="formSettings.count" :min="1" :max="6" :disabled="formSettings.enable ? false : true"
            class="ml-5" />
        </a-form-item>
        <a-form-item label="改变概率">
          <a-slider v-model:value="formSettings.changeRate" :min="0.1" :max="0.9" :step="0.1"
            :disabled="formSettings.enable ? false : true" class="ml-5" />
        </a-form-item>
      </a-form>
      <a-divider />
      <div class="mt-10">
        <h4 class="text-center">快捷键</h4>
        <ul class="ml-30 mt-3 spacey-10">
          <li>ctrl+enter <span class="ml-15">新建对话框</span></li>
          <li>ctrl+backspace <span class="ml-7">刷新重做</span></li>
          <li>ctrl+\ <span class="ml-22">提交结果</span></li>
        </ul>
      </div>
      <div class="text-center spacex-45 mt-25">
        <a-button @click="resetForm">重做</a-button>
        <a-button type="primary" @click="submitForm">提交</a-button>
      </div>
    </a-card>
  </div>
</template>
<script setup>
import { ref, reactive, toRaw, onMounted, watch, nextTick } from 'vue'
import { notification } from 'ant-design-vue'
import axios from 'axios'

const inputCount = ref(1)

const inputValue = reactive([''])
const areaRef = ref(null)

onMounted(() => {
  areaRef.value[0].focus()
})

const showMsg = (type, msg) => {
  notification[type]({
    message: msg,
    duration: 2.5
  })
}

// 阻止 tab 键失去焦点
const tabDown = (event) => {
  // 获取当前光标位置
  const pos = event.target.selectionStart
  const inputValue = event.target.value
  // 在当前光标位置插入制表符
  const newValue = inputValue.substring(0, pos) + '\t' + inputValue.substring(pos)
  event.target.value = newValue
  // 更新光标位置
  event.target.selectionEnd = pos + 1
}

const addArea = () => {
  if (inputValue.length >= 2 * formSettings.maxTurns) {
    showMsg('warning', '已达轮次上限')
    return
  }
  inputValue.push('')
  inputCount.value += 1
  nextTick(() => {
    areaRef.value[inputCount.value - 1].focus()
  })
}

const formSettings = reactive({
  title: '',
  author: '',
  maxTurns: 3,
  enable: false,
  scope: 'question',
  strategy: [],
  count: 1,
  changeRate: 0.3,
  firstAugmentation: false
})

// 更新保存用户设置
if (sessionStorage.getItem('formSettings')) {
  Object.assign(formSettings, JSON.parse(sessionStorage.getItem('formSettings')))
}

watch(formSettings, () => {
  sessionStorage.setItem('formSettings', JSON.stringify(formSettings))
})

const resetForm = () => {
  location.reload()
}

// 提交前检查
const checkVaild = () => {
  for (let v of inputValue) {
    if (v.trim() === '') {
      showMsg('error', '对话不能为空')
      return false
    }
  }
  if (inputValue.length % 2) {
    showMsg('error', '对话不能以问句结尾')
    return false
  }
  if (formSettings.enable && !formSettings.strategy.length) {
    showMsg('error', '请配置增强策略或关闭配置')
    return false
  }
  return true
}

const submitForm = () => {
  if (checkVaild()) {
    // 去掉每行的结尾的空格和制表符
    const text = toRaw(inputValue)
      .map(item => item.trim())
      .map(item => item.split('\n').map(line => line.trim()).join('\n'))
    axios.post('/req/handle-dialog', {
      settings: formSettings,
      dialog: text
    }).then(() => {
      showMsg('success', '提交成功')
    }).catch(err => {
      if (err.response && err.response.status === 500) {
        showMsg('error', '后端未开启或出现错误')
      } else {
        showMsg('error', `其他错误：${err}`)
      }
    })
  }
}
</script>