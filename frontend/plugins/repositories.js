import createRepository from '~/repositories/Repository'

export default (ctx, inject) => {
  const api = ctx.$axios.create({
    headers: {
      common: {
        'x-bb-channelid': 'WEB',
      },
    },
  })

  api.interceptors.request.use(function (config) {
    config.headers.Authorization = `Bearer ${
      ctx.$cookies.get('user').userToken
    }`

    return config
  })

  inject('repositories', createRepository(api))
}
