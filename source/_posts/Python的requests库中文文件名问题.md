title: Python的requests库中文文件名问题
date: 2016-09-23 19:39:06
tags:
    - Python
    - requests
categories:
---
在使用requests库时，遇到中文文件名问题，现象如下

如果是英文文件名，body中的内容为
```
Content-Disposition: form-data; name="document"; filename="my.doc"
```

如果是中文文件名，body中的内容为
```
Content-Disposition: form-data; name="document"; filename*=utf-8''03%E7%BD%91%E7%AB%99%E5%A4%87%E6%A1%88%E4%BF%A1%E6%81%AF%E7%9C%9F%E5%AE%9E%E6%80%A7%E6%8F%90%E4%BE%9B%E7%94%B5%E5%AD%90%E7%89%88%E6%89%AB%E6%8F%8F%E4%BB%B6.doc
```

查看requests的源码，从request.post一路跟踪，进入session.request, 进入 session.prepare_request, 进入PreparedRequest.prepare, 进入进入PreparedRequest.prepare_body, 进入PreparedRequest._encode_files, 进入RequestField.make_multipart, 进入RequestField._render_parts, 进入RequestField._render_part,最后进入RequestField.format_header_param方法, 内容如下 
```
def format_header_param(name, value):
    """
    Helper function to format and quote a single header parameter.

    Particularly useful for header parameters which might contain
    non-ASCII values, like file names. This follows RFC 2231, as
    suggested by RFC 2388 Section 4.4.

    :param name:
        The name of the parameter, a string expected to be ASCII only.
    :param value:
        The value of the parameter, provided as a unicode string.
    """
    if not any(ch in value for ch in '"\\\r\n'):
        result = '%s="%s"' % (name, value)
        try:
            result.encode('ascii')
        except UnicodeEncodeError:
            pass
        else:
            return result
    if not six.PY3:  # Python 2:
        value = value.encode('utf-8')
    value = email.utils.encode_rfc2231(value, 'utf-8')
    value = '%s*=%s' % (name, value)
    return value
```
这里明确说明文件名只能是ascii, 于是只好将文件名urlencode一下，使用urllib将文件对象的名字修改后，例如假设document是一个文件对象, 可以进行如下修改
```
f = {'document': (urllib.quote(document.name.encode('utf-8')), document, document.content_type)}
response = requests.post(UPLOAD_DOCUMENT_URL + "?access_token=%s" % access_token,  files=f, data=params)
```

参考资料:
* [Python requests post中文文件名问题](http://www.guoguoday.com/post/Python-requests-post%E4%B8%AD%E6%96%87%E6%96%87%E4%BB%B6%E5%90%8D%E9%97%AE%E9%A2%98/)
