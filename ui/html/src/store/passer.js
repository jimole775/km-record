/**
 * 专门用于页面间传值，使用后注意释放变量，参考InterviewApprove.vue
 */
export default {
  state: {
    interviewVO: {},
    taskVO: {}
  },
  mutations: {
    setInterviewVO (state, interviewVO) {
      state.interviewVO = interviewVO || {}
    },
    setTaskVO (state, taskVO) {
      state.taskVO = taskVO || {}
    }
  },
  actions: {

  }
}
