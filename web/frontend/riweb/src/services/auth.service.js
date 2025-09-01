import  Api  from "./Api";

export default{
  //should return userId, token, tenantCode
  login(userId, password, tenantCode){
    return Api().post('/token',{
        "user_id": userId,
        "password" : password,
        "tenant_code": tenantCode
    }).then((response) => {
      return response.data
    }).catch((error) => {
      throw error
    })
  },

  refreshTokens(refreshToken){
    const user = JSON.parse(localStorage.getItem('user'))
    return Api().post('/refresh',{
      "token_type":"refresh token",
      "token": refreshToken,
      "user_name": user.user_name
    }).then((response) => {
      return response.data
    }).catch((error) => {
      throw error
    })
  },

  verifyToken(){
    return Api().get('/verify').then((response) => {
      return response.data
    }).catch((error) => {
      throw error
    })
  },
}
