
const TokenKey = 'OMSToken'
const JumpKey = 'OMSJump'

export function getToken () {
  return localStorage[TokenKey] || ' '
}

export function setToken (token) {
  localStorage[TokenKey] = token
}

export function removeToken () {
  return delete localStorage[TokenKey]
}

export function setOMSJump (omsjump) {
  localStorage[JumpKey] = omsjump
}

export function getOMSJump () {
  return localStorage[JumpKey] || ' '
}

export function removeOMSJump () {
  return delete localStorage[JumpKey]
}
