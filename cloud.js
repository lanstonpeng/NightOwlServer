var AV = require('leanengine');
var qiniu = require('qiniu');

qiniu.conf.ACCESS_KEY = 'ETRZmSoIoK-VUPMXBwNLF89xjLUM8qNEp8gIB4HQ';
qiniu.conf.SECRET_KEY = 'fIvu13JBUbWhQ5FetU-v5aLlVuT5HePap0ZnSu0q';

/**
 * 一个简单的云代码方法
 */
AV.Cloud.define('hello', function(request, response) {
  response.success('youku');
});

AV.Cloud.define('get_token', function(request, response) {
    var putPolicy = new qiniu.rs.PutPolicy("nightowl");
    response.success(putPolicy.token() );
});

module.exports = AV.Cloud;
