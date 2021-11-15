import Vue from "vue"
const TokenKey = 'OMSToken'
const JumpKey = 'OMSJump'

export function getToken () {
  const data = Vue.localStorage.getItem(TokenKey)
  return  data || ' '
}

export function setToken (token) {
  Vue.localStorage.setItem(TokenKey, token)
}

export function removeToken () {
  return Vue.localStorage.removeItem(TokenKey)
}

export function setOMSJump (omsjump) {
  Vue.localStorage.setItem(JumpKey, omsjump)
}

export function getOMSJump () {
  const data = Vue.localStorage.getItem(JumpKey)
  return  data || ' '
}

export function removeOMSJump () {
  return Vue.localStorage.removeItem(JumpKey)
}
