const httpHost = "http://localhost";
function getFormCustomConfigCode(){  
	let formCustomConfig = `
	const {file, util, okCb, errCb} = CUSTOM_ARG
	const param = new FormData()
	param.append('file', file)
	util.axios.post(httpHost+'/api/upload', param, {
	  headers: { 'Content-Type': 'multipart/form-data' }
	}).then(res => {
	  okCb(res.url)
	}).catch(err => {
	  errCb(err)
	})`
	return formCustomConfig;
}